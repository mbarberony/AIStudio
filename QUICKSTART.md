# Quickstart

Get a running AIStudio instance in under 20 minutes.

AIStudio runs entirely on your Mac — no cloud account, no API keys, no data 
leaving your machine. You'll have a local search engine over your own documents, 
accessible from your browser.

---

## Before You Start — Open a Terminal

All commands in this guide are run in the Terminal app.

To open Terminal quickly: press **⌘ Space**, type **Terminal**, press Enter.

Keep Terminal open throughout the setup. When a step asks you to open a 
second terminal tab, press **⌘ T**.

Paste and run commands one at a time. Each command ends when you press Enter.

---

## Prerequisites

- macOS with Apple Silicon (M1/M2/M3/M4) — Intel also works but is slower
- Python **3.10 or later** — 3.13 recommended for new setups
- Git
- ~8GB free disk space (for models)

> **On Python versions:** Python 3.10+ is required. AIStudio uses type syntax 
> (`float | None`) that will fail silently on Python 3.9. The system Python 
> that ships with macOS is often 3.9 — check yours with `python3 --version` 
> before proceeding.

---

## 1. Install Homebrew (if not already installed)

Homebrew is the standard package manager for macOS. Skip this step if you 
already have it.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

The installer will ask for your Mac login password — this is normal. You won't 
see characters appear as you type; that's expected.

**After install, add Homebrew to your PATH.** The installer prints these three 
commands at the end — run them now (they start with `echo` and `eval`):

```bash
echo >> ~/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Verify Homebrew is working:

```bash
brew --version
```

---

## 2. Install Python 3.13

```bash
brew install python@3.13
```

Verify:

```bash
python3.13 --version
```

Expected output: `Python 3.13.x`

---

## 3. Install Ollama

Ollama runs the AI models locally on your machine.

```bash
brew install ollama
```

Start Ollama as a background service:

```bash
brew services start ollama
```

Verify it's running:

```bash
ollama list
```

If you see a list (even empty), Ollama is up. 

> **Note:** If you later run `ollama serve` manually and see "address already in 
> use", that's expected — it means Ollama is already running as a background 
> service. That's the correct state.

---

## 4. Pull Required Models

This downloads the AI models to your machine. Total download is roughly 
5–6 GB — allow 5 to 10 minutes depending on your connection.

Pull the embedding model (required):

```bash
ollama pull nomic-embed-text
```

Pull the language model. Choose based on your hardware:

**Standard (recommended for most users)** — requires ~8GB RAM:
```bash
ollama pull llama3.1:8b
```

**High-performance** — requires 128GB RAM, ~42GB download:
```bash
ollama pull llama3.1:70b
```

The 70b model delivers noticeably better answer quality and reasoning. On an 
M4 Max MacBook Pro with 128GB, warm query latency is 9–17 seconds.

---

## 5. Clone AIStudio

Create the Developer folder and move into it:

```bash
mkdir -p ~/Developer && cd ~/Developer
```

Clone the repository:

```bash
git clone git@github.com:mbarberony/AIStudio.git && cd AIStudio
```

> **SSH error?** You may need to add your SSH key to GitHub first. 
> See [GitHub SSH setup](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

---

## 6. Set Up a Python Virtual Environment

Create the virtual environment using Python 3.13:

```bash
python3.13 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Your prompt will change to show `(.venv)` — this confirms it's active. 
**Run this activation command every time you open a new terminal tab.**

Install dependencies:

```bash
pip install -r requirements.txt
pip install ollama python-multipart
```

> The second line installs two packages not yet in requirements.txt. This will 
> be consolidated in an upcoming release.

---

## 7. Ingest Documents

A **corpus** is a named collection of documents that AIStudio indexes and 
makes searchable. You have two options: start with the included demo corpus, 
or jump straight to your own documents.

---

### Option A — Use the Demo Corpus (recommended for first run)

AIStudio ships with a curated demo corpus: 17 documents spanning 20+ years 
of financial services technology architecture — strategy documents, 
methodology papers, AI reference architecture, and more. It gives you 
something substantive to query immediately, without needing your own 
documents first.

Make sure your virtual environment is active, then run:

```bash
PYTHONPATH=src python -m local_llm_bot.app.ingest \
  --corpus demo \
  --root data/demo
```

This indexes all documents in `data/demo/` into a corpus named `demo`. 
Select `demo` from the corpus dropdown in the UI and start querying.

Some questions to try:
- *"What is the Air Traffic Controller model and how does it apply to IT strategy?"*
- *"What does a reference architecture for enterprise AI look like?"*
- *"What are the key risk and compliance considerations for financial services IT?"*

See [data/demo/DEMO_CORPUS.md](data/demo/DEMO_CORPUS.md) for the full 
document inventory and a complete set of suggested demo questions.

---

### Option B — Use Your Own Documents

Copy your documents into a new corpus directory (PDF, Word, PowerPoint, 
Excel, and Markdown are all supported):

```bash
mkdir -p data/corpora/my_corpus/uploads
cp /path/to/your/documents/* data/corpora/my_corpus/uploads/
```

Run ingestion:

```bash
PYTHONPATH=src python -m local_llm_bot.app.ingest \
  --corpus my_corpus \
  --root data/corpora/my_corpus
```

Expected output: chunk count, document count, and zero failures. Re-run 
after adding new documents.

---

## 8. Start the Backend

With your virtual environment active:

```bash
PYTHONPATH=src python -m uvicorn src.local_llm_bot.app.api:app --reload --port 8000
```

Leave this terminal running. Open a new tab (⌘ T), activate the environment, 
and verify:

```bash
source ~/Developer/AIStudio/.venv/bin/activate
curl http://localhost:8000/health
```

Expected: `{"status": "ok"}`

---

## 9. Open the Frontend

Open the UI directly in your browser:

```bash
open ~/Developer/AIStudio/front_end/rag_studio.html
```

You should see the AIStudio interface. Select your corpus from the dropdown 
and ask a question in plain English.

Answers include inline citations (`[1]`, `[2]`) with a References section 
showing the source document and passage for each citation.

---

## 10. Verify Embedding Quality (Optional)

```bash
cd ~/Developer/AIStudio
PYTHONPATH=src python tests/test_embeddings.py
```

This runs three semantic reasoning checks (King − Man + Woman ≈ Queen, etc.). 
All three should pass with score > 0.75. If they don't, re-pull the model:

```bash
ollama pull nomic-embed-text
```

---

## What's Running

| Component | Address | Purpose |
|---|---|---|
| FastAPI backend | `localhost:8000` | RAG retrieval, LLM inference, corpus management |
| Frontend | (file:// or localhost) | Browser UI |
| Ollama | `localhost:11434` | Embeddings + LLM inference |
| Chroma | (embedded) | Vector store, runs in-process with backend |

Ollama runs as a background service and starts automatically on login. 
The backend requires a terminal tab each session.

> **Coming soon:** one-click install and a menu bar launcher so you never 
> have to touch the terminal after initial setup.

---

## Troubleshooting

**`python3.13` not found** — run `brew install python@3.13` and try again.

**`(.venv)` not showing in prompt** — virtual environment isn't active. Run 
`source ~/Developer/AIStudio/.venv/bin/activate`.

**`ModuleNotFoundError` on backend start** — make sure you're using 
`PYTHONPATH=src` in front of the uvicorn command.

**`ollama serve` — "address already in use"** — Ollama is already running 
as a background service. This is correct; proceed normally.

**Input field disabled / "No corpora"** — no corpus found. Complete Step 7.

**Poor answer quality** — confirm `llama3.1:8b` (or 70b) is set in config. 
`llama3.2:3b` is faster but significantly weaker on synthesis tasks.

**git clone permission error** — see 
[GitHub SSH setup](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

---

For architecture context and design decisions, see 
[docs/architecture_decisions.md](docs/architecture_decisions.md).
