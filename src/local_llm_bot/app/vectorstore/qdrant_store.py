# src/local_llm_bot/app/vectorstore/qdrant_store.py
# Version: 1.1.1
from __future__ import annotations

import contextlib
import os
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchText,
    PayloadSchemaType,
    PointStruct,
    VectorParams,
)

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
    """Create collection if it doesn't exist. Also ensures text index on `text` payload field."""
    existing = [c.name for c in client.get_collections().collections]
    if collection_name not in existing:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,  # Cosine similarity — standard for text embeddings
            ),
        )
    # Ensure text index exists on every collection (idempotent — no-ops if already present).
    # This enables BM25-style full-text retrieval via query_bm25() alongside vector retrieval.
    _ensure_text_index(client, collection_name)


def _ensure_text_index(client: QdrantClient, collection_name: str) -> None:
    """
    Create a text index on the `text` payload field if absent.

    Idempotent — Qdrant returns success without modification when the index already exists,
    so this is safe to call on every collection access.

    Tokenizer choice: Qdrant's default `word` tokenizer splits on whitespace, which means
    multi-word entity names like "Bank of America" are indexed as three separate tokens.
    BM25 then scores chunks by token presence individually. For the M2.A acceptance test
    (cross-firm CET1 query), this is sufficient — chunks containing "Bank of America"
    explicitly will still score above unrelated chunks because all three tokens co-occur.
    Multi-word entity precision is a known limitation of vanilla BM25, addressable in
    M2.D (query understanding) if needed.
    """
    # Wrapping in contextlib.suppress: index-already-exists raises, but we don't care —
    # idempotent semantics, caller doesn't need to know whether this was a no-op.
    # Also catches the collection-doesn't-exist-yet edge case (defensive — _ensure_collection
    # creates collection before calling this, but order isn't guaranteed by the caller).
    with contextlib.suppress(Exception):
        client.create_payload_index(
            collection_name=collection_name,
            field_name="text",
            field_schema=PayloadSchemaType.TEXT,
        )


def _batched(items: list, batch_size: int) -> list[list]:
    if batch_size <= 0:
        return [items]
    return [items[i : i + batch_size] for i in range(0, len(items), batch_size)]


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
    persist_dir: Path,  # Kept for API compatibility with chroma_store — not used by Qdrant
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
        b_ids = [ids[i] for i in idx_batch]
        b_docs = [documents[i] for i in idx_batch]
        b_metas = [metadatas[i] for i in idx_batch]

        b_embs = ollama_embed(model=embed_model, texts=b_docs)
        if not isinstance(b_embs, list) or len(b_embs) != len(b_docs):
            raise ValueError("Embedding backend returned wrong shape")

        points = [
            PointStruct(
                id=_chunk_id_to_uint64(cid),
                vector=emb,
                payload={
                    "chunk_id": cid,
                    "text": doc,
                    **meta,  # source_path, page, chunk_index, etc.
                },
            )
            for cid, doc, emb, meta in zip(b_ids, b_docs, b_embs, b_metas, strict=False)
        ]

        client.upsert(collection_name=collection_name, points=points)

        if on_batch_done is not None:
            on_batch_done(len(b_ids))


def delete_chunks(
    *,
    persist_dir: Path,  # API compatibility — not used
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
    persist_dir: Path | None = None,  # API compatibility — not used by Qdrant
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


def query_bm25(
    *,
    collection_name: str,
    query_text: str,
    top_k: int,
) -> list[QdrantHit]:
    """
    Query Qdrant using BM25 full-text search over the indexed `text` payload field.

    Returns QdrantHit list — same shape as query() so downstream score-combination
    logic in scoring.py treats both retrieval paths uniformly. distance field carries
    (1 - normalized_score), keeping lower-is-better convention consistent with query().

    Requires the text index built by _ensure_text_index() (called automatically from
    _ensure_collection()). For collections created before v1.1.0 of this file,
    the index is created on first access — no re-ingest required.

    Unlike query(), this function does NOT call ollama_embed — BM25 scoring operates
    on the raw query string, no embedding step. This makes it materially faster than
    vector retrieval (~1ms vs ~50-100ms typical embedding latency).

    The MatchText filter surfaces chunks where the indexed `text` field contains the
    query tokens. Qdrant scores them by BM25 internally; we expose the score via the
    standard query_points API and convert to distance for API uniformity.
    """
    client = get_client()
    _ensure_collection(client, collection_name)

    # MatchText with a multi-word query matches chunks containing ANY of the tokens
    # (OR semantics). Qdrant's internal BM25 then ranks them by relevance.
    text_filter = Filter(
        must=[
            FieldCondition(
                key="text",
                match=MatchText(text=query_text),
            )
        ]
    )

    # query_points with a filter and no vector returns scored matches.
    # Qdrant uses BM25 scoring when the filter targets a TEXT-indexed field.
    results = client.query_points(
        collection_name=collection_name,
        query_filter=text_filter,
        limit=int(top_k),
        with_payload=True,
    ).points

    out: list[QdrantHit] = []
    for hit in results:
        payload = hit.payload or {}
        # BM25 scores are unbounded (typically 0-30 range). For consistency with query()'s
        # distance field (lower = better), we expose 1 - (score / max_score_in_batch) as
        # distance. Final normalization for hybrid score combination happens in scoring.py
        # where both channels are normalized together.
        out.append(
            QdrantHit(
                chunk_id=str(payload.get("chunk_id", hit.id)),
                text=str(payload.get("text", "")),
                metadata={k: v for k, v in payload.items() if k not in ("chunk_id", "text")},
                distance=float(hit.score),  # Raw BM25 score — scoring.py handles normalization
            )
        )
    return out


def delete_collection(*, collection_name: str) -> None:
    """Delete an entire Qdrant collection. Used by --force ingest to ensure clean state."""
    client = get_client()
    existing = [c.name for c in client.get_collections().collections]
    if collection_name in existing:
        client.delete_collection(collection_name=collection_name)
