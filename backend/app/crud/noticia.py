# app/crud/noticia.py
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.noticia import Noticia
from app.schemas.noticia import NoticiaCreate, NoticiaUpdate


class CRUDNoticia(CRUDBase[Noticia, NoticiaCreate, NoticiaUpdate]):
    def get_by_slug(self, db: Session, slug: str) -> Noticia | None:
        stmt = select(Noticia).where(
            Noticia.slug == slug, Noticia.deleted_at.is_(None)
        )
        return db.execute(stmt).scalar_one_or_none()

    def list_publicadas(self, db: Session, skip: int = 0, limit: int = 20):
        stmt = (
            select(Noticia)
            .where(Noticia.publicado.is_(True), Noticia.deleted_at.is_(None))
            .order_by(Noticia.fecha_publicacion.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(db.execute(stmt).scalars().all())


noticia = CRUDNoticia(Noticia)