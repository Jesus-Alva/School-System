from sqlalchemy import select
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.boleta import Boleta
from app.schemas.boleta import BoletaCreate, BoletaUpdate


class CRUDBoleta(CRUDBase[Boleta, BoletaCreate, BoletaUpdate]):
    def get_by_folio(self, db: Session, folio: str) -> Boleta | None:
        stmt = select(Boleta).where(
            Boleta.folio == folio, Boleta.deleted_at.is_(None)
        )
        return db.execute(stmt).scalar_one_or_none()

    def get_by_inscripcion_ciclo(
        self, db: Session, inscripcion_id: int, ciclo_id: int
    ) -> Boleta | None:
        stmt = select(Boleta).where(
            Boleta.inscripcion_id == inscripcion_id,
            Boleta.ciclo_id == ciclo_id,
            Boleta.deleted_at.is_(None),
        )
        return db.execute(stmt).scalar_one_or_none()

    def publicar(self, db: Session, boleta: Boleta) -> Boleta:
        boleta.publicada = True
        db.add(boleta)
        db.commit()
        db.refresh(boleta)
        return boleta


boleta = CRUDBoleta(Boleta)