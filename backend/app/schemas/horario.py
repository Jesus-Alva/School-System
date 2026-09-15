from datetime import time
from pydantic import BaseModel, ConfigDict, model_validator
from app.enum import DiaSemana


class HorarioBase(BaseModel):
    grupo_id: int
    materia_id: int
    docente_id: int
    salon_id: int
    ciclo_id: int
    dia_semana: DiaSemana
    hora_inicio: time
    hora_fin: time

    @model_validator(mode="after")
    def validar_horas(self):
        if self.hora_fin <= self.hora_inicio:
            raise ValueError("hora_fin debe ser posterior a hora_inicio")
        return self


class HorarioCreate(HorarioBase):
    pass


class HorarioUpdate(BaseModel):
    salon_id: int | None = None
    dia_semana: DiaSemana | None = None
    hora_inicio: time | None = None
    hora_fin: time | None = None


class HorarioRead(HorarioBase):
    model_config = ConfigDict(from_attributes=True)
    id: int