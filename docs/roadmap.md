# Roadmap

> AIStudio — phased delivery plan.
> This is a living document. Priorities shift based on deployment learnings,
> interview feedback, and what breaks in production. Manuel Barbero serves as
> both product owner and tech lead — decisions get made fast and the backlog
> reflects real-world constraints, not wishful thinking. Agile in practice,
> not in ceremony.

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

- [x] Document ingestion (PDF, Word, PowerPoint, Excel, Markdown, HTML)
- [x] Embedding-based retrieval via Qdrant vector store (replaced ChromaDB)
- [x] RAG query with inline citations and References section
- [x] Browser UI — corpus selector, model selector, query interface
- [x] FastAPI backend — /ask, /health, /corpus/*, /debug/* endpoints
- [x] nomic-embed-text embeddings (768 dimensions, cosine similarity)
- [x] llama3.1:8b and llama3.1:70b tested and benchmarked
- [x] Auto-launch script, benchmark harness, metadata filtering
- [x] 143 SEC 10-K corpus — 105,964 chunks, 34 min ingest, 54 chunks/sec, 0 failures
- [x] ChromaDB → Qdrant migration

---

## Beta — In Progress

### Recently Completed ✅
- [x] mistral:7b installed
- [x] sentence-transformers installed (reranker dependency ready)
- [x] CI/CD pipeline green (GitHub Actions)
- [x] Makefile — make check, make test-unit, make coverage
- [x] pre-commit hooks — ruff + ruff-format on every commit
- [x] CI badge in README
- [x] Conventional commits in practice
- [x] Coverage reporting (~26%)

### Retrieval Quality
- [ ] Reranker — CrossEncoder ms-marco-MiniLM — START HERE next session
- [ ] Relevance threshold
- [ ] XBRL stripping in HTML ingestion
- [ ] Embedding model eval: nomic-embed-text vs bge-large

### Citation & Hallucination
- [ ] Citation numbering carry-over fix
- [ ] Citation compliance — stricter prompt or 70b default
- [ ] Phantom citation numbers fix

### Corpus UI
- [ ] Per-file removal, corpus delete/rename
- [ ] Progress bar during ingest
- [ ] Corpus dropdown auto-refresh
- [ ] ingested_at timestamp in manifest

### Engineering
- [ ] OBE test — clean install in fresh directory (AFTER reranker)
- [ ] MacBook Air validation
- [ ] Swagger/OpenAPI — enable FastAPI auto-docs
- [ ] About modal in UI
- [ ] SDLC.md, HOW_TO.md
- [ ] CI dependency caching
- [ ] Mock/container for integration tests in CI

### Conversation
- [ ] Auto-save, restore on page load
- [ ] Named conversation history
- [ ] Export as Markdown

---

## v1.0 — Production Ready

- [ ] Page-aware chunking (pdfplumber, page=N in Qdrant payload)
- [ ] PDF viewer — click citation → scroll to source page
- [ ] PDF image identification and citation
- [ ] Respond with images (LLaVA via Ollama)
- [ ] Hybrid retrieval (dense + BM25)
- [ ] One-click installer (.dmg)
- [ ] Windows / Linux support
- [ ] uv migration
- [ ] LiteLLM integration
- [ ] Config file for benchmark, compare_runs.py, rich output
- [ ] Parallel CI jobs, semantic-release

---

## v2.0 — Multi-User & Cloud

- [ ] User accounts with roles
- [ ] Shared corpora
- [ ] AWS ECS Fargate + S3-backed Qdrant + ALB + CloudFront
- [ ] GPU inference (Inferentia2 or g4dn.xlarge)
- [ ] MCP connectors
- [ ] Compiled distribution (PyInstaller/Nuitka)

---

## Known Issues

| Issue | Severity | Fix |
|-------|----------|-----|
| Vocabulary mismatch (no reranker yet) | Critical | CrossEncoder — next commit |
| XBRL noise in HTML 10-K chunks | Medium | Strip ix:* tags |
| Northern Trust / Nuveen CIK collision | Medium | Deduplicate at download |
| BNY Mellon CIK incorrect | Medium | Correct CIK in script |
| Citation null on confident answers | Medium | Stricter prompt / 70b |
| Citation numbering carry-over | Medium | Reset counter per response |
| Corpus dropdown doesn't refresh | Low | JS event fix |
| Stats button wired to Upload listener | Low | Fix event binding |
| chroma/ created on new corpus init | Low | Remove stale mkdir |
