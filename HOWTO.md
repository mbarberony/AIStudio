# HOWTO — AIStudio Operational Guide

Practical recipes for day-to-day AIStudio use.
Not a getting-started guide (see QUICKSTART.md) — reach for this when
something is behaving unexpectedly or you need to do something specific.

---

## Shell & Terminal

**zsh and special characters:**
Always use single quotes when echoing strings containing `!` or `$`:
```bash
echo '!data/corpora/demo/'        # correct
echo "!data/corpora/demo/"        # wrong — zsh interprets ! as history expansion
```

**Emptying a file safely:**
Use `truncate` instead of `>` — the redirect operator can leave your prompt
hanging in zsh if something goes wrong:
```bash
truncate -s 0 ~/Developer/AIStudio/data/corpora/demo/manifest.jsonl
```

**Don't paste comment lines:**
When copying multi-line commands, paste only the commands — not `#` comment
lines. zsh will try to execute them and produce `command not found` errors.

**PATH not updated in existing tabs:**
After adding something to `~/.zshrc`, run `source ~/.zshrc` in every open
terminal tab. New tabs pick up changes automatically; existing ones don't.

**Aliases not available after `source ~/.zshrc &&` chaining:**
zsh aliases defined during a `source` call are not available in the same `&&`
chain. Always run `source ~/.zshrc` on its own line first:
```bash
source ~/.zshrc   # must be its own line
ais_start         # then call the alias
```
Not: `source ~/.zshrc && ais_start` — this will fail with `command not found`.

---

## User Commands (ais_*)

After running `bash install.sh` from the repo root, these aliases are available
from any terminal:

| Command | What it does |
|---|---|
| `ais_start` | Start all services (Qdrant, Ollama, FastAPI, opens UI) |
| `ais_stop` | Stop all services |
| `ais_bench` | Run benchmark on demo corpus with default settings |
| `ais_sec_download` | Download SEC 10-K corpus from EDGAR (~500MB) |
| `ais_help` | Print user command reference |

Run `ais_help` at any time for a quick reminder.
Every `ais_*` command supports `--help` for usage details:
```bash
ais_start --help
ais_bench --help
```

**Promoting files from ~/Downloads to the repo:**
Always use `ais_deploy` — never bare `cp`. macOS appends `(N)` to duplicate
filenames (e.g. `rag_studio (1).html`), which breaks `cp` silently.
`ais_deploy` strips the suffix, finds the correct destination automatically,
and runs lint:
```bash
ais_deploy rag_studio.html
ais_deploy PIPELINE.md          # works for meta/ files too
ais_deploy api.py rag_studio.html   # multiple files in one shot
```

---

## FastAPI Backend

**Port already in use:**
```bash
kill $(lsof -ti:8000)
```
`lsof -ti:8000` returns the PID of whatever is using port 8000; `kill` sends
SIGTERM to it. Then restart with `ais_start`.

**Keep model warm between queries:**
Always start uvicorn with `OLLAMA_KEEP_ALIVE=30m`:
```bash
OLLAMA_KEEP_ALIVE=30m AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src \
  uvicorn local_llm_bot.app.api:app --reload --port 8000
```
Without this, the model unloads after each query and the next one takes 20–50s.

**Backend changes not reflected:**
uvicorn `--reload` watches for file changes. If changes still don't appear,
kill and restart:
```bash
kill $(lsof -ti:8000)
```

---

## Qdrant

**Qdrant persists across restarts:**
All collections and chunks are stored in `~/qdrant_storage/` on disk. When
you restart Qdrant or reboot your Mac, everything is restored automatically.
You do not need to re-ingest after a restart.

**Check collection chunk counts:**
```bash
curl -s http://localhost:6333/collections/aistudio_demo | python3 -m json.tool | grep points_count
curl -s http://localhost:6333/collections/aistudio_sec_10k | python3 -m json.tool | grep points_count
```

**Wipe and rebuild a collection:**
Use `--force` to atomically wipe Qdrant + JSONL artifacts and re-ingest clean:
```bash
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \
  --corpus demo --root data/corpora/demo/uploads --force
```

**List all collections:**
```bash
curl -s http://localhost:6333/collections | python3 -m json.tool
```

---

## Corpus Management

**Standard ingest command:**
```bash
cd ~/Developer/AIStudio && source .venv/bin/activate
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \
  --corpus <name> --root data/corpora/<name>/uploads
```

**Force re-ingest (wipes everything first):**
```bash
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \
  --corpus <name> --root data/corpora/<name>/uploads --force
```

**Recovering a deleted file:**
When you delete a file from a corpus via the UI, it moves to
`data/corpora/<name>/uploads/trash/` — it is NOT permanently deleted.
To restore it:
```bash
# See what's in trash
ls ~/Developer/AIStudio/data/corpora/<name>/uploads/trash/

# Move it back to uploads
mv ~/Developer/AIStudio/data/corpora/<name>/uploads/trash/<filename> \
   ~/Developer/AIStudio/data/corpora/<name>/uploads/

# Re-ingest to restore it to the vector store
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \
  --corpus <name> --root data/corpora/<name>/uploads --force
```

**Recovering a deleted corpus:**
When you delete an entire corpus via the UI, the folder moves to
`~/.Trash/AIStudio_<name>/`. To restore:
```bash
mv ~/.Trash/AIStudio_<name> ~/Developer/AIStudio/data/corpora/<name>
# Then re-ingest as above
```

**Ingest the SEC 10-K corpus:**
Download first using `ais_sec_download`, then:
```bash
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \
  --corpus sec_10k --root ~/Downloads/sec_10k_corpus --force
```
Allow ~34 minutes. Safe to run in background.

---

## Tests

**Default test run (unit tests only, no backend needed):**
```bash
make test
# or: ais_test
```
31 tests, runs in ~4 seconds. Integration tests are excluded by default.

**Integration tests (requires Qdrant + Ollama running):**
```bash
make test-integration
```
Runs tests marked `@pytest.mark.integration`. Start services first with `ais_start`.

**Why the split:** `test_retrieve_finds_hits_jsonl` requires a live Qdrant connection.
Marked `@pytest.mark.integration` so `make test` stays fast and offline-safe.

---

## Benchmark

```bash
cd ~/Developer/AIStudio && source .venv/bin/activate

# Demo corpus — 12 curated questions, YAML auto-detected
python3 benchmarks/benchmark.py --corpus demo --top-k 5 --temperature 0.3

# With specific model
python3 benchmarks/benchmark.py --corpus demo --top-k 5 --temperature 0.3 --model llama3.1:70b

# SEC 10-K corpus
python3 benchmarks/benchmark.py --corpus sec_10k --top-k 10 --temperature 0.3

# See all flags
python3 benchmarks/benchmark.py --help
```

Reports written to `benchmarks/reports/` as timestamped `.md` and `.json` pairs.

---

## Frontend / Browser

**Hard-refresh after HTML changes:**
After deploying `rag_studio.html`, always hard-refresh:
- **Chrome / Safari (macOS):** `Cmd+Shift+R`

A normal reload (`Cmd+R`) serves the cached version and changes won't appear.

**Open ↗ links open to page 1:**
Known Beta limitation — Chrome and Safari don't honor `#page=N` fragments for
proxied PDFs. The cited page number is correct and visible in the References
section. Full scroll-to-page requires pdfjs viewer (v2.0 roadmap).

---

## Git & Pre-commit

**Pre-commit ruff reformatting loop:**
When `git commit` triggers ruff and files are reformatted, the commit is
aborted. Re-stage the reformatted files and commit again:
```bash
git add <files>
git commit -m "your message"
```
Ruff modifies on the first pass, then passes on the second. This is by design.

---

For architecture context, see [docs/architecture_decisions.md](docs/architecture_decisions.md).
For getting started, see [QUICKSTART.md](QUICKSTART.md).
