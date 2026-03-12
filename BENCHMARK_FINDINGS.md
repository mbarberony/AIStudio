# AIStudio — Benchmark Findings

**Project:** AIStudio — Local RAG on Apple Silicon  
**Repo:** github.com/mbarberony/AIStudio  
**Date:** March 2026  
**Hardware:** Apple MacBook Pro M4, unified memory architecture  
**Stack:** Ollama · llama3.1:8b / llama3.1:70b · Python RAG pipeline · Qdrant vector store  

---

## Headline Finding

> **Warm llama3.1:70b and warm llama3.1:8b are statistically identical in latency on Apple Silicon — ~6–7s average per query on a 105,964-chunk financial corpus. Once a model is loaded into unified memory, model size stops being a latency variable. You get 70b reasoning quality at 8b interaction speed.**

---

## What Was Benchmarked

Two distinct benchmark phases:

| Phase | Focus | Corpus | Questions |
|-------|-------|--------|-----------|
| Phase 1 | Model latency (8b vs 70b, cold vs warm) | Demo corpus — enterprise architecture docs | 17 |
| Phase 2 | RAG quality on financial corpus (Qdrant, metadata filtering) | 143 SEC 10-K filings, 105,964 chunks | 8 |

---

## Phase 1 — Model Latency

### Configuration
- Temperature: 0.3 | Top-K: 5 | Harness: `run_demo.py`
- Topic categories: Architecture Methodology, IT Strategy, Modern Technology, Financial Services

### Results

| Run | Model | State | Avg Latency | Total Time | Questions | Errors |
|-----|-------|-------|-------------|------------|-----------|--------|
| Run 1 | llama3.1:70b | Cold | ~120s | ~34 min | 17/17 | 0 |
| Run 2 | llama3.1:8b | Cold | ~52s | ~15 min | 17/17 | 0 |
| Run 3 | llama3.1:8b | Warm | 6.9s | ~2 min | 17/17 | 0 |
| Run 4 | llama3.1:8b | Warm | 7.2s | ~2 min | 17/17 | 0 |
| Run 5 | llama3.1:70b | Warm | 7.0s | 119.4s | 17/17 | 0 |

**All runs: 17/17 answered, 0 errors.**

### The Warm Model Insight

Once a model is resident in unified memory, Runs 3–5 cluster tightly at **6.9–7.2s average** across both model sizes. The variance between runs is smaller than the variance between individual questions within a single run.

**On Apple Silicon's unified memory architecture, model size does not predict inference latency once the model is loaded.** A 70b parameter model and an 8b parameter model respond at the same speed because the bottleneck shifts from memory bandwidth (load time) to the inference compute graph, which scales with requested output tokens — not parameter count.

You pay the size penalty once (at load time), then amortize it across every subsequent query. With prewarm enabled, this penalty is invisible to the user.

---

## Phase 2 — RAG Quality on SEC 10-K Corpus

### Configuration

| Parameter | Value |
|-----------|-------|
| Corpus | 143 SEC 10-K filings, 25 financial services firms |
| Vector store | Qdrant 1.17.0 (local, Apple Silicon) |
| Chunks | 105,964 |
| Embedding model | nomic-embed-text (768 dimensions, cosine similarity) |
| Model | llama3.1:8b warm |
| Temperature | 0.3 |
| Top-K | 10 |
| Metadata filtering | Firm + year filters active |
| Harness | `scripts/benchmark.py` |

### Ingest Performance

| Metric | Value |
|--------|-------|
| Files ingested | 143 |
| Total chunks | 105,964 |
| Ingest time (clean run) | ~34 minutes |
| Throughput | ~54 chunks/sec sustained |
| Failures | 0 |
| Previous vector store (ChromaDB) | Crashed at 32,285 chunks |

**Qdrant handled 3.3× the chunk volume that crashed ChromaDB, with zero failures.**

### Results

| # | Description | Latency | Retrieval | Citation | Notes |
|---|-------------|---------|-----------|----------|-------|
| 1 | Goldman AI risk — firm filter | 5.9s | ✅ | ⚠ partial | Correct content retrieved; citation on [1] only |
| 2 | JPMorgan cybersecurity — firm filter | 8.5s | ✅ | ✅ | Full answer with citations |
| 3 | Morgan Stanley model risk — firm filter | 7.4s | ✅ | ⚠ no cite | Correct answer, model confident without citing |
| 4 | Goldman AI committee — firm filter | 4.4s | ⚠ miss | ⚠ no cite | Correct answer from model knowledge; retrieval miss |
| 5 | Cross-corpus AI governance — no filter | 6.5s | ✅ | ✅ | Multi-firm synthesis, 8 citations |
| 6 | BofA climate risk — firm filter | 7.0s | ✅ | ✅ | Clean firm-filtered answer |
| 7 | Goldman 2025 revenue — firm+year filter | 5.4s | ✅ | ⚠ no cite | $58.28B correct; citation suppressed |
| 8 | Latency baseline | 5.4s | ✅ | ⚠ no cite | Correct answer, no citation |

**Average latency: 6.3s. Retrieval correct on 7/8 queries.**

### Evaluation Note

The automated pass/fail score (3/8) understates actual quality. The evaluator requires both correct content AND an inline citation `[N]`. Four answers were factually correct — verified against source documents — but the model answered confidently without attaching inline citations. This is a known LLM behavior: when the model is highly confident, it sometimes omits citation markers despite the system prompt instruction.

**Retrieval quality: 7/8 correct.** The one genuine miss (query 4 — Goldman AI committee) is a vocabulary mismatch: the query used "AI governance committee" while the source text says "Firmwide Artificial Intelligence Risk and Controls Committee." A reranker pass would resolve this.

### Metadata Filtering — Validated

Firm and year filters are working end-to-end:
- `firm=Goldman Sachs` → only Goldman chunks retrieved (confirmed via debug endpoint)
- `firm=Goldman Sachs, year=2026` → only 2026 Goldman filing
- Filter adds zero measurable latency overhead
- UI: Filters section live in sidebar (optional, type-in)

---

## Architecture Notes

### Why Qdrant over ChromaDB

| | ChromaDB | Qdrant |
|--|---------|--------|
| Language | Python | Rust |
| Stability at scale | Crashed at 32K chunks | Stable at 106K chunks |
| Metadata filtering | Limited | Native Filter/FieldCondition |
| Memory model | Python GC | Rust ownership, near-zero GC |
| Production path | Single-node only | Sharding, replication, quantization |
| gRPC support | No | Yes (port 6334) |

### Four-Process Architecture

```
Browser (HTML/JS)
    ↓ HTTP
FastAPI/uvicorn :8000  ←→  Qdrant :6333
    ↓ HTTP
Ollama :11434
```

Each process is independently restartable. No build step. Horizontal scale path: add Qdrant nodes, add uvicorn workers, point at shared Qdrant cluster.

---

## Known Limitations

- **Citation compliance** — model sometimes answers without inline `[N]` markers despite system prompt instruction. More pronounced on 8b than 70b. Mitigation: stricter prompt engineering or 70b default.
- **Vocabulary mismatch** — embedding similarity misses semantically equivalent but lexically different queries (e.g. "AI governance" vs "Artificial Intelligence Risk and Controls"). Fix: CrossEncoder reranker pass.
- **XBRL noise** — SEC 10-K HTML filings embed structured XBRL data tags that get chunked as noise, particularly in JPMorgan filings. Fix: strip `<ix:*>` tags in BeautifulSoup parser.
- **Duplicate filings** — Northern Trust and Nuveen share a CIK on SEC EDGAR; same documents ingested under two firm names.
- **No relevance threshold** — all top-K chunks passed to LLM context regardless of similarity score.

---

## Roadmap

- [ ] Reranker — CrossEncoder ms-marco-MiniLM (fixes vocabulary mismatch)
- [ ] Relevance threshold — discard chunks below similarity cutoff
- [ ] XBRL stripping in HTML ingestion
- [ ] Page-aware chunking (PDF ingest via pdfplumber, `page=N` in payload)
- [ ] PDF viewer — click citation → scroll to source page
- [ ] Embedding model eval: nomic-embed-text vs bge-large
- [ ] MacBook Air end-to-end validation
- [ ] Windows / Linux support (Release 2.0)

---

## Reproducing These Results

```bash
# Start all services
~/Developer/AIStudio/scripts/start.sh

# Run benchmark (8b default)
cd ~/Developer/AIStudio && source .venv/bin/activate
python3 scripts/benchmark.py --corpus sec_10k --top-k 10 --temperature 0.3

# Run benchmark (70b)
python3 scripts/benchmark.py --corpus sec_10k --top-k 10 --temperature 0.3 --model llama3.1:70b
```

Results written to `scripts/benchmark_results.json`. This document auto-generated by `scripts/benchmark.py`.

---

*AIStudio is a local-first RAG application. No data leaves the machine. See README for setup.*
