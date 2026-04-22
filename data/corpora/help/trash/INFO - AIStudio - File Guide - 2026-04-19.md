# INFO - AIStudio - File Guide - 2026-04-19.md
*Type: INFO | Domain: AIStudio | Status: ACTIVE*
*Version: 1.0.0*
*Created: 2026-04-19 | Owner: Manuel Barbero*

---

## Purpose

A guide to the files and commands that make up AIStudio — what each one does,
when you'd use it, and where to find it. Written for users who want to understand
what they're working with.

---

## Commands

These are the commands available after running `./ais_install`.

| Command | What it does | When to use it |
|---|---|---|
| `ais_start` | Starts all AIStudio services and opens the UI | Beginning of every session |
| `ais_stop` | Stops all AIStudio services cleanly | End of every session |
| `ais_log` | Shows the live backend log | Debugging; watching queries in real time |
| `ais_bench` | Runs the benchmark suite against a corpus | Validating retrieval quality |
| `ais_download_sec_10k` | Downloads SEC 10-K filings from EDGAR | Setting up the SEC corpus (optional) |
| `ais_ingest_sec_10k` | Ingests SEC 10-K filings into AIStudio | After downloading SEC filings |
| `ais_help` | Shows the command reference | When you forget a command |
| `ais_install` | Installs or updates AIStudio commands | Fresh install; adding a new command |

---

## The Frontend

`front_end/rag_studio.html` is the entire AIStudio user interface — a single HTML
file you open directly in your browser. No server required. Everything is inline.

Key areas of the UI:
- **Corpus selector** — choose which document collection to query
- **Chat** — ask questions, see answers with citations
- **Add / Delete** — manage documents in a corpus
- **Stats** — see how many documents and chunks are indexed
- **Help** — powered by AIStudio itself, answers questions about how to use it

---

## Your Documents

Documents live in `data/corpora/<corpus-name>/uploads/`. When you delete a file
from the UI, it moves to `data/corpora/<corpus-name>/trash/` — it's never
permanently destroyed. Qdrant chunks are removed at delete time.

The **demo corpus** ships with AIStudio and contains 9 original documents spanning
2003–2026 — enterprise architecture, IT strategy, financial services technology,
and agentic AI. Querying it is querying 20 years of original practitioner work.

---

## Key Documentation Files

| File | What it covers |
|---|---|
| `README.md` | What AIStudio is, why it was built, how it performs |
| `QUICKSTART.md` | How to install and run AIStudio from scratch |
| `HOWTO.md` | How to do specific things — corpus management, troubleshooting |
| `docs/architecture_decisions.md` | Why key technical choices were made (Qdrant, CrossEncoder, etc.) |
| `docs/PRODUCT_ROADMAP.md` | What's coming in Beta, v2.0, and beyond |
| `docs/QA_TESTING_LESSONS_LEARNED.md` | What was discovered during fresh install testing |

---

## The System Prompt

AIStudio uses a system prompt (`prompts/system.txt`) to guide how the language
model answers questions. It instructs the model to answer only from provided
sources, cite every factual claim, and be direct and specific.

The corpus metadata file (`data/corpora/<name>/<name>_corpus_meta.yaml`) adds
per-corpus routing guidance on top of the system prompt — telling the model which
document to consult for which type of question.

---

## Services

When AIStudio is running, four processes are active:

| Service | Address | What it does |
|---|---|---|
| FastAPI backend | `localhost:8000` | RAG pipeline, corpus management, all API endpoints |
| Qdrant | `localhost:6333` | Vector store — stores and retrieves document chunks |
| Ollama | `localhost:11434` | Runs the language model and embedding model locally |
| Frontend | `file://` in browser | The UI — no server needed |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0.0 | 2026-04-19 | Initial version — user-facing companion to the folder structure reference. |
