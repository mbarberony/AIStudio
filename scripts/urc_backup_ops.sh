#!/usr/bin/env zsh
# urc_backup_ops.sh — Cross-domain workspace backup wrapper
# Usage: urc_backup [--target <path>] [--no-sec-10k] [--help] [--version]
#
# Thin wrapper per STD - AIStudio - Command Development and Management §7.
# All business logic lives in scripts/urc/backup_ops.py. Wrapper handles only:
#   - --help  (reads from ais_command_help_ops.txt with inline fallback)
#   - PYTHONPATH setup
#   - exec to Python module
# --version, --target, --no-sec-10k all parsed by the Python module.
#
# See: scripts/urc/backup_ops.py for the actual backup logic.


# ── Source guard: this script must be executed, not sourced ──────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

SCRIPT_NAME="urc_backup"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$SCRIPT_DIR/.." && pwd)"
HELP_FILE="$REPO/ais_command_help_ops.txt"

_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$"
    else
        echo "$SCRIPT_NAME — Cross-domain workspace backup"
        echo ""
        echo "Usage: $SCRIPT_NAME [--target <path>] [--no-sec-10k] [--help] [--version]"
        echo ""
        echo "Options:"
        echo "  --target <path>   Directory to back up (default: ~/Developer/AIStudio)"
        echo "  --no-sec-10k      Exclude data/corpora/sec_10k/uploads/ (large SEC files)"
        echo "  --help            Show this help"
        echo "  --version         Show version"
        echo ""
        echo "Backup destination:"
        echo "  ~/Library/Mobile Documents/com~apple~CloudDocs/Backups/urcrew/"
        echo "  (iCloud-synced, NOT under ~/Documents/)"
    fi
}

# Wrapper handles --help only. Everything else goes to Python.
if [[ "${1:-}" == "--help" ]]; then _show_help; exit 0; fi

# ── Set up PYTHONPATH and exec the Python module ─────────────────────────────
exec env PYTHONPATH="$REPO/scripts:${PYTHONPATH:-}" python3 -m urc.backup_ops "$@"
