#!/bin/bash
# AIStudio Stop Script
# Run from anywhere — stops all AIStudio services
# Mac/Apple Silicon only (Release 1.x)

echo "🛑 Stopping AIStudio..."

# 1. Uvicorn / FastAPI backend
if lsof -ti:8000 > /dev/null 2>&1; then
    kill $(lsof -ti:8000) 2>/dev/null
    echo "✓ Backend stopped (port 8000)"
else
    echo "  Backend not running"
fi

# 2. Qdrant
if lsof -ti:6333 > /dev/null 2>&1; then
    kill $(lsof -ti:6333) 2>/dev/null
    echo "✓ Qdrant stopped (port 6333)"
else
    echo "  Qdrant not running"
fi

# 3. Ollama — leave running (system service, fast to reuse)
echo "  Ollama left running (system service)"

echo ""
echo "✅ AIStudio stopped."
echo "   To restart: type ais_start from any terminal"
