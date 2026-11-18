

from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.schemas.auth import UserRegister, UserLogin
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


class AuthService:

    def __init__(self, db: Session):
        # Database session for user operations.
        self.db = db

    def register_user(self, user_data: UserRegister) -> User:
        # Check whether the email is already registered.
        existing_user = (
            self.db.query(User)
            .filter(User.email == user_data.email)
            .first()
        )

        if existing_user:
            raise ValueError("Email is already registered")

        # Public registration must never grant administrator privileges.
        new_user = User(
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            role=UserRole.OPERATIONS_ENGINEER,
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        return new_user

    def login_user(self, login_data: UserLogin) -> dict:
        # Find the account using its email.
        user = (
            self.db.query(User)
            .filter(User.email == login_data.email)
            .first()
        )

        # Use the same error for incorrect email or password.
        if not user or not verify_password(
            login_data.password, user.password_hash
        ):
            raise ValueError("Invalid email or password")

        # Disabled accounts cannot log in.
        if not user.is_active:
            raise ValueError("User account is inactive")

        # Include user ID and role in the signed JWT.
        token = create_access_token(
            user_id=str(user.id),
            role=user.role.value,
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }
