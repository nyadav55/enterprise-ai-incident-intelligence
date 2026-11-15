# Create the database model
# Why do we use a database model?

# Our Pydantic schema validates incoming API requests. Our SQLAlchemy model defines how data is stored in PostgreSQL.
# Pydantic schema	SQLAlchemy model
# Validates API input	Defines database columns
# Controls API response	Controls database persistence
# Used by FastAPI	Used by database repository

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, Enum, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.schemas.incident import IncidentSeverity, IncidentStatus


class Incident(Base):
    # Actual PostgreSQL table name.
    __tablename__ = "incidents"

    # Unique identifier for each incident.
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    # Short incident title.
    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    # Detailed description of the incident.
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Business severity of the incident.
    severity: Mapped[IncidentSeverity] = mapped_column(
        Enum(IncidentSeverity, name="incident_severity"),
        nullable=False,
    )

    # Current incident lifecycle status.
    status: Mapped[IncidentStatus] = mapped_column(
        Enum(IncidentStatus, name="incident_status"),
        nullable=False,
        default=IncidentStatus.NEW,
    )

    # Origin of the incident: monitoring, manual, etc.
    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="manual",
    )

    # Timestamp when the incident was created.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # Timestamp when the incident was last updated.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
