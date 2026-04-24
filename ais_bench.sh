#!/usr/bin/env zsh
# ais_bench.sh — Run AIStudio benchmark
# Version: 1.3.4


# ── Source guard: this script must be executed, not sourced ──────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

VERSION="1.3.4"

SCRIPT_NAME="ais_bench"
HELP_FILE="$SCRIPT_DIR/ais_command_help.txt"

_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$"
    else
        echo "$SCRIPT_NAME v$VERSION"
        echo ""
        echo "Usage: $SCRIPT_NAME [--help] [--version]"
        echo ""
        echo "Run from: ~/Developer/AIStudio"
    fi
}

if [[ "$1" == "--help" ]]; then _show_help; exit 0; fi
if [[ "$1" == "--version" ]]; then echo "$SCRIPT_NAME v$VERSION"; exit 0; fi

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ANSI helpers
_dim()  { printf '\033[2m\033[3m%s\033[0m' "$1"; }
_sep()  { echo "$(_dim "--- $1")"; }

printf '\033[1m[ais_bench v%s — Run AIStudio benchmark]\033[0m\n' "$VERSION"

if [[ ! -d "$UPLOADS_DIR" ]]; then
    echo "❌ Corpus '$CORPUS' has no uploads/ directory — not yet ingested."
    exit 1
fi

file_count=$(find "$UPLOADS_DIR" -maxdepth 1 -type f ! -name ".*" 2>/dev/null | wc -l | tr -d ' ')
if [[ "$file_count" -eq 0 ]]; then
    echo "❌ Corpus '$CORPUS' has no documents in uploads/."
    echo "· Ingest documents first via the UI or ais_ingest_* commands."
    exit 1
fi

# 2. Questions YAML must exist
QUESTIONS_FILE="$REPO/benchmarks/$CORPUS/${CORPUS}_questions.yaml"
if [[ ! -f "$QUESTIONS_FILE" ]]; then
    echo "❌ No questions file found for corpus '$CORPUS'."
    echo "· Expected: benchmarks/$CORPUS/${CORPUS}_questions.yaml"
    echo "· Available question files:"
    for f in "$REPO/benchmarks/"**/*_questions.yaml; do
        [[ -f "$f" ]] && echo "  · $(basename "$(dirname "$f")")"
    done
    exit 1
fi

echo "✅ Corpus '$CORPUS' ready — $file_count document(s), questions file found."

cd "$REPO"
source .venv/bin/activate
python3 benchmarks/bench.py "$@"
