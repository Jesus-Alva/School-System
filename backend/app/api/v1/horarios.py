from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_admin_o_directivo
from app.crud import horario as crud
from app.schemas.common import MessageResponse
from app.schemas.horario import HorarioCreate, HorarioRead, HorarioUpdate
from app.services import horario_service

router = APIRouter(prefix="/horarios", tags=["Horarios"])


@router.get("/por-grupo/{grupo_id}", response_model=list[HorarioRead])
def por_grupo(
    grupo_id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    return crud.list_by_grupo(db, grupo_id)


@router.post("/", response_model=HorarioRead, status_code=status.HTTP_201_CREATED)
def crear(
    payload: HorarioCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    return horario_service.crear(db, payload)


@router.patch("/{id}", response_model=HorarioRead)
def actualizar(
    id: int,
    payload: HorarioUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    return horario_service.actualizar(db, id, payload)


@router.delete("/{id}", response_model=MessageResponse)
def eliminar(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    horario_service.eliminar(db, id)
    return MessageResponse(detail="Horario eliminado")
