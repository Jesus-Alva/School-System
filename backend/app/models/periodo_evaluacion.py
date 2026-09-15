from datetime import date
from sqlalchemy import String, Integer, Date, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class PeriodoEvaluacion(Base, TimestampMixin):
    __tablename__ = "periodo_evaluacion"
    __table_args__ = (
        UniqueConstraint("ciclo_id", "orden", name="uq_periodo_ciclo_orden"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    ciclo_id: Mapped[int] = mapped_column(ForeignKey("ciclo_escolar.id"))
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    orden: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[date] = mapped_column(Date, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    ciclo: Mapped["CicloEscolar"] = relationship(back_populates="periodos")
    calificaciones: Mapped[list["Calificacion"]] = relationship(
        back_populates="periodo"
    )
