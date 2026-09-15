from sqlalchemy import select
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.enum import RolUsuario, EstadoUsuario


class CRUDUsuario(CRUDBase[Usuario, UsuarioCreate, UsuarioUpdate]):
    def get_by_email(self, db: Session, email: str) -> Usuario | None:
        stmt = select(Usuario).where(
            Usuario.email == email, Usuario.deleted_at.is_(None)
        )
        return db.execute(stmt).scalar_one_or_none()

    def get_by_persona(self, db: Session, persona_id: int) -> Usuario | None:
        stmt = select(Usuario).where(
            Usuario.persona_id == persona_id, Usuario.deleted_at.is_(None)
        )
        return db.execute(stmt).scalar_one_or_none()

    def list_by_rol(
        self, db: Session, rol: RolUsuario, skip: int = 0, limit: int = 100
    ) -> list[Usuario]:
        stmt = (
            select(Usuario)
            .where(Usuario.rol == rol, Usuario.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
        )
        return list(db.execute(stmt).scalars().all())

    def activar(self, db: Session, usuario: Usuario) -> Usuario:
        usuario.estado = EstadoUsuario.ACTIVO
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    def bloquear(self, db: Session, usuario: Usuario) -> Usuario:
        usuario.estado = EstadoUsuario.BLOQUEADO
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario


usuario = CRUDUsuario(Usuario)