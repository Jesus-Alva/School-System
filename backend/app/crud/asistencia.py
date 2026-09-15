from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.asistencia import Asistencia
from app.schemas.asistencia import AsistenciaCreate, AsistenciaUpdate


class CRUDAsistencia(CRUDBase[Asistencia, AsistenciaCreate, AsistenciaUpdate]):
    def get_by_inscripcion_fecha(
        self, db: Session, inscripcion_id: int, fecha: date
    ) -> Asistencia | None:
        stmt = select(Asistencia).where(
            Asistencia.inscripcion_id == inscripcion_id,
            Asistencia.fecha == fecha,
            Asistencia.deleted_at.is_(None),
        )
        return db.execute(stmt).scalar_one_or_none()

    def list_by_grupo_fecha(
        self, db: Session, grupo_id: int, fecha: date
    ) -> list[Asistencia]:
        from app.models.inscripcion import Inscripcion
        stmt = (
            select(Asistencia)
            .join(Inscripcion, Asistencia.inscripcion_id == Inscripcion.id)
            .where(
                Inscripcion.grupo_id == grupo_id,
                Asistencia.fecha == fecha,
                Asistencia.deleted_at.is_(None),
            )
        )
        return list(db.execute(stmt).scalars().all())


asistencia = CRUDAsistencia(Asistencia)