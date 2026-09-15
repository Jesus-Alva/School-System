from datetime import date
from sqlalchemy import String, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class CicloEscolar(Base, TimestampMixin):
    __tablename__ = "ciclo_escolar"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[date] = mapped_column(Date, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=False)

    grados: Mapped[list["Grado"]] = relationship(back_populates="ciclo")
    grupos: Mapped[list["Grupo"]] = relationship(back_populates="ciclo")
    inscripciones: Mapped[list["Inscripcion"]] = relationship(back_populates="ciclo")
    asignaciones: Mapped[list["AsignacionDocente"]] = relationship(
        back_populates="ciclo"
    )
    periodos: Mapped[list["PeriodoEvaluacion"]] = relationship(back_populates="ciclo")
    horarios: Mapped[list["Horario"]] = relationship(back_populates="ciclo")
    boletas: Mapped[list["Boleta"]] = relationship(back_populates="ciclo")
