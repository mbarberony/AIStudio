#!/usr/bin/env bash
# urc_xray_repo — thin wrapper (Command Dev STD §7). Lives in scripts/ like urc_deploy_ops.sh
# and urc_backup_ops.sh. Owns NO version: --version and the bold header come from
# scripts/urc/xray_repo_ops.py (single source of truth). Resolves REPO (parent of scripts/),
# serves --help (central file first, full inline fallback second per CLI Script Help STD),
# sets PYTHONPATH, exec's the module. Rarely changes.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"   # .../scripts
REPO="$(dirname "$SCRIPT_DIR")"                              # repo root (Shell Conventions §2)
SCRIPT_NAME="urc_xray_repo"
HELP_FILE="$REPO/ais_command_help_ops.txt"                  # operator tier, repo root

_show_help() {
    if [[ -f "$HELP_FILE" ]] && grep -q "^## $SCRIPT_NAME$" "$HELP_FILE"; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$" | grep -v "^## "
    else
        # Inline fallback — MUST mirror the ## urc_xray_repo section in ais_command_help_ops.txt
        # (CLI Script Help STD: scripts must work with no central file — fresh clone / missing file).
        cat <<'HELP'
Usage: urc_xray_repo [--root DIR] [--out DIR] [--narrative] [--krr-md] [--silent] [--version]

Repo X-Ray. Classifies every asset across 3 dimensions: domain (ais/job/krr/urc),
type (pure-code/english-code/data/artifact), POS structure (core vs extension).
Reports engine/assets split, type x domain crosstab, and the code-to-.pos inversion.
Raw files -> ~/Downloads; rolling data log -> meta/krr/notes (NOTES - KRR - Repo Xray Data.yaml).

Options:
  --root DIR     Repo to scan (default ~/Developer/AIStudio)
  --out DIR      Raw-file output dir (default ~/Downloads)
  --narrative    Print the sentence-ready narrative block
  --krr-md       Also refresh the human-readable .md snapshot
  --silent       Suppress stdout report (files still written)
  --version      Print version and exit
HELP
    fi
}

# --help handled here (before Python loads). --version is delegated to Python (it owns VERSION).
if [[ "${1:-}" == "--help" ]]; then _show_help; exit 0; fi

exec env PYTHONPATH="$REPO" python3 -m scripts.urc.xray_repo_ops "$@"
