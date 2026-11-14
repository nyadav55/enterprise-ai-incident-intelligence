


from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.schemas.incident import (
    IncidentCreate,
    IncidentResponse,
    IncidentStatus,
)


# Temporary storage for our first working API.
# This data disappears when the application restarts.
class IncidentRepository:

# __init__() method is a constructor which is automatically called when a new object of a class is created. 
    def __init__(self):
# • single leading underscore (_) is a Python naming convention indicating that this variable is intended for internal or "private" use within the class.
        
        self._incidents: dict[UUID, IncidentResponse] = {}

    def create(self, data: IncidentCreate) -> IncidentResponse:
        now = datetime.now(timezone.utc)

        incident = IncidentResponse(
            id=uuid4(),
            title=data.title,
            description=data.description,
            severity=data.severity,
            status=IncidentStatus.NEW,
            source=data.source,
            created_at=now,
            updated_at=now,
        )

        self._incidents[incident.id] = incident
        return incident

    def get_by_id(self, incident_id: UUID):
        return self._incidents.get(incident_id)

    def list_all(self):
        return list(self._incidents.values())

    def update_status(
        self,
        incident_id: UUID,
        status: IncidentStatus,
    ):
        incident = self.get_by_id(incident_id)

        if incident is None:
            return None

        updated = incident.model_copy(
            update={
                "status": status,
                "updated_at": datetime.now(timezone.utc),
            }
        )

        self._incidents[incident_id] = updated
        return updated


# One repository instance shared by this application process.
incident_repository = IncidentRepository()
