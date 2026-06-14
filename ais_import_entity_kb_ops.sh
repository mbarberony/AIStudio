#!/usr/bin/env zsh
# ais_import_entity_kb_ops.sh — Build the GLEIF/Wikidata entity KB for a corpus (Operator only)
# Version: 1.1.0
# Thin "$@" passthrough to scripts/ais_import_entity_kb_ops.py — the wrapper the v1.8.27
# KB-importer split never created (the .py backing script shipped without it, so the command
# never resolved on PATH). Reads the corpus full_scope (which IS the worksheet), links each
# row to its uploads filing(s), resolves identity (LEI-is-input), and on --apply builds the
# xbrl-keyed entity KB the ingest pipeline reads for the [Document:] alias prefix.
# v1.1.0 — banner reads the backing engine version (STD §2); --help fallback reconciled to the
#   1.5.0 full_scope flow (dropped the dead --rescan/--force/worksheet language).

# ── Source guard: this script must be executed, not sourced ──────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

VERSION="1.1.0"
SCRIPT_NAME="ais_import_entity_kb_ops"
SCRIPT_DIR="${0:A:h}"
HELP_FILE="$SCRIPT_DIR/ais_command_help_ops.txt"

_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$" | grep -v "^## "
    else
        echo "$SCRIPT_NAME v$VERSION — Build the GLEIF/Wikidata entity KB for a corpus"
        echo ""
        echo "Usage: $SCRIPT_NAME --corpus <C> [--apply] [--list]"
        echo ""
        echo "  --corpus <C>   Corpus name (reads data/corpora/<C>/<C>_full_scope.yaml)"
        echo "  --apply        Build the entity KB from the resolved rows (default: review only)"
        echo "  --list         Show the import catalog"
        echo "  --help         Show this help"
        echo "  --version      Show version"
        echo ""
        echo "Run from: ~/Developer/AIStudio"
    fi
}

if [[ "${1:-}" == "--help" ]]; then _show_help; exit 0; fi
if [[ "${1:-}" == "--version" ]]; then echo "$SCRIPT_NAME v$VERSION"; exit 0; fi

REPO="$SCRIPT_DIR"
PYTHON="$REPO/.venv/bin/python3"
SCRIPT="$REPO/scripts/ais_import_entity_kb_ops.py"

# Header shows the BACKING engine version (the one that changes), per STD §2.
BACKING_VERSION=$(grep -m1 -E '^VERSION = ' "$SCRIPT" 2>/dev/null | sed -E 's/.*"([^"]+)".*/\1/')
[[ -z "$BACKING_VERSION" ]] && BACKING_VERSION="$VERSION"
printf '\033[1m[ais_import_entity_kb_ops v%s — Build entity KB]\033[0m\n' "$BACKING_VERSION"

if [[ ! -f "$PYTHON" ]]; then
    echo "❌ Python venv not found: $PYTHON"
    exit 1
fi
if [[ ! -f "$SCRIPT" ]]; then
    echo "❌ Script not found: $SCRIPT"
    echo "· Run: ais_restore_scripts"
    exit 1
fi

cd "$REPO"
source .venv/bin/activate
exec env PYTHONPATH=src python3 "$SCRIPT" "$@"
