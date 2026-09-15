from datetime import date
from pydantic import BaseModel, ConfigDict
from app.enum import EstadoAsistencia


class AsistenciaBase(BaseModel):
    inscripcion_id: int
    fecha: date
    estado: EstadoAsistencia
    justificacion: str | None = None


class AsistenciaCreate(AsistenciaBase):
    pass


class AsistenciaUpdate(BaseModel):
    estado: EstadoAsistencia | None = None
    justificacion: str | None = None


class AsistenciaRead(AsistenciaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    registrado_por: int


class AsistenciaMasiva(BaseModel):
    grupo_id: int
    fecha: date
    items: list[dict]  # [{inscripcion_id, estado, justificacion?}]