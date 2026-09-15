from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_admin_o_directivo
from app.core.exceptions import NotFoundError
from app.crud import asignacion_docente as crud
from app.schemas.asignacion_docente import (
    AsignacionDocenteCreate,
    AsignacionDocenteRead,
    AsignacionDocenteUpdate,
)
from app.schemas.common import MessageResponse
from app.services import asignacion_service

router = APIRouter(prefix="/asignaciones", tags=["Asignaciones docente-materia-grupo"])


@router.get("/por-grupo/{grupo_id}", response_model=list[AsignacionDocenteRead])
def por_grupo(
    grupo_id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    return crud.list_by_grupo(db, grupo_id)


@router.get("/por-docente/{docente_id}", response_model=list[AsignacionDocenteRead])
def por_docente(
    docente_id: int,
    ciclo_id: int | None = None,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    return crud.list_by_docente(db, docente_id, ciclo_id)


@router.post(
    "/", response_model=AsignacionDocenteRead, status_code=status.HTTP_201_CREATED
)
def crear(
    payload: AsignacionDocenteCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    return asignacion_service.crear(db, payload)


@router.patch("/{id}", response_model=AsignacionDocenteRead)
def actualizar(
    id: int,
    payload: AsignacionDocenteUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    return asignacion_service.actualizar(db, id, payload)


@router.delete("/{id}", response_model=MessageResponse)
def eliminar(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    asignacion_service.eliminar(db, id)
    return MessageResponse(detail="Asignación eliminada")
