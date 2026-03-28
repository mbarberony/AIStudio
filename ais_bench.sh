#!/usr/bin/env zsh
# ais_bench — Run AIStudio benchmark on demo corpus
# Usage: ais_bench [--corpus NAME] [--top-k N] [--temperature F] [--model NAME]
# Defaults: demo corpus, top-k 5, temperature 0.3

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
source .venv/bin/activate
python benchmarks/benchmark.py --corpus demo --top-k 5 --temperature 0.3 "$@"
