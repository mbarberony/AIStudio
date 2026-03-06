# Quickstart

Get a running AIStudio instance in under 15 minutes.

AIStudio runs entirely on your Mac — no cloud account, no API keys, no data 
leaving your machine. You'll have a local search engine over your own documents, 
accessible from your browser.

---

## Prerequisites

- macOS with Apple Silicon (M1/M2/M3) or Intel — Apple Silicon recommended
- Python 3.10+
- Git
- ~8GB free disk space (for models)

---

## 1. Install Ollama

Ollama runs the AI models locally on your machine.

Go to [ollama.com](https://ollama.com) and follow the instructions — you can 
either download the Mac app directly or run the install script in your terminal:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Note:** the installer will ask for your computer password — this is normal, 
it needs admin rights to complete the installation. Enter your Mac login 
password when prompted.

Verify Ollama is running:

```bash
ollama list
```

If you see a list (even empty), Ollama is up. If you get "connection refused", 
start it manually with `ollama serve`.

---

## 2. Pull Required Models

```bash
# Embedding model (required for vector retrieval)
ollama pull nomic-embed-text

# LLM — recommended for good answer quality
ollama pull llama3.1:8b
```

**Note on hardware:** `llama3.1:8b` runs well on current-generation MacBook 
Pro with Apple Silicon — performance is comparable to a mid-tier server from 
a couple of years ago. On older or CPU-only machines, use `llama3.2:3b` 
instead (faster, but noticeably lower answer quality).

Model download will take a few minutes depending on your connection.

---

## 3. Install AIStudio

AIStudio lives in your `~/Developer` folder — the standard Mac location for 
developer tools and personal projects.

```bash
# Create the Developer folder if it doesn't exist
mkdir -p ~/Developer

# Clone the repository
cd ~/Developer
git clone git@github.com:mbarberony/AIStudio.git
cd AIStudio

# Install Python dependencies
pip install -r requirements.txt
```

**Note:** if `git clone` gives a permissions error, you may need to add your 
SSH key to GitHub first. See 
[GitHub SSH setup](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

---

## 4. Create a Corpus and Ingest Documents

A **corpus** is a named collection of documents that AIStudio indexes and 
makes searchable. You can have multiple corpora — one per project, client, 
or topic.

```bash
# Create a corpus directory
mkdir -p data/corpora/my_corpus/uploads

# Copy your documents in (PDF, Word, PowerPoint, Excel, Markdown supported)
cp /path/to/your/documents/* data/corpora/my_corpus/uploads/

# Run ingestion — this embeds and indexes your documents
python -m local_llm_bot.app.ingest --corpus my_corpus --root data/corpora/my_corpus
```

Ingestion is a one-time step per corpus. Incremental updates are supported — 
re-run the command after adding new documents and only new files will be 
processed.

---

## 5. Start the Backend

```bash
python -m uvicorn src.local_llm_bot.app.api:app --reload --port 8000
```

Verify it's running:

```bash
curl http://localhost:8000/health
```

Expected response: `{"status": "ok"}`

---

## 6. Start the Frontend

Open a second terminal tab, navigate back to your AIStudio folder, and run:

```bash
cd ~/Developer/AIStudio/front_end
python server.py 3000
```

Then open your browser at:

```
http://localhost:3000/rag_studio.html
```

You should see the AIStudio interface with two main areas:
- **Corpus Manager** — manage your document collections and trigger indexing
- **Chat** — ask questions and get source-attributed answers

---

## 7. Ask a Question

Select your corpus from the dropdown and type a question in plain English.

Answers include inline citations (`[1]`, `[2]`) with a References section 
showing exactly which document and passage the answer came from.

**Tuning parameters** (available in the UI):
- **Temperature** — controls how literal vs. creative the answer is. Lower = 
  more precise, higher = more expansive
- **k** — number of passages retrieved from your corpus before generating 
  an answer. Higher k = more context, slower response
- **Relevance threshold** — minimum match quality required. If nothing in 
  your corpus meets the threshold, the system will say so rather than 
  hallucinate an answer

The system maintains a 10-turn conversation memory — follow-up questions 
work without re-stating context.

---

## 8. Verify Embedding Quality (Optional)

```bash
cd ~/Developer/AIStudio/tests
python test_embeddings.py
```

This runs three semantic arithmetic tests:
- King − Man + Woman ≈ Queen
- Paris − France + Italy ≈ Rome  
- Python − Django + JavaScript ≈ React

All three should pass with score > 0.75. If they don't, re-pull the 
embedding model: `ollama pull nomic-embed-text`.

---

## What's Running

| Component | Address | Purpose |
|---|---|---|
| FastAPI backend | `localhost:8000` | RAG retrieval, LLM inference, corpus management |
| Frontend server | `localhost:3000` | Browser UI |
| Ollama | `localhost:11434` | Embeddings + LLM inference (managed separately) |
| Chroma | (embedded) | Vector store, runs in-process with the backend |

All four need to be running for the full experience. Ollama starts 
automatically on most setups; the backend and frontend need to be started 
manually for now.

> **Coming soon:** one-click install and a menu bar launcher so you never 
> have to touch the terminal after setup.

---

## Troubleshooting

**"Error loading models"** — Ollama isn't running. Start it with `ollama serve`.

**Input field disabled / "No corpora"** — No corpus found. Complete Step 4.

**Citations show as plain text `[1]`** — You're serving the wrong HTML file. 
Confirm you're at `http://localhost:3000/rag_studio.html` and that the file 
is from `front_end/rag_studio.html` in this repo.

**Poor answer quality** — Check which LLM is active in the UI. `llama3.1:8b` 
significantly outperforms `llama3.2:3b` for synthesis and reasoning tasks.

**pip install fails** — Try `pip3 install -r requirements.txt`. If you have 
multiple Python versions, consider using a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

For architecture context and design decisions, see 
[docs/architecture_decisions.md](docs/architecture_decisions.md).
