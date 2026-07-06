#!/usr/bin/env zsh
# ais_download_esef.sh — Download ESEF iXBRL annual reports from filings.xbrl.org
# Version: 1.5.2
# v1.5.2 (2026-07-05): A17 — --help "next step" said "create corpus in the UI, then ingest via
#   Upload", which contradicted the actual TUTORIAL Module 3 flow (all Terminal) and the SEC twin.
#   ais_ingest_esef builds the corpus directly from uploads/, so the real next step is the
#   Terminal chain: ais_import_entity_kb → ais_import_glossary_kb → ais_ingest_esef.
# v1.1.0 (2026-06-10): Ported to the download_esef_corpus.py 1.5.0 architecture. Added a
#   dynamic backing-version banner (greps the .py `Version:` line, mirrors the SEC wrapper)
#   + a --version const + the source guard. Flag surface is now resolver-driven: the script
#   forwards everything to the .py (which owns --lei/--scope/--latest/--years/--no-inventory);
#   the wrapper only fixes --out to the corpus uploads dir and activates the venv.

# -- Source guard --------------------------------------------------------------
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "Do not source this script -- execute it directly."; return 1; }

SCRIPT_DIR="${0:A:h}"
HELP_FILE="$SCRIPT_DIR/ais_command_help.txt"
SCRIPT_NAME="ais_download_esef"
VERSION="1.5.2"

_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$" | grep -v "^## "
    else
        echo "$SCRIPT_NAME -- Download ESEF iXBRL annual reports from filings.xbrl.org"
        echo ""
        echo "Usage: $SCRIPT_NAME [--scope <stem>|--lei <LEI>] [--latest N|--years YYYY...] [options]"
        echo ""
        echo "Options:"
        echo "  --scope <stem>    A named subset (scopes/esef_banks_<stem>_scope.yaml) or a path."
        echo "                    Absence -> the corpus inventory (esef_banks_full_scope.yaml)."
        echo "  --lei <LEI>       Single firm by LEI."
        echo "  --latest [N]      The N most-recent filings per firm (bare = 1; default 1)."
        echo "  --years YYYY ...  Explicit fiscal year(s). Mutually exclusive with --latest."
        echo "  --no-inventory    Skip the *_full_scope write-back (throwaway/test runs)."
        echo "  --help            Show this help"
        echo "  --version         Show script version"
        echo ""
        echo "- Streams the primary XHTML report per firm (~50-200MB each) with a live progress bar."
        echo "- Source: filings.xbrl.org (XBRL International public ESEF repository)."
        echo "- Next step (in the Terminal): ais_import_entity_kb --corpus esef_banks --apply,"
        echo "  then ais_import_glossary_kb --source bis_basel, then ais_ingest_esef. See TUTORIAL Module 3."
    fi
}

if [[ "$1" == "--help" ]]; then _show_help; exit 0; fi
if [[ "$1" == "--version" ]]; then echo "$SCRIPT_NAME v$VERSION"; exit 0; fi

REPO="${0:A:h}"
UPLOADS="$REPO/data/corpora/esef_banks/uploads"
mkdir -p "$UPLOADS"

# Dynamic backing-version banner -- the .py is the source of truth for the download logic
# version; the wrapper version (above) tracks only this shell file. Mirrors the SEC wrapper.
BACKING_VERSION=$(grep -m1 -E '^Version:' "$REPO/scripts/download_esef_corpus.py" 2>/dev/null | awk '{print $2}')
[[ -z "$BACKING_VERSION" ]] && BACKING_VERSION="$VERSION"
printf "\033[1m[ais_download_esef v$BACKING_VERSION -- Download ESEF annual reports from filings.xbrl.org]\033[0m\n"

cd "$REPO"
source .venv/bin/activate

exec env PYTHONPATH=src python3 "$REPO/scripts/download_esef_corpus.py" --out "$UPLOADS" "$@"
