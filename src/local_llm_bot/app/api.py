from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from local_llm_bot.app import rag_core
from local_llm_bot.app.config import CONFIG
from local_llm_bot.app.debug_stats import compute_stats
from local_llm_bot.app.utils.corpus_paths import corpus_paths
from local_llm_bot.app.utils.repo_root import find_repo_root

app = FastAPI(title="AIStudio Local LLM Bot", version="0.1.0")


class AskRequest(BaseModel):
    query: str = Field(..., min_length=1)
    corpus: str = Field(default="default")
    top_k: int | None = Field(default=None, ge=1, le=50)


class AskResponse(BaseModel):
    answer: str


class RetrieveRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=50)
    corpus: str = Field(default="default", min_length=1)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest) -> AskResponse:
    docs = rag_core.retrieve(query=req.query, top_k=req.top_k, corpus=req.corpus)
    answer = rag_core.generate_answer(query=req.query, docs=docs)
    return AskResponse(answer=answer)


@app.post("/debug/retrieve")
def debug_retrieve(req: RetrieveRequest) -> dict[str, Any]:
    # def retrieve(*, query: str, top_k: int | None = None, corpus: str = "default") -> list[RetrievedDoc]:
    docs = rag_core.retrieve(query=req.query, top_k=req.top_k, corpus=req.corpus)
    return {
        "count": len(docs),
        "docs": [
            {"id": d.id, "score": d.score, "source": d.source, "content_preview": d.content[:240]}
            for d in docs
        ],
    }


def _count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())


# @app.get("/debug/stats")
# def debug_stats(corpus: str = "default") -> dict[str, Any]:
#     repo_root = find_repo_root(Path(__file__))
#     paths = corpus_paths(repo_root, corpus)
#
#     rows = read_jsonl(paths["index"])
#     sources = [str(r.get("source_path", "")) for r in rows if r.get("source_path")]
#
#     counts: dict[str, int] = {}
#     for s in sources:
#         counts[s] = counts.get(s, 0) + 1
#
#     top_sources = sorted(
#         [{"source": k, "chunks": v} for k, v in counts.items()],
#         key=lambda x: x["chunks"],
#         reverse=True,
#     )[:10]
#
#     return {
#         "corpus": corpus,
#         "data_dir": str(paths["base"]),
#         "paths": {k: str(v) for k, v in paths.items()},
#         "counts": {
#             "chunks_total": _count_jsonl(paths["index"]),
#             "manifest_entries": _count_jsonl(paths["manifest"]),
#             "failures_total": _count_jsonl(paths["failures"]),
#             "docmap_exists": paths["docmap"].exists(),
#         },
#         "bytes": {
#             "index": paths["index"].stat().st_size if paths["index"].exists() else 0,
#             "manifest": paths["manifest"].stat().st_size if paths["manifest"].exists() else 0,
#             "failures": paths["failures"].stat().st_size if paths["failures"].exists() else 0,
#         },
#         "top_sources": top_sources,
#     }


@app.get("/debug/stats")
def debug_stats(corpus: str = "default") -> dict[str, Any]:
    data = compute_stats(corpus=corpus, top_n=10)
    # Optional: include config snapshot (this is a reasonable use of CONFIG)
    data["config"] = {
        "use_chroma": CONFIG.rag.use_chroma,
        "top_k": CONFIG.rag.top_k,
        "max_distance": CONFIG.rag.max_distance,
        "default_model": CONFIG.rag.default_model,
        "default_embed_model": CONFIG.rag.default_embed_model,
        "ollama_base_url": CONFIG.ollama.base_url,
        "chroma_query_include": CONFIG.chroma.query_include,
    }
    return data


@app.get("/debug/corpora")
def debug_corpora() -> dict[str, Any]:
    repo_root = find_repo_root(Path(__file__))
    base = repo_root / "data" / "corpora"
    base.mkdir(parents=True, exist_ok=True)

    corpora: list[dict[str, Any]] = []
    for d in sorted([p for p in base.iterdir() if p.is_dir()]):
        name = d.name
        paths = corpus_paths(repo_root, name)
        corpora.append(
            {
                "corpus": name,
                "paths": {k: str(v) for k, v in paths.items()},
                "counts": {
                    "chunks_total": _count_jsonl(paths["index"]),
                    "manifest_entries": _count_jsonl(paths["manifest"]),
                    "failures_total": _count_jsonl(paths["failures"]),
                },
            }
        )
    return {"corpora": corpora}
