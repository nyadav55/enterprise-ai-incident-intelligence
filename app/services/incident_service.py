
from uuid import UUID

from fastapi import HTTPException, status

from app.repositories.incident_repository import IncidentRepository
from app.schemas.incident import IncidentCreate, IncidentStatus


# Defines which incident lifecycle transitions are permitted.
# Keeping these rules in the service prevents invalid business operations.
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
    """
    Contains incident business rules.

    It delegates database operations to IncidentRepository.
    """

    def __init__(self, repository: IncidentRepository):
        # Receive the repository created for this request.
        self.repository = repository

    def create_incident(self, data: IncidentCreate):
        # Delegate incident creation to the database repository.
        return self.repository.create(data)

    def get_incident(self, incident_id: UUID):
        # Retrieve the incident from PostgreSQL.
        incident = self.repository.get_by_id(incident_id)

        # Return HTTP 404 if the incident does not exist.
        if incident is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Incident not found",
            )

        return incident

    def list_incidents(self):
        # Delegate the database query to the repository.
        return self.repository.list_all()

    def update_status(
        self,
        incident_id: UUID,
        new_status: IncidentStatus,
    ):
        # First confirm that the incident exists.
        incident = self.get_incident(incident_id)

        # Find the permitted next statuses for its current status.
        allowed = ALLOWED_TRANSITIONS[incident.status]

        # Reject transitions that violate the incident lifecycle.
        if new_status not in allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Invalid transition: "
                    f"{incident.status} to {new_status}"
                ),
            )

        # Persist the approved status change in PostgreSQL.
        return self.repository.update_status(incident_id, new_status)