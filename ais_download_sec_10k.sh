#!/usr/bin/env zsh
# ais_download_sec_10k.sh — Download SEC 10-K corpus from EDGAR
# Version: 1.1.7
# Thin "$@" passthrough to scripts/download_sec_corpus.py. Firm set and year selection
# (--latest N / --years YYYY ...) are owned by the backing argparse. Default run (no args)
# = the scope's firms × latest 1. Output → data/corpora/sec_10k/uploads/ by default.
#
# v1.1.7 — STD - AIStudio - CLI Output v2.3.0 reconciliation. (1) The bold §2 header now
#   shows the BACKING engine version (download_sec_corpus.py), the version that actually
#   changes, not the wrapper's. (2) Dropped the wrapper's own `--- Downloading ▶ Fetching…`
#   opener and `--- Summary ✅ N filings` block — the backing script now owns the processing
#   bundle (▶ Downloading…) and the closing summary (✅ … downloaded), so those were doubling.
#   The wrapper keeps only the Preflight bundle + the version header.


# ── Source guard: this script must be executed, not sourced ──────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

VERSION="1.1.7"

SCRIPT_NAME="ais_download_sec_10k"
SCRIPT_DIR="${0:A:h}"
HELP_FILE="$SCRIPT_DIR/ais_command_help.txt"

_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$" | grep -v "^## "
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

REPO="${0:A:h}"

# Header shows the BACKING engine version (the one that changes), per STD §2.
BACKING_VERSION=$(grep -m1 -E '^Version [0-9]' "$REPO/scripts/download_sec_corpus.py" 2>/dev/null | awk '{print $2}')
[[ -z "$BACKING_VERSION" ]] && BACKING_VERSION="$VERSION"
printf "\033[1m[ais_download_sec_10k v$BACKING_VERSION — Download SEC 10-K filings from EDGAR]\033[0m\n"

# Create corpus upload directory if needed
UPLOADS="$REPO/data/corpora/sec_10k/uploads"
mkdir -p "$UPLOADS"

cd "$REPO"
source .venv/bin/activate

echo "--- Preflight"
echo "✅ Output directory ready: data/corpora/sec_10k/uploads/"
echo ""

# The backing script owns the processing bundle (▶ Downloading…) and the summary
# (✅ … downloaded · · output/inventory/next) per STD §1/§8 — no wrapper opener/summary.
python3 scripts/download_sec_corpus.py --out "$UPLOADS" "$@"
