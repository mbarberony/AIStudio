import re
from dataclasses import dataclass
from pathlib import Path

from local_llm_bot.app.utils.paths import find_repo_root

from .ingest.index import read_jsonl
from .ollama_client import ollama_generate

DEFAULT_MODEL = "llama3.2:3b"
REPO_ROOT = find_repo_root(Path(__file__))
INDEX_PATH = REPO_ROOT / "data" / "index.jsonl"


@dataclass
class RetrievedDoc:
    """Simple placeholder for a retrieved document chunk."""

    id: str
    content: str
    score: float
    source: str


def retrieve(query: str, top_k: int = 3) -> list[RetrievedDoc]:
    rows = read_jsonl(INDEX_PATH)
    if not rows:
        return []

    q = query.lower()
    tokens = {t for t in re.findall(r"[a-z0-9]+", q) if len(t) >= 3}

    scored: list[tuple[int, dict]] = []
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
                id=str(r.get("chunk_id")),
                content=str(r.get("text")),
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
