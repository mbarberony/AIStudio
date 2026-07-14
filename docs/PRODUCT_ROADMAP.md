# AIStudio — Product Roadmap

*Version: 1.2.0 | Updated: 2026-07-12*

> A product-level view of where AIStudio is, where it is going, and why.

---

## What AIStudio Is

AIStudio is a local RAG (Retrieval-Augmented Generation) application for Apple Silicon.
It lets you ingest your own documents, ask questions in natural language, and get
answers that cite exactly which document and page they came from — all running
on your machine, with no data sent anywhere.

The core value proposition: your documents stay private, the system runs without
internet, and the answers are grounded in your corpus rather than in a model's
training data.

---

## Release Philosophy

AIStudio is intentionally in a state of permanent Beta. Not as a disclaimer, but as a design principle: the proof point is a living system, always being improved, never declared finished. Versioning marks milestones, not completion.

There is no v1.0. Beta is the current state; everything beyond is described here as post-Beta direction — capabilities and themes, not committed version numbers.

Each release milestone has a clear definition of "ready":

| Milestone | Definition |
|---|---|
| **Beta (current)** | Stable on Apple Silicon, clean install under 30 minutes, benchmark-validated retrieval quality, full documentation. Permanent — never closed. |
| **Post-Beta** | Source Dive (click citation → open to exact page), one-click installer, API documentation published, corpus metadata at creation time |
| **Future** | Multi-user, shared corpora, cloud deployment |

---

## Beta — Current State

Beta is the foundation release. Everything here either works reliably or is
explicitly documented as a known limitation.

**What works:**
- Ingest PDF, Word, PowerPoint, Markdown, and HTML documents into named corpora
- Two-stage retrieval: vector search + CrossEncoder reranking for high-relevance answers
- Page-accurate citations with one-click source access
- Multiple LLM options via Ollama (llama3.1:8b default, llama3.1:70b for quality)
- Conversation memory within a session, persisted across page refresh
- Per-corpus routing guidance to steer retrieval toward the right documents
- Hybrid retrieval (M2.A) — Retrieval Mix slider blends vector semantic search with BM25 keyword matching; tunable per query
- Firm isolation with grounded no-answer — a question about one firm is answered only from that firm's documents; when the corpus doesn't cover a firm, AIStudio says so (and names what it does cover) rather than answering from the wrong company
- Memory-fit guard — models are checked against the machine's available RAM before use; the UI's model picker shows a fit verdict and disables a model too large to run, so an oversized model is caught rather than silently loaded-then-hung
- Benchmark harness with YAML question files and timestamped pass/fail reports — memory-aware, with `--fit-policy` (skip / downshift / force) and a `--dry-run` preview so a run on a memory-constrained Mac won't stall on an oversized model
- REST API exposing all capabilities for scripted access, documented for integrators (including MCP builders)
- Full documentation: QUICKSTART, HOWTO, TUTORIAL, architecture decisions, benchmark guide

**Known limitations at Beta:**
- Apple Silicon only (Intel Mac, Windows, Linux: post-Beta)
- Single-user, local only (multi-user: future)
- Source Dive (click citation → scroll to exact page in PDF viewer): post-Beta
- Corpus metadata entered manually via YAML file (UI entry: post-Beta)

---

## Near-Term Quality Work — In Progress

Retrieval-quality improvements underway within Beta — not new milestones, but the
work that most improves answer accuracy on dense financial corpora:

- **Entity name-resolution** — bind every ingested filing to a canonical firm identity (keyed on the filer's registration number, not the filename) so a firm is recognized and isolated regardless of how a document names itself.
- **Table-aware chunking** — multi-cell numeric tables (e.g. a metric × firm × year grid) retrieve poorly today and can be misread by smaller models; chunking that preserves table structure keeps those figures attributable.
- **Per-entity retrieval floor** — guarantee thinly-represented firms (a firm with only one or two filings) still rank into the retrieved set under blended retrieval, so a sparse firm isn't crowded out.

---

## Post-Beta — First External Release

The first external release. The three themes are: **better source access,
easier onboarding, and a published API**.

### Source Dive
The highest-impact feature on the roadmap. Citations currently show document
name and page number with a link that opens the PDF. Source Dive goes further:
click a citation and the PDF opens at the exact page, with the cited passage
highlighted. The backend already stores chunk-level page positions in Qdrant.
The remaining work is the frontend PDF viewer (PDF.js).

### One-Click Installer
The current install is guided and takes under 30 minutes, but requires terminal
familiarity. Post-Beta ships a `.dmg` installer that handles the full setup — Python
environment, Qdrant, Ollama pull, alias registration — without a terminal.

### Corpus Metadata at Creation Time
When creating a corpus, users can provide a short description, a summary of
what's in it, and routing guidance (hints about which documents answer which
kinds of questions). This metadata is injected into the system prompt at query
time to improve retrieval precision. Currently this requires manual YAML editing;
Post-Beta adds UI fields to the New Corpus modal.

### Published API Documentation
AIStudio's REST API is stable at Beta. Post-Beta publishes full API documentation
(`API_DOC.md`) with request/response schemas, error codes, and examples. FastAPI's
built-in Swagger UI (`/docs`) is also enabled, making the API self-documenting
for developers integrating AIStudio into their own workflows.

### Intel Mac, Windows, Linux
Platform support extended beyond Apple Silicon.

### Benchmark Harness v2
Comparison tooling — run benchmarks across multiple configurations and view results side by side.

---

## Future — Multi-User and Cloud

The team release. The core addition is a user model: accounts, roles,
and shared corpora. Multiple users can query the same corpus, with answers
attributed to the correct source documents.

Cloud deployment target: AWS ECS Fargate with S3-backed Qdrant storage and
CloudFront for the frontend. The four-process architecture (browser → FastAPI
→ Qdrant → Ollama) maps directly to containerized deployment — no architecture
change required, only configuration.

GPU inference support (AWS Inferentia2 or g4dn.xlarge) is also a future item,
enabling frontier-quality LLMs at production latency.

---

## What Is Not on the Roadmap

**Web search integration** — deliberate exclusion. AIStudio answers from your
corpus, not from the internet. Mixing web results would undermine the core
value proposition: grounded, citable, private answers from your own documents.

**Hosted SaaS** — not planned. The local-first design is the product, not a
limitation to eventually overcome.

---

*For architecture decisions and rationale, see [architecture_decisions.pdf](architecture_decisions.pdf).*
