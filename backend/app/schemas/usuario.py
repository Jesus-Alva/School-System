from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.enum import RolUsuario, EstadoUsuario


class UsuarioBase(BaseModel):
    email: EmailStr
    rol: RolUsuario
    estado: EstadoUsuario = EstadoUsuario.ACTIVO
    two_factor_enabled: bool = False


class UsuarioCreate(UsuarioBase):
    persona_id: int
    password: str = Field(..., min_length=8, max_length=128)


class UsuarioUpdate(BaseModel):
    email: EmailStr | None = None
    rol: RolUsuario | None = None
    estado: EstadoUsuario | None = None
    two_factor_enabled: bool | None = None


class UsuarioChangePassword(BaseModel):
    password_actual: str
    password_nueva: str = Field(..., min_length=8, max_length=128)


class UsuarioRead(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    persona_id: int
    ultimo_acceso: datetime | None = None


class UsuarioConPersona(UsuarioRead):
    persona: "PersonaRead"
