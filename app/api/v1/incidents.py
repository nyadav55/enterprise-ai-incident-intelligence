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

from fastapi import APIRouter, Depends, status, Query
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
    IncidentSeverity, IncidentStatus
)

from app.core.dependencies import get_current_user, require_roles
from app.models.user import User, UserRole

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
    current_user: User = Depends(get_current_user),
):
    return service.create_incident(data)


# Retrieve all incidents.
# Retrieve incidents with pagination, filtering and search.
@router.get("/", response_model=list[IncidentResponse])
def list_incidents(
    skip: int = Query(0, ge=0),  # Cannot skip a negative number of records.
    limit: int = Query(10, ge=1, le=100),  # Restrict page size to 1–100.
    severity: IncidentSeverity | None = None,
    incident_status: IncidentStatus | None = Query(None, alias="status"),
    search: str | None = Query(None, min_length=2, max_length=100),
    service: IncidentService = Depends(get_incident_service),
    current_user: User = Depends(get_current_user),
):
    return service.list_incidents(
        skip=skip,
        limit=limit,
        severity=severity,
        status=incident_status,
        search=search,
    )


# Retrieve one incident by ID.
@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: UUID,
    service: IncidentService = Depends(get_incident_service),
    current_user: User = Depends(get_current_user),
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
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.INCIDENT_MANAGER,
        )
    ),
):
    return service.update_status(
        incident_id,
        data.status,
    )