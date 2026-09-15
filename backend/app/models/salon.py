from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class Salon(Base, TimestampMixin):
    __tablename__ = "salon"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    capacidad: Mapped[int] = mapped_column(Integer, default=30)
    ubicacion: Mapped[str | None] = mapped_column(String(150))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    grupos: Mapped[list["Grupo"]] = relationship(back_populates="salon")
    horarios: Mapped[list["Horario"]] = relationship(back_populates="salon")
