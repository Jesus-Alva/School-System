from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_admin_o_directivo
from app.core.exceptions import NotFoundError
from app.crud import persona as crud
from app.schemas.common import MessageResponse
from app.schemas.persona import PersonaCreate, PersonaRead, PersonaUpdate

router = APIRouter(prefix="/personas", tags=["Personas"])


@router.get("/", response_model=list[PersonaRead])
def listar(
    skip: int = 0,
    limit: int = 100,
    q: str | None = None,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    if q:
        return crud.search(db, q, skip=skip, limit=limit)
    return crud.list(db, skip=skip, limit=limit)


@router.post("/", response_model=PersonaRead, status_code=status.HTTP_201_CREATED)
def crear(
    payload: PersonaCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    return crud.create(db, payload)


@router.get("/{id}", response_model=PersonaRead)
def obtener(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    obj = crud.get(db, id)
    if not obj:
        raise NotFoundError("Persona no encontrada")
    return obj


@router.patch("/{id}", response_model=PersonaRead)
def actualizar(
    id: int,
    payload: PersonaUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    obj = crud.get(db, id)
    if not obj:
        raise NotFoundError("Persona no encontrada")
    return crud.update(db, obj, payload)


@router.delete("/{id}", response_model=MessageResponse)
def eliminar(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    if not crud.get(db, id):
        raise NotFoundError("Persona no encontrada")
    crud.remove(db, id)
    return MessageResponse(detail="Persona eliminada")
