from pydantic import BaseModel, ConfigDict


class TutorAlumnoBase(BaseModel):
    es_principal: bool = False


class TutorAlumnoCreate(TutorAlumnoBase):
    tutor_id: int
    alumno_id: int


class TutorAlumnoUpdate(BaseModel):
    es_principal: bool | None = None


class TutorAlumnoRead(TutorAlumnoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    tutor_id: int
    alumno_id: int