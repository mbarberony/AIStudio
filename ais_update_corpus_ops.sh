#!/usr/bin/env zsh
# ais_update_corpus_ops.sh — AIStudio Corpus Updater (Operator only)
# Version: 1.0.0
# Thin wrapper around scripts/update_corpus_ops.py
# Identical CLI options for all corpora.
#
# Usage:
#   ais_update_corpus_ops help [--verbose] [--subject NAME] [--force] [--meta-only]
#   ais_update_corpus_ops demo [--verbose] [--rebuild] [--force] [--meta-only]

# ── Source guard ──────────────────────────────────────────────────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

VERSION="1.0.0"
SCRIPT_NAME="ais_update_corpus_ops"

if [[ "$1" == "--help" || -z "$1" ]]; then
    printf '\033[1m%s v%s\033[0m\n' "$SCRIPT_NAME" "$VERSION"
    echo ""
    echo "Usage: $SCRIPT_NAME <corpus> [options]"
    echo ""
    echo "  <corpus>       Corpus name: help, demo, or any future corpus"
    echo ""
    echo "Options (identical for all corpora):"
    echo "  --meta-only    Seed metadata + deploy questions only — no sync or ingest"
    echo "  --rebuild      Wipe uploads/ and Qdrant, re-ingest everything"
    echo "  --verbose      Show live ingest progress bars"
    echo "  --force        Force redeploy questions even if seed unchanged"
    echo "  --subject NAME Regenerate + surgical re-ingest one subject (generated corpora)"
    exit 0
fi

if [[ "$1" == "--version" ]]; then echo "$SCRIPT_NAME v$VERSION"; exit 0; fi

REPO="$(cd "$(dirname "$0")" && pwd)"
PYTHON="$REPO/.venv/bin/python3"
SCRIPT="$REPO/scripts/update_corpus_ops.py"

CORPUS="$1"
shift  # pass remaining args to Python

printf '\033[1m[ais_update_corpus_ops v%s — %s corpus]\033[0m\n' "$VERSION" "$CORPUS"

if [[ ! -f "$PYTHON" ]]; then
    echo "❌ Python venv not found: $PYTHON"
    exit 1
fi

if [[ ! -f "$SCRIPT" ]]; then
    echo "❌ Script not found: $SCRIPT"
    echo "· Run: ais_restore_scripts"
    exit 1
fi

exec "$PYTHON" "$SCRIPT" "$CORPUS" --repo-root "$REPO" "$@"
