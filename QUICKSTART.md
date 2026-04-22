# Quickstart

Get a running AIStudio instance in under 30 minutes.

AIStudio runs entirely on your Mac — no cloud account, no API keys, no data
leaving your machine. You'll have a local AI search engine over your own documents,
accessible from your browser.

---

## Before You Start

**Open Terminal first.** Press **⌘ Space**, type **Terminal**, press **Enter**.

You'll see a window with a prompt that looks something like this:
```
yourusername@Mac ~ %
```
All commands in this guide are typed after that prompt. The exact text varies by machine — don't worry about it.

Use `python3` — not `python` — on macOS. The system `python` command may point
to Python 2 or not exist.

> **What is a shell?** Terminal gives you access to the shell — a text interface for running commands on your Mac. AIStudio setup uses the shell for tasks the UI doesn't cover.

---

## Prerequisites

You need a Mac with Apple Silicon (M1/M2/M3/M4). Everything else — Python, Homebrew, Qdrant, Ollama — is installed in the steps below.

> Not sure if you have Apple Silicon? Click the **Apple menu** → **About This Mac**. Look for "Chip: Apple M1" (or M2/M3/M4). Intel Macs are not supported in this release.

---

## 1. Install Homebrew

Homebrew is a package manager for macOS — it installs the software AIStudio needs.

First, check if it's already installed:
```bash
brew --version
```

If you see a version number (e.g. `Homebrew 4.2.0`) — Homebrew is already installed. Skip to `brew install pango` below.

If you see `command not found`, install it:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

The installer will print three lines at the end — run them to add Homebrew to your PATH:
```bash
echo >> ~/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Verify:
```bash
brew --version
```

Then install the `pango` system library (required for PDF generation):
```bash
brew install pango
```

---

## 2. Install Python 3.13

Check if you already have Python 3.10 or later:
```bash
python3 --version
```

If you see `Python 3.10` or higher — you're good, skip to Step 3.

If you see `Python 3.9` or lower (or `command not found`), install Python 3.13:
```bash
brew install python@3.13
python3.13 --version
```

Expected: `Python 3.13.x`

> AIStudio uses type syntax (`float | None`) that fails on Python 3.9. The macOS system Python is often 3.9 — that's why we check.

---

## 3. Install Ollama

Ollama is a local model runtime — it downloads, manages, and serves AI language models on your machine. Think of it as a local equivalent of the OpenAI API, running entirely on your hardware.

Check if already installed:
```bash
ollama --version
```

If you see a version number — Ollama is installed. Check if it's running:
```bash
ollama list
```

If you see a list (even empty) — Ollama is running. Skip to Step 4.

If Ollama is not installed:
```bash
brew install ollama
```

Then start it:
```bash
brew services start ollama
```

> **Note:** `brew services start ollama` only works if Ollama was installed via Homebrew. If you previously installed Ollama from [ollama.com](https://ollama.com) directly (via .dmg), run `ollama serve` in a separate terminal tab instead.

Verify it's running:
```bash
ollama list
```

If you see a list (even empty) — Ollama is running correctly.

---

## 4. Pull Required Models

AIStudio needs two types of models: an **embedding model** (converts your documents into searchable vectors — think of it as building the index) and a **language model** (generates answers from that index).

Check what you already have:
```bash
ollama list
```

If you see `nomic-embed-text` and at least one of `llama3.1:8b` or `llama3.1:70b` — skip to Step 5.

Otherwise, pull what's missing:

```bash
# Embedding model (required — ~274 MB)
ollama pull nomic-embed-text

# Language model — choose based on your hardware:
ollama pull llama3.1:8b      # ~4.9 GB — 8GB RAM minimum, recommended default
ollama pull llama3.1:70b     # ~42 GB — 64GB RAM required, best answer quality
ollama pull mistral:7b       # ~4.4 GB — good alternative on constrained hardware
```

> **Download time:** At 100 Mbps, expect ~7 min for 8b, ~60 min for 70b.

> **First query vs. subsequent queries:** The first query after startup loads the model into memory (10–15 seconds) — this is the "cold start". After that, queries run in ~6–7 seconds. Don't worry if the first one seems slow.

> **On Apple Silicon:** Once loaded into unified memory, `llama3.1:70b` and `llama3.1:8b` have identical query latency (~6–7s). Model size stops being a latency variable. Choose based on your RAM, not speed.

---

## 5. Install Qdrant

Qdrant is the database that stores your document chunks. When AIStudio ingests a document, it splits it into overlapping passages (chunks) — typically a few paragraphs each — and stores them as vectors in Qdrant. When you query, AIStudio searches across all chunks to find the most relevant passages.

> **Why not Homebrew?** Qdrant is a Rust-based binary not available via Homebrew — install it directly:

Check if already installed:
```bash
qdrant --version
```

If you see a version number — skip to `mkdir -p ~/qdrant_storage` below.

If not installed:

First, create a home for Qdrant's data:
```bash
mkdir -p ~/qdrant_storage
```

Then install the binary:
```bash
curl -L https://github.com/qdrant/qdrant/releases/latest/download/qdrant-aarch64-apple-darwin.tar.gz | tar xz
mkdir -p ~/bin
mv qdrant ~/bin/qdrant
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
qdrant --version
```

Expected: `qdrant 1.17.0` (or newer). You will also see:
```
<jemalloc>: option background_thread currently supports pthread only
```
This warning is harmless — ignore it.

> **Why Qdrant over alternatives?** The previous vector store (ChromaDB) crashed at 32,285 chunks. Qdrant — written in Rust — is stable at 105,964 chunks with native metadata filtering and near-zero memory overhead.

---

## 6. Clone AIStudio

> **What is git?** Git is a version control system that also lets you download software from GitHub. If you received this guide from someone, this is how you get the actual AIStudio code. It's easier than it sounds.

First, create a folder for your development projects:
```bash
mkdir -p ~/Developer
```

> `mkdir -p` creates the folder if it doesn't exist — safe to run even if it's already there.

Clone the repo (this downloads ~115 MB — expect under 30 seconds on a fast connection):
```bash
cd ~/Developer
git clone git@github.com:mbarberony/AIStudio.git
cd AIStudio
```

> **SSH error?** See [GitHub SSH setup](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

> **Already have AIStudio installed?** If `~/Developer/AIStudio` already exists, git will refuse with `fatal: destination path already exists`. You're doing an upgrade, not a fresh install — see HOWTO.md for upgrade instructions.

> **This guide assumes you clone into `~/Developer/AIStudio`** — every command below uses this exact path. If you choose a different location, substitute your path throughout.

---

## 7. Install AIStudio Commands

`./ais_install` does three things:
1. Verifies your environment (checks Steps 1–5 are complete)
2. Creates the Python environment and installs all dependencies
3. Installs the `ais_*` commands into your shell

```bash
cd ~/Developer/AIStudio
./ais_install
```

You should see all green checkmarks. Then:
```bash
source ~/.zshrc
```

Verify all commands are active:
```bash
ais_install --verify
```

Expected: 8 green checkmarks ✅.

---

## 8. Activate the Virtual Environment

Each time you open a new terminal tab, activate the virtual environment before running AIStudio commands:

```bash
source ~/Developer/AIStudio/.venv/bin/activate
```

Your prompt will show `(.venv)` when active. `ais_start` handles this automatically — you only need to activate manually if running Python commands directly.

---

## 9. Start All Services

```bash
ais_start
```

AIStudio starts four processes — Qdrant, Ollama, the FastAPI backend, and the frontend — and opens the UI in your browser automatically. The demo corpus is indexed on first run (~45 seconds).

**To verify the backend is up:**
```bash
curl http://localhost:8000/health
```
Expected: `{"status": "ok"}`

---

## 10. What You're Looking At

The AIStudio interface has three main areas:

**Corpus selector** (top left) — choose which document collection to query. The **demo** corpus is already loaded — 9 original documents spanning 2003–2026, covering enterprise architecture, IT strategy, financial services, and agentic AI.

**Chat** — type a question, get a cited answer. References below each answer show exactly which document and page the answer came from. Click **Open ↗** to see the source.

**Settings sidebar** — controls how AIStudio retrieves and generates answers. See Step 12.

Try these questions on the demo corpus to start:
- *"What is QFD and how does it apply to technology architecture?"*
- *"How should a CTO prioritize a three-year technology strategy?"*
- *"What are the key principles for modernizing legacy applications?"*

Then try switching to the **help** corpus and asking: *"How do I re-ingest a corpus?"* — AIStudio answering questions about itself.

> For a full guided walkthrough — including the SEC 10-K at-scale exercise and benchmarking — see [TUTORIAL.md](TUTORIAL.md).

---

## 11. The Frontend

The UI lives at `~/Developer/AIStudio/front_end/rag_studio.html` — a single HTML file opened directly in your browser. No server required.

If it didn't open automatically:
```bash
open ~/Developer/AIStudio/front_end/rag_studio.html
```

---

## 12. Tuning Parameters

| Parameter | Default | Effect |
|-----------|---------|--------|
| Top K | 5 | Chunks retrieved per query. Higher = more context, slower. Try 10 for large corpora. |
| Temperature | 0.3 | LLM creativity. Lower = more factual. Keep at 0.3 for document Q&A. |
| Firm | (empty) | Filter by firm — only relevant for corpora with firm metadata (e.g. SEC 10-K). |
| Year | (empty) | Filter by year — only relevant for corpora with year metadata. |

> For more on query settings, see [HOWTO.md](HOWTO.md).

---

## What's Running

| Process | Address | Purpose |
|---------|---------|---------|
| FastAPI/uvicorn | `localhost:8000` | RAG pipeline, embeddings, corpus management |
| Qdrant | `localhost:6333` | Vector store (REST), `localhost:6334` (gRPC) |
| Ollama | `localhost:11434` | LLM inference + embeddings |
| Frontend | `file://` | Browser UI — no server required |

---

## Qdrant Startup Warnings

These three warnings appear on every Qdrant startup and are **harmless**:

```
<jemalloc>: option background_thread currently supports pthread only
Config file not found — using defaults
Static folder not found
```

Qdrant is running correctly. Ignore these messages.

---

## Troubleshooting

**`brew --version` returns `command not found`** — Homebrew not installed. Run the installer in Step 1.

**`python3.13` not found** — run `brew install python@3.13`

**`ollama list` hangs** — Ollama is not running. If brew-installed: `brew services start ollama`. If .dmg installed: `ollama serve` in a separate tab.

**UI shows "Error loading corpora" or "Ollama not running" on startup** — the browser opened before the backend finished starting. Hard-refresh (`Cmd+Shift+R`). If it persists, check for a Qdrant WAL error in the terminal (see below).

**Qdrant WAL lock — `Can't init WAL: Resource temporarily unavailable`** — a collection's write-ahead log was left locked from an unclean shutdown. Fix:
```bash
ais_stop
rm -rf ~/qdrant_storage/collections/aistudio_help   # replace with collection named in error
ais_start
```
Then re-ingest the affected corpus via the UI (Add button). ⚠️ Delete only the collection named in the error — not the entire `qdrant_storage/` folder.

To prevent this: always stop with `ais_stop`, never force-quit the terminal while running.

**`(.venv)` not in prompt** — run `source ~/Developer/AIStudio/.venv/bin/activate`

**`ModuleNotFoundError`** — ensure `PYTHONPATH=src` and `AISTUDIO_VECTORSTORE=qdrant` are set before the uvicorn command.

**`Failed to fetch` in UI** — the FastAPI backend is down. Run:
```bash
kill $(lsof -ti:8000)
cd ~/Developer/AIStudio && source .venv/bin/activate
OLLAMA_KEEP_ALIVE=30m AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
  uvicorn local_llm_bot.app.api:app --reload --port 8000
```

**`ollama serve` — "address already in use"** — Ollama already running. Correct state.

**Stats show 0 chunks** — corpus not yet ingested. Run `ais_start` and wait for indexing to complete.

**Qdrant not found** — `~/bin` not in PATH. Run `source ~/.zshrc` or add `export PATH="$HOME/bin:$PATH"` to `~/.zshrc`.

**Citations show wrong page numbers** — re-ingest with `--force`:
```bash
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \
  --corpus demo --root data/corpora/demo/uploads --force
```

---

## Optional — Disable Qdrant Telemetry

```bash
export QDRANT__TELEMETRY_DISABLED=true
```

Add to `~/.zshrc` to make permanent.

---

For architecture context, see [docs/architecture_decisions.md](docs/architecture_decisions.md).
For day-to-day usage, see [HOWTO.md](HOWTO.md).
For guided walkthroughs, see [TUTORIAL.md](TUTORIAL.md).
