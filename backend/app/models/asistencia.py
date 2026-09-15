from datetime import date
from sqlalchemy import Date, Text, ForeignKey, Enum as SAEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.enum import EstadoAsistencia


class Asistencia(Base, TimestampMixin):
    __tablename__ = "asistencia"
    __table_args__ = (
        UniqueConstraint("inscripcion_id", "fecha", name="uq_asistencia_dia"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    inscripcion_id: Mapped[int] = mapped_column(ForeignKey("inscripcion.id"))
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[EstadoAsistencia] = mapped_column(SAEnum(EstadoAsistencia))
    justificacion: Mapped[str | None] = mapped_column(Text)
    registrado_por: Mapped[int] = mapped_column(ForeignKey("docente.id"))

    inscripcion: Mapped["Inscripcion"] = relationship(back_populates="asistencias")
