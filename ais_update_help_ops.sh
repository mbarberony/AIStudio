#!/usr/bin/env bash
# ais_update_help_ops.sh — AIStudio Help Corpus Updater (Operator only)
# Version: 1.3.0
# Regenerates help corpus PDFs and copies to data/corpora/help/uploads/

VERSION="1.3.0"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="$REPO_ROOT/.venv/bin/python3"
SCRIPT="$REPO_ROOT/scripts/update_help_corpus.py"

if [[ "$1" == "--version" ]]; then
    echo "ais_update_help_ops v$VERSION"
    exit 0
fi

if [[ "$1" == "--help" ]]; then
    echo "ais_update_help_ops v$VERSION"
    echo ""
    echo "Usage:"
    echo "  ais_update_help_ops              Update all help corpus subjects"
    echo "  ais_update_help_ops <subject>    Update one subject (e.g. howto, readme, quickstart)"
    echo "  ais_update_help_ops --help       Show this help"
    echo ""
    echo "What it does:"
    echo "  1. Reads meta/help_manifest.yaml"
    echo "  2. Resolves latest dated version of source .md files"
    echo "  3. Generates PDFs from source .md files"
    echo "  4. Copies PDFs to data/corpora/help/uploads/"
    echo ""
    echo "After running, re-ingest the help corpus via the UI:"
    echo "  1. Open AIStudio"
    echo "  2. Select the 'help' corpus"
    echo "  3. Click Add and select all PDFs from ~/Downloads/"
    exit 0
fi

echo "+============================================================+"
echo "|        AIStudio Help Corpus Updater v$VERSION               |"
echo "+============================================================+"
echo ""

if [[ ! -f "$PYTHON" ]]; then
    echo "❌ Python venv not found. Activate: source $REPO_ROOT/.venv/bin/activate"
    exit 1
fi

if [[ ! -f "$SCRIPT" ]]; then
    echo "❌ Script not found: $SCRIPT"
    echo "   Run: ais_restore_scripts"
    exit 1
fi

if [[ -n "$1" ]]; then
    "$PYTHON" "$SCRIPT" --repo-root "$REPO_ROOT" --subject "$1"
else
    "$PYTHON" "$SCRIPT" --repo-root "$REPO_ROOT"
fi
