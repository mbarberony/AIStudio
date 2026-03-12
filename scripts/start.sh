#!/bin/bash

# AIStudio Auto-Launch Script
# Mac/Apple Silicon only (Release 1.x)

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
cd "$REPO_ROOT"
source "$VENV/bin/activate"
OLLAMA_KEEP_ALIVE=30m AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
    uvicorn local_llm_bot.app.api:app --port 8000 &
sleep 2
echo "✓ Backend started on http://localhost:8000"

# 4. Open frontend
echo "▶ Opening frontend..."
open "$FRONTEND"

echo ""
echo "✅ AIStudio is running."
echo "   Frontend : $FRONTEND"
echo "   Backend  : http://localhost:8000"
echo "   Qdrant   : http://localhost:6333"
echo "   Ollama   : http://localhost:11434"
echo ""
echo "To stop everything: kill \$(lsof -ti:8000) \$(lsof -ti:6333)"
