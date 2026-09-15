from sqlalchemy import Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class TutorAlumno(Base, TimestampMixin):
    __tablename__ = "tutor_alumno"
    __table_args__ = (UniqueConstraint("tutor_id", "alumno_id", name="uq_tutor_alumno"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    tutor_id: Mapped[int] = mapped_column(ForeignKey("tutor.id"))
    alumno_id: Mapped[int] = mapped_column(ForeignKey("alumno.id"))
    es_principal: Mapped[bool] = mapped_column(Boolean, default=False)

    tutor: Mapped["Tutor"] = relationship(back_populates="alumnos")
    alumno: Mapped["Alumno"] = relationship(back_populates="tutores")