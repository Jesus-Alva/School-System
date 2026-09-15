from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.crud.base import CRUDBase
from app.models.asignacion_docente import AsignacionDocente
from app.schemas.asignacion_docente import (
    AsignacionDocenteCreate, AsignacionDocenteUpdate,
)


class CRUDAsignacionDocente(
    CRUDBase[AsignacionDocente, AsignacionDocenteCreate, AsignacionDocenteUpdate]
):
    def list_by_grupo(self, db: Session, grupo_id: int) -> list[AsignacionDocente]:
        stmt = (
            select(AsignacionDocente)
            .options(
                joinedload(AsignacionDocente.docente).joinedload("persona"),
                joinedload(AsignacionDocente.materia),
            )
            .where(
                AsignacionDocente.grupo_id == grupo_id,
                AsignacionDocente.deleted_at.is_(None),
            )
        )
        return list(db.execute(stmt).scalars().all())

    def list_by_docente(
        self, db: Session, docente_id: int, ciclo_id: int | None = None
    ) -> list[AsignacionDocente]:
        stmt = select(AsignacionDocente).where(
            AsignacionDocente.docente_id == docente_id,
            AsignacionDocente.deleted_at.is_(None),
        )
        if ciclo_id:
            stmt = stmt.where(AsignacionDocente.ciclo_id == ciclo_id)
        return list(db.execute(stmt).scalars().all())

    def existe_titular(
        self, db: Session, grupo_id: int, materia_id: int, ciclo_id: int
    ) -> bool:
        stmt = select(AsignacionDocente).where(
            AsignacionDocente.grupo_id == grupo_id,
            AsignacionDocente.materia_id == materia_id,
            AsignacionDocente.ciclo_id == ciclo_id,
            AsignacionDocente.deleted_at.is_(None),
        )
        return db.execute(stmt).scalar_one_or_none() is not None


asignacion_docente = CRUDAsignacionDocente(AsignacionDocente)