# Dependencies

> AIStudio — what's installed, why, and what's deliberately not (yet).  
> This document is the narrative companion to `requirements.txt`.

---

## Design Philosophy

Dependencies are chosen conservatively. Every package in `requirements.txt` 
earns its place. Commented-out items are documented here as deliberate 
deferrals — not oversights — with notes on when and why they would be added.

This matters for a project whose purpose includes understanding the stack 
at the implementation level. Pulling in a framework that abstracts away 
the hard parts defeats the point.

---

## Core Web & API

### `fastapi`
The web framework powering all backend endpoints (`/ask`, `/corpus/create`, 
`/health`, etc). Chosen for three reasons: native async support, automatic 
OpenAPI documentation generation, and tight Pydantic integration that makes 
request/response validation nearly free. Every endpoint signature is also 
a schema definition.

### `uvicorn[standard]`
The ASGI server that runs FastAPI. FastAPI is the engine; uvicorn is the 
chassis. The `[standard]` extra pulls in `websockets` and `httptools` for 
faster HTTP parsing and WebSocket support. Run with `--reload` during 
development for automatic restart on file changes.

### `ollama`
Python client for the Ollama service running locally on port 11434. Used 
to send prompts to the LLM and receive streamed or batch responses. Ollama 
itself is not a Python package — it runs as a separate background service 
(`brew services start ollama`). This client is the bridge between the 
FastAPI backend and that service.

### `python-multipart`
Enables FastAPI to parse `multipart/form-data` — the encoding used by 
browsers and HTTP clients when uploading files. Without this package, any 
endpoint that accepts a file upload will silently fail with a 422 error. 
Required for the corpus file upload endpoint.

---

## Vector Store & Embeddings

### `chromadb`
The local vector database. Stores document chunks as embedding vectors 
and handles similarity search at query time. Runs in-process — no separate 
server, no Docker, no configuration. Data persists to disk in the 
`data/corpora/{corpus}/chroma/` directory.

Chroma was chosen over alternatives (Pinecone, Weaviate, Qdrant) 
specifically because it runs locally with zero infrastructure. For a 
cloud deployment, the abstraction layer makes swapping to a hosted vector 
store a configuration change rather than a rewrite.

### ~~`sentence-transformers`~~ *(deferred)*
Would provide an alternative embedding model running directly in Python 
(e.g. `all-MiniLM-L6-v2`). Currently deferred because embeddings are 
handled by `nomic-embed-text` via Ollama, which keeps the embedding and 
inference stacks unified under one service.

**When to add:** if you want to benchmark embedding quality across multiple 
models, or if you need embeddings without Ollama running.

### ~~`langchain`~~ *(deliberately excluded)*
A popular LLM orchestration framework that provides pre-built RAG 
pipelines, prompt templates, and agent tooling. Not used here by design.

AIStudio implements the retrieval pipeline, context assembly, citation 
extraction, and conversation memory directly. This is slower to build but 
produces genuine understanding of where RAG breaks down, how context 
windows become a constraint, and what observability you lose when 
orchestration is managed for you.

LangChain is the right choice for shipping a product quickly. It is the 
wrong choice for a project whose purpose is substrate knowledge.

**When to add:** if AIStudio ever becomes a platform others build on top 
of, LangChain compatibility (or LiteLLM) would be worth adding as an 
optional integration layer.

---

## Utilities

### `httpx`
Async HTTP client used internally for making requests to the Ollama REST 
API and any future external services. The `requests` library is the more 
common choice but is synchronous — in an async FastAPI application, 
`httpx` is the correct tool.

### `python-dotenv`
Loads environment variables from a `.env` file at startup. Used for 
configuration values (model name, Ollama port, data paths) that should 
not be hardcoded. Keeps secrets and environment-specific settings out of 
the codebase and out of git history.

### `pydantic`
Data validation and serialization library. Every request body, response 
schema, and config object in AIStudio is a Pydantic `BaseModel`. FastAPI 
uses Pydantic natively — defining an endpoint's input type is also 
defining its validation rules and its OpenAPI schema entry. One definition, 
three benefits.

---

## Progress / UX

### `tqdm`
Draws progress bars in the terminal during document ingestion. Without it, 
indexing a large corpus produces no output while it runs — you stare at a 
blank cursor and wonder if it crashed. With it, you see chunk-by-chunk 
progress and an ETA. Small quality-of-life improvement with zero 
architectural cost.

---

## Document Parsing

These four packages handle the ingestion pipeline's format support. Each 
reads a different file type and returns extractable text for chunking and 
embedding. Markdown requires no library — Python reads it as plain text.

### `pypdf`
Extracts text from PDF files. Handles multi-page documents, embedded fonts, 
and most standard PDF encodings. Does not handle scanned PDFs (image-only) 
— those would require OCR, which is a separate workstream.

**Future:** add `pytesseract` or `aws-textract` for scanned document support.

### `openpyxl`
Reads Excel files (`.xlsx` and `.xlsm`). Extracts cell values sheet by 
sheet. Does not handle legacy `.xls` format — add `xlrd` if that becomes 
necessary.

### `python-docx`
Reads Word documents (`.docx`). Extracts paragraph text, table contents, 
and heading structure. Does not handle legacy `.doc` format.

### `python-pptx`
Reads PowerPoint files (`.pptx`). Extracts slide text, speaker notes, and 
text boxes. Slide order is preserved in the extracted text.

---

## Development

These packages are used during development and testing only. They are not 
required to run AIStudio — a future split into `requirements.txt` and 
`requirements-dev.txt` would separate them.

### `pre-commit`
Runs configured code quality hooks automatically before every `git commit`. 
Currently configured to run `ruff` for linting. Catches formatting issues 
before they reach the repository. Run `pre-commit install` once after 
cloning to activate.

### `pytest`
The standard Python testing framework. Used for the embedding quality tests 
(`tests/test_embeddings.py`) and any future regression tests. Run with 
`pytest tests/` from the repo root.

### `ruff`
A fast Python linter and formatter written in Rust. Replaces three separate 
tools — `flake8` (linting), `black` (formatting), and `isort` (import 
sorting) — with one. Configured in `pyproject.toml`.

### `setuptools` / `wheel`
Python packaging utilities. Required for building AIStudio as an 
installable package. Not needed for running the development server, but 
will be essential for the v1.0 one-click installer (`.dmg`).

---

## Planned Additions

| Package | Purpose | Release |
|---|---|---|
| `litellm` | Unified abstraction for local + cloud LLMs (OpenAI, Anthropic, Bedrock) — swap providers via config, no code changes | v1.0 |
| `pytest-asyncio` | Async test support for testing FastAPI endpoints properly | Beta |
| `structlog` | Structured JSON logging for query traces, latency, and retrieval scores | Beta |
| `sentence-transformers` | Alternative embedding models for quality benchmarking | v1.0 |
