from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class Grupo(Base, TimestampMixin):
    __tablename__ = "grupo"
    __table_args__ = (
        UniqueConstraint("grado_id", "ciclo_id", "nombre", name="uq_grupo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    grado_id: Mapped[int] = mapped_column(ForeignKey("grado.id"))
    ciclo_id: Mapped[int] = mapped_column(ForeignKey("ciclo_escolar.id"))
    nombre: Mapped[str] = mapped_column(String(10), nullable=False)
    capacidad: Mapped[int] = mapped_column(Integer, default=30)
    salon_id: Mapped[int | None] = mapped_column(ForeignKey("salon.id"))

    grado: Mapped["Grado"] = relationship(back_populates="grupos")
    ciclo: Mapped["CicloEscolar"] = relationship(back_populates="grupos")
    salon: Mapped["Salon"] = relationship(back_populates="grupos")
    inscripciones: Mapped[list["Inscripcion"]] = relationship(back_populates="grupo")
    asignaciones: Mapped[list["AsignacionDocente"]] = relationship(back_populates="grupo")
    horarios: Mapped[list["Horario"]] = relationship(back_populates="grupo")