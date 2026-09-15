from datetime import date
from pydantic import BaseModel, Field, ConfigDict
from app.enum import EstadoAlumno, NivelEducativo


class AlumnoBase(BaseModel):
    matricula: str = Field(..., max_length=30)
    fecha_ingreso: date | None = None
    estado: EstadoAlumno = EstadoAlumno.ACTIVO
    nivel_actual: NivelEducativo | None = None


class AlumnoCreate(AlumnoBase):
    persona_id: int


class AlumnoUpdate(BaseModel):
    matricula: str | None = Field(None, max_length=30)
    fecha_ingreso: date | None = None
    estado: EstadoAlumno | None = None
    nivel_actual: NivelEducativo | None = None


class AlumnoRead(AlumnoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    persona_id: int


class AlumnoConPersona(AlumnoRead):
    persona: "PersonaRead"