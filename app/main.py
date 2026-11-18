
from fastapi import FastAPI

# Import the incident API router.
from app.api.v1.incidents import router as incident_router
from app.core.logging_config import logging
from app.core.middleware import request_logging_middleware
from app.api.v1.auth import router as auth_router

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

# Add the logging configuration import and logger.
logger = logging.getLogger("eaiirp")
logger.info("EAII application started")

# Register middleware
app.middleware("http")(request_logging_middleware)

# Register the router
app.include_router(auth_router, prefix="/api/v1")