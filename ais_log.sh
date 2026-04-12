#!/bin/bash
# ais_log — Tail the AIStudio backend log
# Version: 1.0.0
# Mac/Apple Silicon only (Release 1.x)

VERSION="1.0.0"
LOG_FILE="$HOME/Library/Logs/AIStudio/backend.log"

if [[ "$1" == "--version" ]]; then echo "ais_log v$VERSION — Tail AIStudio backend log"; exit 0; fi
if [[ "$1" == "--help" ]]; then
    echo "ais_log v$VERSION — Tail AIStudio backend log"
    echo ""
    echo "Show live backend log output from the AIStudio FastAPI server."
    echo "Useful for debugging — run in a separate terminal tab after ais_start."
    echo ""
    echo "Usage: ais_log"
    echo ""
    echo "Options:"
    echo "  --version   Show version and exit"
    echo "  --help      Show this help and exit"
    echo ""
    echo "· Log file: $LOG_FILE"
    echo "· Press Ctrl+C to exit"
    exit 0
fi

echo "ais_log v$VERSION — Tail AIStudio backend log"

if [[ ! -f "$LOG_FILE" ]]; then
    echo "⚠ Log file not found: $LOG_FILE"
    echo "· Run ais_start first to create the log."
    exit 1
fi

echo "· Tailing: $LOG_FILE"
echo "· Press Ctrl+C to exit."
echo ""
tail -f "$LOG_FILE"
