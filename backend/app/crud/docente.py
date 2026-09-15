from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.crud.base import CRUDBase
from app.models.docente import Docente
from app.schemas.docente import DocenteCreate, DocenteUpdate
from app.enum import EstadoDocente


class CRUDDocente(CRUDBase[Docente, DocenteCreate, DocenteUpdate]):
    def get_by_persona(self, db: Session, persona_id: int) -> Docente | None:
        stmt = select(Docente).where(
            Docente.persona_id == persona_id, Docente.deleted_at.is_(None)
        )
        return db.execute(stmt).scalar_one_or_none()

    def get_con_persona(self, db: Session, docente_id: int) -> Docente | None:
        stmt = (
            select(Docente)
            .options(joinedload(Docente.persona), joinedload(Docente.materia_principal))
            .where(Docente.id == docente_id, Docente.deleted_at.is_(None))
        )
        return db.execute(stmt).scalar_one_or_none()

    def list_por_materia(
        self, db: Session, materia_id: int, solo_activos: bool = True
    ) -> list[Docente]:
        stmt = select(Docente).where(
            Docente.materia_principal_id == materia_id,
            Docente.deleted_at.is_(None),
        )
        if solo_activos:
            stmt = stmt.where(Docente.estado == EstadoDocente.ACTIVO)
        return list(db.execute(stmt).scalars().all())

    def list_con_persona(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> list[Docente]:
        stmt = (
            select(Docente)
            .options(joinedload(Docente.persona))
            .where(Docente.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
        )
        return list(db.execute(stmt).scalars().all())


docente = CRUDDocente(Docente)