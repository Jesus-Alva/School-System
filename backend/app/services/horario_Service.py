from sqlalchemy.orm import Session
from app.core.exceptions import BadRequestError, ConflictError, NotFoundError
from app.crud import (
    horario as crud_horario,
    asignacion_docente as crud_asignacion,
    salon as crud_salon,
)
from app.models.horario import Horario
from app.schemas.horario import HorarioCreate, HorarioUpdate


def crear(db: Session, payload: HorarioCreate) -> Horario:
    # Validar que la asignación docente-materia-grupo exista
    asignacion = crud_asignacion.get_by(
        db,
        docente_id=payload.docente_id,
        materia_id=payload.materia_id,
        grupo_id=payload.grupo_id,
        ciclo_id=payload.ciclo_id,
    )
    if not asignacion:
        raise BadRequestError(
            "No existe asignación docente-materia-grupo para ese ciclo"
        )

    salon = crud_salon.get(db, payload.salon_id)
    if not salon:
        raise NotFoundError("Salón no encontrado")

    # Validar choques
    if crud_horario.detectar_choque_docente(
        db,
        payload.docente_id,
        payload.ciclo_id,
        payload.dia_semana,
        payload.hora_inicio,
        payload.hora_fin,
    ):
        raise ConflictError("El docente ya tiene clase en ese horario")

    if crud_horario.detectar_choque_grupo(
        db,
        payload.grupo_id,
        payload.dia_semana,
        payload.hora_inicio,
        payload.hora_fin,
    ):
        raise ConflictError("El grupo ya tiene clase en ese horario")

    if crud_horario.detectar_choque_salon(
        db,
        payload.salon_id,
        payload.dia_semana,
        payload.hora_inicio,
        payload.hora_fin,
    ):
        raise ConflictError("El salón ya está ocupado en ese horario")

    return crud_horario.create(db, payload)


def actualizar(db: Session, horario_id: int, payload: HorarioUpdate) -> Horario:
    horario = crud_horario.get(db, horario_id)
    if not horario:
        raise NotFoundError("Horario no encontrado")

    nueva_dia = payload.dia_semana or horario.dia_semana
    nueva_ini = payload.hora_inicio or horario.hora_inicio
    nueva_fin = payload.hora_fin or horario.hora_fin
    nuevo_salon = payload.salon_id or horario.salon_id

    if nueva_fin <= nueva_ini:
        raise BadRequestError("hora_fin debe ser posterior a hora_inicio")

    if crud_horario.detectar_choque_docente(
        db,
        horario.docente_id,
        horario.ciclo_id,
        nueva_dia,
        nueva_ini,
        nueva_fin,
        excluir_id=horario.id,
    ):
        raise ConflictError("Choque con el docente")

    if crud_horario.detectar_choque_grupo(
        db, horario.grupo_id, nueva_dia, nueva_ini, nueva_fin, excluir_id=horario.id
    ):
        raise ConflictError("Choque con el grupo")

    if crud_horario.detectar_choque_salon(
        db, nuevo_salon, nueva_dia, nueva_ini, nueva_fin, excluir_id=horario.id
    ):
        raise ConflictError("Choque con el salón")

    return crud_horario.update(db, horario, payload)


def eliminar(db: Session, horario_id: int) -> None:
    if not crud_horario.get(db, horario_id):
        raise NotFoundError("Horario no encontrado")
    crud_horario.remove(db, horario_id)
