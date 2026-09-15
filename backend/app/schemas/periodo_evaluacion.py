from datetime import date
from pydantic import BaseModel, Field, ConfigDict, model_validator


class PeriodoEvaluacionBase(BaseModel):
    ciclo_id: int
    nombre: str = Field(..., max_length=80)
    orden: int = Field(..., ge=1)
    fecha_inicio: date
    fecha_fin: date
    activo: bool = True

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.fecha_fin <= self.fecha_inicio:
            raise ValueError("fecha_fin debe ser posterior a fecha_inicio")
        return self


class PeriodoEvaluacionCreate(PeriodoEvaluacionBase):
    pass


class PeriodoEvaluacionUpdate(BaseModel):
    nombre: str | None = Field(None, max_length=80)
    orden: int | None = Field(None, ge=1)
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    activo: bool | None = None


class PeriodoEvaluacionRead(PeriodoEvaluacionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int