# src/local_llm_bot/app/vectorstore/qdrant_store.py
# Version: 1.3.1
# Changelog: 1.3.1 — AIStudio_891: index `firm` payload field (TEXT) in _ensure_text_index
#             so _build_entity_filter's firm-match clause works — corpus-agnostic entity
#             isolation keyed on the chunk's own entity, not source_path/filename. Pairs
#             with pipeline.py v1.8.29 (stamps firm at ingest). Re-ingest required. Also
#             corrects the stale Version line (was 1.2.5; top changelog already 1.3.0).
# Changelog: 1.3.0 — AIStudio_882 (scope application): query()/query_bm25() accept
#             allowed_source_paths — the scope firm-boundary. ANDed with entity_filter:
#             vector path nests two Filter(should=...) OR-clauses inside must=[] (AND-of-ORs,
#             the 1.2.4 idiom); BM25 path adds a second source_path post-filter after the
#             entity one. Empty intersection → zero hits (an out-of-scope firm fails the
#             scope clause). Both params default None = pre-1.3.0 behavior.
# Changelog: 1.2.5 — AIStudio_800 v4: post-filter BM25 results by source_path in Python.
#             Qdrant BM25 path (query_points with MatchText filter, no vector) does not
#             reliably enforce additional payload filters. Fetch 4x candidates then filter
#             client-side to guarantee entity isolation on BM25 channel.
# Changelog: 1.2.4 — AIStudio_800 v3: use nested Filter(should=[entity_conds]) inside
#             must list. Qdrant docs confirm Filter is a valid Condition type — must list
#             accepts both FieldCondition and nested Filter objects. This gives:
#             must=[text_FC, Filter(should=[src1, src2])] = text AND (src1 OR src2).
# Changelog: 1.2.3 — AIStudio_800 v2: nested Filter in must not supported by client.
#             Fix: build combined filter with must=[text_condition] + must_not empty
#             and use should for entity OR, but wrap in outer Filter with must=[text]
#             and a second Filter(should=entity_conds, minimum_should_match=1).
#             Simpler: use two separate must conditions joined via Filter.must list
#             where entity is a plain FieldCondition using MatchText on source_path.
# Changelog: 1.2.2 — AIStudio_800: fix entity_filter ignored on BM25 path.
#             Qdrant Filter(must=[...], should=[entity]) treats should as optional.
#             Fix: nest entity conditions as Filter(should=[...]) inside must list
#             so entity isolation is enforced on both vector and BM25 channels.
# Changelog: 1.2.1 — Fix AIStudio_798: MatchValue does exact match, not substring.
#             Switch to MatchText on source_path field (requires text index).
#             Add source_path text index in _ensure_text_index() — idempotent,
#             no re-ingest needed. Qdrant indexes existing payload on creation.
# Changelog: 1.2.0 — AIStudio_798: add optional payload_filter to query() and query_bm25().
#             Accepts list[str] of filename substrings; matched against source_path field
#             with OR semantics using Qdrant Should. Works for both sec_10k (firm names
#             in filenames) and esef_banks (no firm metadata field needed). No re-ingest.
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
    # AIStudio_798: text index on source_path enables MatchText substring filtering.
    # Idempotent — safe to call on every access. Qdrant indexes existing payload.
    with contextlib.suppress(Exception):
        client.create_payload_index(
            collection_name=collection_name,
            field_name="source_path",
            field_schema=PayloadSchemaType.TEXT,
        )
    # AIStudio_891: text index on `firm` — the intended entity-match field for
    # _build_entity_filter (firm == entity, corpus-agnostic, no source_path/filename
    # dependency). MatchText requires a text index; pipeline.py v1.8.29 stamps firm at
    # ingest. Idempotent — indexes existing payload on creation. Re-ingest required for
    # chunks predating the firm field (they carry no firm to index).
    with contextlib.suppress(Exception):
        client.create_payload_index(
            collection_name=collection_name,
            field_name="firm",
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


def _build_entity_filter(entity_filter: list[str]) -> Filter:
    """
    AIStudio_798: Build a Qdrant OR filter matching source_path against any of the
    provided substrings using MatchText (requires text index on source_path — created
    by _ensure_text_index() on first access, no re-ingest needed).

    MatchText tokenizes the field value and the filter string, then checks for token
    presence. "JPMorgan_Chase" matches any source_path containing that token, e.g.:
    /Users/.../sec_10k/uploads/JPMorgan_Chase_10K_2023-02-21.htm

    OR semantics: chunk is included if source_path contains ANY of the filter strings.
    Also checks firm metadata field if present (sec_10k stores explicit firm field).
    """
    conditions = []
    for token in entity_filter:
        # MatchText substring match on source_path (works for all corpora, no re-ingest)
        conditions.append(FieldCondition(key="source_path", match=MatchText(text=token)))
        # Also match against firm metadata field if present (sec_10k explicit firm field)
        conditions.append(FieldCondition(key="firm", match=MatchText(text=token)))
    return Filter(should=conditions)


def query(
    *,
    persist_dir: Path | None = None,  # API compatibility — not used by Qdrant
    collection_name: str,
    query_text: str,
    top_k: int,
    embed_model: str,
    entity_filter: list[str] | None = None,  # AIStudio_798: OR filter on source_path substrings
    allowed_source_paths: list[str] | None = None,  # AIStudio_882: scope boundary, ANDed with entity_filter
) -> list[QdrantHit]:
    """
    Query Qdrant using a query embedding from Ollama.
    Returns QdrantHit list — identical shape to ChromaHit.
    Distance is 1 - cosine_similarity (lower = more similar).
    """
    client = get_client()
    _ensure_collection(client, collection_name)

    q_emb = ollama_embed(model=embed_model, texts=[query_text])[0]

    # AIStudio_798: per-question entity_filter (OR over source_path substrings).
    # AIStudio_882: allowed_source_paths is the scope boundary — a second OR-clause ANDed
    # with the entity clause (nested Filter(should=...) inside must=[] gives AND-of-ORs, the
    # 1.2.4 idiom). entity=[BNP] AND scope=[6 firms] → BNP only; entity=[HSBC] AND scope=[6] →
    # ∅ (HSBC matches the entity clause but no scope clause); entity=None AND scope=[6] → the 6.
    _clauses = []
    if entity_filter:
        _clauses.append(_build_entity_filter(entity_filter))
    if allowed_source_paths:
        _clauses.append(_build_entity_filter(allowed_source_paths))
    _query_filter = Filter(must=_clauses) if _clauses else None

    results = client.query_points(
        collection_name=collection_name,
        query=q_emb,
        limit=int(top_k),
        with_payload=True,
        query_filter=_query_filter,
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
    entity_filter: list[str] | None = None,  # AIStudio_798: OR filter on source_path substrings
    allowed_source_paths: list[str] | None = None,  # AIStudio_882: scope boundary, ANDed with entity_filter
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
    # AIStudio_800 v2: enforce entity_filter on BM25 path using minimum_should_match=1.
    # Filter(must=[text], should=[entity_conds], minimum_should_match=1) means:
    # - must: chunk text contains query tokens (BM25 scoring)
    # - should with min=1: source_path must match at least one entity token (enforced OR)
    # AIStudio_800 v4: Qdrant BM25 path (MatchText filter, no vector) does not reliably
    # enforce additional payload filters. Use simple text filter for BM25 scoring,
    # then post-filter results by source_path in Python to guarantee entity isolation.
    # Fetch 4x top_k candidates to ensure enough remain after post-filtering.
    # AIStudio_882: the scope boundary (allowed_source_paths) is enforced the same way —
    # a second AND post-filter — so widen the candidate pool when EITHER firm filter is set.
    _any_firm_filter = bool(entity_filter or allowed_source_paths)
    _bm25_fetch_k = int(top_k) * 4 if _any_firm_filter else int(top_k)
    text_filter = Filter(
        must=[FieldCondition(key="text", match=MatchText(text=query_text))]
    )

    # query_points with a filter and no vector returns scored matches.
    # Qdrant uses BM25 scoring when the filter targets a TEXT-indexed field.
    results = client.query_points(
        collection_name=collection_name,
        query_filter=text_filter,
        limit=_bm25_fetch_k,
        with_payload=True,
    ).points

    # AIStudio_800 v4: post-filter by source_path to enforce entity isolation.
    # AIStudio_882: then AND the scope boundary — a chunk must satisfy BOTH (entity OR-set)
    # and (scope OR-set). An out-of-scope firm passes entity but fails scope → dropped.
    if entity_filter:
        results = [
            r for r in results
            if any(
                token in str((r.payload or {}).get("source_path", ""))
                for token in entity_filter
            )
        ]
    if allowed_source_paths:
        results = [
            r for r in results
            if any(
                token in str((r.payload or {}).get("source_path", ""))
                for token in allowed_source_paths
            )
        ]
    if _any_firm_filter:
        results = results[:int(top_k)]

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
