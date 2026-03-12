# Roadmap

> AIStudio — phased delivery plan
> Each release is a coherent, usable product. Nothing is a stepping stone
> to something else — every version ships real value.

---

## Release Philosophy

- **Alpha** — core RAG loop working end-to-end. Credible demo, usable by
  the builder. Suitable for sharing with technical reviewers.
- **Beta** — production-scale corpus, metadata filtering, conversation
  management, full corpus UI. Usable by a non-technical person who has
  been onboarded.
- **v1.0** — validated at scale, one-click install, automated tests.
  Suitable for open-source release.
- **v2.0** — multi-user, teams, shared corpora, cloud deployment.

---

## Alpha — Completed ✅

**Theme:** Core loop working. Demonstrate the concept.

- [x] Document ingestion (PDF, Word, PowerPoint, Excel, Markdown, HTML)
- [x] Embedding-based retrieval via Qdrant vector store (replaced ChromaDB)
- [x] RAG query with inline citations `[1][2]` and References section
- [x] Browser UI — corpus selector, model selector, query interface, corpus stats
- [x] FastAPI backend — `/ask`, `/health`, `/corpus/*`, `/debug/*` endpoints
- [x] Model selection via UI (any Ollama-hosted model)
- [x] `nomic-embed-text` embeddings (768 dimensions, cosine similarity)
- [x] `llama3.1:8b` and `llama3.1:70b` tested and benchmarked
- [x] End-to-end tested on M4 Max MacBook Pro 128GB
- [x] README, QUICKSTART, BENCHMARK_FINDINGS reflecting real install experience
- [x] Auto-launch script (`scripts/start.sh`) — starts all four processes
- [x] Benchmark harness (`scripts/benchmark.py`) — CLI flags, auto-generates findings
- [x] Metadata filtering — firm and year filters, backend + API + UI
- [x] 143 SEC 10-K corpus — 105,964 chunks, 34 min ingest, 54 chunks/sec, 0 failures
- [x] ChromaDB → Qdrant migration (Qdrant stable at 106K chunks; ChromaDB crashed at 32K)

---

## Beta — In Progress

**Theme:** Production-quality retrieval. Usable by others on their own documents.

### Retrieval Quality
- [ ] **Reranker** — CrossEncoder (ms-marco-MiniLM, ~90MB local). Two-stage
      retrieval: vector similarity → joint reranker scoring. Fixes vocabulary
      mismatch (e.g. "AI governance" ≠ "Artificial Intelligence Risk and Controls").
      Adds ~1–2s latency. High priority.
- [ ] **Relevance threshold** — discard chunks below minimum similarity score.
      Currently all top-K chunks passed to LLM context regardless of quality.
- [ ] **XBRL stripping** — SEC 10-K HTML files embed XBRL structured data tags
      that get chunked as noise. Strip `<ix:*>` tags in BeautifulSoup parser.
- [ ] **Embedding model eval** — nomic-embed-text vs bge-large (768 vs 1024 dims).

### Citation & Hallucination
- [ ] **Citation compliance hardening** — model sometimes answers without inline
      `[N]` markers despite system prompt. More pronounced on 8b than 70b.
      Stricter prompt engineering or 70b default for production.
- [ ] **Citation verification pass** — confirm cited source actually contains
      the claimed fact.

### Corpus UI
- [ ] Per-file removal from corpus
- [ ] Corpus delete via UI
- [ ] Corpus rename via UI
- [ ] Progress bar / ingestion completion notification
- [ ] Corpus dropdown auto-refresh when new corpus created while UI open
- [ ] Manifest deduplication — keep only latest entry per file
- [ ] `ingested_at` timestamp in manifest
- [ ] Re-ingest `demo` corpus into Qdrant (currently no Qdrant backing)

### Conversation
- [ ] Auto-save conversation after every exchange
- [ ] Restore conversation on page load
- [ ] Named conversation history (date-grouped)
- [ ] Export conversation as Markdown

### Engineering
- [ ] Rename `chroma_upserts` → `vector_upserts` in result JSON (cosmetic)
- [ ] Double message bug — verify resolved post-Qdrant migration
- [ ] `DEMO_CORPUS.md` excluded from retrieval results
- [ ] MacBook Air end-to-end validation

---

## v1.0 — Production Ready

**Theme:** Validated at scale, open-source ready.

### Crown Jewel Features
- [ ] **Page-aware chunking** — PDF ingest via pdfplumber, store `page=N`
      in Qdrant payload. Prerequisite for PDF viewer.
- [ ] **PDF viewer** — click citation `[N]` → open PDF, scroll to source page.
      The feature that turns demo into product.

### Scale & Quality
- [ ] Conversation memory validation — multi-turn testing at scale
- [ ] Hybrid retrieval (dense vector + BM25 keyword) configurable
- [ ] Quantization — consider for 300+ doc corpus
- [ ] Observability — similarity scores visible in UI per citation

### Benchmark & Tooling
- [ ] Config file support — benchmark defaults from `config/benchmark.yaml`.
      Pattern: file → env vars → CLI flags (CLI wins).
- [ ] Benchmark visual output — rich terminal display with colored pass/fail,
      latency bars, summary table (`rich` library).
- [ ] `--json` flag for machine-readable benchmark output (default: human-readable)
- [ ] `compare_runs.py` — diff two benchmark runs on latency and answer quality
- [ ] `--help` verified on all scripts

### Install & Launch
- [ ] One-click installer (.dmg for macOS)
- [ ] Menu bar / dock icon to start server and open UI
- [ ] No terminal required after initial setup
- [ ] Windows / Linux support

### Integrations
- [ ] LiteLLM integration — unified abstraction for local + cloud models
      (OpenAI, Anthropic, Bedrock) via single config change
- [ ] Multi-tenancy / API key auth — for sharing with team members

### Engineering
- [ ] Automated test suite with CI (GitHub Actions)
- [ ] Architecture Decision Records (ADRs)
- [ ] INSTALL.md — step-by-step for non-technical users / AI teams

---

## v2.0 — Multi-User & Cloud

**Theme:** Teams, shared corpora, cloud deployment.

- [ ] User accounts with roles (owner, admin, member, viewer)
- [ ] Shared corpora — team members query same indexed documents
- [ ] Cloud deployment — AWS ECS + S3-backed vector store
- [ ] REST API documented (OpenAPI spec)
- [ ] Mobile-friendly web UI
- [ ] MCP connectors — Gmail, Google Calendar, Slack, Notion

---

## Known Issues (Current)

| Issue | Severity | Fix |
|-------|----------|-----|
| XBRL noise in JPMorgan HTML chunks | Medium | Strip `<ix:*>` in BeautifulSoup |
| Northern Trust / Nuveen CIK collision | Medium | Deduplicate at download time |
| BNY Mellon CIK incorrect — 2007 only | Medium | Correct CIK in download script |
| Citation null on confident answers | Medium | Stricter prompt / 70b default |
| Corpus dropdown doesn't refresh | Low | JS event on corpus creation |
| Double message bug | Low | Verify post-migration |

---

## Dependency Map

```
Alpha ✅
  └── Beta (current)
        └── v1.0
              └── v2.0
```
