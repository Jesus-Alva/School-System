from sqlalchemy import ForeignKey, Enum as SAEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.enum import RolDocente


class AsignacionDocente(Base, TimestampMixin):
    __tablename__ = "asignacion_docente"
    __table_args__ = (
        # Un grupo solo puede tener UN titular por materia en el ciclo
        UniqueConstraint(
            "grupo_id", "materia_id", "ciclo_id", name="uq_grupo_materia_ciclo"
        ),
        # Evita duplicar la misma asignación
        UniqueConstraint(
            "docente_id",
            "grupo_id",
            "materia_id",
            "ciclo_id",
            name="uq_docente_grupo_materia_ciclo",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    docente_id: Mapped[int] = mapped_column(ForeignKey("docente.id"))
    materia_id: Mapped[int] = mapped_column(ForeignKey("materia.id"))
    grupo_id: Mapped[int] = mapped_column(ForeignKey("grupo.id"))
    ciclo_id: Mapped[int] = mapped_column(ForeignKey("ciclo_escolar.id"))
    rol_docente: Mapped[RolDocente] = mapped_column(
        SAEnum(RolDocente), default=RolDocente.TITULAR
    )

    docente: Mapped["Docente"] = relationship(back_populates="asignaciones")
    materia: Mapped["Materia"] = relationship(back_populates="asignaciones")
    grupo: Mapped["Grupo"] = relationship(back_populates="asignaciones")
    ciclo: Mapped["CicloEscolar"] = relationship(back_populates="asignaciones")
