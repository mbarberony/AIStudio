"""Pytest configuration for AIStudio.

Integration tests (``@pytest.mark.integration``) exercise the live local stack:
Qdrant (vector store), Ollama (embeddings/generation), and the FastAPI app.
On a hosted CI runner none of those services exist, so the integration step
would otherwise error out with connection failures.

This hook turns that into a clean *skip*: if any required service is
unreachable at collection time, every integration-marked test is skipped with a
reason naming the missing service(s). Locally — with the stack up via
``ais_start`` — the services answer and the tests run normally. Unit-test
behavior is unchanged (no marker, no probe).

Service host/port can be overridden via environment variables for non-default
setups; otherwise localhost defaults are used.
"""
from __future__ import annotations

import os
import socket

import pytest

# name -> (host_env, port_env, host_default, port_default)
_INTEGRATION_SERVICES: dict[str, tuple[str, str, str, int]] = {
    "Qdrant": ("AISTUDIO_QDRANT_HOST", "AISTUDIO_QDRANT_PORT", "127.0.0.1", 6333),
    "Ollama": ("AISTUDIO_OLLAMA_HOST", "AISTUDIO_OLLAMA_PORT", "127.0.0.1", 11434),
    "API": ("AISTUDIO_API_HOST", "AISTUDIO_API_PORT", "127.0.0.1", 8000),
}
_PROBE_TIMEOUT_S = 0.5


def _reachable(host: str, port: int) -> bool:
    """True if a TCP connection to host:port succeeds within the probe timeout."""
    try:
        with socket.create_connection((host, port), timeout=_PROBE_TIMEOUT_S):
            return True
    except OSError:
        return False


def _missing_services() -> list[str]:
    """Return 'Name (host:port)' for each unreachable integration service."""
    missing: list[str] = []
    for name, (host_env, port_env, host_def, port_def) in _INTEGRATION_SERVICES.items():
        host = os.environ.get(host_env, host_def)
        port = int(os.environ.get(port_env, port_def))
        if not _reachable(host, port):
            missing.append(f"{name} ({host}:{port})")
    return missing


def pytest_collection_modifyitems(items):
    """Skip integration tests when the live stack isn't fully reachable."""
    integration = [it for it in items if it.get_closest_marker("integration")]
    if not integration:
        return  # nothing to guard — don't pay the probe cost
    missing = _missing_services()
    if not missing:
        return  # full stack up — run them
    reason = "integration stack unavailable — not reachable: " + ", ".join(missing)
    skip = pytest.mark.skip(reason=reason)
    for item in integration:
        item.add_marker(skip)
