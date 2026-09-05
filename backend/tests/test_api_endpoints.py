"""Integration tests for AI Finance Controller API endpoints."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_transaction_ingest_pipeline():
    payload = {
        "raw_merchant": "AMAZON.IN 18499.00 CARD 4532 1111 2222 9988",
        "amount": 18499.0,
        "category": "Electronics"
    }
    response = client.post("/api/v1/transactions/ingest", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "****-****-****-9988" in data["transaction"]["clean_merchant"]
    assert "4532" not in data["transaction"]["clean_merchant"]
    assert data["is_anomaly"] is True
    assert "evidence_payload" in data


def test_copilot_simulate():
    payload = {
        "amount": 20000.0,
        "category": "Electronics"
    }
    response = client.post("/api/v1/copilot/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "feasible" in data
    assert "projected_end_of_month_balance" in data


def test_copilot_chat():
    payload = {
        "query": "Why was my last transaction flagged?"
    }
    response = client.post("/api/v1/copilot/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "evidence_citation" in data


def test_list_audit_logs():
    response = client.get("/api/v1/audit/logs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
