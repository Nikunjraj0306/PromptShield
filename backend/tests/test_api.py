from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200


def test_inspect_rejects_invalid_application_id():
    response = client.post(
        "/api/v1/inspect",
        json={
            "application_id": -1,
            "endpoint_id": 1,
            "text": "normal test",
        },
    )
    assert response.status_code == 422


def test_inspect_returns_allow_for_clean_text():
    expected = {
        "correlation_id": "test-correlation-id",
        "risk_score": 0,
        "decision": "Allow",
        "reason_code": "NO_BLOCKING_RULE_MATCHED",
        "findings": [],
    }

    with patch("app.main.inspect_and_store", return_value=expected):
        response = client.post(
            "/api/v1/inspect",
            json={
                "application_id": 1,
                "endpoint_id": 1,
                "text": "Hello, normal request.",
            },
        )

    assert response.status_code == 200
    assert response.json()["decision"] == "Allow"
    assert response.json()["risk_score"] == 0


def test_inspect_returns_block_for_critical_finding():
    expected = {
        "correlation_id": "test-correlation-id",
        "risk_score": 60,
        "decision": "Block",
        "reason_code": "CRITICAL_FINDING",
        "findings": [
            {
                "rule_name": "Command Injection Pattern",
                "category": "COMMAND_INJECTION",
                "severity": "Critical",
                "weight": 60,
                "is_critical": True,
                "evidence_summary": "Matched heuristic rule",
            }
        ],
    }

    with patch("app.main.inspect_and_store", return_value=expected):
        response = client.post(
            "/api/v1/inspect",
            json={
                "application_id": 1,
                "endpoint_id": 1,
                "text": "test; whoami",
            },
        )

    assert response.status_code == 200
    assert response.json()["decision"] == "Block"
    assert response.json()["reason_code"] == "CRITICAL_FINDING"
