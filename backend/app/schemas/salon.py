from pydantic import BaseModel, Field, ConfigDict


class SalonBase(BaseModel):
    nombre: str = Field(..., max_length=50)
    capacidad: int = Field(30, ge=1, le=200)
    ubicacion: str | None = Field(None, max_length=150)
    activo: bool = True


class SalonCreate(SalonBase):
    pass


class SalonUpdate(BaseModel):
    nombre: str | None = Field(None, max_length=50)
    capacidad: int | None = Field(None, ge=1, le=200)
    ubicacion: str | None = Field(None, max_length=150)
    activo: bool | None = None


class SalonRead(SalonBase):
    model_config = ConfigDict(from_attributes=True)
    id: int