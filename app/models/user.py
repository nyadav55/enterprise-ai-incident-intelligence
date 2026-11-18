# Create User database model


from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum as SQLAlchemyEnum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


# Defines the permissions category assigned to each user.
class UserRole(str, Enum):
    ADMIN = "ADMIN"
    INCIDENT_MANAGER = "INCIDENT_MANAGER"
    OPERATIONS_ENGINEER = "OPERATIONS_ENGINEER"


# Defines the database structure for application users.
class User(Base):
    __tablename__ = "users"

    # Unique ID for every user.
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )

    # Email is the user's login identity and must be unique.
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )

    # Store only the password hash, never the original password.
    password_hash: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    # Controls which operations the user is allowed to perform.
    role: Mapped[UserRole] = mapped_column(
        SQLAlchemyEnum(UserRole, name="user_role"),
        nullable=False,
        default=UserRole.OPERATIONS_ENGINEER,
    )

    # Allows administrators to disable accounts without deleting them.
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    # Records when the account was created.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
