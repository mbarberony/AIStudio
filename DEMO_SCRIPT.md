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

- **Discover bar**: counts how many files are found under `--root` (fast scan).
- **Process bar**: advances when each supported file is actually parsed/chunked (you’ll see live counters: processed/skipped/failed/chunks).
- **Embed bar** (Chroma mode): tracks chunk embedding/upserts; if it’s slow, this bar makes it obvious you’re in the embedding phase.
- A final **JSON summary** is printed with counts (files/chunks), failures, and runtime.


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



