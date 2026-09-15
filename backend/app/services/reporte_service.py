from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.calificacion import Calificacion
from app.models.inscripcion import Inscripcion
from app.models.materia import Materia
from app.enum import EstadoCalificacion


def promedio_por_grupo_materia(
    db: Session, grupo_id: int, materia_id: int
) -> dict:
    stmt = (
        select(
            func.avg(Calificacion.valor).label("promedio"),
            func.count(Calificacion.id).label("total"),
            func.min(Calificacion.valor).label("minimo"),
            func.max(Calificacion.valor).label("maximo"),
        )
        .join(Inscripcion, Calificacion.inscripcion_id == Inscripcion.id)
        .where(
            Inscripcion.grupo_id == grupo_id,
            Calificacion.materia_id == materia_id,
            Calificacion.deleted_at.is_(None),
        )
    )
    row = db.execute(stmt).one()
    return {
        "promedio": float(row.promedio) if row.promedio else None,
        "total_calificaciones": row.total,
        "minimo": float(row.minimo) if row.minimo else None,
        "maximo": float(row.maximo) if row.maximo else None,
    }


def aprobados_reprobados(
    db: Session, grupo_id: int, materia_id: int, minimo_aprobatorio: float = 6.0
) -> dict:
    aprobados = db.execute(
        select(func.count())
        .select_from(Calificacion)
        .join(Inscripcion, Calificacion.inscripcion_id == Inscripcion.id)
        .where(
            Inscripcion.grupo_id == grupo_id,
            Calificacion.materia_id == materia_id,
            Calificacion.valor >= minimo_aprobatorio,
            Calificacion.deleted_at.is_(None),
        )
    ).scalar_one()

    reprobados = db.execute(
        select(func.count())
        .select_from(Calificacion)
        .join(Inscripcion, Calificacion.inscripcion_id == Inscripcion.id)
        .where(
            Inscripcion.grupo_id == grupo_id,
            Calificacion.materia_id == materia_id,
            Calificacion.valor < minimo_aprobatorio,
            Calificacion.deleted_at.is_(None),
        )
    ).scalar_one()

    return {"aprobados": aprobados, "reprobados": reprobados}


def concentrado_grupo(db: Session, grupo_id: int) -> list[dict]:
    """Promedio por materia de un grupo."""
    stmt = (
        select(
            Materia.id,
            Materia.nombre,
            func.avg(Calificacion.valor).label("promedio"),
        )
        .join(Calificacion, Calificacion.materia_id == Materia.id)
        .join(Inscripcion, Calificacion.inscripcion_id == Inscripcion.id)
        .where(
            Inscripcion.grupo_id == grupo_id,
            Calificacion.deleted_at.is_(None),
        )
        .group_by(Materia.id, Materia.nombre)
    )
    return [
        {"materia_id": r.id, "materia": r.nombre, "promedio": float(r.promedio or 0)}
        for r in db.execute(stmt).all()
    ]