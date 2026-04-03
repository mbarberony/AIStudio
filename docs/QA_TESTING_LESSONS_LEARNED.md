# QA Testing — Lessons Learned
*Mac Air OBE Clean Install — March 17, 2026*
*Tester: Manuel Barbero | Platform: MacBook Air M4, 16GB, macOS Sequoia 15.6*

---

## Executive Summary

The OBE clean install on a fresh Mac Air exposed critical gaps that would have
blocked or confused any first-time user. Most issues were invisible during
development because the developer machine already had all dependencies installed.
The most severe issues were PDF line-wrapping breaking shell commands, Python
version detection, and the start.sh demo path bug.

**Severity breakdown:**
- 🔴 Showstoppers (would block install): 3
- 🟡 Significant friction (confusing, recoverable): 8
- 🟢 Polish (UX improvements): 7

**Root cause categories:**
- **[ENV]** Environment assumption — dev machine had something pre-installed
- **[DOC]** Documentation gap — step unclear or missing
- **[BUG]** Code/config bug — actual defect in the product
- **[UX]** User experience — confusing but not broken
- **[PDF]** PDF rendering artifact — commands broken by line-wrapping

---

## 🔴 Showstopper Issues

### 1. Python Version Detection Failure
**What happened:** Step 7 used `python3` which resolved to the system Python 3.9
(from Xcode Command Line Tools) instead of the user-installed Python 3.14.
This built a broken `.venv` that failed with:
```
TypeError: Unable to evaluate type annotation 'float | None'
```
**Root cause category:** [ENV] + [DOC]
Dev machine had Python 3.13 as the default `python3`. Fresh Mac doesn't.
QUICKSTART never warned that macOS system `python3` is 3.9.

**Fix applied:** Step 7 now uses auto-detect chain trying 3.14 → 3.13 → ... → 3.10.
**QUICKSTART:** Step 7 updated.
**README:** Minimum Python changed to 3.10+.
**TODO:** Add a preflight check script (`scripts/check_env.sh`) that validates
Python version, PATH, and required tools before the user starts.

---

### 2. PDF Line-Wrapping Breaks Shell Commands
**What happened:** The Qdrant install command in Step 5 was split across lines
in the PDF. Copy-pasting wrote a broken line to `~/.zshrc`, corrupting PATH
for every subsequent Terminal session. Basic commands (`mkdir`, `ollama`, `echo`)
stopped working.
**Root cause category:** [PDF] + [DOC]
Multi-line commands are inherently fragile in PDF format. No warning was given.

**Fix applied:** Step 5 now uses a single `&&`-chained command that PDF cannot
break. Warning added at top of QUICKSTART directing users to GitHub for
copy-paste.
**TODO:** All commands in QUICKSTART must be single-line or verified PDF-safe.
Add automated check to CI that validates no command in QUICKSTART spans more
than one line (future).

---

### 3. start.sh Demo Corpus Path Bug
**What happened:** `start.sh` referenced `data/demo/demo_data` — the old path
before corpus restructure. Auto-ingest failed on first run.
**Root cause category:** [BUG]
Corpus restructure commit updated the ingest command but missed start.sh.

**Fix applied:** Patched in fbfebf8, validated via `git pull` on Mac Air.
**TODO:** When moving files, add a repo-wide grep for old paths as part of
the commit checklist. Consider adding a test that validates start.sh paths
exist in the repo.

---

## 🟡 Significant Friction Issues

### 4. `llama3.1:8b` Not Marked as Required
**What happened:** Listed alongside optional models. Tester skipped it.
Every query returned 500 error: `model 'llama3.1:8b' not found`.
**Root cause category:** [DOC]
**Fix applied:** Step 4 now clearly separates required vs optional.
**TODO:** start.sh should check that `llama3.1:8b` is available before starting
and print a clear error if not.

---

### 5. Ollama `ollama list` Timing Issue
**What happened:** `ollama list` immediately after `brew services start` returned
`could not connect to ollama server`.
**Root cause category:** [DOC]
Ollama needs ~3 seconds to initialize after brew starts it.
**Fix applied:** Added "wait 5 seconds, then verify" to Step 3.
**TODO:** start.sh already handles this with a wait loop — document the pattern.

---

### 6. Skip Logic Not Explained
**What happened:** "Skip if already installed" confused tester — didn't know
what a successful install looks like.
**Root cause category:** [DOC]
**Fix applied:** Every step now has explicit "if you see X — skip to next step" language.
**TODO:** Consider a preflight script that checks and reports which steps can be skipped.

---

### 7. `#` Comment Lines in Commands Cause Errors
**What happened:** Multiple `zsh: command not found: #` errors from copy-pasting
blocks that included comment lines.
**Root cause category:** [DOC] + [UX]
Despite warnings, this kept happening because the PDF presented commands and
comments as a single visual block.
**Fix applied:** All `#` comments removed from all commands in QUICKSTART.
**TODO:** Zero tolerance policy — enforce in doc review. Consider a linter.

---

### 8. Two Pythons Coexisting Silently
**What happened:** `python3 --version` returned 3.9.6 on the same machine where
`python3.14 --version` returned 3.14.0. No warning in QUICKSTART.
**Root cause category:** [ENV] + [DOC]
**Fix applied:** Note added explaining macOS Python version coexistence.
**TODO:** preflight check script would catch this automatically.

---

### 9. First Query 30-40 Second Wait With No Feedback
**What happened:** First query appeared to hang — no UI feedback during model
cold load.
**Root cause category:** [UX]
**Fix applied:** QUICKSTART now warns: "First query may take 30-40 seconds."
**TODO:** Add a loading indicator or progress message in the UI for first-query
cold load. Current amber→green status pill doesn't communicate this.

---

### 10. Absolute Path Required After PATH Corruption
**What happened:** After `~/.zshrc` corruption, `ollama` stopped working entirely.
Required `/opt/homebrew/bin/ollama` as workaround.
**Root cause category:** [PDF] (downstream of issue #2)
**Fix applied:** Documented in Troubleshooting section A.
**TODO:** Add `~/.zshrc` health check to preflight script.

---

### 11. Port 8000 Already in Use on start.sh Re-run
**What happened:** Second `start.sh` run (after `git pull`) tried to start a
second uvicorn on port 8000. Got `[Errno 48] address already in use`. Auto-ingest
still completed despite the error — confusing output.
**Root cause category:** [BUG]
**Fix applied:** None yet — documented in troubleshooting.
**TODO:** start.sh should check if port 8000 is occupied before starting uvicorn,
and either kill the old process or skip starting a new one.

---

## 🟢 Polish / UX Issues

### 12. Terminal Not Explained for Non-Technical Users
**Root cause category:** [DOC] — assumed knowledge.
**Fix applied:** Step-by-step Terminal instructions, ⌘ Space shortcut explained,
Dock tip added.

### 13. Progress Bar Interleaved with Qdrant Log Messages
**Root cause category:** [UX] — Qdrant and ingest run in parallel, logs mix.
**TODO:** `--quiet` flag for start.sh (v2.0).

### 14. Brew Version Said 4.x, Got 5.x
**Root cause category:** [DOC] — stale version number.
**Fix applied:** "5.x.x or newer (current as of 2026)."

### 15. No Terminal Shortcut / Dock Tip
**Root cause category:** [DOC].
**Fix applied:** Added Dock tip and ⌘ Space instruction.

### 16. PDF vs GitHub Version Gap
**Root cause category:** [PDF].
**Fix applied:** Warning at top of QUICKSTART.
**TODO:** Ship QUICKSTART.pdf with repo but watermark: "For commands, use GitHub."

### 17. HF Hub Authentication Warning
**Root cause category:** [UX] — alarming but harmless.
**Fix applied:** Documented in Step 8 expected output.

### 18. UNEXPECTED CrossEncoder Key Warning
**Root cause category:** [UX] — alarming but harmless.
**Fix applied:** Documented in Step 8 expected output.

---

## What the Developer Machine Masked

The following issues were invisible during development:

| Issue | Why Masked |
|-------|-----------|
| System Python 3.9 vs user Python 3.14 | Dev machine had 3.13 as default `python3` |
| Fresh `~/.zshrc` | Dev's was already correctly configured |
| `llama3.1:8b` not downloaded | Already on dev machine |
| start.sh path bug | Demo already ingested on dev machine |
| First-query 40s cold load | Model always warm on dev machine |
| Qdrant binary PATH issue | Dev's `~/bin` already in PATH |
| PDF line-wrapping | Dev never copy-pastes from PDF |

**Key lesson:** The developer environment is a terrible proxy for a fresh install.
OBE on a truly clean machine should be run after every significant release.

---

## Recommended Demo Questions (Mac Air Validated)

Questions that produced strong answers on both llama3.1:8b and mistral:7b:

1. "Explain the concept of plateau and its use in the context of planning"
2. "Why should you not spend too much time on intermediary plateaus?"
3. "How should a CTO prioritize a three-year technology strategy?"
4. "What are the key principles for modernizing legacy applications?"

**Notes on these questions:**
- Question 1 is best overall — grounded in the 2006 FS Journal article
- Question 2 is a great follow-up to question 1
- Question 3 produces a strong multi-source answer
- Question 4 takes ~22s but good results on both models

**Avoid as demo questions:**
- Questions about CMDB — retrieves IT Infrastructure doc first, less relevant
- Open-ended AI limitation questions — may not have strong demo corpus grounding

---

## Validation Results

| Check | Result | Notes |
|-------|--------|-------|
| Clean install from zero | ✅ Success | With workarounds for 3 showstoppers |
| Demo corpus auto-ingest | ✅ After git pull fix | fbfebf8 |
| llama3.1:8b query | ✅ 22s first query | Cold load |
| mistral:7b query | ✅ 18s, strong answer | Often better than 8b |
| Page numbers in citations | ✅ Correct | p.20, p.16, p.5 etc. |
| Open ↗ links | ✅ Opens correct document | Page scroll is v2.0 |
| git pull → instant fix | ✅ Confirmed | Key workflow validated |
| Python 3.14 compatibility | ✅ Confirmed | Not officially tested before |

---

## Action Items Summary

| Item | Priority | Owner | Target |
|------|----------|-------|--------|
| preflight check script (`scripts/check_env.sh`) | 🟡 | Dev | v1.1 |
| start.sh: check llama3.1:8b available | 🟡 | Dev | v1.1 |
| start.sh: port 8000 conflict handling | 🟡 | Dev | v1.1 |
| start.sh: `--quiet` flag | 🟢 | Dev | v2.0 |
| Ship QUICKSTART.pdf with GitHub watermark | 🟢 | Doc | Next release |
| Repo-wide path grep on corpus moves | 🟢 | Process | Ongoing |
| UI loading indicator for cold model load | 🟢 | Dev | v2.0 |

---
*Generated: March 17, 2026 | OBE Session — Mac Air M4 Fresh Install*
*File: QA_TESTING_LESSONS_LEARNED.md*
