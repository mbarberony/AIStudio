AIStudio
========

AIStudio is a modular AI engineering environment designed for exploring
local-first LLM workflows, retrieval-augmented generation (RAG),
agentic automation, observability, guardrails, and lightweight CI/CD practices.

It serves as a personal laboratory for experimenting with modern AI
architectures and engineering techniques in both local and cloud-ready contexts.


HIGH-LEVEL OVERVIEW
-------------------

User
  |
  v
HTTP Client / Web UI
  |
  v
FastAPI API  (/ask, /debug/*)
  |
  v
Retriever + Prompt Builder
  |
  +--> Vector Store (Chroma OR JSONL baseline)
  |
  +--> Embedding Model (Ollama embeddings)
  |
  v
LLM Runtime (Ollama)

In parallel:
- Ingestion pipeline processes documents into chunks
- Agentic workflows can call tools (RAG, file I/O, summarization)
- Observability and guardrails capture usage and enforce limits


CORE OBJECTIVES
---------------

- Build a local knowledge engine capable of answering questions over
  a private corpus using open-source LLMs and embeddings.
- Experiment with agentic AI: tool-using agents, multi-step workflows,
  planning, and controlled autonomy.
- Establish a “vibe-coding” workflow using PyCharm and conversational coding.
- Apply structured engineering discipline: CI/CD, tests, observability,
  reproducibility.
- Extend the system to AWS and Azure (Epic 2) to compare cloud-native
  and local architectures.


ARCHITECTURE (EPIC 1 – LOCAL AI STUDIO)
--------------------------------------

Local Knowledge Engine (RAG)
- Open-source LLMs via Ollama
- Embedding-based retrieval using Chroma
- Incremental ingestion pipeline for:
  PDF, Word, PowerPoint, Excel, Markdown, text
- FastAPI /ask endpoint
- Source-aware answers
- Refusal when context is insufficient
- Debug-friendly JSONL artifacts

Agentic Lab
- Isolated experimentation area for agent workflows
- Tools:
  - RAG queries
  - File I/O
  - Summarization and transformation
- Example workflows:
  - Detect → ingest → summarize new files
  - Multi-step assistants combining retrieval and transformation
- Execution traces and logs for inspection

Developer Experience (Vibe Coding)
- PyCharm-first workflow
- CLI-driven ingestion and diagnostics
- Clear separation between:
  - Debug artifacts
  - Production-style components
- Emphasis on clarity, inspectability, and reversibility


JSONL RAG BASELINE (DEBUG ARTIFACT)
----------------------------------

In addition to Chroma, AIStudio maintains a JSONL-based RAG baseline
used for debugging, testing, and deterministic behavior.

Artifacts:
- data/index.jsonl            : chunk store
- data/manifest.jsonl         : incremental ingestion tracking
- data/ingest_failures.jsonl  : parse failures
- data/doc_chunk_map.json     : mapping used to remove stale chunks

Ingest a corpus (incremental):
  python -m local_llm_bot.app.ingest --root "/path/to/corpus" --reset-index
  python -m local_llm_bot.app.ingest --root "/path/to/corpus"

Run API and inspect stats:
  uvicorn local_llm_bot.app.api:app --reload --port 8000
  curl http://127.0.0.1:8000/debug/stats


TESTING (JSONL BASELINE)
-----------------------

The JSONL baseline allows deterministic testing without embeddings.

Example test verifies that lexical retrieval finds expected hits
without requiring Chroma or Ollama embeddings.


REPOSITORY STRUCTURE
--------------------

Repo root
  ├── src/
  │   ├── local_llm_bot/
  │   │   ├── app/
  │   │   │   ├── api.py
  │   │   │   ├── rag_core.py
  │   │   │   ├── config.py
  │   │   │   ├── ollama_client.py
  │   │   │   ├── ingest/
  │   │   │   ├── vectorstore/
  │   │   │   └── utils/
  │   │   └── __init__.py
  │   └── agentic_lab/
  │       └── workflows, tools, logs, tests
  ├── data/
  │   ├── index.jsonl
  │   ├── manifest.jsonl
  │   ├── ingest_failures.jsonl
  │   ├── doc_chunk_map.json
  │   └── chroma/
  ├── tests/
  ├── infra/
  ├── cloud/
  └── .github/
  ├── .gitignore
  ├── LICENSE
  └── README.md

TODO:

├── infra/                 # CI/CD configs, Docker, scripts, utilities
│   ├── cicd/
│   ├── docker/
│   ├── scripts/
│   └── configs/
│
├── cloud/                 # Cloud extension (Epic 2 — AWS, Azure)
│   ├── aws/
│   ├── azure/
│   └── docs/
│
├── docs/                  # Architecture notes, diagrams, decisions, logs
│   ├── architecture_overview.md
│   ├── learning_log.md
│   ├── rag_bot_v1.md
│   └── agentic_lab_v1.md



CONFIGURATION (ENV + .ENV)
--------------------------

AIStudio reads configuration from environment variables at startup.
Variables can be set via shell exports or via a .env file (auto-loaded).

Examples:

  export AISTUDIO_USE_CHROMA=true
  export AISTUDIO_DEFAULT_MODEL=llama3.2:3b
  export AISTUDIO_DEFAULT_EMBED_MODEL=nomic-embed-text
  export AISTUDIO_TOP_K=5
  export AISTUDIO_MAX_DISTANCE=1.0
  export AISTUDIO_INGEST_CHUNK_SIZE=1200
  export AISTUDIO_INGEST_OVERLAP=200

Notes:
- AISTUDIO_MAX_DISTANCE controls retrieval strictness (lower is stricter).

- If you change env vars, restart the server to pick them up.
```bash
uvicorn local_llm_bot.app.api:app --reload --port 8000
````

WHAT COMES NEXT
---------------

Epic 1 (continuing):
- Corpus management (multiple named corpora)
- Include/exclude rules and safe defaults
- Guardrails (path allow-lists, redaction, refusal policies)
- Observability and usage metering
- Agent execution controls and dry-run modes

Epic 2:
- Cloud deployments (AWS and Azure)
- Managed vector stores
- Remote ingestion and indexing
- Cost and performance comparisons




