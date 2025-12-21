from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ChunkRow:
    chunk_id: str
    doc_id: str
    source_path: str
    text: str


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                # ignore malformed lines
                continue
    return rows


def append_rows(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def rewrite_excluding_doc(index_path: Path, tmp_path: Path, doc_id: str) -> None:
    """
    Remove all chunks from index.jsonl with doc_id == doc_id.
    Rewrite to tmp then atomic replace.
    """
    if not index_path.exists():
        return

    with index_path.open("r", encoding="utf-8") as src, tmp_path.open("w", encoding="utf-8") as dst:
        for line in src:
            s = line.strip()
            if not s:
                continue
            try:
                row = json.loads(s)
            except Exception:
                # keep unknown/malformed lines out of the new file
                continue
            if str(row.get("doc_id", "")) == doc_id:
                continue
            dst.write(line if line.endswith("\n") else line + "\n")

    tmp_path.replace(index_path)


def load_doc_chunk_map(path: Path) -> dict[str, list[str]]:
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


def save_doc_chunk_map(path: Path, docmap: dict[str, list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(docmap, indent=2, ensure_ascii=False), encoding="utf-8")
