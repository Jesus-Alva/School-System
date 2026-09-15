from pydantic import BaseModel, Field, ConfigDict


class TutorBase(BaseModel):
    parentesco: str = Field(..., max_length=50)
    ocupacion: str | None = Field(None, max_length=120)


class TutorCreate(TutorBase):
    persona_id: int


class TutorUpdate(BaseModel):
    parentesco: str | None = Field(None, max_length=50)
    ocupacion: str | None = Field(None, max_length=120)


class TutorRead(TutorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    persona_id: int


class TutorConPersona(TutorRead):
    persona: "PersonaRead"