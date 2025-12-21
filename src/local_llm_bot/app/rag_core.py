from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from local_llm_bot.app.ingest.index_jsonl import read_jsonl
from local_llm_bot.app.ollama_client import ollama_generate
from local_llm_bot.app.utils.paths import find_repo_root

DEFAULT_MODEL = "llama3.2:3b"

REPO_ROOT = find_repo_root(Path(__file__))
INDEX_PATH = REPO_ROOT / "data" / "index.jsonl"


@dataclass(frozen=True)
class RetrievedDoc:
    id: str
    content: str
    score: float
    source: str


def _tokens(s: str) -> set[str]:
    # basic alnum tokens; ignore tiny ones
    return {t for t in re.findall(r"[a-z0-9]+", s.lower()) if len(t) >= 3}


def retrieve(query: str, top_k: int = 3) -> list[RetrievedDoc]:
    rows = read_jsonl(INDEX_PATH)
    if not rows:
        return []

    q_tokens = _tokens(query)
    if not q_tokens:
        return []

    scored: list[tuple[int, dict]] = []
    for r in rows:
        text = str(r.get("text", "")).lower()
        score = sum(1 for tok in q_tokens if tok in text)
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


def generate_answer(query: str, docs: list[RetrievedDoc]) -> str:
    context = "\n\n".join(f"[{d.source}] {d.content}" for d in docs) if docs else "None"
    system = (
        "You are a concise assistant. Use the provided context. "
        "If the context is insufficient, say you do not know."
    )
    prompt = f"Question:\n{query}\n\nContext:\n{context}\n\nAnswer:"
    return ollama_generate(model=DEFAULT_MODEL, prompt=prompt, system=system)
