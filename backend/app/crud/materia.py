from sqlalchemy import select
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.materia import Materia
from app.schemas.materia import MateriaCreate, MateriaUpdate
from app.enum import NivelEducativo


class CRUDMateria(CRUDBase[Materia, MateriaCreate, MateriaUpdate]):
    def get_by_clave(self, db: Session, clave: str) -> Materia | None:
        stmt = select(Materia).where(
            Materia.clave == clave, Materia.deleted_at.is_(None)
        )
        return db.execute(stmt).scalar_one_or_none()

    def list_by_nivel(
        self, db: Session, nivel: NivelEducativo, solo_activas: bool = True
    ) -> list[Materia]:
        stmt = select(Materia).where(
            Materia.nivel == nivel, Materia.deleted_at.is_(None)
        )
        if solo_activas:
            stmt = stmt.where(Materia.activo.is_(True))
        return list(db.execute(stmt).scalars().all())


materia = CRUDMateria(Materia)