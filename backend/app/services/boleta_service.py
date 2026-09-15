import uuid
from decimal import Decimal
from sqlalchemy.orm import Session
from app.core.exceptions import BadRequestError, NotFoundError
from app.crud import (
    boleta as crud_boleta,
    inscripcion as crud_inscripcion,
    calificacion as crud_calificacion,
    periodo_evaluacion as crud_periodo,
)
from app.models.boleta import Boleta


def generar_folio() -> str:
    return f"BOL-{uuid.uuid4().hex[:10].upper()}"


def generar_para_inscripcion(db: Session, inscripcion_id: int, ciclo_id: int) -> Boleta:
    inscripcion = crud_inscripcion.get(db, inscripcion_id)
    if not inscripcion:
        raise NotFoundError("Inscripción no encontrada")

    if inscripcion.ciclo_id != ciclo_id:
        raise BadRequestError("La inscripción no pertenece a ese ciclo")

    existente = crud_boleta.get_by_inscripcion_ciclo(db, inscripcion_id, ciclo_id)
    if existente:
        return existente

    # Validar que todas las materias tengan calificaciones publicadas
    periodos = crud_periodo.list_by_ciclo(db, ciclo_id)
    califs = crud_calificacion.list_by_inscripcion(db, inscripcion_id)
    if not califs:
        raise BadRequestError("El alumno no tiene calificaciones registradas")

    boleta = crud_boleta.create(
        db,
        {
            "inscripcion_id": inscripcion_id,
            "ciclo_id": ciclo_id,
            "folio": generar_folio(),
            "publicada": False,
        },
    )
    # TODO: encolar generación de PDF en Celery
    # from app.tasks import generar_pdf_boleta
    # generar_pdf_boleta.delay(boleta.id)
    return boleta


def publicar(db: Session, boleta_id: int) -> Boleta:
    boleta = crud_boleta.get(db, boleta_id)
    if not boleta:
        raise NotFoundError("Boleta no encontrada")
    if not boleta.pdf_url:
        raise BadRequestError("La boleta aún no tiene PDF generado")
    return crud_boleta.publicar(db, boleta)


def promedio_general(
    db: Session, inscripcion_id: int, materia_id: int
) -> Decimal | None:
    return crud_calificacion.promedio_alumno_materia(db, inscripcion_id, materia_id)
