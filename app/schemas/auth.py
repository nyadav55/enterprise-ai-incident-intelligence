# Create authentication schemas


from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.user import UserRole


# Data required when a user registers.
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


# Data required when a user logs in.
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Standard user information returned by the API.
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    role: UserRole
    is_active: bool


# JWT response returned after successful login.
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
