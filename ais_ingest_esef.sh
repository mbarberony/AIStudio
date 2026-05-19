#!/usr/bin/env zsh
# ais_ingest_esef.sh — Ingest an ESEF iXBRL corpus into AIStudio
# Version: 1.0.1
# Changelog:
#   1.0.1 — STD CLI Output §6 compliance: move terminal/sleep notices into
#           --- Important section before --- Ingesting. Remove blank line
#           before --- Ingesting (section label IS the visual break per §6).
#   1.0.0 — Initial version.

# ── Source guard ─────────────────────────────────────────────────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

VERSION="1.0.1"
SCRIPT_NAME="ais_ingest_esef"
REPO="${0:A:h}"
HELP_FILE="$REPO/ais_command_help.txt"

# ── Help ──────────────────────────────────────────────────────────────────────
_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$" | grep -v "^## "
    else
        echo "$SCRIPT_NAME v$VERSION — Ingest ESEF iXBRL corpus into AIStudio"
        echo ""
        echo "Usage: $SCRIPT_NAME [--corpus <name>] [--force] [--verbose] [--help] [--version]"
        echo ""
        echo "Options:"
        echo "  --corpus <name>   Corpus name (default: esef_banks)"
        echo "  --force           Re-ingest even if corpus already indexed in Qdrant"
        echo "  --verbose         Print full JSON result payload after summary"
        echo "  --help            Show this help and exit"
        echo "  --version         Print version and exit"
        echo ""
        echo "· Prerequisites : ais_start · ais_download_esef · corpus metadata file"
        echo "· To benchmark  : ais_bench --corpus <name>"
    fi
}

if [[ "$1" == "--help" ]]; then _show_help; exit 0; fi
if [[ "$1" == "--version" ]]; then echo "$SCRIPT_NAME v$VERSION"; exit 0; fi

# ── Argument parsing ──────────────────────────────────────────────────────────
CORPUS="esef_banks"
FORCE=0
VERBOSE=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --corpus)
            CORPUS="$2"
            shift 2
            ;;
        --force)
            FORCE=1
            shift
            ;;
        --verbose)
            VERBOSE=1
            shift
            ;;
        *)
            echo "❌ Unknown flag: $1"
            echo "· Run: $SCRIPT_NAME --help"
            exit 1
            ;;
    esac
done

# ── Derived paths ─────────────────────────────────────────────────────────────
API="http://localhost:8000"
QDRANT="http://localhost:6333"
CORPUS_DIR="$REPO/data/corpora/$CORPUS"
UPLOADS="$CORPUS_DIR/uploads"
METADATA_FILE="$CORPUS_DIR/${CORPUS}_corpus_metadata.yaml"

printf "\033[1m[ais_ingest_esef v$VERSION — Ingest ESEF corpus: $CORPUS]\033[0m\n"

# ── Preflight ─────────────────────────────────────────────────────────────────
echo "--- Preflight"

# 1. Corpus metadata file must exist — gate
if [[ ! -f "$METADATA_FILE" ]]; then
    echo "❌ Corpus metadata not found: data/corpora/$CORPUS/${CORPUS}_corpus_metadata.yaml"
    echo "· Create it via one of:"
    echo "  · AIStudio UI → Settings → New Corpus → fill description + search guidance"
    echo "  · REST: POST http://localhost:8000/corpus/create"
    echo "    Body: {\"name\": \"$CORPUS\", \"short_description\": \"...\", \"search_guidance\": \"...\"}"
    echo "  · Ask Claude to generate the metadata file for your corpus"
    exit 1
fi
echo "✅ Corpus metadata found: ${CORPUS}_corpus_metadata.yaml"

# 2. Uploads directory must exist and contain .xhtml files
if [[ ! -d "$UPLOADS" ]]; then
    echo "❌ Uploads directory not found: data/corpora/$CORPUS/uploads/"
    echo "· Run: ais_download_esef  (or create uploads/ and add .xhtml files manually)"
    exit 1
fi

FILE_COUNT=$(find "$UPLOADS" -maxdepth 1 -name "*.xhtml" | wc -l | tr -d ' ')
if [[ "$FILE_COUNT" -eq 0 ]]; then
    echo "❌ No .xhtml files found in data/corpora/$CORPUS/uploads/"
    echo "· Run: ais_download_esef"
    exit 1
fi

# Compute total size (macOS stat)
TOTAL_BYTES=0
while IFS= read -r f; do
    sz=$(stat -f%z "$f" 2>/dev/null || echo 0)
    TOTAL_BYTES=$(( TOTAL_BYTES + sz ))
done < <(find "$UPLOADS" -maxdepth 1 -name "*.xhtml")
TOTAL_MB=$(echo "scale=1; $TOTAL_BYTES / 1048576" | bc)
echo "✅ $FILE_COUNT filings ready · ${TOTAL_MB} MB"

# 3. Backend health check
if ! curl -sf "$API/health" > /dev/null 2>&1; then
    echo "❌ Backend not reachable at $API"
    echo "· Run: ais_start"
    exit 1
fi
echo "✅ Backend healthy."

# 4. Qdrant collection check — warn if already indexed, require --force
COLLECTION="aistudio_${CORPUS}"
QDRANT_RESPONSE=$(curl -sf "$QDRANT/collections/$COLLECTION" 2>/dev/null)
EXISTING_CHUNKS=""
if [[ -n "$QDRANT_RESPONSE" ]]; then
    EXISTING_CHUNKS=$(echo "$QDRANT_RESPONSE" | python3 -c \
        "import sys,json; d=json.load(sys.stdin); print(d.get('result',{}).get('points_count','?'))" \
        2>/dev/null)
fi

if [[ -n "$EXISTING_CHUNKS" && "$EXISTING_CHUNKS" != "?" && "$EXISTING_CHUNKS" -gt 0 ]]; then
    if [[ "$FORCE" -eq 0 ]]; then
        echo "⚠ Corpus '$CORPUS' already indexed in Qdrant: ${EXISTING_CHUNKS} chunks."
        echo "· Re-ingesting will wipe and rebuild the collection (~${TOTAL_MB} MB · ~20 min)."
        echo "· To proceed: $SCRIPT_NAME --corpus $CORPUS --force"
        exit 1
    else
        echo "⚠ --force: wiping existing collection ($EXISTING_CHUNKS chunks) and re-ingesting."
    fi
else
    echo "✅ No existing Qdrant collection — clean ingest."
fi

# ── Setup ─────────────────────────────────────────────────────────────────────
echo "--- Setup"
echo "· Corpus      : $CORPUS"
echo "· Files       : $FILE_COUNT filings · ${TOTAL_MB} MB"
echo "· Format      : ESEF iXBRL (.xhtml) — IFRS inline XBRL"
echo "· Normalizer  : ESEF Document-Head Extraction (pipeline.py) — entity + FY year prefix per chunk"
echo "· Chunk size  : 1,200 chars · Overlap: 200 chars"
echo "· Embed model : nomic-embed-text"
echo "· Source      : $UPLOADS"

# ── Important notice ─────────────────────────────────────────────────────────
echo "--- Important"
echo "· This terminal can be minimized but not closed."
echo "· Sleep prevention: caffeinate -i is active for the duration."
# ── Hardware-aware time estimate ──────────────────────────────────────────────
# ~130s/file on M4 Pro 128GB (observed 2026-05-18: 716s / 9 files)
# ~320s/file estimated on M4 Air 16GB (proportional from sec_10k ratio)
ESTIMATE_PRO=$(( FILE_COUNT * 130 / 60 ))
ESTIMATE_AIR=$(( FILE_COUNT * 320 / 60 ))
echo "--- Ingesting"
echo "▶ Ingesting $FILE_COUNT filings — ~${ESTIMATE_PRO} min on M4 Pro · ~${ESTIMATE_AIR} min on M4 Air."

# ── Ingest ────────────────────────────────────────────────────────────────────
cd "$REPO"
source .venv/bin/activate

INGEST_ARGS=(
    --corpus "$CORPUS"
    --root "$UPLOADS"
)
[[ "$FORCE" -eq 1 ]] && INGEST_ARGS+=(--force)
[[ "$VERBOSE" -eq 1 ]] && INGEST_ARGS+=(--verbose)

caffeinate -i env AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
    python3 -m local_llm_bot.app.ingest "${INGEST_ARGS[@]}"

INGEST_EXIT=$?

# ── Post-ingest summary ───────────────────────────────────────────────────────
echo "--- Next steps"
if [[ "$INGEST_EXIT" -eq 0 ]]; then
    echo "✅ Corpus '$CORPUS' ready."
    echo "· Select '$CORPUS' in the AIStudio corpus dropdown to query."
    echo "· To benchmark : ais_bench --corpus $CORPUS"
    echo "· To re-ingest : $SCRIPT_NAME --corpus $CORPUS --force"
else
    echo "❌ Ingest exited with error code $INGEST_EXIT."
    echo "· Check output above for details."
    echo "· To retry    : $SCRIPT_NAME --corpus $CORPUS --force"
fi

exit $INGEST_EXIT
