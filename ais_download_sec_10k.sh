#!/usr/bin/env zsh
# ais_download_sec_10k.sh — Download SEC 10-K corpus from EDGAR
# Version: 1.1.2
# Downloads ~143 filings from 25 financial services firms (~500MB)
# Output goes to data/corpora/sec_10k/uploads/ by default


# ── Source guard: this script must be executed, not sourced ──────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

VERSION="1.1.2"

SCRIPT_NAME="ais_download_sec_10k"
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

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

printf "\033[1m[ais_download_sec_10k v$VERSION — Download SEC 10-K filings from EDGAR]\033[0m\n"

# Create corpus upload directory if needed
UPLOADS="$REPO/data/corpora/sec_10k/uploads"
mkdir -p "$UPLOADS"

cd "$REPO"
source .venv/bin/activate

echo "--- Preflight"
echo "✅ Output directory ready: data/corpora/sec_10k/uploads/"

echo ""
echo "--- Downloading"
echo "▶ Fetching SEC 10-K filings from EDGAR..."
echo "· ~143 filings, ~500MB — allow 5–10 minutes"
echo ""

python3 scripts/download_sec_corpus.py --out "$UPLOADS" "$@"

echo ""
echo "--- Summary"
FILE_COUNT=$(ls "$UPLOADS"/*.htm 2>/dev/null | wc -l | tr -d ' ')
echo "✅ $FILE_COUNT filings downloaded to data/corpora/sec_10k/uploads/"
echo "· Next step: ais_ingest_sec_10k"
