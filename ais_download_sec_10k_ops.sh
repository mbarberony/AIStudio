#!/usr/bin/env zsh
# ais_download_sec_10k_ops.sh — Operator SEC 10-K downloader (single-CIK capable)
# Version: 1.0.0
# Operator variant of ais_download_sec_10k. Adds --cik <cik> to (re)download a
# single firm's 5 most-recent 10-Ks — e.g. replacing the contaminated CBOE files
# (AIStudio_667). Defaults --out to data/corpora/sec_10k/uploads (sec_10k only).
# Passthrough wrapper (§7): all flags/defaults live in scripts/download_sec_corpus_ops.py.


# ── Source guard: this script must be executed, not sourced ──────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

VERSION="1.0.0"

SCRIPT_NAME="ais_download_sec_10k_ops"
SCRIPT_DIR="${0:A:h}"
HELP_FILE="$SCRIPT_DIR/ais_command_help_ops.txt"

_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$" | grep -v "^## "
    else
        echo "$SCRIPT_NAME v$VERSION"
        echo ""
        echo "Usage: $SCRIPT_NAME [--cik <cik>] [--name <name>] [--max-results-per-firm N] [--out DIR]"
        echo ""
        echo "Run from: ~/Developer/AIStudio"
    fi
}

if [[ "$1" == "--help" ]]; then _show_help; exit 0; fi
if [[ "$1" == "--version" ]]; then echo "$SCRIPT_NAME v$VERSION"; exit 0; fi

REPO="${0:A:h}"

printf "\033[1m[ais_download_sec_10k_ops v$VERSION — Operator SEC 10-K downloader]\033[0m\n"

# cd to repo so the backing script's relative --out default
# (data/corpora/sec_10k/uploads) resolves against the repo root.
cd "$REPO" || { echo "❌ Could not cd to repo root: $REPO"; exit 1; }
source .venv/bin/activate || { echo "❌ Could not activate .venv"; exit 1; }

echo "--- Preflight"
echo "✅ Repo: $REPO"
echo "· Default output (unless --out given): data/corpora/sec_10k/uploads/"
echo ""

# §7 passthrough — all flags and defaults are owned by the backing argparse.
python3 scripts/download_sec_corpus_ops.py "$@"
RC=$?

echo ""
echo "--- Next step"
echo "· Re-ingest to replace stale chunks: ais_ingest_sec_10k  (use --force to wipe + reindex)"

exit $RC
