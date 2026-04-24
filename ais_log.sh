#!/bin/bash
# ais_log — Tail the AIStudio backend log
# Version: 1.0.1
# Mac/Apple Silicon only (Release 1.x)


# ── Source guard: this script must be executed, not sourced ──────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

VERSION="1.0.1"

SCRIPT_NAME="ais_log"
HELP_FILE="$SCRIPT_DIR/ais_command_help.txt"

_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$"
    else
        echo "$SCRIPT_NAME v$VERSION"
        echo ""
        echo "Usage: $SCRIPT_NAME [--help] [--version]"
        echo ""
        echo "Run from: ~/Developer/AIStudio"
    fi
}

if [[ "$1" == "--help" ]]; then _show_help; exit 0; fi
if [[ "$1" == "--version" ]]; then echo "$SCRIPT_NAME v$VERSION"; exit 0; fi

LOG_FILE="$HOME/Library/Logs/AIStudio/backend.log"

echo "· Tailing: $LOG_FILE"
echo "· Press Ctrl+C to exit."
echo ""
tail -f "$LOG_FILE"
