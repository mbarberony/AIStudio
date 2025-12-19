import json
import urllib.request

import pytest
from fastapi.testclient import TestClient

from local_llm_bot.app.api import app


def _ollama_can_generate(model: str) -> bool:
    try:
        payload = json.dumps({"model": model, "prompt": "ping", "stream": False}).encode("utf-8")
        req = urllib.request.Request(
            "http://127.0.0.1:11434/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return bool(data.get("response", "").strip())
    except Exception:
        return False


def _ollama_ready() -> bool:
    # Fast check: is the Ollama HTTP server reachable?
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434", timeout=1) as _:
            pass
        return True
    except Exception:
        return False


def _ollama_has_model(model: str) -> bool:
    # Check if a specific model is available (pulled) in Ollama
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:11434/api/tags",
            headers={"Content-Type": "application/json"},
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=2) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        names = {m.get("name") for m in data.get("models", [])}
        return model in names
    except Exception:
        return False


@pytest.mark.integration
def test_health_integration() -> None:
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


@pytest.mark.integration
def test_ask_integration() -> None:
    # Skip if Ollama isn't available locally (so CI/other machines don't fail)
    if not _ollama_ready():
        pytest.skip("Ollama is not running on http://127.0.0.1:11434")

    # If you wire a default model (recommended), validate it's present.
    # Keep this string aligned with your rag_core DEFAULT_MODEL.
    model = "llama3.2:3b"

    if not _ollama_can_generate(model):
        pytest.skip(f"Ollama not ready to generate with model: {model}")

    if not _ollama_has_model(model):
        pytest.skip(f"Ollama model not available: {model}. Run: ollama pull {model}")

    client = TestClient(app)
    r = client.post("/ask", json={"query": "Tell me about AIStudio"})
    assert r.status_code == 200
    data = r.json()
    assert "answer" in data
    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 0
