#!/usr/bin/env zsh
# ais_import_knowledge_base.sh — Import external knowledge source data for a corpus scope
# Version: 1.0.0

# ── Source guard ─────────────────────────────────────────────────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

set -euo pipefail

SCRIPT_DIR="${0:A:h}"
REPO="$SCRIPT_DIR"
SCRIPT_NAME="ais_import_knowledge_base"
HELP_FILE="$SCRIPT_DIR/ais_command_help.txt"

_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$" | grep -v "^## "
    else
        echo "$SCRIPT_NAME — Import external knowledge source data for a corpus scope"
        echo ""
        echo "Usage: $SCRIPT_NAME --source <K> --corpus <C> --scope <S> [options]"
        echo "       $SCRIPT_NAME --list"
        echo ""
        echo "Options:"
        echo "  --source <K>      Knowledge source: gleif | sec_edgar | bis_basel | nist_ai_rmf | esrs"
        echo "  --corpus <C>      Corpus name (e.g. sec_10k, esef_banks)"
        echo "  --scope <S>       Scope ID (e.g. 25_firms, full)"
        echo "  --force           Overwrite existing output file"
        echo "  --list            Show all imported knowledge sources from catalog"
        echo "  --help            Show this help"
        echo "  --version         Show version"
        echo ""
        echo "Examples:"
        echo "  $SCRIPT_NAME --source gleif --corpus sec_10k --scope 25_firms"
        echo "  $SCRIPT_NAME --source bis_basel --corpus any_corpus --scope full"
        echo "  $SCRIPT_NAME --list"
    fi
}

if [[ "$1" == "--help" ]]; then _show_help; exit 0; fi

cd "$REPO"
source .venv/bin/activate

exec env PYTHONPATH=src python3 "$REPO/scripts/ais_import_knowledge_base.py" "$@"
