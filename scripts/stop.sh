#!/bin/bash
# AIStudio Stop Script v1.3.0
# Run from anywhere — stops all AIStudio services
# Mac/Apple Silicon only (Release 1.x)
# v1.1.0: graceful Qdrant shutdown (SIGTERM + wait) — prevents WAL corruption (AIStudio_066)
# v1.2.0: log PID when killing backend — visibility into what was running
# v1.3.0: kill ALL PIDs on port 8000 — handles multiple backend processes

echo "🛑 Stopping AIStudio..."

# 1. Uvicorn / FastAPI backend — kill all PIDs on port 8000 (may be multiple workers)
BACKEND_PIDS=$(lsof -ti:8000 2>/dev/null || true)
if [ -n "$BACKEND_PIDS" ]; then
    echo "$BACKEND_PIDS" | xargs kill 2>/dev/null || true
    echo "✓ Backend stopped (pid(s): $(echo $BACKEND_PIDS | tr '\n' ' '), port 8000)"
else
    echo "  Backend not running"
fi

# 2. Qdrant — graceful shutdown (SIGTERM + wait, then SIGKILL fallback)
# SIGKILL bypasses WAL flush and corrupts collections on next start.
# SIGTERM lets Qdrant close WAL cleanly before exiting.
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
    echo "✓ Qdrant stopped (port 6333)"
else
    echo "  Qdrant not running"
fi

# 3. Ollama — leave running (system service, fast to reuse)
echo "  Ollama left running (system service)"

echo ""
echo "✅ AIStudio stopped."
echo "   To restart: type ais_start from any terminal"
