# HOW_TO — AIStudio Operational Guide

Practical recipes and lessons learned for day-to-day AIStudio use.
This is not a getting-started guide (see QUICKSTART.md) — it's the reference
you reach for when something is behaving unexpectedly or you need to do
something specific.

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
When copying multi-line commands, paste only the commands — not `#` comment lines.
zsh will try to execute them and produce `command not found` errors.

**PATH not updated in existing tabs:**
After adding something to `~/.zshrc`, run `source ~/.zshrc` in every open
terminal tab. New tabs pick up changes automatically; existing ones don't.

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

**Committing gitignored files:**
To force-add a file that's in `.gitignore`:
```bash
git add -f data/corpora/demo/index.jsonl
```

**Un-ignoring a path in .gitignore:**
Use `!` negation (must be in single quotes in zsh):
```bash
echo '!data/corpora/demo/uploads/' >> .gitignore
```

---

## FastAPI Backend

**Port already in use:**
```bash
kill $(lsof -ti:8000)
```
Then restart normally. `lsof -ti:8000` returns the PID of whatever is using
port 8000; `kill` sends SIGTERM to it.

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

**Ingest the SEC 10-K corpus:**
Files live at `~/Downloads/sec_10k_corpus/` (not in repo — ~500MB).
Download them first using `scripts/download_sec_corpus.py`, then:
```bash
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \
  --corpus sec_10k --root ~/Downloads/sec_10k_corpus --force
```
Allow ~34 minutes. Safe to run in background.

---

## Benchmark

```bash
cd ~/Developer/AIStudio && source .venv/bin/activate

# Demo corpus — 12 curated questions, YAML auto-detected
python3 scripts/benchmark.py --corpus demo --top-k 5 --temperature 0.3

# With specific model
python3 scripts/benchmark.py --corpus demo --top-k 5 --temperature 0.3 --model llama3.1:70b

# SEC 10-K corpus
python3 scripts/benchmark.py --corpus sec_10k --top-k 10 --temperature 0.3

# See all flags
python3 scripts/benchmark.py --help
```

Results written to `scripts/benchmark_results.json` and `scripts/BENCHMARK_FINDINGS.md`.

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

## Deploy Script

```bash
~/Developer/AIStudio/scripts/deploy_files.sh <file1> [file2] ...
```

Copies files from `~/Downloads/` to their correct repo location, runs lint,
shows git status. Run with no arguments to see all known file mappings.

**Updating deploy_files.sh itself:**
The script cannot install itself. Manual process:
```bash
rm ~/Downloads/deploy_files.sh          # remove old version
# download new version from Claude
cp ~/Downloads/deploy_files.sh ~/Developer/AIStudio/scripts/deploy_files.sh
chmod +x ~/Developer/AIStudio/scripts/deploy_files.sh
```

---

## State Packets

Generate an end-of-day state packet for thread continuity:
```bash
~/Developer/AIStudio/scripts/generate_packet.sh --end_of_day
```

Saves to `~/Downloads/` and `~/state_packets/`. The `.md` file is the
bootstrap document for starting a new Claude thread.

---

For architecture context, see [docs/architecture_decisions.md](docs/architecture_decisions.md).
For getting started, see [QUICKSTART.md](QUICKSTART.md).
