from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, require_admin_o_directivo
from app.enum import EstadoCalificacion
from app.models.usuario import Usuario
from app.schemas.calificacion import (
    CalificacionCambioEstado,
    CalificacionCreate,
    CalificacionMasiva,
    CalificacionRead,
    CalificacionUpdate,
)
from app.services import calificacion_service

router = APIRouter(prefix="/calificaciones", tags=["Calificaciones"])


@router.post("/", response_model=CalificacionRead, status_code=status.HTTP_201_CREATED)
def capturar(
    payload: CalificacionCreate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    return calificacion_service.capturar(db, payload, user)


@router.post("/masiva", response_model=list[CalificacionRead])
def capturar_masiva(
    payload: CalificacionMasiva,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    return calificacion_service.capturar_masiva(db, payload, user)


@router.get("/por-grupo")
def listar_por_grupo(
    grupo_id: int,
    materia_id: int,
    periodo_id: int,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    return calificacion_service.listar_por_grupo(
        db, grupo_id, materia_id, periodo_id, user
    )


@router.patch("/{id}", response_model=CalificacionRead)
def actualizar(
    id: int,
    payload: CalificacionUpdate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    return calificacion_service.actualizar(db, id, payload, user)


@router.post("/{id}/estado", response_model=CalificacionRead)
def cambiar_estado(
    id: int,
    payload: CalificacionCambioEstado,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    return calificacion_service.cambiar_estado(db, id, payload.estado, user)


@router.post("/grupo/{grupo_id}/materia/{materia_id}/periodo/{periodo_id}/publicar")
def publicar_grupo(
    grupo_id: int,
    materia_id: int,
    periodo_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    """Publica todas las calificaciones en bloque (directivo)."""
    from app.crud import calificacion as crud

    califs = crud.list_by_grupo_materia_periodo(db, grupo_id, materia_id, periodo_id)
    for c in califs:
        c.estado = EstadoCalificacion.PUBLICADA
    db.commit()
    return {"publicadas": len(califs)}
