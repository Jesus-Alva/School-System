from decimal import Decimal
from sqlalchemy import Numeric, Text, ForeignKey, Enum as SAEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.enum import EstadoCalificacion


class Calificacion(Base, TimestampMixin):
    __tablename__ = "calificacion"
    __table_args__ = (
        UniqueConstraint(
            "inscripcion_id",
            "materia_id",
            "periodo_id",
            name="uq_calificacion_insc_materia_periodo",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    inscripcion_id: Mapped[int] = mapped_column(ForeignKey("inscripcion.id"))
    materia_id: Mapped[int] = mapped_column(ForeignKey("materia.id"))
    periodo_id: Mapped[int] = mapped_column(ForeignKey("periodo_evaluacion.id"))
    valor: Mapped[Decimal] = mapped_column(Numeric(4, 2), nullable=False)
    observaciones: Mapped[str | None] = mapped_column(Text)
    capturado_por: Mapped[int] = mapped_column(ForeignKey("docente.id"))
    estado: Mapped[EstadoCalificacion] = mapped_column(
        SAEnum(EstadoCalificacion), default=EstadoCalificacion.BORRADOR
    )

    inscripcion: Mapped["Inscripcion"] = relationship(back_populates="calificaciones")
    materia: Mapped["Materia"] = relationship(back_populates="calificaciones")
    periodo: Mapped["PeriodoEvaluacion"] = relationship(back_populates="calificaciones")
    docente: Mapped["Docente"] = relationship()
