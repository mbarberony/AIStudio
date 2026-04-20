#!/bin/bash

# AIStudio Auto-Launch Script v1.6.3
# Mac/Apple Silicon only (Release 1.x)
# v1.1.0: poll /health before opening browser — fixes race condition (AIStudio_066)
# v1.2.0: kill stale process on port 8000 before launch — fixes port conflict (AIStudio_103)
# v1.2.1: fix set -e interaction with lsof — lsof returns exit 1 when port is free
# v1.3.0: venv activated internally; Ollama install check; idempotent start (AIStudio_173/174)
# v1.4.0: call stop.sh first — guarantees clean state, no manual ais_stop needed
# v1.5.0: silent help corpus auto-ingest on start
# v1.6.0: --verbose flag; suppress Qdrant/backend noise by default; file counts
# v1.6.1: use --force ingest for help corpus — preserves uploads/ on disk
# v1.6.2: CLI output standard; --help/--version; always print version; fix chunk/PDF count
# v1.6.3: call stop.sh --silent; --- section separators; --no-separator flag
# v1.6.4: self-healing help corpus — regenerate PDFs if uploads/ empty before ingest
# v1.6.5: --show-log flag opens iTerm2 tab with live backend log; uvicorn logs to file
# v1.6.6: fix set -e exit on PDF generation failure; warn on missing help_search_guidance
# v1.6.7: skip help re-ingest if collection healthy — prevents WAL corruption on restart (AIStudio_066)
# v1.6.8: llama3.1:8b availability check (AIStudio_102); port 8000 conflict handling (AIStudio_103)

set -e

VERSION="1.6.8"
ITALIC=$'\e[3m'
RESET=$'\e[0m'
DIM=$'\e[2m'

# ── Parse flags ───────────────────────────────────────────────────
VERBOSE=0
SEPARATOR=1
SHOW_LOG=0
LOG_FILE="$HOME/Library/Logs/AIStudio/backend.log"

for arg in "$@"; do
    [[ "$arg" == "--verbose" ]] && VERBOSE=1
    [[ "$arg" == "--no-separator" ]] && SEPARATOR=0
    [[ "$arg" == "--show-log" ]] && SHOW_LOG=1
    [[ "$arg" == "--version" ]] && { echo "ais_start v$VERSION — Start AIStudio services"; exit 0; }
    if [[ "$arg" == "--help" ]]; then
        echo "ais_start v$VERSION — Start AIStudio services"
        echo ""
        echo "Start all AIStudio services: Qdrant, Ollama, FastAPI backend, and frontend."
        echo "Stops any running services first — safe to run even if already running."
        echo ""
        echo "Usage: ais_start [options]"
        echo ""
        echo "Options:"
        echo "  --verbose        Show full service output (Qdrant, uvicorn, backend logs)"
        echo "  --show-log       Open new iTerm2 tab with live backend log after start"
        echo "  --no-separator   Use blank lines between sections instead of --- labels"
        echo "  --version        Show version and exit"
        echo "  --help           Show this help and exit"
        echo ""
        echo "· To stop: ais_stop"
        echo "· Logs:    ais_log"
        exit 0
    fi
done

sep() {
    if [[ "$SEPARATOR" -eq 1 ]]; then
        echo "${DIM}--- ${ITALIC}$1${RESET}"
    else
        echo ""
    fi
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
FRONTEND="$REPO_ROOT/front_end/rag_studio.html"
QDRANT_STORAGE="$HOME/qdrant_storage"
VENV="$REPO_ROOT/.venv"

echo "ais_start v$VERSION — Start AIStudio services"

if [ -f "$VENV/bin/activate" ]; then
    source "$VENV/bin/activate"
else
    echo "❌ Virtual environment not found at $VENV."
    echo "· Run: ./ais_install"
    exit 1
fi

# ── Cleanup ───────────────────────────────────────────────────────
sep "Cleanup"
echo "🛑 Stopping any running services..."
"$SCRIPT_DIR/stop.sh" --silent 2>/dev/null || true

# ── Ecosystem ─────────────────────────────────────────────────────
sep "Ecosystem"
echo "▶ Starting AIStudio..."

if curl -s http://localhost:6333/healthz > /dev/null 2>&1; then
    echo "✅ Qdrant already running."
else
    echo "▶ Starting Qdrant..."
    mkdir -p "$QDRANT_STORAGE"
    cd "$QDRANT_STORAGE"
    if [[ "$VERBOSE" -eq 1 ]]; then
        QDRANT__STORAGE__STORAGE_PATH="$QDRANT_STORAGE" qdrant &
    else
        QDRANT__STORAGE__STORAGE_PATH="$QDRANT_STORAGE" qdrant > /dev/null 2>&1 &
    fi
    sleep 2
    echo "✅ Qdrant started."
fi

if ! command -v ollama > /dev/null 2>&1; then
    echo "❌ Ollama not found."
    echo "· Install from: https://ollama.com"
    exit 1
fi
if curl -s http://localhost:11434 > /dev/null 2>&1; then
    echo "✅ Ollama already running."
else
    echo "▶ Starting Ollama..."
    if [[ "$VERBOSE" -eq 1 ]]; then
        ollama serve &
    else
        ollama serve > /dev/null 2>&1 &
    fi
    sleep 3
    echo "✅ Ollama started."
fi

# AIStudio_102: verify required model is available
if ! ollama list 2>/dev/null | grep -q "llama3.1:8b"; then
    echo "❌ Required model not found: llama3.1:8b"
    echo "· Run: ollama pull llama3.1:8b"
    echo "· This takes ~5 minutes on first run (~4.7 GB download)."
    exit 1
fi

echo "▶ Starting AIStudio backend..."
cd "$REPO_ROOT"
mkdir -p "$HOME/Library/Logs/AIStudio"

# AIStudio_103: kill any stale process on port 8000 before starting
STALE_PIDS=$(lsof -ti:8000 2>/dev/null || true)
if [[ -n "$STALE_PIDS" ]]; then
    echo "$STALE_PIDS" | xargs kill 2>/dev/null || true
    sleep 1
fi
if [[ "$VERBOSE" -eq 1 ]]; then
    OLLAMA_KEEP_ALIVE=30m AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
        uvicorn local_llm_bot.app.api:app --port 8000 2>&1 | tee "$LOG_FILE" &
else
    OLLAMA_KEEP_ALIVE=30m AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
        uvicorn local_llm_bot.app.api:app --port 8000 > "$LOG_FILE" 2>&1 &
fi

BACKEND_READY=0
for i in $(seq 1 15); do
    sleep 1
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        BACKEND_READY=1
        break
    fi
done
if [ "$BACKEND_READY" -eq 1 ]; then
    echo "✅ Backend started."
else
    echo "⚠ Backend slow to start — opening UI anyway."
fi

# ── Processing ────────────────────────────────────────────────────
sep "Processing"
DEMO_COLLECTION="aistudio_demo"
DEMO_CHECK=$(curl -s "http://localhost:6333/collections/$DEMO_COLLECTION" 2>/dev/null)

if echo "$DEMO_CHECK" | grep -q '"status":"ok"'; then
    DEMO_COUNT=$(echo "$DEMO_CHECK" | python3 -c "
import sys, json
d = json.load(sys.stdin)
r = d.get('result', {})
print(r.get('points_count') or r.get('vectors_count') or '?')
" 2>/dev/null || echo "?")
    echo "✅ Demo corpus indexed: $DEMO_COUNT chunks."
else
    echo "▶ Demo corpus not found — ingesting for first time (~45 seconds)..."
    echo "· This happens once. Subsequent starts are instant."
    cd "$REPO_ROOT"
    AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
        python3 -m local_llm_bot.app.ingest \
        --corpus demo \
        --root data/corpora/demo/uploads
    echo "✅ Demo corpus indexed."
fi

if [ "$BACKEND_READY" -eq 1 ]; then
    HELP_UPLOADS="$REPO_ROOT/data/corpora/help/uploads"
    HELP_PDF_COUNT=$(find "$HELP_UPLOADS" -name "*.pdf" 2>/dev/null | wc -l | tr -d ' ')

    # Self-heal: if uploads/ is empty, regenerate PDFs from manifest sources
    if [ "$HELP_PDF_COUNT" -eq 0 ]; then
        # Check for help_search_guidance.yaml — warn if missing
        GUIDANCE_FILE="$REPO_ROOT/meta/corpora/help_search_guidance.yaml"
        if [ ! -f "$GUIDANCE_FILE" ]; then
            echo "⚠ Help search guidance not found: meta/corpora/help_search_guidance.yaml"
            echo "· Run: ais_deploy help_search_guidance.yaml"
        fi
        echo "▶ Preparing help corpus — generating PDFs from sources..."
        cd "$REPO_ROOT"
        if python3 scripts/update_help_corpus.py --repo-root "$REPO_ROOT" > /dev/null 2>&1; then
            HELP_PDF_COUNT=$(find "$HELP_UPLOADS" -name "*.pdf" 2>/dev/null | wc -l | tr -d ' ')
            echo "✅ Help corpus PDFs ready: $HELP_PDF_COUNT files."
        else
            echo "⚠ Help corpus PDF generation failed — run ais_ingest_help_ops to retry."
        fi
    fi

    HELP_COLLECTION="aistudio_help"
    HELP_CHECK=$(curl -s "http://localhost:6333/collections/$HELP_COLLECTION" 2>/dev/null)
    HELP_CHUNKS=$(echo "$HELP_CHECK" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    r = d.get('result', {})
    print(r.get('points_count') or r.get('vectors_count') or 0)
except:
    print(0)
" 2>/dev/null || echo "0")

    if [[ "$HELP_CHUNKS" -gt 0 ]]; then
        # Collection healthy — skip re-ingest to prevent WAL corruption (AIStudio_066)
        echo "✅ Help corpus indexed: $HELP_CHUNKS chunks."
    else
        # Collection missing or empty — ingest needed
        HELP_MSG="indexing"
        echo "$HELP_CHECK" | grep -q '"status":"ok"' && HELP_MSG="refreshing"
        (cd "$REPO_ROOT" && \
         AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
             python3 -m local_llm_bot.app.ingest \
             --corpus help \
             --root "$HELP_UPLOADS" \
             --force > /dev/null 2>&1) &
        echo "✅ Help corpus $HELP_MSG in background: $HELP_PDF_COUNT files."
    fi
fi

# ── Reporting ─────────────────────────────────────────────────────
sep "Reporting"
echo "▶ Opening frontend..."
open "$FRONTEND"
echo "✅ AIStudio is running."
echo "· Frontend : $FRONTEND"
echo "· Backend  : http://localhost:8000"
echo "· Qdrant   : http://localhost:6333"
echo "· Ollama   : http://localhost:11434"
echo "· Logs     : ais_log"
echo "· To stop  : ais_stop"
echo "· To restart: ais_start"
[[ "$VERBOSE" -eq 1 ]] && echo "· Verbose mode active — run ais_start for quiet output."

# --show-log: open new iTerm2 tab tailing the backend log
if [[ "$SHOW_LOG" -eq 1 ]]; then
    osascript 2>/dev/null << APPLESCRIPT
tell application "iTerm2"
    tell current window
        create tab with default profile
        tell current session
            write text "tail -f '$LOG_FILE'"
        end tell
    end tell
end tell
APPLESCRIPT
fi
