from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BoletaBase(BaseModel):
    inscripcion_id: int
    ciclo_id: int
    folio: str
    pdf_url: str | None = None
    publicada: bool = False


class BoletaCreate(BaseModel):
    inscripcion_id: int
    ciclo_id: int


class BoletaUpdate(BaseModel):
    publicada: bool | None = None
    pdf_url: str | None = None


class BoletaRead(BoletaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    generada_en: datetime