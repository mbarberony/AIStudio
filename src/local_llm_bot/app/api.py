from __future__ import annotations

import asyncio
import os
import re
import shutil
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from local_llm_bot.app.config import CONFIG
from local_llm_bot.app.debug_stats import JsonlStats, compute_jsonl_stats
from local_llm_bot.app.ingest.index_jsonl import read_jsonl
from local_llm_bot.app.ollama_client import ollama_generate
from local_llm_bot.app.rag_core import RetrievedDoc, retrieve
from local_llm_bot.app.utils.corpus_paths import corpus_exists, corpus_paths, list_corpora
from local_llm_bot.app.utils.repo_root import find_repo_root

# ============================================================================
# INLINE CITATION SUPPORT (embedded in API for simplicity)
# ============================================================================


def extract_page_number(source_path: str, chunk_id: str = "") -> int | None:
    """Extract page number from source path or chunk_id"""
    # Try from source path: "document.pdf#page=5"
    page_match = re.search(r"#page=(\d+)", source_path)
    if page_match:
        return int(page_match.group(1))

    # Try from filename: "document_p12.pdf"
    page_match = re.search(r"[_\-]p(\d+)", source_path, re.IGNORECASE)
    if page_match:
        return int(page_match.group(1))

    # Try from chunk_id: "chunk-page-3"
    if chunk_id:
        page_match = re.search(r"page[_\-]?(\d+)", chunk_id, re.IGNORECASE)
        if page_match:
            return int(page_match.group(1))

    return None


def _load_corpus_search_guidance(corpus_name: str) -> str:
    """
    Load search_guidance from corpus_meta.yaml if it exists.
    Returns empty string silently if file missing or field absent.
    """
    try:
        repo_root = _get_repo_root()
        meta_path = repo_root / "data" / "corpora" / corpus_name / "corpus_meta.yaml"
        if meta_path.exists():
            import yaml

            with open(meta_path) as f:
                meta = yaml.safe_load(f) or {}
            guidance = meta.get("search_guidance", "").strip()
            return guidance
    except Exception:
        pass
    return ""


def generate_answer_with_citations(
    query: str,
    docs: list[RetrievedDoc],
    conversation_history: list[dict[str, str]] | None = None,
    corpus: str | None = None,
) -> dict[str, Any]:
    """Generate answer with citation support"""

    if not docs:
        return {
            "answer": "I don't have any relevant documents to answer this question.",
            "citations": [],
            "has_citations": False,
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
    num_sources = len(docs)
    system = (
        "You are a precise research assistant. Answer using ONLY the provided sources.\n"
        f"There are exactly {num_sources} sources, numbered [1] through [{num_sources}].\n"
        "CITATION RULES — follow exactly:\n"
        "- Cite every factual claim with [N] where N is the source number.\n"
        "- You may combine citations: [1,2] or [1][2].\n"
        f"- NEVER use numbers outside the range [1] to [{num_sources}] as citations.\n"
        "- Never write [Source N] — only [N].\n"
        "- Do NOT append a References or Sources section — citations are rendered separately.\n"
        "- If the sources lack sufficient information, say so explicitly.\n"
        "- NEVER mention file paths, directory names, or system paths in your answer. Refer to sources by citation number [N] only."
    )

    # Inject corpus search guidance if available (corpus_meta.yaml → search_guidance field)
    if corpus:
        guidance = _load_corpus_search_guidance(corpus)
        if guidance:
            system += (
                "\n\nCORPUS SEARCH GUIDANCE — follow these routing rules when selecting sources:\n"
                + guidance
            )

    # Build prompt with conversation history
    if conversation_history:
        history_text = "\n".join(
            [
                f"{msg['role'].upper()}: {msg['content']}"
                for msg in conversation_history[-6:]  # Last 3 exchanges
            ]
        )
        prompt = f"Conversation History:\n{history_text}\n\nCurrent Question:\n{query}\n\nAvailable Sources:\n{context}\n\nAnswer:"
    else:
        prompt = f"Question:\n{query}\n\nAvailable Sources:\n{context}\n\nAnswer:"

    # Generate answer
    answer = ollama_generate(model=CONFIG.rag.default_model, prompt=prompt, system=system)

    # Extract citations from answer
    citations = []
    cited_indices = set()

    # Normalize [Source N] -> [N] before extracting
    answer = re.sub(r"\[Source\s+(\d+)\]", r"[\1]", answer, flags=re.IGNORECASE)
    # Find all citation patterns: [1], [2,3], [1][2], etc.
    citation_patterns = re.findall(r"\[(\d+(?:\s*,\s*\d+)*)\]", answer)

    for pattern in citation_patterns:
        for idx_str in re.split(r",\s*", pattern):
            idx = int(idx_str.strip())
            if idx > 0 and idx <= len(docs) and idx not in cited_indices:
                doc = docs[idx - 1]
                page = extract_page_number(doc.source, doc.id)

                citations.append(
                    {
                        "index": idx,
                        "source": doc.source,
                        "page": page,
                        "chunk_id": doc.id,
                        "score": float(doc.score),
                    }
                )
                cited_indices.add(idx)

    # Sort citations by index
    citations.sort(key=lambda c: c["index"])

    return {"answer": answer, "citations": citations, "has_citations": len(citations) > 0}


app = FastAPI(title="AIStudio Local LLM Bot")

# In-memory ingest status keyed by corpus name
_ingest_status: dict[str, dict] = {}

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
    firm: str | None = None
    year: str | None = None
    temperature: float | None = None
    top_p: float | None = None
    conversation_history: list[dict[str, str]] | None = None  # NEW: For follow-up questions


class CitationResponse(BaseModel):
    index: int
    source: str
    page: int | None = None
    chunk_id: str | None = None
    score: float = 0.0


class AskResponse(BaseModel):
    answer: str
    citations: list[CitationResponse] | None = None  # NEW: Citation metadata
    has_citations: bool = False  # NEW: Flag indicating if citations are present


class RetrieveRequest(BaseModel):
    query: str
    corpus: str = "default"
    top_k: int = 5
    firm: str | None = None
    year: str | None = None


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
        raise HTTPException(status_code=500, detail=f"Prewarm failed: {str(e)}") from e


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
        for dirpath, _dirnames, filenames in os.walk(corpus_dir):
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
    docs = retrieve(query=req.query, top_k=top_k, corpus=req.corpus, firm=req.firm, year=req.year)

    # Generate answer with citations
    result = generate_answer_with_citations(
        query=req.query,
        docs=docs,
        conversation_history=req.conversation_history,
        corpus=req.corpus,
    )

    # Convert to response format
    citation_responses = (
        [CitationResponse(**c) for c in result["citations"]] if result["citations"] else None
    )

    return AskResponse(
        answer=result["answer"], citations=citation_responses, has_citations=result["has_citations"]
    )


@app.post("/debug/retrieve")
async def debug_retrieve(req: RetrieveRequest) -> dict[str, Any]:
    _require_corpus(req.corpus)
    docs = retrieve(
        query=req.query, top_k=req.top_k, corpus=req.corpus, firm=req.firm, year=req.year
    )
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
async def get_corpora() -> list[CorpusInfo]:
    """
    Get list of available corpora with metadata.
    """
    corpus_names = list_corpora(find_repo_root(Path(__file__)))

    corpora_info = []
    for name in corpus_names:
        doc_count = _get_corpus_document_count(name)
        size_bytes = _get_corpus_size(name)

        corpora_info.append(CorpusInfo(name=name, document_count=doc_count, size_bytes=size_bytes))

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

    # Get real chunk count from Qdrant
    qdrant_chunk_count = 0
    try:
        from qdrant_client import QdrantClient

        qc = QdrantClient(host="localhost", port=6333)
        col_info = qc.get_collection(f"aistudio_{corpus_name}")
        qdrant_chunk_count = col_info.points_count or 0
    except Exception:
        qdrant_chunk_count = stats.chunks_total  # fallback to JSONL count

    # List files in corpus
    # Return plain filenames from uploads/ only
    uploads_dir = paths["base"] / "uploads"
    files: list[str] = []
    if uploads_dir.exists():
        files = sorted(
            f.name for f in uploads_dir.iterdir() if f.is_file() and not f.name.startswith(".")
        )

    return {
        "name": corpus_name,
        "status": "available",
        "document_count": doc_count,
        "chunk_count": qdrant_chunk_count,
        "size_bytes": size_bytes,
        "files": files,
        "file_count": len(files),
        "stats": stats,
        "paths": {
            "base": str(paths["base"]),
            "index": str(paths["index"]),
        },
    }


async def _run_ingest_background(corpus_name: str, uploads_dir) -> None:
    """Run ingest as a background task after upload.

    Streams stderr line-by-line to parse tqdm progress output in real time.
    tqdm emits lines like:
      Process: 100%|...| 143/143 [03:46<00:00, 1.59s/file, chunks=105964, failed=0, processed=143, skipped=0]
    We parse chunks=N, processed=N, and elapsed time so the UI can show live progress.
    """
    import os
    import re
    import sys
    import time

    cmd = [
        sys.executable,
        "-m",
        "local_llm_bot.app.ingest",
        "--corpus",
        corpus_name,
        "--root",
        str(uploads_dir),
    ]
    env = {**os.environ, "PYTHONPATH": "src", "PYTHONUNBUFFERED": "1"}
    start_time = time.time()
    _ingest_status[corpus_name] = {
        "status": "running",
        "chunks_written": 0,
        "files_processed": 0,
        "files_total": 0,
        "elapsed_sec": 0,
        "message": "Indexing…",
    }

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        env=env,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    # Stream stderr lines as they arrive — tqdm writes progress to stderr.
    # tqdm emits two bar types:
    #   Discover: N file [...]           — file discovery phase, no chunks
    #   Process:  N%|...| N/N [..., chunks=N, processed=N, ...]  — actual indexing
    # We track the last Process line separately so the final summary uses
    # real chunk/file counts, not the Discover line which has no chunks.
    async def _stream_stderr() -> str:
        last_process_line = ""
        assert proc.stderr is not None
        async for raw in proc.stderr:
            line = raw.decode(errors="replace").strip()
            if not line:
                continue
            elapsed = int(time.time() - start_time)

            # Only parse lines from the Process bar (has chunks= or N/N pattern with %)
            is_process_line = "chunks=" in line or (
                "%" in line and re.search(r"\|\s*\d+/\d+", line)
            )
            if not is_process_line:
                continue

            last_process_line = line

            # Parse tqdm postfix fields: chunks=N, processed=N, failed=N
            chunks = 0
            files_processed = 0
            files_total = 0

            m_chunks = re.search(r"chunks=(\d+)", line)
            if m_chunks:
                chunks = int(m_chunks.group(1))

            m_proc = re.search(r"processed=(\d+)", line)
            if m_proc:
                files_processed = int(m_proc.group(1))

            # Parse "N/N" from tqdm bar: "143/143"
            m_total = re.search(r"\|\s*(\d+)/(\d+)", line)
            if m_total:
                files_processed = files_processed or int(m_total.group(1))
                files_total = int(m_total.group(2))

            # Build human message
            if chunks > 0 and files_total > 0:
                msg = f"{files_processed}/{files_total} files · {chunks:,} chunks"
            elif files_total > 0:
                msg = f"{files_processed}/{files_total} files"
            else:
                msg = "Indexing…"

            _ingest_status[corpus_name] = {
                "status": "running",
                "chunks_written": chunks,
                "files_processed": files_processed,
                "files_total": files_total,
                "elapsed_sec": elapsed,
                "message": msg,
            }
        return last_process_line

    # Drain stdout silently (keep pipe from blocking)
    async def _drain_stdout() -> None:
        assert proc.stdout is not None
        async for _ in proc.stdout:
            pass

    last_line, _ = await asyncio.gather(_stream_stderr(), _drain_stdout())
    await proc.wait()

    elapsed = int(time.time() - start_time)
    mins, secs = divmod(elapsed, 60)
    elapsed_str = f"{mins}m {secs}s" if mins else f"{secs}s"

    if proc.returncode == 0:
        # Extract final counts from last tqdm line
        final_chunks = 0
        final_files = 0
        m_chunks = re.search(r"chunks=(\d+)", last_line)
        if m_chunks:
            final_chunks = int(m_chunks.group(1))
        m_total = re.search(r"\|\s*(\d+)/(\d+)", last_line)
        if m_total:
            final_files = int(m_total.group(2))

        summary = f"{final_files} files · {final_chunks:,} chunks · {elapsed_str}"
        _ingest_status[corpus_name] = {
            "status": "done",
            "chunks_written": final_chunks,
            "files_processed": final_files,
            "files_total": final_files,
            "elapsed_sec": elapsed,
            "elapsed_str": elapsed_str,
            "summary": summary,
            "message": summary,
        }
        print(f"[ingest] '{corpus_name}' complete — {summary}")
    else:
        _ingest_status[corpus_name] = {
            "status": "error",
            "chunks_written": 0,
            "files_processed": 0,
            "files_total": 0,
            "elapsed_sec": elapsed,
            "message": "Ingestion failed — check server logs",
        }
        print(f"[ingest] '{corpus_name}' failed after {elapsed_str}:\n{last_line}")


@app.post("/corpus/{corpus_name}/upload")
async def upload_to_corpus(
    corpus_name: str,
    file: UploadFile = File(...),  # noqa: B008
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

        # File saved only — ingest triggered separately via POST /corpus/{name}/ingest
        # Batch uploads must NOT each spawn their own ingest: concurrent processes
        # stomp on each other in Qdrant, causing false error status.
        return {
            "status": "saved",
            "message": "File saved. Call /ingest to index.",
            "filename": file.filename,
            "file_path": str(file_path),
            "size_bytes": file_size,
            "content_type": file.content_type,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}") from e


@app.post("/corpus/{corpus_name}/ingest")
async def trigger_ingest(corpus_name: str) -> dict[str, Any]:
    """
    Trigger a single ingest pass over all files in uploads/.
    Call once after all files are uploaded — never per-file.
    Guards against concurrent runs (returns already_running if busy).
    """
    _require_corpus(corpus_name)
    repo_root = _get_repo_root()
    paths = corpus_paths(repo_root=repo_root, corpus=corpus_name)
    uploads_dir = paths["base"] / "uploads"

    if _ingest_status.get(corpus_name, {}).get("status") == "running":
        return {"status": "already_running", "message": "Ingestion already in progress."}

    asyncio.create_task(_run_ingest_background(corpus_name, uploads_dir))
    return {"status": "started", "message": f"Ingestion started for corpus '{corpus_name}'."}


class CreateCorpusRequest(BaseModel):
    name: str


@app.get("/corpus/{corpus_name}/ingest-status")
async def get_ingest_status(corpus_name: str) -> dict:
    """Poll ingestion progress. status: idle|running|done|error"""
    return _ingest_status.get(
        corpus_name,
        {"status": "idle", "chunks_written": 0, "message": "No recent ingestion"},
    )


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
            detail="Corpus name must contain only letters, numbers, hyphens, and underscores",
        )

    if corpus_exists(find_repo_root(Path(__file__)), name):
        raise HTTPException(status_code=409, detail=f"Corpus '{name}' already exists")

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
                "chroma": str(chroma_dir),
            },
            "next_steps": f"Upload files to corpus or add documents to {corpus_dir / 'uploads'}",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create corpus: {str(e)}") from e


@app.delete("/corpus/{corpus_name}")
async def delete_corpus(corpus_name: str, confirm: str = "") -> dict[str, Any]:
    """
    Move a corpus to Mac Trash (~/.Trash) and delete its Qdrant collection.
    Requires confirm=yes query parameter.
    To restore: move folder from ~/.Trash back to data/corpora/ and re-ingest.
    See HOW_TO.md for recovery instructions.
    """
    if confirm.lower() != "yes":
        raise HTTPException(
            status_code=400, detail="Confirmation required. Pass ?confirm=yes to proceed."
        )

    _require_corpus(corpus_name)

    if corpus_name == "default":
        raise HTTPException(status_code=403, detail="Cannot delete the default corpus")

    repo_root = _get_repo_root()
    paths = corpus_paths(repo_root=repo_root, corpus=corpus_name)
    corpus_dir = paths["base"]

    # Step 1: Delete Qdrant collection
    try:
        from qdrant_client import QdrantClient

        qc = QdrantClient(host="localhost", port=6333)
        qc.delete_collection(f"aistudio_{corpus_name}")
    except Exception as e:
        print(f"[delete_corpus] Qdrant cleanup warning: {e}")

    # Step 2: Move corpus folder to Mac Trash (recoverable)
    try:
        trash_dir = Path.home() / ".Trash"
        trash_dir.mkdir(exist_ok=True)
        dest = trash_dir / f"AIStudio_{corpus_name}"
        if dest.exists():
            import time as _time

            dest = trash_dir / f"AIStudio_{corpus_name}_{int(_time.time())}"
        if corpus_dir.exists():
            shutil.move(str(corpus_dir), str(dest))

        return {
            "status": "success",
            "message": f"Corpus '{corpus_name}' moved to Trash. To restore, see HOW_TO.md.",
            "name": corpus_name,
            "trash_path": str(dest),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete corpus: {str(e)}") from e


@app.delete("/corpus/{corpus_name}/file/{filename:path}")
async def delete_file_from_corpus(corpus_name: str, filename: str) -> dict[str, Any]:
    """Move a file to trash and remove its Qdrant chunks surgically."""
    _require_corpus(corpus_name)
    repo_root = _get_repo_root()
    paths = corpus_paths(repo_root=repo_root, corpus=corpus_name)
    uploads_dir = paths["base"] / "uploads"
    file_path = uploads_dir / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {filename}")

    try:
        file_path.resolve().relative_to(uploads_dir.resolve())
    except ValueError as e:
        raise HTTPException(status_code=403, detail="Access denied") from e

    deleted_chunks = 0
    try:
        from qdrant_client import QdrantClient
        from qdrant_client.models import FieldCondition, Filter, MatchValue

        qc = QdrantClient(host="localhost", port=6333)
        collection = f"aistudio_{corpus_name}"
        scroll_result = qc.scroll(
            collection_name=collection,
            scroll_filter=Filter(
                must=[FieldCondition(key="source_path", match=MatchValue(value=str(file_path)))]
            ),
            limit=10000,
            with_payload=False,
        )
        point_ids = [p.id for p in scroll_result[0]]
        deleted_chunks = len(point_ids)
        if point_ids:
            qc.delete(collection_name=collection, points_selector=point_ids)
    except Exception as e:
        print(f"[delete_file] Qdrant warning: {e}")

    manifest_path = paths["base"] / "manifest.jsonl"
    if manifest_path.exists():
        kept = [ln for ln in manifest_path.read_text().splitlines() if str(file_path) not in ln]
        manifest_path.write_text("\n".join(kept) + ("\n" if kept else ""))

    index_path = paths.get("index")
    if index_path and Path(index_path).exists():
        kept = [ln for ln in Path(index_path).read_text().splitlines() if str(file_path) not in ln]
        Path(index_path).write_text("\n".join(kept) + ("\n" if kept else ""))

    import time as _time

    trash_dir = uploads_dir / "trash"
    trash_dir.mkdir(parents=True, exist_ok=True)
    trash_path = trash_dir / filename
    if trash_path.exists():
        stem, suffix = Path(filename).stem, Path(filename).suffix
        trash_path = trash_dir / f"{stem}_{int(_time.time())}{suffix}"
    shutil.move(str(file_path), str(trash_path))

    return {
        "status": "success",
        "message": f"'{filename}' moved to trash. {deleted_chunks} chunks removed.",
        "filename": filename,
        "chunks_removed": deleted_chunks,
    }


@app.get("/about")
async def get_about() -> dict[str, Any]:
    """Serve about.md content for the About modal.
    Rewrites relative markdown links to absolute file:// paths so they work
    offline without any external dependency."""
    import re

    repo_root = _get_repo_root()
    for fname in ["about.md", "ABOUT.md"]:
        p = repo_root / fname
        if p.exists():
            content = p.read_text(encoding="utf-8")

            # Rewrite relative links [text](relative/path) → [text](file:///abs/path)
            def rewrite_link(m: re.Match) -> str:
                text, href = m.group(1), m.group(2)
                if href.startswith(("http", "mailto", "file://")):
                    return m.group(0)  # leave absolute links alone
                # Split anchor from path before resolving
                anchor = ""
                if "#" in href:
                    href, anchor = href.split("#", 1)
                    anchor = f"#{anchor}"
                abs_path = (repo_root / href).resolve()
                return f"[{text}](file://{abs_path}{anchor})"

            content = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", rewrite_link, content)
            return {"content": content, "format": "markdown"}
    return {
        "content": "# AIStudio\n\nLocal RAG system — Apple Silicon, no cloud dependency.",
        "format": "markdown",
    }


@app.get("/howto")
async def get_howto() -> dict[str, Any]:
    """Serve HOWTO.md as a local file:// URL redirect.
    Returns the absolute path so the frontend can open it directly.
    Used by the corpus-deleted message link: see HOWTO.
    """
    repo_root = _get_repo_root()
    for fname in ["HOWTO.md", "howto.md"]:
        p = repo_root / fname
        if p.exists():
            return {"path": str(p.resolve()), "url": f"file://{p.resolve()}"}
    return {"path": "", "url": ""}


# MODEL MANAGEMENT ENDPOINTS


@app.get("/models")
async def get_models() -> list[ModelInfo]:
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
            if hasattr(models_response, "models"):
                ollama_models = models_response.models  # new SDK: list of Model objects
            else:
                ollama_models = models_response.get("models", [])  # old SDK: dict

            # Convert Ollama models to our format
            available_models = []
            for model in ollama_models:
                # New SDK: model is a Model object with a .model attribute (e.g. "llama3.1:8b")
                # Old SDK: model is a dict with 'name' key
                if hasattr(model, "model"):
                    full_name = model.model  # e.g. "llama3.1:8b"
                elif hasattr(model, "name"):
                    full_name = model.name
                else:
                    full_name = model.get("name", "") if isinstance(model, dict) else ""

                if not full_name:
                    continue

                # Show full name with tag for clarity (e.g. "llama3.1:8b" → "Llama3.1:8b")
                # Capitalise only the first letter to avoid "Llama3.1" vs "llama3.1" confusion
                display_name = full_name[0].upper() + full_name[1:]
                available_models.append(
                    ModelInfo(id=full_name, name=display_name, provider="Ollama", available=True)
                )

            # If we got models, return them
            if available_models:
                return available_models

        except Exception as e:
            print(f"Could not connect to Ollama: {e}")

        # Fallback: return common models with availability unknown
        return [
            ModelInfo(
                id="llama3.2:3b", name="Llama 3.2 3B", provider="Meta/Ollama", available=False
            ),
            ModelInfo(
                id="llama3.1:8b", name="Llama 3.1 8B", provider="Meta/Ollama", available=False
            ),
            ModelInfo(
                id="mistral:7b", name="Mistral 7B", provider="Mistral/Ollama", available=False
            ),
            ModelInfo(
                id="qwen2.5:7b", name="Qwen 2.5 7B", provider="Alibaba/Ollama", available=False
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
            ollama_models = models_response.get("models", [])
            model_names = [m.get("name", "") for m in ollama_models]

            if model_id not in model_names:
                return {
                    "status": "warning",
                    "message": f"Model '{model_id}' not found in Ollama. It may need to be pulled first.",
                    "model_id": model_id,
                    "suggestion": f"Run: ollama pull {model_id}",
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
            "note": "Restart the API server after updating environment variables",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error selecting model: {str(e)}") from e


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
        },
    }


@app.get("/source")
async def serve_source(path: str, page: int | None = None) -> FileResponse:
    """
    Serve a local source document (PDF, PPTX, etc.) by absolute path.
    Replaces file:// links — works in all browsers including Safari.
    The optional page parameter is passed as a URL fragment hint in the
    response header so the browser can scroll to the cited page.
    """
    file_path = Path(path)
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail=f"Source file not found: {path}")

    # Security: only serve files within known corpus/data directories
    repo = _get_repo_root()
    allowed_roots = [
        repo / "data",
        Path.home() / "Downloads",
    ]
    resolved = file_path.resolve()
    if not any(str(resolved).startswith(str(r.resolve())) for r in allowed_roots):
        raise HTTPException(status_code=403, detail="Access to this path is not permitted")

    media_type = (
        "application/pdf" if file_path.suffix.lower() == ".pdf" else "application/octet-stream"
    )

    headers = {}
    if page is not None:
        # Hint the browser to scroll to the page via Content-Disposition filename fragment
        headers["X-PDF-Page"] = str(page)

    return FileResponse(
        path=str(resolved),
        media_type=media_type,
        headers=headers,
        filename=file_path.name,
        content_disposition_type="inline",
    )
