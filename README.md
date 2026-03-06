# AIStudio
![CI](https://github.com/mbarberony/AIStudio/actions/workflows/ci.yml/badge.svg)

> A hands-on AI engineering lab exploring production-relevant patterns 
> for LLM-enabled systems — local RAG, agentic workflows, observability, 
> and cloud-ready architecture.

---

## What This Does

AIStudio gives you a **private, local search engine over your own documents** — 
running entirely on your Mac, with no data leaving your machine and no external 
API dependency.

Point it at a folder of PDFs, Word docs, PowerPoints, or Markdown files. Ask 
questions in plain English. Get source-attributed answers drawn from your own 
content, not from the internet.

Under the hood: documents are chunked, embedded, and stored in a local vector 
database. Queries are matched by semantic similarity, assembled into a prompt, 
and answered by a locally-running LLM via Ollama — the full RAG pipeline, 
running offline.

**On performance:** the system runs on a current-generation MacBook Pro with 
Apple Silicon. In practice, inference latency and throughput are comparable to 
a mid-tier server from two years ago — sufficient for serious evaluation work, 
and a meaningful demonstration that local AI infrastructure is no longer just 
a toy. No GPU cluster required.

---

## About This Project

This is a personal engineering lab, not production software. I built it 
to stay hands-on with the stack I reason about professionally — and to 
develop informed opinions about what actually holds up under real 
operational constraints versus what looks good in a demo.

The work here directly informs how I think about AI architecture 
decisions: where RAG breaks down, how agentic workflows fail, what 
observability actually requires in an LLM system, and how local and 
cloud deployments differ in practice.

If you're reviewing this as part of evaluating my background: the goal 
isn't to show production-grade software. It's to show that I engage with 
these systems at the implementation level, not just the whiteboard level.

---

## On Agent Architecture

The current wave of managed agent platforms — Claude's computer use, 
OpenAI Operator, Microsoft Copilot Studio — abstracts away the 
implementation details. That's useful for adoption. It also means most 
people building on top of them don't understand what's happening 
underneath: how tool boundaries work, where context windows become a 
constraint, why agents fail on ambiguous inputs, and what observability 
you lose when orchestration is managed for you.

This lab was built specifically to work at that lower level — to 
understand the failure modes before relying on the abstractions. The 
agentic workflows here are deliberately constructed without managed 
platforms: explicit tool definitions, traced execution, documented 
failure cases.

The goal is substrate knowledge, not API consumption.

---

## What's Here

### Local Knowledge Engine (RAG)
- Embedding-based retrieval using Chroma vector store
- Open-source LLMs via Ollama — no external API dependency
- Incremental document ingestion: PDF, Word, PowerPoint, Excel, Markdown
- FastAPI `/ask` endpoint with source-aware answers
- JSONL baseline for deterministic testing without embeddings
- Explicit refusal behavior when context is insufficient

### Agentic Lab
- Tool-using agent workflows: RAG queries, file I/O, summarization
- DAG-based orchestration for multi-step pipelines
- Execution tracing and guardrail layers
- Documented failure modes — built to understand where autonomy 
  breaks down, not just where it works

### Engineering Discipline
- CI/CD via GitHub Actions
- Pre-commit hooks and code quality checks
- Reproducible setup via bootstrap script
- Separation between debug artifacts and production-style components

---

## Architecture

The diagram below shows the full intended architecture. **Solid nodes are 
deployed and running locally today.** Greyed nodes are planned extensions 
on the roadmap — primarily cloud deployment and provider abstraction.

```mermaid
flowchart TD
    U[User / HTTP Client]
    U --> API

    subgraph API["FastAPI — /ask  /debug/*  /health"]
        AV[Request validation]
        AS[Source attribution]
    end

    API --> RPB

    subgraph RPB["Retriever + Prompt Builder"]
        RH[Hybrid retrieval strategy]
        RC[Context window management]
        RR[Refusal when below threshold]
    end

    RPB --> C
    RPB --> J
    RPB --> O
    RPB -.->|planned| L

    C[(Chroma\nvector store)]
    J[(JSONL\nbaseline / deterministic testing)]
    O[Ollama\nembeddings + LLM inference\nlocal — no external API dependency\nmodel substitution via config]
    L[/"LiteLLM\nunified provider abstraction\nlocal + cloud models\n(planned)"/]

    subgraph AG["Agentic Layer"]
        DAG[DAG orchestrator] --> TR[tool registry]
        TR --> ET[execution tracer]
        ET --> GC[guardrail checks]
    end

    subgraph ING["Ingestion Pipeline"]
        IN[PDF · Word · PPT · Excel · Markdown] --> CH[chunker]
        CH --> EM[embedder]
        EM --> C
    end

    subgraph CLOUD["Cloud Deployment — AWS (planned)"]
        ECS[/"ECS container hosting"/]
        S3[/"S3-backed vector store"/]
        OBS[/"Observability dashboard"/]
    end

    API -.->|planned| CLOUD

    style L fill:#e0e0e0,stroke:#aaaaaa,color:#888888
    style CLOUD fill:#f5f5f5,stroke:#bbbbbb,color:#888888
    style ECS fill:#eeeeee,stroke:#cccccc,color:#999999
    style S3 fill:#eeeeee,stroke:#cccccc,color:#999999
    style OBS fill:#eeeeee,stroke:#cccccc,color:#999999
```

### What the diagram shows

**Currently deployed (local):**
- A FastAPI layer handles all inbound requests, with request validation and 
  source attribution built in
- The Retriever + Prompt Builder selects a retrieval strategy (dense vector, 
  JSONL baseline, or hybrid), manages context window budget, and enforces 
  refusal when retrieved context falls below a quality threshold
- Chroma provides persistent vector storage; the JSONL baseline enables 
  deterministic regression testing independent of embedding drift
- Ollama runs LLM inference and embedding generation entirely locally — 
  model substitution is config-driven, no code changes required
- The Ingestion Pipeline handles multi-format document parsing, semantic 
  chunking, and embedding into Chroma
- The Agentic Layer provides DAG-based orchestration with explicit tool 
  boundaries, execution tracing, and guardrail enforcement

**Planned extensions (greyed):**
- **LiteLLM** — unified abstraction layer enabling seamless switching between 
  local Ollama models and cloud providers (OpenAI, Anthropic, Bedrock) without 
  changing application code
- **AWS cloud deployment** — ECS-hosted containers with S3-backed vector store, 
  enabling cost and latency comparison against the local baseline
- **Observability dashboard** — aggregated metrics for retrieval quality, 
  latency distribution, and failure classification across sessions

---

## Why These Choices

See [Architecture Decisions](docs/architecture_decisions.md) for the 
reasoning behind key technical choices — vector store selection, 
local-first design, orchestration approach, and what I would change 
for a production deployment at scale.

---

## Point of View

For the broader strategic context behind this work — how agentic AI 
is evolving, where its current limitations actually lie, and what 
that means for financial services specifically — see:

**[Agentic AI in Financial Services: Some Reflections](docs/agentic_ai_pov.pdf)**

This document explores the transition from descriptive to generative 
to agentic AI, the practical constraints on autonomous systems today, 
and a framework for thinking about where AI adds durable value versus 
where human judgment remains irreplaceable. Written December 2025.

---

## Quickstart

See [QUICKSTART.md](QUICKSTART.md) to get a running `/ask` endpoint 
in under 10 minutes.

---

## Roadmap

**In progress**
- Corpus management with named corpora and include/exclude rules
- Guardrails: path allow-lists, redaction, refusal policies
- Usage metering and observability dashboard

**Planned**
- Cloud deployment on AWS (ECS + S3-backed vector store)
- Comparison of local vs. cloud latency and cost tradeoffs
- Multi-step agent demo with documented execution traces
- LiteLLM integration for unified provider abstraction

---

## Stack

Python · FastAPI · Ollama · Chroma · GitHub Actions · AWS
