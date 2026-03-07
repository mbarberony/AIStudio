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

def corpus_exists(repo_root: Path, corpus: str) -> bool:
    """Return True if the named corpus directory exists."""
    return corpus_base_dir(repo_root, corpus).exists()

def list_corpora(repo_root: Path) -> list[str]:
    """Return a list of all corpus names found under data/corpora/."""
    corpora_dir = repo_root / "data" / "corpora"
    if not corpora_dir.exists():
        return []
    return [p.name for p in corpora_dir.iterdir() if p.is_dir()]
