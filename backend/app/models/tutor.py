from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class Tutor(Base, TimestampMixin):
    __tablename__ = "tutor"

    id: Mapped[int] = mapped_column(primary_key=True)
    persona_id: Mapped[int] = mapped_column(ForeignKey("persona.id"), unique=True)
    parentesco: Mapped[str] = mapped_column(String(50), nullable=False)
    ocupacion: Mapped[str | None] = mapped_column(String(120))

    persona: Mapped["Persona"] = relationship(back_populates="tutores")
    alumnos: Mapped[list["TutorAlumno"]] = relationship(back_populates="tutor")