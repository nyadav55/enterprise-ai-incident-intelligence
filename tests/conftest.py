

import os
import pytest

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
from app.core.security import hash_password
from app.main import app
from app.models.incident import Incident
from app.models.user import User, UserRole

load_dotenv()

# Safety check: tests must never connect to the main database.
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL or "eaiirp_test_db" not in TEST_DATABASE_URL:
    raise RuntimeError("TEST_DATABASE_URL must point to eaiirp_test_db")

test_engine = create_engine(TEST_DATABASE_URL)


@pytest.fixture
def db():
    # Ensure all registered test tables exist.
    Base.metadata.create_all(bind=test_engine)

    # Open a connection and start an outer transaction.
    connection = test_engine.connect()
    transaction = connection.begin()

    TestingSessionLocal = sessionmaker(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        # Close the session and roll back all test data.
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db):
    # Override FastAPI's database dependency with our test session.
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def authenticated_client(client):
    # Register a normal Operations Engineer account.
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "engineer@test.com",
            "password": "TestPassword@123",
        },
    )

    assert register_response.status_code == 201, register_response.text

    # Log in to obtain a JWT access token.
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "engineer@test.com",
            "password": "TestPassword@123",
        },
    )

    assert login_response.status_code == 200, login_response.text

    token = login_response.json()["access_token"]

    # Attach the token to subsequent protected API requests.
    client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return client


# Why this design is useful in production testing:
# - authenticated_client represents a normal Operations Engineer.
# - admin_client represents an Administrator.
# - Both use the same isolated test database mechanism.
# - Production authorization rules remain unchanged.
# - Test data is rolled back after each test.

@pytest.fixture
def admin_client(client, db):
    # Create an administrator directly in the test database.
    # Public registration must not allow self-assignment of admin roles.
    admin = User(
        email="admin@test.com",
        password_hash=hash_password("AdminPassword@123"),
        role=UserRole.ADMIN,
        is_active=True,
    )

    db.add(admin)
    db.commit()

    # Authenticate the administrator through the real login endpoint.
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@test.com",
            "password": "AdminPassword@123",
        },
    )

    assert login_response.status_code == 200, login_response.text

    token = login_response.json()["access_token"]

    # Attach the administrator's JWT to protected requests.
    client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return client
