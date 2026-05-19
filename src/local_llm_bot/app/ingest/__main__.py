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

# Version: 1.2.0
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

    print("--- Ingest result", file=_sys.stderr)
    print(f"✅ {result.files_processed} files ingested · {result.chunks_written:,} chunks · {dur_str}", file=_sys.stderr)
    print(f"· config     : chunk_size={result.chunk_size:,} · overlap={result.overlap} · model={result.embed_model}", file=_sys.stderr)
    print(f"· avg        : {avg_chunks:,.0f} chunks/file · {avg_secs:.1f}s/file", file=_sys.stderr)
    if size_line:
        print(size_line, file=_sys.stderr)
    print(failure_line, file=_sys.stderr)

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
            # All hits — show source breakdown
            if len(_norm_by_source) == 1:
                _src_label = f"source: {list(_norm_by_source.keys())[0]}"
            elif _norm_by_source:
                _src_label = "source: " + " · ".join(f"{v} {k}" for k, v in sorted(_norm_by_source.items()))
            else:
                _src_label = "source: tag"
            print(f"✅ {_n_hits}/{_n_markup} markup files augmented · {_src_label}", file=_sys.stderr)
        else:
            print(f"· {_n_hits}/{_n_markup} markup files augmented · {_n_misses} no structured header detected", file=_sys.stderr)
        if _year_missing > 0 and _year_missing == _n_hits:
            print("· prefix     : [Document: <entity>] — year tag absent in all files, filename year used", file=_sys.stderr)
        elif _year_missing > 0:
            print(f"· prefix     : [Document: <entity> FY<year>] · ⚠ {_year_missing} files missing year tag", file=_sys.stderr)
        else:
            print("· prefix     : [Document: <entity> FY<year>]", file=_sys.stderr)
        if _entities:
            _entity_list = " · ".join(sorted(_entities))
            print(f"· entities   : {_entity_list}", file=_sys.stderr)
        if _n_mm > 0:
            print(f"· ⚠ {_n_mm} entity mismatch warning{'s' if _n_mm > 1 else ''} — entity did not match filename stem", file=_sys.stderr)

    # ── JSON payload → stdout (always — consumed by api.py _capture_stdout) ──
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
    print(json.dumps(payload))

    if args.verbose:
        print("", file=_sys.stderr)
        print(json.dumps(payload, indent=2), file=_sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
