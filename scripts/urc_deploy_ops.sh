#!/usr/bin/env bash
# urc_deploy_ops.sh — Wrapper for urc_deploy (cross-domain operator file deploy)
# Wraps scripts/urc/deploy_ops.py per Command Development STD §0 + §7
# (Wrapper-Backed Command Pattern).
#
# Per STD: wrapper handles --help and --version locally. Everything else
# (file args, --last, --to, --silent, --verbose, --no-separator, etc.) passes
# through to Python via exec.
#
# Version is owned by the Python module (single source of truth).
# Bold bracketed header is printed by Python on every run.

set -euo pipefail

SCRIPT_NAME="urc_deploy"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(dirname "$SCRIPT_DIR")"
HELP_FILE="$REPO/ais_command_help_ops.txt"
PYTHON="$REPO/.venv/bin/python3"

_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        # Extract this command's section from central help file
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$"
    else
        # Inline fallback — works on fresh clone without help file
        echo "$SCRIPT_NAME — cross-domain operator file deploy"
        echo ""
        echo "Usage: $SCRIPT_NAME [--help] [--version] [<file1> [file2] ...] [--last] [--to <dest> <file>] [<bundle.zip>]"
        echo ""
        echo "Options:"
        echo "  --help              Show this help and exit"
        echo "  --version           Show version and exit"
        echo "  --last              Deploy the most recently downloaded file in ~/Downloads"
        echo "  --to <dest>         Override destination directory for the file"
        echo "  --silent            Suppress informational output (errors still shown)"
        echo "  --verbose           Show full subprocess output"
        echo "  --no-separator      Replace --- Section labels with blank lines"
        echo ""
        echo "· Routing: --to override → bundle_manifest.yaml deploy_to → repo search → prompt"
        echo "· Docs: meta/bundle_manifest.yaml and HOWTO_OPS.md"
    fi
}

# --help and --version: handled by wrapper (STD §1 — must be first checks)
if [[ "${1:-}" == "--help" ]]; then _show_help; exit 0; fi
if [[ "${1:-}" == "--version" ]]; then
    # Delegate to Python — single source of truth for version
    exec env PYTHONPATH="$REPO/scripts" "$PYTHON" -m urc.deploy_ops --version
fi

# Verify Python venv exists
if [[ ! -x "$PYTHON" ]]; then
    echo "❌ Python venv not found: $PYTHON" >&2
    echo "· Run install_ops to set up the venv, or check ~/Developer/AIStudio/.venv/." >&2
    exit 1
fi

# Pass through to Python with all args. PYTHONPATH points at scripts/ so
# `python3 -m urc.deploy_ops` finds the package at scripts/urc/.
exec env PYTHONPATH="$REPO/scripts" "$PYTHON" -m urc.deploy_ops "$@"
