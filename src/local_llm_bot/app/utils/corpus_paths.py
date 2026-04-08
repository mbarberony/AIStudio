from __future__ import annotations

from pathlib import Path


def corpus_base_dir(repo_root: Path, corpus: str) -> Path:
    return repo_root / "data" / "corpora" / corpus


def corpus_paths(repo_root: Path, corpus: str) -> dict[str, Path]:
    """
    Return all data artifact paths for a named corpus.
    Creates the base directory if needed.

    Path layout:
        data/corpora/<n>/
            uploads/          ← live source files only (no subdirs)
            trash/            ← deleted files (sibling of uploads, not inside it)
            index.jsonl       ← chunk metadata (JSONL — legacy, kept as audit log)
            manifest.jsonl    ← ingest manifest (JSONL — legacy, kept as audit log)
            ingest_failures.jsonl
            doc_chunk_map.json

    trash/ is a sibling of uploads/, not a subdirectory.
    This ensures pipeline.py ingest (rooted at uploads/) never sees deleted files.
    """
    base = corpus_base_dir(repo_root, corpus)
    base.mkdir(parents=True, exist_ok=True)

    return {
        "base": base,
        "uploads": base / "uploads",
        "trash": base / "trash",  # sibling of uploads/ — never inside it
        "index": base / "index.jsonl",
        "manifest": base / "manifest.jsonl",
        "failures": base / "ingest_failures.jsonl",
        "docmap": base / "doc_chunk_map.json",
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
