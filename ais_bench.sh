#!/usr/bin/env zsh
# ais_bench.sh — Run AIStudio benchmark
# Version: 1.3.0

VERSION="1.3.2"
REPO="$(cd "$(dirname "$0")" && pwd)"

# ANSI helpers
_dim()  { printf '\033[2m\033[3m%s\033[0m' "$1"; }
_sep()  { echo "$(_dim "--- $1")"; }

printf '\033[1m[ais_bench v%s — Run AIStudio benchmark]\033[0m\n' "$VERSION"

if [[ "$1" == "--version" ]]; then exit 0; fi

if [[ "$1" == "--help" ]]; then
    echo ""
    echo "Usage: ais_bench [--corpus NAME] [--top-k N] [--temperature F] [--model NAME]"
    echo ""
    echo "Runs the benchmark harness against a corpus using a YAML question file."
    echo "Question file is auto-detected: benchmarks/<corpus>_questions.yaml"
    echo ""
    echo "Defaults: --corpus demo  --top-k 5  --temperature 0.3"
    echo ""
    echo "Examples:"
    echo "  ais_bench                                            # demo corpus, defaults"
    echo "  ais_bench --corpus sec_10k                          # SEC corpus"
    echo "  ais_bench --top-k 10                                # demo corpus, top-k 10"
    echo "  ais_bench --corpus demo --model llama3.1:70b        # 70b model"
    echo ""
    echo "· Reports written to benchmarks/<corpus>/reports/"
    exit 0
fi

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

if [[ ! -d "$CORPUS_DIR" ]]; then
    echo "❌ Corpus '$CORPUS' does not exist."
    echo "· Available corpora:"
    for d in "$REPO/data/corpora"/*/; do
        [[ -d "$d" ]] && echo "  · $(basename "$d")"
    done
    exit 1
fi

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
