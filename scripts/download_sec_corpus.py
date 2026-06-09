#!/usr/bin/env python3
"""
AIStudio — SEC 10-K Corpus Downloader
Version 1.2.2

Downloads 10-K annual filings from SEC EDGAR. Membership is no longer hardcoded:
the firm set comes from a scope file (default sec_10k_US_scope.yaml), or a single
firm via --cik / --tkr. Each downloaded filing is verified at download time for the
iXBRL entity tag the ingest pipeline relies on (dei:EntityRegistrantName), so a filing
that cannot be auto-recognized is flagged before you waste a 30-minute ingest on it.

Changelog:
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
          absent and record it to a sidecar overrides file. --no-verify to skip the check.
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
    ais_download_sec_10k --scope my_firms.yaml             # bring your own list
    ais_download_sec_10k --tkr BNY --years 5 --force_name "The Bank of New York Mellon Corporation"
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import requests
import yaml

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
DEFAULT_SCOPE_REL = "data/corpora/sec_10k/sec_10k_US_scope.yaml"

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
            f"  or restore the default scope at data/corpora/sec_10k/sec_10k_US_scope.yaml."
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


# ── EDGAR filing retrieval (unchanged proven logic) ─────────────────────────────
def get_filings(cik: str, form_type: str = "10-K", max_results: int = 5, delay: float = 0.5) -> list:
    """Fetch filing metadata from EDGAR for a given CIK (recent block, then paginate)."""
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

    def _extract(block: dict) -> None:
        forms = block.get("form", [])
        accessions = block.get("accessionNumber", [])
        dates = block.get("filingDate", [])
        primary_docs = block.get("primaryDocument", [])
        for i, form in enumerate(forms):
            if form == form_type and len(results) < max_results:
                results.append(
                    {
                        "accession": accessions[i].replace("-", ""),
                        "accession_raw": accessions[i],
                        "date": dates[i],
                        "primary_doc": primary_docs[i],
                        "cik": cik_padded,
                    }
                )

    _extract(data.get("filings", {}).get("recent", {}))
    if len(results) < max_results:
        for entry in data.get("filings", {}).get("files", []):
            if len(results) >= max_results:
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


def download_filing(filing: dict, label: str, out_dir: Path, delay: float = 0.5) -> Path | None:
    """Download the main 10-K document; return the saved path (or None on failure)."""
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

    if out_file.exists():
        print(f"  [skip] {out_file.name} already exists")
        return out_file
    try:
        r = requests.get(base_url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        out_file.write_bytes(r.content)
        print(f"  [ok]   {out_file.name} ({len(r.content) / 1024:.0f} KB)")
        return out_file
    except Exception as e:
        print(f"  [fail] {label} {date}: {e}")
        return None


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


def _write_override(out_dir: Path, filename: str, force_name: str | None, force_year: str | None) -> None:
    """Record an operator-asserted identity to a sidecar at the corpus base.

    NOTE: ingest honoring this override is the paired worksheet/ingest step (Annex 1,
    name-extraction lever) and is NOT wired yet — this preserves the assertion so it
    isn't lost between download and ingest.
    """
    corpus_base = out_dir.parent  # uploads/ -> corpus base
    sidecar = corpus_base / "sec_10k_entity_overrides.yaml"
    data = {}
    if sidecar.exists():
        with open(sidecar) as f:
            data = yaml.safe_load(f) or {}
    data.setdefault("overrides", {})
    entry: dict[str, str] = {}
    if force_name:
        entry["force_name"] = force_name
    if force_year:
        entry["force_year"] = str(force_year)
    data["overrides"][filename] = entry
    with open(sidecar, "w") as f:
        f.write("# sec_10k_entity_overrides.yaml — operator-asserted identities for filings\n")
        f.write("# lacking dei:EntityRegistrantName. Consumed at ingest (paired step, AIStudio_899).\n")
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)
    print(f"  [override] recorded {filename} → {entry} in {sidecar.name}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ais_download_sec_10k",
        description="AIStudio — SEC 10-K Corpus Downloader | Version 1.2.2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  ais_download_sec_10k                                # default scope\n"
            "  ais_download_sec_10k --tkr BNY --years 5            # single firm by ticker\n"
            "  ais_download_sec_10k --cik 0000886982 --years 3    # single firm by CIK\n"
            "  ais_download_sec_10k --scope my_firms.yaml         # bring your own list\n"
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
    parser.add_argument(
        "--years",
        "--max-results-per-firm",
        dest="years",
        type=int,
        default=5,
        help="Most recent filings per firm (default: 5)",
    )
    parser.add_argument("--delay", type=float, default=0.5, help="Request delay (min 0.1)")
    parser.add_argument("--no-verify", action="store_true", help="Skip the download-time iXBRL tag check")
    parser.add_argument("--force_name", help="Assert entity name when the tag is absent (single-firm modes)")
    parser.add_argument("--force_year", help="Assert fiscal year when the tag is absent (single-firm modes)")
    args = parser.parse_args()

    if (args.force_name or args.force_year) and args.scope:
        parser.error("--force_name / --force_year apply to single-firm modes (--cik/--tkr), not --scope")

    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Resolve the firm set from the chosen mode.
    targets: list[dict] = []
    if args.cik:
        targets = [{"label": f"CIK_{args.cik.zfill(10)}", "cik": args.cik.zfill(10)}]
    elif args.tkr:
        hit = _resolve_ticker(args.tkr, delay=args.delay)
        if hit is None:
            raise SystemExit(f"Ticker '{args.tkr}' not found in EDGAR company_tickers.json")
        cik, title = hit
        targets = [{"label": title, "cik": cik}]
    else:
        scope_path = Path(args.scope).expanduser() if args.scope else (_repo_root() / DEFAULT_SCOPE_REL)
        targets = _load_scope(scope_path, delay=args.delay)

    print(f"Output directory: {out_dir}")
    print(f"Targeting {len(targets)} firm(s) × up to {args.years} filings each\n")

    total_ok = total_fail = 0
    for t in targets:
        label, cik = t["label"], t["cik"]
        print(f"\n{label} (CIK: {cik})")
        filings = get_filings(cik, max_results=args.years, delay=args.delay)
        if not filings:
            print("  [warn] No 10-K filings found")
            total_fail += 1
            continue

        verify_results: list[tuple[str, bool]] = []  # (date, has_entity_tag)
        for filing in filings:
            saved = download_filing(filing, label, out_dir, delay=args.delay)
            if saved is None:
                total_fail += 1
                continue
            total_ok += 1

            if args.no_verify:
                continue
            entity, year = _verify_filing(saved)
            has_tag = entity is not None
            verify_results.append((filing["date"], has_tag))
            if has_tag:
                yr = year or "?"
                print(f"         ✅ verify: entity tag present ({entity} FY{yr})")
            elif args.force_name:
                print(f"         ⚠ forced : no entity tag — asserting '{args.force_name}'"
                      + (f" FY{args.force_year}" if args.force_year else ""))
                _write_override(out_dir, saved.name, args.force_name, args.force_year)
            else:
                print("         ❌ verify: no dei:EntityRegistrantName tag")
            time.sleep(args.delay)

        # Coaching: every downloaded filing for this firm lacks the entity tag, not forced.
        if verify_results and not any(has for _, has in verify_results) and not args.force_name:
            years_str = ", ".join(d[:4] for d, _ in verify_results)
            ident = f"--tkr {args.tkr}" if args.tkr else (f"--cik {cik}" if args.cik else f'--scope (entry "{label}")')
            print(
                f"\n  ❌ {label}: none of the downloaded filings ({years_str}) carry an iXBRL\n"
                f"     entity tag (dei:EntityRegistrantName), so ingest can't auto-recognize them.\n"
                f"     You can override:\n"
                f"       ais_download_sec_10k {ident} --years {args.years} "
                f'--force_name "<name to use>" [--force_year <YYYY>]\n'
                f"     But it's worth finding out *why* the filing lacks the tag first — see Tutorial Annex 1."
            )

    print(f"\n{'=' * 50}")
    print(f"Downloaded: {total_ok} filings")
    print(f"Failed:     {total_fail}")
    print(f"Output:     {out_dir}")
    print("\nTo ingest these files into AIStudio, run:\n  ais_ingest_sec_10k")


if __name__ == "__main__":
    sys.exit(main())
