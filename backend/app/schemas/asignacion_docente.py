from pydantic import BaseModel, ConfigDict, model_validator
from app.enum import RolDocente


class AsignacionDocenteBase(BaseModel):
    docente_id: int
    materia_id: int
    grupo_id: int
    ciclo_id: int
    rol_docente: RolDocente = RolDocente.TITULAR


class AsignacionDocenteCreate(AsignacionDocenteBase):
    pass


class AsignacionDocenteUpdate(BaseModel):
    rol_docente: RolDocente | None = None


class AsignacionDocenteRead(AsignacionDocenteBase):
    model_config = ConfigDict(from_attributes=True)
    id: int