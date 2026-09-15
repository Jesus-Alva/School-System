from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.crud.base import CRUDBase
from app.models.calificacion import Calificacion
from app.schemas.calificacion import CalificacionCreate, CalificacionUpdate
from app.enum import EstadoCalificacion


class CRUDCalificacion(
    CRUDBase[Calificacion, CalificacionCreate, CalificacionUpdate]
):
    def get_unica(
        self,
        db: Session,
        inscripcion_id: int,
        materia_id: int,
        periodo_id: int,
    ) -> Calificacion | None:
        stmt = select(Calificacion).where(
            Calificacion.inscripcion_id == inscripcion_id,
            Calificacion.materia_id == materia_id,
            Calificacion.periodo_id == periodo_id,
            Calificacion.deleted_at.is_(None),
        )
        return db.execute(stmt).scalar_one_or_none()

    def list_by_grupo_materia_periodo(
        self,
        db: Session,
        grupo_id: int,
        materia_id: int,
        periodo_id: int,
    ) -> list[Calificacion]:
        from app.models.inscripcion import Inscripcion
        stmt = (
            select(Calificacion)
            .join(Inscripcion, Calificacion.inscripcion_id == Inscripcion.id)
            .options(joinedload(Calificacion.inscripcion))
            .where(
                Inscripcion.grupo_id == grupo_id,
                Calificacion.materia_id == materia_id,
                Calificacion.periodo_id == periodo_id,
                Calificacion.deleted_at.is_(None),
            )
        )
        return list(db.execute(stmt).scalars().all())

    def list_by_inscripcion(
        self, db: Session, inscripcion_id: int
    ) -> list[Calificacion]:
        stmt = select(Calificacion).where(
            Calificacion.inscripcion_id == inscripcion_id,
            Calificacion.deleted_at.is_(None),
        )
        return list(db.execute(stmt).scalars().all())

    def cambiar_estado(
        self, db: Session, calificacion: Calificacion, nuevo_estado: EstadoCalificacion
    ) -> Calificacion:
        calificacion.estado = nuevo_estado
        db.add(calificacion)
        db.commit()
        db.refresh(calificacion)
        return calificacion

    def promedio_alumno_materia(
        self, db: Session, inscripcion_id: int, materia_id: int
    ) -> Decimal | None:
        from sqlalchemy import func
        stmt = select(func.avg(Calificacion.valor)).where(
            Calificacion.inscripcion_id == inscripcion_id,
            Calificacion.materia_id == materia_id,
            Calificacion.deleted_at.is_(None),
            Calificacion.estado == EstadoCalificacion.PUBLICADA,
        )
        valor = db.execute(stmt).scalar_one()
        return Decimal(valor).quantize(Decimal("0.01")) if valor is not None else None


calificacion = CRUDCalificacion(Calificacion)