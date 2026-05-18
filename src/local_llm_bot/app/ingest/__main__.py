from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict
from pathlib import Path

from local_llm_bot.app.config import CONFIG
from local_llm_bot.app.ingest.pipeline import ingest_corpus
from local_llm_bot.app.utils.corpus_paths import corpus_paths
from local_llm_bot.app.utils.repo_root import find_repo_root


def _repo_root() -> Path:
    return find_repo_root(Path(__file__))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m local_llm_bot.app.ingest")
    p.add_argument("--corpus", default="default", help="Corpus name (under data/corpora/)")
    p.add_argument("--root", required=True, help="Directory to ingest (recursive)")

    # Reset / incremental controls
    p.add_argument(
        "--reset-index", action="store_true", help="Reset JSONL artifacts for this corpus"
    )
    p.add_argument(
        "--force", action="store_true", help="Force reprocessing even if manifest shows unchanged"
    )

    # CLI overrides
    p.add_argument("--chunk-size", type=int, default=None, help="Override chunk size (chars)")
    p.add_argument("--overlap", type=int, default=None, help="Override overlap (chars)")
    p.add_argument("--embed-model", default=None, help="Override embedding model")
    p.add_argument("--max-files", type=int, default=None, help="Safety cap for a run")
    p.add_argument("--verbose", action="store_true", help="Print full JSON result payload after summary")

    args = p.parse_args(argv)

    corpus = str(args.corpus).strip()
    root = Path(args.root).expanduser()
    if not root.exists():
        raise SystemExit(f"Path not found: {root}")
    if not root.is_dir():
        raise SystemExit(f"--root must be a directory: {root}")

    # Provide tqdm to pipeline (pipeline will create multiple progress bars)
    try:
        from tqdm import tqdm  # type: ignore
    except Exception:
        tqdm = None  # type: ignore

    repo = _repo_root()
    paths = corpus_paths(repo, corpus)

    t0 = time.time()
    result = ingest_corpus(
        root=root,
        corpus=corpus,
        reset_index=bool(args.reset_index),
        force=bool(args.force),
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        embed_model=args.embed_model,
        max_files=args.max_files,
        tqdm_cls=tqdm,  # <-- key change: pipeline controls bars
    )
    dur = time.time() - t0

    # ── Human-readable summary ──────────────────────────────────────────────
    mins, secs = divmod(int(dur), 60)
    dur_str = f"{mins}m {secs}s" if mins else f"{secs}s"
    avg_chunks = result.chunks_written / result.files_processed if result.files_processed else 0
    avg_secs = dur / result.files_processed if result.files_processed else 0

    # Largest and smallest files by chunk count
    file_stats = result.file_stats or {}
    if file_stats:
        sorted_files = sorted(file_stats.items(), key=lambda x: x[1].get("chunks", 0))
        smallest = sorted_files[0]
        largest = sorted_files[-1]
        size_line = (
            f"· Largest : {largest[0]} ({largest[1].get('chunks', 0):,} chunks)\n"
            f"· Smallest: {smallest[0]} ({smallest[1].get('chunks', 0):,} chunks)"
        )
    else:
        size_line = ""

    failures = result.files_failed or 0
    failure_line = f"· ⚠ Failures : {failures}" if failures else "· Failures  : 0"

    print("")
    print("--- Ingest result")
    print(f"✅ {result.files_processed} files ingested · {result.chunks_written:,} chunks · {dur_str}")
    print(f"· Config    : chunk_size={result.chunk_size} overlap={result.overlap} model={result.embed_model}")
    print(f"· Avg       : {avg_chunks:.0f} chunks/file · {avg_secs:.1f}s/file")
    if size_line:
        print(size_line)
    print(failure_line)

    # ── JSON payload (always written for operator use) ───────────────────
    payload = {
        "action": "ingest",
        "corpus": corpus,
        "root": str(root),
        "duration_sec": round(dur, 3),
        "effective_config": {
            "chunk_size": result.chunk_size,
            "overlap": result.overlap,
            "embed_model": result.embed_model,
            "default_model": CONFIG.rag.default_model,
        },
        "paths": {k: str(v) for k, v in paths.items()},
        "result": asdict(result),
    }
    if args.verbose:
        print("")
        print(json.dumps(payload, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
