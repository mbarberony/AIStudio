from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ManifestEntry:
    path: str
    mtime: float
    size: int
    extracted_chars: int
    chunks: int


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
    return out


def load_manifest(manifest_path: Path) -> dict[str, ManifestEntry]:
    rows = _read_jsonl(manifest_path)
    out: dict[str, ManifestEntry] = {}
    for r in rows:
        p = str(r.get("path", "")).strip()
        if not p:
            continue
        out[p] = ManifestEntry(
            path=p,
            mtime=float(r.get("mtime", 0.0)),
            size=int(r.get("size", 0)),
            extracted_chars=int(r.get("extracted_chars", 0)),
            chunks=int(r.get("chunks", 0)),
        )
    return out


def append_manifest(manifest_path: Path, entry: ManifestEntry) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry.__dict__, ensure_ascii=False) + "\n")


def unchanged(prev: ManifestEntry | None, *, mtime: float, size: int) -> bool:
    if prev is None:
        return False
    return prev.mtime == mtime and prev.size == size
