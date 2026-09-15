from pydantic import BaseModel, EmailStr
from app.enum import RolUsuario


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    rol: RolUsuario


class TokenPayload(BaseModel):
    sub: int
    rol: RolUsuario
    exp: int