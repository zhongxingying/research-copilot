# tests/test_chat.py
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_chat_validation_empty_message():
    r = client.post("/api/chat", json={"message": ""})
    assert r.status_code == 422


def test_chat_trace_id_header():
    r = client.post("/api/chat", json={"message": "hi"})
    assert "X-Trace-Id" in r.headers
