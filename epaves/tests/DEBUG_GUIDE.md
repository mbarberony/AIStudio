
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


