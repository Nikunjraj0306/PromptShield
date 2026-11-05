
import pytest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.auth_dependencies import get_current_user


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


def enable_admin_access():
    app.dependency_overrides[get_current_user] = lambda: {
        "user_id": 1,
        "role": "Admin",
    }


def enable_viewer_access():
    app.dependency_overrides[get_current_user] = lambda: {
        "user_id": 2,
        "role": "Viewer",
    }


# HEALTH TESTS

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200


def test_readiness_endpoint_returns_database_status():
    with patch(
        "app.main.check_database_connection",
        return_value=True,
    ):
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"
    assert response.json()["database"] == "connected"


# AUTHENTICATION TESTS

def test_login_returns_access_token():
    expected = {
        "access_token": "test-access-token",
        "token_type": "bearer",
        "expires_in": 1800,
    }

    with patch(
        "app.main.authenticate_user",
        return_value=expected,
    ):
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "admin@example.com",
                "password": "TestPassword123!",
            },
        )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["expires_in"] == 1800
    assert response.json()["access_token"] == "test-access-token"


def test_login_rejects_invalid_credentials():
    with patch(
        "app.main.authenticate_user",
        return_value=None,
    ):
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "wrong@example.com",
                "password": "WrongPassword123!",
            },
        )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


# AUTHORIZATION TESTS

def test_analytics_rejects_unauthorized_request():
    response = client.get("/api/v1/analytics/summary")
    assert response.status_code == 401


def test_events_rejects_unauthorized_request():
    response = client.get("/api/v1/events")
    assert response.status_code == 401


def test_inspect_rejects_unauthorized_request():
    response = client.post(
        "/api/v1/inspect",
        json={
            "application_id": 1,
            "endpoint_id": 1,
            "text": "normal request",
        },
    )

    assert response.status_code == 401


def test_viewer_cannot_inspect_requests():
    enable_viewer_access()

    response = client.post(
        "/api/v1/inspect",
        json={
            "application_id": 1,
            "endpoint_id": 1,
            "text": "normal request",
        },
    )

    assert response.status_code == 403


# INSPECTION TESTS

def test_inspect_rejects_invalid_application_id():
    enable_admin_access()

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
    enable_admin_access()

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
    enable_admin_access()

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


# SECURITY EVENTS TESTS

def test_events_endpoint_returns_events():
    enable_admin_access()

    sample_events = [
        {
            "event_id": 7,
            "application_id": 1,
            "application_name": "PromptShield Demo App",
            "endpoint_id": 1,
            "endpoint_path": "/demo/inspect",
            "endpoint_method": "POST",
            "request_time": "2026-10-29T10:00:00",
            "risk_score": 35,
            "decision": "Allow",
            "reason_code": "NO_BLOCKING_RULE_MATCHED",
            "correlation_id": "test-correlation-id",
            "request_path": "/api/v1/inspect",
            "processing_status": "Completed",
            "findings": [
                {
                    "rule_name": "SQL Injection Pattern",
                    "category": "SQL_INJECTION",
                    "severity": "High",
                    "weight": 35,
                    "is_critical": False,
                    "confidence": None,
                    "evidence_summary": "Matched heuristic rule",
                }
            ],
        }
    ]

    with patch("app.main.get_recent_events", return_value=sample_events):
        response = client.get("/api/v1/events?limit=50")

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 1
    assert body["events"][0]["findings"][0]["confidence"] is None


def test_events_endpoint_rejects_invalid_limit():
    enable_admin_access()

    response = client.get("/api/v1/events?limit=101")
    assert response.status_code == 400


def test_events_endpoint_hides_internal_errors():
    enable_admin_access()

    with patch(
        "app.main.get_recent_events",
        side_effect=RuntimeError("internal SQL details"),
    ):
        response = client.get("/api/v1/events?limit=50")

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Security events are temporarily unavailable"
    )
    assert "internal SQL details" not in response.text


# ANALYTICS TESTS

def test_analytics_summary_returns_metrics():
    enable_admin_access()

    expected = {
        "total_events": 7,
        "blocked_events": 1,
        "allowed_events": 6,
        "average_risk": 23.57,
    }

    with patch(
        "app.main.get_security_summary",
        return_value=expected,
    ):
        response = client.get("/api/v1/analytics/summary")

    assert response.status_code == 200
    body = response.json()
    assert body["total_events"] == 7
    assert body["blocked_events"] == 1
    assert body["allowed_events"] == 6


def test_analytics_summary_hides_internal_errors():
    enable_admin_access()

    with patch(
        "app.main.get_security_summary",
        side_effect=RuntimeError("internal SQL details"),
    ):
        response = client.get("/api/v1/analytics/summary")

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Analytics service temporarily unavailable"
    )
    assert "internal SQL details" not in response.text
