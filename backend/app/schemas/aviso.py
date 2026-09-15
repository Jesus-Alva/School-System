from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.enum import AlcanceAviso, RolUsuario


class AvisoBase(BaseModel):
    titulo: str = Field(..., max_length=200)
    contenido: str
    alcance: AlcanceAviso
    rol_destino: RolUsuario | None = None
    grupo_id: int | None = None
    materia_id: int | None = None
    expira_en: datetime | None = None


class AvisoCreate(AvisoBase):
    pass


class AvisoUpdate(BaseModel):
    titulo: str | None = Field(None, max_length=200)
    contenido: str | None = None
    expira_en: datetime | None = None


class AvisoRead(AvisoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    autor_id: int
    fecha_publicacion: datetime | None = None