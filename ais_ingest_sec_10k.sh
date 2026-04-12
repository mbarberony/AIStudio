#!/usr/bin/env zsh
# ais_ingest_sec_10k — Ingest the SEC 10-K corpus into AIStudio
# Version: 1.0.0
# Ingests all .htm files from ~/Downloads/sec_10k_corpus/ into the sec_10k corpus.
# Requires: AIStudio backend running (ais_start) and files downloaded (ais_download_sec_10k)

VERSION="1.0.0"
REPO="$(cd "$(dirname "$0")" && pwd)"
API="http://localhost:8000"
SEC_DIR="$HOME/Downloads/sec_10k_corpus"

if [[ "$1" == "--version" ]]; then echo "ais_ingest_sec_10k v$VERSION"; exit 0; fi
if [[ "$1" == "--help" ]]; then
    echo "ais_ingest_sec_10k v$VERSION"
    echo ""
    echo "Usage: ais_ingest_sec_10k [--dir PATH]"
    echo ""
    echo "Ingests SEC 10-K filings into AIStudio as the 'sec_10k' corpus."
    echo ""
    echo "Requirements:"
    echo "  1. AIStudio must be running: ais_start"
    echo "  2. Filings must be downloaded: ais_download_sec_10k"
    echo ""
    echo "Default source: ~/Downloads/sec_10k_corpus/"
    echo "Override:       ais_ingest_sec_10k --dir /path/to/filings"
    echo ""
    echo "⏱  Expected time: ~30 minutes on M4 MacBook Pro"
    echo "   143 filings · 25 firms · ~106,000 chunks"
    exit 0
fi

# Parse optional --dir flag
while [[ $# -gt 0 ]]; do
    case "$1" in
        --dir) SEC_DIR="$2"; shift 2 ;;
        *) shift ;;
    esac
done

echo "+============================================================+"
echo "|        AIStudio SEC 10-K Corpus Ingest v$VERSION            |"
echo "+============================================================+"
echo ""
echo "  Source : $SEC_DIR"
echo "  Corpus : sec_10k"
echo ""
echo "  ⏱  This will take ~30 minutes on a fast machine."
echo "  Leave this terminal open until complete."
echo ""

# Check files exist
if [[ ! -d "$SEC_DIR" ]]; then
    echo "❌ Source directory not found: $SEC_DIR"
    echo "   Run: ais_download_sec_10k"
    exit 1
fi

FILE_COUNT=$(ls "$SEC_DIR"/*.htm 2>/dev/null | wc -l | tr -d ' ')
if [[ "$FILE_COUNT" -eq 0 ]]; then
    echo "❌ No .htm files found in $SEC_DIR"
    echo "   Run: ais_download_sec_10k"
    exit 1
fi
echo "  Found $FILE_COUNT .htm files"
echo ""

# Check backend
if ! curl -sf "$API/health" > /dev/null 2>&1; then
    echo "❌ Backend not reachable at $API"
    echo "   Run: ais_start"
    exit 1
fi
echo "✓ Backend healthy"
echo ""

# Copy files to corpus uploads
UPLOADS="$REPO/data/corpora/sec_10k/uploads"
mkdir -p "$UPLOADS"
echo "▶ Copying files to $UPLOADS..."
cp "$SEC_DIR"/*.htm "$UPLOADS/"
echo "✓ $FILE_COUNT files copied"
echo ""

# Ingest
echo "▶ Ingesting (this will take a while)..."
cd "$REPO"
source .venv/bin/activate
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
    python3 -m local_llm_bot.app.ingest \
    --corpus sec_10k \
    --root "$UPLOADS"

echo ""
echo "✅ SEC 10-K corpus ingested. Select 'sec_10k' in the AIStudio corpus dropdown."
