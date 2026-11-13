
from fastapi.testclient import TestClient

# Import the FastAPI application we created.
from app.main import app

# TestClient allows us to test API endpoints without starting a server.
client = TestClient(app)

def test_health_check():
    # Send a GET request to the health endpoint.
    response = client.get("/health")

    # Verify that the API returns HTTP 200 (success).
    assert response.status_code == 200

    # Verify the response contains the expected application status.
    assert response.json()["status"] == "healthy"
    assert response.json()["application"] == "EAII"