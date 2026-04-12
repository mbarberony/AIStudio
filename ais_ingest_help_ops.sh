#!/usr/bin/env zsh
# ais_ingest_help_ops.sh — Update and re-ingest the AIStudio help corpus (Operator only)
# Version: 1.2.0
# Changelog: 1.2.0 — removed delete/create cycle; corpus is preserved across re-ingest
#            1.1.0 — staging fix (superseded)
#            1.0.0 — initial version
#
# Runs ais_update_help_ops (PDF generation) then re-ingests into Qdrant via --force.
# The corpus directory and uploads/ are never deleted — PDFs are written directly then ingested.
# If backend is not running, PDFs are generated and ingest will happen automatically at ais_start.

VERSION="1.2.0"
REPO="$(cd "$(dirname "$0")" && pwd)"
API="http://localhost:8000"
HELP_UPLOADS="$REPO/data/corpora/help/uploads"

if [[ "$1" == "--version" ]]; then echo "ais_ingest_help_ops v$VERSION"; exit 0; fi
if [[ "$1" == "--help" ]]; then
    echo "ais_ingest_help_ops v$VERSION"
    echo ""
    echo "Usage: ais_ingest_help_ops"
    echo ""
    echo "What it does:"
    echo "  1. Regenerates all help corpus PDFs into data/corpora/help/uploads/"
    echo "  2. Ensures help corpus exists (creates if missing)"
    echo "  3. If backend is running: re-ingests PDFs into Qdrant immediately (--force)"
    echo "  4. If backend is not running: PDFs are ready; ingest runs at next ais_start"
    exit 0
fi

echo "+============================================================+"
echo "|      AIStudio Help Corpus Update + Ingest v$VERSION        |"
echo "+============================================================+"
echo ""

# Step 1 — Regenerate PDFs directly into uploads/
echo "── Step 1: Regenerating help corpus PDFs ────────────────────"
"$REPO/ais_update_help_ops.sh"
echo ""

# Count PDFs now in uploads/
PDF_COUNT=$(find "$HELP_UPLOADS" -name "*.pdf" 2>/dev/null | wc -l | tr -d ' ')
if [[ "$PDF_COUNT" -eq 0 ]]; then
    echo "❌ No PDFs found in $HELP_UPLOADS — PDF generation failed."
    echo "   Check ais_update_help_ops output above."
    exit 1
fi
echo "  ✓ $PDF_COUNT PDFs ready in uploads/"

# Step 2 — Ensure corpus exists (create only if missing)
echo ""
echo "── Step 2: Ensuring corpus exists ───────────────────────────"
if ! curl -sf "$API/health" > /dev/null 2>&1; then
    echo "  ⚠  Backend not running — PDFs are ready."
    echo "  ℹ  Help corpus will be ingested automatically at next ais_start."
    exit 0
fi

CORPUS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$API/corpus/help/info")
if [[ "$CORPUS_STATUS" == "404" ]]; then
    echo "  ▶ Help corpus not found — creating..."
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$API/corpus/create" \
        -H "Content-Type: application/json" \
        -d '{"name": "help"}')
    if [[ "$HTTP_STATUS" == "200" || "$HTTP_STATUS" == "201" ]]; then
        echo "  ✓ Help corpus created"
    else
        echo "  ❌ Could not create help corpus (status $HTTP_STATUS)"
        exit 1
    fi
else
    echo "  ✓ Help corpus exists"
fi

# Step 3 — Ingest with --force (re-embeds all PDFs, wipes stale Qdrant entries)
echo ""
echo "── Step 3: Ingesting into Qdrant ────────────────────────────"
echo "  ▶ Ingesting $PDF_COUNT PDFs..."
cd "$REPO"
source .venv/bin/activate
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
    python3 -m local_llm_bot.app.ingest \
    --corpus help \
    --root data/corpora/help/uploads \
    --force

echo ""
echo "✅ Help corpus updated and re-ingested."
