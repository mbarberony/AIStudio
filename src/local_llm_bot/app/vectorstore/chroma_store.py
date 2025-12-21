from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import chromadb

from local_llm_bot.app.ollama_client import ollama_embed
from local_llm_bot.app.utils.paths import find_repo_root

DEFAULT_COLLECTION = "aistudio_chunks"


@dataclass(frozen=True)
class SearchHit:
    chunk_id: str
    text: str
    source_path: str
    distance: float


def chroma_dir() -> Path:
    repo_root = find_repo_root(Path(__file__))
    return repo_root / "data" / "chroma"


def get_collection(name: str = DEFAULT_COLLECTION):
    client = chromadb.PersistentClient(path=str(chroma_dir()))
    return client.get_or_create_collection(name=name)


def upsert_chunks(
    *,
    chunk_ids: list[str],
    texts: list[str],
    metadatas: list[dict[str, Any]],
    embed_model: str,
    collection: str = DEFAULT_COLLECTION,
) -> None:
    if not (len(chunk_ids) == len(texts) == len(metadatas)):
        raise ValueError("chunk_ids, texts, metadatas must be same length")

    embs = ollama_embed(model=embed_model, texts=texts)
    col = get_collection(collection)
    col.upsert(ids=chunk_ids, documents=texts, metadatas=metadatas, embeddings=embs)


def delete_doc(*, doc_id: str, collection: str = DEFAULT_COLLECTION) -> None:
    col = get_collection(collection)
    # Delete all chunks for that doc_id
    col.delete(where={"doc_id": doc_id})


def query(
    *,
    query_text: str,
    top_k: int,
    embed_model: str,
    collection: str = DEFAULT_COLLECTION,
) -> list[SearchHit]:
    q_emb = ollama_embed(model=embed_model, texts=[query_text])[0]
    col = get_collection(collection)

    res = col.query(
        query_embeddings=[q_emb],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    # Chroma returns lists-of-lists
    ids = res["ids"][0]
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]

    hits: list[SearchHit] = []
    for cid, doc, meta, dist in zip(ids, docs, metas, dists, strict=False):
        m = meta or {}
        hits.append(
            SearchHit(
                chunk_id=str(cid),
                text=str(doc),
                source_path=str(m.get("source_path", "")),
                distance=float(dist),
            )
        )
    return hits
