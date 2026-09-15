from sqlalchemy import String, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.enum import EstadoDocente


class Docente(Base, TimestampMixin):
    __tablename__ = "docente"

    id: Mapped[int] = mapped_column(primary_key=True)
    persona_id: Mapped[int] = mapped_column(ForeignKey("persona.id"), unique=True)
    # Regla: un docente solo imparte UNA materia
    materia_principal_id: Mapped[int] = mapped_column(
        ForeignKey("materia.id"), unique=True, nullable=False
    )
    especialidad: Mapped[str | None] = mapped_column(String(150))
    cedula_profesional: Mapped[str | None] = mapped_column(String(50))
    estado: Mapped[EstadoDocente] = mapped_column(
        SAEnum(EstadoDocente), default=EstadoDocente.ACTIVO
    )

    persona: Mapped["Persona"] = relationship(back_populates="docente")
    materia_principal: Mapped["Materia"] = relationship(back_populates="docentes")
    asignaciones: Mapped[list["AsignacionDocente"]] = relationship(back_populates="docente")
    horarios: Mapped[list["Horario"]] = relationship(back_populates="docente")