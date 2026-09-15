from sqlalchemy import Integer, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class PlanEstudio(Base, TimestampMixin):
    __tablename__ = "plan_estudio"
    __table_args__ = (
        UniqueConstraint("grado_id", "materia_id", name="uq_plan_grado_materia"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    grado_id: Mapped[int] = mapped_column(ForeignKey("grado.id"))
    materia_id: Mapped[int] = mapped_column(ForeignKey("materia.id"))
    horas_semana: Mapped[int] = mapped_column(Integer, default=0)
    obligatoria: Mapped[bool] = mapped_column(Boolean, default=True)

    grado: Mapped["Grado"] = relationship(back_populates="plan_estudios")
    materia: Mapped["Materia"] = relationship(back_populates="planes")