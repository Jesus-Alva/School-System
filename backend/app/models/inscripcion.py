from datetime import date
from sqlalchemy import Date, ForeignKey, Enum as SAEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.enum import EstadoInscripcion


class Inscripcion(Base, TimestampMixin):
    __tablename__ = "inscripcion"
    __table_args__ = (
        UniqueConstraint("alumno_id", "ciclo_id", name="uq_alumno_ciclo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    alumno_id: Mapped[int] = mapped_column(ForeignKey("alumno.id"))
    grupo_id: Mapped[int] = mapped_column(ForeignKey("grupo.id"))
    ciclo_id: Mapped[int] = mapped_column(ForeignKey("ciclo_escolar.id"))
    fecha_inscripcion: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[EstadoInscripcion] = mapped_column(
        SAEnum(EstadoInscripcion), default=EstadoInscripcion.ACTIVO
    )

    alumno: Mapped["Alumno"] = relationship(back_populates="inscripciones")
    grupo: Mapped["Grupo"] = relationship(back_populates="inscripciones")
    ciclo: Mapped["CicloEscolar"] = relationship(back_populates="inscripciones")
    calificaciones: Mapped[list["Calificacion"]] = relationship(
        back_populates="inscripcion"
    )
    asistencias: Mapped[list["Asistencia"]] = relationship(back_populates="inscripcion")
    boletas: Mapped[list["Boleta"]] = relationship(back_populates="inscripcion")
