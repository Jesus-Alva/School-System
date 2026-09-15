from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_admin_o_directivo
from app.core.exceptions import NotFoundError
from app.crud import materia as crud
from app.enum import NivelEducativo
from app.schemas.common import MessageResponse
from app.schemas.materia import MateriaCreate, MateriaRead, MateriaUpdate

router = APIRouter(prefix="/materias", tags=["Materias"])


@router.get("/", response_model=list[MateriaRead])
def listar(
    nivel: NivelEducativo | None = None,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    if nivel:
        return crud.list_by_nivel(db, nivel)
    return crud.list(db, limit=500)


@router.post("/", response_model=MateriaRead, status_code=status.HTTP_201_CREATED)
def crear(
    payload: MateriaCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    return crud.create(db, payload)


@router.get("/{id}", response_model=MateriaRead)
def obtener(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    obj = crud.get(db, id)
    if not obj:
        raise NotFoundError("Materia no encontrada")
    return obj


@router.patch("/{id}", response_model=MateriaRead)
def actualizar(
    id: int,
    payload: MateriaUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    obj = crud.get(db, id)
    if not obj:
        raise NotFoundError("Materia no encontrada")
    return crud.update(db, obj, payload)


@router.delete("/{id}", response_model=MessageResponse)
def eliminar(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    if not crud.get(db, id):
        raise NotFoundError("Materia no encontrada")
    crud.remove(db, id)
    return MessageResponse(detail="Materia eliminada")
