# Version: 1.8.34
# Changelog: 1.8.34 — AIS_12 follow-up: capped bar at {bar:20} so timing (elapsed/remaining/avg) sits right after the bar, not pushed to the far-right edge of a wide terminal by the unsized {bar}. Prior step:
#            created with fixed ncols=130 + {bar:40}; the rendered line (label + long filename +
#            bar:40 + elapsed/remaining/avg) ran ~130-135 cols, so on a narrower terminal it
#            WRAPPED and tqdm's \r could only clear the current visual row — leaving every prior
#            frame behind (the "wall of repeated lines", and 0%-looking partial frames). 1.8.33 switched
#            to dynamic_ncols=True (auto-fit terminal, re-detect on resize — matching the existing
#            comment) and {bar:20} (tqdm sizes the bar to remaining width) in all bar_format strings,
#            so the line never exceeds terminal width and \r overwrites cleanly. Render-only; no
#            change to n/total/timing math. NEEDS LIVE VERIFY (tqdm rendering is untestable in CI).
# Version: 1.8.32
# Changelog: 1.8.32 — AIStudio_912 (Manuel CLI signature change, 2026-06-14): --files tokens are
#            now OR-matched against basenames — each token is a literal substring, or a regex if it
#            contains regex metacharacters (* + ? [ ] ( ) | ^ $ { } \). New _selective_match() helper;
#            the only_files filter at discovery no longer requires an exact basename match. Covers
#            every ais_ingest_<corpus> (shared engine). Backward compatible: an exact filename still
#            matches as its own literal substring.
# Version: 1.8.31
# Changelog: 1.8.31 — Ingest-status freeze fix (source side). Gate the live tqdm Process bar
#            on _sys.stderr.isatty() (line ~894) so it renders ONLY in an operator TTY, not
#            under api.py's pipe. __main__.py passes tqdm_cls unconditionally ("pipeline
#            controls bars") but pipeline never applied the TTY gate, so the bar was created in
#            pipe mode; routing the [ingest] file_complete:/normalizer: machine signals through
#            pbar.write() while that bar was live did NOT reliably flush them to the pipe, so
#            api.py's _stream_stderr received no per-file progress — files_processed/elapsed
#            stayed 0 and the UI bar crawled (endpoint Qdrant-overlay only) then froze. With no
#            bar in pipe mode, _tqdm_write falls to plain print(file=_sys.stderr): newline-
#            terminated and (PYTHONUNBUFFERED=1) flushed immediately → the signals arrive and the
#            api.py 1.10.1 parser updates progress live. p_process=None is the existing else
#            path (917), already handled throughout. Cross-ref AIStudio_613 (file_complete
#            signal), AIStudio_722 (TTY-noise gate this completes). PIPELINE item to file at EOS
#            (provisional — reconcile with the 891 / SESS-2026-06-09 905-912 number collision).
# Changelog: 1.8.30 — AIStudio_907 (display-only): two progress/log aesthetics. (1) Intra-file
#            interpolation-thread ETA collapsed to ~00:00 mid-file — it computed
#            `t_remaining_est - _el + …` where `_el = now - t0` is total-elapsed-since-INGEST
#            (not within-file) subtracted from a file-start duration, going negative → max(0)=0.
#            Now driven off the bar's true global fraction (the % is correct) × observed overall
#            rate, matching the per-file-completion formula; can't pin to 0 while progress<total.
#            `t_remaining_est` param now vestigial. (2) `_prefix_label` in the completion line
#            omitted the alias suffix, so the log understated the stored prefix; now mirrors the
#            stored `[Document: <entity> | <aliases> FY<year>]` (also visually confirms the
#            AIStudio_895 enrichment binding is live). Provisional item number — reconcile at
#            PIPELINE update.
# Changelog: 1.8.29 — AIStudio_891: stamp `firm` = doc_entity (the normalizer entity, same
#             value used in the [Document:] prefix) into every chunk's Qdrant payload, so
#             _build_entity_filter's intended firm-match clause fires — corpus-agnostic entity
#             isolation keyed on the chunk's own entity, not source_path/filename. Pairs with
#             qdrant_store.py v1.3.1 (firm TEXT index). Requires re-ingest (payload written at
#             ingest; pre-existing chunks carry no firm).
# Changelog: 1.8.27 — AIStudio_801: ingest-time alias injection into [Document:] prefix.
#            _load_ks_alias_map() reads gleif_{corpus}_*_entities.yaml and returns
#            canonical → [wikidata_label, wikidata_short_name, wikidata_tickers] map.
#            Loaded once per ingest run. When doc_entity matches a known entity,
#            prefix becomes "[Document: CANONICAL | scope_name | ticker FY year]".
#            Format-driven (XBRL tag extraction must succeed) — not corpus-dependent.
#            Graceful no-op when no knowledge sources exist for the corpus.
# Changelog: 1.8.28 — AIStudio: per-file selective ingest. ingest_corpus() accepts
#            only_files: set[str]|None. When provided, the discovered list is filtered
#            to exactly those basenames after Phase 1 discovery, so all totals/denominators
#            reflect only the chosen files; every other file under root (already-indexed or
#            parked-but-unchosen) is left untouched. Selected files bypass the Qdrant skip
#            check (only_files active ⇒ always re-embed them). chunk_id is deterministic
#            (abs_path::page::chunk-i) so re-embed overwrites in place — no duplicates.
# Changelog: 1.8.26 — prior version.
# Changelog: 1.8.26 — Fix _extract_document_metadata() early-exit returns: 5-tuple
#            → 7-tuple (None, None appended for doc_tag/doc_year_tag). Fixes
#            ValueError unpacking for all non-markup files (PDF, DOCX, MD, etc.).
#            AIStudio_736.
# Changelog: 1.8.8 — Plain tqdm, no subclass. bar_format mutated per-file via
#            p_process.bar_format = f"  {n} of {T} · {pct}|{bar:20}| {elapsed}<{remaining}"
#            tqdm native {elapsed}/{remaining} supply timing. Chunk-based total.
#            dynamic_ncols=True auto-detects terminal width (no parasitic box).
#            No {desc} in bar_format — eliminates ": " desc_pad artifact.
#            update(_file_chunks) for smooth chunk-based fill per file.
# Changelog: 1.8.7 — Definitive bar overhaul. tqdm subclass _NoColonTqdm suppresses
#            ": " desc_pad artifact. Chunk-based total (D_SEED * supported_bytes).
#            All set_postfix_str/set_postfix replaced with set_description carrying
#            full "N of T · elapsed · remaining · avg" label. update(file_chunks)
#            for smooth chunk-based fill. ncols=None auto-detects terminal width.
#            Completion lines indented 2 spaces to align under ▶ Ingesting "I".
# Changelog: 1.8.4 — Bar fixes: move brackets to bar_format (removes leading comma
#            from set_postfix_str). Remove p_process.update(1) for unsupported files
#            (fixes 100% at file 8 and spurious 10/None tick). Add compact XBRL tag
#            name to source field: "tag (ifrs-full:)" / "tag (dei:)".
#            _extract_document_metadata() returns 6-tuple (adds tag_name).
# Changelog: 1.8.3 — AIStudio_722: CLI terminal output fixes.
#            (a) TTY-gate [ingest] normalizer: and [ingest] file_complete: lines —
#            these machine signals now only emit when stderr is a pipe (api.py subprocess),
#            not when running in an operator TTY. Fixes noisy terminal output.
#            (b) Pre-compute _total_supported before loop — fixes "1 of 1", "2 of 2"
#            denominator bug. files_supported incremented during loop; _total_supported
#            is fixed. N-of-T in activity + completion lines now correct from file 1.
#            (c) Fix tqdm bar format: bar_format now starts with "Process:" label + bar,
#            not {desc}, eliminating the "size: 16,005,771: : 20%" double-colon artifact.
#            Activity line lives in set_description() only (description-only, no bar).
#            Postfix brackets in set_postfix_str() not bar_format (avoids leading comma).
#            avg unit changed to s/file (per prescription) from ms/chunk.
#            (d) prefix: [brackets] not "quotes" in completion lines per STD §8.
# Changelog: 1.8.2 — AIStudio_721: normalize entity string in _extract_document_metadata()
#            before return. XBRL source documents contain \u00a0 (non-breaking space),
#            \u200b (zero-width space), \ufeff (BOM) in entity name tags. These corrupt
#            the [Document: entity FY year] prefix and break BM25 tokenization in alias
#            map. Fix: replace \u00a0 → space, strip zero-width/BOM, NFC normalize,
#            collapse multiple spaces. Affects all HTML/XHTML corpora (SEC + ESEF).
#            XML year tag absent (ESEF DateOfEndOfReportingPeriod2013 + DEI FiscalYear).
#            ESEF year tag value is YYYY-MM-DD — extract first 4 chars.
#            AIStudio_707: use files_supported (not len(discovered)) as N-of-T total
#            in completion lines — eliminates phantom +1 from unsupported files in dir.
#            Normalizer fields (entity, year, source, mismatch) stored in file_stats
#            for __main__.py summary entity list + source breakdown.
#            tqdm bar_format fixed: {bar:20} explicit width renders fill characters.
# Changelog: 1.8.0 — AIStudio_675 + AIStudio_680 + AIStudio_697.
#            (675) STD §8 completion line per file: N of T · filename · size · chunks · format · prefix · source · ⚠ warnings.
#            (680) Emit structured [ingest] normalizer: stderr line per file for api.py parsing → UI SSE stream.
#            (697) Fix normalizer guard: add .xhtml to suffix check so ESEF files reach normalizer.
#            Normalizer summary added to IngestResult (normalizer_hits, normalizer_misses, normalizer_mismatches).
#            tqdm activity line (set_description) updated per-file with current filename + format detected.
# Changelog: 1.7.9 — AIStudio_700: rename top-level `import re` → `import re as _re`; remove all late re imports; replace re./_re2. with _re. throughout. Fixes ruff F823 false positive permanently.
# Changelog: 1.7.7 — Fix I001: blank line between stdlib and third-party imports. Fix import block ordering per isort convention.
# Changelog: 1.7.6 — Move re and bs4 imports to top-level (fixes persistent I001/E402 lint). No late imports needed — bs4 is always available in the venv.
# Changelog: 1.7.5 — Fix I001 noqa on first line of late import blocks (block-level suppression).
# Changelog: 1.7.4 — Fix I001 import order in late imports: bs4 before re (alphabetical).
# Changelog: 1.7.3 — Lint fixes: SIM102 combine nested if statements (4 instances);
#             I001 noqa annotations for intentional late imports of re + BeautifulSoup
#             inside try blocks (E402/I001 — late import is correct pattern here,
#             avoids loading BeautifulSoup for non-HTML files).
# Changelog: 1.7.2 — Bug fix: company_prefixes NameError — initialized outside
#            Strategy 1b block so mismatch detection can reference it even when
#            entity found via Strategy 1a. Was silently swallowed by except clause
#            causing all files to return (None, None, None, None, False).
# Changelog: 1.7.1 — Bug fixes: (1) _tqdm_write argument order reversed (pbar, msg)
#            (2) ZeroDivisionError on _chunks_per_sec when first file too fast.
# Changelog: 1.7.0 — AIStudio_682: Merge _extract_document_head() and
#            _extract_fiscal_year() into single _extract_document_metadata()
#            returning (entity, year, format, strategy, mismatch). Single
#            BeautifulSoup parse per file — eliminates duplicate DOM parse.
#            AIStudio_675: emit per-file [normalizer] message via _tqdm_write
#            showing format detected, entity+year extracted, strategy used,
#            and mismatch warning when company namespace prefix doesn't match
#            filename stem.
# Changelog: 1.6.9 — AIStudio_673: Replace tqdm EMA rate/remaining with exact
#            calculation from true elapsed time and file count. True avg =
#            elapsed / files_done; true remaining = (total - done) × true_avg.
#            Also Option A bar_format: "[elapsed: HH:MM · remaining: ~HH:MM · avg: Xs/file]".
#            EMA was misleading — fluctuated 15→12s/file as file sizes varied while
#            true average was stable at ~18s/file.
# Changelog: 1.6.8 — AIStudio_674: Temporal Context Injection. New function
#            _extract_fiscal_year() extracts dei:DocumentFiscalYearFocus from inline
#            XBRL files — the SEC-mandated 4-digit fiscal year tag, always present in
#            10-K filings. When both entity and year are extracted, chunk prefix becomes
#            "[Document: <entity> FY<year>]" instead of "[Document: <entity>]". This
#            makes temporal trend queries precise at K=5 — chunks from different filing
#            years are now distinguishable in vector space. Year extraction is a no-op
#            when dei:DocumentFiscalYearFocus is absent (non-XBRL files unchanged).
# Changelog: 1.6.7 — AIStudio_640: Fix Strategy 1b visible text scan. Skip single-word
#            section headers, Exhibit references, and known document structure phrases
#            before matching entity names. Require 2+ words for ALL-CAPS candidates.
#            Add Title-Case + entity-suffix matching. Fixes BNY Mellon extraction
#            (was hitting 'FINANCIAL SECTION' before entity name).
# Changelog: 1.6.6 — AIStudio_640: Replace Strategy 1b ticker-in-text heuristic with
#            visible text entity scan. Ticker approach was too fragile (short tickers like
#            'bk' and 'ab' appear as substrings of common words). New approach: scan visible
#            HTML elements for first string matching legal entity name pattern (ALL-CAPS or
#            Title-Case multi-word), filtering generic section header words. Works for any
#            inline XBRL file regardless of ticker length or filing format.
# Changelog: 1.6.5 — AIStudio_640: Add Strategy 1b — company-specific XBRL namespace
#            prefix extraction. Every inline XBRL filing has exactly one company-specific
#            namespace prefix (the filer stock ticker: wfc, bk, aig, ab...). When
#            dei:EntityRegistrantName is absent (older filing formats), find the ticker
#            prefix then search visible HTML text for a matching string. Strips trailing
#            footnote superscripts. Handles corrupt files correctly (returns None rather
#            than contaminating with wrong entity). Covers all inline XBRL filing formats
#            without filename or corpus dependency.
# Changelog: 1.6.4 — AIStudio_640: Fix Strategy 1 false-positive namespace detection.
#            Previously detected namespace presence via any dei: tag, then looked for
#            dei:EntityRegistrantName separately — causing BNY Mellon and Wells Fargo
#            (older filings with dei:AuditorName but no dei:EntityRegistrantName) to
#            fall through to Strategy 2 on XBRL-noise text. Fix: check for the entity
#            tag directly. Added filename fallback for HTM files with no registry tag
#            match: parse stem up to filing-type marker (_10K_, _20F_ etc) and convert
#            underscores to spaces. Also removed now-unused lambda from namespace loop.
# Changelog: 1.6.3 — Fix two lint errors: UP037 unquote type annotation; B023 lambda
#            closure bug in namespace detection loop.
# Changelog: 1.6.1 — AIStudio_640: Rewrote _extract_document_head with XML namespace
#            registry architecture. Strategy 1 now detects inline XBRL (SEC, ESEF) and
#            other domain-specific XML formats via namespace prefix detection, then extracts
#            the mandatory entity identifier tag (dei:EntityRegistrantName for SEC filings).
#            Format-driven not corpus-driven — generalizes to any regulatory filing format.
#            Added file_path parameter to enable raw HTML parsing. Strategy 2 (Title-Case
#            text scan) retained as fallback for non-HTML documents.
# Changelog: 1.6.0 — AIStudio_640: Document-Head Extraction normalizer initial implementation.
# Changelog: 1.5.0 — AIStudio_613: unconditional per-file [ingest] file_complete: emit so api.py async stderr iterator receives newline-terminated progress signal. Was conditional on `p_process is None` (tqdm bar absent), which suppressed the signal in the production path where the bar IS active. _tqdm_write routes through pbar.write() preserving bar cleanliness. New line shape: "[ingest] file_complete: N/M chunks=C bytes=B file=NAME" — parseable by api.py for files_processed/chunks_written/bytes_processed/d_observed updates.
# Changelog: 1.4.0 — Same line as before (no functional change at this version pin — historical)
# Changelog: 1.3.5 — fixed tqdm ncols=100 to keep stats adjacent to bar
#            1.3.4 — suppress [ingest] log lines when tqdm bar active
#            1.3.3 — remove tqdm postfix clutter; bar shows progress only
#            1.3.2 — tqdm.write() for clean progress bars; remove noisy Discover bar
#            1.3.1 — fix datetime.UTC → timezone.utc (AttributeError on Python 3.13)
#            1.3.0 — Per-file timing, chunk count, size_bytes captured in IngestResult.file_stats
#            1.2.0 — Per-file embed+upsert (constant memory, live Qdrant progress); alphabetical file order
#            1.1.0 — MD5 stored in Qdrant payload; skip logic fixed (Qdrant-only); per-file INFO logging
from __future__ import annotations

import contextlib
import hashlib
import json
import os as _os
import re as _re
import sys as _sys
import threading
import time
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

from local_llm_bot.app.config import CONFIG
from local_llm_bot.app.ingest.chunking import chunk_text
from local_llm_bot.app.ingest.index_jsonl import append_rows
from local_llm_bot.app.ingest.loaders import SUPPORTED_EXTS, load_document
from local_llm_bot.app.ingest.manifest import (
    build_entry,
    write_manifest_entry,
)
from local_llm_bot.app.utils.corpus_paths import corpus_paths
from local_llm_bot.app.utils.repo_root import find_repo_root

# Qdrant is the only supported vectorstore.
# Chroma support has been removed — see chroma eradication ticket.
from local_llm_bot.app.vectorstore import qdrant_store as _store

try:
    import yaml as _yaml
    _YAML_AVAILABLE = True
except ImportError:
    _YAML_AVAILABLE = False


def _load_ks_alias_map(repo: Path, corpus: str) -> dict[str, list[str]]:
    """
    Load GLEIF entity Wikidata fields for a corpus and return a dict mapping
    canonical name → list of natural query forms for [Document:] prefix injection.

    Uses wikidata_label, wikidata_short_name, wikidata_tickers from the entities
    YAML (schema_version 1.1+). These are the forms users naturally type in queries.
    Full aliases list (mechanical variants) is used query-side in rag_core, not here.

    Returns empty dict if no knowledge sources file exists — prefix falls back to
    unenriched form silently. Format-driven: only called when doc_entity was
    extracted from an XBRL tag (iXBRL/ESEF filings).
    """
    if not _YAML_AVAILABLE:
        return {}
    ks_dir = repo / "data" / "knowledge_sources" / "gleif"
    if not ks_dir.exists():
        return {}
    matches = sorted(ks_dir.glob(f"gleif_{corpus}_*_entities.yaml"))
    if not matches:
        return {}
    try:
        with open(matches[0], encoding="utf-8") as f:
            data = _yaml.safe_load(f)
        alias_map: dict[str, list[str]] = {}
        for entity in data.get("entities", []):
            canonical = entity.get("canonical", "")
            if not canonical:
                continue
            # Natural query forms only — Wikidata-sourced
            natural: list[str] = []
            label = entity.get("wikidata_label", "")
            short = entity.get("wikidata_short_name", "")
            tickers = entity.get("wikidata_tickers", [])
            scope_name = entity.get("scope_name", "")
            # scope_name is always a natural form (what users type)
            if scope_name and scope_name != canonical:
                natural.append(scope_name)
            # Wikidata label if different from scope_name
            if label and label != scope_name and label != canonical:
                natural.append(label)
            # Wikidata short name if different
            if short and short not in natural and short != canonical:
                natural.append(short)
            # Tickers — short discriminating tokens
            for t in (tickers or []):
                if t and len(t) <= 6 and t not in natural:
                    natural.append(t)
            alias_map[canonical] = natural
        return alias_map
    except Exception:  # noqa: BLE001
        return {}


def _dt_now() -> str:
    """Return current UTC time as ISO string."""
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat(timespec="seconds")  # noqa: UP017


@dataclass(frozen=True)
class IngestResult:
    corpus: str
    root: str
    chunk_size: int
    overlap: int
    embed_model: str

    files_discovered: int
    files_supported: int
    files_processed: int
    files_skipped_unchanged: int
    files_failed: int

    chunks_written: int

    duration_sec: float
    vectorstore: str = "qdrant"
    # Per-file stats: {filename: {size_bytes, chunks, duration_sec, ingested_at}}
    file_stats: dict = None  # type: ignore[assignment]
    # Normalizer summary — counts across all files processed this run
    normalizer_hits: int = 0       # files where entity+year was extracted
    normalizer_misses: int = 0     # HTML/XHTML files where normalizer found nothing
    normalizer_mismatches: int = 0 # files where entity didn't match filename stem


def _repo_root() -> Path:
    return find_repo_root(Path(__file__))


def _iter_files(root: Path) -> Iterable[Path]:
    """
    Yield all files under root, excluding the trash/ directory.

    trash/ is now a sibling of uploads/ at the corpus level, so this guard
    is belt-and-suspenders — uploads/ should never contain a trash/ subdir.
    Kept explicitly to prevent any legacy or accidental trash/ inside uploads/
    from being ingested.
    """
    for p in root.rglob("*"):
        if p.is_file() and "trash" not in p.parts:
            yield p


def _load_qdrant_source_paths(collection_name: str) -> set[str]:
    """
    Fetch all source_path values currently indexed in Qdrant for a collection.
    Returns a set of absolute path strings.

    Used at the start of each ingest run to determine which files are already
    indexed — replacing the manifest-based skip check with Qdrant as the
    single source of truth.

    Uses scroll pagination to handle large collections (e.g. 105K chunks).
    Each page fetches up to 1000 points. Payload fetch is limited to
    source_path only to minimise data transfer.
    """
    from qdrant_client import QdrantClient
    from qdrant_client.models import PayloadSelectorInclude

    source_paths: set[str] = set()
    try:
        client = QdrantClient(
            host=_os.getenv("QDRANT_HOST", "localhost"),
            port=int(_os.getenv("QDRANT_PORT", "6333")),
        )
        existing = [c.name for c in client.get_collections().collections]
        if collection_name not in existing:
            return source_paths

        offset = None
        while True:
            result, next_offset = client.scroll(
                collection_name=collection_name,
                limit=1000,
                offset=offset,
                with_payload=PayloadSelectorInclude(include=["source_path"]),
                with_vectors=False,
            )
            for point in result:
                sp = (point.payload or {}).get("source_path")
                if sp:
                    source_paths.add(str(sp))
            if next_offset is None:
                break
            offset = next_offset
    except Exception:
        # If Qdrant is unreachable, return empty set — all files will be processed.
        # This is the safe fallback: re-ingest is idempotent via upsert.
        pass
    return source_paths


def _file_unchanged(source_path: Path, manifest_map: dict) -> bool:
    """
    NOTE: intentionally NOT used in skip decision — kept for reference only.
    Qdrant is the single source of truth for skip logic (AIStudio_186).
    manifest.jsonl is stale after corpus recreation and cannot be relied upon.
    """
    from local_llm_bot.app.ingest.manifest import ManifestEntry

    abs_path = str(source_path.resolve())
    prev: ManifestEntry | None = manifest_map.get(abs_path)
    if prev is None:
        return False
    try:
        st = source_path.stat()
        return (prev.mtime == int(st.st_mtime)) and (prev.size == int(st.st_size))
    except FileNotFoundError:
        return False


def _md5_of_file(path: Path) -> str:
    """Compute MD5 hex digest of a file. Stored in Qdrant payload for duplicate detection."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def _tqdm_write(pbar: Any | None, msg: str) -> None:
    """Write a message without disrupting the tqdm progress bar.
    Clears the bar before writing so the line does not collide.
    """
    if pbar is not None:
        pbar.clear()  # erase current bar line before writing
        pbar.write(msg, file=_sys.stderr)
        pbar.refresh()  # redraw bar below the written line
    else:
        print(msg, file=_sys.stderr)


# Chars that signal a token is meant as a regex. `.` and `-` are deliberately EXCLUDED —
# they appear in nearly every filename and are almost always meant literally; a token with
# only those is matched as a literal substring (where `.` still matches itself anyway).
_FILES_REGEX_META = _re.compile(r"[*+?\[\]()|^${}\\]")


def _selective_match(name: str, patterns: Iterable[str]) -> bool:
    """AIStudio_912 — match a basename against the --files token set, OR semantics.

    Each token is matched case-insensitively. A token containing regex metacharacters
    (* + ? [ ] ( ) | ^ $ { } \\) is compiled as a regex and `re.search`ed against the
    name; any other token is treated as a literal substring. A malformed regex falls back
    to a literal-substring test so a stray metacharacter never aborts a run. `name` matches
    if ANY token matches (so `--files BlackRock` selects BlackRock_10K_*.htm, and
    `--files 'JPM.*2025,Citi'` selects either).
    """
    low = name.lower()
    for pat in patterns:
        if not pat:
            continue
        if _FILES_REGEX_META.search(pat):
            try:
                if _re.search(pat, name, _re.IGNORECASE):
                    return True
                continue
            except _re.error:
                pass  # malformed regex → fall through to literal-substring test
        if pat.lower() in low:
            return True
    return False


def _extract_document_head(
    text: str,
    file_path: Path | None = None,
    max_chars: int = 800,
) -> str | None:
    """
    AIStudio_640 — Document-Head Extraction normalizer.

    Extract the primary named entity from a document to resolve anaphoric
    references in downstream chunks. Applies strategies in priority order,
    stopping at the first result:

    Strategy 1 — Domain-specific XML namespace registry (file_path required).
      Detects structured markup formats by presence of known namespace prefixes
      in the raw HTML. Each format has a mandatory entity identifier field defined
      by its standard — authoritative and always correct when present.
      Format-driven, not corpus-driven: works for any SEC 10-K, any ESEF filing,
      without knowing what corpus the file belongs to.

      Current registry:
        - SEC inline XBRL:  dei:EntityRegistrantName
        - ESEF (EU XBRL):   ifrs-full:NameOfReportingEntityOrOtherMeansOfIdentification

    Strategy 2 — Title-Case multi-word phrase scan of doc.text head.
      Fallback for plain-text documents (MD, TXT, DOCX, PDF). Finds the longest
      2+ Title-Case word sequence in the first max_chars, filtering stopwords.

    Strategy 3 — None (no-op).
      Returns None when no entity can be reliably extracted. Caller leaves
      chunk text unchanged. Correct for self-referential documents.

    Controlled by AISTUDIO_DOC_HEAD_NORMALIZER env var (default: "true").
    """
    if _os.getenv("AISTUDIO_DOC_HEAD_NORMALIZER", "true").lower() == "false":
        return None

    # ------------------------------------------------------------------
    # Strategy 1 — Domain-specific XML namespace registry
    # ------------------------------------------------------------------
    _XML_ENTITY_REGISTRY = [
        # SEC DEI taxonomy — covers 10-K, 10-Q, 20-F, 8-K, S-1, 40-F, 6-K
        # and UK FCA iXBRL filings (same DEI namespace).
        ("dei:",        "dei:EntityRegistrantName"),
        # IFRS / ESEF — EU listed companies (ESMA mandate).
        # Also covers EBA FINREP/COREP HTML supervisory reports.
        ("ifrs-full:",  "ifrs-full:NameOfReportingEntityOrOtherMeansOfIdentification"),
        # UK GAAP inline XBRL — Companies House filings for UK entities
        # not subject to ESEF (uses uk-bus or uk-gaap namespace).
        ("uk-bus:",     "uk-bus:NameOfUltimateParentOfGroup"),
        ("uk-gaap:",    "uk-gaap:EntityCurrentLegalOrRegisteredName"),
    ]

    if file_path is not None and file_path.suffix.lower() in (".htm", ".html"):
        try:

            # SEC-standard extensions that appear across all filers — not company-specific.
            _XBRL_STD = {
                "dei", "us-gaap", "us-roles", "us-types", "xbrli", "xbrldi",
                "xlink", "iso4217", "num", "nonnum", "ref", "ix", "ixt",
                "link", "xl", "xsi", "xml", "srt", "ecd", "cyd",
            }

            soup = BeautifulSoup(file_path.read_bytes(), "html.parser")

            # Strategy 1a — Authoritative entity tag from XML namespace registry.
            # Check for the entity tag directly — don't rely on namespace prefix
            # detection. Older filings may have dei: tags for auditor/period but
            # omit dei:EntityRegistrantName entirely.
            for _ns_prefix, entity_tag in _XML_ENTITY_REGISTRY:
                tag = soup.find(attrs={"name": entity_tag})
                if tag:
                    entity = tag.get_text(strip=True)
                    if entity:
                        return entity

            # Strategy 1b — Visible text scan for legal entity name.
            # For inline XBRL files that lack dei:EntityRegistrantName (older
            # filing formats), scan visible HTML elements for the first string
            # that looks like a legal entity name. Key filters:
            #   - Skip single-word strings (section headers like "General", "Overview")
            #   - Skip "Exhibit N" references (filing attachments, not entity names)
            #   - Skip known document structure phrases (Review, Summary, Section etc.)
            #   - Require 2+ words for ALL-CAPS candidates
            #   - Strip trailing footnote superscripts
            # BNY Mellon pattern: Exhibit 13.1 → FINANCIAL SECTION → entity name
            # → entity name appears at 3rd/4th visible element, after single-word headers
            _SKIP_PATTERNS = _re.compile(
                r"^(Exhibit\s+\d|Table\s+of|Annual\s+Report|Financial\s+(Review|Section|"
                r"Summary|Highlights|Statements?)|Overview|General|Contents|Index)$",
                _re.IGNORECASE,
            )
            _ENTITY_SUFFIXES = (
                "corporation", "company", "incorporated", "inc", "corp",
                "ltd", "llc", "lp", "l.p.", "n.a.", "group", "holdings",
                "bancorp", "bancshares", "trust", "partners", "capital",
                "financial", "services", "fund",
            )
            for tag in soup.find_all(["p", "span", "div", "td"]):
                txt = tag.get_text(strip=True)
                # Strip trailing footnote superscripts (digits, *, †, ‡, §)
                txt = _re.sub(r"[\d\*†‡§]+$", "", txt).strip()
                if not txt or len(txt) < 8 or len(txt) > 100:
                    continue
                if _SKIP_PATTERNS.match(txt):
                    continue
                words = txt.split()
                # ALL-CAPS multi-word: require 2+ words, all uppercase letters/spaces/&
                if txt == txt.upper() and txt.replace("&", "").replace(" ", "").isalpha() and len(words) >= 2:
                        return txt
                # Title-Case ending with known entity suffix
                last_word = words[-1].lower().rstrip(".,")
                if last_word in _ENTITY_SUFFIXES and len(words) >= 2 and words[0][0].isupper():
                        return txt

        except Exception:
            pass

    # ------------------------------------------------------------------
    # Strategy 2 — Title-Case phrase scan of plain text head
    # ------------------------------------------------------------------
    _STOPWORDS = {
        "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December",
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
        "Annual", "Report", "Form", "Filing", "United", "States", "America",
        "Securities", "Exchange", "Commission", "Washington", "Pursuant",
        "Fiscal", "Year", "Ended", "For", "The", "And", "Or",
        "Part", "Item", "Note", "Section", "Table", "Contents", "Index",
    }

    candidates = _re.findall(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b", text[:max_chars])
    filtered = [c for c in candidates if not all(w in _STOPWORDS for w in c.split())]
    if filtered:
        return max(filtered, key=len)

    return None


def _extract_document_metadata(
    file_path: Path | None,
) -> tuple[str | None, str | None, str | None, str | None, bool, str | None, str | None]:
    """
    AIStudio_682 — Merged Document-Head + Temporal Context extraction.

    Replaces separate _extract_document_head() + _extract_fiscal_year() calls
    with a single BeautifulSoup parse. Eliminates duplicate DOM parse per file.

    Returns (entity, year, format_name, strategy, mismatch) where:
      entity      — extracted entity name or None
      year        — 4-digit fiscal year string or None
      format_name — "SEC_XBRL" | "ESEF" | "UK_GAAP" | "plain_html" | None
      strategy    — "1a" | "1b" | "2" | None
      mismatch    — True if company namespace prefix doesn't match filename stem

    None entity is a no-op — caller uses entity-only or no prefix.
    Only applies to .htm/.html files; non-HTML returns (None, None, None, None, False, None, None).
    """
    if _os.getenv("AISTUDIO_DOC_HEAD_NORMALIZER", "true").lower() == "false":
        return None, None, None, None, False, None, None

    if file_path is None or file_path.suffix.lower() not in (".htm", ".html", ".xhtml"):
        return None, None, None, None, False, None, None


    _XBRL_STD = {
        "dei", "us-gaap", "us-roles", "us-types", "xbrli", "xbrldi",
        "xlink", "iso4217", "num", "nonnum", "ref", "ix", "ixt",
        "link", "xl", "xsi", "xml", "srt", "ecd", "cyd",
    }
    # Entity tag registry — maps format name to XBRL namespace + authoritative entity tag.
    # Strategy 1a: extract entity from the tag with this name attribute.
    # Source logic: entity from tag, year from DateOfEndOfReportingPeriod (ESEF) or
    # DocumentFiscalYearFocus (SEC), falling back to filename year if tag absent.
    # Year filename rules: 4-digit 1900–2099 used as-is; 2-digit 60–99 → 19xx; 00–59 → 20xx.
    # Decoupling target: src/local_llm_bot/app/ingest/normalizers/xbrl.py (AIStudio_724).
    _XML_ENTITY_REGISTRY = [
        ("SEC_XBRL", "dei:",       "dei:EntityRegistrantName",                                    "1a"),
        ("ESEF",     "ifrs-full:", "ifrs-full:NameOfReportingEntityOrOtherMeansOfIdentification", "1a"),
        ("UK_GAAP",  "uk-bus:",    "uk-bus:NameOfUltimateParentOfGroup",                          "1a"),
        ("UK_GAAP",  "uk-gaap:",   "uk-gaap:EntityCurrentLegalOrRegisteredName",                  "1a"),
    ]

    _SKIP_PATTERNS = _re.compile(
        r"^(Exhibit\s+\d|Table\s+of|Annual\s+Report|Financial\s+(Review|Section|"
        r"Summary|Highlights|Statements?)|Overview|General|Contents|Index)$",
        _re.IGNORECASE,
    )
    _ENTITY_SUFFIXES = (
        "corporation", "company", "incorporated", "inc", "corp",
        "ltd", "llc", "lp", "l.p.", "n.a.", "group", "holdings",
        "bancorp", "bancshares", "trust", "partners", "capital",
        "financial", "services", "fund",
    )

    try:
        soup = BeautifulSoup(file_path.read_bytes(), "html.parser")

        # Strategy 1a — authoritative entity tag from XML namespace registry
        entity = None
        year = None
        fmt = None
        strategy = None

        _matched_tag = None
        for format_name, _ns_prefix, entity_tag, strat in _XML_ENTITY_REGISTRY:
            tag = soup.find(attrs={"name": entity_tag})
            if tag:
                val = tag.get_text(strip=True)
                if val:
                    entity = val
                    fmt = format_name
                    strategy = strat
                    _matched_tag = entity_tag  # e.g. "ifrs-full:NameOfReportingEntity..."
                    break

        # Extract fiscal year (single parse — same soup object)
        _year_tag_name = None
        year_tag = soup.find(attrs={"name": "dei:DocumentFiscalYearFocus"})
        if year_tag:
            yr = year_tag.get_text(strip=True)
            _year_tag_name = "dei:DocumentFiscalYearFocus"
            if yr and yr.isdigit() and len(yr) == 4:
                year = yr

        # ESEF year tag — value is YYYY-MM-DD, extract first 4 chars
        if year is None and fmt == "ESEF":
            esef_year_tag = soup.find(attrs={"name": "ifrs-full:DateOfEndOfReportingPeriod2013"})
            if esef_year_tag:
                yr_raw = esef_year_tag.get_text(strip=True)
                _year_tag_name = "ifrs-full:DateOfEndOfReportingPeriod2013"
                if yr_raw and len(yr_raw) >= 4 and yr_raw[:4].isdigit():
                    year = yr_raw[:4]

        # Filename year fallback — parse year from stem when XML tag absent.
        # 4-digit: 1900–2099 used as-is.
        # 2-digit: 60–99 → 1960–1999; 00–59 → 2000–2059 (for projections).
        # Decoupling target: src/local_llm_bot/app/ingest/normalizers/xbrl.py (AIStudio_724).
        if year is None and file_path is not None:
            # 4-digit year first
            _yr_match = _re.search(r"[_\-](\d{4})(?:[_\-.]|$)", file_path.stem)
            if _yr_match:
                _yr_cand = int(_yr_match.group(1))
                if 1900 <= _yr_cand <= 2099:
                    year = str(_yr_cand)
            # 2-digit year fallback
            if year is None:
                _yr2_match = _re.search(r"[_\-](\d{2})(?:[_\-.]|$)", file_path.stem)
                if _yr2_match:
                    _yr2 = int(_yr2_match.group(1))
                    year = str(1900 + _yr2) if _yr2 >= 60 else str(2000 + _yr2)

        # Strategy 1b — visible text scan (fallback for older XBRL without entity tag)
        company_prefixes = set()  # initialized here so mismatch block can always reference it
        if entity is None:
            for tag in soup.find_all(attrs={"name": True}):
                ns = tag.get("name", "").split(":")[0]
                if ns and ns not in _XBRL_STD:
                    company_prefixes.add(ns)

            if company_prefixes:
                fmt = "SEC_XBRL"
                strategy = "1b"
                for tag in soup.find_all(["p", "span", "div", "td"]):
                    txt = tag.get_text(strip=True)
                    txt = _re.sub(r"[\d\*†‡§]+$", "", txt).strip()
                    if not txt or len(txt) < 8 or len(txt) > 100:
                        continue
                    if _SKIP_PATTERNS.match(txt):
                        continue
                    words = txt.split()
                    if txt == txt.upper() and txt.replace("&", "").replace(" ", "").isalpha() and len(words) >= 2:
                            entity = txt
                            break
                    last_word = words[-1].lower().rstrip(".,")
                    if last_word in _ENTITY_SUFFIXES and len(words) >= 2 and words[0][0].isupper():
                            entity = txt
                            break

        # Mismatch detection — company namespace prefix vs filename stem
        mismatch = False
        if entity and file_path and company_prefixes:
            stem_lower = file_path.stem.lower()
            for prefix in company_prefixes:
                if prefix not in _XBRL_STD:
                    # If prefix doesn't appear anywhere in filename → mismatch
                    if prefix.lower() not in stem_lower:
                        # Additional check: entity name words vs filename
                        entity_words = set(_re.sub(r"[^a-z]", " ", entity.lower()).split())
                        stem_words = set(_re.sub(r"[^a-z]", " ", stem_lower).split())
                        overlap = entity_words & stem_words - {"the", "of", "and", "inc", "corp", "group"}
                        if not overlap:
                            mismatch = True
                    break

        if entity is None:
            fmt = "plain_html" if fmt is None else fmt

        # AIStudio_721 — normalize entity string before return.
        # XBRL source documents contain non-breaking spaces (\u00a0) and other
        # Unicode noise in entity name tags. These corrupt the prefix and break
        # BM25 tokenization. Normalize: collapse \u00a0 → regular space, strip
        # leading/trailing whitespace, collapse multiple spaces.
        if entity is not None:
            import unicodedata as _unicodedata
            entity = entity.replace("\u00a0", " ")   # non-breaking space → space
            entity = entity.replace("\u200b", "")    # zero-width space → remove
            entity = entity.replace("\ufeff", "")    # BOM → remove
            entity = _unicodedata.normalize("NFC", entity)  # canonical Unicode form
            entity = " ".join(entity.split())        # collapse multiple spaces

        return entity, year, fmt, strategy, mismatch, _matched_tag, _year_tag_name

    except Exception:
        return None, None, None, None, False, None, None



def _tag_local_name(tag: str | None) -> str:
    """Extract local part of XBRL tag name, stripping namespace prefix and verbose suffixes.
    e.g. "ifrs-full:NameOfReportingEntityOrOtherMeansOfIdentification" → "NameOfReportingEntity"
         "ifrs-full:DateOfEndOfReportingPeriod2013" → "DateOfEndOfReportingPeriod"
         "dei:EntityRegistrantName" → "EntityRegistrantName"
         "dei:DocumentFiscalYearFocus" → "DocumentFiscalYearFocus"
    """
    if not tag:
        return ""
    local = tag.split(":")[-1]  # strip namespace prefix
    local = local.replace("OrOtherMeansOfIdentification", "")  # verbose ESEF suffix
    local = local.rstrip("0123456789")  # strip trailing year digits e.g. "2013"
    return local


def ingest_corpus(
    *,
    root: Path,
    corpus: str,
    reset_index: bool = False,
    force: bool = False,
    # CLI overrides (None => use CONFIG defaults)
    vectorstore: str | None = None,
    chunk_size: int | None = None,
    overlap: int | None = None,
    embed_model: str | None = None,
    max_files: int | None = None,
    # Explicit allowlist of filenames (basename) to ingest. When provided, ONLY
    # these files are processed — all other files under root (already-indexed OR
    # parked-but-not-yet-chosen) are left untouched. Selected files are always
    # (re-)embedded regardless of whether Qdrant already has them. None => whole
    # corpus, today's behavior. (AIStudio: per-file selective ingest.)
    only_files: set[str] | None = None,
    # progress bar class (tqdm) passed from __main__
    tqdm_cls: Any | None = None,
) -> IngestResult:
    """
    Ingest a directory into Qdrant.

    Skip logic (Qdrant is the single source of truth):
      - Pre-load all source_path values currently in Qdrant for this corpus.
      - Skip a file if: (a) its abs_path is in the Qdrant source set AND
        (b) its mtime+size match the manifest (i.e. file is unchanged on disk).
      - force=True bypasses both checks.

    Progress bars (if tqdm_cls is available):
      1) Discover files
      2) Process supported files (parse + chunk + manifest + JSONL rows)
      3) Embed/upsert chunks into Qdrant in batches
    """
    t0 = time.time()

    repo = _repo_root()
    paths = corpus_paths(repo, corpus)
    paths["base"].mkdir(parents=True, exist_ok=True)

    # Resolve effective settings
    _vs = (vectorstore or CONFIG.rag.vectorstore or "qdrant").lower()
    chunk_size_eff = CONFIG.ingest.chunk_size if chunk_size is None else int(chunk_size)
    overlap_eff = CONFIG.ingest.overlap if overlap is None else int(overlap)
    embed_model_eff = CONFIG.rag.default_embed_model if embed_model is None else str(embed_model)

    collection_name = f"aistudio_{corpus}"

    # AIStudio_801: load knowledge source alias map once per ingest run.
    # Maps canonical GLEIF name → [natural query forms] for [Document:] prefix enrichment.
    # Empty dict if no knowledge sources exist for this corpus — graceful no-op.
    _ks_alias_map = _load_ks_alias_map(repo, corpus)

    # Reset handling
    if reset_index:
        for k in ("index", "manifest", "failures"):
            if paths[k].exists():
                paths[k].unlink()

    # --force: atomic wipe of Qdrant collection + manifest + index
    if force:
        for k in ("index", "manifest", "failures"):
            if paths[k].exists():
                paths[k].write_text("", encoding="utf-8")  # truncate, don't delete
        with contextlib.suppress(Exception):
            _store.delete_collection(collection_name=collection_name)

    # Pre-load Qdrant source paths — single scroll, O(n chunks), done once per run.
    # This is the skip-decision source of truth. Empty on first ingest or after --force.
    qdrant_source_paths = _load_qdrant_source_paths(collection_name) if not force else set()

    files_discovered = 0
    files_supported = 0
    files_processed = 0
    files_skipped_unchanged = 0
    files_failed = 0

    chunks_written = 0
    failures: list[dict[str, Any]] = []
    file_stats: dict[str, dict] = {}
    # Normalizer counters — accumulated across all HTML/XHTML files
    _normalizer_hits = 0
    _normalizer_misses = 0
    _normalizer_mismatches = 0


    _PAGE_RE = _re.compile(r"^\[PAGE_(\d+)\]\s*", _re.MULTILINE)

    # -----------------------
    # Phase 1: Discover
    # -----------------------
    # Files are sorted alphabetically — consistent order matches the pre-scan
    # in api.py trigger_ingest, which also sorts alphabetically. This ensures
    # bytes_processed accumulates in the correct order for the progress bar.

    discovered: list[Path] = []
    p_discover = None  # Discover is instant — no progress bar needed

    try:
        for p in sorted(_iter_files(root), key=lambda x: x.name):
            discovered.append(p)
            files_discovered += 1
            if max_files is not None and files_discovered >= int(max_files):
                break
            if p_discover is not None:
                p_discover.update(1)
    finally:
        if p_discover is not None:
            p_discover.close()

    # Selective ingest: restrict to the explicit allowlist if given. AIStudio_912 — each
    # --files token is OR-matched against the basename: a literal substring, or a regex if it
    # contains regex metacharacters. (The UI still sends exact filenames, which match as their
    # own literal substring.) Everything not matched — whether already indexed or parked in
    # uploads/ awaiting a later decision — is dropped from this run entirely, so totals/
    # denominators below reflect ONLY the chosen files.
    if only_files is not None:
        discovered = [p for p in discovered if _selective_match(p.name, only_files)]
        files_discovered = len(discovered)

    # -----------------------
    # Phase 2: Process + Embed + Upsert (per file)
    # -----------------------
    # Each file is fully processed — chunked, embedded, upserted to Qdrant —
    # before moving to the next. Memory footprint is constant regardless of
    # corpus size. Qdrant gets live chunk counts as each file completes,
    # enabling accurate progress reporting.

    # Pre-compute total bytes for byte-based progress estimation (same algo as UI).
    _total_bytes = sum(f.stat().st_size for f in discovered if f.is_file())

    # AIStudio_722b — pre-compute supported file count BEFORE the loop so N-of-T
    # denominator is fixed. Without this, files_supported increments during the loop
    # producing "1 of 1", "2 of 2" etc. in completion lines.
    _total_supported = sum(
        1 for f in discovered
        if f.suffix.lower() in SUPPORTED_EXTS and not f.name.startswith("~$")
    )

    # Estimate total chunks for chunk-based bar fill.
    # D_SEED_BAR = 40 chunks/MB — slightly above observed ESEF/SEC ratio (~37/MB)
    # so bar runs a touch slower than reality (better UX than overshooting).
    # Property of document type + chunk size (1,200 chars), not hardware.
    # Self-corrects to actual d_observed after file 1 completes.
    _D_SEED_BAR = 40.0 / (1024 * 1024)
    _supported_bytes = sum(
        f.stat().st_size for f in discovered
        if f.suffix.lower() in SUPPORTED_EXTS and not f.name.startswith("~$")
    )
    _est_total_chunks_bar = max(1, int(_D_SEED_BAR * _supported_bytes))
    _n_width = len(str(_total_supported))  # digit width for right-justify in label

    # Seed chunks_per_sec — used for interpolation before file 1 completes.
    # 45 chunks/sec is the observed M4 Pro embedding rate (nomic-embed-text).
    # Self-corrects to actual observed rate after each file completes.
    _chunks_per_sec = 45.0

    # AIStudio (ingest-status freeze fix) — render the live tqdm Process bar ONLY in an
    # operator TTY. Under api.py's pipe there is no human to display it to, and routing the
    # [ingest] machine signals through pbar.write() while the bar is live did not reliably
    # flush them to the pipe, so api.py's _stream_stderr never received per-file progress
    # (files_processed/elapsed stayed 0; the UI bar crawled then froze). With no bar in pipe
    # mode, _tqdm_write falls to plain print(..., file=_sys.stderr) — newline-terminated and,
    # with PYTHONUNBUFFERED=1, flushed at once — so the signals arrive. This is the
    # "pipeline controls bars" gate __main__.py delegated. Cross-ref AIStudio_722 / AIStudio_613.
    if tqdm_cls is not None and _sys.stderr.isatty():
        # STD §8 Phase 2 — plain tqdm, no subclass, full label control via bar_format.
        # bar_format is mutated per-file update (p_process.bar_format = ...) to inject
        # the current "N of T" file counter directly into the format string.
        # tqdm's own {elapsed} and {remaining} supply timing (EMA-based — acceptable
        # for operator UX; d_observed drives the UI bar separately).
        # Rate displayed as ms/chunk computed from tqdm's {rate} field.
        # No {desc} in bar_format — avoids the hardcoded ": " desc_pad artifact.
        # dynamic_ncols=True auto-detects terminal width — avoids parasitic box.
        _bar_n_str = "0".rjust(_n_width)
        _bar_fmt_base = (
            f"  {_bar_n_str} of {_total_supported} · "
            "{percentage:.0f}%|{bar:20}| elapsed: -- · remaining: -- · avg: --"
        )
        p_process = tqdm_cls(
            total=_est_total_chunks_bar,
            desc="",
            unit="chunk",
            dynamic_ncols=True,  # auto-fit terminal width (re-detects on resize) so the bar never wraps → \r overwrites cleanly (AIS_12)
            bar_format=_bar_fmt_base,
            leave=True,
        )
    else:
        p_process = None

    try:
        for file_path in discovered:
            ext = file_path.suffix.lower()
            if ext not in SUPPORTED_EXTS or file_path.name.startswith("~$"):
                # Unsupported file — skip silently. Do NOT update the bar:
                # _total_supported excludes these files, so updating here would
                # push the bar past 100% and produce a spurious 10/None final tick.
                continue

            files_supported += 1

            try:
                abs_path = str(file_path.resolve())

                # Skip decision: Qdrant already has this file — no re-ingest needed.
                # _file_unchanged() removed: manifest.jsonl stale after corpus recreation. (AIStudio_186)
                # Exception: when an explicit allowlist (only_files) is active, the user
                # chose these files on purpose — always (re-)embed them, never skip.
                if not force and only_files is None and abs_path in qdrant_source_paths:
                    files_skipped_unchanged += 1
                    if p_process is not None:
                        p_process.update(1)
                    continue

                t_file_start = time.time()
                # AIStudio_722a — STD §8 Phase 1 activity line: gerund header + N of T +
                # filename + size. Format/augmentation fields added after normalizer runs.
                # Uses _total_supported (pre-computed) so N-of-T is always correct.
                # Description-only — bar is a separate line below (no bar content here).
                if p_process is not None:
                    # Update bar_format: N of T + file size as % of corpus
                    _n_str = str(files_supported).rjust(_n_width)
                    p_process.bar_format = (
                        f"  {_n_str} of {_total_supported} · {file_path.name} · "
                        "{percentage:.0f}%|{bar:20}| elapsed: -- · remaining: -- · avg: --"
                    )
                    p_process.refresh()
                doc = load_document(file_path)
                if not doc or not doc.text.strip():
                    write_manifest_entry(paths["manifest"], build_entry(file_path))
                    files_processed += 1
                    if p_process is not None:
                        p_process.update(1)
                    continue

                chunks = chunk_text(doc.text, chunk_size=chunk_size_eff, overlap=overlap_eff)

                # AIStudio_640 + AIStudio_674 — Document-Head + Temporal normalizers.
                # Extract entity (AIStudio_640) and fiscal year (AIStudio_674) from
                # the document head. When both are found, prefix is
                # "[Document: <entity> FY<year>]" — making chunks distinguishable by
                # both identity and time in vector space. When only entity is found,
                # prefix is "[Document: <entity>]". Neither found = no-op.
                # AIStudio_682 — single parse via merged _extract_document_metadata()
                doc_entity, doc_year, doc_fmt, doc_strategy, doc_mismatch, doc_tag, doc_year_tag = (
                    _extract_document_metadata(file_path)
                )

                # Compute MD5 once per file — stored in every chunk payload
                file_md5 = _md5_of_file(file_path)

                # Build rows for this file only
                file_rows: list[dict[str, Any]] = []
                last_page: int | None = None
                for i, c in enumerate(chunks):
                    page_match = _PAGE_RE.search(c)
                    if page_match:
                        last_page = int(page_match.group(1))
                    page_num = last_page
                    clean_text = _PAGE_RE.sub("", c).strip()

                    # Apply normalizer prefix if entity was extracted.
                    # AIStudio_801: if knowledge sources exist for this corpus,
                    # enrich prefix with Wikidata natural query forms (scope_name,
                    # label, short_name, tickers). These are embedded into every
                    # chunk from this entity — improving both BM25 and vector recall
                    # for user queries that use the natural name rather than the
                    # full GLEIF legal name.
                    # Format (entity + aliases + year): "[Document: THE GOLDMAN SACHS GROUP, INC. | Goldman Sachs | GS FY2025] <chunk>"
                    # Format (entity + year, no aliases): "[Document: JPMorgan Chase & Co. FY2025] <chunk>"
                    # Format (entity only):               "[Document: JPMorgan Chase & Co.] <chunk>"
                    _ks_aliases = _ks_alias_map.get(doc_entity, []) if doc_entity else []
                    _alias_suffix = (" | " + " | ".join(_ks_aliases)) if _ks_aliases else ""
                    if doc_entity and doc_year:
                        clean_text = f"[Document: {doc_entity}{_alias_suffix} FY{doc_year}] {clean_text}"
                    elif doc_entity:
                        clean_text = f"[Document: {doc_entity}{_alias_suffix}] {clean_text}"

                    chunk_id = (
                        f"{abs_path}::page-{page_num}::chunk-{i}"
                        if page_num is not None
                        else f"{abs_path}::chunk-{i}"
                    )
                    file_rows.append(
                        {
                            "chunk_id": chunk_id,
                            "doc_id": abs_path,
                            "source_path": abs_path,
                            "text": clean_text,
                            "page": page_num,
                            "md5": file_md5,
                            "firm": doc_entity or "",
                        }
                    )


                # Embed + upsert this file's chunks immediately — no accumulation
                if file_rows:
                    ids = [str(r["chunk_id"]) for r in file_rows]
                    documents = [str(r["text"]) for r in file_rows]
                    metadatas = [
                        {
                            "source_path": str(r["source_path"]),
                            "doc_id": str(r["doc_id"]),
                            "page": r["page"],
                            "md5": str(r["md5"]),
                            "firm": str(r.get("firm", "")),
                        }
                        for r in file_rows
                    ]

                    # Interpolation thread: tick bar forward at expected rate
                    # during upsert so progress appears continuous not jumpy.
                    # Uses seed _chunks_per_sec (45/s) for file 1, then
                    # self-corrects to observed rate from file 2 onwards.
                    _interp_bar_n = p_process.n if p_process is not None else 0
                    _interp_stop = threading.Event()

                    def _fmt_s(s: float) -> str:
                        m, sec = divmod(int(s), 60)
                        return f"{m:02d}:{sec:02d}"

                    def _interpolate(pbar, n_chunks, cps, stop, t_start,
                                     n_file, n_total, n_w, t_remaining_est,
                                     fname=""):
                        if cps <= 0 or pbar is None:
                            return
                        tick_interval = 0.1  # 100ms ticks
                        bar_update_interval = 0.5  # refresh bar_format every 500ms
                        chunks_per_tick = max(1, int(cps * tick_interval))
                        sent = 0
                        last_bar_update = -bar_update_interval  # force immediate first update
                        while not stop.is_set() and sent < n_chunks:
                            time.sleep(tick_interval)
                            if stop.is_set():
                                break
                            ticks = min(chunks_per_tick, n_chunks - sent)
                            pbar.update(ticks)
                            sent += ticks
                            # Update timing in bar_format every 500ms
                            now = time.time()
                            if now - last_bar_update >= bar_update_interval:
                                last_bar_update = now
                                _el = now - t_start
                                # AIStudio_907: ETA from the bar's true global fraction (the %
                                # is correct) × observed overall rate (elapsed ÷ progress) —
                                # self-corrects each tick, never pins to 00:00 while progress <
                                # total. The prior form subtracted total-elapsed-since-ingest
                                # (_el = now − t0) from a file-start duration (t_remaining_est),
                                # going negative → max(0, …) → 00:00 mid-file.
                                _bar_total = getattr(pbar, "total", 0) or 0
                                _total_remaining = (
                                    _el * (_bar_total - pbar.n) / pbar.n
                                    if getattr(pbar, "n", 0) > 0 and _bar_total > pbar.n
                                    else 0.0
                                )
                                _avg = f"{1000/cps:.0f}ms/chunk"
                                _n_str = str(n_file).rjust(n_w)
                                pbar.bar_format = (
                                    f"  {_n_str} of {n_total} · {fname} · "
                                    f"{{percentage:.0f}}%|{{bar:20}}| "
                                    f"elapsed: {_fmt_s(_el)} · "
                                    f"remaining: ~{_fmt_s(_total_remaining)} · "
                                    f"avg: {_avg}"
                                )

                    # Estimate remaining time at start of this file
                    _interp_remaining_est = (
                        (_est_total_chunks_bar - p_process.n) / _chunks_per_sec
                        if _chunks_per_sec > 0 and hasattr(p_process, "n") and p_process is not None
                        else 0.0
                    )
                    _interp_thread = threading.Thread(
                        target=_interpolate,
                        args=(p_process, len(file_rows), _chunks_per_sec, _interp_stop,
                              t0, files_supported, _total_supported, _n_width,
                              _interp_remaining_est, file_path.name),
                        daemon=True,
                    )
                    if p_process is not None:
                        _interp_thread.start()

                    _store.upsert_chunks(
                        persist_dir=Path("."),
                        collection_name=collection_name,
                        embed_model=embed_model_eff,
                        ids=ids,
                        documents=documents,
                        metadatas=metadatas,
                    )

                    # Stop interpolation and correct any over/undershoot
                    _interp_stop.set()
                    if p_process is not None:
                        _interp_thread.join(timeout=0.5)
                        # Correct bar to exact chunk count (interp may over/undershoot)
                        _interp_actual = p_process.n - _interp_bar_n
                        _interp_delta = len(file_rows) - _interp_actual
                        if _interp_delta != 0:
                            p_process.update(_interp_delta)

                    # Persist JSONL audit log per file
                    append_rows(paths["index"], file_rows)

                chunks_written += len(chunks)
                file_dur = round(time.time() - t_file_start, 3)
                file_stats[file_path.name] = {
                    "size_bytes": file_path.stat().st_size,
                    "chunks": len(chunks),
                    "duration_sec": file_dur,
                    "ingested_at": _dt_now(),
                }

                # AIStudio_675 + AIStudio_680 + AIStudio_697 — normalizer instrumentation.
                # Fires AFTER upsert so chunk count is final.
                # Guard extended to .xhtml (AIStudio_697 fix — ESEF files were silently skipped).
                # Two outputs:
                #   (1) STD §8 completion line via _tqdm_write — operator terminal
                #   (2) Structured [ingest] normalizer: stderr line — parsed by api.py → UI
                _is_markup = file_path.suffix.lower() in (".htm", ".html", ".xhtml")
                _file_chunks = len(chunks)
                _file_size = file_path.stat().st_size

                if _is_markup:
                    # Use _total_supported (pre-computed before loop) as fixed denominator.
                    # files_supported increments during the loop so using it here would
                    # produce "1 of 1", "2 of 2" etc. _total_supported is correct.
                    _n_width = len(str(_total_supported))
                    _n_str = str(files_processed + 1).rjust(_n_width)
                    _t_str = str(_total_supported)

                    if doc_entity:
                        _normalizer_hits += 1
                        if doc_mismatch:
                            _normalizer_mismatches += 1
                        # Build source label — reflects what provided entity and year.
                        # Three cases per STD prescription:
                        #   (a) Both from XBRL tags  → tags [NameOfReportingEntity, DateOfEndOfReportingPeriod]
                        #   (b) Entity from tag, year from filename → [tag: NameOfReportingEntity · filename]
                        #   (c) Entity from tag, no year → source: tag [NameOfReportingEntity]
                        # Decoupling target: src/local_llm_bot/app/ingest/normalizers/xbrl.py (AIStudio_724)
                        if doc_strategy == "1a":
                            _entity_local = _tag_local_name(doc_tag)
                            _year_local = _tag_local_name(doc_year_tag)
                            if _year_local and doc_year_tag:
                                # (a) Both entity and year from XBRL tags
                                _tag_sep = ", "
                                _tag_parts = list(dict.fromkeys([p for p in [_entity_local, _year_local] if p]))
                                _tag_suffix = "s" if len(_tag_parts) > 1 else ""
                                _source = f"tag{_tag_suffix} [{_tag_sep.join(_tag_parts)}]" if _tag_parts else "tag"
                            elif doc_year and _entity_local:
                                # (b) Entity from tag, year from filename
                                _source = f"[tag: {_entity_local} · filename]"
                            else:
                                # (c) Entity from tag, no year extracted
                                _source = f"source: tag [{_entity_local}]" if _entity_local else "tag"
                        elif doc_strategy == "1b":
                            _source = "scan"
                        else:
                            _source = "filename"
                        # Store normalizer fields in file_stats for __main__.py summary
                        file_stats[file_path.name]["normalizer_entity"] = doc_entity
                        file_stats[file_path.name]["normalizer_year"] = doc_year or ""
                        file_stats[file_path.name]["normalizer_source"] = _source
                        file_stats[file_path.name]["normalizer_mismatch"] = doc_mismatch

                        _fmt_label = doc_fmt or "unknown"
                        # Human-readable prefix label — STD §8 uses [brackets] not "quotes".
                        # AIStudio_907: mirror the STORED prefix exactly — include the Wikidata
                        # alias suffix (same computation as the chunk-text prefix above), so the
                        # log no longer understates what was embedded. Also surfaces the
                        # AIStudio_895 enrichment binding for visual confirmation at ingest.
                        _label_aliases = _ks_alias_map.get(doc_entity, []) if doc_entity else []
                        _label_suffix = (" | " + " | ".join(_label_aliases)) if _label_aliases else ""
                        _prefix_label = (
                            f"[{doc_entity}{_label_suffix} FY{doc_year}]"
                            if doc_year
                            else f"[{doc_entity}{_label_suffix}]"
                        )

                        # STD §8 completion line — scrolls in terminal, stays in history
                        _completion = (
                            f"  {_n_str} of {_t_str} · {file_path.name} · "
                            f"size: {_file_size:,} · chunks: {_file_chunks:,} · "
                            f"format: {_fmt_label} · chunk prefix aug.: {_prefix_label} · source: {_source}"
                        )
                        if doc_mismatch:
                            _completion += f" · \u26a0 entity mismatch: filename={file_path.stem[:30]}"
                        _tqdm_write(p_process, _completion)

                        # Structured machine-parseable line for api.py → UI (AIStudio_680)
                        # AIStudio_722a — TTY-gate: emit only when stderr is a pipe
                        # (subprocess from api.py). In TTY (operator terminal) this line
                        # is noise — the completion line above already shows all info.
                        if not _sys.stderr.isatty():
                            _structured = (
                                f"[ingest] normalizer: file={file_path.name} "
                                f"format={_fmt_label} "
                                f'entity="{doc_entity}" '
                                f"year={doc_year or ''} "
                                f"chunks={_file_chunks} "
                                f"source={_source} "
                                f"mismatch={str(doc_mismatch).lower()}"
                            )
                            _tqdm_write(p_process, _structured)

                    else:
                        _normalizer_misses += 1
                        # No normalizer hit — emit completion line without prefix fields
                        _completion = (
                            f"  {_n_str} of {_t_str} · {file_path.name} · "
                            f"size: {_file_size:,} · chunks: {_file_chunks:,}"
                        )
                        _tqdm_write(p_process, _completion)

                else:
                    # Non-markup file — plain completion line, no normalizer fields
                    # Use _total_supported (pre-computed) as fixed denominator.
                    _n_width = len(str(_total_supported))
                    _n_str = str(files_processed + 1).rjust(_n_width)
                    _t_str = str(_total_supported)
                    _completion = (
                        f"  {_n_str} of {_t_str} · {file_path.name} · "
                        f"size: {_file_size:,} · chunks: {_file_chunks:,}"
                    )
                    _tqdm_write(p_process, _completion)
                # Per-file completion signal for api.py async stderr iterator.
                # AIStudio_722a — TTY-gate: emit only when stderr is a pipe (api.py
                # subprocess). In TTY (operator terminal) this is noise.
                # api.py parses this line to update UI progress bar (AIStudio_613).
                if not _sys.stderr.isatty():
                    _bytes_done = sum(s["size_bytes"] for s in file_stats.values())
                    _tqdm_write(
                        p_process,
                        f"[ingest] file_complete: {files_processed + 1}/{len(discovered)} "
                        f"chunks={chunks_written} bytes={_bytes_done} "
                        f"file={file_path.name}",
                    )

                write_manifest_entry(paths["manifest"], build_entry(file_path))
                files_processed += 1

                if p_process is not None:
                    # Bar advance handled by interpolation thread + correction above
                    # Chunk-based progress estimation — same algorithm as the UI
                    # (AIStudio_613 / api.py). Time scales with chunks not bytes
                    # (per NOTES - AIStudio - Indexing Performance Notes 2026-05-03:
                    # "time scales linearly with chunks, not file size").
                    # d_observed = chunks/byte ratio, self-corrects each file.
                    # D_SEED = 200/MB starting estimate (same as api.py reconciled seed).
                    # remaining = remaining_chunks_est / chunks_per_sec
                    _D_SEED = 200.0 / (1024 * 1024)  # 200 chunks/MB starting estimate
                    _elapsed = time.time() - t0
                    _bytes_done = sum(s["size_bytes"] for s in file_stats.values())
                    _d_obs = (
                        chunks_written / _bytes_done
                        if _bytes_done > 0
                        else _D_SEED
                    )
                    # Clamp d_observed to sane range [1e-5, 1e-2] per api.py
                    _d_obs = max(1e-6, min(1e-2, _d_obs))
                    _chunks_per_sec = chunks_written / _elapsed if _elapsed > 0.001 else 0.001
                    # Simple remaining formula: (elapsed / pct_complete) - elapsed
                    # No clamping needed, self-corrects naturally each file.
                    _est_total_chunks = _d_obs * _supported_bytes
                    if p_process is not None:
                        p_process.total = max(chunks_written + 1, int(_est_total_chunks))
                    _pct_complete = chunks_written / max(1, int(_est_total_chunks))
                    _remaining = (
                        (_elapsed / _pct_complete) - _elapsed
                        if _pct_complete > 0.001
                        else 0.0
                    )
                    def _fmt_sec(s: float) -> str:
                        m, sec = divmod(int(s), 60)
                        return f"{m:02d}:{sec:02d}"
                    # STD §8 Phase 2: brackets in postfix string (not bar_format) to
                    # avoid tqdm leading comma artifact. avg: ms/chunk (chunk is the
                    # fundamental processing unit — consistent with STD §8).
                    # Bake d_observed timing into bar_format as literal strings —
                    # avoids tqdm {elapsed}/{remaining} tokens which use EMA not d_observed.
                    _n_done = str(files_processed).rjust(_n_width)  # files_processed already incremented
                    _avg_ms = f"{1000/_chunks_per_sec:.0f}ms/chunk" if _chunks_per_sec > 0 else "--ms/chunk"
                    p_process.bar_format = (
                        f"  {_n_done} of {_total_supported} · {file_path.name} · "
                        f"{{percentage:.0f}}%|{{bar:20}}| "
                        f"elapsed: {_fmt_sec(_elapsed)} · "
                        f"remaining: ~{_fmt_sec(_remaining)} · "
                        f"avg: {_avg_ms}"
                    )
                    p_process.refresh()

            except Exception as e:
                files_failed += 1
                failures.append(
                    {"source_path": str(file_path), "reason": type(e).__name__, "detail": str(e)}
                )
                if p_process is not None:
                    # Failed file — no chunks to advance, just refresh timing
                    # Chunk-based progress estimation — same algorithm as the UI
                    # (AIStudio_613 / api.py). Time scales with chunks not bytes
                    # (per NOTES - AIStudio - Indexing Performance Notes 2026-05-03:
                    # "time scales linearly with chunks, not file size").
                    # d_observed = chunks/byte ratio, self-corrects each file.
                    # D_SEED = 200/MB starting estimate (same as api.py reconciled seed).
                    # remaining = remaining_chunks_est / chunks_per_sec
                    _D_SEED = 200.0 / (1024 * 1024)  # 200 chunks/MB starting estimate
                    _elapsed = time.time() - t0
                    _bytes_done = sum(s["size_bytes"] for s in file_stats.values())
                    _d_obs = (
                        chunks_written / _bytes_done
                        if _bytes_done > 0
                        else _D_SEED
                    )
                    # Clamp d_observed to sane range [1e-5, 1e-2] per api.py
                    _d_obs = max(1e-6, min(1e-2, _d_obs))
                    _chunks_per_sec = chunks_written / _elapsed if _elapsed > 0.001 else 0.001
                    # Simple remaining formula: (elapsed / pct_complete) - elapsed
                    # No clamping needed, self-corrects naturally each file.
                    _est_total_chunks = _d_obs * _supported_bytes
                    if p_process is not None:
                        p_process.total = max(chunks_written + 1, int(_est_total_chunks))
                    _pct_complete = chunks_written / max(1, int(_est_total_chunks))
                    _remaining = (
                        (_elapsed / _pct_complete) - _elapsed
                        if _pct_complete > 0.001
                        else 0.0
                    )
                    def _fmt_sec(s: float) -> str:
                        m, sec = divmod(int(s), 60)
                        return f"{m:02d}:{sec:02d}"
                    # STD §8 Phase 2: brackets in postfix string (not bar_format) to
                    # avoid tqdm leading comma artifact. avg: ms/chunk (chunk is the
                    # fundamental processing unit — consistent with STD §8).
                    # Bake d_observed timing into bar_format as literal strings —
                    # avoids tqdm {elapsed}/{remaining} tokens which use EMA not d_observed.
                    _n_done = str(files_processed).rjust(_n_width)  # files_processed already incremented
                    _avg_ms = f"{1000/_chunks_per_sec:.0f}ms/chunk" if _chunks_per_sec > 0 else "--ms/chunk"
                    p_process.bar_format = (
                        f"  {_n_done} of {_total_supported} · {file_path.name} · "
                        f"{{percentage:.0f}}%|{{bar:20}}| "
                        f"elapsed: {_fmt_sec(_elapsed)} · "
                        f"remaining: ~{_fmt_sec(_remaining)} · "
                        f"avg: {_avg_ms}"
                    )
                    p_process.refresh()

    finally:
        if p_process is not None:
            # Erase the final bar render, then disable before close.
            # clear() wipes the current line; disable=True prevents close() re-rendering.
            p_process.clear()  # erase final 100% line from terminal
            p_process.disable = True
            p_process.close()

    if failures:
        paths["failures"].parent.mkdir(parents=True, exist_ok=True)
        with paths["failures"].open("a", encoding="utf-8") as f:
            for r in failures:
                f.write(json.dumps(r) + "\n")

    dur = time.time() - t0
    return IngestResult(
        corpus=corpus,
        root=str(root),
        vectorstore=_vs,
        chunk_size=chunk_size_eff,
        overlap=overlap_eff,
        embed_model=embed_model_eff,
        files_discovered=files_discovered,
        files_supported=files_supported,
        files_processed=files_processed,
        files_skipped_unchanged=files_skipped_unchanged,
        files_failed=files_failed,
        chunks_written=chunks_written,
        duration_sec=round(dur, 3),
        file_stats=file_stats,
        normalizer_hits=_normalizer_hits,
        normalizer_misses=_normalizer_misses,
        normalizer_mismatches=_normalizer_mismatches,
    )
