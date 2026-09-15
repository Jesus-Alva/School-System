from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.crud.base import CRUDBase
from app.models.grupo import Grupo
from app.schemas.grupo import GrupoCreate, GrupoUpdate


class CRUDGrupo(CRUDBase[Grupo, GrupoCreate, GrupoUpdate]):
    def list_by_ciclo(self, db: Session, ciclo_id: int) -> list[Grupo]:
        stmt = (
            select(Grupo)
            .options(joinedload(Grupo.grado), joinedload(Grupo.salon))
            .where(Grupo.ciclo_id == ciclo_id, Grupo.deleted_at.is_(None))
        )
        return list(db.execute(stmt).scalars().all())

    def list_by_grado(self, db: Session, grado_id: int) -> list[Grupo]:
        stmt = select(Grupo).where(
            Grupo.grado_id == grado_id, Grupo.deleted_at.is_(None)
        )
        return list(db.execute(stmt).scalars().all())

    def asignar_salon(
        self, db: Session, grupo: Grupo, salon_id: int | None
    ) -> Grupo:
        grupo.salon_id = salon_id
        db.add(grupo)
        db.commit()
        db.refresh(grupo)
        return grupo


grupo = CRUDGrupo(Grupo)