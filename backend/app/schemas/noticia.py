from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class NoticiaBase(BaseModel):
    titulo: str = Field(..., max_length=200)
    slug: str = Field(..., max_length=220)
    contenido: str
    imagen_url: str | None = Field(None, max_length=500)
    publicado: bool = False


class NoticiaCreate(NoticiaBase):
    pass


class NoticiaUpdate(BaseModel):
    titulo: str | None = Field(None, max_length=200)
    slug: str | None = Field(None, max_length=220)
    contenido: str | None = None
    imagen_url: str | None = Field(None, max_length=500)
    publicado: bool | None = None


class NoticiaRead(NoticiaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    autor_id: int
    fecha_publicacion: datetime | None = None