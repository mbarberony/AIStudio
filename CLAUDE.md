# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AIStudio is a local-first RAG (Retrieval-Augmented Generation) system. Users upload documents to named corpora, ask natural-language questions, and get answers with inline citations. Runs entirely locally — no external LLM APIs.

**Four-process architecture:** Browser (rag_studio.html) → FastAPI (:8000) → Qdrant (:6333) + Ollama (:11434)

## Common Commands

```bash
# Setup
make venv && source .venv/bin/activate && make install

# Development
make run                    # uvicorn on port 8000
make check                  # lint + unit tests (mirrors CI)
make lint                   # ruff check
make format                 # ruff check --fix

# Tests
make test                   # all pytest tests
make test-unit              # fast, no external services needed
make test-integration       # requires running backend + Ollama
make coverage               # unit tests with coverage report

# Run a single test
.venv/bin/python -m pytest tests/test_health.py -v
.venv/bin/python -m pytest tests/test_corpus_paths.py::TestCorpusPaths::test_some_method -v -m unit

# Ingestion
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python -m local_llm_bot.app.ingest \
  --corpus demo --root data/corpora/demo/uploads

# Benchmarks
python benchmarks/benchmark.py --corpus demo --top-k 5 --temperature 0.3
```

## Architecture

Source lives in `src/local_llm_bot/app/` with `PYTHONPATH=src`:

- **api.py** — FastAPI app, all endpoints (`/ask`, `/corpus/*`, `/health`), citation extraction logic
- **rag_core.py** — RAG pipeline: `retrieve()`, `RetrievedDoc`, `Citation`, CrossEncoder reranker, JSONL fallback
- **config.py** — `AppConfig`, `RagConfig`, `IngestConfig`, env var loading
- **ollama_client.py** — `ollama_generate()`, `ollama_embed()`
- **ingest/** — Pipeline: discover → load → chunk → embed → upsert (pipeline.py, loaders.py, chunking.py, index_jsonl.py, manifest.py)
- **vectorstore/** — `qdrant_store.py` (primary), `chroma_store.py` (legacy fallback). Selected via `AISTUDIO_VECTORSTORE` env var
- **utils/** — corpus_paths.py, repo_root.py

Frontend is a single vanilla JS file: `front_end/rag_studio.html`

## Key Design Decisions

- **No LangChain** — RAG pipeline implemented directly for substrate knowledge
- **Qdrant over ChromaDB** — ChromaDB crashed at 32K chunks; Qdrant stable at 105K+
- **nomic-embed-text** (768 dims, cosine) — best CPU perf on Apple Silicon
- **Citation logic lives in api.py**, not a separate module
- **Process separation** maps directly to containers for cloud deployment

## Testing

- pytest markers: `@pytest.mark.unit` (fast, offline) and `@pytest.mark.integration` (needs backend)
- `test_aistudio.py` is excluded from default pytest run (`addopts = "--ignore=tests/test_aistudio.py"` in pyproject.toml) — it has its own runner
- Unit tests must not require Ollama, Qdrant, or any network access

## Linting

- **ruff** with line-length 100, target py313
- Rules: E, F, I, B, UP, SIM (ignores E501)
- Pre-commit hooks run ruff check + ruff format

## Key Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `AISTUDIO_VECTORSTORE` | `qdrant` | `qdrant` or `chroma` |
| `AISTUDIO_DEFAULT_MODEL` | `llama3.1:8b` | LLM model |
| `AISTUDIO_DEFAULT_EMBED_MODEL` | `nomic-embed-text` | Embedding model |
| `AISTUDIO_TOP_K` | `5` | Retrieval top-k |
| `QDRANT_HOST` / `QDRANT_PORT` | `localhost` / `6333` | Qdrant connection |
| `AISTUDIO_OLLAMA_BASE_URL` | `http://127.0.0.1:11434` | Ollama API |

## Corpus Data Model

Corpora live in `data/corpora/{name}/` with `manifest.jsonl` (file metadata + ingest status), `index.jsonl` (lexical fallback), and `uploads/` directory. Each corpus maps to a Qdrant collection named `aistudio_{name}`. Deleted files move to `uploads/trash/` — recoverable manually.

## Benchmark Harness

Questions live in `benchmarks/demo_questions.yaml` (auto-detected for `--corpus demo`). Reports are written to `benchmarks/reports/` as timestamped `.md` and `.json` pairs. See `docs/HARNESS.md` for full usage.
