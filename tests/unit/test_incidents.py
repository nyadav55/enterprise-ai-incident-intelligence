# Create automated tests

# from fastapi.testauthenticated_client import Testauthenticated_client

# from app.main import app


# # Testauthenticated_client calls our API without starting Uvicorn.
# authenticated_client = Testauthenticated_client(app)


def test_create_incident(authenticated_client):
    response = authenticated_client.post(
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


def test_reject_invalid_incident(authenticated_client):
    response = authenticated_client.post(
        "/api/v1/incidents/",
        json={
            "title": "Bad",
            "description": "Short",
            "severity": "UNKNOWN",
        },
    )

    # Invalid input should return HTTP 422.
    assert response.status_code == 422


def test_incident_status_update(admin_client):
    # First create an incident.
    created = admin_client.post(
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
    updated = admin_client.patch(
        f"/api/v1/incidents/{incident_id}/status",
        json={"status": "INVESTIGATING"},
    )

    assert updated.status_code == 200
    assert updated.json()["status"] == "INVESTIGATING"


def test_reject_invalid_status_transition(admin_client):
    created = admin_client.post(
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
    response = admin_client.patch(
        f"/api/v1/incidents/{incident_id}/status",
        json={"status": "RESOLVED"},
    )

    assert response.status_code == 400

def test_incident_pagination(authenticated_client):
    # Create three incidents for pagination testing.
    for i in range(3):
        authenticated_client.post(
            "/api/v1/incidents/",
            json={
                "title": f"Pagination test {i}",
                "description": "Testing incident pagination.",
                "severity": "LOW",
                "source": "manual",
            },
        )

    # Request only two records.
    response = authenticated_client.get("/api/v1/incidents/?skip=0&limit=2")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_incident_severity_filter(authenticated_client):
    # Create a CRITICAL incident.
    authenticated_client.post(
        "/api/v1/incidents/",
        json={
            "title": "Oracle database failure",
            "description": "Database is unavailable.",
            "severity": "CRITICAL",
            "source": "monitoring",
        },
    )

    # Retrieve only CRITICAL incidents.
    response = authenticated_client.get("/api/v1/incidents/?severity=CRITICAL")

    assert response.status_code == 200
    assert all(item["severity"] == "CRITICAL" for item in response.json())


def test_incident_status_filter(authenticated_client):
    # Create an incident.
    created = authenticated_client.post(
        "/api/v1/incidents/",
        json={
            "title": "API failure",
            "description": "API is unavailable.",
            "severity": "HIGH",
            "source": "monitoring",
        },
    )

    incident_id = created.json()["id"]

    # Move it to INVESTIGATING.
    authenticated_client.patch(
        f"/api/v1/incidents/{incident_id}/status",
        json={"status": "INVESTIGATING"},
    )

    # Filter by status.
    response = authenticated_client.get("/api/v1/incidents/?status=INVESTIGATING")

    assert response.status_code == 200
    assert all(item["status"] == "INVESTIGATING" for item in response.json())


def test_incident_title_search(authenticated_client):
    # Create an incident with a searchable title.
    authenticated_client.post(
        "/api/v1/incidents/",
        json={
            "title": "Oracle database outage",
            "description": "Database connection failure.",
            "severity": "HIGH",
            "source": "monitoring",
        },
    )

    # Search by part of the title.
    response = authenticated_client.get("/api/v1/incidents/?search=Oracle")

    assert response.status_code == 200
    assert all("Oracle" in item["title"] for item in response.json())    
