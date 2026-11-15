# Implement REST API endpoints
# current API imports a global incident_service. We need to remove that and use FastAPI dependency injection.
# Understand the dependency injection
# This is the most important new line: db: Session = Depends(get_db)
# It tells FastAPI:
# 1. Call get_db().
# 2. Create a database session.
# 3. Inject that session into the API dependency.
# 4. Create the repository and service.
# 5. Execute the API operation.
# 6. Close the session after the request completes.

from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

# Database session dependency.
from app.core.database import get_db

# Repository and service classes.
from app.repositories.incident_repository import IncidentRepository
from app.services.incident_service import IncidentService

# Pydantic request and response schemas.
from app.schemas.incident import (
    IncidentCreate,
    IncidentResponse,
    IncidentStatusUpdate,
)


router = APIRouter(
    prefix="/incidents",
    tags=["Incident Management"],
)


# Create a service instance for each API request.
def get_incident_service(
    db: Session = Depends(get_db),
) -> IncidentService:

    # Repository uses the database session for SQL operations.
    repository = IncidentRepository(db)

    # Service contains the incident business rules.
    return IncidentService(repository)


# Create a new incident.
@router.post(
    "/",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_incident(
    data: IncidentCreate,
    service: IncidentService = Depends(get_incident_service),
):
    return service.create_incident(data)


# Retrieve all incidents.
@router.get("/", response_model=list[IncidentResponse])
def list_incidents(
    service: IncidentService = Depends(get_incident_service),
):
    return service.list_incidents()


# Retrieve one incident by ID.
@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: UUID,
    service: IncidentService = Depends(get_incident_service),
):
    return service.get_incident(incident_id)


# Change an incident's status.
@router.patch(
    "/{incident_id}/status",
    response_model=IncidentResponse,
)
def update_incident_status(
    incident_id: UUID,
    data: IncidentStatusUpdate,
    service: IncidentService = Depends(get_incident_service),
):
    return service.update_status(
        incident_id,
        data.status,
    )
