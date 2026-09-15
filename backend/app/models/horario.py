from datetime import time
from sqlalchemy import Time, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.enum import DiaSemana


class Horario(Base, TimestampMixin):
    __tablename__ = "horario"

    id: Mapped[int] = mapped_column(primary_key=True)
    grupo_id: Mapped[int] = mapped_column(ForeignKey("grupo.id"))
    materia_id: Mapped[int] = mapped_column(ForeignKey("materia.id"))
    docente_id: Mapped[int] = mapped_column(ForeignKey("docente.id"))
    salon_id: Mapped[int] = mapped_column(ForeignKey("salon.id"))
    ciclo_id: Mapped[int] = mapped_column(ForeignKey("ciclo_escolar.id"))
    dia_semana: Mapped[DiaSemana] = mapped_column(SAEnum(DiaSemana))
    hora_inicio: Mapped[time] = mapped_column(Time)
    hora_fin: Mapped[time] = mapped_column(Time)

    grupo: Mapped["Grupo"] = relationship(back_populates="horarios")
    materia: Mapped["Materia"] = relationship(back_populates="horarios")
    docente: Mapped["Docente"] = relationship(back_populates="horarios")
    salon: Mapped["Salon"] = relationship(back_populates="horarios")
    ciclo: Mapped["CicloEscolar"] = relationship(back_populates="horarios")
