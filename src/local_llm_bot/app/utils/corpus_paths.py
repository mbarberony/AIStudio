from __future__ import annotations

from pathlib import Path


def corpus_base_dir(repo_root: Path, corpus: str) -> Path:
    return repo_root / "data" / "corpora" / corpus


def corpus_paths(repo_root: Path, corpus: str) -> dict[str, Path]:
    """
    Return all data artifact paths for a named corpus.
    Creates the base directory if needed.
    """
    base = corpus_base_dir(repo_root, corpus)
    base.mkdir(parents=True, exist_ok=True)

    chroma_dir = base / "chroma"
    chroma_dir.mkdir(parents=True, exist_ok=True)

    return {
        "base": base,
        "index": base / "index.jsonl",
        "manifest": base / "manifest.jsonl",
        "failures": base / "ingest_failures.jsonl",
        "docmap": base / "doc_chunk_map.json",
        "chroma": chroma_dir,
    }
