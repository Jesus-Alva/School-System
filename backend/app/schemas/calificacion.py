from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from app.enum import EstadoCalificacion


class CalificacionBase(BaseModel):
    inscripcion_id: int
    materia_id: int
    periodo_id: int
    valor: Decimal = Field(..., ge=0, le=10, decimal_places=2)
    observaciones: str | None = None


class CalificacionCreate(CalificacionBase):
    pass


class CalificacionUpdate(BaseModel):
    valor: Decimal | None = Field(None, ge=0, le=10, decimal_places=2)
    observaciones: str | None = None


class CalificacionCambioEstado(BaseModel):
    estado: EstadoCalificacion


class CalificacionRead(CalificacionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    capturado_por: int
    estado: EstadoCalificacion


class CalificacionMasiva(BaseModel):
    """Para captura por lote de un grupo-materia-periodo."""
    grupo_id: int
    materia_id: int
    periodo_id: int
    items: list[dict]  # [{inscripcion_id, valor, observaciones?}]