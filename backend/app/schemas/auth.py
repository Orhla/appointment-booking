from typing import Annotated
from pydantic import AfterValidator, BaseModel, EmailStr, Field
from app.models.user import Role

class AuthCredentials(BaseModel):
    email: Annotated[EmailStr, AfterValidator(str.lower)]
    password: str = Field(..., min_length=8, max_length=64)

class RegisterRequest(AuthCredentials):
    pass

class LoginRequest(AuthCredentials):
    pass

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: Role
    model_config = {"from_attributes": True}