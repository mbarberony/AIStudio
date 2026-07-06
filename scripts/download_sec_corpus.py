#!/usr/bin/env python3
"""
AIStudio — SEC 10-K Corpus Downloader
Version 1.7.3

VERSION = "1.7.3"  # authoritative version — read by deploy_ops extract_version

Downloads 10-K annual filings from SEC EDGAR. Membership is no longer hardcoded:
the firm set comes from a scope file (default sec_10k_full_scope.yaml), or a single
firm via --cik / --tkr. Each downloaded filing is verified at download time for the
iXBRL entity tag the ingest pipeline relies on (dei:EntityRegistrantName), so a filing
that cannot be auto-recognized is flagged before you waste a 30-minute ingest on it.

Changelog:
- 1.7.2 — CLI-Output pass (Manuel): per-firm header gains a ▶ marker; per-file + verify
          lines unified to a 3-space indent; inter-firm blank lines removed; the 50-char
          ==== rule dropped and the --- Summary lines bulleted (·). Output-only, no logic change.
- 1.7.1 — F-011: --cik mode now uses --force_name as the label (filename slug) when provided,
          falling back to CIK_<padded> only when no --force_name given. Prevents confusing
          CIK_0000886982_10K filenames when the firm is known. F-019: --years guard added —
          values < 1900 are rejected with a clear error ("did you mean --latest N?") since they
          almost certainly represent a count, not a fiscal year. Both fixes in main() argument
          handling.
- 1.7.0 — Output wired to the shared _cli_output_ops helper (STD CLI-Output 4-glyph
          vocabulary). A skipped (already-on-disk) file is white-✓-on-yellow (succeeded,
          no new download), a fresh fetch is ✅, a fetch error is white-✗-on-red, and the
          all-filings-lack-a-tag coaching block is the yellow-✗ recoverable case. download_filing
          now returns (path, fresh_bytes) so the new `--- Summary` reports fresh-vs-present
          split + MB + elapsed + MB/s + MB/file. No download-logic change.
- 1.6.0 — (1) Write-back migrated to the unified stemless resolver: _inventory_path now
          calls _scope.discover_full (the SAME resolver the read side uses), so downloads
          write back to the canonical stemless <corpus>_full_scope.yaml — never a stale
          sec_10k_US_full_scope.yaml. DEFAULT_SCOPE_REL + the not-found hint corrected to the
          stemless name. Retires the --no-inventory workaround for the read/write stem split.
          (2) Atomic download: each filing is written to a .part temp and Path.replace()'d into
          place, so an interrupted run leaves a .part orphan (ignored by the skip-if-exists),
          never a truncated .htm. Re-running the exact command resumes — no flag.
- 1.5.0 — Inventory model simplified to the row-as-identity. (1) last_updated is now a
          date+TIME stamp (ISO seconds, e.g. 2026-06-09T17:36:42) so re-downloads are
          distinguishable within a day. (2) Inventory rows carry a modified_lei field
          (operator-corrected LEI; preserved across writes alongside lei). (3) REMOVED the
          sec_10k_entity_overrides.yaml sidecar — a --force_name assertion now lands only in
          the inventory row's `label` (the single source of entity identity). Ingest reads the
          name from the row, not a separate file. Nothing else writes a sidecar.
          (4) _inventory_path now enforces the one-inventory invariant on the write side:
          zero *_full_scope → create the default; >1 → hard error (was: silently default).
- 1.4.0 — (1) --scope now resolves a STEM via _scope_common_ops: bare 'initial_list' →
          data/corpora/sec_10k/scopes/sec_10k_initial_list_scope.yaml; a path (contains /
          or .) is still taken literally; no --scope → the corpus inventory (discover_full).
          (2) Inventory write-back: after a run, every downloaded firm is upserted (by CIK)
          into the *_full_scope inventory — label (forced label if used), cik, ticker, lei/
          modified_lei (PRESERVED if already set — hand-corrections never clobbered), and a
          stamped last_updated. The subset scope passed via --scope is READ-ONLY, never
          written. The inventory is tool-owned local data (gitignored): row data round-trips,
          an existing header comment is preserved, GLEIF later fills lei in place.
- 1.3.0 — Year selection split into two flags (AIStudio_882-adjacent). --latest N = the N
          most-recent filings by filing date (bare --latest = 1; default when neither flag
          is given = 1); --years YYYY [YYYY ...] = explicit fiscal year(s), selected by each
          filing's reportDate (periodOfReport). Mutually exclusive. get_filings now parses
          reportDate and supports both modes. BREAKING: --years changed meaning — it was an
          alias for "most-recent N", now it takes fiscal years; use --latest N for the old
          behavior (--max-results-per-firm kept as a --latest alias). A future shared
          year/period resolver is the eventual home for this logic.
- 1.2.3 — Unified-scope relocation (step 2b). Default scope renamed + relocated:
          data/corpora/sec_10k/sec_10k_US_scope.yaml -> sec_10k_US_full_scope.yaml
          (the corpus full inventory). Bring-your-own example moved to
          data/corpora/sec_10k/scopes/sec_10k_my_firms_scope.yaml. Path constants only;
          scope-resolver wiring is a later step.
- 1.2.2 — Scope-not-found message de-leaked (dropped operator-command reference); civilian-clean.
- 1.2.1 — Default scope renamed sec_10k_22_US_scope.yaml -> sec_10k_US_scope.yaml (count-less).
          Scope ships with cik|ticker|lei fields per entry (empty = fill if you have it).
- 1.2.0 — AIStudio_899 de-wire. Removed the hardcoded FIRMS list. New mutually-exclusive
          input modes: --cik <cik> | --tkr <ticker> | --scope <file.yaml> (default scope
          data/corpora/sec_10k/sec_10k_US_scope.yaml). Ticker→CIK resolved via EDGAR
          company_tickers.json. Download-time verify (default on) reads dei:EntityRegistrantName
          + dei:DocumentFiscalYearFocus from each filing and reports ✅/❌ per filing; on an
          all-❌ firm it prints a coaching error and the --force_name / --force_year remedy.
          --force_name / --force_year (single-firm modes) assert an identity when the tag is
          absent (in 1.5.0 this is recorded in the inventory row label). --no-verify to skip.
          Membership is now scope-driven; the old hardcoded firm list is removed.
- 1.1.8 — Robust size parsing in index.json (pre-de-wire).
- 1.1.6 — Multi-document filing fix: pick largest HTML doc as the main 10-K body.
- 1.1.5 — Pagination through filings.files[].

TERMS OF USE — SEC EDGAR
Data is retrieved from the U.S. Securities and Exchange Commission's EDGAR system
(https://www.sec.gov/edgar). Use is subject to SEC EDGAR's terms and conditions.
This tool identifies itself to the SEC servers as required by their fair access policy.
Do not reduce the request delay below 0.1s or run repeatedly in the same session.
All filings retrieved are public documents under SEC disclosure requirements.

Usage:
    ais_download_sec_10k                                   # default scope
    ais_download_sec_10k --tkr BNY --years 5               # single firm by ticker, verify
    ais_download_sec_10k --cik 0000886982 --years 3        # single firm by CIK
    ais_download_sec_10k --scope scopes/sec_10k_my_firms_scope.yaml   # bring your own list
    ais_download_sec_10k --tkr BNY --years 5 --force_name "The Bank of New York Mellon Corporation"
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
import yaml

# _scope_common_ops is a sibling in scripts/ — used for --scope stem resolution and to
# locate the inventory (_full_scope) write-back target. scripts/ is on sys.path when run
# directly; insert defensively for -m / odd-cwd invocations.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import _cli_output as cli  # noqa: E402  shared CLI output (glyph vocabulary)
import _scope_common as _scope  # noqa: E402

try:
    from bs4 import BeautifulSoup  # type: ignore
except Exception:  # pragma: no cover - bs4 is a venv dep, present in the AIStudio env
    BeautifulSoup = None  # type: ignore

# SEC EDGAR requires a User-Agent header identifying the caller (fair-access policy).
HEADERS = {
    "User-Agent": "AIStudio Research Tool manuel@aistudio.local",
    "Accept-Encoding": "gzip, deflate",
}

SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"

# Default scope (the membership list the bare command consumes). Corpus-attached,
# at the base of the corpus directory — NOT benchmarks/, NOT uploads/.
DEFAULT_SCOPE_REL = "data/corpora/sec_10k/sec_10k_full_scope.yaml"

# The single iXBRL tag the ingest pipeline's primary strategy reads to recognize a
# filing's entity. A filing lacking it cannot be auto-recognized at ingest (the
# BNY Mellon / Wells Fargo older-filing class: they carry dei:AuditorName but not this).
ENTITY_TAG_SUFFIX = "EntityRegistrantName"
YEAR_TAG_SUFFIX = "DocumentFiscalYearFocus"


def _repo_root() -> Path:
    """scripts/ lives one level under the repo root."""
    return Path(__file__).resolve().parent.parent


# ── Ticker → CIK resolution (EDGAR company_tickers.json) ────────────────────────
_TICKER_MAP: dict[str, tuple[str, str]] | None = None


def _load_company_tickers(delay: float = 0.5) -> dict[str, tuple[str, str]]:
    """Fetch and cache EDGAR's ticker→CIK map. Keys are upper-cased tickers;
    values are (zero-padded 10-digit CIK, company title)."""
    global _TICKER_MAP  # noqa: PLW0603
    if _TICKER_MAP is not None:
        return _TICKER_MAP
    time.sleep(delay)
    try:
        r = requests.get(TICKERS_URL, headers=HEADERS, timeout=15)
        r.raise_for_status()
        raw = r.json()
    except Exception as e:
        print(f"  [warn] Could not fetch company_tickers.json: {e}")
        _TICKER_MAP = {}
        return _TICKER_MAP
    # Shape: {"0": {"cik_str": 886982, "ticker": "GS", "title": "GOLDMAN SACHS GROUP INC"}, ...}
    mapping: dict[str, tuple[str, str]] = {}
    for row in raw.values():
        tkr = str(row.get("ticker", "")).upper().strip()
        cik = str(row.get("cik_str", "")).strip()
        if tkr and cik:
            mapping[tkr] = (cik.zfill(10), str(row.get("title", tkr)))
    _TICKER_MAP = mapping
    return _TICKER_MAP


def _resolve_ticker(ticker: str, delay: float = 0.5) -> tuple[str, str] | None:
    """Return (cik_padded, title) for a ticker, or None if unknown."""
    return _load_company_tickers(delay=delay).get(ticker.upper().strip())


# ── Scope loading (the membership file) ─────────────────────────────────────────
def _load_scope(path: Path, delay: float = 0.5) -> list[dict]:
    """Read a scope YAML into a list of {label, cik} dicts.

    Schema (per entry): a label plus ONE of cik | ticker. An optional lei is allowed
    (shared with the benchmark use of this same file) and ignored here. Tickers are
    resolved to CIK via EDGAR.
    """
    if not path.exists():
        raise SystemExit(
            f"Scope file not found: {path}\n"
            f"  Pass your own list with --scope <file.yaml> (schema: entities: [{{label, cik|ticker}}]),\n"
            f"  or restore the default scope at data/corpora/sec_10k/sec_10k_full_scope.yaml."
        )
    with open(path) as f:
        doc = yaml.safe_load(f) or {}
    entities = doc.get("entities", [])
    if not entities:
        raise SystemExit(f"Scope file has no `entities:` list: {path}")

    resolved: list[dict] = []
    for ent in entities:
        label = str(ent.get("label", "")).strip()
        cik = str(ent.get("cik", "")).strip()
        ticker = str(ent.get("ticker", "")).strip()
        if not label:
            print(f"  [warn] scope entry missing label, skipping: {ent}")
            continue
        if not cik and ticker:
            hit = _resolve_ticker(ticker, delay=delay)
            if hit is None:
                print(f"  [warn] {label}: ticker '{ticker}' not found in EDGAR map, skipping")
                continue
            cik = hit[0]
        if not cik:
            print(f"  [warn] {label}: no cik or ticker, skipping")
            continue
        resolved.append({"label": label, "cik": cik.zfill(10)})
    return resolved


# ── Inventory write-back (the *_full_scope ledger) ──────────────────────────────
_INVENTORY_HEADER = (
    "# SEC 10-K corpus inventory — the running ledger of every firm downloaded.\n"
    "# Maintained by ais_download_sec_10k: rows are upserted by CIK on each download and\n"
    "# the `last_updated` field is stamped per touched row. Hand-edit `lei` (and labels)\n"
    "# as needed — row data round-trips across tool writes, so corrections are preserved.\n"
    "# This file is the default download membership and the entity source for\n"
    "# ais_import_knowledge_base (GLEIF). Tool-owned local data (gitignored).\n"
)


def _inventory_path() -> Path:
    """The single stemless <corpus>_full_scope inventory to write firms back into — resolved
    by the SAME function the read side uses (_scope.discover_full), so read and write can never
    diverge on the filename. Exactly one → use it; zero → the canonical stemless default,
    created on first write. (>1 is impossible: discover_full globs the exact stemless name.)"""
    try:
        return _scope.discover_full("sec_10k")
    except _scope.ScopeError:
        return _repo_root() / DEFAULT_SCOPE_REL  # zero → create the canonical default on write


def _read_inventory_header(path: Path) -> str:
    """Preserve an existing file's leading comment block (everything before `entities:`);
    fall back to the canonical header for a fresh inventory."""
    if path.exists():
        head: list[str] = []
        for ln in path.read_text().splitlines(keepends=True):
            if ln.lstrip().startswith("entities:"):
                break
            head.append(ln)
        if any(h.strip() for h in head):
            return "".join(head)
    return _INVENTORY_HEADER


def _upsert_inventory(learned: list[dict]) -> tuple[Path, int, int]:
    """Merge downloaded firms into the inventory, keyed by CIK. Preserves every existing
    row field (especially a hand-corrected `lei`); only sets label (when changed/forced),
    fills an absent ticker, and stamps last_updated. Returns (path, n_added, n_touched).
    Read-only on the subset scope — this only ever writes the *_full_scope inventory."""
    path = _inventory_path()
    rows: list[dict] = []
    if path.exists():
        doc = yaml.safe_load(path.read_text()) or {}
        rows = doc.get("entities", []) or []
    by_cik = {str(r.get("cik", "")).zfill(10): r for r in rows if r.get("cik")}
    stamp = datetime.now().isoformat(timespec="seconds")  # date+time, e.g. 2026-06-09T17:36:42
    added = touched = 0
    for f in learned:
        cik = str(f["cik"]).zfill(10)
        if cik in by_cik:
            r = by_cik[cik]
            if f.get("label"):
                r["label"] = f["label"]  # honor forced/scope label on re-download
            if f.get("ticker") and not r.get("ticker"):
                r["ticker"] = f["ticker"]
            r["last_updated"] = stamp  # lei/modified_lei + any enrichment preserved untouched
            touched += 1
        else:
            rows.append(
                {
                    "label": f.get("label", ""),
                    "cik": cik,
                    "ticker": f.get("ticker", ""),
                    "lei": "",
                    "modified_lei": "",
                    "last_updated": stamp,
                }
            )
            by_cik[cik] = rows[-1]
            added += 1
    header = _read_inventory_header(path)
    body = yaml.safe_dump({"entities": rows}, sort_keys=False, allow_unicode=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(header + body)
    return path, added, touched


# ── EDGAR filing retrieval (unchanged proven logic) ─────────────────────────────
def get_filings(
    cik: str,
    form_type: str = "10-K",
    *,
    max_results: int | None = None,
    years: set[int] | None = None,
    delay: float = 0.5,
) -> list:
    """Fetch 10-K filing metadata from EDGAR for a CIK (recent block, then paginate).

    Exactly one selection mode:
      - max_results=N : the N most-recent filings by filing date (the pre-1.3.0 behavior).
      - years={YYYY,…}: every filing whose fiscal period (reportDate / periodOfReport) year
                        is in the set. Scans until all requested years are found or the
                        submissions history is exhausted.
    """
    cik_padded = cik.zfill(10)
    url = SUBMISSIONS_URL.format(cik=cik_padded)
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"  [warn] Could not fetch submissions for CIK {cik}: {e}")
        return []

    results: list[dict] = []
    _years = set(years) if years else None
    _found_years: set[int] = set()

    def _want_more() -> bool:
        # years mode: keep scanning until every requested year is located;
        # latest mode: stop once max_results filings are collected.
        if _years is not None:
            return not _years.issubset(_found_years)
        return len(results) < (max_results or 0)

    def _extract(block: dict) -> None:
        forms = block.get("form", [])
        accessions = block.get("accessionNumber", [])
        dates = block.get("filingDate", [])
        report_dates = block.get("reportDate", [])  # 1.3.0: periodOfReport (fiscal period end)
        primary_docs = block.get("primaryDocument", [])
        for i, form in enumerate(forms):
            if form != form_type:
                continue
            if not _want_more():
                break
            rdate = report_dates[i] if i < len(report_dates) else ""
            fdate = dates[i] if i < len(dates) else ""
            entry = {
                "accession": accessions[i].replace("-", ""),
                "accession_raw": accessions[i],
                "date": fdate,
                "report_date": rdate,  # 1.3.0
                "primary_doc": primary_docs[i],
                "cik": cik_padded,
            }
            if _years is not None:
                _yr = (rdate or fdate)[:4]
                if _yr.isdigit() and int(_yr) in _years:
                    results.append(entry)
                    _found_years.add(int(_yr))
            else:
                results.append(entry)

    _extract(data.get("filings", {}).get("recent", {}))
    if _want_more():
        for entry in data.get("filings", {}).get("files", []):
            if not _want_more():
                break
            time.sleep(delay)
            try:
                r = requests.get(
                    f"https://data.sec.gov/submissions/{entry['name']}", headers=HEADERS, timeout=15
                )
                r.raise_for_status()
                _extract(r.json())
            except Exception as e:
                print(f"  [warn] Could not fetch {entry['name']}: {e}")
                continue
    return results


def _pick_main_document(cik: str, accession: str, primary_doc: str, delay: float = 0.1) -> str:
    """Pick the largest .htm/.html document in the filing index (the main 10-K body)."""
    index_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession}/index.json"
    time.sleep(delay)
    try:
        r = requests.get(index_url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        idx = r.json()
    except Exception as e:
        print(f"  [warn] Could not fetch filing index for {accession}: {e} — using primary_doc")
        return primary_doc

    items = idx.get("directory", {}).get("item", [])

    def _safe_size(item: dict) -> int:
        s = item.get("size", "")
        try:
            return int(s) if s else 0
        except (ValueError, TypeError):
            return 0

    html_docs = [
        item
        for item in items
        if item.get("name", "").lower().endswith((".htm", ".html")) and _safe_size(item) > 0
    ]
    if not html_docs:
        print("  [warn] No HTML documents in filing index — using primary_doc")
        return primary_doc
    return max(html_docs, key=_safe_size).get("name", primary_doc)


def download_filing(
    filing: dict, label: str, out_dir: Path, delay: float = 0.5
) -> tuple[Path | None, int]:
    """Download the main 10-K document.

    Returns (saved_path | None, fresh_bytes) — fresh_bytes is 0 on skip/fail, so the
    caller can total real download volume for the summary (skips add nothing).
    """
    acc, cik, primary_doc, date = (
        filing["accession"],
        filing["cik"],
        filing["primary_doc"],
        filing["date"],
    )
    doc = _pick_main_document(cik, acc, primary_doc, delay=delay)
    base_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc}/{doc}"
    safe_name = label.replace(" ", "_").replace("/", "_")
    out_file = out_dir / f"{safe_name}_10K_{date}.htm"
    tmp_file = out_file.with_name(out_file.name + ".part")

    if out_file.exists():
        # Succeeded, but no new file fetched → degraded-success (white ✓ on yellow).
        cli.partial(f"{out_file.name} — already on disk, no new download", indent=3)
        return out_file, 0
    try:
        r = requests.get(base_url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        # Atomic publish: write to a .part temp, then rename into place. An interrupted run
        # leaves the .part orphan (ignored by the skip-if-exists above), never a truncated
        # .htm — so re-running the exact command resumes with no flag.
        tmp_file.write_bytes(r.content)
        tmp_file.replace(out_file)
        cli.ok(f"{out_file.name} ({len(r.content) / 1024:.0f} KB)", indent=3)
        return out_file, len(r.content)
    except Exception as e:
        if tmp_file.exists():
            tmp_file.unlink()
        cli.fail(f"{label} {date}: {e}", indent=3)
        return None, 0


# ── Download-time verify (predicts ingest recognition) ──────────────────────────
def _verify_filing(html_path: Path) -> tuple[str | None, str | None]:
    """Read the iXBRL entity + fiscal-year tags from a downloaded filing.

    Matches the ingest pipeline's PRIMARY recognition strategy: locate the inline-XBRL
    fact whose `name` attribute ends in EntityRegistrantName / DocumentFiscalYearFocus.
    (The pipeline has additional fallback strategies; this checks the mandatory tag whose
    absence is exactly the BNY/Wells-Fargo older-filing failure class.)

    Returns (entity_name | None, fiscal_year | None).
    """
    if BeautifulSoup is None:
        return (None, None)
    try:
        soup = BeautifulSoup(html_path.read_bytes(), "html.parser")
    except Exception:
        return (None, None)

    def _find(suffix: str) -> str | None:
        tag = soup.find(attrs={"name": lambda v: bool(v) and v.endswith(suffix)})
        if tag is None:
            return None
        text = tag.get_text(strip=True)
        return text or None

    return (_find(ENTITY_TAG_SUFFIX), _find(YEAR_TAG_SUFFIX))


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ais_download_sec_10k",
        description="AIStudio — SEC 10-K Corpus Downloader | Version 1.7.2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  ais_download_sec_10k                                # default scope, latest 1\n"
            "  ais_download_sec_10k --latest 3                     # 3 most-recent per firm\n"
            "  ais_download_sec_10k --years 2024                   # fiscal year 2024 only\n"
            "  ais_download_sec_10k --years 2024 2025              # FY2024 and FY2025\n"
            "  ais_download_sec_10k --tkr BNY --latest 1          # single firm by ticker\n"
            "  ais_download_sec_10k --cik 0000886982 --years 2024 # single firm, one FY\n"
            "  ais_download_sec_10k --scope scopes/sec_10k_my_firms_scope.yaml   # bring your own list\n"
            "\nafter download: ais_ingest_sec_10k\n"
        ),
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--cik", help="Single firm by CIK (10-digit, zero-padded ok)")
    mode.add_argument("--tkr", help="Single firm by ticker (resolved to CIK via EDGAR)")
    mode.add_argument(
        "--scope",
        help="Scope YAML listing firms (schema: entities: [{label, cik|ticker}]). "
        f"Default: {DEFAULT_SCOPE_REL}",
    )
    parser.add_argument("--out", default="~/Downloads/sec_10k", help="Output directory")
    # Year selection — exactly one of --latest / --years (default: --latest 1).
    year_sel = parser.add_mutually_exclusive_group()
    year_sel.add_argument(
        "--latest",
        "--max-results-per-firm",
        dest="latest",
        nargs="?",
        const=1,
        type=int,
        default=None,
        metavar="N",
        help="The N most-recent 10-K filings per firm, by filing date. Bare --latest = 1. "
        "Default when neither --latest nor --years is given: 1.",
    )
    year_sel.add_argument(
        "--years",
        dest="years",
        nargs="+",
        type=int,
        default=None,
        metavar="YYYY",
        help="Explicit fiscal year(s), e.g. --years 2024  or  --years 2024 2025. Selects "
        "filings by their fiscal period (reportDate). Mutually exclusive with --latest. "
        "(Note: --years changed meaning in 1.3.0 — it used to mean 'latest N'; that is "
        "now --latest N.)",
    )
    parser.add_argument("--delay", type=float, default=0.5, help="Request delay (min 0.1)")
    parser.add_argument(
        "--no-inventory",
        dest="no_inventory",
        action="store_true",
        help="Skip the *_full_scope inventory write-back (download files only; "
        "used by the test harness so throwaway runs don't touch the ledger).",
    )
    parser.add_argument(
        "--no-verify", action="store_true", help="Skip the download-time iXBRL tag check"
    )
    parser.add_argument(
        "--force_name", help="Assert entity name when the tag is absent (single-firm modes)"
    )
    parser.add_argument(
        "--force_year", help="Assert fiscal year when the tag is absent (single-firm modes)"
    )
    args = parser.parse_args()

    if (args.force_name or args.force_year) and args.scope:
        parser.error(
            "--force_name / --force_year apply to single-firm modes (--cik/--tkr), not --scope"
        )

    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Year selection: explicit --years wins; otherwise --latest N (default 1).
    if args.years:
        # F-019 guard: --years expects 4-digit fiscal years (e.g. 2024 2023).
        # A value < 1900 almost certainly means the user intended --latest N.
        _bad = [y for y in args.years if y < 1900]
        if _bad:
            bad_str = ", ".join(str(y) for y in _bad)
            raise SystemExit(
                f"❌  --years value(s) look like a count, not a fiscal year: {bad_str}\n"
                f"   --years expects 4-digit years: --years 2024  or  --years 2024 2023\n"
                f"   For the N most-recent filings use: --latest {_bad[0]}"
            )
        sel_years: set[int] | None = set(args.years)
        latest_n: int | None = None
        sel_label = "fiscal year(s) " + ", ".join(str(y) for y in sorted(sel_years))
    else:
        sel_years = None
        latest_n = args.latest if args.latest is not None else 1
        sel_label = f"the {latest_n} most-recent filing(s)"

    # Resolve the firm set from the chosen mode.
    targets: list[dict] = []
    if args.cik:
        # F-011: prefer --force_name label > CIK_ fallback.
        # CIK_ slug was confusing (e.g. CIK_0000886982 instead of Goldman_Sachs).
        _cik_label = (
            args.force_name.strip()
            if getattr(args, "force_name", None)
            else f"CIK_{args.cik.zfill(10)}"
        )
        targets = [{"label": _cik_label, "cik": args.cik.zfill(10)}]
    elif args.tkr:
        hit = _resolve_ticker(args.tkr, delay=args.delay)
        if hit is None:
            raise SystemExit(f"Ticker '{args.tkr}' not found in EDGAR company_tickers.json")
        cik, title = hit
        targets = [{"label": title, "cik": cik, "ticker": args.tkr.upper().strip()}]
    else:
        # --scope: a bare stem resolves via _scope_common_ops to
        # scopes/sec_10k_<stem>_scope.yaml; a value containing / or . is a literal path;
        # no --scope → the corpus inventory (discover_full). The resolved scope is READ-ONLY.
        try:
            if args.scope:
                _is_stem = not any(c in args.scope for c in "/\\.")
                scope_path = (
                    _scope.resolve_scope_file("sec_10k", stem=args.scope)
                    if _is_stem
                    else _scope.resolve_scope_file("sec_10k", path=args.scope)
                )
            else:
                scope_path = _scope.discover_full("sec_10k")
        except _scope.ScopeError as e:
            raise SystemExit(f"--scope could not be resolved:\n{e}") from e
        targets = _load_scope(scope_path, delay=args.delay)

    print(f"Output directory: {out_dir}")
    print(f"Targeting {len(targets)} firm(s) × {sel_label}")

    total_ok = total_fail = total_fresh = 0
    total_bytes = 0
    t0 = time.time()
    learned: list[dict] = []  # firms with >=1 file on disk this run → upserted into inventory
    for t in targets:
        label, cik = t["label"], t["cik"]
        print(f"▶ {label} (CIK: {cik})")
        filings = get_filings(cik, max_results=latest_n, years=sel_years, delay=args.delay)
        if not filings:
            if sel_years:
                print(f"   [warn] No 10-K filings found for {sel_label}")
            else:
                print("   [warn] No 10-K filings found")
            total_fail += 1
            continue

        # years mode: flag any requested year this firm didn't file.
        if sel_years:
            _got = {
                int((f["report_date"] or f["date"])[:4])
                for f in filings
                if (f["report_date"] or f["date"])[:4].isdigit()
            }
            _missing = sorted(sel_years - _got)
            if _missing:
                print(
                    f"   [warn] {label}: no 10-K for fiscal year(s) {', '.join(map(str, _missing))}"
                )

        firm_ok = False
        verify_results: list[tuple[str, bool]] = []  # (date, has_entity_tag)
        for filing in filings:
            saved, nbytes = download_filing(filing, label, out_dir, delay=args.delay)
            if saved is None:
                total_fail += 1
                continue
            total_ok += 1
            if nbytes:
                total_fresh += 1
                total_bytes += nbytes
            firm_ok = True

            if args.no_verify:
                continue
            entity, year = _verify_filing(saved)
            has_tag = entity is not None
            verify_results.append((filing["date"], has_tag))
            if has_tag:
                yr = year or "?"
                cli.ok(f"verify: entity tag present ({entity} FY{yr})", indent=3)
            elif args.force_name:
                cli.partial(
                    f"forced: no entity tag — asserting '{args.force_name}'"
                    + (f" FY{args.force_year}" if args.force_year else "")
                    + " (recorded as the inventory row label)",
                    indent=3,
                )
            else:
                cli.fail("verify: no dei:EntityRegistrantName tag", indent=3)
            time.sleep(args.delay)

        # Record for inventory write-back: forced label wins (operator's assertion).
        if firm_ok:
            learned.append(
                {
                    "label": args.force_name or label,
                    "cik": cik,
                    "ticker": t.get("ticker", ""),
                }
            )

        # Coaching: every downloaded filing for this firm lacks the entity tag, not forced.
        # This is the recoverable-failure case (yellow ✗): no automated fix, but the operator
        # has a documented override.
        if verify_results and not any(has for _, has in verify_results) and not args.force_name:
            years_str = ", ".join(d[:4] for d, _ in verify_results)
            ident = (
                f"--tkr {args.tkr}"
                if args.tkr
                else (f"--cik {cik}" if args.cik else f'--scope (entry "{label}")')
            )
            _yflag = (
                ("--years " + " ".join(str(y) for y in sorted(sel_years)))
                if sel_years
                else f"--latest {latest_n}"
            )
            cli.fail_recover(
                f"{label}: none of the downloaded filings ({years_str}) carry an "
                f"iXBRL entity tag (dei:EntityRegistrantName) — ingest can't "
                f"auto-recognize them.",
                indent=3,
            )
            print(
                f"      Override:  ais_download_sec_10k {ident} {_yflag} "
                f'--force_name "<name to use>" [--force_year <YYYY>]'
            )
            print("      But find out *why* the tag is missing first — see Tutorial Annex 1.")

    elapsed = time.time() - t0
    mb = total_bytes / 1_048_576
    print()
    cli.section("Summary")
    print(
        f"   · On disk:  {total_ok} filing(s)  ·  {total_fresh} newly fetched, "
        f"{total_ok - total_fresh} already present"
    )
    if total_fail:
        print(f"   · Failed:   {total_fail}")
    if total_fresh and elapsed > 0:
        print(
            f"   · Fetched:  {mb:.1f} MB in {elapsed:.0f}s  ·  {mb / elapsed:.2f} MB/s  ·  "
            f"{mb / total_fresh:.2f} MB/file avg"
        )
    else:
        print(f"   · Elapsed:  {elapsed:.0f}s (no new downloads)")
    print(f"   · Output:   {out_dir}")

    # Inventory write-back — upsert downloaded firms into the *_full_scope ledger.
    # Read-only on any subset scope passed via --scope; preserves hand-corrected lei.
    # --no-inventory suppresses it (throwaway / files-only runs, e.g. the test harness).
    if learned and not args.no_inventory:
        inv_path, n_added, n_touched = _upsert_inventory(learned)
        try:
            _rel = inv_path.relative_to(_repo_root())
        except ValueError:
            _rel = inv_path
        print(f"   · Inventory: {_rel}  (+{n_added} new, {n_touched} updated)")

    print(
        "\nNext steps (all in the Terminal — see TUTORIAL Module 2):"
        "\n   1. ais_import_entity_kb --corpus sec_10k --apply    (build the entity KB)"
        "\n   2. ais_import_glossary_kb --source bis_basel         (build the glossary KB)"
        "\n   3. ais_ingest_sec_10k                                (ingest into AIStudio)"
        "\nThen query the corpus in the AIStudio UI, or benchmark it with ais_bench --corpus sec_10k."
    )


if __name__ == "__main__":
    sys.exit(main())
