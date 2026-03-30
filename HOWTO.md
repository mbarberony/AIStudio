# HOWTO — AIStudio User Guide

Practical answers for day-to-day AIStudio use.
Not a getting-started guide (see [QUICKSTART.md](QUICKSTART.md)) — reach for this when
you need to do something specific or something isn't working as expected.

**Version:** Beta

---

## Contents

- [Shell & Terminal](#shell--terminal)
- [Using AIStudio](#using-aistudio)
- [Corpus Management](#corpus-management)
- [Installing and Managing LLMs](#installing-and-managing-llms)
- [Query Settings](#query-settings)
- [Benchmark & Corpus Testing](#benchmark--corpus-testing)

---


## Shell & Terminal

***What is the shell?***
The shell (Terminal) is a text-based interface for running commands on your Mac.
AIStudio setup and management uses the shell for tasks the UI doesn't cover — like
installing models or ingesting a new corpus. New to the shell?
See [Apple's Terminal User Guide](https://support.apple.com/guide/terminal/welcome/mac).

***How do I open the Terminal?***
Press `Cmd+Space`, type `Terminal`, press Enter. Or open Finder →
Applications → Utilities → Terminal.

***Why does my terminal say "command not found" when I paste commands?***
Two common causes:
- You pasted a `#` comment line — zsh tries to execute it. Paste only the commands,
  not the comment lines.
- Your AIStudio aliases aren't loaded yet. Run:
```bash
source ~/.zshrc
```
Then try the command again on its own line. Do not chain: `source ~/.zshrc && ais_start`
will fail. Run `source ~/.zshrc` first, then `ais_start`.

---

## Using AIStudio

After running `bash install.sh` and `source ~/.zshrc`, these commands are available:

| Command | What it does |
|---|---|
| `ais_start` | Start all services and open the UI in your browser |
| `ais_stop` | Stop all services |
| `ais_bench` | Run a benchmark on the demo corpus |
| `ais_sec_download` | Download the SEC 10-K corpus from EDGAR (~500MB) |
| `ais_help` | Print this command reference |

Every command supports `--help`:
```bash
ais_start --help
ais_bench --help
```

---

## Upgrading AIStudio

**How do I upgrade AIStudio when a new version is released?**

Pull the latest code from GitHub:
```bash
cd ~/Developer/AIStudio && git pull
```

Then update Python dependencies in case new packages were added:
```bash
source .venv/bin/activate && pip install -r requirements.txt
```

Then restart:
```bash
ais_start
```

**Does upgrading delete my corpus data?**
No. Your corpus data lives in `~/qdrant_storage/` on disk — completely separate from the AIStudio codebase. It persists across upgrades, restarts, and reboots. You never need to re-ingest after a routine upgrade.

**When would I need to re-ingest after an upgrade?**
Only if the release notes say the chunk format changed. This is rare and always announced. When it happens, run:
```bash
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest   --corpus <name> --root data/corpora/<name>/uploads --force
```
The `--force` flag wipes and rebuilds the corpus cleanly.

**The demo corpus re-ingests automatically** on first `ais_start` after an upgrade if needed.

---

## Corpus Management

***How do I ingest a new corpus?***
```bash
cd ~/Developer/AIStudio && source .venv/bin/activate
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \
  --corpus <name> --root data/corpora/<name>/uploads
```

***How do I re-ingest a corpus from scratch?***
Add `--force` — atomically wipes and rebuilds:
```bash
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \
  --corpus <name> --root data/corpora/<name>/uploads --force
```

***What happens when I delete a file from a corpus — is it gone forever?***
No. Deleted files move to `data/corpora/<name>/uploads/trash/` — not permanently deleted.

***How do I recover a file I accidentally deleted from a corpus?***
```bash
# See what's in trash
ls ~/Developer/AIStudio/data/corpora/<name>/uploads/trash/

# Move it back
mv ~/Developer/AIStudio/data/corpora/<name>/uploads/trash/<filename> \
   ~/Developer/AIStudio/data/corpora/<name>/uploads/

# Re-ingest to restore it
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \
  --corpus <name> --root data/corpora/<name>/uploads --force
```

***What happens when I delete an entire corpus — is it gone forever?***
No. The corpus folder moves to `~/.Trash/AIStudio_<name>/`.

***How do I recover a corpus I accidentally deleted?***
```bash
mv ~/.Trash/AIStudio_<name> ~/Developer/AIStudio/data/corpora/<name>
# Then re-ingest as above
```

***How do I ingest the SEC 10-K corpus?***
Download first:
```bash
ais_sec_download
```
Then ingest:
```bash
AISTUDIO_VECTORSTORE=qdrant PYTHONPATH=src python3 -m local_llm_bot.app.ingest \
  --corpus sec_10k --root ~/Downloads/sec_10k_corpus --force
```
Allow ~34 minutes. Safe to run in background.

---

## Installing and Managing LLMs

***How do I see what models are installed?***
```bash
ollama list
```

***How do I install a new LLM?***
```bash
ollama pull llama3.1:8b       # ~5GB — recommended default, fast
ollama pull llama3.1:70b      # ~42GB — best quality, requires ~64GB RAM
ollama pull mistral:7b        # ~4.4GB — alternative option
```
Once pulled, the model appears automatically in the **Model** dropdown in the UI.
No restart required.

***Which model should I choose?***
On Apple Silicon, `llama3.1:70b` and `llama3.1:8b` have identical query latency
(~6–7s) once warm. Choose based on available RAM:
- `llama3.1:8b` — 8GB RAM minimum, recommended for most users
- `llama3.1:70b` — 64GB+ RAM, best answer quality
- `mistral:7b` — good alternative on constrained hardware

***How do I remove a model I no longer need?***
```bash
ollama rm mistral:7b
```

See the [Ollama model library](https://ollama.com/library) for all available models.

---

## Query Settings

The **Query Settings** panel in the sidebar controls how AIStudio retrieves and
generates answers. These settings apply to every query until you change them.

**Top K** — *How many document chunks to retrieve*
The number of passages retrieved from your corpus before generating an answer.
Higher values give the model more context but increase latency slightly.
- Default: `5` — good for most queries
- Try `10` for complex questions spanning multiple documents
- Try `3` for faster responses on focused questions
Adjust using the **Top K** input field in the sidebar.

**Temperature** — *How creative vs. precise the answer is*
Controls randomness in the model's output.
- `0.1–0.3` — precise, factual, stays close to the source documents. Best for research.
- `0.5–0.7` — more varied, synthesizes across sources. Better for summaries.
- Default: `0.3` — recommended starting point
Adjust using the **Temperature** input field in the sidebar.

**Keywords (optional)** — *Pre-filter the corpus before retrieval*
Enter comma-separated terms to narrow retrieval to chunks containing those keywords.
Useful when your corpus spans multiple topics and you want to focus on a specific area.
Example: `Goldman Sachs, 2024, risk`
Leave blank for full corpus retrieval.
Enter keywords in the **Keywords** field in the sidebar.

---

## Benchmark & Corpus Testing

The benchmark harness serves two purposes:
- **Performance** — measures query latency per question
- **Veracity** — validates answer quality against a questions file

***How do I run a benchmark on the demo corpus?***
```bash
ais_bench
```

***How do I benchmark a different corpus?***
```bash
ais_bench --corpus help
ais_bench --corpus sec_10k --top-k 10
```

***How do I test with a specific model or settings?***
```bash
ais_bench --corpus demo --model llama3.1:70b --top-k 10 --temperature 0.1
```

***How do I write my own test questions for a corpus?***
Create `benchmarks/<corpus_name>_questions.yaml`:
```yaml
- topic: Getting Started
  questions:
    - id: start_aistudio
      question: How do I start AIStudio?
      notes: Should reference ais_start command
```
Run `ais_bench --corpus <n>` — the questions file is auto-detected by corpus name.

***Where do reports go?***
`benchmarks/reports/` — timestamped `.md` and `.json` pairs. The `.md` shows pass/fail per question with latency and citations.

For full benchmark documentation see [HARNESS.pdf](docs/HARNESS.pdf).

---

For architecture context, see [docs/architecture_decisions.pdf](docs/architecture_decisions.pdf).
For getting started, see [QUICKSTART.md](QUICKSTART.md).
