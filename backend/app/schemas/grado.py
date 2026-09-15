from pydantic import BaseModel, Field, ConfigDict
from app.enum import NivelEducativo


class GradoBase(BaseModel):
    ciclo_id: int
    nombre: str = Field(..., max_length=50)
    nivel: NivelEducativo
    orden: int = 0


class GradoCreate(GradoBase):
    pass


class GradoUpdate(BaseModel):
    nombre: str | None = Field(None, max_length=50)
    nivel: NivelEducativo | None = None
    orden: int | None = None


class GradoRead(GradoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int