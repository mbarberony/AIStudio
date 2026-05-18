#!/usr/bin/env zsh
# ais_download_esef.sh — Download ESEF iXBRL annual reports from filings.xbrl.org

# ── Source guard ─────────────────────────────────────────────────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

SCRIPT_DIR="${0:A:h}"
HELP_FILE="$SCRIPT_DIR/ais_command_help.txt"
SCRIPT_NAME="ais_download_esef"

_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$" | grep -v "^## "
    else
        echo "$SCRIPT_NAME — Download ESEF iXBRL annual reports from filings.xbrl.org"
        echo ""
        echo "Usage: $SCRIPT_NAME [--out DIR] [--period-start YYYY-MM-DD] [--period-end YYYY-MM-DD]"
        echo ""
        echo "Options:"
        echo "  --help            Show this help"
        echo "  --version         Show script version"
        echo "  --out DIR         Output directory (default: data/corpora/esef_banks/uploads/)"
        echo "  --period-start    Earliest filing period end date (default: 2022-01-01)"
        echo "  --period-end      Latest filing period end date (default: 2025-12-31)"
        echo ""
        echo "· Downloads ~10 ESEF XHTML filings (~50-200MB total)"
        echo "· Source: filings.xbrl.org (XBRL International public repository)"
        echo "· Next step: create corpus 'esef_banks' in UI, then ingest"
    fi
}

if [[ "$1" == "--help" ]]; then _show_help; exit 0; fi

REPO="${0:A:h}"
UPLOADS="$REPO/data/corpora/esef_banks/uploads"
mkdir -p "$UPLOADS"

cd "$REPO"
source .venv/bin/activate

exec env PYTHONPATH=src python3 "$REPO/scripts/download_esef_corpus.py" \
    --out "$UPLOADS" \
    "$@"
