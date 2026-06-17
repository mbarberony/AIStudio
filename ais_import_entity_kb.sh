#!/usr/bin/env zsh
# ais_import_entity_kb.sh — Build the GLEIF/Wikidata entity KB for a corpus (civilian / user command)
# Version: 1.0.0
# Civilian twin of ais_import_entity_kb_ops — a thin "$@" passthrough to the SHARED backing
# scripts/ais_import_entity_kb.py (civilian copy; ais_import_entity_kb.py is bundle-only). User-facing + git-tracked + install:user so it ships to
# users and appears in ais_user_commands_manifest.yaml. Reads the corpus full_scope, links each
# row to its uploads filing(s), resolves identity (LEI-is-input), and on --apply builds the
# xbrl-keyed entity KB the ingest pipeline reads for the [Document:] alias prefix.
# REVIEW-GATE: default is review-only (no writes); --apply performs the build.
# Reads help from the USER help file (ais_command_help.txt). _show_help falls back to the inline
# usage whenever the file is missing OR the section yields nothing (fixes the silent-empty F-012).

# ── Source guard: this script must be executed, not sourced ──────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

VERSION="1.0.0"
SCRIPT_NAME="ais_import_entity_kb"
SCRIPT_DIR="${0:A:h}"
HELP_FILE="$SCRIPT_DIR/ais_command_help.txt"

_inline_help() {
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
    echo "Without --apply nothing is written — the run previews the resolved rows only."
    echo "Run from: ~/Developer/AIStudio"
}

_show_help() {
    # Try the help file first; FALL BACK to inline usage if the file is missing OR the
    # section parse comes back empty (the silent-empty failure mode — F-012 hardening).
    local from_file=""
    if [[ -f "$HELP_FILE" ]]; then
        from_file=$(awk "/^## $SCRIPT_NAME\$/,/^---\$/" "$HELP_FILE" | grep -v "^---\$" | grep -v "^## ")
    fi
    if [[ -n "${from_file//[[:space:]]/}" ]]; then
        print -r -- "$from_file"
    else
        _inline_help
    fi
}

if [[ "${1:-}" == "--help" ]]; then _show_help; exit 0; fi
if [[ "${1:-}" == "--version" ]]; then echo "$SCRIPT_NAME v$VERSION"; exit 0; fi

REPO="$SCRIPT_DIR"
PYTHON="$REPO/.venv/bin/python3"
SCRIPT="$REPO/scripts/ais_import_entity_kb.py"

# Header shows the BACKING engine version (the one that changes), per STD §2.
BACKING_VERSION=$(grep -m1 -E '^VERSION = ' "$SCRIPT" 2>/dev/null | sed -E 's/.*"([^"]+)".*/\1/')
[[ -z "$BACKING_VERSION" ]] && BACKING_VERSION="$VERSION"
printf '\033[1m[ais_import_entity_kb v%s — Build entity KB]\033[0m\n' "$BACKING_VERSION"

if [[ ! -f "$PYTHON" ]]; then
    echo "❌ Python venv not found: $PYTHON"
    exit 1
fi
if [[ ! -f "$SCRIPT" ]]; then
    echo "❌ Script not found: $SCRIPT"
    exit 1
fi

cd "$REPO"
source .venv/bin/activate
exec env PYTHONPATH=src python3 "$SCRIPT" "$@"
