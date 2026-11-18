# Update model registration

from app.models.incident import Incident
from app.models.user import User, UserRole

# Expose models for Alembic and other application modules.
__all__ = ["Incident", "User", "UserRole"]