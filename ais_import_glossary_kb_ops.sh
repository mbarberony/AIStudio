#!/usr/bin/env zsh
# ais_import_glossary_kb_ops.sh — Build the term-glossary KB for a corpus (Operator only)
# Version: 1.0.0
# Thin "$@" passthrough to scripts/ais_import_glossary_kb_ops.py — the wrapper the v1.8.27
# KB-importer split never created (manifest entry + backing .py shipped, .sh did not, so the
# command never resolved on PATH). Builds a term->expansion glossary from a static curated
# seed (bis_basel now; nist_ai_rmf/esrs planned), read at query time by rag_core for BM25
# expansion. Deterministic — writes in one pass, no review gate.

# ── Source guard: this script must be executed, not sourced ──────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

VERSION="1.0.0"
SCRIPT_NAME="ais_import_glossary_kb_ops"
SCRIPT_DIR="${0:A:h}"
HELP_FILE="$SCRIPT_DIR/ais_command_help_ops.txt"

_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$" | grep -v "^## "
    else
        echo "$SCRIPT_NAME v$VERSION — Build the term-glossary KB for a corpus"
        echo ""
        echo "Usage: $SCRIPT_NAME --source <K> [--corpus <C>] [--scope <S>] [--force]"
        echo ""
        echo "  --source <K>   Glossary source: bis_basel (nist_ai_rmf, esrs planned)"
        echo "  --corpus <C>   Corpus name (default applies corpus-wide)"
        echo "  --scope <S>    Scope ID"
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
SCRIPT="$REPO/scripts/ais_import_glossary_kb_ops.py"

printf '\033[1m[ais_import_glossary_kb_ops v%s — Build glossary KB]\033[0m\n' "$VERSION"

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
