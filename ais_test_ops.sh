#!/usr/bin/env zsh
# ais_test_ops.sh — AIStudio operator test runner
# Version: 1.2.0
# 1.2.0: fix PYTHONPATH=src and python3 binary (AIStudio_557)

# ── Source guard ──────────────────────────────────────────────────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

set -euo pipefail

VERSION="1.2.0"
SCRIPT_DIR="${0:A:h}"
REPO="$SCRIPT_DIR"
SCRIPT_NAME="ais_test_ops"
HELP_FILE="$SCRIPT_DIR/ais_command_help_ops.txt"

# ── Output helpers ────────────────────────────────────────────────────────────
_sep()  { printf '\033[2m\033[3m--- %s\033[0m\n' "$1"; }
_out()  { echo "$@"; }
_err()  { echo "$@" >&2; }

# ── Help ──────────────────────────────────────────────────────────────────────
_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$"
    else
        echo "$SCRIPT_NAME v$VERSION"
        echo ""
        echo "Usage: $SCRIPT_NAME [--help] [--version] [--group <name>] [<group>]"
        echo ""
        echo "Options:"
        echo "  --help            Show this help"
        echo "  --version         Show script version"
        echo "  --group <name>    Test group to run"
        echo "  <group>           Shorthand: ais_test_ops lifecycle (no flag needed)"
        echo ""
        echo "Groups: unit | all | health | models | corpora | upload | lifecycle | api | citations | memory | retrieval"
        echo ""
        echo "· Default: unit (pytest, no server required)"
        echo "· Integration groups require: ais_start must be running"
    fi
}

# ── Flags before any logic ────────────────────────────────────────────────────
if [[ "${1:-}" == "--help" ]];    then _show_help; exit 0; fi
if [[ "${1:-}" == "--version" ]]; then _out "$SCRIPT_NAME v$VERSION"; exit 0; fi

printf '\033[1m[%s v%s — AIStudio operator test runner]\033[0m\n' "$SCRIPT_NAME" "$VERSION"

# ── Parse group — supports both --group <name> and positional <name> ──────────
GROUP="unit"
if [[ "${1:-}" == "--group" && -n "${2:-}" ]]; then
    GROUP="$2"
elif [[ -n "${1:-}" && "${1:-}" != --* ]]; then
    GROUP="$1"
fi

# ── Unit tests (pytest) ───────────────────────────────────────────────────────
if [[ "$GROUP" == "unit" ]]; then
    _sep "Unit tests"
    cd "$REPO"
    source .venv/bin/activate
    PYTHONPATH="$REPO/src" .venv/bin/python3 -m pytest -q -m "not integration"
    exit $?
fi

# ── Integration tests — verify backend first ─────────────────────────────────
if ! curl -sf "http://localhost:8000/health" > /dev/null 2>&1; then
    _err "❌ Backend not reachable — integration tests require a running AIStudio instance."
    _err "· Run: ais_start"
    exit 1
fi

_sep "Integration tests — group: $GROUP"
cd "$REPO"
source .venv/bin/activate
PYTHONPATH="$REPO/src" .venv/bin/python3 tests/test_aistudio.py --group "$GROUP"
exit $?
