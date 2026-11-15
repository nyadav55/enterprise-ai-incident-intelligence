
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.incident import Incident
from app.schemas.incident import IncidentCreate, IncidentStatus


class IncidentRepository:
    """
    Handles all database operations for incidents.

    The repository receives a database session from FastAPI.
    It does not create or manage a global database connection.
    """

    def __init__(self, db: Session):
        # Store the session for this particular API request.
        self.db = db

    def create(self, data: IncidentCreate) -> Incident:
        # Convert validated API input into a SQLAlchemy database object.
        incident = Incident(
            title=data.title,
            description=data.description,
            severity=data.severity,
            status=IncidentStatus.NEW,
            source=data.source,
        )

        # Stage the new incident for insertion into PostgreSQL.
        self.db.add(incident)

        # Commit the transaction so the record is permanently stored.
        self.db.commit()

        # Refresh the object to load database-generated/default values.
        self.db.refresh(incident)

        return incident

    def get_by_id(self, incident_id: UUID) -> Incident | None:
        # Fetch one incident using its primary key.
        return self.db.get(Incident, incident_id)

    def list_all(self) -> list[Incident]:
        # Build a query that returns the newest incidents first.
        query = select(Incident).order_by(Incident.created_at.desc())

        # Execute the query and return all matching ORM objects.
        return list(self.db.scalars(query).all())

    def update_status(
        self,
        incident_id: UUID,
        new_status: IncidentStatus,
    ) -> Incident | None:
        # Find the incident that needs to be updated.
        incident = self.get_by_id(incident_id)

        # Return None if the requested incident does not exist.
        if incident is None:
            return None

        # Update the status on the SQLAlchemy object.
        incident.status = new_status

        # SQLAlchemy's onupdate setting updates updated_at on this change.
        self.db.commit()

        # Reload the updated values from PostgreSQL.
        self.db.refresh(incident)

        return incident