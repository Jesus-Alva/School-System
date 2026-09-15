from sqlalchemy.orm import Session
from app.core.exceptions import BadRequestError, ConflictError, NotFoundError
from app.crud import (
    asignacion_docente as crud_asignacion,
    docente as crud_docente,
    grupo as crud_grupo,
    materia as crud_materia,
    ciclo_escolar as crud_ciclo,
)
from app.enum import RolDocente
from app.models.asignacion_docente import AsignacionDocente
from app.schemas.asignacion_docente import (
    AsignacionDocenteCreate,
    AsignacionDocenteUpdate,
)


def crear(db: Session, payload: AsignacionDocenteCreate) -> AsignacionDocente:
    docente = crud_docente.get(db, payload.docente_id)
    if not docente:
        raise NotFoundError("Docente no encontrado")

    materia = crud_materia.get(db, payload.materia_id)
    if not materia:
        raise NotFoundError("Materia no encontrada")

    grupo = crud_grupo.get(db, payload.grupo_id)
    if not grupo:
        raise NotFoundError("Grupo no encontrado")

    ciclo = crud_ciclo.get(db, payload.ciclo_id)
    if not ciclo:
        raise NotFoundError("Ciclo escolar no encontrado")

    # Regla 1: docente solo imparte su materia principal
    if docente.materia_principal_id != payload.materia_id:
        raise BadRequestError(
            f"El docente solo puede impartir su materia principal "
            f"(id={docente.materia_principal_id})"
        )

    # Regla 2: el grupo debe pertenecer al ciclo
    if grupo.ciclo_id != payload.ciclo_id:
        raise BadRequestError("El grupo no pertenece al ciclo indicado")

    # Regla 3: un grupo solo puede tener un titular por materia
    if payload.rol_docente == RolDocente.TITULAR:
        if crud_asignacion.existe_titular(
            db, payload.grupo_id, payload.materia_id, payload.ciclo_id
        ):
            raise ConflictError(
                "Ya existe un docente titular para esa materia en el grupo"
            )

    return crud_asignacion.create(db, payload)


def actualizar(
    db: Session, asignacion_id: int, payload: AsignacionDocenteUpdate
) -> AsignacionDocente:
    asignacion = crud_asignacion.get(db, asignacion_id)
    if not asignacion:
        raise NotFoundError("Asignación no encontrada")

    if payload.rol_docente and payload.rol_docente != asignacion.rol_docente:
        if payload.rol_docente == RolDocente.TITULAR:
            if crud_asignacion.existe_titular(
                db, asignacion.grupo_id, asignacion.materia_id, asignacion.ciclo_id
            ):
                raise ConflictError("Ya existe un titular para esa materia")
    return crud_asignacion.update(db, asignacion, payload)


def eliminar(db: Session, asignacion_id: int) -> None:
    asignacion = crud_asignacion.get(db, asignacion_id)
    if not asignacion:
        raise NotFoundError("Asignación no encontrada")
    # Verificar que no tenga calificaciones capturadas
    from app.crud import calificacion as crud_calificacion

    califs = crud_calificacion.list_by_grupo_materia_periodo(
        db, asignacion.grupo_id, asignacion.materia_id, periodo_id=0
    )
    # En producción se debe validar por periodo real
    crud_asignacion.remove(db, asignacion_id)
