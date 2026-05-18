#!/usr/bin/env bash
# ais_start.sh — Start all AIStudio services
# Version: 2.0.4
# Changelog: 2.0.4 — fix Ollama "already running" check: use /api/tags not bare port (AIStudio_541)
# Changelog: 2.0.3 — replace hardcoded llama3.1:8b check with /api/tags API check (AIStudio_532)
# Changelog: 2.0.1 — fix ZSH_EVAL_CONTEXT unbound variable under set -u in bash (use :- default)

set -euo pipefail

# ── Source guard ──────────────────────────────────────────────────────────────
[[ "${ZSH_EVAL_CONTEXT:-}" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

VERSION="2.0.4"
SCRIPT_NAME="ais_start"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$SCRIPT_DIR"
HELP_FILE="$REPO/ais_command_help.txt"

# ── Output helpers ────────────────────────────────────────────────────────────
ITALIC=$'\e[3m'
RESET=$'\e[0m'
DIM=$'\e[2m'

_sep() {
    if [[ "${SEPARATOR:-1}" -eq 1 ]]; then
        echo "${DIM}--- ${ITALIC}$1${RESET}"
    else
        echo ""
    fi
}

# ── Help ──────────────────────────────────────────────────────────────────────
_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$" | grep -v "^## "
    else
        echo "$SCRIPT_NAME v$VERSION — Start all AIStudio services"
        echo ""
        echo "Usage: $SCRIPT_NAME [options]"
        echo ""
        echo "Options:"
        echo "  --verbose        Show full service output"
        echo "  --show-log       Open new iTerm2 tab with live backend log"
        echo "  --show-splash    Show splash dialog on startup"
        echo "  --no-separator   Use blank lines between sections"
        echo "  --no-open        Suppress browser open (for desktop shortcut)"
        echo "  --version        Show version and exit"
        echo "  --help           Show this help and exit"
        echo ""
        echo "· To stop: ais_stop"
        echo "· Logs:    ais_log"
    fi
}

if [[ "${1:-}" == "--help" ]];    then _show_help; exit 0; fi
if [[ "${1:-}" == "--version" ]]; then echo "$SCRIPT_NAME v$VERSION"; exit 0; fi

printf '\033[1m[%s v%s — Start all AIStudio services]\033[0m\n' "$SCRIPT_NAME" "$VERSION"

# ── Parse flags ───────────────────────────────────────────────────────────────
VERBOSE=0
SEPARATOR=1
SHOW_LOG=0
SHOW_SPLASH=0
NO_OPEN=0
LOG_FILE="$HOME/Library/Logs/AIStudio/backend.log"

for arg in "$@"; do
    [[ "$arg" == "--verbose" ]]      && VERBOSE=1
    [[ "$arg" == "--no-separator" ]] && SEPARATOR=0
    [[ "$arg" == "--show-log" ]]     && SHOW_LOG=1
    [[ "$arg" == "--show-splash" ]]  && SHOW_SPLASH=1
    [[ "$arg" == "--no-open" ]]      && NO_OPEN=1
done

FRONTEND="$REPO/front_end/rag_studio.html"
QDRANT_STORAGE="$HOME/qdrant_storage"
VENV="$REPO/.venv"
API="http://localhost:8000"

# ── Venv ──────────────────────────────────────────────────────────────────────
if [[ -f "$VENV/bin/activate" ]]; then
    source "$VENV/bin/activate"
else
    echo "❌ Virtual environment not found at $VENV."
    echo "· Run: ./ais_install"
    exit 1
fi

# ── Cleanup ───────────────────────────────────────────────────────────────────
_sep "Cleanup"
echo "🛑 Stopping any running services..."
"$REPO/scripts/stop.sh" --silent 2>/dev/null || true

# ── Ecosystem ─────────────────────────────────────────────────────────────────
_sep "Ecosystem"
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
    cd "$REPO"
fi

if ! command -v ollama > /dev/null 2>&1; then
    echo "❌ Ollama not found."
    echo "· Install from: https://ollama.com"
    exit 1
fi

if curl -sf http://localhost:11434/api/tags > /dev/null 2>&1; then
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

# Check Ollama has at least one chat model available (AIStudio_532)
# Uses /api/tags — works regardless of which model is configured.
# Model-specific validation is handled by the backend at query time.
_OLLAMA_READY=0
for _attempt in 1 2 3; do
    _MODELS=$(curl -sf http://localhost:11434/api/tags 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    chat = [m for m in d.get('models', []) if 'embed' not in m.get('name','').lower()]
    print(len(chat))
except: print(0)
" 2>/dev/null || echo "0")
    if [[ "$_MODELS" -gt 0 ]]; then
        _OLLAMA_READY=1
        break
    fi
    [[ "$_attempt" -lt 3 ]] && sleep 2
done
if [[ "$_OLLAMA_READY" -eq 0 ]]; then
    echo "❌ No chat models found in Ollama."
    echo "· Run: ollama pull llama3.1:8b"
    echo "· This takes ~5 minutes on first run (~4.7 GB download)."
    exit 1
fi

echo "▶ Starting AIStudio backend..."
cd "$REPO"
mkdir -p "$HOME/Library/Logs/AIStudio"

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
    if curl -s "$API/health" > /dev/null 2>&1; then
        BACKEND_READY=1
        break
    fi
done
if [[ "$BACKEND_READY" -eq 1 ]]; then
    echo "✅ Backend started."
else
    echo "⚠ Backend slow to start — opening UI anyway."
fi

# ── Processing ────────────────────────────────────────────────────────────────
_sep "Processing"

# First-run detection: trigger ingest for demo and help if collections are empty
_trigger_first_run_ingest() {
    local corpus="$1"
    local collection="aistudio_${corpus}"

    # Check Qdrant collection status
    local check
    check=$(curl -s "http://localhost:6333/collections/${collection}" 2>/dev/null)

    if echo "$check" | grep -q '"status":"ok"'; then
        local count
        count=$(echo "$check" | python3 -c "
import sys, json
d = json.load(sys.stdin)
r = d.get('result', {})
print(r.get('points_count') or r.get('vectors_count') or 0)
" 2>/dev/null || echo "0")
        if [[ "$count" -gt 0 ]]; then
            echo "✅ ${corpus} corpus indexed: ${count} chunks."
            return
        fi
    fi

    # Collection missing or empty — trigger first-run ingest (fire and forget)
    echo "▶ First run: indexing ${corpus} corpus — UI will show progress..."
    curl -sf -X POST "${API}/corpus/${corpus}/ingest" > /dev/null 2>&1 || \
        echo "⚠ Could not trigger ${corpus} ingest — start may have been too fast. UI will retry."
}

_trigger_first_run_ingest "demo"
_trigger_first_run_ingest "help"

# ── Reporting ─────────────────────────────────────────────────────────────────
_sep "Reporting"
echo "▶ Opening frontend..."
if [[ "$NO_OPEN" -eq 0 ]]; then
    open "$FRONTEND"
fi
echo "✅ AIStudio is running."
echo "· Frontend : $FRONTEND"
echo "· Backend  : $API"
echo "· Qdrant   : http://localhost:6333"
echo "· Ollama   : http://localhost:11434"
echo "· Logs     : ais_log"
echo "· To stop  : ais_stop"
echo "· To restart: ais_start"
[[ "$VERBOSE" -eq 1 ]] && echo "· Verbose mode active."

# ── Show splash (AIStudio_515) ────────────────────────────────────────────────
if [[ "$SHOW_SPLASH" -eq 1 ]]; then
    osascript > /dev/null 2>&1 << APPLESCRIPT
display dialog "AIStudio is running.

Frontend: file://${FRONTEND}
Backend:  ${API}" with title "AIStudio" buttons {"OK"} default button "OK" with icon note
APPLESCRIPT
fi

# ── Show log tab ──────────────────────────────────────────────────────────────
if [[ "$SHOW_LOG" -eq 1 ]]; then
    osascript 2>/dev/null << APPLESCRIPT
tell application "iTerm2"
    tell current window
        create tab with default profile
        tell current session
            write text "tail -f '${LOG_FILE}'"
        end tell
    end tell
end tell
APPLESCRIPT
fi
