import pytest
from fastapi.testclient import TestClient

from local_llm_bot.app.api import app


@pytest.mark.unit
def test_health_ok() -> None:
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
