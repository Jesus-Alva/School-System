from pydantic import BaseModel, ConfigDict


class PlanEstudioBase(BaseModel):
    grado_id: int
    materia_id: int
    horas_semana: int = 0
    obligatoria: bool = True


class PlanEstudioCreate(PlanEstudioBase):
    pass


class PlanEstudioUpdate(BaseModel):
    horas_semana: int | None = None
    obligatoria: bool | None = None


class PlanEstudioRead(PlanEstudioBase):
    model_config = ConfigDict(from_attributes=True)
    id: int