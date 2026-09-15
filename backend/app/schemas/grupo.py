from pydantic import BaseModel, Field, ConfigDict


class GrupoBase(BaseModel):
    grado_id: int
    ciclo_id: int
    nombre: str = Field(..., max_length=10)
    capacidad: int = Field(30, ge=1, le=100)
    salon_id: int | None = None


class GrupoCreate(GrupoBase):
    pass


class GrupoUpdate(BaseModel):
    nombre: str | None = Field(None, max_length=10)
    capacidad: int | None = Field(None, ge=1, le=100)
    salon_id: int | None = None


class GrupoRead(GrupoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int