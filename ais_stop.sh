#!/usr/bin/env bash
# ais_stop — Stop AIStudio services
# Wrapper around scripts/stop.sh for user convenience

# ── Source guard: this script must be executed, not sourced ──────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

VERSION="1.0.3"

SCRIPT_NAME="ais_stop"
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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

printf '\033[1m[ais_stop v%s — Stop all AIStudio services]\033[0m\n' "$VERSION"
exec "$SCRIPT_DIR/scripts/stop.sh" "$@"
