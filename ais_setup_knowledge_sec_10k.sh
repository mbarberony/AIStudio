#!/usr/bin/env zsh
# ais_setup_knowledge_sec_10k.sh — Provision the knowledge bases for the sec_10k corpus
# Version: 1.0.0
# Changelog: 1.0.0 — AIStudio_876: hardwired KB-setup primitive for sec_10k. Orchestrates
#            ais_import_knowledge_base for the entity KB (GLEIF, 25_firms) + the term KB
#            (bis_basel, corpus-wide). Presents as modular but is hardwired for this corpus,
#            parallel to ais_ingest_sec_10k. OPS-tier for now; civilian when the knowledge
#            layer is released.

# ── Source guard ─────────────────────────────────────────────────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

SCRIPT_DIR="${0:A:h}"
HELP_FILE="$SCRIPT_DIR/ais_command_help_ops.txt"
SCRIPT_NAME="ais_setup_knowledge_sec_10k"
VERSION="1.0.0"

_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$" | grep -v "^## "
    else
        echo "$SCRIPT_NAME — Provision knowledge bases for the sec_10k corpus"
        echo ""
        echo "Usage: $SCRIPT_NAME [--help] [--version]"
        echo ""
        echo "· Imports the GLEIF entity KB (25 firms) used for entity recognition,"
        echo "  query expansion, and source_path entity-filtering."
        echo "· Imports the BIS Basel term KB (corpus-wide) for term expansion."
        echo "· After running, sec_10k_corpus_metadata.yaml should declare these under"
        echo "  knowledge_sources (entity_synonyms: gleif; term_expansion: bis_basel)."
    fi
}

if [[ "$1" == "--help" ]]; then _show_help; exit 0; fi
if [[ "$1" == "--version" ]]; then echo "$SCRIPT_NAME v$VERSION"; exit 0; fi

REPO="${0:A:h}"
IMPORT="$REPO/scripts/ais_import_knowledge_base.py"

cd "$REPO"
source .venv/bin/activate

echo "▶ Setting up knowledge bases for sec_10k …"
echo ""
echo "── 1/2 · Entity KB (GLEIF, scope 25_firms) ──────────────────────────────"
env PYTHONPATH=src python3 "$IMPORT" --source gleif --corpus sec_10k --scope 25_firms || {
    echo "❌ GLEIF entity KB import failed"; exit 1; }
echo ""
echo "── 2/2 · Term KB (BIS Basel, corpus-wide) ───────────────────────────────"
env PYTHONPATH=src python3 "$IMPORT" --source bis_basel --corpus sec_10k --scope full || {
    echo "❌ BIS Basel term KB import failed"; exit 1; }
echo ""
echo "✅ sec_10k knowledge bases provisioned."
echo "   Ensure sec_10k_corpus_metadata.yaml declares both under knowledge_sources:"
echo "     - type: entity_synonyms, source: gleif,    scope: 25_firms"
echo "     - type: term_expansion,  source: bis_basel, scope: full"
