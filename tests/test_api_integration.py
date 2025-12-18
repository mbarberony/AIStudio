import pytest
from fastapi.testclient import TestClient

from local_llm_bot.app.api import app


@pytest.mark.integration
def test_health_integration() -> None:
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


@pytest.mark.integration
def test_ask_integration() -> None:
    client = TestClient(app)
    r = client.post("/ask", json={"query": "Tell me about AIStudio"})
    assert r.status_code == 200
    data = r.json()
    assert "answer" in data
    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 0
