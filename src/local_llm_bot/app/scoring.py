# src/local_llm_bot/app/scoring.py
# Version: 1.0.0
"""
Score combination and normalization for hybrid retrieval.

Pure functions — no I/O, no global state, no model loading. Designed to be trivially
unit-testable and to compose cleanly with future score channels (M2.B table-relevance,
M2.D entity-boost) without rewrites.

Public surface:
    normalize_minmax(scores)         — min-max normalize a score list to [0, 1]
    combine_hybrid(...)              — merge vector + BM25 retrieval results

Design constraint: this module knows about QdrantHit but not about Qdrant the database,
not about Ollama, not about CONFIG. It operates on already-retrieved hits and produces
a merged ranked list. All I/O happens in qdrant_store.py and rag_core.py.
"""

from __future__ import annotations

from local_llm_bot.app.vectorstore.qdrant_store import QdrantHit


def normalize_minmax(scores: list[float]) -> list[float]:
    """
    Min-max normalize a list of scores to [0, 1].

    Returns all-0.5 if all scores are equal (degenerate case — can't differentiate,
    so neutral mid-value preserves combination semantics without dividing by zero).
    Returns empty list if input is empty.

    The convention this module uses: HIGHER is BETTER after normalization, regardless
    of the input convention. Callers are responsible for flipping distance-style scores
    (lower-is-better) before passing them in.
    """
    if not scores:
        return []
    s_min = min(scores)
    s_max = max(scores)
    if s_max == s_min:
        # All scores identical — return neutral mid-value to avoid division by zero
        # and to keep the channel from dominating or vanishing in weighted combination.
        return [0.5] * len(scores)
    span = s_max - s_min
    return [(s - s_min) / span for s in scores]


def combine_hybrid(
    *,
    vector_hits: list[QdrantHit],
    bm25_hits: list[QdrantHit],
    alpha: float,
    top_k: int,
) -> list[QdrantHit]:
    """
    Merge vector and BM25 retrieval results into a single ranked list.

    Algorithm:
        1. Flip vector distances (lower=better) to similarities (higher=better)
        2. BM25 scores arrive as raw scores in `distance` field (higher=better, no flip)
        3. Min-max normalize each channel independently to [0, 1]
        4. For each unique chunk_id appearing in either channel, compute:
               final_score = alpha * vector_norm + (1 - alpha) * bm25_norm
           Missing channel contributes 0 (chunk only matched one signal — that's fine,
           it just means the other channel didn't surface it in its top-K).
        5. Sort descending by final_score, return top_k

    Args:
        vector_hits: Output of qdrant_store.query() — distance is 1-cosine_similarity
        bm25_hits:   Output of qdrant_store.query_bm25() — distance is raw BM25 score
        alpha:       Weight on vector channel. 1.0 = vector only, 0.0 = BM25 only,
                     0.5 = equal weight. Must be in [0, 1].
        top_k:       Maximum results to return.

    Returns:
        List of QdrantHit (capped at top_k), sorted by combined score descending.
        The `distance` field of each returned hit carries (1 - combined_score) so the
        downstream convention (lower = better) is preserved for consistency.

    Raises:
        ValueError: if alpha is outside [0, 1].
    """
    if not 0.0 <= alpha <= 1.0:
        raise ValueError(f"alpha must be in [0, 1], got {alpha}")

    if top_k <= 0:
        return []

    # Edge case: both channels empty
    if not vector_hits and not bm25_hits:
        return []

    # Edge case: alpha=1.0 and BM25 channel ignored — short-circuit to vector-only
    # (avoids unnecessary normalization work; semantically identical to full path)
    if alpha == 1.0:
        return vector_hits[:top_k]
    # Symmetric short-circuit for BM25-only
    if alpha == 0.0:
        return bm25_hits[:top_k]

    # Build per-channel similarity maps keyed by chunk_id.
    # Vector channel: flip distance → similarity by computing (1 - distance).
    # Cosine distance is in [0, 2] in principle but [0, 1] in practice for normalized
    # embeddings (which nomic-embed-text produces). We use 1 - distance which gives
    # cosine similarity in [-1, 1] but typically [0, 1] for our embeddings.
    vector_sims = {hit.chunk_id: 1.0 - hit.distance for hit in vector_hits}
    # BM25 channel: distance field already carries raw BM25 score (higher = better)
    bm25_sims = {hit.chunk_id: hit.distance for hit in bm25_hits}

    # Normalize each channel independently. Per-channel normalization is the right
    # choice (vs joint normalization across channels) because the score scales are
    # incommensurable — cosine sim is bounded [0, 1], BM25 is unbounded ~[0, 30].
    # Joint normalization would let BM25's larger absolute range dominate trivially.
    vector_norm = dict(
        zip(vector_sims.keys(), normalize_minmax(list(vector_sims.values())), strict=False)
    )
    bm25_norm = dict(
        zip(bm25_sims.keys(), normalize_minmax(list(bm25_sims.values())), strict=False)
    )

    # Build hit lookup so we can return full QdrantHit objects after ranking.
    # When a chunk appears in both channels, prefer the vector_hits version
    # (arbitrary but consistent — the QdrantHit content is identical, only `distance`
    # differs, and we'll overwrite distance below anyway).
    hit_by_id: dict[str, QdrantHit] = {hit.chunk_id: hit for hit in bm25_hits}
    hit_by_id.update({hit.chunk_id: hit for hit in vector_hits})  # vector wins ties

    # Compute combined scores for the union of chunk_ids
    all_ids = set(vector_norm.keys()) | set(bm25_norm.keys())
    combined: list[tuple[float, str]] = []
    for cid in all_ids:
        v_score = vector_norm.get(cid, 0.0)  # absent → 0 contribution
        b_score = bm25_norm.get(cid, 0.0)
        final = alpha * v_score + (1.0 - alpha) * b_score
        combined.append((final, cid))

    # Sort by combined score descending (highest first)
    combined.sort(key=lambda x: x[0], reverse=True)

    # Take top_k, rebuild as QdrantHit list with distance = 1 - combined_score
    # so downstream code (rerank, RetrievedDoc construction) sees lower=better.
    out: list[QdrantHit] = []
    for final_score, cid in combined[:top_k]:
        original = hit_by_id[cid]
        out.append(
            QdrantHit(
                chunk_id=original.chunk_id,
                text=original.text,
                metadata=original.metadata,
                distance=1.0 - final_score,
            )
        )
    return out
