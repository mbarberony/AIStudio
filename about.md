**Version:** Beta

## What it does
Enables users to ingest documents as distinct corpora, ask questions, and get cited answers — entirely local, no data leaves your machine. Built for Apple Silicon, no cloud dependency.

For more information, see [README.pdf](README.pdf).

## Key Features
- **Local and private** — all inference runs on your machine via Ollama; no data sent to any external service
- **Multi-corpus** — create named corpora for different document sets; switch between them instantly
- **Two-stage retrieval** — vector search followed by CrossEncoder reranking for vocabulary-independent relevance
- **Page-accurate citations** — every answer references the exact source document and page number; click to open
- **Conversation memory** — follow-up questions carry context from the current session; history persists across page refresh
- **Corpus routing guidance** — per-corpus metadata steers retrieval toward the right documents for each question type
- **REST API** — all capabilities exposed via a clean HTTP API; consumable by scripts, notebooks, or agent frameworks
- **Benchmark harness** — YAML question files with pass/fail veracity testing and timestamped reports

## Demo Corpus
9 documents spanning enterprise architecture, IT strategy, and financial services technology — the author's original work from 2003 to 2021. Ask it anything about architecture methodology, technology strategy, or risk and compliance frameworks.

## Architecture and Components
- **Architecture:** See [Architecture decisions](docs/architecture_decisions.pdf)
- **Vector store:** Qdrant 1.17.0
- **Embeddings:** nomic-embed-text (768 dimensions)
- **Reranker:** CrossEncoder ms-marco-MiniLM-L-6-v2
- **LLM:** Ollama — ships with llama3.1:8b; llama3.1:70b tested. See [Updating LLM options](HOWTO.pdf) for details.

---
Manuel Barbero | [mbarberony@gmail.com](mailto:mbarberony@gmail.com) | [github.com/mbarberony/AIStudio](https://github.com/mbarberony/AIStudio)
