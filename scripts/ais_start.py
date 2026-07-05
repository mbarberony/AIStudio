# Version: 1.4.0
# Changelog: 1.4.0 — (A1c) desktop-icon lifecycle: detach the three spawned services
#            (Qdrant, Ollama, backend) with start_new_session=True. They were plain child
#            Popens — fine in a terminal (they orphan-survive), but under launchd (the desktop
#            icon's path) the agent job exits after ais_start returns and launchd REAPS its
#            whole process tree, killing the just-started services. start_new_session puts each
#            in its own session/process-group so the agent's exit no longer cascades. Safe for
#            interactive stop: ais_stop/stop.sh kill by PORT (lsof -ti:8000/6333), not by parent.
#            ALSO (takeover notice): when a start supersedes a stale backend on :8000, announce
#            it in THIS window (pid + start time) and append a timestamped line to
#            ~/Library/Logs/AIStudio/superseded.log — so an older terminal's stale "running"
#            output no longer silently misleads, and the handoff is auditable.
# Changelog: 1.3.0 — C18 / #888 model guard. (1) Zero chat models → graceful hard-fail
#            referencing the RESOLVED default (was: stale `ollama pull llama3.1:8b`), with
#            generic guidance for any model + the AISTUDIO_DEFAULT_MODEL override. (2) If the
#            configured default is NOT installed but other model(s) ARE, the backend is
#            launched on an available model FOR THIS SESSION (default model from config.py /
#            env — single source of truth) so the first query can't 500; this is announced
#            after startup with both permanent fixes (pull the default, or export the model
#            as default). Works with a single imported model. (3) Default present → echoed.
# Changelog: 1.2.0 — PARK-20/21: guard the Qdrant launch. Pre-check shutil.which("qdrant")
#            and, if absent, print the QUICKSTART §5 install recipe + ais_restore note and
#            exit 1 (was: raw FileNotFoundError traceback from subprocess.Popen). Post-check
#            health after launch and fail with actionable hints if it never comes up.
# Changelog: 1.1.0 — STD CLI Output v2.4.0 §2 conformance: collapse the 7 section labels
#            to the 4 canonical bundles (Cleanup / Ecosystem / Processing / Reporting).
#            Backend folds into Ecosystem; Frontend + References + Next commands fold into
#            Reporting; "Default corpora" → "Processing"; Reporting · lines flush-left.
#            Glyphs unchanged — §2 endorses ✅ for "already running" (§8 yellow-✓ is
#            processing-loop-scoped, N/A to discrete service checks).
# Changelog: 1.0.6 — noqa SIM115 on ExitStack.enter_context(open(...)); remove duplicate
#            running message; add --start_with tip on plain start; corpus name in ✅ line.
#            weights, takes ~20s); add waiting message with 10s progress ticks; add
#            corpus name to frontend open message when --start_with is set.
#            fix F841 remove unused venv var; fix SIM115 with noqa (intentional fd leak
#            for daemon Popen — context manager semantics are wrong here).
#            resolves localhost → ::1 on macOS, curl resolves → 127.0.0.1; mismatch caused
#            30s timeout despite uvicorn running fine). Bind uvicorn to 0.0.0.0 for
#            robustness. Bump api var to http://127.0.0.1:8000 throughout.
# Changelog: 1.0.1 — fix lint (SIM105, F541); use bare uvicorn command.
#            Wrapper (ais_start.sh) owns --help and exec. Python owns VERSION, bold bracketed
#            header, all business logic: retry health loop (poll /health every 1s up to 30s,
#            open browser immediately on first healthy response), gate browser open on backend
#            health (AIStudio_715: don't open if backend fails), proper --start_with fragment
#            support via webbrowser, masked stop.sh output, reordered output sections.
from __future__ import annotations

import argparse
import contextlib
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path

SCRIPT_NAME = "ais_start"
VERSION = "1.4.0"

# ── ANSI helpers ──────────────────────────────────────────────────────────────
BOLD   = "\033[1m"
DIM    = "\033[2m"
ITALIC = "\033[3m"
RESET  = "\033[0m"


def _sep(label: str, separator: bool = True) -> None:
    if separator:
        print(f"{DIM}--- {ITALIC}{label}{RESET}")
    else:
        print()


def _health(url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=1) as r:
            return r.status == 200
    except Exception:
        return False


def _qdrant_collection_count(collection: str) -> int:
    """Returns chunk count, 0 if collection missing/empty, -1 if Qdrant unreachable."""
    try:
        url = f"http://localhost:6333/collections/{collection}"
        with urllib.request.urlopen(url, timeout=3) as r:
            d = json.loads(r.read())
        result = d.get("result", {})
        return int(result.get("points_count") or result.get("vectors_count") or 0)
    except Exception:
        return -1


def _ollama_chat_models() -> list[str]:
    """Names of installed chat (non-embedding) models, e.g. ['gemma3:4b', 'mistral:7b']."""
    try:
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3) as r:
            d = json.loads(r.read())
        return [
            m.get("name", "")
            for m in d.get("models", [])
            if "embed" not in m.get("name", "").lower()
        ]
    except Exception:
        return []


def _resolve_default_model(repo: Path) -> str | None:
    """The default model the backend WILL use: AISTUDIO_DEFAULT_MODEL env, else the
    backend's own config.py default. Single source of truth — never hardcoded here.
    Returns None only if the import fails (best-effort)."""
    env = os.environ.get("AISTUDIO_DEFAULT_MODEL")
    if env:
        return env
    try:
        from local_llm_bot.app.config import CONFIG
        return CONFIG.rag.default_model
    except Exception:
        return None


def _ollama_chat_model_count() -> int:
    try:
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3) as r:
            d = json.loads(r.read())
        return sum(
            1 for m in d.get("models", [])
            if "embed" not in m.get("name", "").lower()
        )
    except Exception:
        return 0


def main() -> int:
    # REPO is one level up from scripts/
    repo = Path(__file__).resolve().parent.parent

    # ── Parse args (--help handled by wrapper, not here) ──────────────────────
    parser = argparse.ArgumentParser(prog=SCRIPT_NAME, add_help=False)
    parser.add_argument("--version",      action="store_true")
    parser.add_argument("--verbose",      action="store_true")
    parser.add_argument("--no-separator", action="store_true", dest="no_separator")
    parser.add_argument("--show-log",     action="store_true", dest="show_log")
    parser.add_argument("--show-splash",  action="store_true", dest="show_splash")
    parser.add_argument("--no-open",      action="store_true", dest="no_open")
    parser.add_argument("--start_with",   default="", metavar="CORPUS")
    args, _ = parser.parse_known_args()

    separator = not args.no_separator

    # ── --version: Python owns this ───────────────────────────────────────────
    if args.version:
        print(f"{SCRIPT_NAME} v{VERSION}")
        return 0

    # ── Bold bracketed header (CLI Output STD §2) ─────────────────────────────
    print(f"{BOLD}[{SCRIPT_NAME} v{VERSION} — Start all AIStudio services]{RESET}")

    frontend       = repo / "front_end" / "rag_studio.html"
    log_dir        = Path.home() / "Library" / "Logs" / "AIStudio"
    log_file       = log_dir / "backend.log"
    qdrant_storage = Path.home() / "qdrant_storage"
    api            = "http://127.0.0.1:8000"

    # ── Takeover detection (BEFORE Cleanup — stop.sh clears :8000, so we must capture first) ──
    # If a backend is already live on :8000, THIS start supersedes it. We detect + stamp here,
    # but PRINT inside the Cleanup bundle below (CLI Output STD §2 — a supersede is a Cleanup event).
    _pre = subprocess.run(["lsof", "-ti:8000"], capture_output=True, text=True)
    _stale_pids = _pre.stdout.strip().splitlines() if _pre.stdout.strip() else []
    _superseded_msg = None
    if _stale_pids:
        _now = time.strftime("%Y-%m-%d %H:%M:%S")
        _started = "unknown"
        with contextlib.suppress(Exception):
            _ps = subprocess.run(
                ["ps", "-o", "lstart=", "-p", _stale_pids[0]],
                capture_output=True, text=True,
            )
            _started = _ps.stdout.strip() or "unknown"
        _pidlist = ", ".join(_stale_pids)
        _superseded_msg = (_pidlist, _started)  # printed in Cleanup below (STD §2)
        # (A) record the handoff, timestamped, for the record / ais_status
        with contextlib.suppress(Exception):
            log_dir.mkdir(parents=True, exist_ok=True)
            with open(log_dir / "superseded.log", "a") as _sf:
                _sf.write(
                    f"{_now}  superseded pid(s) {_pidlist} (started {_started}) "
                    f"by new start (pid {os.getpid()})\n"
                )

    # ── Cleanup ───────────────────────────────────────────────────────────────
    _sep("Cleanup", separator)
    # (B) supersede notice — belongs in the Cleanup bundle (STD §2). ⚠ ends with a period;
    # the · sub-detail takes no trailing punctuation (STD §glyphs).
    if _superseded_msg:
        _pidlist, _started = _superseded_msg
        print(f"⚠ Superseding a previous AIStudio backend (pid(s): {_pidlist}, started {_started}).")
        print("· That other terminal's instance is now stale — this window is the live one")
    print("🛑 Stopping any running services...")
    subprocess.run(
        [str(repo / "scripts" / "stop.sh"), "--silent"],
        capture_output=True,   # mask stop.sh banner — internal implementation detail
    )

    # ── Ecosystem ─────────────────────────────────────────────────────────────
    _sep("Ecosystem", separator)

    # Qdrant
    if _health("http://localhost:6333/healthz"):
        print("✅ Qdrant already running.")
    else:
        print("▶ Starting Qdrant...")
        # PARK-20/21: the Qdrant binary is NOT in any backup and is not Homebrew —
        # it's a GitHub release binary (QUICKSTART §5). A missing binary used to crash
        # here with a raw FileNotFoundError; fail with actionable guidance instead.
        if shutil.which("qdrant") is None:
            print("❌ Qdrant binary not found on PATH.")
            print("· Qdrant isn't a Homebrew package — it's a GitHub release binary (QUICKSTART §5).")
            print("· Install (Apple Silicon):")
            print("    mkdir -p ~/bin && cd ~/bin \\")
            print("      && curl -L https://github.com/qdrant/qdrant/releases/latest/download/qdrant-aarch64-apple-darwin.tar.gz | tar xz \\")
            print("      && chmod +x ~/bin/qdrant")
            print("· Then ensure ~/bin is on PATH (source ~/.zshrc) and re-run: ais_start")
            print("· (ais_restore auto-installs the binary if you're recovering from a backup.)")
            return 1
        qdrant_storage.mkdir(parents=True, exist_ok=True)
        qdrant_env = {**os.environ, "QDRANT__STORAGE__STORAGE_PATH": str(qdrant_storage)}
        popen_kwargs: dict = dict(cwd=str(qdrant_storage), env=qdrant_env, start_new_session=True)
        if not args.verbose:
            popen_kwargs.update(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.Popen(["qdrant"], **popen_kwargs)
        for _ in range(10):
            time.sleep(1)
            if _health("http://localhost:6333/healthz"):
                break
        if not _health("http://localhost:6333/healthz"):
            print("❌ Qdrant binary launched but did not become healthy after 10s.")
            print("· Check it runs: ~/bin/qdrant --version")
            print("· Check the storage dir isn't locked: ls ~/qdrant_storage")
            return 1
        print("✅ Qdrant started.")

    # Ollama
    if _ollama_chat_model_count() > 0:
        print("✅ Ollama already running.")
    else:
        print("▶ Starting Ollama...")
        popen_kwargs = {}
        if not args.verbose:
            popen_kwargs = dict(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        popen_kwargs["start_new_session"] = True  # A1c: detach so launchd doesn't reap it when the agent exits
        subprocess.Popen(["ollama", "serve"], **popen_kwargs)
        for _ in range(15):
            time.sleep(1)
            if _ollama_chat_model_count() > 0:
                break
        if _ollama_chat_model_count() == 0:
            _dm = _resolve_default_model(repo) or "gemma3:4b"
            print("❌ No chat models found in Ollama — AIStudio can't answer queries.")
            print(f"· Pull the default model:  ollama pull {_dm}")
            print("· (First pull is a few-GB download; smaller models like gemma3:4b are quickest.)")
            print("· Any Ollama chat model works — if you pull a different one, start with:")
            print("    AISTUDIO_DEFAULT_MODEL=<that-model> ais_start   (or export it in ~/.zshrc)")
            return 1
        print("✅ Ollama started.")

    # ── Resolve the model the backend will actually use (C18 / #888 guard) ────
    # Decide BEFORE launching the backend so it runs with a model that EXISTS.
    # default present → use it. default absent but other model(s) present →
    # fall back to an available one FOR THIS SESSION (transparent) so the first
    # query can't 500. Zero models was already a hard fail above.
    _present = _ollama_chat_models()
    _default = _resolve_default_model(repo)
    _active_model = _default
    _model_overridden = False
    if _default and _present and _default not in _present:
        _active_model = sorted(_present)[0]
        _model_overridden = True

    # ── Backend (continues the Ecosystem bundle — no separator per STD §2) ────
    print("▶ Starting AIStudio backend...")

    log_dir.mkdir(parents=True, exist_ok=True)

    # Kill stale process on port 8000 (belt-and-suspenders; Cleanup's stop.sh usually
    # cleared it already. Takeover announcement/stamp happens BEFORE Cleanup — see top of main).
    result = subprocess.run(["lsof", "-ti:8000"], capture_output=True, text=True)
    if result.stdout.strip():
        for pid in result.stdout.strip().splitlines():
            with contextlib.suppress(Exception):
                subprocess.run(["kill", pid], capture_output=True)
        time.sleep(1)

    backend_env = {
        **os.environ,
        "OLLAMA_KEEP_ALIVE": "30m",
        "AISTUDIO_VECTORSTORE": "qdrant",
        "PYTHONPATH": str(repo / "src"),
    }
    # If the configured default isn't installed, run the backend on an available
    # model for this session so the first query can't 500 (#888). Transparent —
    # announced after startup with how to make it permanent.
    if _model_overridden and _active_model:
        backend_env["AISTUDIO_DEFAULT_MODEL"] = _active_model
    # Use bare 'uvicorn' — venv is activated by wrapper before exec, so
    # venv/bin/ is already on PATH. Matches old shell behavior exactly.
    cmd = ["uvicorn", "local_llm_bot.app.api:app", "--host", "0.0.0.0", "--port", "8000"]

    if args.verbose:
        subprocess.Popen(cmd, env=backend_env, cwd=str(repo), start_new_session=True)
    else:
        # ExitStack lets us keep the log file open for the daemon's lifetime
        # without triggering SIM115 — context manager is present, just not closed.
        stack = contextlib.ExitStack()
        lf = stack.enter_context(open(log_file, "w"))  # noqa: SIM115 — intentional: fd kept open for daemon Popen
        subprocess.Popen(cmd, env=backend_env, cwd=str(repo), stdout=lf, stderr=lf, start_new_session=True)

    # AIStudio_714: poll every 1s up to 60s — open browser on first healthy response.
    # Cold start takes ~20s (CrossEncoder reranker loads weights before first request).
    print("  · Waiting for backend (loading model weights, up to 60s)...")
    backend_ready = False
    for i in range(60):
        time.sleep(1)
        if _health(f"{api}/health"):
            backend_ready = True
            break
        if (i + 1) % 10 == 0:
            print(f"  · Still waiting... ({i + 1}s)")

    if backend_ready:
        print("✅ Backend started.")
        # C18: make the model AIStudio will actually use visible at startup — the #888
        # trap (a stale/absent default that 500s the first query) is otherwise invisible.
        if _active_model:
            if _model_overridden:
                only = " (your only installed model)" if len(_present) == 1 else ""
                print(f"⚠ Configured default '{_default}' is NOT installed.")
                print(f"· Using '{_active_model}'{only} for THIS session so queries work.")
                print(f"· Make it permanent — either install the default:  ollama pull {_default}")
                print(f"  or set your model as the default:  export AISTUDIO_DEFAULT_MODEL={_active_model}  (add to ~/.zshrc)")
            else:
                print(f"· Default model: {_active_model}  (override: AISTUDIO_DEFAULT_MODEL)")
    else:
        # AIStudio_715: do NOT open browser if backend failed to start
        print("❌ Backend did not start after 60s.")
        print("· Check logs: ais_log")
        print("· To retry: ais_start")
        return 1

    # ── Processing ────────────────────────────────────────────────────────────
    # demo and help ship with the repo (tracked in git, data/corpora/).
    # On first run their Qdrant collections are empty — trigger ingest via
    # the backend API (fire-and-forget; UI shows live progress).
    # Subsequent starts: collections already populated, just report count.
    _sep("Processing", separator)

    for corpus in ("demo", "help"):
        count = _qdrant_collection_count(f"aistudio_{corpus}")
        if count > 0:
            print(f"✅ {corpus} corpus: {count} chunks.")
        else:
            print(f"▶ First run: indexing {corpus} corpus in background...")
            try:
                req = urllib.request.Request(
                    f"{api}/corpus/{corpus}/ingest",
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    data=b"{}",
                )
                urllib.request.urlopen(req, timeout=5)
                print(f"  · {corpus} indexing started — UI will show progress.")
            except Exception as e:
                print(f"  ⚠ Could not trigger {corpus} ingest: {e}")

    # ── Reporting ─────────────────────────────────────────────────────────────
    _sep("Reporting", separator)
    if args.start_with:
        print(f"▶ Opening frontend with corpus: {args.start_with}...")
    else:
        print("▶ Opening frontend...")

    if not args.no_open:
        url = f"file://{frontend}"
        if args.start_with:
            url += f"#corpus={args.start_with}"
        webbrowser.open(url)

    if args.start_with:
        print(f"✅ AIStudio is running — corpus: {args.start_with}.")
    else:
        print("✅ AIStudio is running.")
        print("· Tip: use --start_with <corpus> to open on a specific corpus.")

    # ── (References — part of Reporting bundle, no separator) ─────────────────
    print(f"· Frontend : {frontend}")
    print(f"· Backend  : {api}")
    print("· Qdrant   : http://localhost:6333")
    print("· Ollama   : http://localhost:11434")
    print("· Logs     : ais_log")

    # ── (Next commands — part of Reporting bundle, no separator) ──────────────
    print("· To stop  : ais_stop")
    print("· To restart: ais_start")
    if args.verbose:
        print("· Verbose mode active.")

    # ── Show splash ───────────────────────────────────────────────────────────
    if args.show_splash:
        subprocess.run(
            ["osascript", "-e",
             f'display dialog "AIStudio is running.\\n\\nFrontend: file://{frontend}\\n'
             f'Backend:  {api}" with title "AIStudio" buttons {{"OK"}} '
             f'default button "OK" with icon note'],
            capture_output=True,
        )

    # ── Show log tab (iTerm2) ─────────────────────────────────────────────────
    if args.show_log:
        subprocess.run(
            ["osascript", "-e",
             'tell application "iTerm2" to tell current window to create tab '
             'with default profile'],
            capture_output=True,
        )
        subprocess.run(
            ["osascript", "-e",
             f'tell application "iTerm2" to tell current window to tell current session '
             f'to write text "tail -f \'{log_file}\'"'],
            capture_output=True,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
