#!/bin/bash
# AIStudio Stop Script v1.4.0
# Run from anywhere — stops all AIStudio services
# Mac/Apple Silicon only (Release 1.x)
# v1.1.0: graceful Qdrant shutdown (SIGTERM + wait) — prevents WAL corruption (AIStudio_066)
# v1.2.0: log PID when killing backend — visibility into what was running
# v1.3.0: kill ALL PIDs on port 8000 — handles multiple backend processes
# v1.4.0: CLI output standard; --silent flag; --help/--version

VERSION="1.4.0"
ITALIC=$'\e[3m'
RESET=$'\e[0m'
DIM=$'\e[2m'

# ── Parse flags ───────────────────────────────────────────────────
SILENT=0
SEPARATOR=1
for arg in "$@"; do
    [[ "$arg" == "--silent" ]] && SILENT=1
    [[ "$arg" == "--no-separator" ]] && SEPARATOR=0
    [[ "$arg" == "--version" ]] && { echo "ais_stop v$VERSION — Stop AIStudio services"; exit 0; }
    if [[ "$arg" == "--help" ]]; then
        echo "ais_stop v$VERSION — Stop AIStudio services"
        echo ""
        echo "Stop all AIStudio services: FastAPI backend and Qdrant."
        echo "Ollama is left running (system service)."
        echo ""
        echo "Usage: ais_stop [options]"
        echo ""
        echo "Options:"
        echo "  --silent       Suppress all output except errors (for use by other commands)"
        echo "  --no-separator Use blank lines instead of --- section labels"
        echo "  --version      Show version and exit"
        echo "  --help         Show this help and exit"
        echo ""
        echo "· To restart: ais_start"
        exit 0
    fi
done

sep() {
    [[ "$SILENT" -eq 1 ]] && return
    if [[ "$SEPARATOR" -eq 1 ]]; then
        echo "${DIM}--- ${ITALIC}$1${RESET}"
    else
        echo ""
    fi
}

out() { [[ "$SILENT" -eq 0 ]] && echo "$@"; }
err() { echo "$@"; }  # errors always print

[[ "$SILENT" -eq 0 ]] && echo "ais_stop v$VERSION — Stop AIStudio services"

# ── Cleanup ───────────────────────────────────────────────────────
sep "Cleanup"
out "🛑 Stopping AIStudio..."

# 1. Uvicorn / FastAPI backend
BACKEND_PIDS=$(lsof -ti:8000 2>/dev/null || true)
if [ -n "$BACKEND_PIDS" ]; then
    echo "$BACKEND_PIDS" | xargs kill 2>/dev/null || true
    sleep 1
    out "✅ Backend stopped (pid(s): $(echo $BACKEND_PIDS | tr '\n' ' '), port 8000)."
else
    out "· Backend not running."
fi

# 2. Qdrant — graceful shutdown (SIGTERM + wait, then SIGKILL fallback)
if lsof -ti:6333 > /dev/null 2>&1; then
    QDRANT_PID=$(lsof -ti:6333)
    kill -TERM "$QDRANT_PID" 2>/dev/null
    for i in 1 2 3 4 5; do
        sleep 1
        if ! kill -0 "$QDRANT_PID" 2>/dev/null; then
            break
        fi
    done
    if kill -0 "$QDRANT_PID" 2>/dev/null; then
        kill -KILL "$QDRANT_PID" 2>/dev/null
    fi
    out "✅ Qdrant stopped (port 6333)."
else
    out "· Qdrant not running."
fi

# 3. Ollama — leave running
out "· Ollama left running (system service)."

# ── Reporting ─────────────────────────────────────────────────────
sep "Reporting"
out "✅ AIStudio stopped."
out "· To restart: ais_start"
