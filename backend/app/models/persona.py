from datetime import date
from sqlalchemy import String, Date, Text, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.enum import Sexo


class Persona(Base, TimestampMixin):
    __tablename__ = "persona"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombres: Mapped[str] = mapped_column(String(120), nullable=False)
    apellido_paterno: Mapped[str] = mapped_column(String(120), nullable=False)
    apellido_materno: Mapped[str | None] = mapped_column(String(120))
    fecha_nacimiento: Mapped[date | None] = mapped_column(Date)
    curp: Mapped[str | None] = mapped_column(String(18), unique=True)
    sexo: Mapped[Sexo | None] = mapped_column(SAEnum(Sexo))
    telefono: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    direccion: Mapped[str | None] = mapped_column(Text)
    foto_url: Mapped[str | None] = mapped_column(String(500))

    usuario: Mapped["Usuario"] = relationship(back_populates="persona", uselist=False)
    alumno: Mapped["Alumno"] = relationship(back_populates="persona", uselist=False)
    docente: Mapped["Docente"] = relationship(back_populates="persona", uselist=False)
    directivo: Mapped["Directivo"] = relationship(
        back_populates="persona", uselist=False
    )
    tutores: Mapped[list["Tutor"]] = relationship(back_populates="persona")
