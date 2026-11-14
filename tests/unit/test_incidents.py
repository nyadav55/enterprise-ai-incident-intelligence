# Create automated tests

from fastapi.testclient import TestClient

from app.main import app


# TestClient calls our API without starting Uvicorn.
client = TestClient(app)


def test_create_incident():
    response = client.post(
        "/api/v1/incidents/",
        json={
            "title": "Payment service unavailable",
            "description": "Payment API is returning HTTP 500 errors.",
            "severity": "CRITICAL",
            "source": "monitoring",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Payment service unavailable"
    assert data["severity"] == "CRITICAL"
    assert data["status"] == "NEW"


def test_reject_invalid_incident():
    response = client.post(
        "/api/v1/incidents/",
        json={
            "title": "Bad",
            "description": "Short",
            "severity": "UNKNOWN",
        },
    )

    # Invalid input should return HTTP 422.
    assert response.status_code == 422


def test_incident_status_update():
    # First create an incident.
    created = client.post(
        "/api/v1/incidents/",
        json={
            "title": "Database connection failure",
            "description": "Application cannot connect to the database.",
            "severity": "HIGH",
            "source": "manual",
        },
    )

    incident_id = created.json()["id"]

    # Change NEW to INVESTIGATING.
    updated = client.patch(
        f"/api/v1/incidents/{incident_id}/status",
        json={"status": "INVESTIGATING"},
    )

    assert updated.status_code == 200
    assert updated.json()["status"] == "INVESTIGATING"


def test_reject_invalid_status_transition():
    created = client.post(
        "/api/v1/incidents/",
        json={
            "title": "Network connectivity issue",
            "description": "Service cannot reach the upstream endpoint.",
            "severity": "MEDIUM",
            "source": "manual",
        },
    )

    incident_id = created.json()["id"]

    # NEW cannot move directly to RESOLVED.
    response = client.patch(
        f"/api/v1/incidents/{incident_id}/status",
        json={"status": "RESOLVED"},
    )

    assert response.status_code == 400
