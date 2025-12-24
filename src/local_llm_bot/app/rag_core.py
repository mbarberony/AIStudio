from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from local_llm_bot.app.config import CONFIG
from local_llm_bot.app.ingest.index_jsonl import read_jsonl
from local_llm_bot.app.ollama_client import ollama_generate
from local_llm_bot.app.utils.corpus_paths import corpus_paths
from local_llm_bot.app.utils.repo_root import find_repo_root
from local_llm_bot.app.vectorstore import chroma_store


@dataclass(frozen=True)
class RetrievedDoc:
    id: str
    content: str
    source: str
    score: float  # distance for Chroma (lower is better); token score for JSONL (higher is better)


def _repo_root() -> Path:
    return find_repo_root(Path(__file__))


def _lexical_jsonl_retrieve(*, query: str, top_k: int, corpus: str) -> list[RetrievedDoc]:
    """
    Simple lexical fallback retrieval from index.jsonl:
    - tokenizes query (alnum tokens len>=3)
    - scores chunks by token containment count
    """
    paths = corpus_paths(_repo_root(), corpus)
    rows = read_jsonl(paths["index"])
    if not rows:
        return []

    q = query.lower()
    tokens = {t for t in re.findall(r"[a-z0-9]+", q) if len(t) >= 3}
    if not tokens:
        return []

    scored: list[tuple[int, dict[str, Any]]] = []
    for r in rows:
        text = str(r.get("text", "")).lower()
        score = sum(1 for token in tokens if token in text)
        if score > 0:
            scored.append((score, r))

    scored.sort(key=lambda x: x[0], reverse=True)
    best = scored[:top_k]

    out: list[RetrievedDoc] = []
    for score, r in best:
        out.append(
            RetrievedDoc(
                id=str(r.get("chunk_id", "")),
                content=str(r.get("text", "")),
                source=str(r.get("source_path", "")),
                score=float(score),
            )
        )
    return out


def retrieve(
    *, query: str, top_k: int | None = None, corpus: str = "default"
) -> list[RetrievedDoc]:
    k = int(top_k) if top_k is not None else int(CONFIG.rag.top_k)

    # Primary: Chroma retrieval
    if CONFIG.rag.use_chroma:
        paths = corpus_paths(_repo_root(), corpus)

        hits = chroma_store.query(
            query_text=query,
            top_k=k,
            embed_model=CONFIG.rag.default_embed_model,
            persist_dir=paths["chroma"],
            collection_name=f"aistudio_{corpus}",
        )

        # Optional distance filter (OFF by default if max_distance is None)
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
                    score=float(h.distance),  # distance
                )
                for h in hits
            ]

        # Fallback if Chroma yields nothing (best default UX)
        return _lexical_jsonl_retrieve(query=query, top_k=k, corpus=corpus)

    # JSONL-only mode
    return _lexical_jsonl_retrieve(query=query, top_k=k, corpus=corpus)


def generate_answer(*, query: str, docs: list[RetrievedDoc]) -> str:
    context = "\n\n".join(f"[{d.source}] {d.content}" for d in docs) if docs else ""
    system = (
        "You are a concise assistant. Use the provided context. "
        "If the context is insufficient, say you do not know."
    )
    prompt = f"Question:\n{query}\n\nContext:\n{context}\n\nAnswer:"
    return ollama_generate(model=CONFIG.rag.default_model, prompt=prompt, system=system)
