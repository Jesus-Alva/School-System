from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.enum import AlcanceAviso, RolUsuario


class Aviso(Base, TimestampMixin):
    __tablename__ = "aviso"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    alcance: Mapped[AlcanceAviso] = mapped_column(SAEnum(AlcanceAviso))
    rol_destino: Mapped[RolUsuario | None] = mapped_column(SAEnum(RolUsuario))
    grupo_id: Mapped[int | None] = mapped_column(ForeignKey("grupo.id"))
    materia_id: Mapped[int | None] = mapped_column(ForeignKey("materia.id"))
    autor_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"))
    fecha_publicacion: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expira_en: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    autor: Mapped["Usuario"] = relationship(back_populates="avisos")
