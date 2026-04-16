#!/usr/bin/env zsh
# ais_download_sec_10k.sh — Download SEC 10-K corpus from EDGAR
# Version: 1.1.0
# Downloads ~143 filings from 25 financial services firms (~500MB)
# Output goes to data/corpora/sec_10k/uploads/ by default

VERSION="1.1.0"
REPO="$(cd "$(dirname "$0")" && pwd)"

printf "\033[1m[ais_download_sec_10k v$VERSION — Download SEC 10-K filings from EDGAR]\033[0m\n"

if [[ "$1" == "--version" ]]; then
    exit 0
fi

if [[ "$1" == "--help" ]]; then
    echo ""
    echo "Usage: ais_download_sec_10k [--out DIR] [--firms N] [--years N]"
    echo ""
    echo "Downloads ~143 SEC 10-K filings from 25 financial services firms (~500MB)."
    echo ""
    echo "Defaults:"
    echo "  · Output: data/corpora/sec_10k/uploads/"
    echo "  · ~143 filings, 25 firms, most recent 3 years"
    echo ""
    echo "After download, ingest with: ais_ingest_sec_10k"
    echo "  · Requires AIStudio backend running — ~30 min on M4 MacBook Pro"
    exit 0
fi

# Create corpus upload directory if needed
UPLOADS="$REPO/data/corpora/sec_10k/uploads"
mkdir -p "$UPLOADS"

cd "$REPO"
source .venv/bin/activate

echo "--- Preflight"
echo "✅ Output directory ready: data/corpora/sec_10k/uploads/"

echo ""
echo "--- Downloading"
echo "▶ Fetching SEC 10-K filings from EDGAR..."
echo "· ~143 filings, ~500MB — allow 5–10 minutes"
echo ""

python3 scripts/download_sec_corpus.py --out "$UPLOADS" "$@"

echo ""
echo "--- Summary"
FILE_COUNT=$(ls "$UPLOADS"/*.htm 2>/dev/null | wc -l | tr -d ' ')
echo "✅ $FILE_COUNT filings downloaded to data/corpora/sec_10k/uploads/"
echo "· Next step: ais_ingest_sec_10k"
