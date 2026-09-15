from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class Boleta(Base, TimestampMixin):
    __tablename__ = "boleta"

    id: Mapped[int] = mapped_column(primary_key=True)
    inscripcion_id: Mapped[int] = mapped_column(ForeignKey("inscripcion.id"))
    ciclo_id: Mapped[int] = mapped_column(ForeignKey("ciclo_escolar.id"))
    folio: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    pdf_url: Mapped[str | None] = mapped_column(String(500))
    publicada: Mapped[bool] = mapped_column(Boolean, default=False)
    generada_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    inscripcion: Mapped["Inscripcion"] = relationship(back_populates="boletas")
    ciclo: Mapped["CicloEscolar"] = relationship(back_populates="boletas")
