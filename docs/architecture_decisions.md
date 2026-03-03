# Architecture Decisions

Key technical choices made in this project, with rationale. This document is intended for anyone reviewing the codebase who wants to understand not just what was built, but why.

---

## 1. Local-First Design (Ollama, No External API)

**Decision:** All LLM inference and embedding runs locally via Ollama. No OpenAI, Anthropic, or other cloud API dependency in the core stack.

**Why:**
- Forces genuine understanding of model behavior at the infrastructure level — latency, memory pressure, model selection tradeoffs
- Eliminates API cost as a variable during experimentation
- Relevant to financial services contexts where data residency and network egress are real constraints, not afterthoughts
- Makes the system runnable in air-gapped or restricted environments

**Tradeoff:** Inference quality is lower than frontier models. This is a deliberate constraint, not a limitation. The goal is substrate knowledge, not benchmark performance.

**Would change for production:** Add LiteLLM as a provider abstraction layer. Local inference for development and sensitive data; cloud inference (with appropriate data handling) for production quality. The architecture is designed to make this substitution straightforward — Ollama client is isolated in `ollama_client.py`.

---

## 2. Chroma as Vector Store

**Decision:** Chroma, running embedded (in-process), not as a separate service.

**Why:**
- Zero operational overhead for a personal lab — no separate process to manage, no network hop
- Persistent storage between runs without configuration
- Python-native, fits naturally into the FastAPI stack
- Sufficient for the document volumes in scope

**Tradeoff:** Doesn't scale horizontally. Single-process means no concurrent write safety at scale.

**Would change for production:** Pinecone or Weaviate for cloud-native deployment with horizontal scaling. Alternatively, pgvector if the deployment already has PostgreSQL — reduces operational surface area significantly. The vector store interface is abstracted in `vectorstore/chroma_store.py`, making substitution a contained change.

---

## 3. Embedding Model: `nomic-embed-text`

**Decision:** `nomic-embed-text` as the default embedding model.

**Why:**
- Best CPU performance among locally available models at time of selection — low latency without GPU
- Produces meaningful semantic representations for the document types in scope (resumes, technical docs, markdown)
- Passes the embedding arithmetic tests (King − Man + Woman = Queen), which is a practical signal of semantic quality

**Considered:** `bge-large-en` — approximately 5% quality improvement on retrieval benchmarks, but roughly 2x slower on CPU. The tradeoff didn't justify it for this use case.

**Would change for production:** Benchmark against the specific corpus and query patterns in scope. Embedding model selection is highly workload-dependent; the right choice for financial documents may differ from the right choice for code or legal text.

---

## 4. Citation Logic Embedded in API, Not Modularized

**Decision:** Citation extraction and formatting lives in `api.py` rather than as a separate module.

**Why:**
- Citation logic is tightly coupled to the response pipeline — it operates on the LLM output immediately before it's returned
- Separating it into a module adds indirection without architectural benefit at this scale
- Simpler deployment: one file to update, no import chain to maintain

**Tradeoff:** `api.py` is longer as a result. The citation functions (`generate_answer_with_citations`, `extract_page_number`) are clearly named and easy to locate.

**Would change for production:** With multiple citation formats (inline, footnote, structured JSON) or multiple output channels, a dedicated citation module with a clean interface would be worth the overhead.

---

## 5. Semantic Chunking Over Fixed-Size Chunking

**Decision:** `chunking_generic.py` uses boundary-aware semantic chunking. The previous implementation used fixed character counts.

**Why:**
- Fixed chunking fragments natural language units — a sentence split across two chunks degrades retrieval significantly
- Document structure carries semantic information: section headers, paragraph breaks, and sentence boundaries are meaningful signals
- Measured improvement: approximately 25–40% accuracy improvement on resume-style queries after switching

**Implementation:** Three-tier fallback — semantic boundary detection → sentence splitting → character fallback. Pre-built strategies for common document types (`for_resumes()`, `for_technical_docs()`).

**Tradeoff:** Chunks are variable-length, which creates some unpredictability in context window usage. Handled via explicit context window management in the retriever.

---

## 6. Page Number Tracking: Deferred

**Decision:** Page numbers are not tracked in citations at this time.

**Why:**
- The primary corpus in scope is resumes — 1–2 pages. Page attribution adds no meaningful value.
- Implementation requires reliable page boundary detection during ingestion, which varies significantly by document type (PDF pagination is reliable; Word documents are layout-dependent).
- The accuracy cost of getting page numbers wrong outweighs the benefit of showing them.

**Would add when:** Indexing long documents (contracts, research reports, regulatory filings) where page attribution genuinely aids verification.

---

## 7. Conversation Memory: Sliding Window of 10 Turns

**Decision:** The system maintains the last 10 conversation turns as context for follow-up questions.

**Why:**
- 10 turns covers most realistic conversational patterns without excessive context window consumption
- Stateless between sessions by design — no persistence layer required, no privacy surface area
- Simple to reason about and debug

**Tradeoff:** Long research sessions lose early context. For use cases requiring persistent memory across sessions, a vector-based memory store (storing conversation summaries as embeddings) would be more appropriate.

---

## 8. JSONL Baseline for Deterministic Testing

**Decision:** A JSONL retrieval path exists alongside the Chroma path, returning deterministic results without embedding inference.

**Why:**
- Embedding models are nondeterministic under some conditions and slow to run in CI
- Deterministic tests that don't depend on model inference are more reliable and much faster
- Allows testing the full API response pipeline without Ollama running

**Usage:** Set via config; the test suite uses the JSONL path by default. Production queries use Chroma.

---

## What I Would Do Differently at Scale

A few things that are acceptable for a personal lab but would need to change for a real deployment:

- **Authentication:** The API has no auth. Fine for localhost; needs at minimum API key validation before any network exposure.
- **Observability:** Structured logging exists but there's no metrics layer. LLM latency, retrieval score distributions, and refusal rates are the three most important things to instrument first.
- **Async ingestion:** Document ingestion is currently synchronous and blocking. At any meaningful document volume, this needs to move to a queue-backed async pipeline.
- **Vector store backup:** Chroma's embedded mode has no backup strategy. In production, the vector store is effectively a derived artifact (documents → embeddings), but regenerating it is expensive. Treat it like a database and back it up.
