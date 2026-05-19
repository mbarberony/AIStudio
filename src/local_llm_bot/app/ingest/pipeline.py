# Version: 1.7.9
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
    """Write a message without disrupting the tqdm progress bar."""
    if pbar is not None:
        pbar.write(msg, file=_sys.stderr)
    else:
        print(msg, file=_sys.stderr)


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
) -> tuple[str | None, str | None, str | None, str | None, bool]:
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
    Only applies to .htm/.html files; non-HTML returns (None, None, None, None, False).
    """
    if _os.getenv("AISTUDIO_DOC_HEAD_NORMALIZER", "true").lower() == "false":
        return None, None, None, None, False

    if file_path is None or file_path.suffix.lower() not in (".htm", ".html"):
        return None, None, None, None, False


    _XBRL_STD = {
        "dei", "us-gaap", "us-roles", "us-types", "xbrli", "xbrldi",
        "xlink", "iso4217", "num", "nonnum", "ref", "ix", "ixt",
        "link", "xl", "xsi", "xml", "srt", "ecd", "cyd",
    }
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

        for format_name, _ns_prefix, entity_tag, strat in _XML_ENTITY_REGISTRY:
            tag = soup.find(attrs={"name": entity_tag})
            if tag:
                val = tag.get_text(strip=True)
                if val:
                    entity = val
                    fmt = format_name
                    strategy = strat
                    break

        # Extract fiscal year (single parse — same soup object)
        year_tag = soup.find(attrs={"name": "dei:DocumentFiscalYearFocus"})
        if year_tag:
            yr = year_tag.get_text(strip=True)
            if yr and yr.isdigit() and len(yr) == 4:
                year = yr

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

        return entity, year, fmt, strategy, mismatch

    except Exception:
        return None, None, None, None, False



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

    # -----------------------
    # Phase 2: Process + Embed + Upsert (per file)
    # -----------------------
    # Each file is fully processed — chunked, embedded, upserted to Qdrant —
    # before moving to the next. Memory footprint is constant regardless of
    # corpus size. Qdrant gets live chunk counts as each file completes,
    # enabling accurate progress reporting.

    # Pre-compute total bytes for byte-based progress estimation (same algo as UI).
    # Byte-based is more accurate than file-count-based because file sizes vary
    # significantly — larger files take proportionally more time to embed.
    _total_bytes = sum(f.stat().st_size for f in discovered if f.is_file())

    if tqdm_cls is not None:
        p_process = tqdm_cls(
            total=len(discovered),
            desc="Process",
            unit=" file",
            ncols=120,
            bar_format="{l_bar}{bar}| {n}/{total} [{postfix}]",
        )
    else:
        p_process = None

    try:
        for file_path in discovered:
            ext = file_path.suffix.lower()
            if ext not in SUPPORTED_EXTS or file_path.name.startswith("~$"):
                if p_process is not None:
                    p_process.update(1)
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
                    _d_obs = max(1e-5, min(1e-2, _d_obs))
                    _chunks_per_sec = chunks_written / _elapsed if _elapsed > 0.001 else 0.001
                    _est_total_chunks = _d_obs * _total_bytes
                    _est_remaining_chunks = max(0.0, _est_total_chunks - chunks_written)
                    _remaining = (
                        _est_remaining_chunks / _chunks_per_sec
                        if _chunks_per_sec > 0
                        else 0.0
                    )
                    def _fmt_sec(s: float) -> str:
                        m, sec = divmod(int(s), 60)
                        return f"{m:02d}:{sec:02d}"
                    p_process.set_postfix_str(
                        f"elapsed: {_fmt_sec(_elapsed)} · "
                        f"remaining: ~{_fmt_sec(_remaining)} · "
                        f"avg: {1000/_chunks_per_sec:.0f}ms/chunk" if _chunks_per_sec > 0 else "avg: --ms/chunk",
                        refresh=True,
                    )
                continue

            files_supported += 1

            try:
                abs_path = str(file_path.resolve())

                # Skip decision: Qdrant already has this file — no re-ingest needed.
                # _file_unchanged() removed: manifest.jsonl stale after corpus recreation. (AIStudio_186)
                if not force and abs_path in qdrant_source_paths:
                    files_skipped_unchanged += 1
                    if p_process is not None:
                        p_process.update(1)
                    continue

                t_file_start = time.time()
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
                doc_entity, doc_year, doc_fmt, doc_strategy, doc_mismatch = (
                    _extract_document_metadata(file_path)
                )

                # AIStudio_675 — per-file normalizer message
                if file_path is not None and file_path.suffix.lower() in (".htm", ".html"):
                    if doc_entity:
                        _prefix = f"[Document: {doc_entity} FY{doc_year}]" if doc_year else f"[Document: {doc_entity}]"
                        _strat_label = f" (Strategy {doc_strategy})" if doc_strategy and doc_strategy != "1a" else ""
                        _fmt_label = doc_fmt or "unknown"
                        _msg = f"[normalizer] {_fmt_label}{_strat_label} → {_prefix}"
                        if doc_mismatch:
                            _msg += f" \u26a0 entity mismatch: filename={file_path.stem[:30]}"
                    else:
                        _msg = "[normalizer] No structured header detected → unaugmented"
                    _tqdm_write(p_process, _msg)

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
                    # Format (entity + year): "[Document: JPMorgan Chase & Co. FY2025] <chunk>"
                    # Format (entity only):   "[Document: JPMorgan Chase & Co.] <chunk>"
                    # The bracketed tag is compact and unlikely to appear in
                    # organic text, reducing false-positive embedding signal.
                    if doc_entity and doc_year:
                        clean_text = f"[Document: {doc_entity} FY{doc_year}] {clean_text}"
                    elif doc_entity:
                        clean_text = f"[Document: {doc_entity}] {clean_text}"

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
                        }
                        for r in file_rows
                    ]
                    _store.upsert_chunks(
                        persist_dir=Path("."),
                        collection_name=collection_name,
                        embed_model=embed_model_eff,
                        ids=ids,
                        documents=documents,
                        metadatas=metadatas,
                    )
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
                # Per-file completion line — newline-terminated so api.py's async
                # stderr iterator sees it (tqdm's bar uses \r-updates which the
                # iterator never receives). _tqdm_write routes through pbar.write()
                # when the bar is active, preserving visual cleanliness while still
                # emitting a parseable progress signal. AIStudio_613.
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
                    p_process.update(1)
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
                    _d_obs = max(1e-5, min(1e-2, _d_obs))
                    _chunks_per_sec = chunks_written / _elapsed if _elapsed > 0.001 else 0.001
                    _est_total_chunks = _d_obs * _total_bytes
                    _est_remaining_chunks = max(0.0, _est_total_chunks - chunks_written)
                    _remaining = (
                        _est_remaining_chunks / _chunks_per_sec
                        if _chunks_per_sec > 0
                        else 0.0
                    )
                    def _fmt_sec(s: float) -> str:
                        m, sec = divmod(int(s), 60)
                        return f"{m:02d}:{sec:02d}"
                    p_process.set_postfix_str(
                        f"elapsed: {_fmt_sec(_elapsed)} · "
                        f"remaining: ~{_fmt_sec(_remaining)} · "
                        f"avg: {1000/_chunks_per_sec:.0f}ms/chunk" if _chunks_per_sec > 0 else "avg: --ms/chunk",
                        refresh=True,
                    )

            except Exception as e:
                files_failed += 1
                failures.append(
                    {"source_path": str(file_path), "reason": type(e).__name__, "detail": str(e)}
                )
                if p_process is not None:
                    p_process.update(1)
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
                    _d_obs = max(1e-5, min(1e-2, _d_obs))
                    _chunks_per_sec = chunks_written / _elapsed if _elapsed > 0.001 else 0.001
                    _est_total_chunks = _d_obs * _total_bytes
                    _est_remaining_chunks = max(0.0, _est_total_chunks - chunks_written)
                    _remaining = (
                        _est_remaining_chunks / _chunks_per_sec
                        if _chunks_per_sec > 0
                        else 0.0
                    )
                    def _fmt_sec(s: float) -> str:
                        m, sec = divmod(int(s), 60)
                        return f"{m:02d}:{sec:02d}"
                    p_process.set_postfix_str(
                        f"elapsed: {_fmt_sec(_elapsed)} · "
                        f"remaining: ~{_fmt_sec(_remaining)} · "
                        f"avg: {1000/_chunks_per_sec:.0f}ms/chunk" if _chunks_per_sec > 0 else "avg: --ms/chunk",
                        refresh=True,
                    )

    finally:
        if p_process is not None:
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
    )
