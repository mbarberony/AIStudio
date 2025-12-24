from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, Field


def _env_bool(name: str, default: bool) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "y", "on"}


def _env_int(name: str, default: int) -> int:
    v = os.getenv(name)
    if v is None:
        return default
    return int(v)


def _env_float(name: str, default: float) -> float:
    v = os.getenv(name)
    if v is None:
        return default
    return float(v)


def _env_str(name: str, default: str) -> str:
    v = os.getenv(name)
    return default if v is None else v


# class RagConfig(BaseModel):
#     use_chroma: bool = Field(default=True)
#     top_k: int = Field(default=5, ge=1, le=50)
#     max_distance: float = Field(default=1.0, ge=0.0)
#     default_model: str = Field(default="llama3.2:3b")
#     default_embed_model: str = Field(default="nomic-embed-text")
#     strict_unknown_reply: str = Field(default="I don't know based on the provided documents.")


class RagConfig(BaseModel):
    use_chroma: bool = Field(default=True)
    top_k: int = Field(default=5, ge=1, le=50)

    # ✅ OFF by default (None = no distance filtering)
    max_distance: float | None = Field(default=None, ge=0.0)

    default_model: str = Field(default="llama3.2:3b")
    default_embed_model: str = Field(default="nomic-embed-text")
    strict_unknown_reply: str = Field(default="I don't know based on the provided documents.")


class IngestConfig(BaseModel):
    chunk_size: int = Field(default=1200, ge=1)
    overlap: int = Field(default=200, ge=0)
    xlsx_max_cells: int = Field(default=2_000_000, ge=1)


class ChromaConfig(BaseModel):
    collection: str = Field(default="aistudio_chunks")
    query_include: list[str] = Field(
        default_factory=lambda: ["documents", "metadatas", "distances"]
    )


class OllamaConfig(BaseModel):
    base_url: str = Field(default="http://127.0.0.1:11434")
    request_timeout_s: float = Field(default=60.0, ge=1.0)


@dataclass(frozen=True)
class VectorstoreConfig:
    embed_batch_size: int = 32
    chroma_query_include: tuple[str, ...] = ("documents", "metadatas", "distances")


class AppConfig(BaseModel):
    # ✅ default_factory avoids "mutable default" error in pydantic v2
    rag: RagConfig = Field(default_factory=RagConfig)
    ingest: IngestConfig = Field(default_factory=IngestConfig)
    chroma: ChromaConfig = Field(default_factory=ChromaConfig)
    ollama: OllamaConfig = Field(default_factory=OllamaConfig)
    stats: dict[str, Any] = Field(default_factory=lambda: {})
    # Vector Store
    # vectorstore : str | None = Field(default=None)


def load_config_from_env() -> AppConfig:
    cfg = AppConfig()

    # RAG
    cfg.rag.use_chroma = _env_bool("AISTUDIO_USE_CHROMA", cfg.rag.use_chroma)
    cfg.rag.top_k = _env_int("AISTUDIO_TOP_K", cfg.rag.top_k)
    # cfg.rag.max_distance = _env_float("AISTUDIO_MAX_DISTANCE", cfg.rag.max_distance)

    v = os.getenv("AISTUDIO_MAX_DISTANCE")
    if v is not None and v.strip() != "":
        cfg.rag.max_distance = float(v)
    else:
        cfg.rag.max_distance = None

    cfg.rag.default_model = _env_str("AISTUDIO_DEFAULT_MODEL", cfg.rag.default_model)
    cfg.rag.default_embed_model = _env_str(
        "AISTUDIO_DEFAULT_EMBED_MODEL", cfg.rag.default_embed_model
    )

    # Ingest
    cfg.ingest.chunk_size = _env_int("AISTUDIO_INGEST_CHUNK_SIZE", cfg.ingest.chunk_size)
    cfg.ingest.overlap = _env_int("AISTUDIO_INGEST_OVERLAP", cfg.ingest.overlap)
    cfg.ingest.xlsx_max_cells = _env_int(
        "AISTUDIO_INGEST_XLSX_MAX_CELLS", cfg.ingest.xlsx_max_cells
    )

    # Chroma
    # (collection is typically per-corpus at runtime, but keep a default)
    cfg.chroma.collection = _env_str("AISTUDIO_CHROMA_COLLECTION", cfg.chroma.collection)

    # Ollama
    cfg.ollama.base_url = _env_str("AISTUDIO_OLLAMA_BASE_URL", cfg.ollama.base_url)
    cfg.ollama.request_timeout_s = _env_float(
        "AISTUDIO_OLLAMA_TIMEOUT_S", cfg.ollama.request_timeout_s
    )

    return cfg


# Global config instance
CONFIG = load_config_from_env()
