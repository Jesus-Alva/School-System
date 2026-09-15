from sqlalchemy import select
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.salon import Salon
from app.schemas.salon import SalonCreate, SalonUpdate


class CRUDSalon(CRUDBase[Salon, SalonCreate, SalonUpdate]):
    def get_by_nombre(self, db: Session, nombre: str) -> Salon | None:
        stmt = select(Salon).where(
            Salon.nombre == nombre, Salon.deleted_at.is_(None)
        )
        return db.execute(stmt).scalar_one_or_none()

    def list_disponibles(self, db: Session, ciclo_id: int) -> list[Salon]:
        """Salones sin grupo asignado en el ciclo dado."""
        from app.models.grupo import Grupo
        subq = (
            select(Grupo.salon_id)
            .where(Grupo.ciclo_id == ciclo_id, Grupo.salon_id.isnot(None))
        )
        stmt = select(Salon).where(
            Salon.activo.is_(True),
            Salon.deleted_at.is_(None),
            Salon.id.notin_(subq),
        )
        return list(db.execute(stmt).scalars().all())


salon = CRUDSalon(Salon)