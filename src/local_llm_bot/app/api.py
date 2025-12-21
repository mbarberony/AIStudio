from fastapi import FastAPI
from pydantic import BaseModel

from local_llm_bot.app.debug_stats import compute_jsonl_stats

from . import rag_core  # relative import within local_llm_bot.app

app = FastAPI(
    title="AIStudio RAG API",
    version="0.1.0",
    description="Minimal FastAPI skeleton for the local knowledge engine.",
)


class AskRequest(BaseModel):
    query: str


class AskResponse(BaseModel):
    answer: str


class DebugRetrieveRequest(BaseModel):
    query: str
    top_k: int = 5


@app.get("/health")
async def health() -> dict:
    """
    Simple health check endpoint to verify the API is running.
    """
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest) -> AskResponse:
    """
    RAG-style endpoint (stubbed):
    - Uses rag_core.retrieve() to select relevant docs.
    - Uses rag_core.generate_answer() to build a response.
    Later, rag_core will talk to a real vector store and local LLM.
    """
    docs = rag_core.retrieve(req.query)
    answer = rag_core.generate_answer(req.query, docs)
    return AskResponse(answer=answer)


@app.post("/debug/retrieve")
async def debug_retrieve(req: DebugRetrieveRequest):
    docs = rag_core.retrieve(req.query, top_k=req.top_k)
    return {
        "count": len(docs),
        "docs": [
            {"id": d.id, "source": d.source, "score": d.score, "preview": d.content[:200]}
            for d in docs
        ],
    }


@app.get("/debug/stats")
def debug_stats() -> dict:
    s = compute_jsonl_stats()
    return {
        "data_dir": s.data_dir,
        "paths": {
            "index": s.index_path,
            "manifest": s.manifest_path,
            "failures": s.failures_path,
            "docmap": s.docmap_path,
        },
        "counts": {
            "chunks_total": s.chunks_total,
            "docs_unique": s.docs_unique,
            "sources_unique": s.sources_unique,
            "manifest_entries": s.manifest_entries,
            "failures_total": s.failures_total,
            "docmap_entries": s.docmap_entries,
        },
        "bytes": {
            "index": s.bytes_index,
            "manifest": s.bytes_manifest,
            "failures": s.bytes_failures,
        },
        "top_sources": [{"source": src, "chunks": n} for src, n in s.top_sources],
    }
