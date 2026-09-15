from datetime import date
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.enum import Sexo


class PersonaBase(BaseModel):
    nombres: str = Field(..., max_length=120)
    apellido_paterno: str = Field(..., max_length=120)
    apellido_materno: str | None = Field(None, max_length=120)
    fecha_nacimiento: date | None = None
    curp: str | None = Field(None, max_length=18)
    sexo: Sexo | None = None
    telefono: str | None = Field(None, max_length=20)
    email: EmailStr
    direccion: str | None = None
    foto_url: str | None = Field(None, max_length=500)


class PersonaCreate(PersonaBase):
    pass


class PersonaUpdate(BaseModel):
    nombres: str | None = Field(None, max_length=120)
    apellido_paterno: str | None = Field(None, max_length=120)
    apellido_materno: str | None = Field(None, max_length=120)
    fecha_nacimiento: date | None = None
    curp: str | None = Field(None, max_length=18)
    sexo: Sexo | None = None
    telefono: str | None = Field(None, max_length=20)
    email: EmailStr | None = None
    direccion: str | None = None
    foto_url: str | None = Field(None, max_length=500)


class PersonaRead(PersonaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
