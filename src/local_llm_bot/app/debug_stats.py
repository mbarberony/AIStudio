from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from local_llm_bot.app.ingest.index_jsonl import read_jsonl
from local_llm_bot.app.utils.paths import find_repo_root


@dataclass(frozen=True)
class JsonlStats:
    data_dir: str
    index_path: str
    manifest_path: str
    failures_path: str
    docmap_path: str

    chunks_total: int
    docs_unique: int
    sources_unique: int
    failures_total: int
    manifest_entries: int
    docmap_entries: int

    bytes_index: int
    bytes_manifest: int
    bytes_failures: int

    top_sources: list[tuple[str, int]]


def _size(p: Path) -> int:
    try:
        return p.stat().st_size
    except Exception:
        return 0


def _read_docmap(path: Path) -> dict[str, list[str]]:
    if not path.exists():
        return {}
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(obj, dict):
            out: dict[str, list[str]] = {}
            for k, v in obj.items():
                if (
                    isinstance(k, str)
                    and isinstance(v, list)
                    and all(isinstance(x, str) for x in v)
                ):
                    out[k] = v
            return out
    except Exception:
        return {}
    return {}


def compute_jsonl_stats(data_dir: Path | None = None, *, top_n: int = 10) -> JsonlStats:
    repo_root = find_repo_root(Path(__file__))
    data = data_dir or (repo_root / "data")

    index_path = data / "index.jsonl"
    manifest_path = data / "manifest.jsonl"
    failures_path = data / "ingest_failures.jsonl"
    docmap_path = data / "doc_chunk_map.json"

    rows = read_jsonl(index_path)
    chunks_total = len(rows)

    doc_ids: set[str] = set()
    sources: set[str] = set()
    source_counts: dict[str, int] = {}

    for r in rows:
        doc_id = str(r.get("doc_id", ""))
        src = str(r.get("source_path", ""))
        if doc_id:
            doc_ids.add(doc_id)
        if src:
            sources.add(src)
            source_counts[src] = source_counts.get(src, 0) + 1

    failures_total = len(read_jsonl(failures_path))
    manifest_entries = len(read_jsonl(manifest_path))
    docmap = _read_docmap(docmap_path)

    top_sources = sorted(source_counts.items(), key=lambda kv: kv[1], reverse=True)[:top_n]

    return JsonlStats(
        data_dir=str(data),
        index_path=str(index_path),
        manifest_path=str(manifest_path),
        failures_path=str(failures_path),
        docmap_path=str(docmap_path),
        chunks_total=chunks_total,
        docs_unique=len(doc_ids),
        sources_unique=len(sources),
        failures_total=failures_total,
        manifest_entries=manifest_entries,
        docmap_entries=len(docmap),
        bytes_index=_size(index_path),
        bytes_manifest=_size(manifest_path),
        bytes_failures=_size(failures_path),
        top_sources=top_sources,
    )
