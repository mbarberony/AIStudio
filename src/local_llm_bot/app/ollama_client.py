# src/local_llm_bot/app/ollama_client.py
# Version: 1.3.0
# Changelog: 1.3.0 — AIStudio_941: ollama_generate accepts `timeout` (transport-level HTTP timeout),
#            defaults from CONFIG.ollama.request_timeout_s when None, applied via ollama.Client(timeout=…).
#            NOT a build_generate_kwargs option (it's httpx-level, not an Ollama generate option).
# Version: 1.2.0
# Changelog: 1.2.0 — AIStudio_958: build_generate_kwargs now defaults num_ctx from CONFIG.rag.num_ctx
#            (16384) when the caller passes None — so every generation path gets a window big enough
#            for the assembled prompt instead of Ollama's ~2-4k default. Lazy CONFIG import (no cycle).
# Version: 1.1.0
# Changelog: 1.1.0 — AIStudio_960/_958: extracted build_generate_kwargs() as the SINGLE source of
#            truth for the Ollama /api/generate payload. Both ollama_generate() and the new
#            /debug/prompt endpoint call it, so the debug view is the real bytes, not a
#            re-implementation. Added a num_ctx parameter (threaded into options; still None by
#            default — the _958 fix that SETS it from config lands separately). ollama_generate
#            behavior is unchanged (num_ctx omitted → Ollama applies its own default context).
from __future__ import annotations

from typing import Any


def build_generate_kwargs(
    *,
    model: str,
    prompt: str,
    system: str | None = None,
    temperature: float | None = None,
    num_ctx: int | None = None,
) -> dict[str, Any]:
    """Single source of truth for the Ollama /api/generate payload.

    Both ollama_generate() and /debug/prompt call this, so what you inspect in debug is exactly
    what gets sent to the model.

    NOTE (AIStudio_958): num_ctx defaults to None → 'num_ctx' is omitted from options → Ollama
    applies its OWN default context window (~2048 tokens), which silently truncates any prompt
    larger than that. Assembled RAG prompts here run ~6k tokens, so until a caller passes num_ctx
    the model never sees the full prompt.
    """
    kwargs: dict[str, Any] = {"model": model, "prompt": prompt}
    if system:
        kwargs["system"] = system
    options: dict[str, Any] = {}
    if temperature is not None:
        options["temperature"] = temperature
    # AIStudio_958: default the context window from config when the caller didn't specify one, so
    # every path (/ask, rag_core, bench, /debug/prompt) gets a window big enough for the assembled
    # prompt instead of Ollama's ~2-4k default. Import lazily to avoid any load-order coupling.
    if num_ctx is None:
        try:
            from local_llm_bot.app.config import CONFIG

            num_ctx = CONFIG.rag.num_ctx
        except Exception:
            num_ctx = None
    if num_ctx is not None:
        options["num_ctx"] = num_ctx
    if options:
        kwargs["options"] = options
    return kwargs


def ollama_generate(
    *,
    model: str,
    prompt: str,
    system: str | None = None,
    temperature: float | None = None,
    num_ctx: int | None = None,
    timeout: float | None = None,
) -> str:
    """Generate text using Ollama. Requires the Ollama server to be installed and running."""
    import ollama

    kwargs = build_generate_kwargs(
        model=model, prompt=prompt, system=system, temperature=temperature, num_ctx=num_ctx
    )
    # AIStudio_941: apply an HTTP request timeout. This is TRANSPORT-level (httpx client), NOT an
    # Ollama generate option — so it does NOT go through build_generate_kwargs. Default from config
    # so every path inherits it; a caller (per-request / per-corpus) may override. A too-small
    # timeout kills slow-model generations mid-flight, so the config default is generous (300s).
    if timeout is None:
        try:
            from local_llm_bot.app.config import CONFIG

            timeout = CONFIG.ollama.request_timeout_s
        except Exception:
            timeout = None
    if timeout is not None:
        resp = ollama.Client(timeout=timeout).generate(**kwargs)
    else:
        resp = ollama.generate(**kwargs)
    return str(resp.get("response", "")).strip()


def ollama_embed(*, model: str, texts: list[str]) -> list[list[float]]:
    """Compute embeddings using Ollama.

    Example embedding model:
      - nomic-embed-text
    """
    import ollama

    out: list[list[float]] = []
    for t in texts:
        r = ollama.embeddings(model=model, prompt=t)
        out.append(list(r["embedding"]))
    return out
