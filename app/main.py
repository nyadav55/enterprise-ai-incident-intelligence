
from email.base64mime import header_length
from fastapi import FastAPI

# Create the main FastAPI application.
# This is the entry point for our backend APIs.
app = FastAPI(
    title="EAII - Enterprise AI Incident Intelligence",
    description="Agentic AI platform for incident investigation",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    """
    Check whether the backend application is running.
    This endpoint will later support monitoring and Kubernetes probes.
    """
    return{
        "status": "healthy",
        "application": "EAII",
        "version": "0.1.0"
    }