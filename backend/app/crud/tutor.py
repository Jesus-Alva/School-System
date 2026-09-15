# app/crud/tutor.py
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.crud.base import CRUDBase
from app.models.tutor import Tutor
from app.schemas.tutor import TutorCreate, TutorUpdate


class CRUDTutor(CRUDBase[Tutor, TutorCreate, TutorUpdate]):
    def get_by_persona(self, db: Session, persona_id: int) -> Tutor | None:
        stmt = select(Tutor).where(
            Tutor.persona_id == persona_id, Tutor.deleted_at.is_(None)
        )
        return db.execute(stmt).scalar_one_or_none()

    def list_by_alumno(self, db: Session, alumno_id: int) -> list[Tutor]:
        from app.models.tutor_alumno import TutorAlumno
        stmt = (
            select(Tutor)
            .join(TutorAlumno, TutorAlumno.tutor_id == Tutor.id)
            .options(joinedload(Tutor.persona))
            .where(
                TutorAlumno.alumno_id == alumno_id,
                Tutor.deleted_at.is_(None),
            )
        )
        return list(db.execute(stmt).scalars().all())


tutor = CRUDTutor(Tutor)