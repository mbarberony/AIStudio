# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## What this project is

AIStudio is a local RAG (Retrieval-Augmented Generation) system for Apple Silicon. Users upload documents to named corpora, ask natural-language questions, and get cited answers. No cloud dependency — all inference runs locally via Ollama.

**Architecture:** Browser (`front_end/rag_studio.html`) → FastAPI (:8000) → Qdrant (:6333) + Ollama (:11434)

## Setup and Start

```bash
./ais_install          # first-time install — creates venv, installs deps, installs aliases
source ~/.zshrc        # activate aliases
bash check_env.sh      # verify environment (Python 3.10+, Homebrew, Qdrant, Ollama)
ais_start              # start all services and open UI
ais_stop               # stop all services
```

## Development Commands

```bash
# Activate venv
source .venv/bin/activate

# Run backend manually
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
  uvicorn local_llm_bot.app.api:app --reload --port 8000

# Ingest a corpus
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
  python -m local_llm_bot.app.ingest \
  --corpus demo --root data/corpora/demo/uploads

# Run benchmarks
ais_bench --corpus demo
ais_bench --corpus demo --top-k 5 --temperature 0.3 --model llama3.1:70b
```

## Tests and Lint

```bash
# Run tests
.venv/bin/python -m pytest tests/ -v
.venv/bin/python -m pytest tests/ -v -m unit        # fast, no services needed
.venv/bin/python -m pytest tests/ -v -m integration # requires running backend + Ollama

# Lint and format
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format .
```

## Key Source Files

- `src/local_llm_bot/app/api.py` — FastAPI app, all endpoints (`/ask`, `/corpus/*`, `/health`)
- `src/local_llm_bot/app/rag_core.py` — RAG pipeline: retrieve → rerank → generate → citations
- `src/local_llm_bot/app/config.py` — env var loading, RagConfig, IngestConfig
- `src/local_llm_bot/app/ingest/` — load → chunk → embed → upsert pipeline
- `front_end/rag_studio.html` — entire frontend, single file, no build step

## Corpus Data

Each corpus lives in `data/corpora/{name}/` with:
- `uploads/` — source documents
- `index.jsonl` — chunk metadata
- `manifest.jsonl` — ingest tracking
- `{name}_corpus_meta.yaml` — search routing guidance loaded into system prompt at query time

Deleted files move to `uploads/trash/` — recoverable.

## Key Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `AISTUDIO_VECTORSTORE` | `qdrant` | vectorstore backend |
| `AISTUDIO_DEFAULT_MODEL` | `llama3.1:8b` | LLM model |
| `AISTUDIO_DEFAULT_EMBED_MODEL` | `nomic-embed-text` | embedding model |
| `AISTUDIO_TOP_K` | `5` | retrieval top-k |
