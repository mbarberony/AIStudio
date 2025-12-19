from fastapi import FastAPI
from pydantic import BaseModel

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
