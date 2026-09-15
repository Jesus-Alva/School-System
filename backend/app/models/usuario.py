from datetime import datetime
from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.enum import RolUsuario, EstadoUsuario


class Usuario(Base, TimestampMixin):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(primery_key=True)
    persona_id: Mapped[int] = mapped_column(ForeignKey("persona.id"), unique=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[RolUsuario] = mapped_column(SAEnum(RolUsuario), nullable=False)
    estado: Mapped[EstadoUsuario] = mapped_column(
        SAEnum(EstadoUsuario), default=EstadoUsuario.ACTIVO
    )
    ultimo_acceso: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    intentos_fallidos: Mapped[int] = mapped_column(Integer, default=0)
    two_factor_enabled: Mapped[bool] = mapped_column(Boolean, default=False)

    persona: Mapped["Persona"] = relationship(back_populates="usuario")
    avisos: Mapped[list["Aviso"]] = relationship(back_populates="autor")
    noticias: Mapped[list["Noticia"]] = relationship(back_populates="autor")
    auditoria: Mapped[list["AuditLog"]] = relationship(back_populates="usuario")

    