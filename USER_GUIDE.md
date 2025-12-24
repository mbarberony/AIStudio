# AIStudio — Quick User Guide & Demo Script

AIStudio is a local-first AI engineering workspace for:
- **Corpus ingestion** (PDF/DOCX/XLSX/PPTX/TXT/MD → chunks)
- **Retrieval** via:
  - **Chroma + embeddings** (semantic search)
  - **JSONL lexical fallback** (keyword/token match)
- **Answering** via local LLMs (Ollama) using retrieved context
- **Debugging & observability** via `/debug/*` endpoints and corpus-level stats 

This guide is designed to be used as a quick reference *and* as a live demo script.

---
## Key Concepts

### Corpus
A named dataset you ingest and query, stored under:

`data/corpora/<corpus_name>/`

Each corpus maintains its own:
- `index.jsonl` — chunk store (debug artifact)
- `manifest.jsonl` — incremental ingest tracking
- `ingest_failures.jsonl` — parse failures
- `doc_chunk_map.json` — doc → chunk IDs mapping (used for stale chunk deletion)
- `chroma/` — Chroma persistence directory (if enabled)

### Manifest-based incremental ingestion
AIStudio skips unchanged files using `(mtime, size)` tracked in `manifest.jsonl`.
Use `--force` to reprocess anyway.

### Retrieval backends
- **Chroma** (semantic): embedding similarity search with optional distance filtering.
- **JSONL** (lexical): basic token containment scoring.

Default behavior: if Chroma returns nothing (or filtered out), AIStudio falls back to JSONL retrieval.

## Prerequisites

Make sure Ollama is installed and running:
```bash
ollama list
ollama pull nomic-embed-text
ollama pull llama3.2:3b
```
## Configuration (ENV overrides)
AIStudio loads a .env automatically (if your project is configured that way) and reads environment variables at startup.
Common overrides:

### Retrieval backend
```bash
export AISTUDIO_USE_CHROMA=true          # semantic retrieval
export AISTUDIO_USE_CHROMA=false         # JSONL lexical only
```
### Models
```bash
export AISTUDIO_DEFAULT_MODEL=llama3.2:3b
export AISTUDIO_DEFAULT_EMBED_MODEL=nomic-embed-text
```
### Retrieval tuning
```bash
export AISTUDIO_TOP_K=5
export AISTUDIO_MAX_DISTANCE=1.0         # lower = stricter, can filter out hits
```

### Embedding Batch Size 
```batch
export AISTUDIO_CHROMA_EMBED_BATCH_SIZE=32
```
After changing env vars, restart the API server.

---
## Demo Script (End-to-End)

### Step 1 — Ingest a corpus (fresh)
Pick a directory and a corpus name:
```bash
python -m local_llm_bot.app.ingest \
  --corpus job_search_02 \
  --root "/Users/<you>/Documents/AIStudio_Corpus" \
  --reset-index --reset-chroma \
  --use-chroma true \
  --embed-model nomic-embed-text
```
What to watch:
- A progress bar (if tqdm is installed).
- JSON output summary including counts and runtime.

### Step 2 — Ingest incrementally (fast rerun)
```bash
python -m local_llm_bot.app.ingest \
  --corpus job_search_02 \
  --root "/Users/<you>/Documents/AIStudio_Corpus"
```
### Step 3 — Start the API server
From repo root (with your venv activated):
```bash
uvicorn local_llm_bot.app.api:app --reload --port 8000
```
Open interactive docs:
```bash
http://127.0.0.1:8000/docs
```

### Step 4 — Check health
```bash
curl -s http://127.0.0.1:8000/health | python -m json.tool
```
### Step 5 — Inspect corpus stats
```bash
curl -s "http://127.0.0.1:8000/debug/stats?corpus=job_search_02" | python -m json.tool
```
This tells you:
- number of chunks
- number of docs
- failures count
- chroma dir location
- top sources by chunk count
- effective config
### Step 6 — Debug retrieval (what’s being returned)
```bash
curl -s -X POST "http://127.0.0.1:8000/debug/retrieve" \
  -H "Content-Type: application/json" \
  -d '{"query":"NORTHWESTERN", "top_k": 5, "corpus": "job_search_02"}' \
| python -m json.tool
```
If you see count=0:
- Try mixed case / different tokens
- Confirm the corpus has the term in JSONL (see Debugging section)
- Check if AISTUDIO_MAX_DISTANCE is filtering everything
### Step 7 — Ask a real question (RAG)
```bash
curl -s -X POST "http://127.0.0.1:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"query":"What did I do at Bridgewater and in what years?", "corpus":"job_search_02"}' \
| python -m json.tool
```
Expected output:
answer string

If documents are insufficient: “I don’t know based on the provided documents.”

---
## Debugging Playbook
### A) Verify the term exists in JSONL
```bash
grep -in "northwestern" "data/corpora/job_search_02/index.jsonl" | head
```
If grep finds it but /debug/retrieve returns no hits, the issue is usually:

- query tokenization differences
- top_k too low 
- you’re querying the wrong corpus 
- distance filtering in Chroma (if use_chroma is enabled)

### B) Confirm which backend is active

Use stats endpoint:
```bash
curl -s "http://127.0.0.1:8000/debug/stats?corpus=job_search_02" | python -m json.tool
```

Look at:

- config.use_chroma
- config.max_distance
- config.default_embed_model

### C) Disable distance filtering temporarily

If you suspect everything is filtered out:

export AISTUDIO_MAX_DISTANCE=
(empty/undefined means "off" if your config supports None)

Restart server and try again.

### D) Confirm Chroma has data

Chroma persistence exists here:
data/corpora/<corpus>/chroma/

If needed, reset and re-ingest:
```bash
python -m local_llm_bot.app.ingest \
  --corpus job_search_02 \
  --root "/Users/<you>/Documents/AIStudio_Corpus" \
  --reset-index --reset-chroma \
  --use-chroma true
```

### E) Common runtime issues

Port already in use
```bash
lsof -i :8000
kill -9 <PID>
```

Ollama not reachable

Check:

```bash
curl -s http://127.0.0.1:11434/api/tags
```

Ensure AISTUDIO_OLLAMA_BASE_URL matches.

---
# Handy Commands

```bash
Run tests
make test
```

Lint / format
```bash
make lint
make format
```

Show git status and push
```bash
git status
git add -A
git commit -m "Update corpus ingest and docs"
git push origin main
```


