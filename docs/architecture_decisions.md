# Architecture Decisions

Key technical choices made in this project, with rationale. This document is
intended for anyone reviewing the codebase who wants to understand not just
what was built, but why.

---

## 1. Local-First Design (Ollama, No External API)

**Decision:** All LLM inference and embedding runs locally via Ollama. No OpenAI,
Anthropic, or other cloud API dependency in the core stack.

**Why:**
- Forces genuine understanding of model behavior at the infrastructure level —
  latency, memory pressure, model selection tradeoffs
- Eliminates API cost as a variable during experimentation
- Relevant to financial services contexts where data residency and network egress
  are real constraints, not afterthoughts
- Makes the system runnable in air-gapped or restricted environments

**Tradeoff:** Inference quality is lower than frontier models. This is a deliberate
constraint, not a limitation. The goal is substrate knowledge, not benchmark
performance.

**Would change for production:** Add LiteLLM as a provider abstraction layer.
Local inference for development and sensitive data; cloud inference (with
appropriate data handling) for production quality. The architecture is designed
to make this substitution straightforward — Ollama client is isolated in
`ollama_client.py`.

---

## 2. Qdrant as Vector Store (replaced ChromaDB)

**Decision:** Qdrant 1.17.0, running as a separate process on port 6333.
ChromaDB was the original choice and was replaced in production.

**Why the switch:**
ChromaDB crashed at 32,285 chunks during the SEC 10-K corpus ingest. Not a
configuration issue — a hard failure at scale. Qdrant was stable at 105,964
chunks with zero failures across multiple full re-ingests.

**Why Qdrant specifically:**
- Written in Rust — near-zero GC overhead vs ChromaDB's Python-based memory model
- Native metadata filtering via `Filter`/`FieldCondition` — firm and year filters
  run at the vector search layer, not post-hoc on results
- Production upgrade path: sharding, replication, quantization, gRPC (port 6334)
- Separate process model — independently restartable, independently scalable,
  maps directly to a Docker container in cloud deployment

**The four-process pattern is deliberate:** Browser → FastAPI → Qdrant → Ollama.
Each process independently restartable. The separation that looks like operational
overhead in a personal lab is the same separation that enables horizontal scaling
in production — add Qdrant nodes, add uvicorn workers, point at shared Qdrant
cluster. No architecture change required.

**Tradeoff:** Qdrant requires a separate process and persistent storage directory
(`~/qdrant_storage/`). ChromaDB ran in-process with zero operational overhead.
The stability gain at scale makes this tradeoff non-negotiable.

**Would change for production:** Same Qdrant, configured for replication and
S3-backed snapshots. Alternatively Qdrant Cloud for managed hosting.
The `qdrant_store.py` adapter makes the substitution a configuration change.

---

## 3. Embedding Model: `nomic-embed-text`

**Decision:** `nomic-embed-text` as the default embedding model (768 dimensions,
cosine similarity).

**Why:**
- Best CPU/unified memory performance among locally available models at time
  of selection — low latency without GPU
- Produces meaningful semantic representations for the document types in scope
- Passes embedding arithmetic tests (King − Man + Woman ≈ Queen), a practical
  signal of semantic quality

**Considered:** `bge-large-en` — approximately 5% quality improvement on
retrieval benchmarks, but roughly 2x slower. The tradeoff didn't justify it.

**Would change for production:** Benchmark against the specific corpus and
query patterns in scope. Embedding model selection is highly workload-dependent.

---

## 4. Citation Logic Embedded in API, Not Modularized

**Decision:** Citation extraction and formatting lives in `api.py` rather than
as a separate module.

**Why:**
- Citation logic is tightly coupled to the response pipeline — it operates on
  LLM output immediately before it's returned
- Separating it adds indirection without architectural benefit at this scale
- Simpler deployment: one file to update, no import chain to maintain

**Tradeoff:** `api.py` is longer as a result.

**Would change for production:** With multiple citation formats or output channels,
a dedicated citation module with a clean interface would be worth the overhead.

---

## 5. Semantic Chunking Over Fixed-Size Chunking

**Decision:** Boundary-aware semantic chunking. The previous implementation used
fixed character counts.

**Why:**
- Fixed chunking fragments natural language units — a sentence split across two
  chunks degrades retrieval significantly
- Document structure carries semantic information: section headers, paragraph
  breaks, sentence boundaries are meaningful signals
- Measured improvement: ~25–40% accuracy improvement on document queries

**Implementation:** Three-tier fallback — semantic boundary detection → sentence
splitting → character fallback.

**Tradeoff:** Variable-length chunks create some unpredictability in context
window usage. Handled via explicit context window management in the retriever.

---

## 6. Metadata Filtering at the Vector Layer

**Decision:** Firm and year filters are applied as Qdrant `FieldCondition`
filters at query time, not as post-hoc filtering on results.

**Why:**
- Post-hoc filtering wastes retrieval budget — you retrieve top-K then discard
  most of them. Vector-layer filtering retrieves top-K from the filtered subset.
- Qdrant's native Filter API has zero measurable latency overhead.
- Metadata (firm, year) is parsed from filenames at ingest time
  (`_parse_firm_year()` in `pipeline.py`) and stored as Qdrant payload fields.
  No manual tagging required.

**Pattern:** `Goldman_Sachs_10K_2026-02-25.htm` → `firm=Goldman Sachs, year=2026`
parsed automatically. Filter adds zero latency. Filter is optional — omitting
it runs cross-corpus retrieval.

---

## 7. Page-Aware PDF Chunking via pdfplumber *(implemented Beta)*

**Decision:** pdfplumber as primary PDF extractor, inserting `[PAGE_N]` markers
at each page boundary. pypdf retained as fallback.

**Why pdfplumber over pypdf:**
- pypdf extracts flat text with no page boundary information
- pdfplumber provides page-by-page extraction with reliable boundary detection
- `[PAGE_N]` markers flow through the chunking pipeline into Qdrant payload
  (`page` field) and `chunk_id` (`filename::page-N::chunk-M`)

**Pipeline:** `loaders._extract_pdf()` → `[PAGE_N]` markers in text →
`pipeline.py` extracts page numbers → stored in Qdrant payload → surfaced
in `RetrievedDoc.page` → rendered in UI citation footnotes with `Open ↗` link.

**Null pages are expected** for: non-PDF files (PPTX, DOCX), scanned PDFs
with no text layer, and continuation chunks that start mid-page.

**PDF viewer — click citation → scroll to page** remains a v2.0 item requiring
frontend PDF rendering (pdfjs). Page numbers are ready in the backend; the
viewer frontend is the remaining work.

---

## 8. Conversation Memory: Sliding Window of 10 Turns

**Decision:** Last 10 conversation turns maintained as context for follow-up
questions.

**Why:**
- Covers most realistic conversational patterns without excessive context
  window consumption
- Stateless between sessions by design — no persistence layer required

**Tradeoff:** Long research sessions lose early context. Vector-based memory
store (storing conversation summaries as embeddings) would be more appropriate
for persistent multi-session memory.

---

## 9. JSONL Baseline for Deterministic Testing

**Decision:** A JSONL retrieval path exists alongside the Qdrant path, returning
deterministic results without embedding inference.

**Why:**
- Embedding models are nondeterministic under some conditions and slow in CI
- Allows testing the full API response pipeline without Ollama or Qdrant running
- Unit tests use the JSONL path; integration tests use Qdrant

---

## 10. Single HTML File Frontend

**Decision:** The entire UI is `front_end/rag_studio.html` — one file, ~3,700
lines, no build step.

**Why:**
- Zero build toolchain. Clone and open. Works immediately.
- No npm, no webpack, no node_modules. Nothing to break on a new machine.
- Consistent with the "runnable in under 30 minutes" QUICKSTART promise.

**Tradeoff:** A single 3,700-line file is harder to navigate than a componentized
React app. The tradeoff is deliberate — operational simplicity over developer
ergonomics at this scale.

**Would change for production:** React with component library for multi-user
Beta. The `ui_architecture.md` doc describes the target left-bar layout.

---

## What I Would Do Differently at Scale

- **Authentication:** The API has no auth. Fine for localhost; needs API key
  validation before any network exposure.
- **Observability:** LLM latency, retrieval score distributions, and refusal
  rates are the three most important things to instrument first.
- **Async ingestion:** Currently synchronous and blocking. Needs a queue-backed
  async pipeline at meaningful document volumes.
- **Vector store backup:** Qdrant storage (`~/qdrant_storage/`) is a derived
  artifact but expensive to regenerate. Treat it like a database — back it up.
  In production: S3-backed Qdrant snapshots on a schedule.

---

## 11. CrossEncoder Reranker: Two-Stage Retrieval

**Decision:** CrossEncoder `ms-marco-MiniLM-L-6-v2` as a reranking pass after
vector search, before prompt assembly.

**Why:**
The bi-encoder (nomic-embed-text) compresses query and chunk independently into
fixed vectors. Compression loses nuance — "AI governance committee" and "Firmwide
Artificial Intelligence Risk and Controls Committee" are semantically equivalent
but vector-distant. This is vocabulary mismatch.

The CrossEncoder reads query + chunk concatenated as a single input, with full
attention across both. It scores relevance directly rather than approximating
via cosine distance. Vocabulary mismatch largely disappears.

**Two-stage architecture:**
- Stage 1: Qdrant HNSW vector search — fast, retrieves top-K candidates
- Stage 2: CrossEncoder reranker — slower, reorders by true relevance

**Model selection: `ms-marco-MiniLM-L-6-v2`**
- 22M parameters, 90MB — loads in <1s on Apple Silicon
- Fine-tuned on MS MARCO (500K passage relevance pairs) — directly applicable
  to "rank these passages for this query"
- Best latency/quality tradeoff in the MiniLM family
- Knowledge-distilled from BERT-large — 6 transformer layers, preserves most
  quality at fraction of the depth

**Implementation:** `rag_core.py` — lazy load with graceful fallback if
`sentence-transformers` unavailable. Zero impact on existing behavior if
reranker fails to load.

**Tradeoff:** ~1-2s additional latency per query for CrossEncoder inference on
top-K candidates. Acceptable at current corpus sizes.

---

## 12. Atomic `--force` Ingest

**Decision:** `--force` flag in the ingest pipeline performs an atomic wipe of
Qdrant collection + JSONL index + manifest before re-ingesting.

**Why:**
Without atomic wipe, incremental upserts leave stale chunk IDs in Qdrant when
chunk format changes (e.g. switching from `::chunk-N` to `::page-N::chunk-M`
format). Old and new format chunks coexist, degrading retrieval quality.

**Implementation:** `pipeline.py` `ingest_corpus()` — when `force=True`:
1. Truncate `index.jsonl`, `manifest.jsonl`, `failures.jsonl`, `doc_chunk_map.json`
2. Call `qdrant_store.delete_collection()` — wipes Qdrant collection entirely
3. Re-ingest all files from scratch

`delete_collection()` added to `qdrant_store.py` for this purpose.

**Also used by:** `scripts/start.sh` auto-ingest on first run (without --force,
via collection existence check).
