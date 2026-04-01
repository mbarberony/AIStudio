#!/usr/bin/env zsh
# ais_bench — Run AIStudio benchmark on demo corpus
# Usage: ais_bench [--corpus NAME] [--top-k N] [--temperature F] [--model NAME]
# Defaults: demo corpus, top-k 5, temperature 0.3
# Version: 1.1.0

VERSION="1.1.0"
REPO="$(cd "$(dirname "$0")" && pwd)"

if [[ "$1" == "--version" ]]; then echo "ais_bench v$VERSION"; exit 0; fi
if [[ "$1" == "--help" ]]; then
    echo "ais_bench v$VERSION"
    echo ""
    echo "Usage: ais_bench [--corpus NAME] [--top-k N] [--temperature F] [--model NAME]"
    echo ""
    echo "Runs the benchmark harness against a corpus using a YAML question file."
    echo "Question file is auto-detected: benchmarks/<corpus>_questions.yaml"
    echo ""
    echo "Defaults: --corpus demo --top-k 5 --temperature 0.3"
    echo ""
    echo "Examples:"
    echo "  ais_bench                          # demo corpus, defaults"
    echo "  ais_bench --corpus sec_10k         # SEC corpus"
    echo "  ais_bench --top-k 10               # demo corpus, top-k 10"
    exit 0
fi

cd "$REPO"
source .venv/bin/activate
python3 benchmarks/benchmark.py --corpus demo --top-k 5 --temperature 0.3 "$@"
