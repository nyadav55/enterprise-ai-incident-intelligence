# Create authentication dependency


from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User, UserRole


# Swagger will provide a Bearer token for protected APIs.
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:

    # Extract the actual JWT from the Authorization header.
    token = credentials.credentials

    # Validate JWT signature and expiry.
    payload = decode_access_token(token)

    # Keep the remaining validation and database lookup logic unchanged.
    if not payload or not payload.get("sub"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Fetch the current user from the database.
    user = db.query(User).filter(
        User.id == payload["sub"]
    ).first()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    return user

def require_roles(*allowed_roles: UserRole):
    # Create a reusable authorization dependency.
    def role_checker(
        current_user: User = Depends(get_current_user),
    ):
        # Check whether the logged-in user's role is permitted.
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )

        return current_user

    return role_checker

