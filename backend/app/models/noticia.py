from datetime import datetime
from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class Noticia(Base, TimestampMixin):
    __tablename__ = "noticia"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(220), unique=True, nullable=False)
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    imagen_url: Mapped[str | None] = mapped_column(String(500))
    publicado: Mapped[bool] = mapped_column(Boolean, default=False)
    fecha_publicacion: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    autor_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"))

    autor: Mapped["Usuario"] = relationship(back_populates="noticias")
