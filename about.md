# AIStudio

Local RAG system — Apple Silicon, no cloud dependency.

**Version:** Beta | **Built by:** Manuel Barbero
**Repo:** [github.com/mbarberony/AIStudio](https://github.com/mbarberony/AIStudio)

## Architecture
- **Vector store:** Qdrant 1.17.0
- **Embeddings:** nomic-embed-text (768 dimensions)
- **Reranker:** CrossEncoder ms-marco-MiniLM-L-6-v2
- **LLM:** Ollama — llama3.1:8b default, 70b optional

## What it does
Ingest documents, ask questions, get cited answers — entirely local, no data leaves your machine.

## Demo corpus
15 documents on IT architecture, technology strategy, and financial services. Ask it anything.
