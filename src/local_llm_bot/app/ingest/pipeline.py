from __future__ import annotations

from pathlib import Path

from tqdm import tqdm  # type: ignore

from .chunking import chunk_document
from .index import write_jsonl
from .loaders import SUPPORTED_EXTS, load_document


def ingest_directory(
    root: Path, out_index: Path, chunk_size: int = 1200, overlap: int = 200
) -> int:
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Root directory does not exist or is not a directory: {root}")

    paths = [
        p
        for p in root.rglob("*")
        if p.is_file()
        and p.suffix.lower() in SUPPORTED_EXTS
        and not p.name.startswith("~$")  # Word lock files
    ]

    all_chunks = []
    chunk_count = 0
    for path in tqdm(paths, desc="Ingesting files", unit="file"):
        doc = load_document(path)
        if not doc:
            continue
        chunks = chunk_document(doc, chunk_size=chunk_size, overlap=overlap)
        chunk_count += len(chunks)
        all_chunks.extend(chunks)

    write_jsonl(all_chunks, out_index)
    print(f"Indexed {chunk_count} chunks from {len(paths)} files into {out_index}")
    return len(all_chunks)


# def ingest_directory(
#     root: Path,
#     out_index: Path,
#     chunk_size: int = 1200,
#     overlap: int = 200,
# ) -> int:
#     if not root.exists() or not root.is_dir():
#         raise ValueError(f"Root directory does not exist or is not a directory: {root}")
#
#     all_chunks = []
#     for path in root.rglob("*"):
#
#         if not path.is_file():
#             continue
#         if path.name.startswith("~$"):
#             continue
#         if path.suffix.lower() not in SUPPORTED_EXTS:
#             continue
#
#
#         doc = load_document(path)
#         if not doc:
#             continue
#         all_chunks.extend(chunk_document(doc, chunk_size=chunk_size, overlap=overlap))
#
#     write_jsonl(all_chunks, out_index)
#     return len(all_chunks)
