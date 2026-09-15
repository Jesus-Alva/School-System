from sqlalchemy import select
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.grado import Grado
from app.schemas.grado import GradoCreate, GradoUpdate
from app.enum import NivelEducativo


class CRUDGrado(CRUDBase[Grado, GradoCreate, GradoUpdate]):
    def list_by_ciclo(
        self, db: Session, ciclo_id: int, nivel: NivelEducativo | None = None
    ) -> list[Grado]:
        stmt = select(Grado).where(
            Grado.ciclo_id == ciclo_id, Grado.deleted_at.is_(None)
        )
        if nivel:
            stmt = stmt.where(Grado.nivel == nivel)
        stmt = stmt.order_by(Grado.orden)
        return list(db.execute(stmt).scalars().all())


grado = CRUDGrado(Grado)