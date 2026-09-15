from pydantic import BaseModel, Field, ConfigDict
from app.enum import NivelEducativo


class MateriaBase(BaseModel):
    nombre: str = Field(..., max_length=120)
    clave: str = Field(..., max_length=30)
    nivel: NivelEducativo
    horas_semana: int = Field(0, ge=0, le=40)
    activo: bool = True


class MateriaCreate(MateriaBase):
    pass


class MateriaUpdate(BaseModel):
    nombre: str | None = Field(None, max_length=120)
    clave: str | None = Field(None, max_length=30)
    nivel: NivelEducativo | None = None
    horas_semana: int | None = Field(None, ge=0, le=40)
    activo: bool | None = None


class MateriaRead(MateriaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int