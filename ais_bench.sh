#!/usr/bin/env zsh
# ais_bench.sh — Run AIStudio benchmark
# Version: 1.2.0

VERSION="1.2.0"
REPO="$(cd "$(dirname "$0")" && pwd)"

printf "\033[1m[ais_bench v$VERSION — Run AIStudio benchmark]\033[0m\n"

if [[ "$1" == "--version" ]]; then
    exit 0
fi

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
    echo "· Reports written to benchmarks/reports/"
    exit 0
fi

cd "$REPO"
source .venv/bin/activate
python3 benchmarks/bench.py "$@"
