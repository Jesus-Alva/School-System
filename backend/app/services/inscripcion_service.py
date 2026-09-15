from datetime import date
from sqlalchemy.orm import Session
from app.core.exceptions import BadRequestError, ConflictError, NotFoundError
from app.crud import (
    inscripcion as crud_inscripcion,
    alumno as crud_alumno,
    grupo as crud_grupo,
    ciclo_escolar as crud_ciclo,
)
from app.enum import EstadoInscripcion
from app.models.inscripcion import Inscripcion
from app.schemas.inscripcion import InscripcionCreate, InscripcionUpdate


def inscribir(db: Session, payload: InscripcionCreate) -> Inscripcion:
    alumno = crud_alumno.get(db, payload.alumno_id)
    if not alumno:
        raise NotFoundError("Alumno no encontrado")

    grupo = crud_grupo.get(db, payload.grupo_id)
    if not grupo:
        raise NotFoundError("Grupo no encontrado")

    ciclo = crud_ciclo.get(db, payload.ciclo_id)
    if not ciclo:
        raise NotFoundError("Ciclo escolar no encontrado")

    if grupo.ciclo_id != payload.ciclo_id:
        raise BadRequestError("El grupo no pertenece a ese ciclo")

    # Un alumno solo puede estar en un grupo por ciclo
    existente = crud_inscripcion.get_by_alumno_ciclo(
        db, payload.alumno_id, payload.ciclo_id
    )
    if existente:
        raise ConflictError("El alumno ya está inscrito en este ciclo")

    # Validar capacidad del grupo
    inscritos = crud_inscripcion.contar_en_grupo(db, payload.grupo_id)
    if inscritos >= grupo.capacidad:
        raise ConflictError(
            f"El grupo {grupo.nombre} está lleno ({inscritos}/{grupo.capacidad})"
        )

    return crud_inscripcion.create(db, payload)


def cambiar_grupo(db: Session, inscripcion_id: int, nuevo_grupo_id: int) -> Inscripcion:
    inscripcion = crud_inscripcion.get(db, inscripcion_id)
    if not inscripcion:
        raise NotFoundError("Inscripción no encontrada")

    nuevo_grupo = crud_grupo.get(db, nuevo_grupo_id)
    if not nuevo_grupo:
        raise NotFoundError("Grupo destino no encontrado")

    if nuevo_grupo.ciclo_id != inscripcion.ciclo_id:
        raise BadRequestError("El grupo destino no pertenece al ciclo")

    inscritos = crud_inscripcion.contar_en_grupo(db, nuevo_grupo_id)
    if inscritos >= nuevo_grupo.capacidad:
        raise ConflictError("El grupo destino está lleno")

    return crud_inscripcion.update(
        db, inscripcion, InscripcionUpdate(grupo_id=nuevo_grupo_id)
    )


def dar_de_baja(db: Session, inscripcion_id: int) -> Inscripcion:
    inscripcion = crud_inscripcion.get(db, inscripcion_id)
    if not inscripcion:
        raise NotFoundError("Inscripción no encontrada")
    return crud_inscripcion.update(
        db, inscripcion, InscripcionUpdate(estado=EstadoInscripcion.BAJA)
    )


def listar_por_grupo(db: Session, grupo_id: int) -> list[Inscripcion]:
    return crud_inscripcion.list_by_grupo(db, grupo_id)
