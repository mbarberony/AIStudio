from __future__ import annotations

import asyncio
import os
import re
import shutil
from pathlib import Path
from typing import Any, List, Dict, Optional
from dataclasses import dataclass

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from local_llm_bot.app.config import CONFIG
from local_llm_bot.app.debug_stats import JsonlStats, compute_jsonl_stats


from local_llm_bot.app.rag_core import retrieve, RetrievedDoc
from local_llm_bot.app.ollama_client import ollama_generate

from local_llm_bot.app.utils.corpus_paths import corpus_exists, list_corpora, corpus_paths


from local_llm_bot.app.utils.repo_root import find_repo_root
from local_llm_bot.app.ingest.index_jsonl import read_jsonl


# ============================================================================
# INLINE CITATION SUPPORT (embedded in API for simplicity)
# ============================================================================

def extract_page_number(source_path: str, chunk_id: str = "") -> Optional[int]:
    """Extract page number from source path or chunk_id"""
    # Try from source path: "document.pdf#page=5"
    page_match = re.search(r'#page=(\d+)', source_path)
    if page_match:
        return int(page_match.group(1))
    
    # Try from filename: "document_p12.pdf"
    page_match = re.search(r'[_\-]p(\d+)', source_path, re.IGNORECASE)
    if page_match:
        return int(page_match.group(1))
    
    # Try from chunk_id: "chunk-page-3"
    if chunk_id:
        page_match = re.search(r'page[_\-]?(\d+)', chunk_id, re.IGNORECASE)
        if page_match:
            return int(page_match.group(1))
    
    return None


def generate_answer_with_citations(
    query: str,
    docs: List[RetrievedDoc],
    conversation_history: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    """Generate answer with citation support"""
    
    if not docs:
        return {
            "answer": "I don't have any relevant documents to answer this question.",
            "citations": [],
            "has_citations": False
        }
    
    # Build context with numbered sources
    # Deduplicate by source file — merge chunks from same doc into one numbered source
    seen_sources: dict[str, int] = {}
    source_chunks: dict[int, list[str]] = {}
    doc_to_index: dict[int, int] = {}  # original doc position -> source index
    
    for i, doc in enumerate(docs):
        src = doc.source
        if src not in seen_sources:
            idx = len(seen_sources) + 1
            seen_sources[src] = idx
            source_chunks[idx] = []
        idx = seen_sources[src]
        source_chunks[idx].append(doc.content)
        doc_to_index[i] = idx

    context_parts = []
    for src, idx in seen_sources.items():
        combined = "\n\n".join(source_chunks[idx])
        context_parts.append(f"[{idx}] {src}\n{combined}")

    context = "\n\n".join(context_parts)
    
    # Remap docs list to deduplicated unique sources for citation building
    unique_docs = []
    seen = set()
    for doc in docs:
        if doc.source not in seen:
            seen.add(doc.source)
            unique_docs.append(doc)
    docs = unique_docs
    
    # Enhanced system prompt with citation instructions
    system = (
        "You are a helpful research assistant.\n"
        "Use the provided sources to answer questions accurately.\n"
        "IMPORTANT: When you use information from a source, cite it using [1], [2], etc.\n"
        "The number should match the source number in the context.\n"
        "You can cite multiple sources like [1,2] or [1][2].\n"
        "Always cite your sources - every factual claim should have a citation. ""Cite sources using the exact numbers shown in brackets at the start of each source, e.g. [1], [2]. Never write [Source N]. ""Do NOT append a References or Sources section at the end of your answer — citations are rendered separately."
    )
    
    # Build prompt with conversation history
    if conversation_history:
        history_text = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in conversation_history[-6:]  # Last 3 exchanges
        ])
        prompt = f"Conversation History:\n{history_text}\n\nCurrent Question:\n{query}\n\nAvailable Sources:\n{context}\n\nAnswer:"
    else:
        prompt = f"Question:\n{query}\n\nAvailable Sources:\n{context}\n\nAnswer:"
    
    # Generate answer
    answer = ollama_generate(model=CONFIG.rag.default_model, prompt=prompt, system=system)
    
    # Extract citations from answer
    citations = []
    cited_indices = set()
    
    # Normalize [Source N] -> [N] before extracting
    answer = re.sub(r'\[Source\s+(\d+)\]', r'[\1]', answer, flags=re.IGNORECASE)
    # Find all citation patterns: [1], [2,3], [1][2], etc.
    citation_patterns = re.findall(r'\[(\d+(?:\s*,\s*\d+)*)\]', answer)
    
    for pattern in citation_patterns:
        for idx_str in re.split(r',\s*', pattern):
            idx = int(idx_str.strip())
            if idx > 0 and idx <= len(docs) and idx not in cited_indices:
                doc = docs[idx - 1]
                page = extract_page_number(doc.source, doc.id)
                
                citations.append({
                    "index": idx,
                    "source": doc.source,
                    "page": page,
                    "chunk_id": doc.id,
                    "score": float(doc.score)
                })
                cited_indices.add(idx)
    
    # Sort citations by index
    citations.sort(key=lambda c: c["index"])
    
    return {
        "answer": answer,
        "citations": citations,
        "has_citations": len(citations) > 0
    }

app = FastAPI(title="AIStudio Local LLM Bot")

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    query: str
    corpus: str = "default"
    top_k: int | None = None
    temperature: float | None = None
    top_p: float | None = None
    conversation_history: List[Dict[str, str]] | None = None  # NEW: For follow-up questions


class CitationResponse(BaseModel):
    index: int
    source: str
    page: int | None = None
    chunk_id: str | None = None
    score: float = 0.0


class AskResponse(BaseModel):
    answer: str
    citations: List[CitationResponse] | None = None  # NEW: Citation metadata
    has_citations: bool = False  # NEW: Flag indicating if citations are present


class RetrieveRequest(BaseModel):
    query: str
    corpus: str = "default"
    top_k: int = 5


class CorpusInfo(BaseModel):
    name: str
    document_count: int | None = None
    size_bytes: int | None = None


class ModelInfo(BaseModel):
    id: str
    name: str
    provider: str
    available: bool = True


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


# Track which models are currently loaded in Ollama memory
_warm_models: set[str] = set()


@app.post("/prewarm")
async def prewarm(model_id: str | None = None) -> dict[str, str]:
    """
    Fire a throwaway request to load the model into unified memory.
    Subsequent queries skip the cold-start penalty (~20-50s → ~7s).
    If model_id is provided, warms that model; otherwise warms the default.
    """
    model = model_id or CONFIG.rag.default_model
    if model in _warm_models:
        return {"status": "already_warm", "model": model}
    try:
        ollama_generate(model=model, prompt="hi", system="")
        _warm_models.add(model)
        return {"status": "warm", "model": model}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prewarm failed: {str(e)}")


def _require_corpus(corpus: str) -> None:
    if not corpus_exists(find_repo_root(Path(__file__)), corpus):
        raise HTTPException(
            status_code=404,
            detail={
                "error": f"Unknown corpus '{corpus}'",
                "available": list_corpora(find_repo_root(Path(__file__))),
            },
        )


def _get_repo_root() -> Path:
    """Get repository root directory"""
    return find_repo_root(Path(__file__))


def _get_corpus_document_count(corpus_name: str) -> int:
    """Count documents in a corpus by reading the index.jsonl file"""
    try:
        repo_root = _get_repo_root()
        paths = corpus_paths(repo_root=repo_root, corpus=corpus_name)
        index_file = paths["index"]
        
        if not index_file.exists():
            return 0
        
        rows = read_jsonl(index_file)
        # Count unique document IDs
        doc_ids = set()
        for row in rows:
            doc_id = row.get("doc_id", "")
            if doc_id:
                doc_ids.add(doc_id)
        
        return len(doc_ids)
    except Exception as e:
        print(f"Error counting documents: {e}")
        return 0


def _get_corpus_size(corpus_name: str) -> int:
    """Get total size of corpus directory in bytes"""
    try:
        repo_root = _get_repo_root()
        paths = corpus_paths(repo_root=repo_root, corpus=corpus_name)
        corpus_dir = paths["base"]
        
        if not corpus_dir.exists():
            return 0
        
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(corpus_dir):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total_size += os.path.getsize(fp)
        
        return total_size
    except Exception as e:
        print(f"Error calculating corpus size: {e}")
        return 0


@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest) -> AskResponse:
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="query must not be empty")
    _require_corpus(req.corpus)
    
    # Use provided top_k or default from config
    top_k = req.top_k if req.top_k is not None else CONFIG.rag.top_k
    
    # Retrieve relevant documents
    docs = retrieve(query=req.query, top_k=top_k, corpus=req.corpus)
    
    # Generate answer with citations
    result = generate_answer_with_citations(
        query=req.query,
        docs=docs,
        conversation_history=req.conversation_history
    )
    
    # Convert to response format
    citation_responses = [
        CitationResponse(**c) for c in result["citations"]
    ] if result["citations"] else None
    
    return AskResponse(
        answer=result["answer"],
        citations=citation_responses,
        has_citations=result["has_citations"]
    )


@app.post("/debug/retrieve")
async def debug_retrieve(req: RetrieveRequest) -> dict[str, Any]:
    _require_corpus(req.corpus)
    docs = retrieve(query=req.query, top_k=req.top_k, corpus=req.corpus)
    return {
        "count": len(docs),
        "docs": [
            {
                "id": d.id,
                "score": d.score,
                "source": d.source,
                "content_preview": (d.content[:280] + "...") if len(d.content) > 280 else d.content,
            }
            for d in docs
        ],
        "config": {
            "use_chroma": CONFIG.rag.use_chroma,
            "hybrid_enabled": getattr(CONFIG.rag, "hybrid_enabled", False),
            "decompose_multi_entity": getattr(CONFIG.rag, "decompose_multi_entity", False),
        },
    }


@app.get("/debug/stats")
async def debug_stats(corpus: str = "default") -> JsonlStats:
    _require_corpus(corpus)
    return compute_jsonl_stats(corpus=corpus)


# CORPUS MANAGEMENT ENDPOINTS

@app.get("/corpora")
async def get_corpora() -> List[CorpusInfo]:
    """
    Get list of available corpora with metadata.
    """
    corpus_names = list_corpora(find_repo_root(Path(__file__)))
    
    corpora_info = []
    for name in corpus_names:
        doc_count = _get_corpus_document_count(name)
        size_bytes = _get_corpus_size(name)
        
        corpora_info.append(CorpusInfo(
            name=name,
            document_count=doc_count,
            size_bytes=size_bytes
        ))
    
    return corpora_info


@app.get("/corpus/{corpus_name}/info")
async def get_corpus_info(corpus_name: str) -> dict[str, Any]:
    """
    Get detailed information about a specific corpus.
    """
    _require_corpus(corpus_name)
    
    repo_root = _get_repo_root()
    paths = corpus_paths(repo_root=repo_root, corpus=corpus_name)
    
    # Get basic stats
    stats = compute_jsonl_stats(corpus=corpus_name)
    doc_count = _get_corpus_document_count(corpus_name)
    size_bytes = _get_corpus_size(corpus_name)
    
    # List files in corpus
    files = []
    corpus_dir = paths["base"]
    if corpus_dir.exists():
        for file_path in corpus_dir.rglob("*"):
            if file_path.is_file() and not file_path.name.startswith('.'):
                relative_path = file_path.relative_to(corpus_dir)
                files.append({
                    "name": file_path.name,
                    "path": str(relative_path),
                    "size": file_path.stat().st_size,
                    "type": file_path.suffix
                })
    
    return {
        "name": corpus_name,
        "status": "available",
        "document_count": doc_count,
        "chunk_count": stats.chunks_total,
        "size_bytes": size_bytes,
        "files": files[:50],  # Limit to 50 files for performance
        "file_count": len(files),
        "stats": stats,
        "paths": {
            "base": str(paths["base"]),
            "index": str(paths["index"]),
            "chroma": str(paths["chroma"])
        }
    }



async def _run_ingest_background(corpus_name: str, uploads_dir) -> None:
    """Run ingest as a background task after upload."""
    import sys, os
    cmd = [sys.executable, "-m", "local_llm_bot.app.ingest",
           "--corpus", corpus_name, "--root", str(uploads_dir)]
    env = {**os.environ, "PYTHONPATH": "src"}
    proc = await asyncio.create_subprocess_exec(
        *cmd, env=env,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode == 0:
        print(f"[ingest] Auto-ingest for '{corpus_name}' complete.")
    else:
        print(f"[ingest] Auto-ingest failed:\n{stderr.decode()}")

@app.post("/corpus/{corpus_name}/upload")
async def upload_to_corpus(
    corpus_name: str,
    file: UploadFile = File(...)
) -> dict[str, Any]:
    """
    Upload a file to the specified corpus.
    Note: This saves the file but does NOT automatically ingest it.
    You must run the ingest command separately to process and embed the file.
    """
    _require_corpus(corpus_name)
    
    repo_root = _get_repo_root()
    paths = corpus_paths(repo_root=repo_root, corpus=corpus_name)
    
    # Create uploads directory in corpus
    uploads_dir = paths["base"] / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    
    # Save uploaded file
    file_path = uploads_dir / file.filename
    
    try:
        # Read file content
        content = await file.read()
        
        # Write to disk
        with open(file_path, "wb") as f:
            f.write(content)
        
        file_size = len(content)

        # Auto-ingest in background
        asyncio.create_task(_run_ingest_background(corpus_name, uploads_dir))

        return {
            "status": "success",
            "message": f"File uploaded and ingestion started.",
            "filename": file.filename,
            "file_path": str(file_path),
            "size_bytes": file_size,
            "content_type": file.content_type,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file: {str(e)}"
        )


class CreateCorpusRequest(BaseModel):
    name: str


@app.post("/corpus/create")
async def create_corpus(request: CreateCorpusRequest) -> dict[str, Any]:
    """
    Create a new corpus directory structure.
    """
    name = request.name

    # Validate corpus name
    if not name or not name.replace("_", "").replace("-", "").isalnum():
        raise HTTPException(
            status_code=400,
            detail="Corpus name must contain only letters, numbers, hyphens, and underscores"
        )

    if corpus_exists(find_repo_root(Path(__file__)), name):
        raise HTTPException(
            status_code=409,
            detail=f"Corpus '{name}' already exists"
        )
    
    repo_root = _get_repo_root()
    paths = corpus_paths(repo_root=repo_root, corpus=name)
    
    try:
        # Create corpus directory structure
        corpus_dir = paths["base"]
        corpus_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (corpus_dir / "uploads").mkdir(exist_ok=True)
        
        # Create empty index file
        index_file = paths["index"]
        index_file.parent.mkdir(parents=True, exist_ok=True)
        index_file.touch()
        
        # Create chroma directory
        chroma_dir = paths["chroma"]
        chroma_dir.mkdir(parents=True, exist_ok=True)
        
        return {
            "status": "success",
            "message": f"Corpus '{name}' created successfully",
            "name": name,
            "paths": {
                "base": str(corpus_dir),
                "uploads": str(corpus_dir / "uploads"),
                "index": str(index_file),
                "chroma": str(chroma_dir)
            },
            "next_steps": f"Upload files to corpus or add documents to {corpus_dir / 'uploads'}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create corpus: {str(e)}"
        )


@app.delete("/corpus/{corpus_name}")
async def delete_corpus(corpus_name: str) -> dict[str, Any]:
    """
    Delete a corpus and all its data.
    WARNING: This is irreversible!
    """
    _require_corpus(corpus_name)
    
    # Prevent deletion of default corpus
    if corpus_name == "default":
        raise HTTPException(
            status_code=403,
            detail="Cannot delete the default corpus"
        )
    
    repo_root = _get_repo_root()
    paths = corpus_paths(repo_root=repo_root, corpus=corpus_name)
    corpus_dir = paths["base"]
    
    try:
        # Delete corpus directory
        if corpus_dir.exists():
            shutil.rmtree(corpus_dir)
        
        return {
            "status": "success",
            "message": f"Corpus '{corpus_name}' deleted successfully",
            "name": corpus_name
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete corpus: {str(e)}"
        )


# MODEL MANAGEMENT ENDPOINTS

@app.get("/models")
async def get_models() -> List[ModelInfo]:
    """
    Get list of available LLM models from Ollama.
    """
    try:
        import ollama
        
        # Try to connect to Ollama and list models
        try:
            models_response = ollama.list()
            # Ollama SDK >= 0.3 returns a ListResponse object with a .models attribute
            # (list of Model objects); older versions returned a dict with 'models' key.
            if hasattr(models_response, 'models'):
                ollama_models = models_response.models  # new SDK: list of Model objects
            else:
                ollama_models = models_response.get('models', [])  # old SDK: dict
            
            # Convert Ollama models to our format
            available_models = []
            for model in ollama_models:
                # New SDK: model is a Model object with a .model attribute (e.g. "llama3.1:8b")
                # Old SDK: model is a dict with 'name' key
                if hasattr(model, 'model'):
                    full_name = model.model  # e.g. "llama3.1:8b"
                elif hasattr(model, 'name'):
                    full_name = model.name
                else:
                    full_name = model.get('name', '') if isinstance(model, dict) else ''
                
                if not full_name:
                    continue

                # Show full name with tag for clarity (e.g. "llama3.1:8b" → "Llama3.1:8b")
                # Capitalise only the first letter to avoid "Llama3.1" vs "llama3.1" confusion
                display_name = full_name[0].upper() + full_name[1:]
                available_models.append(ModelInfo(
                    id=full_name,
                    name=display_name,
                    provider="Ollama",
                    available=True
                ))
            
            # If we got models, return them
            if available_models:
                return available_models
                
        except Exception as e:
            print(f"Could not connect to Ollama: {e}")
        
        # Fallback: return common models with availability unknown
        return [
            ModelInfo(
                id="llama3.2:3b",
                name="Llama 3.2 3B",
                provider="Meta/Ollama",
                available=False
            ),
            ModelInfo(
                id="llama3.1:8b",
                name="Llama 3.1 8B",
                provider="Meta/Ollama",
                available=False
            ),
            ModelInfo(
                id="mistral:7b",
                name="Mistral 7B",
                provider="Mistral/Ollama",
                available=False
            ),
            ModelInfo(
                id="qwen2.5:7b",
                name="Qwen 2.5 7B",
                provider="Alibaba/Ollama",
                available=False
            ),
        ]
    except Exception as e:
        print(f"Error listing models: {e}")
        return []


@app.post("/model/select")
async def select_model(model_id: str) -> dict[str, Any]:
    """
    Select the active LLM model.
    Note: This only validates the model exists. Configuration updates would require
    updating environment variables or config files.
    """
    try:
        import ollama
        
        # Try to validate model exists
        try:
            models_response = ollama.list()
            ollama_models = models_response.get('models', [])
            model_names = [m.get('name', '') for m in ollama_models]
            
            if model_id not in model_names:
                return {
                    "status": "warning",
                    "message": f"Model '{model_id}' not found in Ollama. It may need to be pulled first.",
                    "model_id": model_id,
                    "suggestion": f"Run: ollama pull {model_id}"
                }
        except Exception as e:
            print(f"Could not verify model: {e}")
        
        # Mark new model as cold so next /ask triggers a fresh prewarm
        _warm_models.discard(model_id)

        return {
            "status": "info",
            "message": f"To use model '{model_id}', set environment variable: AISTUDIO_DEFAULT_MODEL={model_id}",
            "model_id": model_id,
            "current_model": CONFIG.rag.default_model,
            "note": "Restart the API server after updating environment variables"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error selecting model: {str(e)}"
        )


@app.get("/config")
async def get_config() -> dict[str, Any]:
    """
    Get current configuration including selected model, corpus, and parameters.
    """
    return {
        "current_model": CONFIG.rag.default_model,
        "current_embed_model": CONFIG.rag.default_embed_model,
        "default_corpus": "default",
        "parameters": {
            "temperature": 0.7,
            "top_k": CONFIG.rag.top_k,
            "top_p": 0.9,
        },
        "rag_config": {
            "use_chroma": CONFIG.rag.use_chroma,
            # "hybrid_enabled": CONFIG.rag.hybrid_enabled,
            # "decompose_multi_entity": CONFIG.rag.decompose_multi_entity,
            "max_distance": CONFIG.rag.max_distance,
        },
        "ingest_config": {
            "chunk_size": CONFIG.ingest.chunk_size,
            "overlap": CONFIG.ingest.overlap,
        }
    }
