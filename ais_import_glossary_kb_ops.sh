#!/usr/bin/env zsh
# ais_import_glossary_kb_ops.sh — Operator glossary-KB importer (term→expansion)
# Version: 1.0.0
# Builds a corpus-wide glossary knowledge source from a static curated seed
# (bis_basel now; nist_ai_rmf / esrs planned). The glossary binds at QUERY time
# (acronym → BM25 expansion), distinct from the entity KB (ingest-time identity).
# Splits the glossary half out of the deprecated ais_import_knowledge_base.
# Passthrough wrapper (§7): all flags/defaults live in scripts/ais_import_glossary_kb_ops.py.


# ── Source guard: this script must be executed, not sourced ──────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

VERSION="1.0.0"

SCRIPT_NAME="ais_import_glossary_kb_ops"
SCRIPT_DIR="${0:A:h}"
HELP_FILE="$SCRIPT_DIR/ais_command_help_ops.txt"

_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$" | grep -v "^## "
    else
        echo "$SCRIPT_NAME v$VERSION"
        echo ""
        echo "Usage: $SCRIPT_NAME --source <name> [--corpus C] [--list]"
        echo ""
        echo "Run from: ~/Developer/AIStudio"
    fi
}

if [[ "$1" == "--help" ]]; then _show_help; exit 0; fi
if [[ "$1" == "--version" ]]; then echo "$SCRIPT_NAME v$VERSION"; exit 0; fi

REPO="${0:A:h}"

printf "\033[1m[ais_import_glossary_kb_ops v$VERSION — Operator glossary-KB importer]\033[0m\n"

# cd to repo so the backing script's repo-relative output path
# (data/knowledge_sources/<source>/...) resolves against root.
cd "$REPO" || { echo "❌ Could not cd to repo root: $REPO"; exit 1; }
source .venv/bin/activate || { echo "❌ Could not activate .venv"; exit 1; }

echo "--- Preflight"
echo "✅ Repo: $REPO"
echo "· Static deterministic seed — writes in one pass (no review gate)"
echo ""

# §7 passthrough — all flags and defaults are owned by the backing argparse.
python3 scripts/ais_import_glossary_kb_ops.py "$@"
RC=$?

echo ""
echo "--- Next step"
echo "· Glossary binds at QUERY time — restart the backend (ais_stop && ais_start) to load it"

exit $RC
