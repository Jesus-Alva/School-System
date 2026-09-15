from pydantic import BaseModel, Field, ConfigDict


class DirectivoBase(BaseModel):
    cargo: str = Field(..., max_length=80)
    activo: bool = True


class DirectivoCreate(DirectivoBase):
    persona_id: int


class DirectivoUpdate(BaseModel):
    cargo: str | None = Field(None, max_length=80)
    activo: bool | None = None


class DirectivoRead(DirectivoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    persona_id: int