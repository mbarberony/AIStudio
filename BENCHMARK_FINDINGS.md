# AIStudio Benchmark Findings

**Project:** AIStudio — Local RAG on Apple Silicon  
**Repo:** github.com/mbarberony/AIStudio  
**Date:** March 2026  
**Hardware:** Apple Silicon (MacBook Pro, unified memory architecture)  
**Stack:** Ollama · llama3.1:8b / llama3.1:70b · Python RAG pipeline · FAISS vector store  

---

## Headline Finding

> **Warm llama3.1:70b and warm llama3.1:8b are statistically identical in latency on Apple Silicon — ~7s average per query. Once a model is loaded into unified memory, model size stops being a latency variable. You get 70b reasoning quality at 8b interaction speed.**

---

## Benchmark Configuration

| Parameter | Value |
|---|---|
| Corpus | Demo corpus (enterprise architecture / IT strategy documents) |
| Questions | 17 questions across 4 topic categories |
| Temperature | 0.3 |
| Top-k retrieval | 5 chunks |
| Harness | `run_demo.py` — automated, timed, logged |

**Topic categories:**
- Architecture Methodology (4 questions)
- IT Strategy & Leadership (4 questions)
- Modern Technology (5 questions)
- Financial Services (4 questions)

---

## Results Summary

| Run | Model | State | Avg Latency | Total Time | Questions | Errors |
|---|---|---|---|---|---|---|
| Run 1 | llama3.1:70b | Cold, early codebase | ~120s | ~34 min | 17/17 | 0 |
| Run 2 | llama3.1:8b | Cold | ~52s | ~15 min | 17/17 | 0 |
| Run 3 | llama3.1:8b | Warm | 6.9s | ~2 min | 17/17 | 0 |
| Run 4 | llama3.1:8b | Warm | 7.2s | ~2 min | 17/17 | 0 |
| Run 5 | llama3.1:70b | Warm | 7.0s | 119.4s | 17/17 | 0 |

**All runs: 17/17 questions answered, 0 errors.**

---

## Run 5 — Detail (70b Warm, Current Codebase)

```
[1/17]  Architecture Methodology: What is QFD and how does it apply...     ✓  10.1s
[2/17]  Architecture Methodology: How do you design an IT organization...   ✓   7.3s
[3/17]  Architecture Methodology: What are the core concepts of EA...       ✓   7.5s
[4/17]  Architecture Methodology: How do architecture concepts help...      ✓   5.5s
[5/17]  IT Strategy & Leadership: How should a CTO prioritize a 3-year...   ✓   5.0s
[6/17]  IT Strategy & Leadership: What does a good technology target...     ✓   4.5s
[7/17]  IT Strategy & Leadership: How do you organize a large-scale...      ✓   7.3s
[8/17]  IT Strategy & Leadership: What is the relationship between...       ✓   5.9s
[9/17]  Modern Technology: What does a reference architecture for...        ✓   9.0s
[10/17] Modern Technology: What are the key considerations for cloud...     ✓   9.6s
[11/17] Modern Technology: What is the role of data strategy in...         ✓   5.0s
[12/17] Modern Technology: How does DevOps change IT operations...         ✓  10.5s
[13/17] Modern Technology: What are the key principles for modernizing...   ✓   7.8s
[14/17] Financial Services: What are the key risk and compliance...        ✓   8.0s
[15/17] Financial Services: How has digitization changed financial...      ✓   6.5s
[16/17] Financial Services: What are the infrastructure considerations...   ✓   5.2s
[17/17] Financial Services: What is the role of architecture in managing... ✓   4.9s

Total: 119.4s
```

---

## Analysis

### The Cold Start Problem (Runs 1–2)

Runs 1 and 2 exposed the expected cold-start penalty: when Ollama loads a model from disk into unified memory, latency is dominated by the load time, not the inference time. At 120s avg, Run 1 (cold 70b) is effectively unusable for interactive use — and at 52s avg, cold 8b isn't much better.

These numbers also reflect an early-stage codebase; the RAG pipeline, chunking, and retrieval layer have been significantly improved since Run 1.

### The Warm Model Insight (Runs 3–5)

Once a model is resident in unified memory, the picture changes completely. Runs 3, 4, and 5 — across both model sizes — cluster tightly at **6.9–7.2s average**. The variance between runs is smaller than the variance between individual questions within a single run.

This is the architecturally interesting result: **on Apple Silicon's unified memory architecture, model size does not predict inference latency once the model is loaded.** A 70b parameter model and an 8b parameter model respond at the same speed because the bottleneck shifts from memory bandwidth (load time) to the inference compute graph, which scales with the requested output tokens — not the model's parameter count.

Practically: you pay the size penalty once (at load time), then amortize it across every subsequent query. For a running application with prewarm, this penalty is invisible to the user.

### Warm 8b vs. Warm 70b — Is There a Quality Difference?

Latency is indistinguishable. Quality differences exist but are task-dependent. For retrieval-augmented generation — where the model is grounding its answer in retrieved chunks rather than recalling from weights — the performance gap between 8b and 70b narrows significantly compared to open-ended generation tasks. For RAG on structured professional content, 8b warm is the practical default recommendation; 70b warm is available at zero latency cost for queries where reasoning depth matters.

---

## Practical Implications

**For local development and demos:**  
Run with prewarm enabled. `OLLAMA_KEEP_ALIVE=30m` in the startup environment prevents model eviction between queries. First-query latency is then indistinguishable from steady-state latency.

**For model selection:**  
`llama3.1:8b` is the recommended default — faster to load on cold start, identical warm performance, lower memory footprint. `llama3.1:70b` is available for higher-stakes queries with no interactive latency penalty once warm.

**For production architecture:**  
The prewarm pattern (fire a silent background request on corpus select) eliminates the cold-start UX problem entirely. Combined with keep-alive, users never observe the load penalty. This is the appropriate production default.

---

## Benchmark Harness

Results are reproducible. To replicate:

```bash
# Prewarm model
curl -s http://localhost:11434/api/generate \
  -d '{"model":"llama3.1:8b","prompt":"hi","stream":false}' > /dev/null && echo "Model warm"

# Run benchmark (8b default)
cd ~/Developer/AIStudio && source .venv/bin/activate
python run_demo.py

# Run benchmark (70b)
python run_demo.py --model llama3.1:70b
```

Reports are written to `data/demo/reports/` as timestamped markdown files.

---

*AIStudio is a local-first RAG application. See the repo README for full setup and architecture documentation.*
