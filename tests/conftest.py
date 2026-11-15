

import os
import pytest

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
from app.main import app
from app.models.incident import Incident  # Register the Incident model

load_dotenv()

# Safety check: tests must never connect to the main database.
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL or "eaiirp_test_db" not in TEST_DATABASE_URL:
    raise RuntimeError("TEST_DATABASE_URL must point to eaiirp_test_db")

test_engine = create_engine(TEST_DATABASE_URL)


@pytest.fixture
def client():
    # Ensure test tables exist.
    Base.metadata.create_all(bind=test_engine)

    # Start a transaction that will be rolled back after each test.
    connection = test_engine.connect()
    transaction = connection.begin()

    TestingSessionLocal = sessionmaker(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    db = TestingSessionLocal()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        db.close()
        transaction.rollback()
        connection.close()
