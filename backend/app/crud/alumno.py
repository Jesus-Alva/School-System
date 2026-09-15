from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.crud.base import CRUDBase
from app.models.alumno import Alumno
from app.schemas.alumno import AlumnoCreate, AlumnoUpdate
from app.enum import EstadoAlumno


class CRUDAlumno(CRUDBase[Alumno, AlumnoCreate, AlumnoUpdate]):
    def get_by_matricula(self, db: Session, matricula: str) -> Alumno | None:
        stmt = select(Alumno).where(
            Alumno.matricula == matricula, Alumno.deleted_at.is_(None)
        )
        return db.execute(stmt).scalar_one_or_none()

    def get_by_persona(self, db: Session, persona_id: int) -> Alumno | None:
        stmt = select(Alumno).where(
            Alumno.persona_id == persona_id, Alumno.deleted_at.is_(None)
        )
        return db.execute(stmt).scalar_one_or_none()

    def get_con_persona(self, db: Session, alumno_id: int) -> Alumno | None:
        stmt = (
            select(Alumno)
            .options(joinedload(Alumno.persona))
            .where(Alumno.id == alumno_id, Alumno.deleted_at.is_(None))
        )
        return db.execute(stmt).scalar_one_or_none()

    def list_con_persona(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        estado: EstadoAlumno | None = None,
    ) -> list[Alumno]:
        stmt = (
            select(Alumno)
            .options(joinedload(Alumno.persona))
            .where(Alumno.deleted_at.is_(None))
        )
        if estado:
            stmt = stmt.where(Alumno.estado == estado)
        stmt = stmt.offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())


alumno = CRUDAlumno(Alumno)