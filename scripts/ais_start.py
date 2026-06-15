# Version: 1.1.0
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
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path

SCRIPT_NAME = "ais_start"
VERSION = "1.1.0"

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

    # ── Cleanup ───────────────────────────────────────────────────────────────
    _sep("Cleanup", separator)
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
        qdrant_storage.mkdir(parents=True, exist_ok=True)
        qdrant_env = {**os.environ, "QDRANT__STORAGE__STORAGE_PATH": str(qdrant_storage)}
        popen_kwargs: dict = dict(cwd=str(qdrant_storage), env=qdrant_env)
        if not args.verbose:
            popen_kwargs.update(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.Popen(["qdrant"], **popen_kwargs)
        for _ in range(10):
            time.sleep(1)
            if _health("http://localhost:6333/healthz"):
                break
        print("✅ Qdrant started.")

    # Ollama
    if _ollama_chat_model_count() > 0:
        print("✅ Ollama already running.")
    else:
        print("▶ Starting Ollama...")
        popen_kwargs = {}
        if not args.verbose:
            popen_kwargs = dict(stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.Popen(["ollama", "serve"], **popen_kwargs)
        for _ in range(15):
            time.sleep(1)
            if _ollama_chat_model_count() > 0:
                break
        if _ollama_chat_model_count() == 0:
            print("❌ No chat models found in Ollama.")
            print("· Run: ollama pull llama3.1:8b")
            print("· This takes ~5 minutes on first run (~4.7 GB download).")
            return 1
        print("✅ Ollama started.")

    # ── Backend (continues the Ecosystem bundle — no separator per STD §2) ────
    print("▶ Starting AIStudio backend...")

    log_dir.mkdir(parents=True, exist_ok=True)

    # Kill stale process on port 8000
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
    # Use bare 'uvicorn' — venv is activated by wrapper before exec, so
    # venv/bin/ is already on PATH. Matches old shell behavior exactly.
    cmd = ["uvicorn", "local_llm_bot.app.api:app", "--host", "0.0.0.0", "--port", "8000"]

    if args.verbose:
        subprocess.Popen(cmd, env=backend_env, cwd=str(repo))
    else:
        # ExitStack lets us keep the log file open for the daemon's lifetime
        # without triggering SIM115 — context manager is present, just not closed.
        stack = contextlib.ExitStack()
        lf = stack.enter_context(open(log_file, "w"))  # noqa: SIM115 — intentional: fd kept open for daemon Popen
        subprocess.Popen(cmd, env=backend_env, cwd=str(repo), stdout=lf, stderr=lf)

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
