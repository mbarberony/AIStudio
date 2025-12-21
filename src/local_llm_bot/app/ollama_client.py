from __future__ import annotations

from typing import Any


def ollama_generate(*, model: str, prompt: str, system: str | None = None) -> str:
    """
    Generate text using Ollama.
    Requires the Ollama server to be installed and running.
    """
    import ollama

    kwargs: dict[str, Any] = {"model": model, "prompt": prompt}
    if system:
        kwargs["system"] = system

    resp = ollama.generate(**kwargs)
    return str(resp.get("response", "")).strip()


def ollama_embed(*, model: str, texts: list[str]) -> list[list[float]]:
    """
    Compute embeddings using Ollama.

    Example embedding model:
      - nomic-embed-text
    """
    import ollama

    out: list[list[float]] = []
    for t in texts:
        r = ollama.embeddings(model=model, prompt=t)
        out.append(list(r["embedding"]))
    return out
