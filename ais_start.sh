#!/usr/bin/env bash
# ais_start.sh — Start all AIStudio services (thin wrapper, §7 pattern)
# Version: 3.0.0
# Changelog: 3.0.0 — AIStudio_714/715: migrate to wrapper-backed pattern per STD §7.
#            Wrapper owns --help (reads ais_command_help.txt via awk) + PYTHONPATH + exec.
#            All business logic moved to scripts/ais_start.py.
# Changelog: 2.1.1 — fix --start_with fragment handling
# Changelog: 2.1.0 — AIStudio_767: --start_with <corpus> flag
# Changelog: 2.0.5 — extend backend health poll

set -euo pipefail

[[ "${ZSH_EVAL_CONTEXT:-}" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

SCRIPT_NAME="ais_start"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$SCRIPT_DIR"
HELP_FILE="$REPO/ais_command_help.txt"
VENV="$REPO/.venv"

# ── --help: wrapper owns this, never reaches Python ───────────────────────────
_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$" | grep -v "^## "
    else
        echo "$SCRIPT_NAME — Start all AIStudio services"
        echo "Usage: $SCRIPT_NAME [--help] [--version] [--verbose] [--show-log]"
        echo "       [--show-splash] [--no-separator] [--no-open] [--start_with <corpus>]"
        echo "· To stop: ais_stop  · Logs: ais_log"
    fi
}
if [[ "${1:-}" == "--help" ]] || [[ "${1:-}" == "-h" ]]; then _show_help; exit 0; fi

# ── Venv ──────────────────────────────────────────────────────────────────────
if [[ ! -f "$VENV/bin/activate" ]]; then
    echo "❌ Virtual environment not found at $VENV."
    echo "· Run: ./ais_install"
    exit 1
fi
source "$VENV/bin/activate"

# ── Delegate all remaining logic to Python (§7: exec, PYTHONPATH set here) ───
exec env PYTHONPATH="$REPO/src" python3 "$REPO/scripts/ais_start.py" "$@"
