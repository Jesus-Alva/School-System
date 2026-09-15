from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_admin_o_directivo
from app.crud import ciclo_escolar as crud
from app.core.exceptions import NotFoundError
from app.schemas.ciclo_escolar import (
    CicloEscolarCreate,
    CicloEscolarRead,
    CicloEscolarUpdate,
)
from app.schemas.common import MessageResponse

router = APIRouter(prefix="/ciclos", tags=["Ciclos escolares"])


@router.get("/", response_model=list[CicloEscolarRead])
def listar(db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)):
    return crud.list(db, limit=500)


@router.get("/activo", response_model=CicloEscolarRead | None)
def activo(db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)):
    return crud.get_activo(db)


@router.post("/", response_model=CicloEscolarRead, status_code=status.HTTP_201_CREATED)
def crear(
    payload: CicloEscolarCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    return crud.create(db, payload)


@router.get("/{id}", response_model=CicloEscolarRead)
def obtener(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    obj = crud.get(db, id)
    if not obj:
        raise NotFoundError("Ciclo no encontrado")
    return obj


@router.patch("/{id}", response_model=CicloEscolarRead)
def actualizar(
    id: int,
    payload: CicloEscolarUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    obj = crud.get(db, id)
    if not obj:
        raise NotFoundError("Ciclo no encontrado")
    return crud.update(db, obj, payload)


@router.post("/{id}/activar", response_model=CicloEscolarRead)
def activar(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    return crud.activar(db, id)


@router.delete("/{id}", response_model=MessageResponse)
def eliminar(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    obj = crud.get(db, id)
    if not obj:
        raise NotFoundError("Ciclo no encontrado")
    crud.remove(db, id)
    return MessageResponse(detail="Ciclo eliminado")
