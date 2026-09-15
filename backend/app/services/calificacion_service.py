from decimal import Decimal
from sqlalchemy.orm import Session
from app.core.exceptions import (
    ForbiddenError,
    BadRequestError,
    ConflictError,
    NotFoundError,
)
from app.crud import (
    calificacion as crud_calificacion,
    asignacion_docente as crud_asignacion,
    docente as crud_docente,
    inscripcion as crud_inscripcion,
    periodo_evaluacion as crud_periodo,
)
from app.enum import EstadoCalificacion, RolUsuario
from app.models.calificacion import Calificacion
from app.models.usuario import Usuario
from app.schemas.calificacion import (
    CalificacionCreate,
    CalificacionUpdate,
    CalificacionMasiva,
)

# Transiciones permitidas de estado
TRANSICIONES = {
    EstadoCalificacion.BORRADOR: {EstadoCalificacion.ENVIADA},
    EstadoCalificacion.ENVIADA: {
        EstadoCalificacion.BLOQUEADA,
        EstadoCalificacion.BORRADOR,
    },
    EstadoCalificacion.BLOQUEADA: {
        EstadoCalificacion.PUBLICADA,
        EstadoCalificacion.BORRADOR,
    },
    EstadoCalificacion.PUBLICADA: set(),
}


def _validar_docente_asignado(
    db: Session, usuario: Usuario, materia_id: int, inscripcion_id: int
) -> None:
    """Verifica que el docente imparta esa materia en el grupo del alumno."""
    if usuario.rol != RolUsuario.DOCENTE:
        raise ForbiddenError("Solo docentes pueden capturar calificaciones")

    docente = crud_docente.get_by_persona(db, usuario.persona_id)
    if not docente:
        raise ForbiddenError("Docente no encontrado")

    inscripcion = crud_inscripcion.get(db, inscripcion_id)
    if not inscripcion:
        raise NotFoundError("Inscripción no encontrada")

    asignacion = crud_asignacion.get_by(
        db,
        docente_id=docente.id,
        materia_id=materia_id,
        grupo_id=inscripcion.grupo_id,
        ciclo_id=inscripcion.ciclo_id,
    )
    if not asignacion:
        raise ForbiddenError("No tienes asignada esa materia en ese grupo")


def capturar(
    db: Session, payload: CalificacionCreate, usuario: Usuario
) -> Calificacion:
    _validar_docente_asignado(db, usuario, payload.materia_id, payload.inscripcion_id)

    periodo = crud_periodo.get(db, payload.periodo_id)
    if not periodo:
        raise NotFoundError("Periodo no encontrado")
    if not periodo.activo:
        raise BadRequestError("El periodo de evaluación está cerrado")

    # Validar rango
    if payload.valor < 0 or payload.valor > 10:
        raise BadRequestError("La calificación debe estar entre 0 y 10")

    # Evitar duplicado
    existente = crud_calificacion.get_unica(
        db, payload.inscripcion_id, payload.materia_id, payload.periodo_id
    )
    if existente:
        raise ConflictError(
            "Ya existe una calificación para ese alumno-materia-periodo"
        )

    docente = crud_docente.get_by_persona(db, usuario.persona_id)
    data = payload.model_dump()
    data["capturado_por"] = docente.id
    data["estado"] = EstadoCalificacion.BORRADOR
    return crud_calificacion.create(db, data)


def capturar_masiva(
    db: Session, payload: CalificacionMasiva, usuario: Usuario
) -> list[Calificacion]:
    """Captura todas las calificaciones de un grupo-materia-periodo en una transacción."""
    if usuario.rol != RolUsuario.DOCENTE:
        raise ForbiddenError("Solo docentes pueden capturar calificaciones")

    docente = crud_docente.get_by_persona(db, usuario.persona_id)
    asignacion = crud_asignacion.get_by(
        db,
        docente_id=docente.id,
        materia_id=payload.materia_id,
        grupo_id=payload.grupo_id,
    )
    if not asignacion:
        raise ForbiddenError("No tienes asignada esa materia en ese grupo")

    periodo = crud_periodo.get(db, payload.periodo_id)
    if not periodo or not periodo.activo:
        raise BadRequestError("Periodo no válido o cerrado")

    resultados: list[Calificacion] = []
    try:
        for item in payload.items:
            inscripcion_id = item["inscripcion_id"]
            valor = Decimal(str(item["valor"]))
            observaciones = item.get("observaciones")

            existente = crud_calificacion.get_unica(
                db, inscripcion_id, payload.materia_id, payload.periodo_id
            )
            if existente:
                if existente.estado != EstadoCalificacion.BORRADOR:
                    raise BadRequestError(
                        f"Calificación bloqueada para inscripcion {inscripcion_id}"
                    )
                existente.valor = valor
                existente.observaciones = observaciones
                db.add(existente)
                resultados.append(existente)
            else:
                nueva = Calificacion(
                    inscripcion_id=inscripcion_id,
                    materia_id=payload.materia_id,
                    periodo_id=payload.periodo_id,
                    valor=valor,
                    observaciones=observaciones,
                    capturado_por=docente.id,
                    estado=EstadoCalificacion.BORRADOR,
                )
                db.add(nueva)
                resultados.append(nueva)
        db.commit()
        for r in resultados:
            db.refresh(r)
    except Exception:
        db.rollback()
        raise
    return resultados


def actualizar(
    db: Session, calificacion_id: int, payload: CalificacionUpdate, usuario: Usuario
) -> Calificacion:
    calif = crud_calificacion.get(db, calificacion_id)
    if not calif:
        raise NotFoundError("Calificación no encontrada")

    if calif.estado != EstadoCalificacion.BORRADOR:
        raise ForbiddenError(
            f"No se puede editar una calificación en estado {calif.estado.value}"
        )

    docente = crud_docente.get_by_persona(db, usuario.persona_id)
    if not docente or calif.capturado_por != docente.id:
        raise ForbiddenError("Solo el docente que capturó puede editar")

    if payload.valor is not None and (payload.valor < 0 or payload.valor > 10):
        raise BadRequestError("La calificación debe estar entre 0 y 10")

    return crud_calificacion.update(db, calif, payload)


def cambiar_estado(
    db: Session,
    calificacion_id: int,
    nuevo_estado: EstadoCalificacion,
    usuario: Usuario,
) -> Calificacion:
    calif = crud_calificacion.get(db, calificacion_id)
    if not calif:
        raise NotFoundError("Calificación no encontrada")

    permitidos = TRANSICIONES.get(calif.estado, set())
    if nuevo_estado not in permitidos:
        raise BadRequestError(
            f"Transición no permitida: {calif.estado.value} → {nuevo_estado.value}"
        )

    # Reglas por rol
    if usuario.rol == RolUsuario.DOCENTE:
        if nuevo_estado != EstadoCalificacion.ENVIADA:
            raise ForbiddenError("El docente solo puede enviar a revisión")
        docente = crud_docente.get_by_persona(db, usuario.persona_id)
        if calif.capturado_por != docente.id:
            raise ForbiddenError("No es tu calificación")

    elif usuario.rol == RolUsuario.DIRECTIVO:
        # Directivo puede bloquear, publicar o regresar a borrador
        pass
    else:
        raise ForbiddenError("Rol sin permisos para cambiar estado")

    return crud_calificacion.cambiar_estado(db, calif, nuevo_estado)


def listar_por_grupo(
    db: Session, grupo_id: int, materia_id: int, periodo_id: int, usuario: Usuario
) -> list[Calificacion]:
    if usuario.rol == RolUsuario.DOCENTE:
        docente = crud_docente.get_by_persona(db, usuario.persona_id)
        asignacion = crud_asignacion.get_by(
            db, docente_id=docente.id, materia_id=materia_id, grupo_id=grupo_id
        )
        if not asignacion:
            raise ForbiddenError("No impartes esa materia en ese grupo")
    return crud_calificacion.list_by_grupo_materia_periodo(
        db, grupo_id, materia_id, periodo_id
    )
