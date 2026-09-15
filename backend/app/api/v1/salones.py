from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_admin_o_directivo
from app.core.exceptions import NotFoundError
from app.crud import salon as crud
from app.schemas.common import MessageResponse
from app.schemas.salon import SalonCreate, SalonRead, SalonUpdate

router = APIRouter(prefix="/salones", tags=["Salones"])


@router.get("/", response_model=list[SalonRead])
def listar(db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)):
    return crud.list(db, limit=500)


@router.post("/", response_model=SalonRead, status_code=status.HTTP_201_CREATED)
def crear(
    payload: SalonCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    return crud.create(db, payload)


@router.get("/{id}", response_model=SalonRead)
def obtener(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    obj = crud.get(db, id)
    if not obj:
        raise NotFoundError("Salón no encontrado")
    return obj


@router.patch("/{id}", response_model=SalonRead)
def actualizar(
    id: int,
    payload: SalonUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    obj = crud.get(db, id)
    if not obj:
        raise NotFoundError("Salón no encontrado")
    return crud.update(db, obj, payload)


@router.delete("/{id}", response_model=MessageResponse)
def eliminar(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    if not crud.get(db, id):
        raise NotFoundError("Salón no encontrado")
    crud.remove(db, id)
    return MessageResponse(detail="Salón eliminado")
