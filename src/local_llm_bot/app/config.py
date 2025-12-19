from __future__ import annotations

from typing import Final

DEFAULT_CORPUS_DIRECTORY: Final[str] = "/Users/mbarbero2018/Documents"

# Chunking defaults (should match your ingest defaults)
DEFAULT_CHUNK_SIZE: Final[int] = 1200
DEFAULT_OVERLAP: Final[int] = 200

# Embedding sizing assumptions (for estimates)
DEFAULT_EMBED_DIM: Final[int] = 768
DEFAULT_FLOAT_BYTES: Final[int] = 4  # float32

# Chroma/SQLite/HNSW + metadata overhead is workload-dependent.
# We report a range using these factors.
DEFAULT_OVERHEAD_LOW: Final[float] = 1.3
DEFAULT_OVERHEAD_HIGH: Final[float] = 2.5

# Rough throughput knobs (tune after one real run on your Mac)
DEFAULT_PARSE_FILES_PER_SEC: Final[float] = 6.0
DEFAULT_EMBED_CHUNKS_PER_SEC: Final[float] = 2.0

# XLSX extraction safety cap (avoid scanning enormous spreadsheets forever)
DEFAULT_XLSX_MAX_CELLS: Final[int] = 50_000


def default_excludes() -> list[str]:
    """
    Opinionated excludes for 'index everything' on macOS.
    These patterns apply to full path strings via fnmatch.
    """
    return [
        "*/.git/*",
        "*/.venv/*",
        "*/__pycache__/*",
        "*/node_modules/*",
        "*/.pytest_cache/*",
        "*/.mypy_cache/*",
        "*/.ruff_cache/*",
        "*/.DS_Store",
        "*/Library/*",
        "*/Applications/*",
        "*/System/*",
        "*/Volumes/*",
        "*/.Trash/*",
        "*/.Trash",
        "*/Pictures/*",
        "*/Photos Library.photoslibrary/*",
        "*/Movies/*",
        "*/Music/*",
        "*/iPhoto Library.photolibrary/*",
        "*/iTunes/*",
        "*/MobileSync/*",  # iOS backups
        "*/Caches/*",
        "*/Cache/*",
        "*/.cache/*",
        "*/DerivedData/*",  # Xcode
        "*/Parallels/*",
        "*/Virtual Machines.localized/*",
    ]
