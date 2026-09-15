from sqlalchemy import String, Integer, ForeignKey, Enum as SAEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.enum import NivelEducativo


class Grado(Base, TimestampMixin):
    __tablename__ = "grado"
    __table_args__ = (
        UniqueConstraint("ciclo_id", "nivel", "nombre", name="uq_grado_ciclo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    ciclo_id: Mapped[int] = mapped_column(ForeignKey("ciclo_escolar.id"))
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    nivel: Mapped[NivelEducativo] = mapped_column(
        SAEnum(NivelEducativo), nullable=False
    )
    orden: Mapped[int] = mapped_column(Integer, default=0)

    ciclo: Mapped["CicloEscolar"] = relationship(back_populates="grados")
    grupos: Mapped[list["Grupo"]] = relationship(back_populates="grado")
    plan_estudios: Mapped[list["PlanEstudio"]] = relationship(back_populates="grado")
