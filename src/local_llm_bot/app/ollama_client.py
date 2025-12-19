import json
import urllib.request
from typing import Any

OLLAMA_BASE_URL = "http://127.0.0.1:11434"


def ollama_generate(model: str, prompt: str, system: str | None = None) -> str:
    payload: dict[str, Any] = {"model": model, "prompt": prompt, "stream": False}
    if system:
        payload["system"] = system

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_BASE_URL}/api/generate",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        out = json.loads(resp.read().decode("utf-8"))

    return out.get("response", "").strip()
