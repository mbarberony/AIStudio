from __future__ import annotations

from .types import Chunk, Document


def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be < chunk_size")

    text = text.strip()
    if not text:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = end - overlap
    return chunks


def chunk_document(doc: Document, chunk_size: int = 1200, overlap: int = 200) -> list[Chunk]:
    parts = chunk_text(doc.text, chunk_size=chunk_size, overlap=overlap)
    out: list[Chunk] = []
    for i, part in enumerate(parts):
        out.append(
            Chunk(
                chunk_id=f"{doc.doc_id}::chunk-{i}",
                doc_id=doc.doc_id,
                source_path=doc.source_path,
                text=part,
            )
        )
    return out
