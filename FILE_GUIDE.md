# FILE_GUIDE.md
*Type: REF | Domain: AIStudio | Status: ACTIVE | Audience: User*
*Version: 1.0.0*
*Created: 2026-05-08 | Owner: Manuel Barbero*

---

## How to use this guide

This is a **functional/relational** file guide — answers "what does each file do, what does it consume, what does it produce, what depends on it" rather than just "where does it live."

If you're new to AIStudio, read [README.md](README.md) first, then [QUICKSTART.md](QUICKSTART.md), then this file.

---

## §1 The runtime layer — `src/` + `front_end/` + `data/`

**What runs to answer a query.**

### `src/local_llm_bot/app/` — Python application

| File | Function | Reads | Produces |
|---|---|---|---|
| `api.py` | FastAPI HTTP layer | Corpus metadata, query payload, system prompt | JSON response with citations |
| `rag_core.py` | RAG pipeline orchestration | Query, corpus index | Embedded query → retrieved chunks → reranked → LLM context |
| `ingest/pipeline.py` | Document ingestion (per-file chunked/embedded/upserted) | Files in `data/corpora/<name>/uploads/`, corpus metadata | `index.jsonl`, `manifest.jsonl`, Qdrant chunks |
| `ingest/loaders.py` | File-type-specific loaders | PDF/DOCX/HTML/MD files | Plain text + page metadata |
| `ingest/chunking.py` | Text chunking with overlap | Plain text | Chunks with stable IDs |
| `vectorstore/qdrant_store.py` | Vector store interface | Embeddings, metadata | Qdrant collections, similarity search |
| `ollama_client.py` | Ollama HTTP wrapper | Model name, prompt | Embedding vectors, LLM completions |
| `config.py` | Environment-driven config | OS env vars | Settings dict |

### `front_end/rag_studio.html` — UI

Single self-contained HTML file. Opens directly in your browser, no server needed. Communicates with the FastAPI backend at `localhost:8000`.

**Provides**: corpus selector, chat with citations, corpus CRUD (new/delete/rename), file upload + per-file inspect, metadata edit (description, search_guidance), help modal.

### `data/corpora/<name>/` — Document corpora

Each corpus is a self-contained folder:

| File | What it is | Who writes it |
|---|---|---|
| `uploads/` | Source documents (PDF, DOCX, etc.) | You via UI Add Files |
| `<name>_corpus_metadata.yaml` | Description, search_guidance, sources[], runtime stats | Created at corpus creation, updated at ingest |
| `index.jsonl` | One row per chunk: ID, source path, page, text | Ingest pipeline |
| `manifest.jsonl` | Per-file ingest record: chunks count, last_ingested_at | Ingest pipeline |
| `trash/` | Soft-deleted files (recoverable) | UI delete |

**Demo corpus** ships with the repo. **Help corpus** is built from `docs/` + key root markdown. **User corpora** are private to you.

### `prompts/system.txt` — System prompt

Loaded by `api.py` at query time. Per-corpus `search_guidance` from `<name>_corpus_metadata.yaml` is appended dynamically — that's how AIStudio routes questions to the right document in multi-document corpora.

---

## §2 The command surface

All commands available after running `./ais_install` from repo root.

| Command | What it does | When you use it | Reads / Produces |
|---|---|---|---|
| `ais_start` | Starts FastAPI + Qdrant + Ollama; opens UI | Beginning of every session | — / running services |
| `ais_stop` | Stops all services cleanly | End of every session | — / — |
| `ais_log` | Tails the live backend log | Debugging; watching queries | service logs / stdout |
| `ais_bench` | Runs benchmark suite against a corpus | Validating retrieval quality | `benchmarks/<corpus>/<corpus>_questions.yaml` / `benchmarks/<corpus>/reports/benchmark_<corpus>_<date>_<time>.{json,md,pdf}` |
| `ais_download_sec_10k` | Downloads SEC 10-K filings from EDGAR | Setting up SEC corpus (optional) | EDGAR / `data/corpora/sec_10k/uploads/` |
| `ais_ingest_sec_10k` | Ingests SEC filings into AIStudio | After downloading SEC | uploads/ / index.jsonl + Qdrant |
| `ais_help` | Shows command reference | Forgot a command | `ais_command_help.txt` / stdout |
| `ais_install` | Installs/updates user commands | Fresh install; new command | `ais_user_commands_manifest.yaml` / shell aliases in `~/.zshrc` |
| `ais_create_shortcut` | Creates AIStudio Dock/Desktop icon (macOS) | Optional post-install | / `~/Desktop/AIStudio.app` |

---

## §3 The repo root layout

| File / Dir | What it does | Relationship |
|---|---|---|
| `README.md` | Product overview | Entry point — read first |
| `QUICKSTART.md` | Install + first-run guide | Read after README |
| `HOWTO.md` | Day-to-day usage recipes | Read for "how do I X" |
| `TUTORIAL.md` | Guided walkthroughs | Read after QUICKSTART |
| `CONTRIBUTING.md` | Contribution guide | Read before contributing |
| `LICENSE` | License terms | Repo convention |
| `Makefile` | `make install`, `make test-unit`, `make test`, `make lint` | Build orchestration |
| `pyproject.toml` | Python project config (ruff, pytest) | Tool config |
| `requirements.txt` | Python dependencies | `pip install -r` |
| `ais_install` | User command installer | Reads `ais_user_commands_manifest.yaml` |
| `ais_user_commands_manifest.yaml` | Auto-generated user command list | Produced by install/deploy |
| `ais_*.sh` | User commands (see §2) | Aliased by `ais_install` |
| `AIStudio.png`, `AIStudio.svg`, `AIStudio.icns` | App branding | Used by `ais_create_shortcut` |
| `prompts/system.txt` | LLM system prompt | Loaded by `api.py` |
| `front_end/rag_studio.html` | UI | Opened in browser |
| `src/` | Application source (see §1) | Imported by api.py |
| `tests/` | Test suite | Run by `make test` |
| `docs/` | User documentation + help corpus sources | Ingested into the help corpus |
| `benchmarks/` | Benchmark harness + question files + reports | Run by `ais_bench` |
| `data/` | Corpus data (demo + help shipped; user corpora private) | Read by `rag_core.py` |

---

## §4 Documentation files

| File | What it covers |
|---|---|
| `README.md` | What AIStudio is, why it was built, how it performs |
| `QUICKSTART.md` | How to install and run AIStudio from scratch |
| `HOWTO.md` | How to do specific things — corpus management, troubleshooting |
| `TUTORIAL.md` | Guided walkthroughs |
| `docs/architecture_decisions.md` | Why key technical choices were made (Qdrant, CrossEncoder, etc.) |
| `docs/PRODUCT_ROADMAP.md` | What's coming in Beta, v2.0, and beyond |
| `docs/QA_TESTING_LESSONS_LEARNED.md` | What was discovered during fresh install testing |
| `docs/CODEBASE_GUIDE.md` | How the codebase is organized — data flow, directory layout, API endpoints |
| `docs/HARNESS.md` | How to use the benchmark harness — CLI flags, question files, reading reports |
| `docs/DEMO_CORPUS.md` | What ships in the demo corpus and suggested questions to try |
| `docs/dependencies.md` | Python and system dependencies, version requirements |

---

## §5 The corpus metadata file

Each corpus has a metadata file at `data/corpora/<name>/<name>_corpus_metadata.yaml`. It contains:

- `short_description` — displayed in the header next to the corpus name
- `description` — full description of the corpus contents and purpose
- `search_guidance` — routing hints injected into the system prompt to direct the model to the right document for each type of question
- `sources` — per-file metadata (description, keywords) that helps retrieval
- `last_ingested_at`, `ingest_duration_seconds`, `avg_seconds_per_file` — ingest tracking

Edit these fields via the **Edit** button in the UI, or directly in the YAML file.

---

## §6 The system prompt

AIStudio uses a system prompt (`prompts/system.txt`) to guide how the language model answers questions. It instructs the model to answer only from provided sources, cite every factual claim, and be direct and specific.

The corpus metadata file adds per-corpus routing guidance on top of the system prompt — telling the model which document to consult for which type of question. This significantly improves answer quality on corpora with multiple documents covering distinct topics.

---

## §7 Benchmark question files

Each corpus can have a benchmark questions file at `benchmarks/<corpus>/<corpus>_questions.yaml`. It contains a set of questions with expected keywords and source documents. Run with `ais_bench --corpus <name>` to validate retrieval quality.

| File | Corpus |
|---|---|
| `benchmarks/demo/demo_questions.yaml` | Demo corpus |
| `benchmarks/help/help_questions.yaml` | Help corpus |
| `benchmarks/sec_10k/sec_10k_questions.yaml` | SEC 10-K corpus (auto-generated) |

Reports land in `benchmarks/<corpus>/reports/` as paired `.json` / `.md` / `.pdf` files.

---

## §8 Services

When AIStudio is running, four processes are active:

| Service | Address | What it does |
|---|---|---|
| FastAPI backend | `localhost:8000` | RAG pipeline, corpus management, all API endpoints |
| Qdrant | `localhost:6333` | Vector store — stores and retrieves document chunks |
| Ollama | `localhost:11434` | Runs the language model and embedding model locally |
| Frontend | `file://` in browser | The UI — no server needed |

---

## §9 Cross-cutting workflows

**Concrete scenarios mapped to file flows.**

### Workflow A: Adding documents to a new corpus

1. Create the corpus via UI **New** button (provide name, description)
2. AIStudio creates `data/corpora/<name>/` with metadata file + empty uploads
3. Click **Add Files** → upload PDFs / DOCX / etc. into `data/corpora/<name>/uploads/`
4. Ingest pipeline runs automatically: chunks → embeddings → Qdrant upsert
5. `index.jsonl` + `manifest.jsonl` written to `data/corpora/<name>/`
6. Edit **search_guidance** in the corpus metadata to route questions across documents
7. Query via chat

### Workflow B: Running a benchmark

1. Ensure benchmark questions file exists at `benchmarks/<corpus>/<corpus>_questions.yaml`
2. Run `ais_bench --corpus <name>`
3. Report lands in `benchmarks/<corpus>/reports/` as paired `.json` / `.md` / `.pdf`
4. Review pass/fail, latency, retrieval quality
5. Adjust `search_guidance` in corpus metadata if retrieval is missing the mark
6. Re-run benchmark to validate

### Workflow C: Updating documentation

1. Edit `.md` files in `docs/` or root markdown (`README.md`, `HOWTO.md`, etc.)
2. Run the help corpus update workflow to regenerate the help corpus
3. Help corpus PDFs regenerate; Qdrant chunks update
4. The **Help** button in the UI now reflects your changes

### Workflow D: Troubleshooting

1. Run `ais_log` in a terminal to tail the backend log
2. Make a query in the UI
3. Watch the log for errors or surprising behavior
4. If Qdrant fails: restart with `ais_stop` then `ais_start`
5. If Ollama fails: check `localhost:11434` is reachable; pull the model if missing
6. Consult `HOWTO.md` for known issues

---

## §10 The file-to-action map

**Quick lookup: who reads what, who writes what, what feeds into what.**

| File pattern | Reads | Writes | Feeds into |
|---|---|---|---|
| `<corpus>_corpus_metadata.yaml` | `api.py` (system prompt), UI Edit | Ingest pipeline, UI Edit | LLM routing, search_guidance display |
| `prompts/system.txt` | `api.py` | You (manual edit) | LLM system instructions |
| `data/corpora/<name>/uploads/*` | Ingest pipeline | UI Add Files | Corpus chunks → Qdrant |
| `data/corpora/<name>/index.jsonl` | `rag_core.py` retrieval | Ingest pipeline | Query → ranked chunks |
| `benchmarks/<corpus>/<corpus>_questions.yaml` | `ais_bench` | You (manual edit) | Benchmark reports |
| `benchmarks/<corpus>/reports/*.json/md/pdf` | You | `ais_bench` | Quality validation, regression tracking |
| `ais_user_commands_manifest.yaml` | `ais_install` | Auto-generated | Shell alias creation |

---

## §11 How AIStudio answers questions

AIStudio retrieves relevant chunks from indexed documents and uses them to answer your question. It does not read files directly or display raw file content.

- To read a specific document — use the **Open ↗** link in the references panel
- To see what was retrieved — citations show the source document and page number
- If the answer seems incomplete — try rephrasing or increasing **Top K** in settings
- Search guidance in the corpus metadata improves routing across multi-document corpora

---

## §12 Version history

| Version | Date | Changes |
|---|---|---|
| 1.0.0 | 2026-05-08 | Initial consolidated FILE_GUIDE. Functional/relational framing — what each file does, what it consumes, what it produces. |
