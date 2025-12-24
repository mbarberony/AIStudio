# src/local_llm_bot/app/vectorstore/chroma_store.py
from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import chromadb

from local_llm_bot.app.config import CONFIG
from local_llm_bot.app.ollama_client import ollama_embed


@dataclass(frozen=True)
class ChromaHit:
    chunk_id: str
    text: str
    metadata: dict[str, Any]
    distance: float


def get_client(persist_dir: Path) -> chromadb.ClientAPI:
    """
    Create a persistent Chroma client rooted at persist_dir.
    """
    persist_dir.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(persist_dir))


def get_or_create_collection(
    *,
    client: chromadb.ClientAPI,
    name: str,
    metadata: dict[str, Any] | None = None,
) -> chromadb.Collection:
    try:
        return client.get_collection(name=name)
    except Exception:
        if metadata is None:
            # IMPORTANT: do NOT pass empty metadata
            return client.create_collection(name=name)
        return client.create_collection(name=name, metadata=metadata)


def _batched[T](items: list[T], batch_size: int) -> list[list[T]]:
    if batch_size <= 0:
        return [items]
    return [items[i : i + batch_size] for i in range(0, len(items), batch_size)]


def upsert_chunks(
    *,
    persist_dir: Path,
    collection_name: str,
    embed_model: str,
    ids: list[str],
    documents: list[str],
    metadatas: list[dict[str, Any]],
    on_batch_done: Callable[[int], None] | None = None,
    batch_size: int | None = None,
) -> None:
    """
    Upsert chunk documents into Chroma using embeddings from Ollama.

    - Embeds in batches (default CONFIG.vectorstore.embed_batch_size, else 32)
    - Calls on_batch_done(n) after each batch (for progress bars)
    """
    if not (len(ids) == len(documents) == len(metadatas)):
        raise ValueError("ids, documents, and metadatas must be the same length")

    if not ids:
        return

    client = get_client(persist_dir)
    col = get_or_create_collection(client=client, name=collection_name)

    DEFAULT_EMBED_BATCH_SIZE = 32

    env_bs = os.getenv("AISTUDIO_CHROMA_EMBED_BATCH_SIZE")
    try:
        env_bs_i = int(env_bs) if env_bs else None
    except ValueError:
        env_bs_i = None

    bs = int(batch_size) if batch_size is not None else int(env_bs_i or DEFAULT_EMBED_BATCH_SIZE)
    if bs <= 0:
        bs = DEFAULT_EMBED_BATCH_SIZE

    # process in aligned batches
    for idx_batch in _batched(list(range(len(ids))), bs):
        b_ids = [ids[i] for i in idx_batch]
        b_docs = [documents[i] for i in idx_batch]
        b_metas = [metadatas[i] for i in idx_batch]

        # NOTE: ollama_embed must return list[list[float]] aligned with b_docs
        b_embs = ollama_embed(model=embed_model, texts=b_docs)
        if not isinstance(b_embs, list) or len(b_embs) != len(b_docs):
            raise ValueError("Embedding backend returned wrong shape")

        col.upsert(ids=b_ids, documents=b_docs, metadatas=b_metas, embeddings=b_embs)

        if on_batch_done is not None:
            on_batch_done(len(b_ids))


def delete_chunks(*, persist_dir: Path, collection_name: str, ids: list[str]) -> None:
    """
    Delete chunks by id from a Chroma collection.
    """
    if not ids:
        return
    client = get_client(persist_dir)
    col = get_or_create_collection(client=client, name=collection_name)
    col.delete(ids=ids)


def query(
    *,
    persist_dir: Path,
    collection_name: str,
    query_text: str,
    top_k: int,
    embed_model: str,
) -> list[ChromaHit]:
    """
    Query Chroma using a query embedding computed by Ollama.
    Returns hits with distance (lower is better).
    """
    client = get_client(persist_dir)
    col = get_or_create_collection(client=client, name=collection_name)

    q_emb = ollama_embed(model=embed_model, texts=[query_text])[0]

    # Important: Chroma "include" does NOT accept "ids" (ids are returned separately)
    # Important: Chroma "include" does NOT accept "ids" (ids are returned separately)
    include = getattr(CONFIG.rag, "chroma_query_include", None)
    if not include:
        include = ["documents", "metadatas", "distances"]

    # Defensive: strip any accidental "ids"
    include = [x for x in list(include) if x != "ids"]

    res = col.query(
        query_embeddings=[q_emb],
        n_results=int(top_k),
        include=list(include),
    )

    ids = (res.get("ids") or [[]])[0]
    docs = (res.get("documents") or [[]])[0]
    metas = (res.get("metadatas") or [[]])[0]
    dists = (res.get("distances") or [[]])[0]

    out: list[ChromaHit] = []
    for cid, doc, meta, dist in zip(ids, docs, metas, dists, strict=False):
        out.append(
            ChromaHit(
                chunk_id=str(cid),
                text=str(doc),
                metadata=dict(meta or {}),
                distance=float(dist) if dist is not None else 0.0,
            )
        )
    return out
