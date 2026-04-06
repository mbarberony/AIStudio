#!/bin/bash

# AIStudio Auto-Launch Script v1.2.1
# Mac/Apple Silicon only (Release 1.x)
# v1.1.0: poll /health before opening browser — fixes race condition (AIStudio_066)
# v1.2.0: kill stale process on port 8000 before launch — fixes port conflict (AIStudio_103)
# v1.2.1: fix set -e interaction with lsof — lsof returns exit 1 when port is free

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
FRONTEND="$REPO_ROOT/front_end/rag_studio.html"
QDRANT_STORAGE="$HOME/qdrant_storage"
VENV="$REPO_ROOT/.venv"

echo "🚀 Starting AIStudio..."

# 1. Qdrant
if curl -s http://localhost:6333/healthz > /dev/null 2>&1; then
    echo "✓ Qdrant already running"
else
    echo "▶ Starting Qdrant..."
    mkdir -p "$QDRANT_STORAGE"
    cd "$QDRANT_STORAGE"
    QDRANT__STORAGE__STORAGE_PATH="$QDRANT_STORAGE" qdrant &
    sleep 2
    echo "✓ Qdrant started"
fi

# 2. Ollama
if curl -s http://localhost:11434 > /dev/null 2>&1; then
    echo "✓ Ollama already running"
else
    echo "▶ Starting Ollama..."
    ollama serve &
    sleep 3
    echo "✓ Ollama started"
fi

# 3. Uvicorn
echo "▶ Starting AIStudio backend..."
# Kill any stale process on port 8000 before binding
STALE_PID=$(lsof -ti:8000 2>/dev/null || true)
if [ -n "$STALE_PID" ]; then
    echo "  ⚠ Port 8000 in use — killed stale backend (pid $STALE_PID)"
    kill "$STALE_PID" 2>/dev/null
    sleep 1
fi
cd "$REPO_ROOT"
source "$VENV/bin/activate"
OLLAMA_KEEP_ALIVE=30m AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
    uvicorn local_llm_bot.app.api:app --port 8000 &

# Poll /health up to 15s before opening browser — prevents "Error loading corpora"
# race condition when UI opens before backend is ready
BACKEND_READY=0
for i in $(seq 1 15); do
    sleep 1
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        BACKEND_READY=1
        break
    fi
done
if [ "$BACKEND_READY" -eq 1 ]; then
    echo "✓ Backend started on http://localhost:8000"
else
    echo "⚠ Backend slow to start — opening UI anyway"
fi

# 4. Auto-ingest demo corpus if not already in Qdrant
DEMO_COLLECTION="aistudio_demo"
DEMO_CHECK=$(curl -s "http://localhost:6333/collections/$DEMO_COLLECTION" 2>/dev/null)

if echo "$DEMO_CHECK" | grep -q '"status":"ok"'; then
    echo "✓ Demo corpus already indexed"
else
    echo "▶ Demo corpus not found — ingesting for first time (~45 seconds)..."
    echo "  This happens once. Subsequent starts are instant."
    echo ""
    cd "$REPO_ROOT"
    source "$VENV/bin/activate"
    AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
        python3 -m local_llm_bot.app.ingest \
        --corpus demo \
        --root data/corpora/demo/uploads
    echo ""
    echo "✓ Demo corpus indexed and ready"
fi

# 5. Open frontend
echo "▶ Opening frontend..."
open "$FRONTEND"

echo ""
echo "✅ AIStudio is running."
echo "   Frontend : $FRONTEND"
echo "   Backend  : http://localhost:8000"
echo "   Qdrant   : http://localhost:6333"
echo "   Ollama   : http://localhost:11434"
echo ""
echo "To stop everything: ais_stop"
