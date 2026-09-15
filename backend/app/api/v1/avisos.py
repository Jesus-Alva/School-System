from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, require_admin_o_directivo
from app.crud import aviso as crud
from app.enum import RolUsuario
from app.models.usuario import Usuario
from app.schemas.aviso import AvisoCreate, AvisoRead, AvisoUpdate
from app.schemas.common import MessageResponse

router = APIRouter(prefix="/avisos", tags=["Avisos"])


@router.get("/", response_model=list[AvisoRead])
def listar_para_mi(
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    return crud.list_para_usuario(db, user.rol)


@router.post("/", response_model=AvisoRead, status_code=status.HTTP_201_CREATED)
def crear(
    payload: AvisoCreate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    data = payload.model_dump()
    data["autor_id"] = user.id
    return crud.create(db, data)


@router.patch("/{id}", response_model=AvisoRead)
def actualizar(
    id: int,
    payload: AvisoUpdate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    obj = crud.get(db, id)
    if not obj or obj.autor_id != user.id:
        from app.core.exceptions import ForbiddenError

        raise ForbiddenError("No puedes editar este aviso")
    return crud.update(db, obj, payload)


@router.delete("/{id}", response_model=MessageResponse)
def eliminar(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    from app.core.exceptions import NotFoundError

    if not crud.get(db, id):
        raise NotFoundError("Aviso no encontrado")
    crud.remove(db, id)
    return MessageResponse(detail="Aviso eliminado")
