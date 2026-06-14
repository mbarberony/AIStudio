# src/local_llm_bot/app/rag_core.py
# Version: 1.10.1
# Changelog: 1.10.1 — AIStudio_891: make the Python entity/scope post-filter backstops
#             firm-aware. The Qdrant-side filter (qdrant_store._build_entity_filter) now
#             matches the entity on the `firm` payload field (tokenized MatchText), but the
#             in-Python backstops in retrieve() still checked only source_path with a plain
#             substring `in` — silently dropping every firm-matched hit whose underscored
#             token (e.g. PRICE_T_ROWE_GROUP_INC) is not a literal source_path substring,
#             so /ask returned zero despite a correct Qdrant match. New _entity_token_matches()
#             mirrors MatchText (all word-tokens present) over source_path OR firm. Also
#             corrects the stale Version line (was 1.9.5; top changelog already 1.10.0).
#             qdrant_store BM25 post-filter (372/380) has the same latent bug — fix deferred
#             (only fires under AISTUDIO_HYBRID_UNDER_FILTER, default off).
# Changelog: 1.10.0 — AIStudio_882 (scope application): retrieve() accepts allowed_source_paths
#             — the scope firm-boundary — threaded into all six _store.query/query_bm25
#             call-sites and ANDed as a post-filter backstop across channels. An active scope
#             gates hybrid like entity_filter and skips min_score (iXBRL high-distance). Default
#             None = pre-1.10.0 behavior.
# Changelog: 1.9.5 — AIStudio_881: optional hybrid-under-entity-filter. Env flag
#             AISTUDIO_HYBRID_UNDER_FILTER (default OFF = byte-identical to 1.9.4). When
#             OFF, entity_filter forces vector-only exactly as before. When ON, the BM25
#             (Literal) channel is no longer disabled by entity_filter — both channels run,
#             each isolated to the filtered firm(s) (qdrant_store.query/query_bm25 already
#             accept entity_filter; post-filter at the merge guarantees isolation). Rationale:
#             dense numeric tables (capital ratios) collapse in vector space — actual-CET1,
#             overhead, and regulatory-minimum rows score within ~0.07 of each other, so the
#             right row ranks low or drops; the Literal channel recalls it by exact tokens
#             but AIStudio_800 disabled Literal whenever entity_filter is set. Flag lets the
#             two channels coexist under entity isolation. Multi-firm (n>1): the per-firm
#             quota that AIStudio_877 gave the vector-only branch is mirrored here — each firm
#             runs its own vector+BM25 combine_hybrid at ceil(k/n), merged + deduped, so the
#             densest firm cannot monopolize the merged top-K. Recall fix only; row-level
#             precision (label-value binding vs. the table-blind CrossEncoder) is a separate
#             open item. No reingest. n<=1 + no-filter hybrid paths byte-identical to 1.9.4.
# Changelog: 1.9.4 — AIStudio_877: per-entity retrieval quota. AIStudio_837 raised the
#             slot COUNT with entity count but not its ALLOCATION — a single pooled query
#             at top_k=k with an OR-filter over n firms let the densest 1-2 firms take all
#             k slots (empirically: a 4-firm sec_10k query returned only BofA+WF chunks,
#             0 JPM/Citi, 2026-05-31). Fix: in the vector-only branch, when entity_filter
#             names n>1 firms, issue one filtered query per firm at ceil(k/n) each (floor 1),
#             merge + dedup by chunk_id, then existing rerank selects the global best. n<=1
#             path unchanged (byte-identical to 1.9.3). Guarantees every named firm is
#             represented in the candidate set.
# Changelog: 1.9.3 — lint: SIM102 combine nested if in _detect_entities (no logic change).
# Changelog: 1.9.2 — AIStudio_876: SINGLE entity detector _detect_entities + _normalize_for_match
#            (lower+NFKD de-accent+word-boundary). _resolve_entity_filter_tokens AND
#            _apply_knowledge_sources both call it — one matching rule, no drift. accent-insensitive.
# Changelog: 1.9.1 — AIStudio_876 fix: _resolve_entity_filter_tokens word-boundary match (\\b)
#            for alias + scope_name — prevents short-alias substring false-positives.
# Changelog: 1.9.0 — AIStudio_876: KB-sourced entity filter. New _scope_name_to_source_token
#            + _resolve_entity_filter_tokens — detect query entities via the same alias set
#            used for expansion, derive each one's source_path token (scope_name spaces→_),
#            returned for api.py _auto_entity_filter. Unifies expansion + filter on one entity KB.
# Changelog: 1.8.7 — AIStudio_837: unified K formula. Replaces two independent K
#            calculations (AIStudio_814 GLEIF-based dynamic K + AIStudio_836 entity_filter
#            _store_k) with single formula: k = max(configured_k, 10 + 2×n_entities).
#            n = max(GLEIF entity count, entity_filter list length). beta=2 gives
#            n=1→12, n=2→14, n=3→16, n=5→20. Both Qdrant query and CrossEncoder reranker
#            now use the same k — eliminates divergence that caused CrossEncoder to rerank
#            k=30-40 chunks while Qdrant returned only 15-25. Max k=20 targets ~31s/question.
# Changelog: 1.8.6 — AIStudio_836 (revised v2): simpler linear formula 10 + (n*5).
#            Decoupled from k. n=1→15, n=2→20, n=3→25, n=4→30. k×4 was flooding LLM context (40-120 chunks) causing
#            100s+ latency and timeouts. New formula: n=1→15, n=2→20, n=3→25 chunks.
# Changelog: 1.8.4 — AIStudio_836: multiply k×4 when entity_filter active on vector-only path.
#            Qdrant HNSW returns 0 results for selective filters (~10% collection) at low k.
#            Fix is in rag_core only — no qdrant_store change. Both 835 (min_score skip)
#            and 836 (k×4) are active together.
# Changelog: 1.8.3 — AIStudio_835: skip min_score filter when entity_filter is active.
#            Entity post-filter already guarantees source relevance; min_score was
#            wiping all ESEF hits (high cosine distances due to long iXBRL docs).
#            Artifacts on esg_cross_firm/digital_ing/digital_nordea post-restart fixed.
# Changelog: 1.8.2 — AIStudio_826 (revised): revert vector query enrichment — empirically
#            validated regression on esef_banks (Q1/Q4/Q6 dropped citations). Glossary
#            expansion now BM25-only. Vector query always uses original text. Lesson: vector
#            embedding is sensitive to query length/vocabulary shift; BM25 exact-match is not.
# Changelog: 1.8.1 — AIStudio_826: glossary expansion applied before branch split (reverted).
#            _load_glossary_sources() loads bis_basel_*_glossary.yaml from
#            data/knowledge_sources/bis_basel/. _apply_glossary_sources() matches
#            acronyms/terms in query (word-boundary, case-insensitive) and injects
#            expansion strings into BM25 query. Separate from entity path so
#            glossary term matches do not inflate _count_matched_entities() K scaling.
#            _GS_CACHE mirrors _KS_CACHE pattern. retrieve() merges both expansions.
# Changelog: 1.7.9 — AIStudio_814: dynamic K as function of entity count. retrieve()
#            computes effective_k = max(configured_k, 10 * entity_count) where
#            entity_count = number of GLEIF-known entities matched in the query.
#            1 entity → K unchanged (≥10), 2 → K≥20, 3 → K≥30, 4+ → K≥40.
#            Stepping stone toward M2.D p×q×r decomposition (AIStudio_816).
#            New helper: _count_matched_entities(query, corpus) → int.
# Changelog: 1.7.8 — AIStudio_801: _load_knowledge_sources() now exposes
#            wikidata_label, wikidata_short_name, wikidata_tickers from entities
#            YAML schema_version 1.1. Query-time expansion (_apply_knowledge_sources)
#            continues to use full aliases set for wide BM25 net.
# Changelog: 1.7.7 — AIStudio_801: _apply_knowledge_sources() auto-expands BM25 keywords.
#            from GLEIF entity alias files (data/knowledge_sources/gleif/). Loaded lazily
#            per corpus, cached after first call. User query "Goldman Sachs CET1" auto-
#            expands to include "THE GOLDMAN SACHS GROUP", "GS", etc. without manual
#            keyword entry. Replaces AIStudio_618 manual keywords as the primary path.
# Changelog: 1.6.1 — AIStudio_778: lower MIN_HYBRID_SCORE default 0.5 → 0.3.
#            was filtering small-document chunks (Erder|Pureur 34 chunks, Agentic AI 20 chunks)
#            causing Q1 QFD and Q13 Agentic AI regressions (12/14 vs 14/14 baseline).
# Changelog: 1.6.0 — AIStudio_778: MIN_HYBRID_SCORE threshold filter. Drops retrieved chunks
#            whose combined distance >= MIN_HYBRID_SCORE (i.e. combined score <= 0.5) after
#            score combination. Eliminates BM25-floor noise (e.g. p.3 TOC chunks). Applied
#            to both hybrid and vector-only paths in retrieve(). Threshold: 0.5.
# Changelog: 1.5.0 — hybrid retrieval support via optional hybrid_alpha kwarg on retrieve().
# Changelog: 1.3.3 — fix swap collision in renumbering (AIStudio_480).
# Changelog: 1.3.2 — renumber citations by first appearance in answer text (AIStudio_480).
"""
RAG core: retrieval, answer generation, citation support, and conversation memory.
"""

from __future__ import annotations

import os as _os
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from local_llm_bot.app.config import CONFIG
from local_llm_bot.app.ingest.index_jsonl import read_jsonl
from local_llm_bot.app.ollama_client import ollama_generate
from local_llm_bot.app.utils.corpus_paths import corpus_paths
from local_llm_bot.app.utils.repo_root import find_repo_root

# AIStudio_778: hardcoded fallback threshold used when retrieve() caller passes min_score=None.
# api.py resolves: per-request → corpus metadata default_min_score → this fallback.
_MIN_HYBRID_SCORE_FALLBACK: float = 0.5

_VECTORSTORE = _os.getenv("AISTUDIO_VECTORSTORE", "qdrant").lower()

# AIStudio_881: when truthy, allow the hybrid (vector + BM25) path to run even when an
# entity_filter is active, instead of forcing vector-only (the AIStudio_800 behavior).
# Default OFF — unset/empty/0/false leaves retrieve() byte-identical to 1.9.4. Process-level
# toggle (read at import like AISTUDIO_VECTORSTORE); set in the API server's environment.
_HYBRID_UNDER_FILTER = _os.getenv("AISTUDIO_HYBRID_UNDER_FILTER", "").strip().lower() in (
    "1",
    "true",
    "yes",
    "on",
)

if _VECTORSTORE == "chroma":
    from local_llm_bot.app.vectorstore import chroma_store as _store
else:
    from local_llm_bot.app.vectorstore import qdrant_store as _store

# Hybrid retrieval scoring helpers — pure functions, no I/O, no model load.
# Only invoked when retrieve(hybrid_alpha=...) is called with a non-None value.
from local_llm_bot.app import scoring as _scoring  # noqa: E402

# Reranker — lazy load, graceful fallback if sentence-transformers missing
try:
    from sentence_transformers import CrossEncoder as _CrossEncoder

    _reranker: _CrossEncoder | None = _CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    _RERANKER_AVAILABLE = True
except Exception:  # noqa: BLE001
    _reranker = None
    _RERANKER_AVAILABLE = False


# ---------------------------------------------------------------------------
# Core data types
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RetrievedDoc:
    id: str
    content: str
    source: str
    score: float  # distance for Chroma (lower=better); token score for JSONL (higher=better)
    page: int | None = None  # page number from pdfplumber extraction, None for non-PDF or unknown


@dataclass
class Citation:
    """A citation reference to a source document."""

    index: int
    source: str
    page: int | None = None
    chunk_id: str | None = None
    score: float = 0.0


@dataclass
class AnswerWithCitations:
    """Answer with citation metadata."""

    answer: str
    citations: list[Citation]
    source_docs: list[RetrievedDoc]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

# AIStudio_801: Knowledge sources — lazy-loaded entity alias cache per corpus.
# Populated on first retrieve() call for a given corpus.
# Maps: corpus_name → list of {canonical, aliases: set[str]}
_KS_CACHE: dict[str, list[dict]] = {}

# AIStudio_815: Glossary sources — lazy-loaded BIS Basel term cache.
# Corpus-wide (not per-corpus) — same glossary applies to all corpora.
# _UNLOADED sentinel distinguishes "not yet loaded" from "loaded, empty list".
_UNLOADED: object = object()
_GS_CACHE: object = _UNLOADED  # set to list[dict] after first load


def _load_knowledge_sources(corpus: str) -> list[dict]:
    """
    Load GLEIF entity aliases for a corpus from data/knowledge_sources/gleif/.
    Returns list of {canonical, scope_name, aliases, wikidata_label,
    wikidata_short_name, wikidata_tickers} dicts.
    Empty list if no file exists. Cached after first load.
    """
    if corpus in _KS_CACHE:
        return _KS_CACHE[corpus]

    import yaml  # local import — yaml not needed at module level

    repo = find_repo_root(Path(__file__))
    ks_dir = repo / "data" / "knowledge_sources" / "gleif"
    pattern = f"gleif_{corpus}_*_entities.yaml"
    matches = list(ks_dir.glob(pattern)) if ks_dir.exists() else []

    if not matches:
        _KS_CACHE[corpus] = []
        return []

    entities_path = matches[0]
    try:
        with open(entities_path) as f:
            data = yaml.safe_load(f)
        records = []
        for e in data.get("entities", []):
            aliases_raw = e.get("aliases", [])
            records.append({
                "canonical": e.get("canonical", ""),
                "scope_name": e.get("scope_name", ""),
                "aliases": {a.lower() for a in aliases_raw} | {e.get("canonical", "").lower()},
                "wikidata_label": e.get("wikidata_label", ""),
                "wikidata_short_name": e.get("wikidata_short_name", ""),
                "wikidata_tickers": e.get("wikidata_tickers", []),
            })
        _KS_CACHE[corpus] = records
        return records
    except Exception:  # noqa: BLE001
        _KS_CACHE[corpus] = []
        return []


def _scope_name_to_source_token(scope_name: str) -> str:
    """
    AIStudio_876 — Derive the Qdrant source_path filter token from an entity's
    scope_name. Empirically (2026-05-30) both sec_10k and esef_banks name their
    upload files with the firm's scope_name, spaces→underscores, as the prefix
    before the doc-type marker:
        "BNP Paribas"     → BNP_Paribas   (BNP_Paribas_ESEF_2025.xhtml)
        "Bank of America" → Bank_of_America (Bank_of_America_10K_...htm)
    The token is matched as a source_path substring by qdrant_store._build_entity_filter.
    """
    return scope_name.strip().replace(" ", "_")


def _normalize_for_match(s: str) -> str:
    """
    AIStudio_876 — The single normalization applied to BOTH the query and every
    alias before comparison, so all detection paths treat case and accents
    identically: NFKD accent-strip → ASCII → lowercase. This is the one place
    normalization is defined; every entity-detection consumer uses _detect_entities
    (below), which calls this — there is no second matching rule anywhere.
    """
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii").lower()


def _detect_entities(query: str, corpus: str) -> list[dict]:
    """
    AIStudio_876 — THE single entity-detection function. Given a query and corpus,
    return the list of entity records (from the GLEIF KB) the query mentions.

    Matching rule (identical for every caller):
      • normalize query and each alias/scope_name via _normalize_for_match
        (accent-insensitive + case-insensitive)
      • word-boundary match so a short alias never matches inside an unrelated
        word ("morgan" must not hit "jpmorgan")
      • aliases must be > 2 chars to be considered

    Every consumer — entity filter (_resolve_entity_filter_tokens), BM25 expansion
    (_apply_knowledge_sources), and api.py query expansion — calls THIS. There is no
    second copy of the matching logic. Returns matched entity records (possibly empty).
    """
    entities = _load_knowledge_sources(corpus)
    if not entities:
        return []
    q = _normalize_for_match(query)
    matched: list[dict] = []
    for entity in entities:
        hit = False
        for alias in entity["aliases"]:
            if not alias or len(alias) <= 2:
                continue
            if re.search(rf"\b{re.escape(_normalize_for_match(alias))}\b", q):
                hit = True
                break
        if not hit and entity["scope_name"] and re.search(
            rf"\b{re.escape(_normalize_for_match(entity['scope_name']))}\b", q
        ):
            hit = True
        if hit:
            matched.append(entity)
    return matched


def _resolve_entity_filter_tokens(query: str, corpus: str) -> list[str]:
    """
    AIStudio_876 — KB-sourced entity filter. Detects entities via the single
    _detect_entities function (shared with expansion) and maps each to its
    source_path filter token. Returns [] if no entity detected or no KB exists.
    """
    tokens: list[str] = []
    for entity in _detect_entities(query, corpus):
        tok = _scope_name_to_source_token(entity["scope_name"])
        if tok and tok not in tokens:
            tokens.append(tok)
    return tokens


def _apply_knowledge_sources(query: str, corpus: str,
                              existing_keywords: list[str] | None) -> list[str] | None:
    """
    Expand BM25 keywords automatically from knowledge sources.

    For each entity whose aliases appear in the query, add all its aliases
    to the keyword set. This replaces manual keyword entry — user types
    "Goldman Sachs CET1" and BM25 automatically searches for
    "THE GOLDMAN SACHS GROUP" and "GS" without user intervention.

    Returns merged keyword list, or None if no expansion occurred and
    existing_keywords was also None (preserves None → no-keywords path).
    """
    entities = _load_knowledge_sources(corpus)
    if not entities:
        return existing_keywords

    expanded: set[str] = set(existing_keywords or [])
    matched = False

    # Use the SINGLE detector — identical matching to the entity filter.
    for entity in _detect_entities(query, corpus):
        expanded.update(a for a in entity["aliases"] if len(a) > 1)
        expanded.add(entity["canonical"])
        matched = True

    if not matched and not existing_keywords:
        return None  # preserve no-keywords path — no expansion, no overhead

    return sorted(expanded) if expanded else existing_keywords


def _load_glossary_sources() -> list[dict]:
    """
    Load BIS Basel glossary from data/knowledge_sources/bis_basel/*.yaml.
    Corpus-wide — same glossary applies to all corpora.
    Returns list of {term, full_form, expansion} dicts. Cached after first load.
    """
    global _GS_CACHE  # noqa: PLW0603
    if _GS_CACHE is not _UNLOADED:
        return _GS_CACHE or []

    import yaml  # local import

    repo = find_repo_root(Path(__file__))
    ks_dir = repo / "data" / "knowledge_sources" / "bis_basel"
    matches = list(ks_dir.glob("bis_basel_*_glossary.yaml")) if ks_dir.exists() else []

    if not matches:
        _GS_CACHE = []
        return []

    glossary_path = matches[0]
    try:
        with open(glossary_path) as f:
            data = yaml.safe_load(f)
        records = []
        for entry in data.get("glossary", []):
            term = entry.get("term", "")
            if not term:
                continue
            records.append({
                "term": term,
                "full_form": entry.get("full_form", ""),
                "expansion": entry.get("expansion", ""),
            })
        _GS_CACHE = records
        return records
    except Exception:  # noqa: BLE001
        _GS_CACHE = []
        return []


def _apply_glossary_sources(query: str) -> list[str]:
    """
    Expand BM25 keywords from BIS Basel glossary.

    For each glossary term found in the query (word-boundary match,
    case-insensitive), inject its expansion string into the keyword set.
    This bridges the acronym/full-form vocabulary gap:
      "FRTB exposure" → BM25 also searches "Fundamental Review Trading Book
       market risk capital IMA SA"

    Returns list of expansion tokens to append to BM25 query, or [] if none.
    Kept separate from entity expansion so glossary matches do not affect
    _count_matched_entities() K scaling (AIStudio_814).
    """
    glossary = _load_glossary_sources()
    if not glossary:
        return []

    expanded: set[str] = set()
    for entry in glossary:
        term = entry["term"]
        # Word-boundary match — "AT1" should not match inside "PLAT1NUM"
        pattern = rf"\b{re.escape(term)}\b"
        if re.search(pattern, query, re.IGNORECASE):
            expansion = entry.get("expansion", "")
            if expansion:
                expanded.update(expansion.split())

    return sorted(expanded) if expanded else []


def _count_matched_entities(query: str, corpus: str) -> int:
    """
    Return the number of GLEIF-known entities matched in the query.

    Used by retrieve() to compute dynamic K: effective_k = max(configured_k,
    10 * entity_count). Keeps _apply_knowledge_sources() return signature
    unchanged. Empty list (no knowledge sources for corpus) → returns 0.
    """
    entities = _load_knowledge_sources(corpus)
    if not entities:
        return 0

    query_lower = query.lower()
    count = 0
    for entity in entities:
        hit = any(
            alias and len(alias) > 2 and alias in query_lower
            for alias in entity["aliases"]
        )
        if not hit:
            hit = bool(entity["scope_name"]) and entity["scope_name"].lower() in query_lower
        if hit:
            count += 1
    return count


def _repo_root() -> Path:
    return find_repo_root(Path(__file__))


def _is_tax_corpus(corpus: str) -> bool:
    return "tax" in corpus.lower()


def _tokenize(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", text.lower()) if len(t) >= 3}


def compose_queries(query: str, corpus: str) -> list[str]:
    """Return one or more query variants for retrieval."""
    return [query]


def _lexical_jsonl_retrieve(*, query: str, top_k: int, corpus: str) -> list[RetrievedDoc]:
    """
    Simple lexical fallback retrieval from index.jsonl.
    Scores chunks by token containment count.
    """
    paths = corpus_paths(_repo_root(), corpus)
    rows = read_jsonl(paths["index"])
    if not rows:
        return []

    tokens = _tokenize(query)
    if not tokens:
        return []

    scored: list[tuple[int, dict[str, Any]]] = []
    for r in rows:
        text = str(r.get("text", "")).lower()
        score = sum(1 for token in tokens if token in text)
        if score > 0:
            scored.append((score, r))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [
        RetrievedDoc(
            id=str(r.get("chunk_id", "")),
            content=str(r.get("text", "")),
            source=str(r.get("source_path", "")),
            score=float(score),
        )
        for score, r in scored[:top_k]
    ]


# ---------------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------------


def _entity_token_matches(token: str, *field_values: str) -> bool:
    """True if every word-token of `token` is present in ANY field value's word-tokens.

    Mirrors Qdrant MatchText semantics (all query tokens must appear in the field) over
    the SAME field set the Qdrant-side filter checks — source_path OR firm. This is the
    in-Python backstop that guarantees entity/scope isolation regardless of which channel
    produced a hit; it must stay consistent with qdrant_store._build_entity_filter.

    AIStudio_891: replaces the prior `token in source_path` plain-substring check, which
    only worked when the token was label-shaped (e.g. T_Rowe_Price ⊂ filename) and silently
    dropped firm-matched hits once the token became the iXBRL tag (PRICE_T_ROWE_GROUP_INC),
    which is not a source_path substring but does match the `firm` field token-for-token.
    Tokenizing is backward-compatible: label tokens remain a subset of their filename tokens.
    """
    t_toks = set(re.findall(r"[a-z0-9]+", token.lower()))
    if not t_toks:
        return False
    for value in field_values:
        if t_toks <= set(re.findall(r"[a-z0-9]+", str(value).lower())):
            return True
    return False


def retrieve(
    *,
    query: str,
    top_k: int | None = None,
    corpus: str = "default",
    hybrid_alpha: float | None = None,
    min_score: float | None = None,
    entity_filter: list[str] | None = None,  # AIStudio_798: OR filter on source_path substrings
    allowed_source_paths: list[str] | None = None,  # AIStudio_882: scope boundary, ANDed with entity_filter
    keywords: list[str] | None = None,        # AIStudio_618: BM25 boost terms
) -> list[RetrievedDoc]:
    """
    Retrieve relevant chunks for a query.

    Args:
        query: User question text.
        top_k: Number of chunks to return. Falls back to CONFIG.rag.top_k.
        corpus: Corpus name (e.g. "demo", "help", "sec_10k"). Maps to Qdrant
            collection "aistudio_{corpus}".
        hybrid_alpha: Optional weight for hybrid (vector + BM25) retrieval.
            - None (default): vector-only, identical to v1.4.0 behavior
            - 1.0: vector-only via hybrid path (same result as None, slightly more work)
            - 0.0: BM25-only
            - 0.0 < α < 1.0: weighted combination; 0.5 is equal weight
            See scoring.combine_hybrid() and CONCEPT - AIStudio - Hybrid Retrieval Design.
            Only honored on Qdrant backend (Chroma path ignores it).

    Returns:
        List of RetrievedDoc, reranked by CrossEncoder if available.
    """
    k = int(top_k) if top_k is not None else int(CONFIG.rag.top_k)

    # AIStudio_837: unified K formula — single source of truth for both Qdrant and CrossEncoder.
    # Replaces AIStudio_814 (10×entity_count, too aggressive) and AIStudio_836 (10+n×5,
    # entity_filter path only). Formula: k = max(configured_k, 10 + 2×n_entities).
    # beta=2: n=1→12, n=2→14, n=3→16, n=5→20.
    # At k=20: CrossEncoder ~16s + generation ~15s = ~31s/question, inside 60s budget.
    # n = max(GLEIF entity count, entity_filter list length) — take the stronger signal.
    _entity_count = _count_matched_entities(query, corpus)
    _ef_count = len(entity_filter) if entity_filter else 0
    _n = max(_entity_count, _ef_count)
    k = max(k, 10 + 2 * _n)

    collection = f"aistudio_{corpus}"

    if True:  # Always query — works for both Qdrant and Chroma via _store
        # Hybrid retrieval branch — only active when hybrid_alpha is set AND we're on Qdrant.
        # When hybrid_alpha is None, the vector-only path below runs unchanged (byte-identical
        # to v1.4.0 behavior — the backward-compat guarantee).
        # AIStudio_800 v3: when entity_filter is set, force vector-only retrieval.
        # BM25 channel returns corpus-wide top results regardless of entity_filter,
        # and dominates combine_hybrid() pushing entity-filtered vector hits out of
        # the merged top-K. Vector-only with entity_filter is both correct and fast.
        # AIStudio_826 (revised): glossary expansion applied to BM25 query only.
        # Vector query uses original text — enriching the embedding with 15-20 acronym
        # expansion tokens shifts the vector away from relevant chunks (empirically
        # validated regression on esef_banks 2026-05-28). BM25 exact-match benefits
        # from expansion; vector semantic search does not.
        _glossary_tokens = _apply_glossary_sources(query)

        # AIStudio_800 v3 default: entity_filter forces vector-only (the BM25 channel
        # otherwise returns corpus-wide hits that dominate combine_hybrid()).
        # AIStudio_881: when _HYBRID_UNDER_FILTER is ON, that force-disable is lifted —
        # qdrant_store.query/query_bm25 now accept entity_filter (isolated per firm) and the
        # post-filter below is a backstop, so the two channels can coexist under isolation.
        # AIStudio_882: an active scope (allowed_source_paths) is a firm-boundary too — it
        # gates hybrid exactly like entity_filter (BM25 scope post-filter added in 1.3.0).
        _use_hybrid = (
            hybrid_alpha is not None
            and _VECTORSTORE != "chroma"
            and (not (entity_filter or allowed_source_paths) or _HYBRID_UNDER_FILTER)
        )

        if _use_hybrid:
            channel_k = max(k * 2, 10)

            # AIStudio_801: auto-expand keywords from knowledge sources (GLEIF entity aliases).
            _expanded_keywords = _apply_knowledge_sources(query, corpus, keywords)
            # AIStudio_618 + AIStudio_815: append GLEIF aliases and glossary terms to BM25 query.
            _bm25_query = query
            if _expanded_keywords:
                _bm25_query = _bm25_query + " " + " ".join(_expanded_keywords)
            if _glossary_tokens:
                _bm25_query = _bm25_query + " " + " ".join(_glossary_tokens)

            if entity_filter and len(entity_filter) > 1:
                # AIStudio_881: multi-firm hybrid quota. Mirror the AIStudio_877 per-firm
                # allocation onto the hybrid path so a single pooled vector+BM25 query cannot
                # let the densest firm monopolize the merged top-K. Each firm runs its own
                # vector+BM25 combine_hybrid at ceil(k/n); results merged + deduped by chunk_id,
                # then the rerank below selects the global best across firms.
                _n_firms = len(entity_filter)
                _per_entity_k = max(1, -(-k // _n_firms))  # ceil(k / n_firms), floor 1
                _per_channel_k = max(_per_entity_k * 2, 10)
                _merged: dict = {}
                for _token in entity_filter:
                    _v_hits = _store.query(
                        query_text=query,
                        top_k=_per_channel_k,
                        embed_model=CONFIG.rag.default_embed_model,
                        collection_name=collection,
                        entity_filter=[_token],
                        allowed_source_paths=allowed_source_paths,
                    )
                    _b_hits = _store.query_bm25(
                        query_text=_bm25_query,
                        top_k=_per_channel_k,
                        collection_name=collection,
                        entity_filter=[_token],
                        allowed_source_paths=allowed_source_paths,
                    )
                    _firm_hits = _scoring.combine_hybrid(
                        vector_hits=_v_hits,
                        bm25_hits=_b_hits,
                        alpha=float(hybrid_alpha),
                        top_k=_per_entity_k,
                    )
                    for _h in _firm_hits:
                        # dedup by chunk_id (keep first/best occurrence)
                        if _h.chunk_id not in _merged:
                            _merged[_h.chunk_id] = _h
                hits = list(_merged.values())
            else:
                # n<=1 (single firm or no filter): pooled hybrid — byte-identical to 1.9.4
                # when no entity_filter; entity-isolated single-firm pair when filter is set
                # and the flag is on.
                vector_hits = _store.query(
                    query_text=query,
                    top_k=channel_k,
                    embed_model=CONFIG.rag.default_embed_model,
                    collection_name=collection,
                    entity_filter=entity_filter,
                    allowed_source_paths=allowed_source_paths,
                )
                bm25_hits = _store.query_bm25(
                    query_text=_bm25_query,
                    top_k=channel_k,
                    collection_name=collection,
                    entity_filter=entity_filter,
                    allowed_source_paths=allowed_source_paths,
                )
                hits = _scoring.combine_hybrid(
                    vector_hits=vector_hits,
                    bm25_hits=bm25_hits,
                    alpha=float(hybrid_alpha),
                    top_k=k,
                )
        else:
            # Vector-only path — original query only (glossary expansion degrades vector recall)
            # AIStudio_877: per-entity retrieval quota. A single pooled query at top_k=k with
            # an OR-filter over n firms lets the densest 1-2 firms monopolize all k slots
            # (empirically: a 4-firm query returned only BofA+WF chunks, 0 JPM/Citi —
            # 2026-05-31). AIStudio_837 raised the slot COUNT with entity count but not its
            # ALLOCATION. Fix: when entity_filter names n>1 firms, issue one filtered query
            # per firm at ceil(k/n) each (floor 1), guaranteeing every named firm is
            # represented; merge + dedup by chunk_id, then rerank below selects the global best.
            if entity_filter and len(entity_filter) > 1:
                _n_firms = len(entity_filter)
                _per_entity_k = max(1, -(-k // _n_firms))  # ceil(k / n_firms), floor 1
                _merged: dict = {}
                for _token in entity_filter:
                    _firm_hits = _store.query(
                        query_text=query,
                        top_k=_per_entity_k,
                        embed_model=CONFIG.rag.default_embed_model,
                        collection_name=collection,
                        entity_filter=[_token],
                        allowed_source_paths=allowed_source_paths,
                    )
                    for _h in _firm_hits:
                        # dedup by chunk_id (keep first/best occurrence)
                        if _h.chunk_id not in _merged:
                            _merged[_h.chunk_id] = _h
                hits = list(_merged.values())
            else:
                # n<=1 (single firm or no filter): original pooled behavior, unchanged.
                # AIStudio_837: use unified k (computed above) for Qdrant query.
                hits = _store.query(
                    query_text=query,
                    top_k=k,
                    embed_model=CONFIG.rag.default_embed_model,
                    collection_name=collection,
                    entity_filter=entity_filter,
                    allowed_source_paths=allowed_source_paths,
                )

        # AIStudio_800: apply entity_filter post-filter on combined hits.
        # This guarantees entity isolation regardless of which channel (vector/BM25)
        # provided each hit — BM25 post-filter alone is insufficient because vector
        # hits pass through combine_hybrid() without source_path filtering.
        # AIStudio_891: match the entity on source_path OR firm, tokenized (MatchText
        # parity). The Qdrant filter matches firm; this backstop must too, or it drops
        # the very hits the Qdrant filter just admitted.
        if entity_filter:
            hits = [
                h for h in hits
                if any(
                    _entity_token_matches(
                        token,
                        h.metadata.get("source_path", ""),
                        h.metadata.get("firm", ""),
                    )
                    for token in entity_filter
                )
            ]

        # AIStudio_882: scope boundary backstop — AND the allowed_source_paths set across the
        # merged hits, same rationale as the entity backstop (a vector hit can reach here
        # without per-channel source_path filtering). entity AND scope: an out-of-scope firm
        # that satisfied the entity clause is dropped here; empty intersection → no hits.
        if allowed_source_paths:
            hits = [
                h for h in hits
                if any(
                    _entity_token_matches(
                        token,
                        h.metadata.get("source_path", ""),
                        h.metadata.get("firm", ""),
                    )
                    for token in allowed_source_paths
                )
            ]

        # AIStudio_778: drop BM25-floor chunks below minimum score threshold.
        # AIStudio_835: skip min_score filter when entity_filter is active.
        # Entity post-filter (above) already guarantees source relevance — the
        # correct firm's chunks are retained regardless of score. ESEF iXBRL
        # documents produce high cosine distances (low similarity scores) due to
        # their length and mixed-language content; applying min_score on top of
        # entity_filter wipes all hits and returns empty docs → Artifact answers.
        # AIStudio_882: an active scope is a firm-boundary too — skip min_score under it
        # for the same iXBRL high-distance reason.
        if not (entity_filter or allowed_source_paths):
            _threshold = min_score if min_score is not None else _MIN_HYBRID_SCORE_FALLBACK
            hits = [h for h in hits if float(h.distance) < _threshold]

        max_d = CONFIG.rag.max_distance
        if max_d is not None:
            md = float(max_d)
            hits = [h for h in hits if float(h.distance) <= md]

        if hits:
            if _RERANKER_AVAILABLE and _reranker is not None:
                pairs = [[query, h.text] for h in hits]
                scores = _reranker.predict(pairs)
                hits = [
                    h
                    for _, h in sorted(
                        zip(scores, hits, strict=False), key=lambda x: x[0], reverse=True
                    )
                ]
            return [
                RetrievedDoc(
                    id=h.chunk_id,
                    content=h.text,
                    source=str(h.metadata.get("source_path", "")),
                    score=float(h.distance),
                    page=h.metadata.get("page"),
                )
                for h in hits
            ]

        # AIStudio_800 v2: if entity_filter is set, do not fall back to unfiltered
        # lexical retrieve — return empty list rather than unfiltered results.
        if entity_filter:
            return []
        return _lexical_jsonl_retrieve(query=query, top_k=k, corpus=corpus)

    # AIStudio_800 v2: same guard on outer fallback
    if entity_filter:
        return []
    return _lexical_jsonl_retrieve(query=query, top_k=k, corpus=corpus)


# ---------------------------------------------------------------------------
# Citation helpers
# ---------------------------------------------------------------------------


def extract_page_number(source_path: str, chunk_id: str = "") -> int | None:
    """Attempt to extract page number from source path or chunk_id."""
    page_match = re.search(r"#page=(\d+)", source_path)
    if page_match:
        return int(page_match.group(1))

    page_match = re.search(r"[_\-]p(\d+)", source_path, re.IGNORECASE)
    if page_match:
        return int(page_match.group(1))

    if chunk_id:
        page_match = re.search(r"page[_\-]?(\d+)", chunk_id, re.IGNORECASE)
        if page_match:
            return int(page_match.group(1))

    return None


# ---------------------------------------------------------------------------
# Answer generation
# ---------------------------------------------------------------------------


def generate_answer_with_citations(
    *,
    query: str,
    docs: list[RetrievedDoc],
    conversation_history: list[dict[str, str]] | None = None,
) -> AnswerWithCitations:
    """Generate answer with inline citation markers and return citation metadata."""
    if not docs:
        return AnswerWithCitations(
            answer="I don't have any relevant documents to answer this question.",
            citations=[],
            source_docs=[],
        )

    context_parts = []
    for i, doc in enumerate(docs, 1):
        name = doc.source.split("/")[-1]
        context_parts.append(f"SOURCE [{i}]: {name}\n{doc.content}")
    context = "\n\n---\n\n".join(context_parts)

    num_sources = len(docs)
    system = (
        "You are a precise research assistant. Answer using ONLY the provided sources.\n"
        f"There are exactly {num_sources} sources, numbered [1] through [{num_sources}].\n"
        "CITATION RULES — follow exactly:\n"
        "- Cite every factual claim with [N] where N is the source number (1 to "
        f"{num_sources}).\n"
        "- You may combine citations: [1,2] or [1][2].\n"
        "- NEVER use numbers outside the range [1] to "
        f"[{num_sources}] as citations.\n"
        "- Do NOT append a References or Sources section.\n"
        "- If the sources lack sufficient information, say so explicitly."
    )

    if conversation_history:

        def _clean_history_content(text: str) -> str:
            """Strip citation markers [N] and HTML tags from history so LLM doesn't continue numbering."""
            text = re.sub(r"<[^>]+>", " ", text)  # strip HTML tags
            text = re.sub(r"\[\d+(?:,\s*\d+)*\]", "", text)  # strip [1], [1,2] etc.
            text = re.sub(r"\[Source\s+\d+\]", "", text, flags=re.IGNORECASE)  # strip [Source N]
            text = re.sub(r"\s{2,}", " ", text).strip()  # collapse whitespace
            return text

        history_text = "\n".join(
            [
                f"{msg['role'].upper()}: {_clean_history_content(msg['content'])}"
                for msg in conversation_history[-6:]
            ]
        )
        prompt = f"Conversation History:\n{history_text}\n\nCurrent Question:\n{query}\n\nAvailable Sources:\n{context}\n\nAnswer:"
    else:
        prompt = f"Question:\n{query}\n\nAvailable Sources:\n{context}\n\nAnswer:"

    answer = ollama_generate(model=CONFIG.rag.default_model, prompt=prompt, system=system)

    # Guard against blank or citation-only answers from the model
    answer_stripped = answer.strip()
    if not answer_stripped or all(c in "[]0123456789, \n" for c in answer_stripped):
        answer = (
            "The sources contain relevant information on this topic, but a direct answer "
            "could not be generated. Please use the Open ↗ link on the cited references "
            "to read the source documents directly."
        )
    citations: list[Citation] = []
    cited_indices: set[int] = set()
    raw_indices: list[int] = []

    # Pattern 1: [Source N] or [source N]
    for m in re.finditer(r"\[(?:Source\s+|source\s+)(\d+)\]", answer, re.IGNORECASE):
        raw_indices.append(int(m.group(1)))

    # Pattern 2: [1], [1,2], [1, 2], [1,2,3]
    for m in re.finditer(r"\[(\d+(?:\s*,\s*\d+)*)\]", answer):
        for idx_str in m.group(1).split(","):
            raw_indices.append(int(idx_str.strip()))

    for idx in raw_indices:
        if 0 < idx <= len(docs) and idx not in cited_indices:
            doc = docs[idx - 1]
            citations.append(
                Citation(
                    index=idx,
                    source=doc.source,
                    page=doc.page
                    if doc.page is not None
                    else extract_page_number(doc.source, doc.id),
                    chunk_id=doc.id,
                    score=doc.score,
                )
            )
            cited_indices.add(idx)

    # If model cited nothing, surface all retrieved docs as implicit sources
    if not citations and docs:
        for i, doc in enumerate(docs, 1):
            citations.append(
                Citation(
                    index=i,
                    source=doc.source,
                    page=doc.page
                    if doc.page is not None
                    else extract_page_number(doc.source, doc.id),
                    chunk_id=doc.id,
                    score=doc.score,
                )
            )

    citations.sort(key=lambda c: c.index)

    # Renumber citations consecutively starting at [1] in order of first appearance in text
    # Only cited sources appear in references — no gaps in numbering
    # Two-pass rewrite: old→placeholder, then placeholder→new
    # This avoids collision when renumbering is a swap (e.g. [2]→[1] and [1]→[2])
    if citations:
        cited_set = {c.index for c in citations}
        # Build appearance-order map: scan answer text left-to-right
        appearance_order: dict[int, int] = {}
        for m in re.finditer(r"\[(\d+)\]", answer):
            orig = int(m.group(1))
            if orig not in appearance_order and orig in cited_set:
                appearance_order[orig] = len(appearance_order) + 1
        # Any cited indices not found in text (edge case) get appended at end
        for c in citations:
            if c.index not in appearance_order:
                appearance_order[c.index] = len(appearance_order) + 1
        renumber_map: dict[int, int] = appearance_order
        # Pass 1: replace [old] with placeholder [__N__] to avoid swap collisions
        for old_idx in renumber_map:
            answer = re.sub(rf"\[{old_idx}\]", f"[__{old_idx}__]", answer)
        # Pass 2: replace [__old__] with [new]
        for old_idx, new_idx in renumber_map.items():
            answer = re.sub(rf"\[__{old_idx}__\]", f"[{new_idx}]", answer)
        # Update citation objects to new indices and sort by appearance order
        for c in citations:
            c.index = renumber_map[c.index]
        citations.sort(key=lambda c: c.index)

    return AnswerWithCitations(answer=answer, citations=citations, source_docs=docs)


def generate_answer(*, query: str, docs: list[RetrievedDoc]) -> str:
    """
    Backward-compatible wrapper — returns just the answer string.
    Use generate_answer_with_citations() for citation support.
    """
    context = "\n\n".join(f"[{d.source}] {d.content}" for d in docs) if docs else ""
    system = (
        "You are a concise assistant. Use the provided context. "
        "If the context is insufficient, say you do not know."
    )
    prompt = f"Question:\n{query}\n\nContext:\n{context}\n\nAnswer:"
    return ollama_generate(model=CONFIG.rag.default_model, prompt=prompt, system=system)
