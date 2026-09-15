from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.crud.base import CRUDBase
from app.models.inscripcion import Inscripcion
from app.schemas.inscripcion import InscripcionCreate, InscripcionUpdate


class CRUDInscripcion(CRUDBase[Inscripcion, InscripcionCreate, InscripcionUpdate]):
    def get_by_alumno_ciclo(
        self, db: Session, alumno_id: int, ciclo_id: int
    ) -> Inscripcion | None:
        stmt = select(Inscripcion).where(
            Inscripcion.alumno_id == alumno_id,
            Inscripcion.ciclo_id == ciclo_id,
            Inscripcion.deleted_at.is_(None),
        )
        return db.execute(stmt).scalar_one_or_none()

    def list_by_grupo(self, db: Session, grupo_id: int) -> list[Inscripcion]:
        stmt = (
            select(Inscripcion)
            .options(joinedload(Inscripcion.alumno))
            .where(
                Inscripcion.grupo_id == grupo_id,
                Inscripcion.deleted_at.is_(None),
            )
        )
        return list(db.execute(stmt).scalars().all())

    def contar_en_grupo(self, db: Session, grupo_id: int) -> int:
        from sqlalchemy import func
        stmt = (
            select(func.count())
            .select_from(Inscripcion)
            .where(
                Inscripcion.grupo_id == grupo_id,
                Inscripcion.deleted_at.is_(None),
            )
        )
        return db.execute(stmt).scalar_one()


inscripcion = CRUDInscripcion(Inscripcion)