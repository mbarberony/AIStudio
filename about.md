**Version:** Beta

## What it does
Enables users to ingest documents as distinct corpora, ask questions, and get cited answers — entirely local, no data leaves your machine. Built for Apple Silicon, no cloud dependency.

## Demo Corpus
15 documents on IT architecture, technology strategy, and financial services based on the author's twenty years of output as a thought leader. Ask it anything.

## Architecture and Components
- **Architecture:** See [Architecture decisions](https://github.com/mbarberony/AIStudio/blob/main/docs/architecture_decisions.md)
- **Vector store:** Qdrant 1.17.0
- **Embeddings:** nomic-embed-text (768 dimensions)
- **Reranker:** CrossEncoder ms-marco-MiniLM-L-6-v2
- **LLM:** Ollama — ships with llama3.1:8b; llama3.1:70b tested. See [Updating LLM options](https://github.com/mbarberony/AIStudio/blob/main/docs/architecture_decisions.md) for details.

---
Manuel Barbero | [mbarberony@gmail.com](mailto:mbarberony@gmail.com) | [github.com/mbarberony/AIStudio](https://github.com/mbarberony/AIStudio)
