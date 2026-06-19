#!/usr/bin/env zsh
# ais_setup_knowledge_esef.sh — Provision the knowledge bases for the esef_banks corpus
# Version: 1.0.0
# Changelog: 1.0.0 — AIStudio_876: hardwired KB-setup primitive for esef_banks. Orchestrates
#            ais_import_knowledge_base for the entity KB (GLEIF, 9_firms) + two term KBs
#            (bis_basel + esrs, corpus-wide). Presents as modular but is hardwired for this
#            corpus, parallel to ais_download_esef. OPS-tier for now; civilian when the
#            knowledge layer is released.

# ── Source guard ─────────────────────────────────────────────────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

SCRIPT_DIR="${0:A:h}"
HELP_FILE="$SCRIPT_DIR/ais_command_help_ops.txt"
SCRIPT_NAME="ais_setup_knowledge_esef"
VERSION="1.0.0"

_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$" | grep -v "^## "
    else
        echo "$SCRIPT_NAME — Provision knowledge bases for the esef_banks corpus"
        echo ""
        echo "Usage: $SCRIPT_NAME [--help] [--version]"
        echo ""
        echo "· Imports the GLEIF entity KB (9 firms) used for entity recognition,"
        echo "  query expansion, and source_path entity-filtering."
        echo "· Imports the BIS Basel + ESRS term KBs (corpus-wide) for term expansion."
        echo "· After running, esef_banks_corpus_metadata.yaml should declare these under"
        echo "  knowledge_sources (entity_synonyms: gleif; term_expansion: bis_basel, esrs)."
    fi
}

if [[ "$1" == "--help" ]]; then _show_help; exit 0; fi
if [[ "$1" == "--version" ]]; then echo "$SCRIPT_NAME v$VERSION"; exit 0; fi

REPO="${0:A:h}"
IMPORT="$REPO/scripts/ais_import_knowledge_base.py"

cd "$REPO"
source .venv/bin/activate

echo "▶ Setting up knowledge bases for esef_banks …"
echo ""
echo "── 1/3 · Entity KB (GLEIF, scope 9_firms) ───────────────────────────────"
env PYTHONPATH=src python3 "$IMPORT" --source gleif --corpus esef_banks --scope 9_firms || {
    echo "❌ GLEIF entity KB import failed"; exit 1; }
echo ""
echo "── 2/3 · Term KB (BIS Basel, corpus-wide) ───────────────────────────────"
env PYTHONPATH=src python3 "$IMPORT" --source bis_basel --corpus esef_banks --scope full || {
    echo "❌ BIS Basel term KB import failed"; exit 1; }
echo ""
echo "── 3/3 · Term KB (ESRS, corpus-wide) ────────────────────────────────────"
# ESRS handler is registered but may be planned-not-built (AIStudio_801 parallel track).
# Attempt it, but warn-and-continue rather than hard-fail so the entity + bis_basel KBs
# (the ones that drive filtering today) still complete the setup.
env PYTHONPATH=src python3 "$IMPORT" --source esrs --corpus esef_banks --scope full || {
    echo "⚠  ESRS term KB import skipped/failed (handler may be planned-not-built)."
    echo "   Entity + BIS Basel KBs are provisioned; ESRS can be added when its handler ships."; }
echo ""
echo "✅ esef_banks knowledge bases provisioned (entity + bis_basel; esrs if available)."
echo "   Ensure esef_banks_corpus_metadata.yaml declares under knowledge_sources:"
echo "     - type: entity_synonyms, source: gleif,     scope: 9_firms"
echo "     - type: term_expansion,  source: bis_basel,  scope: full"
echo "     - type: term_expansion,  source: esrs,       scope: full   # once esrs handler ships"
