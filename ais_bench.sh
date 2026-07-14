#!/usr/bin/env zsh
# ais_bench.sh — Run AIStudio benchmark
# Version: 1.9.0
# Changelog: 1.9.0 — AIStudio_1019: export PYTHONUNBUFFERED=1 (right after the source guard) so a
#   `... | tee report.md` run streams live per-question progress without the caller prepending
#   PYTHONUNBUFFERED=1 every time. Passthrough behavior otherwise unchanged.
# Changelog: 1.8.1 — Command Dev STD §7: remove the wrapper's bold [ais_bench v… ] header.
#   bench.py now prints the single identity header (it was a double-header: wrapper v1.8.0
#   then bench.py v2.8.x). Fix stale comment path benchmarks/ → benchmarks/batch/.
# Changelog: 1.8.0 — recognize --batch (bench.py v2.8.x primary flag) for preflight-skip, alongside
#   --canonical (now the deprecated alias). Batch/canonical runs manage their own corpora from
#   benchmarks/batch/bench_canonical.yaml, so the single-corpus preflight does not apply to either.
# Changelog: 1.7.0 — AIStudio_931: +--canonical / --canonical-id passthrough to bench.py v2.7.0.
#   Under --canonical the single-corpus Preflight is skipped (canonical manages its own corpora
#   from benchmarks/bench_canonical.yaml); all other invocations unchanged.
# Changelog: 1.6.0 — version bump to match bench.py v2.2.0: --augment-from REPLACED by
#   --query-expansion N + --entity-filter {none,yaml,auto} (AIStudio_875). Passthrough via "$@".
# Changelog: 1.5.0 — version bump to match bench.py v2.1.0 capability: --augment-from
#   {scaffold,ui,auto,none} (AIStudio_867) passes through via "$@" (passthrough wrapper,
#   no logic change). Default ui = production A3 path (UI keywords + server auto-parse).
# Changelog: 1.4.1 — version bump to match bench.py v2.0.12 capabilities:
#   --scope, --questions stem resolution, --verbose, --super-verbose,
#   --min-score, --lang flags now active (all passed through via $@).


# ── Source guard: this script must be executed, not sourced ──────────────────
[[ "$ZSH_EVAL_CONTEXT" == *:file* ]] && { echo "❌ Do not source this script — execute it directly."; return 1; }

# AIStudio_1019: line-buffer Python so a tee'd long run shows live progress. Harmless if already set.
export PYTHONUNBUFFERED=1

VERSION="1.9.0"

SCRIPT_NAME="ais_bench"
REPO="${0:A:h}"
HELP_FILE="$REPO/ais_command_help.txt"

_show_help() {
    if [[ -f "$HELP_FILE" ]]; then
        awk "/^## $SCRIPT_NAME$/,/^---$/" "$HELP_FILE" | grep -v "^---$" | grep -v "^## "
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

# ANSI helpers
_dim()  { printf '\033[2m\033[3m%s\033[0m' "$1"; }
_sep()  { echo "$(_dim "--- $1")"; }

# Header is owned by the Python module (bench.py), not this wrapper — see
# Command Dev STD §7 (wrapper-backed command pattern). The wrapper prints only
# its phase separators (--- Preflight / --- Batch); bench.py prints the single
# bold [ais_bench v… ] identity header.

# ── Batch/canonical mode (AIStudio_931): manages its own corpora/params from ───
# benchmarks/batch/bench_canonical.yaml. Skip the single-corpus preflight and hand
# straight to bench.py, which orchestrates each run via the normal path.
for _arg in "$@"; do
    if [[ "$_arg" == "--canonical" || "$_arg" == "--batch" ]]; then
        _sep "Batch"
        echo "· Batch mode — corpora & params from benchmarks/batch/bench_canonical.yaml; per-run preflight skipped."
        cd "$REPO"
        source .venv/bin/activate
        python3 benchmarks/bench.py "$@"
        exit $?
    fi
done

# ── Parse --corpus from args ───────────────────────────────────────────────────
CORPUS="demo"
args=("$@")
for (( i=1; i<=${#args}; i++ )); do
    if [[ "${args[$i]}" == "--corpus" ]]; then
        CORPUS="${args[$((i+1))]}"
        break
    fi
done

# ── Preflight ─────────────────────────────────────────────────────────────────
_sep "Preflight"

# 1. Corpus must exist and have documents
CORPUS_DIR="$REPO/data/corpora/$CORPUS"
UPLOADS_DIR="$CORPUS_DIR/uploads"

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
