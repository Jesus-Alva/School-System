from sqlalchemy import select, and_, or_
from sqlalchemy.orm import Session, joinedload
from app.crud.base import CRUDBase
from app.models.horario import Horario
from app.schemas.horario import HorarioCreate, HorarioUpdate
from app.enum import DiaSemana


class CRUDHorario(CRUDBase[Horario, HorarioCreate, HorarioUpdate]):
    def list_by_grupo(self, db: Session, grupo_id: int) -> list[Horario]:
        stmt = (
            select(Horario)
            .options(
                joinedload(Horario.materia),
                joinedload(Horario.docente),
                joinedload(Horario.salon),
            )
            .where(Horario.grupo_id == grupo_id, Horario.deleted_at.is_(None))
            .order_by(Horario.dia_semana, Horario.hora_inicio)
        )
        return list(db.execute(stmt).scalars().all())

    def detectar_choque_docente(
        self,
        db: Session,
        docente_id: int,
        ciclo_id: int,
        dia: DiaSemana,
        hora_inicio,
        hora_fin,
        excluir_id: int | None = None,
    ) -> bool:
        stmt = select(Horario).where(
            Horario.docente_id == docente_id,
            Horario.ciclo_id == ciclo_id,
            Horario.dia_semana == dia,
            Horario.deleted_at.is_(None),
            or_(
                and_(Horario.hora_inicio < hora_fin, Horario.hora_fin > hora_inicio),
            ),
        )
        if excluir_id:
            stmt = stmt.where(Horario.id != excluir_id)
        return db.execute(stmt).scalar_one_or_none() is not None

    def detectar_choque_grupo(
        self,
        db: Session,
        grupo_id: int,
        dia: DiaSemana,
        hora_inicio,
        hora_fin,
        excluir_id: int | None = None,
    ) -> bool:
        stmt = select(Horario).where(
            Horario.grupo_id == grupo_id,
            Horario.dia_semana == dia,
            Horario.deleted_at.is_(None),
            Horario.hora_inicio < hora_fin,
            Horario.hora_fin > hora_inicio,
        )
        if excluir_id:
            stmt = stmt.where(Horario.id != excluir_id)
        return db.execute(stmt).scalar_one_or_none() is not None

    def detectar_choque_salon(
        self,
        db: Session,
        salon_id: int,
        dia: DiaSemana,
        hora_inicio,
        hora_fin,
        excluir_id: int | None = None,
    ) -> bool:
        stmt = select(Horario).where(
            Horario.salon_id == salon_id,
            Horario.dia_semana == dia,
            Horario.deleted_at.is_(None),
            Horario.hora_inicio < hora_fin,
            Horario.hora_fin > hora_inicio,
        )
        if excluir_id:
            stmt = stmt.where(Horario.id != excluir_id)
        return db.execute(stmt).scalar_one_or_none() is not None


horario = CRUDHorario(Horario)