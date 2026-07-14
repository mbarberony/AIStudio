# src/local_llm_bot/app/config.py
# Version: 1.7.0
# Changelog: 1.7.0 — AIStudio_1020: ModelFitConfig — the memory-fit guard's four calibration
#   constants (reserve_bytes, footprint_mult, warn_frac, block_frac), env-overridable
#   (AISTUDIO_FIT_*). Consumed by app/model_fit.py, wired into the /ask preflight + /models `fit`
#   field + bench --fit-policy. Values are PROVISIONAL pending 24GB-tier ESEF calibration
#   (NOTES - AIStudio - Model-Size Guard Re-Scope and Design - 2026-07-12 §3): whether 12b-on-ESEF
#   runs clean on 24GB sets warn_frac/block_frac. Code is stable; only these four numbers move.
# Version: 1.6.0
# Changelog: 1.6.0 — AIStudio_941: ollama.request_timeout_s default 60→300 and now actually APPLIED
#   (ollama_client v1.3.0). Was a dormant field; a bigger _958 window pushed heavy questions past the
#   old wall. 300s covers slow local models; overridable per-request (AskRequest.timeout) / per-corpus
#   (default_timeout). Env AISTUDIO_OLLAMA_TIMEOUT_S.
# Version: 1.5.0
# Changelog: 1.5.0 — AIStudio_958: num_ctx (context window) — new RagConfig field (default 16384,
#   env AISTUDIO_NUM_CTX). Previously unset → Ollama's own ~2-4k default silently truncated the
#   ~6-14k-token RAG prompts. Defaulted at the single source of truth (ollama_client.build_generate_kwargs)
#   so all generation paths inherit it. Fixes the low-RAM + long-follow-up truncation.
# Version: 1.4.0
# Changelog: 1.4.0 — AIStudio_956: full_prompt_min_b — tier boundary for system-prompt selection.
#   New RagConfig field (default 20; env AISTUDIO_FULL_PROMPT_MIN_B). Models with >= N billion
#   params get the full prompts/system.txt; smaller models get the slim prompts/system_small_model.txt
#   (the ~1,944-tok full prompt dilutes instruction-following under a ~6,300-tok context and small /
#   low-RAM models drop [N] citations — Suzanne 24GB 0/0/0, Beast 128GB unaffected). Read by
#   api.py::_is_small_model(). Doubles as the A/B lever: 0 = always full, 999 = always slim.
#   llama3.1:8b -> slim; gemma3:27b / llama3.1:70b -> full.
# Version: 1.3.0
# Changelog: 1.3.0 — AIStudio_945: default_model gemma3:4b → llama3.1:8b ("the good llama" — clean
#   [N] citations; the seven-model sweep showed gemma3:4b drops citations + fabricates entity
#   attribution). ⚠ REQUIRES the install canon to pull llama3.1:8b (cold-install guard — see the
#   field note below; this reverts the AIStudio_888 gemma pin and re-takes on that dependency).
# Changelog: 1.2.0 — AIStudio_888: default_model llama3.1:8b → gemma3:4b (canon). See note at the field.
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


class RagConfig(BaseModel):
    use_chroma: bool = Field(default=False)  # Legacy — use vectorstore instead
    vectorstore: str = Field(default="qdrant")  # "qdrant" or "chroma"
    top_k: int = Field(default=5, ge=1, le=50)

    # ✅ OFF by default (None = no distance filtering)
    max_distance: float | None = Field(default=None, ge=0.0)

    # default_model: str = Field(default="llama3.2:3b")
    # AIStudio_945 (2026-06-30): canon default → llama3.1:8b ("the good llama"). The seven-model
    # citation sweep showed gemma3:4b drops [N] citations and fabricates entity attribution; the 8B
    # llama cites cleanly and is the recommended small/fast default (gemma3:27b for heavy work).
    # ⚠ COLD-INSTALL DEPENDENCY (do not lose): a fresh clone 500s on its FIRST /ask if the install
    # canon does not PULL this model — that is the AIStudio_888 Nuclear-Test-Pass-2 blocker that drove
    # the earlier gemma3:4b pin. The install canon (install.sh + QUICKSTART) MUST pull llama3.1:8b in
    # lockstep with this default. Safe on any machine that already has llama3.1:8b (e.g. Beast).
    default_model: str = Field(default="llama3.1:8b")

    default_embed_model: str = Field(default="nomic-embed-text")
    strict_unknown_reply: str = Field(default="I don't know based on the provided documents.")

    # Hybrid retrieval weight (vector + BM25). None = vector-only (v1.4.0 behavior preserved).
    # 1.0 = vector dominant, 0.0 = BM25 dominant, 0.5 = equal weight.
    # See scoring.combine_hybrid() and CONCEPT - AIStudio - Hybrid Retrieval Design.
    hybrid_alpha: float | None = Field(default=None, ge=0.0, le=1.0)

    # AIStudio_956 — tier boundary for system-prompt selection. A model whose param size (in
    # billions, parsed from its tag) is >= this gets the full prompts/system.txt; a smaller model
    # gets the slim prompts/system_small_model.txt. The slim prompt keeps [N] citations reliable on
    # small / low-RAM models, where the full ~1,944-tok prompt competes with the ~6,300-tok
    # retrieval context and instruction-following degrades. Env AISTUDIO_FULL_PROMPT_MIN_B overrides
    # and doubles as the A/B lever: 0 = always full, 999 = always slim. Read by api.py::_is_small_model().
    full_prompt_min_b: int = Field(default=20, ge=0)

    # AIStudio_958 — context window (Ollama num_ctx). Unset, Ollama applies its own default
    # (~2048-4096), silently truncating the ~6-14k-token RAG prompts assembled here. Setting it
    # explicitly gives deterministic headroom across machines (fixes the low-RAM truncation and the
    # long-follow-up truncation). Threaded via ollama_client.build_generate_kwargs so EVERY
    # generation path (/ask, rag_core, bench, /debug/prompt, warmup) inherits it. Env AISTUDIO_NUM_CTX.
    num_ctx: int = Field(default=16384, ge=512)


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
    request_timeout_s: float = Field(default=300.0, ge=1.0)  # AIStudio_941: Ollama HTTP request timeout, now APPLIED in ollama_client. 300s covers slow local models (gemma3:27b ~110s, 70b ~166s); overridable per-request / per-corpus. Env AISTUDIO_OLLAMA_TIMEOUT_S.


class ModelFitConfig(BaseModel):
    # AIStudio_1020 — memory-fit guard. The guard estimates a model's RUNTIME footprint and compares
    # it to post-reserve available RAM, returning FIT / WARN / BLOCK + a recommended tier. These four
    # constants are the ONLY thing that moves between machine classes or after calibration; the policy
    # code (app/model_fit.py) is fixed. PROVISIONAL — finalize from the 24GB-tier ESEF runs.
    #   • reserve_bytes  — headroom held back from psutil.available (OS + other apps); NOT the nameplate.
    #   • footprint_mult — disk→runtime scalar (weights + KV cache + overhead) over Ollama's on-disk size.
    #   • warn_frac      — FIT→WARN band edge (footprint/available).
    #   • block_frac     — WARN→BLOCK band edge; must land 27b-on-24GB firmly in BLOCK (the confirmed wedge).
    # Env: AISTUDIO_FIT_RESERVE_BYTES / _FOOTPRINT_MULT / _WARN_FRAC / _BLOCK_FRAC.
    reserve_bytes: int = Field(default=3_000_000_000, ge=0)
    footprint_mult: float = Field(default=1.2, ge=1.0)
    warn_frac: float = Field(default=0.80, ge=0.0, le=2.0)
    block_frac: float = Field(default=0.92, ge=0.0, le=2.0)


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
    fit: ModelFitConfig = Field(default_factory=ModelFitConfig)  # AIStudio_1020
    stats: dict[str, Any] = Field(default_factory=lambda: {})
    # Vector Store
    # vectorstore : str | None = Field(default=None)


def load_config_from_env() -> AppConfig:
    cfg = AppConfig()

    # RAG
    cfg.rag.use_chroma = _env_bool("AISTUDIO_USE_CHROMA", cfg.rag.use_chroma)
    _vs = os.getenv("AISTUDIO_VECTORSTORE", cfg.rag.vectorstore).lower()
    cfg.rag.vectorstore = _vs
    # Keep use_chroma in sync for legacy code
    cfg.rag.use_chroma = (_vs == "chroma")
    cfg.rag.top_k = _env_int("AISTUDIO_TOP_K", cfg.rag.top_k)
    # cfg.rag.max_distance = _env_float("AISTUDIO_MAX_DISTANCE", cfg.rag.max_distance)

    v = os.getenv("AISTUDIO_MAX_DISTANCE")
    if v is not None and v.strip() != "":
        cfg.rag.max_distance = float(v)
    else:
        cfg.rag.max_distance = None

    # Hybrid retrieval alpha — same null-semantics pattern as max_distance.
    # Empty string or unset = None (vector-only retrieval, preserves v1.4.0 behavior).
    # Value in [0.0, 1.0] = hybrid mode active with that weight.
    v = os.getenv("AISTUDIO_HYBRID_ALPHA")
    if v is not None and v.strip() != "":
        cfg.rag.hybrid_alpha = float(v)
    else:
        cfg.rag.hybrid_alpha = None

    cfg.rag.default_model = _env_str("AISTUDIO_DEFAULT_MODEL", cfg.rag.default_model)
    cfg.rag.default_embed_model = _env_str(
        "AISTUDIO_DEFAULT_EMBED_MODEL", cfg.rag.default_embed_model
    )
    cfg.rag.full_prompt_min_b = _env_int(
        "AISTUDIO_FULL_PROMPT_MIN_B", cfg.rag.full_prompt_min_b
    )
    cfg.rag.num_ctx = _env_int("AISTUDIO_NUM_CTX", cfg.rag.num_ctx)

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

    # Model-fit guard (AIStudio_1020)
    cfg.fit.reserve_bytes = _env_int("AISTUDIO_FIT_RESERVE_BYTES", cfg.fit.reserve_bytes)
    cfg.fit.footprint_mult = _env_float("AISTUDIO_FIT_FOOTPRINT_MULT", cfg.fit.footprint_mult)
    cfg.fit.warn_frac = _env_float("AISTUDIO_FIT_WARN_FRAC", cfg.fit.warn_frac)
    cfg.fit.block_frac = _env_float("AISTUDIO_FIT_BLOCK_FRAC", cfg.fit.block_frac)

    return cfg


# Global config instance
CONFIG = load_config_from_env()
