#!/usr/bin/env zsh
# ais_import_entity_kb_ops.sh — Operator entity-KB importer (GLEIF, whole-corpus)
# Version: 1.3.0
# Builds the GLEIF entity knowledge source for a corpus: scans the corpus uploads
# for each filing's self-reported XBRL entity name, resolves it via GLEIF, and emits
# a YAML keyed by xbrl_name → {canonical, aliases, lei}. Review-gated by default
# (dry-run); pass --apply to write. Splits the entity half out of the deprecated
# ais_import_knowledge_base.
# Passthrough wrapper (§7): all flags/defaults live in scripts/ais_import_entity_kb_ops.py.


# ── Source guard: this script must be executed, not sourced ──────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

VERSION="1.3.0"

SCRIPT_NAME="ais_import_entity_kb_ops"
SCRIPT_DIR="${0:A:h}"
HELP_FILE="$SCRIPT_DIR/ais_command_help_ops.txt"

_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$" | grep -v "^## "
    else
        echo "$SCRIPT_NAME v$VERSION"
        echo ""
        echo "Usage: $SCRIPT_NAME --corpus <name> [--rescan] [--apply]"
        echo ""
        echo "Run from: ~/Developer/AIStudio"
    fi
}

if [[ "$1" == "--help" ]]; then _show_help; exit 0; fi
if [[ "$1" == "--version" ]]; then echo "$SCRIPT_NAME v$VERSION"; exit 0; fi

REPO="${0:A:h}"

printf "\033[1m[ais_import_entity_kb_ops v$VERSION — Operator entity-KB importer]\033[0m\n"

# cd to repo so the backing script's repo-relative paths
# (data/corpora/<corpus>/uploads, data/knowledge_sources) resolve against root.
cd "$REPO" || { echo "❌ Could not cd to repo root: $REPO"; exit 1; }
source .venv/bin/activate || { echo "❌ Could not activate .venv"; exit 1; }

echo "--- Preflight"
echo "✅ Repo: $REPO"
echo "· Worksheet round-trip: 1st run writes the worksheet; --apply writes the KB"
echo ""

# §7 passthrough — all flags and defaults are owned by the backing argparse.
python3 scripts/ais_import_entity_kb_ops.py "$@"
RC=$?

echo ""
echo "--- Next step"
echo "· Edit lei_corrected in the worksheet (and xbrl_name for name-less groups)"
echo "· Re-run to refresh; --apply writes the KB; then re-ingest to label chunks"

exit $RC
