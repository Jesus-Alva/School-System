# app/crud/tutor_alumno.py
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.tutor_alumno import TutorAlumno
from app.schemas.tutor_alumno import TutorAlumnoCreate, TutorAlumnoUpdate


class CRUDTutorAlumno(
    CRUDBase[TutorAlumno, TutorAlumnoCreate, TutorAlumnoUpdate]
):
    def vincular(
        self, db: Session, tutor_id: int, alumno_id: int, es_principal: bool = False
    ) -> TutorAlumno:
        existente = self.get_by(db, tutor_id=tutor_id, alumno_id=alumno_id)
        if existente:
            return existente
        return self.create(
            db,
            {"tutor_id": tutor_id, "alumno_id": alumno_id, "es_principal": es_principal},
        )


tutor_alumno = CRUDTutorAlumno(TutorAlumno)