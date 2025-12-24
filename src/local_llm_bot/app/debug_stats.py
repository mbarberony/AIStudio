from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from local_llm_bot.app.ingest.index_jsonl import read_jsonl
from local_llm_bot.app.utils.corpus_paths import corpus_paths
from local_llm_bot.app.utils.repo_root import find_repo_root


def _count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())


def _safe_size(path: Path) -> int:
    return path.stat().st_size if path.exists() else 0


def _load_docmap(path: Path) -> dict[str, list[str]]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            # best-effort validation
            out: dict[str, list[str]] = {}
            for k, v in data.items():
                if isinstance(k, str) and isinstance(v, list):
                    out[k] = [str(x) for x in v]
            return out
        return {}
    except Exception:
        return {}


@dataclass(frozen=True)
class JsonlStats:
    data_dir: Path

    # core counts
    chunks_total: int
    docs_unique: int
    sources_unique: int

    # artifact counts
    manifest_entries: int
    failures_total: int
    docmap_entries: int

    # sizes
    index_bytes: int
    manifest_bytes: int
    failures_bytes: int


def compute_jsonl_stats(*, data_dir: Path | None = None, corpus: str = "default") -> JsonlStats:
    """
    Returns a typed stats object for JSONL artifacts.
    - If `data_dir` is provided, reads artifacts from that directory (great for tests).
    - Otherwise, resolves the named `corpus` under the repo's data directory.
    """
    if data_dir is not None:
        base = Path(data_dir)
        paths = {
            "base": base,
            "index": base / "index.jsonl",
            "manifest": base / "manifest.jsonl",
            "failures": base / "ingest_failures.jsonl",
            "docmap": base / "doc_chunk_map.json",
        }
    else:
        repo_root = find_repo_root(Path(__file__))
        paths = corpus_paths(repo_root, corpus)

    rows = read_jsonl(paths["index"])

    # unique doc_id/source_path
    doc_ids = {str(r.get("doc_id")) for r in rows if r.get("doc_id")}
    sources = {str(r.get("source_path")) for r in rows if r.get("source_path")}

    chunks_total = len(rows)
    docs_unique = len(doc_ids)
    sources_unique = len(sources)

    manifest_entries = _count_jsonl(paths["manifest"])
    failures_total = _count_jsonl(paths["failures"])
    docmap_entries = len(_load_docmap(paths["docmap"]))

    return JsonlStats(
        data_dir=Path(paths["base"]),
        chunks_total=chunks_total,
        docs_unique=docs_unique,
        sources_unique=sources_unique,
        manifest_entries=manifest_entries,
        failures_total=failures_total,
        docmap_entries=docmap_entries,
        index_bytes=_safe_size(paths["index"]),
        manifest_bytes=_safe_size(paths["manifest"]),
        failures_bytes=_safe_size(paths["failures"]),
    )


def compute_stats(*, corpus: str = "default", top_n: int = 10) -> dict[str, Any]:
    """
    Dict-shaped stats for API responses (JSON-serializable).
    """
    repo_root = find_repo_root(Path(__file__))
    paths = corpus_paths(repo_root, corpus)

    rows = read_jsonl(paths["index"])
    sources_list = [str(r.get("source_path", "")) for r in rows if r.get("source_path")]

    counts: dict[str, int] = {}
    for s in sources_list:
        counts[s] = counts.get(s, 0) + 1

    top_sources = sorted(
        [{"source": k, "chunks": v} for k, v in counts.items()],
        key=lambda x: x["chunks"],
        reverse=True,
    )[:top_n]

    s = compute_jsonl_stats(corpus=corpus)

    return {
        "corpus": corpus,
        "data_dir": str(s.data_dir),
        "paths": {k: str(v) for k, v in paths.items()},
        "counts": {
            "chunks_total": s.chunks_total,
            "docs_unique": s.docs_unique,
            "sources_unique": s.sources_unique,
            "manifest_entries": s.manifest_entries,
            "failures_total": s.failures_total,
            "docmap_entries": s.docmap_entries,
        },
        "bytes": {
            "index": s.index_bytes,
            "manifest": s.manifest_bytes,
            "failures": s.failures_bytes,
        },
        "top_sources": top_sources,
    }
