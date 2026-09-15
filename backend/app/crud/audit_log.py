from sqlalchemy import select
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.audit_log import AuditLog
from app.schemas.audit_log import AuditLogCreate


class CRUDAuditLog(CRUDBase[AuditLog, AuditLogCreate, AuditLogCreate]):
    def registrar(
        self,
        db: Session,
        usuario_id: int | None,
        accion: str,
        entidad: str,
        entidad_id: int | None = None,
        datos_antes: dict | None = None,
        datos_despues: dict | None = None,
        ip: str | None = None,
    ) -> AuditLog:
        obj = AuditLog(
            usuario_id=usuario_id,
            accion=accion,
            entidad=entidad,
            entidad_id=entidad_id,
            datos_antes=datos_antes,
            datos_despues=datos_despues,
            ip=ip,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def list_by_entidad(
        self, db: Session, entidad: str, entidad_id: int, limit: int = 50
    ) -> list[AuditLog]:
        stmt = (
            select(AuditLog)
            .where(AuditLog.entidad == entidad, AuditLog.entidad_id == entidad_id)
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
        )
        return list(db.execute(stmt).scalars().all())


audit_log = CRUDAuditLog(AuditLog)