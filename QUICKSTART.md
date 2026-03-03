# Quickstart

Get a running `/ask` endpoint in under 10 minutes.

---

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai) installed and running locally
- Git

---

## 1. Clone and Install

```bash
git clone git@github.com:mbarberony/AIStudio.git
cd AIStudio

pip install -r requirements.txt
```

---

## 2. Pull Required Models

```bash
# Embedding model (required for vector retrieval)
ollama pull nomic-embed-text

# LLM (recommended — better answer quality than 3b)
ollama pull llama3.1:8b
```

If you're on a CPU-only machine and memory is constrained, `llama3.2:3b` will work but answer quality will be noticeably lower.

---

## 3. Create a Corpus and Ingest Documents

```bash
# Create a corpus directory
mkdir -p data/corpora/my_corpus/uploads

# Copy your documents in (PDF, Word, PowerPoint, Excel, Markdown supported)
cp /path/to/your/documents/* data/corpora/my_corpus/uploads/

# Run ingestion
python -m local_llm_bot.app.ingest --corpus my_corpus --root data/corpora/my_corpus
```

Ingestion embeds and stores your documents in the Chroma vector store. This is a one-time step per corpus; incremental updates are supported.

---

## 4. Start the Backend

```bash
python -m uvicorn src.local_llm_bot.app.api:app --reload --port 8000
```

Verify it's running:

```bash
curl http://localhost:8000/health
```

Expected response: `{"status": "ok"}`

---

## 5. Start the Frontend

```bash
cd front_end
python server.py 3000
```

Open your browser at:

```
http://localhost:3000/rag_studio.html
```

---

## 6. Ask a Question

Select your corpus from the dropdown and ask a question. Answers include inline citations (`[1]`, `[2]`) with a References section showing source files. The system maintains a 10-turn conversation memory — follow-up questions work without re-stating context.

---

## 7. Verify Embedding Quality (Optional)

```bash
cd tests
python test_embeddings.py
```

This runs three semantic arithmetic tests (King − Man + Woman = Queen, Paris − France + Italy = Rome, Python − Django + JavaScript = React). All three should pass with score > 0.75. If they don't, your embedding model may need to be re-pulled or swapped.

---

## Troubleshooting

**"Error loading models"** — Ollama isn't running. Start it with `ollama serve`.

**Input field disabled / "No corpora"** — No corpus found in `data/corpora/`. Complete Step 3.

**Citations show as plain text `[1]`** — You're serving a different HTML file. Confirm `front_end/rag_studio.html` is the file from this repo.

**Poor answer quality** — Check which LLM is selected in the UI. `llama3.1:8b` significantly outperforms `llama3.2:3b` for synthesis tasks.

---

## What's Running

| Component | Address | Purpose |
|---|---|---|
| FastAPI backend | `localhost:8000` | RAG retrieval, LLM inference, corpus management |
| Frontend server | `localhost:3000` | Browser UI |
| Ollama | `localhost:11434` | Embeddings + LLM (managed separately) |
| Chroma | (embedded) | Vector store, runs in-process |

---

For architecture context and design decisions, see [docs/architecture_decisions.md](docs/architecture_decisions.md).
