# Roadmap

> AIStudio / MBCrew — phased delivery plan  
> Each release is a coherent, usable product. Nothing is a stepping stone 
> to something else — every version ships real value.

---

## Release Philosophy

- **Alpha** — core RAG loop working end-to-end. Credible demo, usable by 
  the builder. Suitable for sharing with technical reviewers.
- **Beta** — conversation management, model switching, full corpus UI. 
  Usable by a non-technical person who has been onboarded.
- **v1.0** — validated at scale, one-click install, automated tests. 
  Suitable for open-source release and resume reference.
- **v2.0** — multi-user, teams, shared corpora, MCP integrations. 
  MBCrew / Stratum layer begins here.

---

## Alpha — Current

**Theme:** Core loop working. Demonstrate the concept.

### Done ✅
- Document ingestion (PDF, Word, PowerPoint, Excel, Markdown)
- Embedding-based retrieval via Chroma vector store
- RAG query with inline citations `[1][2]` and References section
- Browser UI — corpus selector, query interface, corpus stats inspector
- FastAPI backend — `/ask`, `/health`, `/corpus/*` endpoints
- Model selection via config (any Ollama-hosted model)
- `nomic-embed-text` embeddings, `llama3.1:70b` as default
- End-to-end tested on M4 Max MacBook Pro 128GB
- README and QUICKSTART reflecting real install experience
- Both repos synced to GitHub

### Remaining for Alpha ✅
- [ ] Fix `/corpus/create` endpoint (query param vs body mismatch)
- [ ] Fix auto re-index after file upload
- [ ] Add `ollama` and `python-multipart` to `requirements.txt`
- [ ] Remove or disable inoperative UI buttons (No Context, Debug, Clear)
- [ ] Commit `data_model.md`, `ui_architecture.md`, `roadmap.md` to repo

---

## Beta

**Theme:** Conversation management + full corpus UI. Usable by others.

### Conversation
- [ ] Auto-save conversation to `data/conversations/current.json` after 
      every exchange
- [ ] Restore conversation on page load (no lost work on refresh)
- [ ] `+ New Chat` button — archives current, starts fresh
- [ ] Named conversation history in Chat panel (date-grouped)
- [ ] Click past conversation to reopen
- [ ] Rename and delete conversations
- [ ] Export current conversation as Markdown

### Corpus UI
- [ ] Corpus detail view — file list, chunk count, last indexed timestamp
- [ ] Add files via native OS file picker (no drag-and-drop)
- [ ] Automatic re-index after file upload
- [ ] Remove individual files from corpus
- [ ] Delete corpus via UI
- [ ] Multi-corpus file membership (file belongs to multiple corpora)

### Models
- [ ] Model switcher in UI (currently config-only)
- [ ] Add model via UI (triggers `ollama pull` in backend)
- [ ] Show RAM usage per model (loaded vs on-disk)
- [ ] Pull progress indicator

### Chat
- [ ] Response time telemetry ("Research: 11.2s") in footer bar
- [ ] `+File` attachment to query (file sent as context, not indexed)
- [ ] Conversation title auto-generated from first query

### Engineering
- [ ] 10–20 file corpus validation
- [ ] Basic automated test suite (query regression, embedding quality)
- [ ] Logging — structured logs per query with latency, chunk scores, 
      token counts

---

## v1.0

**Theme:** Production-quality, open-source ready, resume-grade artifact.

### Scale & Quality
- [ ] 10–50 file corpus validated (latency, retrieval quality, edge cases)
- [ ] Hybrid retrieval (dense vector + keyword BM25) configurable
- [ ] Explicit refusal tuning — threshold calibration per corpus type
- [ ] Re-ranking layer (cross-encoder) for improved citation relevance

### Install & Launch
- [ ] One-click installer (.dmg for macOS)
- [ ] Menu bar / dock icon to start server and open UI
- [ ] No terminal required after initial setup
- [ ] Windows support (basic)

### Integrations
- [ ] LiteLLM integration — unified abstraction for local + cloud models
      (OpenAI, Anthropic, Bedrock) via single config change
- [ ] Web search toggle in UI (via LiteLLM or Brave Search API)
- [ ] Conversation search (full-text across all saved conversations)

### Observability
- [ ] Metrics panel — latency distribution, retrieval scores, token usage
- [ ] Query history export (CSV)
- [ ] Debug panel — raw prompt, retrieved chunks, token counts

### Engineering
- [ ] Automated test suite with CI (GitHub Actions)
- [ ] Architecture Decision Records (ADRs) for key choices
- [ ] Contribution guide (CONTRIBUTING.md)
- [ ] Open-source LICENSE file

---

## v2.0 — MBCrew / Stratum Layer

**Theme:** Multi-user orchestration. AIStudio becomes the substrate for 
a personal AI operating system.

### Multi-User Foundation
- [ ] User accounts with roles (owner, admin, member, viewer)
- [ ] Teams — named groups with member management
- [ ] Permission system — resource-level access control for corpora, 
      conversations, and models
- [ ] Shared corpora — team members query the same indexed documents
- [ ] Shared conversations — multiple participants in one thread
- [ ] Audit log — who queried what, when

### MBCrew / Stratum Agent Layer
- [ ] Agent entity — named thread with mandate, constraints, reporting cadence
- [ ] Chief of Staff (CoS) agent — maintains context graph across all threads
- [ ] StatePacket protocol — structured JSON state sync between agents and CoS
- [ ] Event-driven architecture — agents publish events, CoS subscribes
- [ ] Role-based prompting — system prompt per agent from structured template
- [ ] Multi-LLM routing — different agents can use different models

### Integrations
- [ ] MCP connectors — Gmail, Google Calendar, Slack, Notion
- [ ] GitHub integration — automated commit, issue creation from agent actions
- [ ] Crawbot / web agent integration
- [ ] REST API for external agent communication

### Client Architecture
- [ ] Client-server architecture (backend hosted, multiple frontends)
- [ ] Mobile-friendly web UI
- [ ] REST API documented (OpenAPI spec)
- [ ] SDK for building custom agents

---

## Cross-Cutting Concerns (All Releases)

### AIStudio ↔ MBCrew Synergy
Every architectural decision in AIStudio is evaluated for reusability 
in the MBCrew/Stratum layer:

| AIStudio Component | MBCrew Reuse |
|---|---|
| LLM abstraction (Ollama + LiteLLM) | Agent LLM routing |
| Conversation JSON schema | Agent thread / StatePacket schema |
| Multi-model support | Per-agent model assignment |
| Corpus / RAG | Agent long-term memory |
| FastAPI backend | Agent API endpoints |
| Auth / users / teams | MBCrew team structure |
| Observability | Agent state transition logging |

### Resume Narrative
The arc is deliberate:

1. **AIStudio Alpha** — hands-on RAG, local LLM infrastructure, production patterns
2. **AIStudio v1.0** — validated at scale, open-source, installer
3. **MBCrew v2.0** — multi-agent orchestration, event-driven, role-based prompting
4. **Self-referential** — used the tools being built to manage the job search 
   that required the tools in the first place

---

## Dependency Map

```
Alpha (now)
  └── Beta
        └── v1.0
              └── v2.0 (MBCrew layer)
                    └── Stratum (open-source / commercial)
```

Each layer is independently useful. None is a dead end.
