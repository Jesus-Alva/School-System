from sqlalchemy import String, Integer, Boolean, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.enum import NivelEducativo


class Materia(Base, TimestampMixin):
    __tablename__ = "materia"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    clave: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    nivel: Mapped[NivelEducativo] = mapped_column(SAEnum(NivelEducativo), nullable=False)
    horas_semana: Mapped[int] = mapped_column(Integer, default=0)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    docentes: Mapped[list["Docente"]] = relationship(back_populates="materia_principal")
    planes: Mapped[list["PlanEstudio"]] = relationship(back_populates="materia")
    asignaciones: Mapped[list["AsignacionDocente"]] = relationship(back_populates="materia")
    calificaciones: Mapped[list["Calificacion"]] = relationship(back_populates="materia")
    horarios: Mapped[list["Horario"]] = relationship(back_populates="materia")