
from fastapi import FastAPI

# Import the incident API router.
from app.api.v1.incidents import router as incident_router


app = FastAPI(
    title="EAII - Enterprise AI Incident Intelligence",
    description="Agentic AI platform for incident investigation",
    version="0.1.0",
)


# Existing health endpoint.
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "EAII",
        "version": "0.1.0",
    }


# Register incident APIs under version 1.
app.include_router(
    incident_router,
    prefix="/api/v1",
)
