# Quickstart

Get a running AIStudio instance in under 15 minutes.

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

- macOS with Apple Silicon (M1/M2/M3) or Intel — Apple Silicon recommended
- Python 3.9 or later (3.11+ recommended for best compatibility)
- Git
- ~8GB free disk space (for models)

**On Python versions:** AIStudio is tested on Python 3.9 and above. The 
system Python that ships with macOS is typically 3.9 — this works fine for 
getting started. If you manage your own Python installation (e.g. via 
Homebrew or pyenv), Python 3.11 or 3.13 will also work and is recommended 
for new setups.

---

## 1. Install Ollama

Ollama runs the AI models locally on your machine.

Go to [ollama.com](https://ollama.com) and follow the instructions — you can 
either download the Mac app directly or run this in Terminal:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

The installer will ask for your computer password — this is normal, it needs 
admin rights to complete. Enter your Mac login password when prompted. You 
won't see characters appear as you type — that's expected.

Verify Ollama is running:

```bash
ollama list
```

If you see a list (even empty), Ollama is up. If you get "connection refused", 
start it manually:

```bash
ollama serve
```

---

## 2. Pull Required Models

This downloads the AI models to your machine. Total download is roughly 
5–6 GB — allow 5 to 10 minutes depending on your connection.

Pull the embedding model:

```bash
ollama pull nomic-embed-text
```

Pull the language model:

```bash
ollama pull llama3.1:8b
```

**Note on hardware:** `llama3.1:8b` runs well on current-generation MacBook 
Pro with Apple Silicon — performance is comparable to a mid-tier server from 
a couple of years ago. On older or CPU-only machines, use `llama3.2:3b` 
instead (faster to download and run, but noticeably lower answer quality):

```bash
ollama pull llama3.2:3b
```

---

## 3. Install AIStudio

Create the Developer folder and move into it:

```bash
mkdir -p ~/Developer && cd ~/Developer
```

Clone the repository and move into it:

```bash
git clone git@github.com:mbarberony/AIStudio.git && cd AIStudio
```

**Note:** if `git clone` gives a permissions error, you may need to add your 
SSH key to GitHub first. See 
[GitHub SSH setup](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

---

## 4. Set Up a Python Virtual Environment

A virtual environment keeps AIStudio's dependencies isolated from the rest 
of your system — this is the recommended approach and avoids a common class 
of PATH and version conflicts.

Create the virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Your terminal prompt will change to show `(.venv)` — this confirms the 
environment is active. **You'll need to run this activation command every 
time you open a new terminal tab and want to work with AIStudio.**

Install dependencies:

```bash
pip install -r requirements.txt
```

Using a virtual environment means `pip` (not `pip3`) works correctly inside 
it, and all installed tools like `uvicorn` and `pytest` are immediately 
available without any PATH changes.

**About the warnings during install:** you may see messages like 
"pip version X is available" or notes about script locations — these are 
harmless and can be safely ignored. The install is successful if the last 
line reads `Successfully installed ...`.

---

## 5. Create a Corpus and Ingest Documents

A **corpus** is a named collection of documents that AIStudio indexes and 
makes searchable. You can have multiple corpora — one per project, client, 
or topic.

Make sure your virtual environment is active (you should see `(.venv)` in 
your prompt). If not:

```bash
source ~/Developer/AIStudio/.venv/bin/activate
```

Create a corpus directory:

```bash
mkdir -p data/corpora/my_corpus/uploads
```

Copy your documents into it. Replace the path below with the actual location 
of your files (PDF, Word, PowerPoint, Excel, and Markdown are all supported):

```bash
cp /path/to/your/documents/* data/corpora/my_corpus/uploads/
```

Run ingestion — this reads, chunks, embeds, and indexes your documents:

```bash
python -m local_llm_bot.app.ingest --corpus my_corpus --root data/corpora/my_corpus
```

Ingestion is a one-time step per corpus. Re-run after adding new documents — 
only new files will be processed.

---

## 6. Start the Backend

Make sure your virtual environment is active, then:

```bash
python -m uvicorn src.local_llm_bot.app.api:app --reload --port 8000
```

Leave this terminal running. Open a new terminal tab (⌘ T), activate the 
virtual environment, and verify the backend is up:

```bash
source ~/Developer/AIStudio/.venv/bin/activate
curl http://localhost:8000/health
```

Expected response: `{"status": "ok"}`

---

## 7. Start the Frontend

In the same new terminal tab, navigate to the frontend folder:

```bash
cd ~/Developer/AIStudio/front_end
```

Start the frontend server:

```bash
python server.py 3000
```

Leave this running. Open your browser at:

```
http://localhost:3000/rag_studio.html
```

You should see the AIStudio interface with two main areas:
- **Corpus Manager** — manage your document collections and trigger indexing
- **Chat** — ask questions and get source-attributed answers

---

## 8. Ask a Question

Select your corpus from the dropdown and type a question in plain English.

Answers include inline citations (`[1]`, `[2]`) with a References section 
showing exactly which document and passage the answer came from.

**Tuning parameters** (available in the UI):

> *Note: check the UI for exact label names — the descriptions below reflect 
> how these controls work conceptually.*

- **Temperature** — how literal vs. creative the answer is; lower is more 
  precise, higher is more expansive
- **k** — number of passages retrieved before generating an answer; higher 
  means more context, slightly slower response
- **Relevance threshold** — minimum match quality required; if nothing in 
  your corpus meets the bar, the system says so rather than guess

The system maintains a 10-turn conversation memory — follow-up questions 
work without re-stating context.

---

## 9. Verify Embedding Quality (Optional)

Navigate to the tests folder:

```bash
cd ~/Developer/AIStudio/tests
```

Run the embedding tests:

```bash
python test_embeddings.py
```

This runs three semantic reasoning checks:
- King − Man + Woman ≈ Queen
- Paris − France + Italy ≈ Rome
- Python − Django + JavaScript ≈ React

All three should pass with score > 0.75. If they don't, re-pull the 
embedding model:

```bash
ollama pull nomic-embed-text
```

---

## What's Running

| Component | Address | Purpose |
|---|---|---|
| FastAPI backend | `localhost:8000` | RAG retrieval, LLM inference, corpus management |
| Frontend server | `localhost:3000` | Browser UI |
| Ollama | `localhost:11434` | Embeddings + LLM inference (managed separately) |
| Chroma | (embedded) | Vector store, runs in-process with the backend |

All four need to be running for the full experience. Ollama starts 
automatically on most setups; the backend and frontend each require 
a terminal tab for now.

> **Coming soon:** one-click install and a menu bar launcher so you never 
> have to touch the terminal after initial setup.

---

## Troubleshooting

**`(.venv)` not showing in prompt** — virtual environment isn't active. Run 
`source ~/Developer/AIStudio/.venv/bin/activate` before any other command.

**Ollama isn't running** — start it with `ollama serve` in a terminal tab.

**Input field disabled / "No corpora"** — no corpus found. Complete Step 5.

**Citations show as plain text `[1]`** — confirm you're at 
`http://localhost:3000/rag_studio.html` using the file from `front_end/` 
in this repo.

**Poor answer quality** — confirm `llama3.1:8b` is selected in the UI; 
it significantly outperforms `llama3.2:3b` for synthesis and reasoning.

**git clone permission error** — you may need to add your SSH key to GitHub. 
See [GitHub SSH setup](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

---

For architecture context and design decisions, see 
[docs/architecture_decisions.md](docs/architecture_decisions.md).
