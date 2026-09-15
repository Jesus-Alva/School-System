from pydantic import BaseModel, Field, ConfigDict
from app.enum import EstadoDocente


class DocenteBase(BaseModel):
    materia_principal_id: int
    especialidad: str | None = Field(None, max_length=150)
    cedula_profesional: str | None = Field(None, max_length=50)
    estado: EstadoDocente = EstadoDocente.ACTIVO


class DocenteCreate(DocenteBase):
    persona_id: int


class DocenteUpdate(BaseModel):
    especialidad: str | None = Field(None, max_length=150)
    cedula_profesional: str | None = Field(None, max_length=50)
    estado: EstadoDocente | None = None


class DocenteRead(DocenteBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    persona_id: int


class DocenteConPersona(DocenteRead):
    persona: "PersonaRead"
    materia_principal: "MateriaRead | None" = None