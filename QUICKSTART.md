# Quickstart

Get a running AIStudio instance in under 30 minutes.

AIStudio runs entirely on your Mac — no cloud account, no API keys, no data
leaving your machine. You'll have a local search engine over your own documents,
accessible from your browser.

---

## Before You Start

All commands run in Terminal. Press **⌘ Space**, type **Terminal**, press Enter.

Use `python3` — not `python` — on macOS. The system `python` command may point
to Python 2 or not exist. Always activate your virtual environment before
running any AIStudio command.

---

## Prerequisites

- macOS with Apple Silicon (M1/M2/M3/M4) — Intel works but is slower
- Python **3.10 or later** — 3.13 recommended
- Git
- ~8GB free disk space (for models)
- `pango` system library (required for PDF generation) — installed via Homebrew in Step 1

Check your Python version:
```bash
python3 --version
```

> Python 3.10+ required. AIStudio uses type syntax (`float | None`) that
> fails on Python 3.9. The system Python on macOS is often 3.9 — install
> a newer version if needed.

---

## 1. Install Homebrew

Skip if already installed.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Add to PATH (run the three lines the installer prints at the end):
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

```bash
brew install python@3.13
python3.13 --version
```

Expected: `Python 3.13.x`

---

## 3. Install Ollama

```bash
brew install ollama
brew services start ollama
ollama list
```

If you see a list (even empty), Ollama is running.

> If you later run `ollama serve` and see "address already in use" — that's
> correct. Ollama is already running as a background service.

---

## 4. Pull Required Models

~5–6 GB download total. Allow 5–10 minutes.

```bash
# Embedding model (required)
ollama pull nomic-embed-text

# Language model — choose based on your hardware:
ollama pull llama3.1:8b      # ~8GB RAM required, recommended default
ollama pull llama3.1:70b     # ~128GB RAM required, best quality
```

> On Apple Silicon, warm `llama3.1:70b` and warm `llama3.1:8b` have identical
> query latency (~6–7s). Once loaded into unified memory, model size stops
> being a latency variable. See [benchmarks/](benchmarks/) for full analysis.

---

## 5. Install Qdrant

Qdrant is the vector store. **It is not available via Homebrew** — install
the binary directly:

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

Create the storage directory:
```bash
mkdir -p ~/qdrant_storage
```

> **Why Qdrant?** ChromaDB (the previous vector store) crashed at 32,285
> chunks. Qdrant — written in Rust — is stable at 105,964 chunks with
> native metadata filtering, near-zero GC overhead, and a production
> upgrade path (sharding, replication, quantization).

---

## 6. Clone AIStudio

```bash
mkdir -p ~/Developer && cd ~/Developer
git clone git@github.com:mbarberony/AIStudio.git && cd AIStudio
```

> **SSH error?** See [GitHub SSH setup](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

---

## 7. Install AIStudio Commands

This installs the `ais_*` command aliases into your shell — `ais_start`, `ais_stop`,
`ais_restart`, `ais_bench`, `ais_sec_download`, and others (used in the rest of this tutorial).
Enter this in your terminal window:

```bash
cd ~/Developer/AIStudio
./ais_install
```

`ais_install` will prompt you to run `source ~/.zshrc` at the end — do that, then verify:

```bash
ais_help
```

Expected: a list of available `ais_*` commands. If you see `command not found`,
run `source ~/.zshrc` and try again.

> **What `./ais_install` does:** Creates the Python virtual environment, installs
> all dependencies, and adds `ais_*` aliases to `~/.zshrc`. Safe to run multiple times.

---

## 8. Activate the Virtual Environment

`./ais_install` creates and populates the Python virtual environment automatically.
Each time you open a new terminal tab, activate it before running any AIStudio commands:

```bash
source ~/Developer/AIStudio/.venv/bin/activate
```

Your prompt will show `(.venv)` when active. `ais_start` handles this automatically —
you only need to activate manually if running Python commands directly.

---

## 9. Start All Services

AIStudio requires four processes: Ollama, Qdrant, FastAPI backend, and the
frontend. Start them all with:

```bash
ais_start
```

`ais_start` checks whether each service is already running before starting it —
safe to run multiple times.

**To start manually instead:**
```bash
# Terminal 1 — Qdrant
cd ~/qdrant_storage && QDRANT__STORAGE__STORAGE_PATH=~/qdrant_storage qdrant &

# Terminal 2 — Backend
cd ~/Developer/AIStudio && source .venv/bin/activate
OLLAMA_KEEP_ALIVE=30m AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
  uvicorn local_llm_bot.app.api:app --reload --port 8000
```

Verify the backend is up:
```bash
curl http://localhost:8000/health
```
Expected: `{"status": "ok"}`

> **API explorer:** Visit `http://localhost:8000/docs` for the full
> interactive Swagger UI — all endpoints with request/response schemas.

---

## 10. Ingest Documents

A **corpus** is a named collection of documents AIStudio indexes and makes
searchable.

### Option A — Demo Corpus (recommended for first run)

AIStudio ships with a curated demo corpus. To ingest it:

```bash
cd ~/Developer/AIStudio && source .venv/bin/activate
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \
  --corpus demo \
  --root data/corpora/demo/uploads
```

Try these questions to start:
- *"What is QFD and how does it apply to technology architecture?"*
- *"How should a CTO prioritize a three-year technology strategy?"*
- *"What are the key principles for modernizing legacy applications?"*

> **About the demo corpus:** This is not sample data. It is a curated set of
> 15 original documents spanning 2003–2021 — IT strategy frameworks, enterprise
> architecture methodology, financial services technology journals, cloud
> migration analysis, and AI reference architecture — produced across senior
> technology roles at major financial institutions. Querying it is querying
> 20 years of original thought leadership. The corpus and the tool are the
> same proof point.
>
> Run `ais_bench` to validate all 12 benchmark questions automatically.

### Option B — Your Own Documents

```bash
mkdir -p data/corpora/my_corpus/uploads
cp /path/to/your/documents/* data/corpora/my_corpus/uploads/

AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python -m local_llm_bot.app.ingest \
  --corpus my_corpus \
  --root data/corpora/my_corpus
```

You can also upload documents directly from the UI using the **Upload** button.

---

## 11. Open the Frontend

```bash
open ~/Developer/AIStudio/front_end/rag_studio.html
```

Select your corpus from the dropdown, choose a model, and ask a question.

**Using Filters (optional):** The sidebar has Firm and Year filter fields.
Leave them blank for cross-corpus queries. Type a firm name (e.g.
`Goldman Sachs`) to restrict retrieval to that firm's documents only.

---

## 12. Tuning Parameters

| Parameter | Default | Effect |
|-----------|---------|--------|
| Top K | 5 | Number of chunks retrieved per query. Higher = more context, slower. Try 10 for large corpora. |
| Temperature | 0.3 | LLM creativity. Lower = more factual and consistent. Higher = more varied. Keep at 0.3 for document Q&A. |
| Firm | (empty) | Restricts retrieval to chunks from this firm. Must match ingested firm name exactly. |
| Year | (empty) | Restricts retrieval to this filing year. Use the filing year (e.g. `2026` for fiscal year 2025 filings). |

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

**`python3.13` not found** — run `brew install python@3.13`

**UI shows "Error loading corpora" or "Ollama not running" on startup** — the browser opened before the backend finished starting. Hard-refresh (`Cmd+Shift+R`). If it persists, check for a Qdrant WAL error in the terminal (see below).

**Qdrant WAL lock — `Can't init WAL: Resource temporarily unavailable`** — a collection's write-ahead log was left locked from an unclean shutdown (force-quit, power loss, or crash). The collection name is in the panic message.

Fix:
```bash
ais_stop
rm -rf ~/qdrant_storage/collections/aistudio_help   # replace with collection named in error
ais_start
```
Then re-ingest the affected corpus via the UI (Add button). ⚠️ Delete only the collection named in the error — not the entire `qdrant_storage/` folder. See HOWTO.md for full details.

To prevent this: always stop with `ais_stop`, never force-quit the terminal while running.

**`(.venv)` not in prompt** — run `source ~/Developer/AIStudio/.venv/bin/activate`

**`ModuleNotFoundError`** — ensure `PYTHONPATH=src` and `AISTUDIO_VECTORSTORE=qdrant`
are set before the uvicorn command

**`Failed to fetch` in UI** — the FastAPI backend is down. Run:
```bash
kill $(lsof -ti:8000)
cd ~/Developer/AIStudio && source .venv/bin/activate
OLLAMA_KEEP_ALIVE=30m AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
  uvicorn local_llm_bot.app.api:app --reload --port 8000
```

**`ollama serve` — "address already in use"** — Ollama already running. Correct state.

**Stats show 0 chunks** — corpus not yet ingested into Qdrant. Run Step 9.

**Backend code changes not reflected** — uvicorn `--reload` watches Python files.
If changes don't appear, kill and restart the backend process.

**Qdrant not found** — `~/bin` not in PATH. Run `source ~/.zshrc` or
add `export PATH="$HOME/bin:$PATH"` to `~/.zshrc`.

**Citations show wrong page numbers or stale content** — corpus has mixed
old/new chunk formats. Re-ingest with `--force` to wipe and rebuild cleanly:
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

## Optional — Run the Benchmark

```bash
cd ~/Developer/AIStudio && source .venv/bin/activate

# Demo corpus — 12 curated questions, auto-detected question file
ais_bench

# SEC 10-K corpus — requires downloading filings first (not in repo, ~2 GB)
# This is one of the few cases where you'll run terminal commands directly.
# ais_sec_download handles the SEC EDGAR protocol automatically.
# The ingest step that follows is identical to ingesting any corpus you build yourself.

# Step 1: Download filings to ~/Downloads (~5 min, ~2 GB)
ais_sec_download

# Step 2: Ingest the files using the AIStudio UI
# Open AIStudio, create a corpus named 'sec_10k', and upload the files
# from ~/Downloads/sec_10k/ using the Upload button.
# Allow ~34 minutes for ingestion. This is the same process as any corpus.
# See HOWTO.md — "How do I ingest the SEC 10-K corpus?" for full instructions.

# Step 3: Benchmark (once ingestion is complete)
# See HOWTO.md — "How do I benchmark a different corpus?" for full options.
ais_bench --corpus sec_10k --top-k 10

# Run with 70b model
ais_bench --corpus demo --top-k 5 --temperature 0.3 --model llama3.1:70b
```

Prints pass/fail with latency per question, writes timestamped JSON and Markdown reports to `benchmarks/reports/`. Question files
auto-detected from `benchmarks/{corpus}_questions.yaml`.

---

For architecture context, see [docs/architecture_decisions.md](docs/architecture_decisions.md).
For benchmark results, see [benchmarks/](benchmarks/) for timestamped reports.
