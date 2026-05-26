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
        echo "Usage: $SCRIPT_NAME [--help] [--version] [options]"
        echo ""
        echo "Options:"
        echo "  --help            Show this help"
        echo "  --version         Show script version"
        echo ""
        echo "· Downloads ~10 ESEF XHTML filings (~50-200MB total)"
        echo "· Source: filings.xbrl.org (XBRL International public repository)"
        echo "· Next step: create corpus 'esef_banks' in UI, then ingest"
        echo "· Additional options: see ais_command_help.txt ## ais_download_esef"
    fi
}

if [[ "$1" == "--help" ]]; then _show_help; exit 0; fi

REPO="${0:A:h}"
UPLOADS="$REPO/data/corpora/esef_banks/uploads"
mkdir -p "$UPLOADS"

cd "$REPO"
source .venv/bin/activate

exec env PYTHONPATH=src python3 "$REPO/scripts/download_esef_corpus.py" --out "$UPLOADS" "$@"
