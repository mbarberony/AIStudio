from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict
from pathlib import Path

from local_llm_bot.app.config import CONFIG
from local_llm_bot.app.ingest.pipeline import ingest_corpus
from local_llm_bot.app.utils.corpus_paths import corpus_paths
from local_llm_bot.app.utils.repo_root import find_repo_root

# Version: 1.3.5
# Changelog: 1.3.5 — AIStudio_912 (Manuel CLI signature change, 2026-06-14): --files help text
#            updated to describe OR-matched literal-substring / regex patterns (matching logic
#            lives in pipeline.py v1.8.32 _selective_match). No parse change here — still one
#            comma-separated string → only_files set; pipeline does the matching.
#            1.3.4 — AIStudio_909 (Manuel CLI-output flag C): entities and File Ingested rosters
#            right-aligned in a field sized to the largest index (numbers stay right-aligned,
#            the `*` shares the field), so the text column is stable and the two sibling lists
#            align. Was: entities at "  {i:>2}." and files at 4-space "    *" (text aligned but
#            markers/indent inconsistent).
#            1.3.3 — AIStudio_909 (flag #5): the ingest summary now ends with a "· File Ingested:"
#            files written this run as indented `* <basename>` bullets (no path, no "source:"
#            prefix, no trailing comma). Replaces eyeballing /debug/retrieve for "what landed."
#            1.3.2 — AIStudio_909 (Manuel CLI-output flag #3): dropped the manual print("")
#            blank-line separator before the "✅ N files ingested" summary. pipeline.py closes the
#            Process bar with p_process.clear() (v1.8.31), already leaving the cursor on a fresh
#            line, so the separator only produced a gratuitous blank line. NEEDS LIVE VERIFY.
# Version: 1.3.1
# Changelog: 1.3.1 — AIStudio_906: reset the corpus_metadata `files`/`deleted_files` maps on a
#            full rebuild (--force, whole corpus) before the per-file merge. The writer only
#            added the files ingested this run and never cleared prior entries, so a --force
#            rebuild of a 22-file corpus that previously held a contaminated 109-file set left
#            all 109 in the map — and the UI file count / data volume / entity list read this
#            map, showing 109 phantom files. Selective (--files A,B) runs still merge. (Item
#            number provisional — reconcile at PIPELINE update with the 891 collision + the
#            SESS-2026-06-09 905-912 earmarks.)
# Changelog: 1.3.0 — AIStudio: per-file selective ingest. New --files arg (comma-separated
#            basenames) → passed to ingest_corpus(only_files=...). When present, ONLY those
#            files are ingested and always re-embedded; all other files under --root are
#            untouched. Enables "index one file at a time" and honest reingest-N denominators.
# Changelog: 1.2.5 — Normalizer summary source label updated to match pipeline
#            completion line format: "tag(s) [ns:]" not "tag (ns:)".
# Changelog: 1.2.4 — Write file_stats to corpus_metadata.yaml unconditionally
#            in __main__.py. Previously relied on api.py subprocess path which
#            never fires when ais_ingest_esef.sh calls pipeline directly (TTY).
#            Writes: file_type, size_bytes, chunks, duration_sec, ingested_at,
#            normalizer_entity/year/source/mismatch, avg_seconds_per_file.
# Changelog: 1.2.3 — Remove spurious f prefix from entities label print (F541).
# Changelog: 1.2.2 — Remove "--- Ingest result" section header per STD §8 update:
#            summary flows directly after completion lines as closing ✅ of ▶.
#            Entities formatted as numbered list (one per line) not inline ·.
# Changelog: 1.2.1 — AIStudio_722: config line format fixed (chunk size: not chunk_size=
#            per STD §8 summary rules). JSON payload TTY-gated: only emits to stdout
#            when stdout is a pipe (api.py subprocess), not operator terminal.
# Changelog: 1.2.0 — Fix stdout/stderr split: human-readable summary → stderr.
#            JSON payload → stdout unconditionally (parsed by api.py _capture_stdout
#            to populate file_stats in corpus_metadata.yaml). Previously JSON was
#            gated on --verbose so files: {} in corpus_metadata was always empty.
#            Normalizer summary improved: source breakdown when mixed, entity list
#            alphabetical, year-absent note when year missing, mismatch warning.
#            --verbose now prints pretty JSON to stderr for operator inspection.
# Changelog: 1.1.0 — AIStudio_675: normalizer summary section added.


def _repo_root() -> Path:
    return find_repo_root(Path(__file__))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m local_llm_bot.app.ingest")
    p.add_argument("--corpus", default="default", help="Corpus name (under data/corpora/)")
    p.add_argument("--root", required=True, help="Directory to ingest (recursive)")

    # Reset / incremental controls
    p.add_argument(
        "--reset-index", action="store_true", help="Reset JSONL artifacts for this corpus"
    )
    p.add_argument(
        "--force", action="store_true", help="Force reprocessing even if manifest shows unchanged"
    )

    # CLI overrides
    p.add_argument("--chunk-size", type=int, default=None, help="Override chunk size (chars)")
    p.add_argument("--overlap", type=int, default=None, help="Override overlap (chars)")
    p.add_argument("--embed-model", default=None, help="Override embedding model")
    p.add_argument("--max-files", type=int, default=None, help="Safety cap for a run")
    p.add_argument(
        "--files",
        default=None,
        help=(
            "Comma-separated list of patterns selecting which files to ingest exclusively. "
            "Each pattern is OR-matched against the basename, case-insensitively: a literal "
            "substring, or a regex if it contains regex metacharacters (* + ? [ ] ( ) | ^ $ "
            "{ } \\). So '--files BlackRock' selects BlackRock_10K_*.htm, and "
            "'--files JPM.*2025,Citi' selects either. When given, ONLY matched files are "
            "processed and always re-embedded; every other file under --root (indexed or "
            "parked) is left untouched. Omit to ingest the whole corpus."
        ),
    )
    p.add_argument("--verbose", action="store_true", help="Print full JSON result payload after summary")

    args = p.parse_args(argv)

    corpus = str(args.corpus).strip()
    root = Path(args.root).expanduser()
    if not root.exists():
        raise SystemExit(f"Path not found: {root}")
    if not root.is_dir():
        raise SystemExit(f"--root must be a directory: {root}")

    # Provide tqdm to pipeline (pipeline will create multiple progress bars)
    try:
        from tqdm import tqdm  # type: ignore
    except Exception:
        tqdm = None  # type: ignore

    repo = _repo_root()
    paths = corpus_paths(repo, corpus)

    # Parse --files allowlist (comma-separated basenames). Empty/blank → None (whole corpus).
    only_files: set[str] | None = None
    if args.files:
        only_files = {n.strip() for n in str(args.files).split(",") if n.strip()}
        if not only_files:
            only_files = None

    t0 = time.time()
    result = ingest_corpus(
        root=root,
        corpus=corpus,
        reset_index=bool(args.reset_index),
        force=bool(args.force),
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        embed_model=args.embed_model,
        max_files=args.max_files,
        only_files=only_files,
        tqdm_cls=tqdm,  # <-- key change: pipeline controls bars
    )
    dur = time.time() - t0

    import sys as _sys

    # ── Human-readable summary → stderr ─────────────────────────────────────
    # stderr = operator-visible stream (same as tqdm). stdout = JSON for api.py.
    mins, secs = divmod(int(dur), 60)
    dur_str = f"{mins}m {secs}s" if mins else f"{secs}s"
    avg_chunks = result.chunks_written / result.files_processed if result.files_processed else 0
    avg_secs = dur / result.files_processed if result.files_processed else 0
    avg_ms_chunk = (dur * 1000) / result.chunks_written if result.chunks_written else 0

    file_stats = result.file_stats or {}
    if file_stats:
        sorted_files = sorted(file_stats.items(), key=lambda x: x[1].get("chunks", 0))
        smallest = sorted_files[0]
        largest = sorted_files[-1]
        size_line = (
            f"· largest    : {largest[0]} ({largest[1].get('chunks', 0):,} chunks)\n"
            f"· smallest   : {smallest[0]} ({smallest[1].get('chunks', 0):,} chunks)"
        )
    else:
        size_line = ""

    failures = result.files_failed or 0
    failure_line = f"· ⚠ failures : {failures}" if failures else "· failures   : 0"

    # STD §8: ✅ echoes the ▶ action line subject — no section header needed.
    # No manual blank-line separator: pipeline.py closes the Process bar with p_process.clear()
    # (v1.8.31), which already leaves the cursor at column 0 of a fresh line, so the summary
    # prints directly under the last per-file completion line. The prior print("") here injected
    # a gratuitous blank line between them (Manuel flag #3, AIStudio_909). In pipe mode the
    # completion line is already newline-terminated, so dropping the separator is safe there too.
    print(f"✅ {result.files_processed} files ingested · {result.chunks_written:,} chunks · {dur_str}", file=_sys.stderr)
    print(f"· config     : chunk size: {result.chunk_size:,} · overlap: {result.overlap} · model: {result.embed_model}", file=_sys.stderr)
    print(f"· avg        : {avg_chunks:,.0f} chunks/file · {avg_secs:.1f}s/file · {avg_ms_chunk:.0f}ms/chunk", file=_sys.stderr)
    if size_line:
        print(size_line, file=_sys.stderr)
    print(failure_line, file=_sys.stderr)
    # File Ingested roster (Manuel flag #5 / AIStudio_909): a clean, de-duplicated list of the
    # files written THIS run — basenames only, indented `*` bullets, no "source:" prefix and no
    # trailing comma (replaces eyeballing /debug/retrieve). file_stats keys are this run's files.
    if file_stats:
        print("· File Ingested:", file=_sys.stderr)
        _files = sorted(file_stats)
        _fw = len(str(len(_files)))  # STD §9: marker field sized to the largest index
        for _fname in _files:
            print(f"  {'*':>{_fw + 1}} {_fname}", file=_sys.stderr)

    # ── Normalizer summary → stderr ──────────────────────────────────────────
    _n_hits = getattr(result, "normalizer_hits", 0)
    _n_misses = getattr(result, "normalizer_misses", 0)
    _n_mm = getattr(result, "normalizer_mismatches", 0)
    _n_markup = _n_hits + _n_misses
    # Collect per-file normalizer data from file_stats for entity list + source breakdown
    _norm_by_source: dict[str, int] = {}
    _entities: list[str] = []
    _year_missing = 0
    for _fname, _fdata in file_stats.items():
        _src = _fdata.get("normalizer_source", "")
        _ent = _fdata.get("normalizer_entity", "")
        _yr = _fdata.get("normalizer_year", "")
        if _src:
            _norm_by_source[_src] = _norm_by_source.get(_src, 0) + 1
        if _ent:
            _entities.append(_ent)
            if not _yr:
                _year_missing += 1

    if _n_markup > 0:
        print("--- Normalizer", file=_sys.stderr)
        if _n_hits == _n_markup:
            # All hits — show source breakdown using the tag format from pipeline
            # _norm_by_source keys are now "tag [ns:]" or "tag(s) [ns1:, ns2:]"
            if len(_norm_by_source) == 1:
                _src_label = list(_norm_by_source.keys())[0]
            elif _norm_by_source:
                _src_label = " · ".join(f"{v}× {k}" for k, v in sorted(_norm_by_source.items()))
            else:
                _src_label = "tag"
            print(f"✅ {_n_hits}/{_n_markup} markup files augmented · source: {_src_label}", file=_sys.stderr)
        else:
            print(f"· {_n_hits}/{_n_markup} markup files augmented · {_n_misses} no structured header detected", file=_sys.stderr)
        if _year_missing > 0 and _year_missing == _n_hits:
            print("· prefix     : [Document: <entity>] — year tag absent in all files, filename year used", file=_sys.stderr)
        elif _year_missing > 0:
            print(f"· prefix     : [Document: <entity> FY<year>] · ⚠ {_year_missing} files missing year tag", file=_sys.stderr)
        else:
            print("· prefix     : [Document: <entity> FY<year>]", file=_sys.stderr)
        if _entities:
            # STD §8: unique entities only, sorted, deduplicated case-insensitively
            _seen: set[str] = set()
            _unique_entities: list[str] = []
            for _e in sorted(_entities):
                if _e.lower() not in _seen:
                    _seen.add(_e.lower())
                    _unique_entities.append(_e)
            print("· entities   :", file=_sys.stderr)
            _ew = len(str(len(_unique_entities)))  # STD §9: marker field sized to the largest index
            for _i, _ent in enumerate(_unique_entities, 1):
                print(f"  {_i:>{_ew}}. {_ent}", file=_sys.stderr)
        if _n_mm > 0:
            print(f"· ⚠ {_n_mm} entity mismatch warning{'s' if _n_mm > 1 else ''} — entity did not match filename stem", file=_sys.stderr)

    # ── Write file_stats to corpus_metadata.yaml unconditionally ───────────────
    # This must happen regardless of TTY — metadata persistence is not optional.
    # api.py also writes this when orchestrating ingest via subprocess, but when
    # ais_ingest_esef.sh calls the pipeline directly (TTY), api.py is not involved.
    # __main__.py is the canonical writer for operator-invoked ingests.
    import yaml as _yaml_meta  # type: ignore

    try:
        _repo_path = _repo_root()
        _meta_path = _repo_path / "data" / "corpora" / corpus / f"{corpus}_corpus_metadata.yaml"
        if _meta_path.exists():
            with open(_meta_path) as _mf:
                _meta = _yaml_meta.safe_load(_mf) or {}
        else:
            _meta = {"corpus_name": corpus, "schema_version": "1.0"}

        # Top-level stats
        _meta["last_ingested_at"] = _dt_now = __import__("datetime").datetime.now().isoformat(timespec="seconds")
        _meta["last_updated"] = __import__("datetime").date.today().isoformat()
        _meta["ingest_duration_seconds"] = round(dur, 2)
        _meta["last_ingest_chunks"] = result.chunks_written
        _meta["last_ingest_files"] = result.files_processed
        if result.files_processed > 0:
            _meta["avg_seconds_per_file"] = round(dur / result.files_processed, 2)
        if "schema_version" not in _meta:
            _meta["schema_version"] = "1.0"
        if "files" not in _meta or not isinstance(_meta.get("files"), dict):
            _meta["files"] = {}
        if "deleted_files" not in _meta or not isinstance(_meta.get("deleted_files"), dict):
            _meta["deleted_files"] = {}

        # AIStudio_906: a full rebuild REPLACES the files map; incremental/selective runs MERGE.
        # The per-file loop below only adds/overwrites the files ingested this run — it never
        # clears stale entries. Without this reset, a `--force` whole-corpus rebuild leaves
        # prior-run entries behind (the 109-vs-22 phantom-file bug the UI surfaced). A selective
        # `--files A,B` run (only_files set) must still merge, so it is explicitly excluded.
        if bool(args.force) and only_files is None:
            _meta["files"] = {}
            _meta["deleted_files"] = {}

        # Per-file stats
        _file_type_map = {
            ".xhtml": "ESEF iXBRL", ".htm": "SEC XBRL", ".html": "SEC XBRL",
            ".pdf": "PDF", ".md": "Markdown", ".txt": "Text",
            ".docx": "Word", ".xlsx": "Excel",
        }
        for _fname, _fdata in file_stats.items():
            _ext = Path(_fname).suffix.lower()
            _meta["files"][_fname] = {
                "file_type": _file_type_map.get(_ext, _ext.lstrip(".").upper()),
                "size_bytes": _fdata.get("size_bytes", 0),
                "chunks": _fdata.get("chunks", 0),
                "duration_sec": _fdata.get("duration_sec", 0),
                "ingested_at": _fdata.get("ingested_at", _dt_now),
                "normalizer_entity": _fdata.get("normalizer_entity", ""),
                "normalizer_year": _fdata.get("normalizer_year", ""),
                "normalizer_source": _fdata.get("normalizer_source", ""),
                "normalizer_mismatch": _fdata.get("normalizer_mismatch", False),
            }

        with open(_meta_path, "w") as _mf:
            _mf.write(f"# {corpus}_corpus_metadata.yaml\n")
            _yaml_meta.dump(dict(_meta), _mf, allow_unicode=True, default_flow_style=False, sort_keys=False)
    except Exception as _me:
        print(f"⚠ Could not write corpus metadata: {_me}", file=_sys.stderr)

    # ── JSON payload → stdout (pipe only — consumed by api.py _capture_stdout) ──
    # AIStudio_722a — TTY-gate: emit JSON only when stdout is a pipe (api.py subprocess).
    # When operator runs ais_ingest directly in terminal, raw JSON dumped to terminal
    # is noise. The human-readable summary above is sufficient for operator use.
    payload = {
        "action": "ingest",
        "corpus": corpus,
        "root": str(root),
        "duration_sec": round(dur, 3),
        "effective_config": {
            "chunk_size": result.chunk_size,
            "overlap": result.overlap,
            "embed_model": result.embed_model,
            "default_model": CONFIG.rag.default_model,
        },
        "paths": {k: str(v) for k, v in paths.items()},
        "result": asdict(result),
    }
    if not _sys.stdout.isatty():
        print(json.dumps(payload))

    if args.verbose:
        print("", file=_sys.stderr)
        print(json.dumps(payload, indent=2), file=_sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
