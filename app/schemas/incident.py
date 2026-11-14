# Implement incident schemas 
# # Architect explanation: Pydantic schemas validate incoming requests and define consistent API responses.

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

# Defines the priority/severity of an incident.
class IncidentSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


# Defines the incident lifecycle.
class IncidentStatus(str, Enum):
    NEW = "NEW"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    INVESTIGATING = "INVESTIGATING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


# Data received when a user creates an incident.
class IncidentCreate(BaseModel):
    title: str = Field(min_length=5, max_length=150)
    description: str = Field(min_length=10, max_length=5000)
    severity: IncidentSeverity
    source: str = Field(default="manual", max_length=50)


# Data received when a user changes incident status.
class IncidentStatusUpdate(BaseModel):
    status: IncidentStatus


# Standard incident response returned by the API.
class IncidentResponse(BaseModel):
    # # Allows Pydantic to read values from Python objects.
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    severity: IncidentSeverity
    status: IncidentStatus
    source: str
    created_at: datetime
    updated_at: datetime

