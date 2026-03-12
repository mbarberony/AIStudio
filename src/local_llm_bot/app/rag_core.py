# src/local_llm_bot/app/rag_core.py
"""
RAG core: retrieval, answer generation, citation support, and conversation memory.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Dict, Optional

from local_llm_bot.app.config import CONFIG
from local_llm_bot.app.ingest.index_jsonl import read_jsonl
from local_llm_bot.app.ollama_client import ollama_generate
from local_llm_bot.app.utils.corpus_paths import corpus_paths
from local_llm_bot.app.utils.repo_root import find_repo_root
import os as _os
_VECTORSTORE = _os.getenv("AISTUDIO_VECTORSTORE", "qdrant").lower()
if _VECTORSTORE == "chroma":
    from local_llm_bot.app.vectorstore import chroma_store as _store
else:
    from local_llm_bot.app.vectorstore import qdrant_store as _store


# ---------------------------------------------------------------------------
# Core data types
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RetrievedDoc:
    id: str
    content: str
    source: str
    score: float  # distance for Chroma (lower=better); token score for JSONL (higher=better)


@dataclass
class Citation:
    """A citation reference to a source document."""
    index: int
    source: str
    page: Optional[int] = None
    chunk_id: Optional[str] = None
    score: float = 0.0


@dataclass
class AnswerWithCitations:
    """Answer with citation metadata."""
    answer: str
    citations: List[Citation]
    source_docs: List[RetrievedDoc]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

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

def retrieve(
    *, query: str, top_k: int | None = None, corpus: str = "default"
) -> list[RetrievedDoc]:
    k = int(top_k) if top_k is not None else int(CONFIG.rag.top_k)

    if True:  # Always query — works for both Qdrant and Chroma via _store
        paths = corpus_paths(_repo_root(), corpus)

        hits = _store.query(
            query_text=query,
            top_k=k,
            embed_model=CONFIG.rag.default_embed_model,
            persist_dir=paths["chroma"],
            collection_name=f"aistudio_{corpus}",
        )

        max_d = CONFIG.rag.max_distance
        if max_d is not None:
            md = float(max_d)
            hits = [h for h in hits if float(h.distance) <= md]

        if hits:
            return [
                RetrievedDoc(
                    id=h.chunk_id,
                    content=h.text,
                    source=str(h.metadata.get("source_path", "")),
                    score=float(h.distance),
                )
                for h in hits
            ]

        return _lexical_jsonl_retrieve(query=query, top_k=k, corpus=corpus)

    return _lexical_jsonl_retrieve(query=query, top_k=k, corpus=corpus)


# ---------------------------------------------------------------------------
# Citation helpers
# ---------------------------------------------------------------------------

def extract_page_number(source_path: str, chunk_id: str = "") -> Optional[int]:
    """Attempt to extract page number from source path or chunk_id."""
    page_match = re.search(r'#page=(\d+)', source_path)
    if page_match:
        return int(page_match.group(1))

    page_match = re.search(r'[_\-]p(\d+)', source_path, re.IGNORECASE)
    if page_match:
        return int(page_match.group(1))

    if chunk_id:
        page_match = re.search(r'page[_\-]?(\d+)', chunk_id, re.IGNORECASE)
        if page_match:
            return int(page_match.group(1))

    return None


# ---------------------------------------------------------------------------
# Answer generation
# ---------------------------------------------------------------------------

def generate_answer_with_citations(
    *,
    query: str,
    docs: List[RetrievedDoc],
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> AnswerWithCitations:
    """Generate answer with inline citation markers and return citation metadata."""
    if not docs:
        return AnswerWithCitations(
            answer="I don't have any relevant documents to answer this question.",
            citations=[],
            source_docs=[]
        )

    context_parts = []
    for i, doc in enumerate(docs, 1):
        context_parts.append(f"[Source {i}] {doc.source}\n{doc.content}")
    context = "\n\n".join(context_parts)

    system = (
        "You are a helpful research assistant.\n"
        "Use the provided sources to answer questions accurately.\n"
        "IMPORTANT: When you use information from a source, cite it using [1], [2], etc.\n"
        "The number should match the source number in the context.\n"
        "You can cite multiple sources like [1,2] or [1][2].\n"
        "If the answer is not in the provided sources, say so clearly.\n"
        "Always cite your sources - every factual claim should have a citation."
    )

    if conversation_history:
        history_text = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in conversation_history[-6:]
        ])
        prompt = f"Conversation History:\n{history_text}\n\nCurrent Question:\n{query}\n\nAvailable Sources:\n{context}\n\nAnswer:"
    else:
        prompt = f"Question:\n{query}\n\nAvailable Sources:\n{context}\n\nAnswer:"

    answer = ollama_generate(model=CONFIG.rag.default_model, prompt=prompt, system=system)

    citations = []
    cited_indices: set[int] = set()
    raw_indices: list[int] = []

    # Pattern 1: [Source N] or [source N]
    for m in re.finditer(r'\[(?:Source\s+|source\s+)(\d+)\]', answer, re.IGNORECASE):
        raw_indices.append(int(m.group(1)))

    # Pattern 2: [1], [1,2], [1, 2], [1,2,3]
    for m in re.finditer(r'\[(\d+(?:\s*,\s*\d+)*)\]', answer):
        for idx_str in m.group(1).split(','):
            raw_indices.append(int(idx_str.strip()))

    for idx in raw_indices:
        if 0 < idx <= len(docs) and idx not in cited_indices:
            doc = docs[idx - 1]
            citations.append(Citation(
                index=idx,
                source=doc.source,
                page=extract_page_number(doc.source, doc.id),
                chunk_id=doc.id,
                score=doc.score
            ))
            cited_indices.add(idx)

    # If model cited nothing, surface all retrieved docs as implicit sources
    if not citations and docs:
        for i, doc in enumerate(docs, 1):
            citations.append(Citation(
                index=i,
                source=doc.source,
                page=extract_page_number(doc.source, doc.id),
                chunk_id=doc.id,
                score=doc.score
            ))

    citations.sort(key=lambda c: c.index)

    return AnswerWithCitations(
        answer=answer,
        citations=citations,
        source_docs=docs
    )


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
