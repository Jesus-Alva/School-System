# app/crud/aviso.py
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.aviso import Aviso
from app.schemas.aviso import AvisoCreate, AvisoUpdate
from app.enum import AlcanceAviso, RolUsuario


class CRUDAviso(CRUDBase[Aviso, AvisoCreate, AvisoUpdate]):
    def list_para_usuario(
        self,
        db: Session,
        rol: RolUsuario,
        grupo_id: int | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Aviso]:
        condiciones = [
            Aviso.alcance == AlcanceAviso.GENERAL,
            (Aviso.alcance == AlcanceAviso.ROL) & (Aviso.rol_destino == rol),
        ]
        if grupo_id:
            condiciones.append(
                (Aviso.alcance == AlcanceAviso.GRUPO) & (Aviso.grupo_id == grupo_id)
            )
        stmt = (
            select(Aviso)
            .where(Aviso.deleted_at.is_(None), or_(*condiciones))
            .order_by(Aviso.fecha_publicacion.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(db.execute(stmt).scalars().all())


aviso = CRUDAviso(Aviso)