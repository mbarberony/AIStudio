#!/usr/bin/env zsh
# ais_sec_download — Download SEC 10-K corpus from EDGAR
# Downloads ~143 filings from 25 financial services firms (~500MB)
# Output goes to ~/Downloads/sec_10k_corpus/ by default
#
# Usage: ais_sec_download [--out DIR] [--firms N] [--years N]
# After download, ingest with:
#   AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python -m local_llm_bot.app.ingest \
#     --corpus sec_10k --root ~/Downloads/sec_10k_corpus --force

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
source .venv/bin/activate
python scripts/download_sec_corpus.py --out ~/Downloads/sec_10k_corpus "$@"
