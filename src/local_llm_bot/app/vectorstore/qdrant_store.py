# src/local_llm_bot/app/vectorstore/qdrant_store.py
from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)

from local_llm_bot.app.config import CONFIG
from local_llm_bot.app.ollama_client import ollama_embed

# Qdrant runs locally on port 6333 by default
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))

# Embedding vector size — must match the model used
# nomic-embed-text = 768, mxbai-embed-large = 1024, bge-large = 1024
VECTOR_SIZE = int(os.getenv("AISTUDIO_VECTOR_SIZE", "768"))

DEFAULT_EMBED_BATCH_SIZE = 32


@dataclass(frozen=True)
class QdrantHit:
    """Mirrors ChromaHit exactly so rag_core.py needs no changes."""
    chunk_id: str
    text: str
    metadata: dict[str, Any]
    distance: float


def get_client() -> QdrantClient:
    """Return a Qdrant client connected to the local server."""
    return QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


def _ensure_collection(client: QdrantClient, collection_name: str) -> None:
    """Create collection if it doesn't exist."""
    existing = [c.name for c in client.get_collections().collections]
    if collection_name not in existing:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,  # Cosine similarity — standard for text embeddings
            ),
        )


def _batched(items: list, batch_size: int) -> list[list]:
    if batch_size <= 0:
        return [items]
    return [items[i: i + batch_size] for i in range(0, len(items), batch_size)]


def _chunk_id_to_uint64(chunk_id: str) -> int:
    """
    Qdrant requires integer or UUID point IDs.
    We hash the string chunk_id to a stable uint64.
    Collision probability is negligible for corpus sizes we target.
    """
    import hashlib
    h = hashlib.sha256(chunk_id.encode()).digest()
    return int.from_bytes(h[:8], "big")


def upsert_chunks(
    *,
    persist_dir: Path,           # Kept for API compatibility with chroma_store — not used by Qdrant
    collection_name: str,
    embed_model: str,
    ids: list[str],
    documents: list[str],
    metadatas: list[dict[str, Any]],
    on_batch_done: Callable[[int], None] | None = None,
    batch_size: int | None = None,
) -> None:
    """
    Upsert chunk documents into Qdrant using embeddings from Ollama.
    API-compatible with chroma_store.upsert_chunks.
    """
    if not (len(ids) == len(documents) == len(metadatas)):
        raise ValueError("ids, documents, and metadatas must be the same length")
    if not ids:
        return

    client = get_client()
    _ensure_collection(client, collection_name)

    env_bs = os.getenv("AISTUDIO_EMBED_BATCH_SIZE")
    try:
        env_bs_i = int(env_bs) if env_bs else None
    except ValueError:
        env_bs_i = None

    bs = int(batch_size) if batch_size is not None else int(env_bs_i or DEFAULT_EMBED_BATCH_SIZE)
    if bs <= 0:
        bs = DEFAULT_EMBED_BATCH_SIZE

    for idx_batch in _batched(list(range(len(ids))), bs):
        b_ids    = [ids[i]       for i in idx_batch]
        b_docs   = [documents[i] for i in idx_batch]
        b_metas  = [metadatas[i] for i in idx_batch]

        b_embs = ollama_embed(model=embed_model, texts=b_docs)
        if not isinstance(b_embs, list) or len(b_embs) != len(b_docs):
            raise ValueError("Embedding backend returned wrong shape")

        points = [
            PointStruct(
                id=_chunk_id_to_uint64(cid),
                vector=emb,
                payload={
                    "chunk_id":   cid,
                    "text":       doc,
                    **meta,           # source_path, page, chunk_index, etc.
                },
            )
            for cid, doc, emb, meta in zip(b_ids, b_docs, b_embs, b_metas)
        ]

        client.upsert(collection_name=collection_name, points=points)

        if on_batch_done is not None:
            on_batch_done(len(b_ids))


def delete_chunks(
    *,
    persist_dir: Path,           # API compatibility — not used
    collection_name: str,
    ids: list[str],
) -> None:
    """Delete chunks by string chunk_id."""
    if not ids:
        return
    client = get_client()
    uint_ids = [_chunk_id_to_uint64(cid) for cid in ids]
    client.delete(
        collection_name=collection_name,
        points_selector=uint_ids,
    )


def query(
    *,
    persist_dir: Path,           # API compatibility — not used
    collection_name: str,
    query_text: str,
    top_k: int,
    embed_model: str,
) -> list[QdrantHit]:
    """
    Query Qdrant using a query embedding from Ollama.
    Returns QdrantHit list — identical shape to ChromaHit.
    Distance is 1 - cosine_similarity (lower = more similar).
    """
    client = get_client()
    _ensure_collection(client, collection_name)

    q_emb = ollama_embed(model=embed_model, texts=[query_text])[0]

    from qdrant_client.models import SearchRequest
    results = client.query_points(
        collection_name=collection_name,
        query=q_emb,
        limit=int(top_k),
        with_payload=True,
    ).points

    out: list[QdrantHit] = []
    for hit in results:
        payload = hit.payload or {}
        out.append(
            QdrantHit(
                chunk_id=str(payload.get("chunk_id", hit.id)),
                text=str(payload.get("text", "")),
                metadata={k: v for k, v in payload.items() if k not in ("chunk_id", "text")},
                # Qdrant returns score = cosine similarity (higher = better)
                # Convert to distance (lower = better) for API compatibility
                distance=float(1.0 - hit.score),
            )
        )
    return out
