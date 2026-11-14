# Implement business logic



from uuid import UUID

from fastapi import HTTPException, status

from app.repositories.incident_repository import incident_repository
from app.schemas.incident import (
    IncidentCreate,
    IncidentStatus,
    IncidentResponse,
)


# Defines which status transitions are allowed.
ALLOWED_TRANSITIONS = {
    IncidentStatus.NEW: [
        IncidentStatus.ACKNOWLEDGED,
        IncidentStatus.INVESTIGATING,
        IncidentStatus.CLOSED,
    ],
    IncidentStatus.ACKNOWLEDGED: [
        IncidentStatus.INVESTIGATING,
        IncidentStatus.CLOSED,
    ],
    IncidentStatus.INVESTIGATING: [
        IncidentStatus.RESOLVED,
    ],
    IncidentStatus.RESOLVED: [
        IncidentStatus.CLOSED,
        IncidentStatus.INVESTIGATING,
    ],
    IncidentStatus.CLOSED: [],
}


class IncidentService:

    def create_incident(self, data: IncidentCreate):
        return incident_repository.create(data)

    def get_incident(self, incident_id: UUID):
        incident = incident_repository.get_by_id(incident_id)

        if incident is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Incident not found",
            )

        return incident

    def list_incidents(self):
        return incident_repository.list_all()

    def update_status(
        self,
        incident_id: UUID,
        new_status: IncidentStatus,
    ) -> IncidentResponse:

        incident = self.get_incident(incident_id)

        allowed = ALLOWED_TRANSITIONS[incident.status]

        if new_status not in allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid transition: {incident.status} to {new_status}",
            )

        return incident_repository.update_status(
            incident_id,
            new_status,
        )


# Shared service instance for the API router.
incident_service = IncidentService()
