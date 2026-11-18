


import pytest


def test_user_registration(client):
    """Verify that a new user can register successfully."""

    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@test.com",
            "password": "TestPassword@123",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "newuser@test.com"

    # Public registration must assign the least-privileged role.
    assert response.json()["role"] == "OPERATIONS_ENGINEER"


def test_duplicate_email_registration(client):
    """Verify that duplicate email registration is rejected."""

    user_data = {
        "email": "duplicate@test.com",
        "password": "TestPassword@123",
    }

    # First registration should succeed.
    first_response = client.post(
        "/api/v1/auth/register",
        json=user_data,
    )

    assert first_response.status_code == 201

    # Second registration with the same email should fail.
    second_response = client.post(
        "/api/v1/auth/register",
        json=user_data,
    )

    # 409 Conflict means the email already exists.
    assert second_response.status_code == 409


def test_successful_login(client):
    """Verify that valid credentials generate a JWT."""

    # Create a user first.
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@test.com",
            "password": "TestPassword@123",
        },
    )

    # Authenticate with valid credentials.
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "login@test.com",
            "password": "TestPassword@123",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_invalid_password_login(client):
    """Verify that an incorrect password is rejected."""

    # Register a valid user.
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "wrongpass@test.com",
            "password": "TestPassword@123",
        },
    )

    # Attempt login using an incorrect password.
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "wrongpass@test.com",
            "password": "WrongPassword@123",
        },
    )

    assert response.status_code == 401


def test_unauthenticated_user_cannot_access_profile(client):
    """Verify that /me requires authentication."""

    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_unauthenticated_user_cannot_access_incidents(client):
    """Verify that incident APIs require authentication."""

    response = client.get("/api/v1/incidents/")

    assert response.status_code == 401


def test_operations_engineer_cannot_update_incident_status(
    authenticated_client,
):
    """Verify that Operations Engineer cannot perform admin actions."""

    # Create an incident using the authenticated engineer.
    create_response = authenticated_client.post(
        "/api/v1/incidents/",
        json={
            "title": "Authentication test incident",
            "description": "Testing role-based access control.",
            "severity": "HIGH",
            "source": "automated-test",
        },
    )

    assert create_response.status_code == 201

    incident_id = create_response.json()["id"]

    # Attempt a privileged status update.
    update_response = authenticated_client.patch(
        f"/api/v1/incidents/{incident_id}/status",
        json={"status": "INVESTIGATING"},
    )

    # 403 confirms authentication succeeded but authorization failed.
    assert update_response.status_code == 403
