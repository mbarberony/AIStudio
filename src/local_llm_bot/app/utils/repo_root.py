from __future__ import annotations

from pathlib import Path


def find_repo_root(start: Path) -> Path:
    """
    Walk up from `start` until we find pyproject.toml.
    """
    p = start.resolve()
    for _ in range(15):
        if (p / "pyproject.toml").exists():
            return p
        if p.parent == p:
            break
        p = p.parent
    raise RuntimeError("Could not locate repo root (pyproject.toml not found).")
