from sqlalchemy import select
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.persona import Persona
from app.schemas.persona import PersonaCreate, PersonaUpdate


class CRUDPersona(CRUDBase[Persona, PersonaCreate, PersonaUpdate]):
    def get_by_email(self, db: Session, email: str) -> Persona | None:
        stmt = select(Persona).where(
            Persona.email == email, Persona.deleted_at.is_(None)
        )
        return db.execute(stmt).scalar_one_or_none()

    def get_by_curp(self, db: Session, curp: str) -> Persona | None:
        stmt = select(Persona).where(Persona.curp == curp, Persona.deleted_at.is_(None))
        return db.execute(stmt).scalar_one_or_none()

    def search(self, db: Session, termino: str, skip: int = 0, limit: int = 20):
        like = f"%{termino}%"
        stmt = (
            select(Persona)
            .where(Persona.deleted_at.is_(None))
            .where(
                Persona.nombres.ilike(like)
                | Persona.apellido_paterno.ilike(like)
                | Persona.apellido_materno.ilike(like)
                | Persona.email.ilike(like)
            )
            .offset(skip)
            .limit(limit)
        )
        return list(db.execute(stmt).scalars().all())


persona = CRUDPersona(Persona)
