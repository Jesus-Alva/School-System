from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_admin_o_directivo
from app.schemas.common import MessageResponse
from app.schemas.inscripcion import (
    InscripcionCreate,
    InscripcionRead,
    InscripcionUpdate,
)
from app.services import inscripcion_service

router = APIRouter(prefix="/inscripciones", tags=["Inscripciones"])


@router.post("/", response_model=InscripcionRead, status_code=status.HTTP_201_CREATED)
def crear(
    payload: InscripcionCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    return inscripcion_service.inscribir(db, payload)


@router.get("/por-grupo/{grupo_id}")
def por_grupo(
    grupo_id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    return inscripcion_service.listar_por_grupo(db, grupo_id)


@router.post("/{id}/cambiar-grupo/{grupo_id}", response_model=InscripcionRead)
def cambiar_grupo(
    id: int,
    grupo_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    return inscripcion_service.cambiar_grupo(db, id, grupo_id)


@router.post("/{id}/baja", response_model=InscripcionRead)
def baja(id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)):
    return inscripcion_service.dar_de_baja(db, id)
