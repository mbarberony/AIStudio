from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ManifestEntry:
    """
    One line per file ingested (stored in manifest.jsonl).

    We use (path, mtime, size) to detect changes.
    """

    path: str
    mtime: int
    size: int


def _safe_stat(path: Path) -> tuple[int, int]:
    st = path.stat()
    # Use integer seconds to keep stable across platforms
    mtime = int(st.st_mtime)
    size = int(st.st_size)
    return mtime, size


def load_manifest_map(manifest_path: Path) -> dict[str, ManifestEntry]:
    """
    Load manifest.jsonl into a dict keyed by absolute path string.
    Newer entries overwrite older ones.
    """
    out: dict[str, ManifestEntry] = {}
    if not manifest_path.exists():
        return out

    with manifest_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj: dict[str, Any] = json.loads(line)
                p = str(obj.get("path", ""))
                if not p:
                    continue
                out[p] = ManifestEntry(
                    path=p,
                    mtime=int(obj.get("mtime", 0)),
                    size=int(obj.get("size", 0)),
                )
            except Exception:
                # Corrupt line: ignore, keep going
                continue
    return out


def write_manifest_entry(manifest_path: Path, entry: ManifestEntry) -> None:
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"path": entry.path, "mtime": entry.mtime, "size": entry.size}) + "\n")


def should_skip(
    *,
    source_path: Path,
    manifest_map: dict[str, ManifestEntry],
    force: bool = False,
) -> bool:
    """
    Return True if we should skip ingesting this file because it appears unchanged.

    - force=True => never skip
    """
    if force:
        return False

    abs_path = str(source_path.resolve())
    prev = manifest_map.get(abs_path)
    if prev is None:
        return False

    try:
        mtime, size = _safe_stat(source_path)
    except FileNotFoundError:
        # If it disappeared, skip (it will be handled via stale-chunk removal elsewhere)
        return True

    return (prev.mtime == mtime) and (prev.size == size)


def build_entry(source_path: Path) -> ManifestEntry:
    """
    Helper: create a ManifestEntry from a file path.
    """
    mtime, size = _safe_stat(source_path)
    return ManifestEntry(path=str(source_path.resolve()), mtime=mtime, size=size)
