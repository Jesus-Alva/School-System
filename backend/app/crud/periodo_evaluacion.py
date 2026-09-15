from sqlalchemy import select
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.periodo_evaluacion import PeriodoEvaluacion
from app.schemas.periodo_evaluacion import (
    PeriodoEvaluacionCreate, PeriodoEvaluacionUpdate,
)


class CRUDPeriodoEvaluacion(
    CRUDBase[PeriodoEvaluacion, PeriodoEvaluacionCreate, PeriodoEvaluacionUpdate]
):
    def list_by_ciclo(self, db: Session, ciclo_id: int) -> list[PeriodoEvaluacion]:
        stmt = (
            select(PeriodoEvaluacion)
            .where(
                PeriodoEvaluacion.ciclo_id == ciclo_id,
                PeriodoEvaluacion.deleted_at.is_(None),
            )
            .order_by(PeriodoEvaluacion.orden)
        )
        return list(db.execute(stmt).scalars().all())

    def get_activo(self, db: Session, ciclo_id: int) -> PeriodoEvaluacion | None:
        stmt = select(PeriodoEvaluacion).where(
            PeriodoEvaluacion.ciclo_id == ciclo_id,
            PeriodoEvaluacion.activo.is_(True),
            PeriodoEvaluacion.deleted_at.is_(None),
        )
        return db.execute(stmt).scalar_one_or_none()


periodo_evaluacion = CRUDPeriodoEvaluacion(PeriodoEvaluacion)