
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.incident import Incident
from app.schemas.incident import IncidentCreate, IncidentStatus, IncidentSeverity


class IncidentRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: IncidentCreate) -> Incident:
        incident = Incident(
            title=data.title,
            description=data.description,
            severity=data.severity,
            status=IncidentStatus.NEW,
            source=data.source,
        )
        self.db.add(incident)
        self.db.commit()
        self.db.refresh(incident)
        return incident

    def get_by_id(self, incident_id: UUID) -> Incident | None:
        return self.db.get(Incident, incident_id)

    # Supports pagination, filtering and title search.
    def list_all(
        self,
        skip: int = 0,
        limit: int = 10,
        severity: IncidentSeverity | None = None,
        status: IncidentStatus | None = None,
        search: str | None = None,
    ) -> list[Incident]:

        query = select(Incident)

        # Apply severity filter when supplied.
        if severity:
            query = query.where(Incident.severity == severity)

        # Apply status filter when supplied.
        if status:
            query = query.where(Incident.status == status)

        # Search incident titles without case sensitivity.
        if search:
            query = query.where(Incident.title.ilike(f"%{search}%"))

        # Return newest incidents first, with pagination.
        query = query.order_by(
            Incident.created_at.desc()
        ).offset(skip).limit(limit)

        return list(self.db.scalars(query).all())

    def update_status(
        self,
        incident_id: UUID,
        new_status: IncidentStatus,
    ) -> Incident | None:

        incident = self.get_by_id(incident_id)

        if incident is None:
            return None

        incident.status = new_status
        self.db.commit()
        self.db.refresh(incident)

        return incident
