# DEBUG_HINTS.md — AIStudio Debugging Playbook

Common issues and how to fix them. Written from real debugging sessions.

---

## Process Health

### Check all 4 processes are running

```bash
curl -s http://localhost:8000/health | python3 -m json.tool  # FastAPI
curl -s http://localhost:6333/healthz                         # Qdrant
curl -s http://localhost:11434/api/tags | python3 -m json.tool  # Ollama
```

### UI shows "Failed to fetch"

FastAPI backend is down. Restart it:

```bash
kill $(lsof -ti:8000)
cd ~/Developer/AIStudio && source .venv/bin/activate
OLLAMA_KEEP_ALIVE=30m AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
  uvicorn local_llm_bot.app.api:app --reload --port 8000
```

### Port already in use

```bash
lsof -i :8000   # find the PID
kill -9 <PID>
```

---

## Retrieval Issues

### Query returns no results / wrong results

1. Check the corpus has chunks in Qdrant:
```bash
curl -s http://localhost:6333/collections/aistudio_sec_10k | python3 -m json.tool
# Look for: "points_count"
```

2. Use the debug endpoint to inspect what's actually being retrieved:
```bash
curl -s -X POST http://localhost:8000/debug/retrieve \
  -H 'Content-Type: application/json' \
  -d '{"query": "your query here", "corpus": "sec_10k", "top_k": 5}' \
  | python3 -m json.tool
```

3. Check scores — if all scores are very low (< 0.3), the query may not
   match the corpus vocabulary. Try rephrasing or use the firm filter.

### Single-firm query returning wrong firms

Always set the firm filter for firm-specific questions:
- UI: type firm name in the Firm field (e.g. `Goldman Sachs`)
- API: add `"firm": "Goldman Sachs"` to the request body

Without the filter, vector similarity may return chunks from other firms
that happen to discuss similar topics.

### "AI governance" query not finding Goldman AI committee

Known vocabulary mismatch — the query "AI governance" doesn't vector-match
"Firmwide Artificial Intelligence Risk and Controls Committee" at the
embedding layer. Fix: CrossEncoder reranker (Beta roadmap item).

Workaround: use a more specific query —
*"Firmwide Artificial Intelligence Risk committee Goldman Sachs"*

---

## Ingestion Issues

### Ingest appears to complete but chunks = 0

The embed step may have been skipped. Check the ingest output for the
`Embed:` progress bar — if it's missing, the vectorstore flag wasn't set:

```bash
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \
  --corpus my_corpus --root /path/to/docs
```

The `AISTUDIO_VECTORSTORE=qdrant` env var is required. Without it, the
system falls back to ChromaDB mode and embeddings are skipped.

### Re-ingest a corpus (force refresh)

```bash
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \
  --corpus my_corpus --root /path/to/docs --force
```

`--force` reprocesses all files even if unchanged (based on mtime/hash).

### Ingest is slow

Expected throughput: ~54 chunks/sec on M4. For 143 files / 106K chunks:
~34 minutes. This is normal. Ollama must be running for embeddings.

---

## Model Issues

### ModuleNotFoundError

Always run with `PYTHONPATH=src`:
```bash
PYTHONPATH=src uvicorn local_llm_bot.app.api:app ...
```

Or use the auto-launch script which sets this automatically:
```bash
~/Developer/AIStudio/scripts/start.sh
```

### Ollama not reachable

```bash
curl -s http://localhost:11434/api/tags
```

If this fails, start Ollama:
```bash
brew services start ollama
# or
ollama serve
```

If you see "address already in use" — Ollama is already running. Correct state.

### Model responding slowly (cold start)

First query after startup is slow (20-120s) because the model loads into
memory. Subsequent queries are ~6-7s. Use the prewarm endpoint to load
the model before the first user query:

```bash
curl -s -X POST http://localhost:8000/prewarm \
  -H 'Content-Type: application/json' \
  -d '{"model": "llama3.1:70b"}'
```

---

## Common pip / Package Mistakes

### `pip3` vs `pip` inside venv

Inside `.venv`, always use `pip` (not `pip3`) or call directly:
```bash
.venv/bin/pip install package-name
```

`pip3` may install to the system Python, not your venv.

### Installing packages on macOS Python 3.13

Always add `--break-system-packages`:
```bash
pip install package-name --break-system-packages
```

macOS marks system Python as "externally managed" — this flag is required
even inside a venv on Python 3.13.

### Package not found via brew

Qdrant is NOT in Homebrew. Install via binary:
```bash
curl -L https://github.com/qdrant/qdrant/releases/latest/download/qdrant-aarch64-apple-darwin.tar.gz | tar xz
mkdir -p ~/bin && mv qdrant ~/bin/qdrant
```

---

## Git / CI

### CI failing with "ModuleNotFoundError: No module named 'local_llm_bot'"

`PYTHONPATH=src` must be set in the CI environment. Check
`.github/workflows/ci.yml` has:
```yaml
env:
  PYTHONPATH: src
```

### Commits not showing on GitHub contribution graph

Git email must match your primary verified GitHub email:
```bash
git config user.email                    # check current
git config --global user.email "your-github-email"  # fix
```

### Ruff lint failures in CI

Run locally first:
```bash
make check
```

This runs ruff + unit tests in the same order as CI. Fix all issues before
pushing. Pre-commit hooks will also catch ruff issues at commit time.
