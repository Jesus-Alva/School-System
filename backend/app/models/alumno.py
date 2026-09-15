from datetime import date
from sqlalchemy import String, Date, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.enum import EstadoAlumno, NivelEducativo


class Alumno(Base, TimestampMixin):
    __tablename__ = "alumno"

    id: Mapped[int] = mapped_column(primary_key=True)
    persona_id: Mapped[int] = mapped_column(ForeignKey("persona.id"), unique=True)
    matricula: Mapped[date | None] = mapped_column(Date)
    fecha_ingreso: Mapped[EstadoAlumno] = mapped_column(
        SAEnum(EstadoAlumno), default=EstadoAlumno.ACTIVO
    )
    nivel_actual: Mapped[NivelEducativo | None] = mapped_column(SAEnum(NivelEducativo))

    persona: Mapped["Persona"] = relationship(back_populates="alumno")
    inscripciones: Mapped[list["Inscripciones"]] = relationship(back_populates="alumno")
    tutores: Mapped[list["TutorAlumno"]] = relationship(back_populates="alumno")