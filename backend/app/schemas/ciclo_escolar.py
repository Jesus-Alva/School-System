from datetime import date
from pydantic import BaseModel, Field, ConfigDict, model_validator


class CicloEscolarBase(BaseModel):
    nombre: str = Field(..., max_length=20)
    fecha_inicio: date
    fecha_fin: date
    activo: bool = False

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.fecha_fin <= self.fecha_inicio:
            raise ValueError("fecha_fin debe ser posterior a fecha_inicio")
        return self


class CicloEscolarCreate(CicloEscolarBase):
    pass


class CicloEscolarUpdate(BaseModel):
    nombre: str | None = Field(None, max_length=20)
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    activo: bool | None = None


class CicloEscolarRead(CicloEscolarBase):
    model_config = ConfigDict(from_attributes=True)
    id: int