from sqlalchemy import select, update
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.ciclo_escolar import CicloEscolar
from app.schemas.ciclo_escolar import CicloEscolarCreate, CicloEscolarUpdate


class CRUDCicloEscolar(CRUDBase[CicloEscolar, CicloEscolarCreate, CicloEscolarUpdate]):
    def get_activo(self, db: Session) -> CicloEscolar | None:
        stmt = select(CicloEscolar).where(
            CicloEscolar.activo.is_(True), CicloEscolar.deleted_at.is_(None)
        )
        return db.execute(stmt).scalar_one_or_none()

    def activar(self, db: Session, ciclo_id: int) -> CicloEscolar:
        # Desactiva cualquier otro
        db.execute(update(CicloEscolar).values(activo=False))
        db.commit()
        ciclo = self.get(db, ciclo_id)
        if not ciclo:
            raise ValueError("Ciclo no encontrado")
        ciclo.activo = True
        db.add(ciclo)
        db.commit()
        db.refresh(ciclo)
        return ciclo


ciclo_escolar = CRUDCicloEscolar(CicloEscolar)