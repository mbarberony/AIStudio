**AIStudio** is a modular AI engineering environment designed for exploring local LLM workflows, retrieval-augmented generation (RAG), agentic automation, observability, guardrails, and lightweight CI/CD practices.  
It serves as a personal laboratory for experimenting with modern AI architectures and engineering techniques in both **local** and **cloud-ready** contexts.

---

## Core Objectives

- Develop a **local knowledge engine** capable of answering questions across a private corpus using open-source LLMs and embeddings.
- Experiment with **agentic AI**: tool-using agents, multi-step workflows, planning, and controlled autonomy.
- Establish a **vibe-coding workflow** using PyCharm and conversational coding patterns.
- Introduce **structured engineering discipline**: CI/CD, issue tracking, observability, and reproducibility.
- Extend the system to **AWS and Azure** (Epic 2) to compare cloud-native and local architectures.

---

## Architecture Overview (Epic 1 – Local AI Studio)

### **Local Knowledge Engine (RAG System)**
- Open-source LLMs via [Ollama](https://ollama.com/) or equivalent runtime.
- Vector store (e.g., Chroma) for embedding-based retrieval.
- Ingestion pipeline for PDFs, Markdown, and text documents.
- FastAPI `/ask` endpoint returning answers with source attribution.
- Usage logging for latency, query patterns, and model metadata.
- Initial guardrails (directory whitelisting, redaction patterns, output limits).

### **Agentic Lab**
- Framework experimentation (LangChain, LangGraph, AutoGen, CrewAI, etc.).
- Tools for RAG queries, file I/O, summarization, and structured content generation.
- Example workflows such as:
  - Detect → ingest → summarize new files
  - Multi-step assistants combining retrieval + transformation tasks
- Session logs for traceability and behavior inspection.

### **Developer Experience / Vibe Coding**
- PyCharm environment configured for conversational coding assistance.
- Run/debug configurations for ingestion, API services, and agent workflows.
- Documentation of engineering patterns, prompts, and workflow decisions.

### **CI/CD & Project Man**

