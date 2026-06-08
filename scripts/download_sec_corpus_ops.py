#!/usr/bin/env python3
"""
AIStudio — SEC 10-K Corpus Downloader (OPS)
Version 1.2.1

Operator variant of download_sec_corpus.py. Same EDGAR download logic, plus a
--cik flag to download a SINGLE firm's filings surgically — e.g. to replace the
contaminated CBOE documents (AIStudio_667) without re-running the full 25-firm set.

Downloads 10-K annual filings from major financial services firms via SEC EDGAR.
Files are saved to data/corpora/sec_10k/uploads/ by default. Ingest with
ais_ingest_sec_10k.

Changelog:
- 1.2.1 — Wire as command ais_download_sec_10k_ops (prog/usage updated). --out default
          changed to data/corpora/sec_10k/uploads (this tool is sec_10k-only; wrapper
          cd's to repo root so the relative default resolves there). §7 passthrough:
          defaults live here in argparse, per Command Dev STD §0.
- 1.2.0 — OPS fork of download_sec_corpus.py v1.1.9 (carries the AIStudio_667 CBOE
          CIK fix). Adds --cik <cik> to download only one firm's filings, and
          --name to set its output filename. When --cik is given, the FIRMS list
          is bypassed; the firm name resolves as --name > FIRMS match (by padded
          CIK) > EDGAR submissions 'name' > CIK_<cik>. Use case: surgical
          re-download (delete the bad files first — existing files are skipped).
- 1.1.9 — AIStudio_667: fix CBOE Global Markets CIK 0001374690 → 0001374310.
          The old CIK is Larimar Therapeutics (biotech) — every "CBOE" filing
          downloaded was actually a Larimar 10-K, across all years. Correct Cboe
          CIK (formerly CBOE Holdings) verified at SEC EDGAR. Re-download + re-ingest
          required to replace the contaminated CBOE documents.
- 1.1.8 — Robust size parsing in index.json: empty strings, missing keys, non-numeric
          values now safely coerce to 0. Filter out zero-size entries (index/header
          files have size=""). Was crashing on ValueError: invalid literal for int().
- 1.1.7 — Fix index.json URL pattern (was building <acc>-index.json, actual is index.json).
          Also lint fix: drop f-string with no placeholders.
- 1.1.6 — Multi-document filing fix: inspect filing index.json to pick the largest
          HTML document as the main 10-K body (was: blindly using primary_doc which
          for some filers, e.g. Wells Fargo recent years, is only one segment).
- 1.1.5 — Pagination through filings.files[]; BNY/Stifel CIK fixes.
- 1.1.4 — Wrapper $SCRIPT_DIR fix; --max-results-per-firm rename.

TERMS OF USE — SEC EDGAR
Data is retrieved from the U.S. Securities and Exchange Commission's EDGAR system
(https://www.sec.gov/edgar). Use is subject to SEC EDGAR's terms and conditions.
This tool identifies itself to the SEC servers as required by their fair access policy.
Do not run this tool more than once per session or modify the request delay below 0.1s.
All filings retrieved are public documents under SEC disclosure requirements.

Usage:
    ais_download_sec_10k_ops                                    # all 25 firms × 5 filings
    ais_download_sec_10k_ops --cik 0001374310                   # single firm (5 most-recent 10-Ks)
    ais_download_sec_10k_ops --cik 0001374310 --name "CBOE Global Markets"  # set output name
    ais_download_sec_10k_ops --out ~/Downloads/mydir            # override output folder
    ais_download_sec_10k_ops --help                             # show all options
"""

import argparse
import time
from pathlib import Path

import requests

# SEC EDGAR requires a User-Agent header identifying yourself
HEADERS = {
    "User-Agent": "AIStudio Research Tool manuel@aistudio.local",
    "Accept-Encoding": "gzip, deflate",
}

# Target firms — mix of banks, asset managers, hedge funds, exchanges
# Format: (company name, CIK number)
# Removed firms (no domestic 10-K filer): Barclays/Deutsche Bank (foreign, file 20-F),
# Vanguard/Fidelity (privately held), Nuveen (TIAA subsidiary, no own 10-K).
FIRMS = [
    # Bulge bracket banks
    ("Goldman Sachs", "0000886982"),
    ("Morgan Stanley", "0000895421"),
    ("JPMorgan Chase", "0000019617"),
    ("Citigroup", "0000831001"),
    ("Bank of America", "0000070858"),
    ("Wells Fargo", "0000072971"),
    # Asset managers
    ("BlackRock", "0001364742"),
    ("T Rowe Price", "0001113169"),
    ("Franklin Templeton", "0000038777"),
    ("Invesco", "0000914208"),
    ("AllianceBernstein", "0000825313"),
    # Exchanges & infrastructure
    ("CME Group", "0001156375"),
    ("Intercontinental Exchange", "0001571949"),
    ("Nasdaq", "0001120193"),
    ("CBOE Global Markets", "0001374310"),
    # Insurance / diversified
    ("AIG", "0000005272"),
    ("MetLife", "0001099219"),
    ("Prudential Financial", "0001137774"),
    ("Travelers", "0000086312"),
    # Custody / services
    ("BNY Mellon", "0001390777"),
    ("State Street", "0000093751"),
    ("Northern Trust", "0000073124"),
    # Boutiques / specialty
    ("Jefferies", "0000096223"),
    ("Raymond James", "0000720005"),
    ("Stifel Financial", "0000720672"),
]

# 25 firms × 5 filings each = up to 125 documents


def get_filings(cik: str, form_type: str = "10-K", max_results: int = 3, delay: float = 0.5) -> list:
    """Fetch filing metadata from EDGAR for a given CIK.

    Reads filings.recent first; if max_results not yet met, paginates through
    filings.files[] (older submission archives) until satisfied or exhausted.
    """
    cik_padded = cik.zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"  [warn] Could not fetch submissions for CIK {cik}: {e}")
        return []

    results = []

    def _extract(block: dict) -> None:
        """Append matching form_type filings from a submissions block to results."""
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

    # Walk recent block first
    _extract(data.get("filings", {}).get("recent", {}))

    # Paginate through older archives if needed
    if len(results) < max_results:
        files_list = data.get("filings", {}).get("files", [])
        for entry in files_list:
            if len(results) >= max_results:
                break
            file_url = f"https://data.sec.gov/submissions/{entry['name']}"
            time.sleep(delay)
            try:
                r = requests.get(file_url, headers=HEADERS, timeout=15)
                r.raise_for_status()
                _extract(r.json())
            except Exception as e:
                print(f"  [warn] Could not fetch {entry['name']}: {e}")
                continue

    return results


def _pick_main_document(cik: str, accession: str, primary_doc: str, delay: float = 0.1) -> str:
    """Inspect a filing's index.json and return the filename of the main 10-K body.

    SEC filings can be split across multiple HTML documents (e.g., Wells Fargo
    2026 filings split into _d1, _d2 segments). The "primary_doc" returned by the
    submissions API is sometimes just one segment, not the full filing.

    Strategy: fetch the per-accession index.json which lists ALL documents in the
    filing with their sizes. Pick the largest .htm/.html document — that's almost
    always the main 10-K body. Fall back to primary_doc on any error.

    Args:
        cik: CIK number (no padding)
        accession: Accession number with hyphens stripped (e.g., '000007297126000007')
        primary_doc: Filename returned by submissions API; used as fallback
        delay: Sleep before request to respect SEC rate limit
    """
    index_url = (
        f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/"
        f"{accession}/index.json"
    )

    time.sleep(delay)
    try:
        r = requests.get(index_url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        idx = r.json()
    except Exception as e:
        print(f"  [warn] Could not fetch filing index for {accession}: {e}")
        print(f"         Falling back to primary_doc: {primary_doc}")
        return primary_doc

    # The index.json structure is: {"directory": {"item": [{name, size, type, ...}, ...]}}
    # Note: size can be "" (empty string) for index/header files — must coerce safely.
    items = idx.get("directory", {}).get("item", [])

    def _safe_size(item: dict) -> int:
        s = item.get("size", "")
        try:
            return int(s) if s else 0
        except (ValueError, TypeError):
            return 0

    html_docs = [
        item for item in items
        if item.get("name", "").lower().endswith((".htm", ".html"))
        and _safe_size(item) > 0  # exclude empty index/header pages
    ]
    if not html_docs:
        print("  [warn] No HTML documents in filing index — using primary_doc")
        return primary_doc

    # Pick the largest HTML doc — that's the main 10-K body in nearly all cases
    largest = max(html_docs, key=_safe_size)
    chosen = largest.get("name", primary_doc)

    if chosen != primary_doc:
        primary_size = next(
            (_safe_size(item) for item in items if item.get("name") == primary_doc),
            0,
        )
        chosen_size = _safe_size(largest)
        print(
            f"  [info] Multi-doc filing: chose {chosen} ({chosen_size:,} bytes) "
            f"over primary_doc {primary_doc} ({primary_size:,} bytes)"
        )

    return chosen


def download_filing(filing: dict, company: str, out_dir: Path, delay: float = 0.5) -> bool:
    """Download the main 10-K document from a filing.

    Inspects the filing's index.json to pick the largest HTML document, which
    handles multi-document filings correctly (e.g., Wells Fargo recent years).
    """
    acc = filing["accession"]
    cik = filing["cik"]
    primary_doc = filing["primary_doc"]
    date = filing["date"]

    # Pick the actual main document, not just the primary_doc one segment
    doc = _pick_main_document(cik, acc, primary_doc, delay=delay)

    base_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc}/{doc}"

    safe_name = company.replace(" ", "_").replace("/", "_")
    out_file = out_dir / f"{safe_name}_10K_{date}.htm"

    if out_file.exists():
        print(f"  [skip] {out_file.name} already exists")
        return True

    try:
        r = requests.get(base_url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        out_file.write_bytes(r.content)
        size_kb = len(r.content) / 1024
        print(f"  [ok]   {out_file.name} ({size_kb:.0f} KB)")
        return True
    except Exception as e:
        print(f"  [fail] {company} {date}: {e}")
        return False


def _company_name_for_cik(cik: str) -> str:
    """Look up the registrant name for a CIK from EDGAR submissions. '' on failure."""
    cik_padded = cik.zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        return r.json().get("name", "")
    except Exception as e:
        print(f"  [warn] Could not resolve name for CIK {cik}: {e}")
        return ""


def main():
    parser = argparse.ArgumentParser(
        prog="ais_download_sec_10k_ops",
        description=(
            "AIStudio — SEC 10-K Corpus Downloader (OPS)  |  Version 1.2.1\n"
            "\n"
            "Downloads 10-K annual filings from major financial services firms\n"
            "via SEC EDGAR. Files are saved to data/corpora/sec_10k/uploads/ by default.\n"
            "Ingest into AIStudio with ais_ingest_sec_10k.\n"
            "\n"
            "TERMS OF USE: Data is retrieved from SEC EDGAR (sec.gov/edgar).\n"
            "Use is subject to SEC EDGAR fair access policy. Do not reduce\n"
            "--delay below 0.1s or run repeatedly in the same session.\n"
            "All filings are public documents under SEC disclosure requirements.\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  ais_download_sec_10k_ops                                # 25 firms × 5 filings (default)\n"
            "  ais_download_sec_10k_ops --cik 0001374310               # single firm (CBOE re-download)\n"
            "  ais_download_sec_10k_ops --cik 0001374310 --name \"CBOE Global Markets\"\n"
            "\n"
            "after download: ais_ingest_sec_10k\n"
        ),
    )
    parser.add_argument(
        "--out",
        default="data/corpora/sec_10k/uploads",
        help="Output directory (default: data/corpora/sec_10k/uploads — sec_10k only). "
             "Relative paths resolve against the repo root (the wrapper cd's there).",
    )
    parser.add_argument(
        "--firms",
        type=int,
        default=30,
        help="Max firms to attempt from the firm list (default: 30, list currently has 25)",
    )
    parser.add_argument(
        "--max-results-per-firm",
        "--years",
        dest="max_results_per_firm",
        type=int,
        default=5,
        help="Most recent filings per firm (default: 5). --years is a deprecated alias.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay between requests in seconds (min: 0.1, default: 0.5)",
    )
    parser.add_argument(
        "--cik",
        default=None,
        help="Download only this single CIK's filings (bypasses the FIRMS list). "
             "Pulls the N most-recent 10-Ks (N = --max-results-per-firm, default 5).",
    )
    parser.add_argument(
        "--name",
        default=None,
        help="Output filename label for --cik (e.g. \"CBOE Global Markets\"). "
             "If omitted, resolved from the FIRMS list, then EDGAR, then CIK_<cik>.",
    )
    args = parser.parse_args()

    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {out_dir}")

    if args.cik:
        cik = args.cik
        # name resolution: --name > FIRMS match (by padded CIK) > EDGAR submissions > CIK_<cik>
        if args.name:
            company = args.name
        else:
            match = next((nm for nm, c in FIRMS if c.zfill(10) == cik.zfill(10)), None)
            company = match or _company_name_for_cik(cik) or f"CIK_{cik}"
        firms_to_process = [(company, cik)]
        print(
            f"Single-CIK mode: {company} (CIK: {cik}) × "
            f"{args.max_results_per_firm} most-recent 10-Ks\n"
        )
    else:
        firms_to_process = list(FIRMS[: args.firms])
        actual_firms = min(args.firms, len(FIRMS))
        print(
            f"Targeting {actual_firms} firms × {args.max_results_per_firm} filings = "
            f"up to {actual_firms * args.max_results_per_firm} documents\n"
        )

    total_ok = 0
    total_fail = 0

    for company, cik in firms_to_process:
        print(f"\n{company} (CIK: {cik})")
        filings = get_filings(cik, max_results=args.max_results_per_firm, delay=args.delay)

        if not filings:
            print("  [warn] No 10-K filings found")
            total_fail += 1
            continue

        for filing in filings:
            ok = download_filing(filing, company, out_dir, delay=args.delay)
            if ok:
                total_ok += 1
            else:
                total_fail += 1
            time.sleep(args.delay)

    print(f"\n{'=' * 50}")
    print(f"Downloaded: {total_ok} filings")
    print(f"Failed:     {total_fail}")
    print(f"Output:     {out_dir}")
    print("\nTo ingest these files into AIStudio, run:")
    print("  ais_ingest_sec_10k")


if __name__ == "__main__":
    main()
