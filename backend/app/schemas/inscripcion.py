from datetime import date
from pydantic import BaseModel, ConfigDict
from app.enum import EstadoInscripcion


class InscripcionBase(BaseModel):
    alumno_id: int
    grupo_id: int
    ciclo_id: int
    fecha_inscripcion: date
    estado: EstadoInscripcion = EstadoInscripcion.ACTIVO


class InscripcionCreate(InscripcionBase):
    pass


class InscripcionUpdate(BaseModel):
    grupo_id: int | None = None
    estado: EstadoInscripcion | None = None


class InscripcionRead(InscripcionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int