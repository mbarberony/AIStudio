# AIStudio — Product Roadmap

*Version: 1.1.0 | Updated: 2026-05-22*

> A product-level view of where AIStudio is, where it is going, and why.
> For the technical backlog and implementation detail, see [roadmap.md](roadmap.md).

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

There is no v1.0. The product goes directly from Beta to v2.1 — the first release intended for external use. This reflects a deliberate choice: internal development milestones don't need public version numbers.

Each release milestone has a clear definition of "ready":

| Milestone | Definition |
|---|---|
| **Beta** | Stable on Apple Silicon, clean install under 30 minutes, benchmark-validated retrieval quality, full documentation. Permanent — never closed. |
| **v2.1** | Source Dive (click citation → open to exact page), one-click installer, API documentation published, corpus metadata at creation time |
| **v3.0** | Multi-user, shared corpora, cloud deployment |

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
- Benchmark harness with YAML question files and timestamped pass/fail reports
- REST API exposing all capabilities for scripted access
- Full documentation: QUICKSTART, HOWTO, architecture decisions, benchmark guide

**Known limitations at Beta:**
- Apple Silicon only (Intel Mac, Windows, Linux: v2.0)
- Single-user, local only (multi-user: v3.0)
- Source Dive (click citation → scroll to exact page in PDF viewer): v2.0
- Corpus metadata entered manually via YAML file (UI entry: v2.0)

---

## v2.1 — First External Release

v2.1 is the first external release. The three themes are: **better source access,
easier onboarding, and a published API**.

### Source Dive
The highest-impact feature on the roadmap. Citations currently show document
name and page number with a link that opens the PDF. Source Dive goes further:
click a citation and the PDF opens at the exact page, with the cited passage
highlighted. The backend already stores chunk-level page positions in Qdrant.
The remaining work is the frontend PDF viewer (PDF.js).

### One-Click Installer
The current install is guided and takes under 30 minutes, but requires terminal
familiarity. v2.1 ships a `.dmg` installer that handles the full setup — Python
environment, Qdrant, Ollama pull, alias registration — without a terminal.

### Corpus Metadata at Creation Time
When creating a corpus, users can provide a short description, a summary of
what's in it, and routing guidance (hints about which documents answer which
kinds of questions). This metadata is injected into the system prompt at query
time to improve retrieval precision. Currently this requires manual YAML editing;
v2.1 adds UI fields to the New Corpus modal.

### Published API Documentation
AIStudio's REST API is stable at Beta. v2.1 publishes full API documentation
(`API_DOC.md`) with request/response schemas, error codes, and examples. FastAPI's
built-in Swagger UI (`/docs`) is also enabled, making the API self-documenting
for developers integrating AIStudio into their own workflows.

### Intel Mac, Windows, Linux
Platform support extended beyond Apple Silicon.

### Benchmark Harness v2
Comparison tooling — run benchmarks across multiple configurations and view results side by side.

---

## v3.0 — Multi-User and Cloud

v3.0 is the team release. The core addition is a user model: accounts, roles,
and shared corpora. Multiple users can query the same corpus, with answers
attributed to the correct source documents.

Cloud deployment target: AWS ECS Fargate with S3-backed Qdrant storage and
CloudFront for the frontend. The four-process architecture (browser → FastAPI
→ Qdrant → Ollama) maps directly to containerized deployment — no architecture
change required, only configuration.

GPU inference support (AWS Inferentia2 or g4dn.xlarge) is also a v3.0 item,
enabling frontier-quality LLMs at production latency.

---

## What Is Not on the Roadmap

**Web search integration** — deliberate exclusion. AIStudio answers from your
corpus, not from the internet. Mixing web results would undermine the core
value proposition: grounded, citable, private answers from your own documents.

**Hosted SaaS** — not planned. The local-first design is the product, not a
limitation to eventually overcome.

---

*For implementation detail and the full technical backlog, see [roadmap.md](roadmap.md).*
*For architecture decisions and rationale, see [architecture_decisions.pdf](architecture_decisions.pdf).*
