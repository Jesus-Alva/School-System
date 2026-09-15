from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.crud.base import CRUDBase
from app.models.plan_estudio import PlanEstudio
from app.schemas.plan_estudio import PlanEstudioCreate, PlanEstudioUpdate


class CRUDPlanEstudio(CRUDBase[PlanEstudio, PlanEstudioCreate, PlanEstudioUpdate]):
    def list_by_grado(self, db: Session, grado_id: int) -> list[PlanEstudio]:
        stmt = (
            select(PlanEstudio)
            .options(joinedload(PlanEstudio.materia))
            .where(PlanEstudio.grado_id == grado_id, PlanEstudio.deleted_at.is_(None))
        )
        return list(db.execute(stmt).scalars().all())


plan_estudio = CRUDPlanEstudio(PlanEstudio)