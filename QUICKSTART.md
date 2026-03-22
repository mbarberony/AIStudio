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
> being a latency variable. See BENCHMARK_FINDINGS.md.

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

## 7. Set Up Python Virtual Environment

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Your prompt will show `(.venv)` when active.
**Run `source .venv/bin/activate` every time you open a new terminal tab.**

---

## 8. Start All Services

AIStudio requires four processes: Ollama, Qdrant, FastAPI backend, and the
frontend. The auto-launch script handles all of them:

```bash
~/Developer/AIStudio/scripts/start.sh
```

The script checks whether each service is already running before starting it —
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

## 9. Ingest Documents

A **corpus** is a named collection of documents AIStudio indexes and makes
searchable.

### Option A — Demo Corpus (recommended for first run)

AIStudio ships with a curated demo corpus. To ingest it:

```bash
cd ~/Developer/AIStudio && source .venv/bin/activate
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \
  --corpus demo \
  --root data/demo/demo_data
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
> Run `python3 scripts/benchmark.py --corpus demo --top-k 5 --temperature 0.3`
> to validate all 12 benchmark questions automatically.

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

## 10. Open the Frontend

```bash
open ~/Developer/AIStudio/front_end/rag_studio.html
```

Select your corpus from the dropdown, choose a model, and ask a question.

**Using Filters (optional):** The sidebar has Firm and Year filter fields.
Leave them blank for cross-corpus queries. Type a firm name (e.g.
`Goldman Sachs`) to restrict retrieval to that firm's documents only.

---

## 11. Tuning Parameters

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
  --corpus demo --root data/demo/demo_data --force
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
python3 scripts/benchmark.py --corpus demo --top-k 5 --temperature 0.3

# SEC 10-K corpus — requires ~/Downloads/sec_10k_corpus/ (not included in repo)
python3 scripts/benchmark.py --corpus sec_10k --top-k 10 --temperature 0.3

# Run with 70b model
python3 scripts/benchmark.py --corpus demo --top-k 5 --temperature 0.3 --model llama3.1:70b
```

Prints pass/fail with latency per question, writes `scripts/benchmark_results.json`
and updates `scripts/BENCHMARK_FINDINGS.md`. Question files auto-detected from
`benchmarks/{corpus}_questions.yaml`.

---

For architecture context, see [docs/architecture_decisions.md](docs/architecture_decisions.md).
For benchmark results, see [BENCHMARK_FINDINGS.md](BENCHMARK_FINDINGS.md).
