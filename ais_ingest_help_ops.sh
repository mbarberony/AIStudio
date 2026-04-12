#!/usr/bin/env zsh
# ais_ingest_help_ops — Regenerate help corpus PDFs and re-ingest (Operator only)
# Version: 1.0.0
# Runs ais_update_help_ops first, then re-ingests into Qdrant if backend is running.
# If backend is not running, PDFs are updated and ingest will run at next ais_start.

VERSION="1.0.0"
REPO="$(cd "$(dirname "$0")" && pwd)"
API="http://localhost:8000"

if [[ "$1" == "--version" ]]; then echo "ais_ingest_help_ops v$VERSION"; exit 0; fi
if [[ "$1" == "--help" ]]; then
    echo "ais_ingest_help_ops v$VERSION"
    echo ""
    echo "Usage: ais_ingest_help_ops"
    echo ""
    echo "What it does:"
    echo "  1. Regenerates all help corpus PDFs (ais_update_help_ops)"
    echo "  2. If backend is running: deletes and re-ingests help corpus immediately"
    echo "  3. If backend is not running: PDFs are ready; ingest runs at next ais_start"
    exit 0
fi

echo "+============================================================+"
echo "|        AIStudio Help Corpus Full Update v$VERSION           |"
echo "+============================================================+"
echo ""

# Step 1 — regenerate PDFs
echo "── Step 1: Regenerating PDFs ──────────────────────────────"
"$REPO/ais_update_help_ops.sh"
echo ""

# Step 2 — ingest if backend is running
echo "── Step 2: Re-ingesting ───────────────────────────────────"
if curl -sf "$API/health" > /dev/null 2>&1; then
    echo "  Backend running — ingesting now..."

    # Delete existing help corpus
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$API/corpus/help?confirm=yes")
    if [[ "$HTTP_STATUS" == "200" || "$HTTP_STATUS" == "204" ]]; then
        echo "  ✓ Help corpus deleted"
    elif [[ "$HTTP_STATUS" == "404" ]]; then
        echo "  (Help corpus did not exist — continuing)"
    else
        echo "  ⚠  Delete returned status $HTTP_STATUS — continuing"
    fi

    # Create fresh corpus
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$API/corpus/create" \
        -H "Content-Type: application/json" \
        -d '{"name": "help"}')
    if [[ "$HTTP_STATUS" == "200" || "$HTTP_STATUS" == "201" ]]; then
        echo "  ✓ Help corpus created"
    else
        echo "  ❌ Could not create help corpus (status $HTTP_STATUS)"
        exit 1
    fi

    # Run ingest
    cd "$REPO"
    source .venv/bin/activate
    AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
        python3 -m local_llm_bot.app.ingest \
        --corpus help \
        --root data/corpora/help/uploads

    echo ""
    echo "✅ Help corpus updated and re-ingested."
else
    echo "  Backend not running — PDFs are ready."
    echo "  Ingest will run automatically at next ais_start."
    echo ""
    echo "✅ Help corpus PDFs updated. Run ais_start to complete ingest."
fi
