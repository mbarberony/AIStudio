#!/usr/bin/env python3
"""
AIStudio — SEC 10-K Corpus Downloader
Version 1.0.0

Downloads 10-K annual filings from major financial services firms via SEC EDGAR.
Files are saved to ~/Downloads/sec_10k/ by default and can then be ingested
into AIStudio using the Upload button in the AIStudio UI

TERMS OF USE — SEC EDGAR
Data is retrieved from the U.S. Securities and Exchange Commission's EDGAR system
(https://www.sec.gov/edgar). Use is subject to SEC EDGAR's terms and conditions.
This tool identifies itself to the SEC servers as required by their fair access policy.
Do not run this tool more than once per session or modify the request delay below 0.1s.
All filings retrieved are public documents under SEC disclosure requirements.

Usage:
    ais_sec_download                          # default: 30 firms, 2 filings each
    ais_sec_download --firms 5 --years 1      # quick test: 5 firms, 1 filing each
    ais_sec_download --out ~/Downloads/mydir  # custom output folder
    ais_sec_download --help                   # show all options
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
FIRMS = [
    # Bulge bracket banks
    ("Goldman Sachs", "0000886982"),
    ("Morgan Stanley", "0000895421"),
    ("JPMorgan Chase", "0000019617"),
    ("Citigroup", "0000831001"),
    ("Bank of America", "0000070858"),
    ("Wells Fargo", "0000072971"),
    ("Barclays", "0000312070"),
    ("Deutsche Bank", "0001159508"),
    # Asset managers
    ("BlackRock", "0001364742"),
    ("Vanguard Group", "0000102909"),
    ("Fidelity", "0000315066"),
    ("T Rowe Price", "0001113169"),
    ("Franklin Templeton", "0000038777"),
    ("Invesco", "0000914208"),
    ("AllianceBernstein", "0000825313"),
    ("Nuveen", "0000073124"),
    # Exchanges & infrastructure
    ("CME Group", "0001156375"),
    ("Intercontinental Exchange", "0001571949"),
    ("Nasdaq", "0001120193"),
    ("CBOE Global Markets", "0001374690"),
    # Insurance / diversified
    ("AIG", "0000005272"),
    ("MetLife", "0001099219"),
    ("Prudential Financial", "0001137774"),
    ("Travelers", "0000086312"),
    # Custody / services
    ("BNY Mellon", "0000009626"),
    ("State Street", "0000093751"),
    ("Northern Trust", "0000073124"),
    # Boutiques / specialty
    ("Jefferies", "0000019617"),
    ("Raymond James", "0000720005"),
    ("Stifel Financial", "0000895655"),
]

YEARS = ["2023", "2022", "2021"]  # Pull last 3 years per firm


def get_filings(cik: str, form_type: str = "10-K", max_results: int = 3) -> list:
    """Fetch filing metadata from EDGAR for a given CIK."""
    cik_padded = cik.zfill(10)
    url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"  [warn] Could not fetch submissions for CIK {cik}: {e}")
        return []

    filings = data.get("filings", {}).get("recent", {})
    forms = filings.get("form", [])
    accessions = filings.get("accessionNumber", [])
    dates = filings.get("filingDate", [])
    primary_docs = filings.get("primaryDocument", [])

    results = []
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
    return results


def download_filing(filing: dict, company: str, out_dir: Path) -> bool:
    """Download the primary document of a filing as a text file."""
    acc = filing["accession"]
    cik = filing["cik"]
    doc = filing["primary_doc"]
    date = filing["date"]

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


def main():
    parser = argparse.ArgumentParser(
        prog="ais_sec_download",
        description=(
            "AIStudio — SEC 10-K Corpus Downloader  |  Version 1.0.0\n"
            "\n"
            "Downloads 10-K annual filings from major financial services firms\n"
            "via SEC EDGAR. Files are saved to ~/Downloads/sec_10k/ by default.\n"
            "\n"
            "TERMS OF USE: Data is retrieved from SEC EDGAR (sec.gov/edgar).\n"
            "Use is subject to SEC EDGAR fair access policy. Do not reduce\n"
            "--delay below 0.1s or run repeatedly in the same session.\n"
            "All filings are public documents under SEC disclosure requirements.\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  ais_sec_download                          # 30 firms × 2 filings (default)\n"
            "  ais_sec_download --firms 5 --years 1      # quick test\n"
            "  ais_sec_download --out ~/Downloads/mydir  # custom output folder\n"
            "\n"
            "after download, open AIStudio and upload the files\n"
            "using the Upload button in the corpus manager\n"
        ),
    )
    parser.add_argument(
        "--out",
        default="~/Downloads/sec_10k",
        help="Output directory (default: ~/Downloads/sec_10k)",
    )
    parser.add_argument(
        "--firms", type=int, default=30, help="Number of firms to download (1-30, default: 30)"
    )
    parser.add_argument(
        "--years", type=int, default=2, help="Most recent filings per firm (1-3, default: 2)"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay between requests in seconds (min: 0.1, default: 0.5)",
    )
    args = parser.parse_args()

    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {out_dir}")
    print(
        f"Targeting {args.firms} firms × {args.years} filings = up to {args.firms * args.years} documents\n"
    )

    total_ok = 0
    total_fail = 0

    for company, cik in FIRMS[: args.firms]:
        print(f"\n{company} (CIK: {cik})")
        filings = get_filings(cik, max_results=args.years)

        if not filings:
            print("  [warn] No 10-K filings found")
            total_fail += 1
            continue

        for filing in filings:
            ok = download_filing(filing, company, out_dir)
            if ok:
                total_ok += 1
            else:
                total_fail += 1
            time.sleep(args.delay)

    print(f"\n{'=' * 50}")
    print(f"Downloaded: {total_ok} filings")
    print(f"Failed:     {total_fail}")
    print(f"Output:     {out_dir}")
    print("\nTo ingest these files into AIStudio:")
    print("  1. Open AIStudio in your browser")
    print("  2. Create a new corpus named 'sec_10k'")
    print(f"  3. Upload the files from {out_dir}")
    print("     or use the Upload button to add them one by one")


if __name__ == "__main__":
    main()
