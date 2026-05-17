from __future__ import annotations

from pathlib import Path


def find_repo_root(start: Path | None = None) -> Path:
    """
    Find repo root by walking up until we see pyproject.toml (or .git).
    Works regardless of src/ layout or refactors.
    """
    p = (start or Path(__file__)).resolve()
    for parent in [p, *p.parents]:
        if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
            return parent
    # Fallback: best-effort
    return p.parents[0]
