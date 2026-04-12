#!/usr/bin/env zsh
# ais_download_sec_10k — Download SEC 10-K corpus from EDGAR
# Version: 1.0.0
# Downloads ~143 filings from 25 financial services firms (~500MB)
# Output goes to ~/Downloads/sec_10k_corpus/ by default
#
# Usage: ais_download_sec_10k [--out DIR] [--firms N] [--years N]
# After download, ingest with: ais_ingest_sec_10k

VERSION="1.0.0"
REPO="$(cd "$(dirname "$0")" && pwd)"

if [[ "$1" == "--version" ]]; then echo "ais_download_sec_10k v$VERSION"; exit 0; fi
if [[ "$1" == "--help" ]]; then
    echo "ais_download_sec_10k v$VERSION"
    echo ""
    echo "Usage: ais_download_sec_10k [--out DIR] [--firms N] [--years N]"
    echo ""
    echo "Downloads ~143 SEC 10-K filings from 25 financial services firms (~500MB)"
    echo "Output: ~/Downloads/sec_10k_corpus/ (default)"
    echo ""
    echo "After download, ingest with: ais_ingest_sec_10k"
    echo "  (requires AIStudio backend running — ~30 min on M4 MacBook Pro)"
    exit 0
fi

cd "$REPO"
source .venv/bin/activate
python3 scripts/download_sec_corpus.py --out ~/Downloads/sec_10k_corpus "$@"
