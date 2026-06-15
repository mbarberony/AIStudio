*Version: Beta | Updated: 2026-06-15*

## What it does
Enables users to ingest documents as distinct corpora, ask questions, and get cited answers — entirely local, no data leaves your machine. Built for Apple Silicon, no cloud dependency.

For more information, see [README.md](README.md).

## Key Features
- **Local and private** — all inference runs on your machine via Ollama; no data sent to any external service
- **Multi-corpus** — create named corpora for different document sets; switch between them instantly
- **Hybrid two-stage retrieval** — vector + BM25 keyword search (tunable α), then CrossEncoder reranking for vocabulary-independent relevance
- **Page-accurate citations** — every answer references the exact source document and page number; click to open
- **Conversation memory** — follow-up questions carry context from the current session; history persists across page refresh
- **Corpus routing guidance** — per-corpus metadata steers retrieval toward the right documents for each question type
- **REST API** — all capabilities exposed via a clean HTTP API; consumable by scripts, notebooks, or agent frameworks
- **Benchmark harness** — YAML question files with pass/fail veracity testing and timestamped reports

## Demo Corpus
9 documents spanning enterprise architecture, IT strategy, and financial services technology — the author's original work from 2003 to 2026. Ask it anything about architecture methodology, technology strategy, or risk and compliance frameworks.

## Architecture and Components
- **Architecture:** See [Architecture decisions](docs/architecture_decisions.pdf)
- **Vector store:** Qdrant 1.17.0
- **Embeddings:** nomic-embed-text (768 dimensions)
- **Reranker:** CrossEncoder ms-marco-MiniLM-L-6-v2
- **LLM:** Ollama — runs any local model (llama3.1, mistral, gemma3, …); benchmarks are normalized on `gemma3:27b`. See [HOWTO.md](HOWTO.md) for details.

---
Manuel Barbero | [mbarberony@gmail.com](mailto:mbarberony@gmail.com) | [github.com/mbarberony/AIStudio](https://github.com/mbarberony/AIStudio)
