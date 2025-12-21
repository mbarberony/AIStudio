from __future__ import annotations

from dataclasses import dataclass

from local_llm_bot.app.ollama_client import ollama_generate
from local_llm_bot.app.vectorstore.chroma_store import query as chroma_query

DEFAULT_MODEL = "llama3.2:3b"
DEFAULT_EMBED_MODEL = "nomic-embed-text"


@dataclass(frozen=True)
class RetrievedDoc:
    id: str
    content: str
    score: float
    source: str


def retrieve(query: str, top_k: int = 3) -> list[RetrievedDoc]:
    hits = chroma_query(query_text=query, top_k=top_k, embed_model=DEFAULT_EMBED_MODEL)
    out: list[RetrievedDoc] = []
    for h in hits:
        out.append(
            RetrievedDoc(
                id=h.chunk_id,
                content=h.text,
                source=h.source_path,
                # Chroma returns distances; smaller is better. Keep as-is for debug.
                score=h.distance,
            )
        )
    return out


def generate_answer(query: str, docs: list[RetrievedDoc]) -> str:
    context = "\n\n".join(f"[{d.source}] {d.content}" for d in docs) if docs else "None"
    system = (
        "You are a concise assistant. Use the provided context. "
        "If the context is insufficient, say you do not know."
    )
    prompt = f"Question:\n{query}\n\nContext:\n{context}\n\nAnswer:"
    return ollama_generate(model=DEFAULT_MODEL, prompt=prompt, system=system)
