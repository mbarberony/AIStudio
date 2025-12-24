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


def _bool(s: str) -> bool:
    v = s.strip().lower()
    if v in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if v in {"0", "false", "f", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"Invalid boolean: {s!r}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m local_llm_bot.app.ingest")
    p.add_argument("--corpus", default="default", help="Corpus name (under data/corpora/)")
    p.add_argument("--root", required=True, help="Directory to ingest (recursive)")

    # Reset / incremental controls
    p.add_argument(
        "--reset-index", action="store_true", help="Reset JSONL artifacts for this corpus"
    )
    p.add_argument(
        "--reset-chroma", action="store_true", help="Also delete Chroma persist dir for this corpus"
    )
    p.add_argument(
        "--force", action="store_true", help="Force reprocessing even if manifest shows unchanged"
    )

    # CLI overrides
    p.add_argument("--use-chroma", type=_bool, default=None, help="Override CONFIG.rag.use_chroma")
    p.add_argument("--chunk-size", type=int, default=None, help="Override chunk size (chars)")
    p.add_argument("--overlap", type=int, default=None, help="Override overlap (chars)")
    p.add_argument("--embed-model", default=None, help="Override embedding model (Chroma upserts)")
    p.add_argument("--max-files", type=int, default=None, help="Safety cap for a run")

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
        reset_chroma=bool(args.reset_chroma),
        force=bool(args.force),
        use_chroma=args.use_chroma,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        embed_model=args.embed_model,
        max_files=args.max_files,
        tqdm_cls=tqdm,  # <-- key change: pipeline controls bars
    )
    dur = time.time() - t0

    payload = {
        "action": "ingest",
        "corpus": corpus,
        "root": str(root),
        "duration_sec": round(dur, 3),
        "effective_config": {
            "use_chroma": result.use_chroma,
            "chunk_size": result.chunk_size,
            "overlap": result.overlap,
            "embed_model": result.embed_model,
            "default_model": CONFIG.rag.default_model,
        },
        "paths": {k: str(v) for k, v in paths.items()},
        "result": asdict(result),
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
