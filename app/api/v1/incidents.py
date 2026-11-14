# Implement REST API endpoints


from uuid import UUID

from fastapi import APIRouter, status

from app.schemas.incident import (
    IncidentCreate,
    IncidentResponse,
    IncidentStatusUpdate,
)
from app.services.incident_service import incident_service


router = APIRouter(
    prefix="/incidents",
    tags=["Incident Management"],
)


# Create a new incident.
@router.post(
    "/",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_incident(data: IncidentCreate):
    return incident_service.create_incident(data)


# Retrieve all incidents.
@router.get("/", response_model=list[IncidentResponse])
def list_incidents():
    return incident_service.list_incidents()


# Retrieve one incident by ID.
@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: UUID):
    return incident_service.get_incident(incident_id)


# Change an incident's status.
@router.patch(
    "/{incident_id}/status",
    response_model=IncidentResponse,
)
def update_incident_status(
    incident_id: UUID,
    data: IncidentStatusUpdate,
):
    return incident_service.update_status(
        incident_id,
        data.status,
    )

# python -m uvicorn app.main:app --reload
