# Quickstart

*Version: 2.0.0 | Updated: 2026-06-18*

Get a running AIStudio instance in under 30 minutes.

AIStudio runs entirely on your Mac — no cloud account, no API keys, no data leaving your machine. You'll have a local AI search engine over your own documents, accessible from your browser.

> **This guide is intentionally detailed** — it explains what each tool does and why it is needed. This is deliberate: AIStudio has several components, and understanding what you are installing makes you a much more effective user. **In a hurry, and already have the developer tools?** Experienced users who already run Homebrew, Python, Ollama, and git can skip to the **[TL;DR — Fast Install](#tldr--fast-install)** at the end and be running in minutes — but you'll miss the explanations of how a RAG system is built (the fun part).

---

## A Note on the Tools Used in This Guide

Installing AIStudio requires a few external tools — package managers, a model runtime, a vector database, and a code host. Each is introduced where it is first needed; for a one-glance summary of all of them with links, see **[Annex 1 — Tools Used in This Guide](#annex-1--tools-used-in-this-guide)**.

The two you'll lean on most are both places software is stored and downloaded from automatically:

**Homebrew** ([https://brew.sh](https://brew.sh)) is a package manager for macOS. Think of it as an App Store for developer tools — instead of clicking buttons in a GUI, you type `brew install <something>` and Homebrew finds it, downloads it, and installs it for you. We use it to install Python and Ollama.

**GitHub** ([https://github.com](https://github.com)) is where AIStudio's code lives. Think of it as a library where software is stored and versioned. We use a tool called `git` to download ("clone") AIStudio from GitHub directly onto your Mac. AIStudio is a public repository — no account or access key required to download it.

> If a command ever does something unexpected, see **[Annex 2 — Troubleshooting](#annex-2--troubleshooting)** at the end — its entries follow the same order as the steps below.

---

## Before You Start

**Open Terminal first.** Press **⌘ Space** (that's the Command key and the Space bar at the same time), type **Terminal**, press **Enter**.

You'll see a window with a prompt that looks something like this:
```
yourusername@Mac ~ %
```
The prompt text varies by machine and depends on your name — don't worry about it.

AIStudio setup uses the shell to get installed and also to perform tasks the AIStudio User Interface (UI), which runs in your browser, doesn't cover. The commands all start with `ais_` — like `ais_start`, `ais_stop`, `ais_bench`. These are presented in Step 8.

> **What is a shell?** Terminal gives you access to the shell — a text interface for running commands on your Mac.

**If you close the Terminal window at any point**, open a new one: press **⌘ Space** (Command key + Space bar), type **Terminal**, press **Enter**. Then re-run the last command you were on and continue from there.

---

## Prerequisites

You need a Mac with Apple Silicon (M1/M2/M3/M4). Everything else you need — Python, Homebrew, Qdrant, Ollama — is installed in the steps below.

> Not sure if you have Apple Silicon? Click the **Apple menu** (on the top left part of the screen) → **About This Mac**. Look for "Chip: Apple M1" (or M2/M3/M4). Intel Macs have not been tested — results may vary.

---

## 1. Install Homebrew

Homebrew is a package manager for macOS — it installs the software AIStudio needs.

First, check if it is already installed; in the Terminal, type:
```bash
brew --version
```

If you see a version number — Homebrew is already installed. **→ Skip to Step 2.**

If you see `command not found`, install Homebrew. You will be asked for your Mac password — this is the same password you use to unlock your Mac. Type it and press Enter. Nothing will appear on screen as you type — that is normal:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

The installer will show a list of directories it will create. Press **Enter** to continue.

When installation completes you will see `==> Installation successful!` Modern Macs set the Homebrew PATH automatically. Verify:
```bash
brew --version
```

If you see a version number — you are all set. On older Macs, if you still see `command not found`, run these three lines (and see [Annex 2 — Troubleshooting](#annex-2--troubleshooting) if it persists):
```bash
echo >> ~/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

---

## 2. Install Python

First, check if Python is already installed; in the Terminal, type:
```bash
python3 --version
```

If you see a version number where the second part is 10 or higher — for example Python 3.10, 3.11, 3.12, 3.13, or 3.14 — Python is recent enough for AIStudio. **→ Skip to Step 3.**

"3.10 or higher" means: look at the number after the first dot. If it is 10 or more, you are good.

If you see `command not found` — Python is not installed. Install it via Homebrew:
```bash
brew install python@3.13
```

This takes less than a minute. You'll see a stream of messages — ignore them. All is good when you're back at the `%` prompt.

You may also see notices like:
```
[notice] A new release of pip is available
```
Ignore these — they do not affect AIStudio.

Verify:
```bash
python3 --version
```

Expected: `Python 3.13.x` or higher.

> AIStudio uses type syntax (`float | None`) that fails on Python 3.9. The macOS system Python is often 3.9 — that's why we check.

---

## 3. Install Ollama

Ollama ([https://ollama.com](https://ollama.com)) is a local model runtime — it downloads, manages, and serves AI language models on your machine. Think of it as a local equivalent of the OpenAI API, running entirely on your hardware.

Check if already installed; in the Terminal, type:
```bash
ollama --version
```

If you see a version number — Ollama is installed. **→ Skip to "Start Ollama" below.**

If Ollama is not installed:
```bash
brew install ollama
```

This takes less than a minute. You'll see a stream of messages — ignore them. All is good when you're back at the `%` prompt.

> You may see a notification saying **"Background Items Added — ollama is an item that can run in the background."** Click to dismiss or ignore it. This means Ollama will start automatically when your Mac starts up — which is exactly what you want.

> You may also see technical notes about `OLLAMA_FLASH_ATTENTION` and background services — ignore them. Ollama is installed correctly.

**Start Ollama** — run this once now. It also ensures Ollama starts automatically every time your Mac starts up:
```bash
brew services start ollama
```

Also install **Pango** — required for PDF report generation (benchmark reports):
```bash
brew install pango
```

> **Why Pango?** AIStudio's benchmark runner generates PDF reports. Pango is a text rendering library that weasyprint (the PDF engine) depends on. It's a system library — `brew install` handles it in under a minute.

Verify it is running:
```bash
ollama list
```

If you see the column headers (NAME, ID, SIZE, MODIFIED) — Ollama is running correctly. The list may be empty — that is normal. You will download models next.

If you see an error, see [Annex 2 — Troubleshooting](#annex-2--troubleshooting), or start Ollama manually in a separate terminal tab:
```bash
ollama serve
```

---

## 4. Pull Required Models

AIStudio uses two kinds of model that do completely different jobs.

**nomic-embed-text** is the indexing model. When you upload a document, this model reads it and converts every passage into a set of numbers that capture its meaning — called an "embedding." When you ask a question, it finds the passages whose meaning is closest to your question. It is small (274 MB), fast, and runs invisibly. You will never interact with it directly. **Everyone needs this model.**

**The language model** reads the relevant passages found by the indexing model and writes a human-language answer with citations. This is what most people think of as "AI." AIStudio supports three open model families, each in a small (fast) and a large (highest-quality) size:

| Family | Small — fast, the default | Large — best quality |
|--------|---------------------------|----------------------|
| **Google Gemma** ⭐ | `gemma3:4b` | `gemma3:27b` |
| Meta Llama | `llama3.1:8b` | `llama3.1:70b` |
| Mistral AI | `mistral:7b` | `mixtral:8x7b` |

**The default is `gemma3:4b`** — Google's Gemma. It loads in seconds and answers the demo corpus fast, which makes for the best first run; Gemma also tops the AIStudio benchmark on the SEC corpus. You can switch models at any time in the UI.

**Which to download — based on your Mac's memory** (Apple menu → **About This Mac** → "Memory"):

- **8–16 GB** — `gemma3:4b` (the default). Plenty for the demo corpus.
- **32 GB** — also pull `gemma3:27b` for top-quality answers on heavier corpora.
- **64 GB or more** — `gemma3:27b` is excellent; pull `llama3.1:70b` or `mixtral:8x7b` only if you want the largest Meta / Mistral options.

> **Don't run a "large" model on too little memory.** `gemma3:27b` and `mixtral:8x7b` want 32 GB+; **never** pull `llama3.1:70b` under 64 GB — it will download but won't fit in memory, and your Mac will become unresponsive when you try to use it.

**Step 1 — Download the indexing model (required for everyone):**
```bash
ollama pull nomic-embed-text
```

**Step 2 — Download your language model.** Start with the default:
```bash
ollama pull gemma3:4b
```

Optional — the larger Gemma for heavier corpora (32 GB+):
```bash
ollama pull gemma3:27b
```

Prefer Meta or Mistral? Small: `ollama pull llama3.1:8b` or `ollama pull mistral:7b`. Large: `ollama pull llama3.1:70b` or `ollama pull mixtral:8x7b`.

> **You'll switch to `gemma3:27b` later — on purpose.** The demo corpus runs beautifully on `gemma3:4b`. When you reach the SEC 10-K corpus in the [Tutorial](TUTORIAL.md), it prompts you to switch to `gemma3:27b` in the model dropdown — the heavier corpus rewards the larger model (it's the model behind AIStudio's top benchmark). Fast first impression now; full power when it counts.

> **Download times** depend on your internet speed (check yours at [fast.com](https://fast.com)). On a 100 Mbps connection, expect about 2 minutes for `gemma3:4b` and 10 minutes for `gemma3:27b`. The estimate shown during download may fluctuate — starting at hours, then dropping to minutes.

> **Note:** If your models show a modified date of several weeks ago — that's fine. They don't expire.

---

## 5. Install Qdrant

Qdrant ([https://qdrant.tech](https://qdrant.tech)) is the database that stores your document chunks. When AIStudio ingests a document, it splits it into overlapping passages — typically a few paragraphs each — and stores them as vectors in Qdrant. When you query, AIStudio searches across all chunks to find the most relevant passages.

> **Why not Homebrew?** Qdrant is a Rust-based binary not available via Homebrew — install it directly.

Check if already installed; in the Terminal, type:
```bash
qdrant --version
```

If you see a version number — **→ Skip to Step 6.**

If you see `zsh: command not found: qdrant`, Qdrant isn't installed yet — first create a home for its data:
```bash
mkdir -p ~/qdrant_storage
```

This command returns no output — silence means success.

Download and install the binary, put it on your PATH, and verify:
```bash
curl -L https://github.com/qdrant/qdrant/releases/latest/download/qdrant-aarch64-apple-darwin.tar.gz | tar xz
mkdir -p ~/bin
mv qdrant ~/bin/qdrant
grep -q 'export PATH="$HOME/bin' ~/.zshrc || echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
qdrant --version
```

> **Why the `grep` before the `echo`?** `~/bin` is where Qdrant now lives, and your PATH is the list of places your Mac searches when you type a command — so `~/bin` has to be on it for `qdrant` to be found. The part before the `||` quietly checks whether that line is already in your `~/.zshrc`; the line is added **only if it's missing**. If you've set AIStudio up before, it's probably already there — so this leaves it alone instead of writing a second identical copy. That's what makes these commands genuinely safe to re-run.

Expected: `qdrant 1.17.0` (or newer). You will also see:
```
<jemalloc>: option background_thread currently supports pthread only
```
This warning is harmless — ignore it.

---

## 6. Check You Have git

`git` is the tool that downloads ("clones") AIStudio from GitHub. It usually ships with macOS developer tools.

Check; in the Terminal, type:
```bash
git --version
```

If you see `git version 2.x.x` or newer — **→ skip to Step 7, Clone AIStudio.**

If you see `command not found`, or macOS shows a dialog asking to install developer tools — run:
```bash
xcode-select --install
```

**A dialog will appear** saying "The xcode-select command requires the command line developer tools. Would you like to install the tools now?" — click **Install**. A **License Agreement** appears — click **Agree**.

A progress dialog appears. The time estimate may start very high — even hours — then drop to minutes within seconds. Ignore the initial estimate; on a 100 Mbps connection expect about 8–10 minutes.

When done, verify:
```bash
git --version
```

Expected: `git version 2.x.x` or newer.

> If no dialog appeared when you ran `git --version`, trigger the installation manually with `xcode-select --install`. If it still won't install, see [Annex 2 — Troubleshooting](#annex-2--troubleshooting).

---

## 7. Clone AIStudio

AIStudio is a public repository — no GitHub account, SSH key, or access token required. Create a folder for it and clone the repository:
```bash
mkdir -p ~/Developer
cd ~/Developer
git clone https://github.com/mbarberony/AIStudio.git
cd AIStudio
```

This downloads about 96 MB — expect under 2 minutes on a 100 Mbps connection. When complete you will see `Resolving deltas: 100% (...), done.` and land in the `AIStudio` folder.

After the clone, AIStudio lives at `~/Developer/AIStudio/` — the path every command in this guide assumes.

> **Cloned to the wrong place?** Only if your prompt shows `~/AIStudio` (not `~/Developer/AIStudio`) did the folder land wrong — move it:
> ```bash
> mkdir -p ~/Developer && mv ~/AIStudio ~/Developer/AIStudio
> ```

---

## 8. Install AIStudio Commands

`./ais_install` does two things: it creates the Python environment and installs all dependencies, then makes the `ais_*` commands available in your Terminal.

```bash
cd ~/Developer/AIStudio
./ais_install
source ~/.zshrc
ais_help
```

The `ais_*` notation is shorthand for *all the commands that begin with* `ais_` — like `ais_start`, `ais_stop`, `ais_bench`; the `*` is a wildcard standing in for the rest of each name. `ais_help` prints the full list by category, and `ais_help <command>` gives detailed help on any one.

This takes 2–3 minutes. You'll see progress messages as dependencies install.

> You may see `WARNING: Cache entry deserialization failed` messages, or a notice like `[notice] A new release of pip is available` — these are harmless. Ignore them.

> You only need to run `source ~/.zshrc` once — right after installing. Every new Terminal window or tab you open in the future loads your commands automatically.

---

## 9. Activate the Virtual Environment

A virtual environment is an isolated Python workspace that keeps AIStudio's dependencies separate from the rest of your system. After this session you'll rarely touch it — especially if you add a Desktop shortcut in Step 12.

```bash
source ~/Developer/AIStudio/.venv/bin/activate
```

This command returns no output — silence means success. Your prompt will show `(.venv)`, confirming the environment is active.

> You do **not** need to activate the virtual environment manually before `ais_start` — it handles that automatically. You only need this if you run other `ais_*` commands from a fresh terminal tab before `ais_start` has run.

---

## 10. Start AIStudio

```bash
ais_start
```

AIStudio starts three processes — Qdrant, Ollama, and the FastAPI backend — and opens the UI in your browser automatically, in about 20 seconds.

> You may see a warning that the backend was slow to start — this is normal on first run. The UI will still open correctly.

> **First run:** On a fresh install, `ais_start` automatically indexes the **demo** and **help** corpora in the background. A progress banner appears in the UI if indexing takes more than 30 seconds — wait for it to finish before asking your first question.

It is OK to **minimize** the Terminal window now — but **do not close it**. The Terminal is where the backend runs; closing it shuts AIStudio down.

**To verify the backend is up:**
```bash
curl http://localhost:8000/health
```
Expected: `{"status": "ok"}`. If you get an error or no response instead, the backend isn't ready — see [Annex 2 — Troubleshooting](#annex-2--troubleshooting) (start with a hard-refresh of the browser, then `ais_stop` and `ais_start`).

---

## 11. What You're Looking At — and Your First Query

When AIStudio opens in your browser, you'll see three main areas:

**On the left** — the corpus selector. This is where you choose which document collection to query. The **demo** corpus is already loaded — original documents spanning 2003–2026, covering enterprise architecture, IT strategy, financial services, and agentic AI.

**In the center** — the chat area. Type a question, get a cited answer. References below each answer show exactly which document and page the answer came from. Click **Open ↗** to see the source.

**On the right** — the settings sidebar. It controls how AIStudio retrieves and generates answers (model, Top K, temperature, retrieval mix). See **[Annex 3 — Tuning Parameters](#annex-3--tuning-parameters)** for what each control does.

The **Model** is set to `gemma3:4b` by default — small and fast, ideal for the demo. (For the heavier SEC 10-K corpus in the [Tutorial](TUTORIAL.md), switch it to `gemma3:27b`.)

Try these questions on the demo corpus to start:
- *"What is QFD and how does it apply to technology architecture?"*
- *"How do you design an IT organization around architectural principles?"*
- *"What does a reference architecture for enterprise AI look like?"*

Then switch to the **help** corpus and ask: *"How do I re-ingest a corpus?"* — AIStudio is answering questions about itself, using the same RAG pipeline to retrieve answers from its own documentation.

> **Initial latency:** Your very first query may take 20–50 seconds while the model loads fully into memory. Every query after that is faster — typically 6–7 seconds.

---

## 12. Add a Desktop Shortcut (Optional)

If you minimized the Terminal window in Step 10, reopen it — press **⌘ Space**, type **Terminal**, press **Enter**.

If you'd like to launch AIStudio by double-clicking an icon instead of opening a terminal:
```bash
ais_create_shortcut
```

This creates `AIStudio.app` in `~/Applications` and adds a shortcut to your Desktop. Double-clicking it starts all AIStudio services and opens the browser automatically — no Terminal needed.

> **Icon not showing correctly?** Run `killall Dock` to refresh the icon cache.

To remove the shortcut later:
```bash
ais_create_shortcut --remove
```

To skip the Desktop symlink and only create the app in `~/Applications`:
```bash
ais_create_shortcut --nodesktop
```

---

## Stopping AIStudio

When you're done for the session:
```bash
ais_stop
```
This shuts down the backend and Qdrant. Your corpora and settings are saved — `ais_start` (or the Desktop shortcut) brings everything back next time.

---

AIStudio is ready. Your documents are waiting.

<div align="center">★★★&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;★★★</div>

For a full guided walkthrough — including the SEC 10-K at-scale exercise and benchmarking — see [TUTORIAL.md](TUTORIAL.md).

---

## TL;DR — Fast Install

*For experienced users who already live in a terminal. This skips every explanation above — you'll get a running instance, but you'll miss the understanding of how a RAG system is built. If anything here is unfamiliar, use the full guide instead.*

**Prereqs:** Apple Silicon Mac. The block below installs Homebrew, Python, Ollama, Pango, Qdrant, and git if missing — skip any you already have.

```bash
# 1. Toolchain
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.13 ollama pango git
brew services start ollama

# 2. Models — embedding (required) + Google's Gemma (the default; small & fast)
ollama pull nomic-embed-text
ollama pull gemma3:4b           # default; add gemma3:27b on 32GB+ for the SEC corpus

# 3. Qdrant binary
mkdir -p ~/qdrant_storage ~/bin
curl -L https://github.com/qdrant/qdrant/releases/latest/download/qdrant-aarch64-apple-darwin.tar.gz | tar xz
mv qdrant ~/bin/qdrant
grep -q 'export PATH="$HOME/bin' ~/.zshrc || echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc

# 4. Clone + install
mkdir -p ~/Developer && cd ~/Developer
git clone https://github.com/mbarberony/AIStudio.git
cd AIStudio
./ais_install
source ~/.zshrc

# 5. Go
ais_start
```

First run auto-indexes the **demo** and **help** corpora (~60s) and opens the UI on `gemma3:4b`. First query is slow (model load, 20–50s); after that ~6–7s. `ais_help` lists commands; `ais_stop` when done.

> In the UI sidebar the demo corpus defaults to **Top K = 10**. Full knobs in [Annex 3](#annex-3--tuning-parameters).

---

## Annex 1 — Tools Used in This Guide

| Tool | What it does | URL |
|------|--------------|-----|
| Homebrew | Package manager for macOS | https://brew.sh |
| Python | Programming language AIStudio runs on | https://www.python.org |
| Ollama | Local AI model runtime | https://ollama.com |
| Pango | Text-rendering library for PDF benchmark reports | https://pango.gnome.org |
| Qdrant | Vector database for document storage | https://qdrant.tech |
| GitHub / git | Code hosting and version control | https://github.com |

The language models themselves — Google **Gemma**, Meta **Llama**, Mistral AI's **Mistral** — are downloaded through Ollama in Step 4.

---

## Annex 2 — Troubleshooting

Entries follow the order of the steps, so you can scan to where you are.

**Something unexpected happened** — close and reopen Terminal (**⌘ Space**, type **Terminal**, **Enter**), then re-run the last command. A fresh terminal always starts with a clean environment.

**(Step 1) `brew --version` returns `command not found`** — Homebrew not installed, or its PATH isn't set. Run the installer in Step 1; on older Macs run the three `~/.zprofile` lines at the end of Step 1.

**(Step 2) `python3` not found** — run `brew install python@3.13`.

**(Step 3) `ollama list` hangs or errors** — Ollama isn't running. If brew-installed: `brew services start ollama`. Otherwise: `ollama serve` in a separate tab.

**(Step 3/10) UI shows "Ollama not running"** — run `brew services start ollama`, then `ais_start` again.

**(Step 5) `qdrant` — `command not found`** — `~/bin` isn't on your PATH. Run `source ~/.zshrc` (and confirm the PATH line is in `~/.zshrc`, per Step 5).

**(Step 9) `(.venv)` not in your prompt** — run `source ~/Developer/AIStudio/.venv/bin/activate`.

**(Step 10) `curl …/health` doesn't return `{"status":"ok"}`, or UI shows "Error loading corpora"** — the browser opened before the backend finished starting. Hard-refresh (`Cmd+Shift+R`). If it persists, run `ais_stop` then `ais_start`.

**(Step 11) Stats show 0 chunks** — the corpus isn't ingested yet. Use the UI **Add** button to upload and ingest documents.

---

## Annex 3 — Tuning Parameters

The settings sidebar (Step 11) controls retrieval and generation. Defaults are tuned for the demo corpus; adjust per corpus as needed.

| Parameter | Default | Effect |
|-----------|---------|--------|
| Model | `gemma3:4b` | The language model that writes answers. Small & fast for the demo; switch to `gemma3:27b` for the SEC 10-K corpus. |
| Top K | 10 | Chunks retrieved per query. Higher = more context, slightly slower. **10 is the default** — the demo has small documents (as few as 20 chunks) that only surface reliably at K=10, and the SEC corpus needs K=10 for cross-firm multi-source queries. |
| Temperature | 0.3 | LLM creativity. Lower = more factual. Keep at 0.3 for document Q&A. |
| Retrieval Mix | 0.5 | Blends keyword matching with semantic understanding. Drag left toward **Literal** (exact word matching) or right toward **Conceptual** (related meaning even when exact terms differ). Center (0.5) works well for most queries; try full Conceptual for thematic questions, center-to-Literal for specific entity or term lookups. |
| Score Threshold | 0.3–0.5 | Filters out retrieved chunks that scored too low to be useful. Low-score chunks cause hedged or incorrect answers. Set lower (0.3) for corpora with small documents; higher (0.5) for large uniform corpora like SEC 10-K. Configured per-corpus — the demo uses 0.3, sec_10k uses 0.5. |

> For more on query settings, see [HOWTO.md](HOWTO.md).

---

For architecture context, see [docs/architecture_decisions.md](docs/architecture_decisions.md).
For day-to-day usage, see [HOWTO.md](HOWTO.md).
For guided walkthroughs, see [TUTORIAL.md](TUTORIAL.md).
