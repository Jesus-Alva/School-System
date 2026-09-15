from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AuditLogBase(BaseModel):
    accion: str
    entidad: str
    entidad_id: int | None = None
    datos_antes: dict | None = None
    datos_despues: dict | None = None
    ip: str | None = None


class AuditLogCreate(AuditLogBase):
    usuario_id: int | None = None


class AuditLogRead(AuditLogBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    usuario_id: int | None
    created_at: datetime