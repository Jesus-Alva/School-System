from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_admin_o_directivo
from app.core.exceptions import NotFoundError
from app.crud import docente as crud
from app.schemas.common import MessageResponse
from app.schemas.docente import DocenteCreate, DocenteRead, DocenteUpdate

router = APIRouter(prefix="/docentes", tags=["Docentes"])


@router.get("/", response_model=list[DocenteRead])
def listar(db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)):
    return crud.list_con_persona(db)


@router.post("/", response_model=DocenteRead, status_code=status.HTTP_201_CREATED)
def crear(
    payload: DocenteCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    return crud.create(db, payload)


@router.get("/{id}", response_model=DocenteRead)
def obtener(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    obj = crud.get(db, id)
    if not obj:
        raise NotFoundError("Docente no encontrado")
    return obj


@router.get("/por-materia/{materia_id}", response_model=list[DocenteRead])
def por_materia(
    materia_id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    return crud.list_por_materia(db, materia_id)


@router.patch("/{id}", response_model=DocenteRead)
def actualizar(
    id: int,
    payload: DocenteUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    obj = crud.get(db, id)
    if not obj:
        raise NotFoundError("Docente no encontrado")
    return crud.update(db, obj, payload)


@router.delete("/{id}", response_model=MessageResponse)
def eliminar(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    if not crud.get(db, id):
        raise NotFoundError("Docente no encontrado")
    crud.remove(db, id)
    return MessageResponse(detail="Docente eliminado")
