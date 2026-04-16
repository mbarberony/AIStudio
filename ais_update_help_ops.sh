#!/usr/bin/env bash
# ais_update_help_ops.sh — AIStudio Help Corpus Updater (Operator only)
# Version: 1.5.0
# Regenerates help corpus PDFs and copies to data/corpora/help/uploads/

VERSION="1.5.0"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="$REPO_ROOT/.venv/bin/python3"
SCRIPT="$REPO_ROOT/scripts/update_help_corpus_ops.py"
SILENT=false

printf "\033[1m[ais_update_help_ops v$VERSION — Regenerate help corpus PDFs]\033[0m\n"

if [[ "$1" == "--version" ]]; then
    exit 0
fi

if [[ "$1" == "--help" ]]; then
    echo ""
    echo "Usage:"
    echo "  ais_update_help_ops              Update all help corpus subjects"
    echo "  ais_update_help_ops <subject>    Update one subject (e.g. howto, readme, quickstart)"
    echo "  ais_update_help_ops --silent     Suppress all output except errors"
    echo "  ais_update_help_ops --version    Print version"
    echo "  ais_update_help_ops --help       Show this help"
    echo ""
    echo "What it does:"
    echo "  · Reads meta/help_manifest.yaml"
    echo "  · Resolves latest dated version of source .md files"
    echo "  · Generates PDFs from source .md files"
    echo "  · Copies PDFs to data/corpora/help/uploads/"
    echo ""
    echo "· After running, re-ingest the help corpus: ais_ingest_help_ops"
    exit 0
fi

if [[ "$1" == "--silent" ]]; then
    SILENT=true
    shift
fi

if [[ ! -f "$PYTHON" ]]; then
    echo "❌ Python venv not found. Activate: source $REPO_ROOT/.venv/bin/activate"
    exit 1
fi

if [[ ! -f "$SCRIPT" ]]; then
    echo "❌ Script not found: $SCRIPT"
    echo "· Run: ais_restore_scripts"
    exit 1
fi

if [[ "$SILENT" == true ]]; then
    if [[ -n "$1" ]]; then
        "$PYTHON" "$SCRIPT" --repo-root "$REPO_ROOT" --subject "$1" --silent
    else
        "$PYTHON" "$SCRIPT" --repo-root "$REPO_ROOT" --silent
    fi
else
    if [[ -n "$1" ]]; then
        "$PYTHON" "$SCRIPT" --repo-root "$REPO_ROOT" --subject "$1"
    else
        "$PYTHON" "$SCRIPT" --repo-root "$REPO_ROOT"
    fi
fi
