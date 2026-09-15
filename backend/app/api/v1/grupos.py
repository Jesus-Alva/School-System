from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_admin_o_directivo
from app.core.exceptions import NotFoundError
from app.crud import grupo as crud, inscripcion as crud_inscripcion
from app.schemas.common import MessageResponse
from app.schemas.grupo import GrupoCreate, GrupoRead, GrupoUpdate

router = APIRouter(prefix="/grupos", tags=["Grupos"])


@router.get("/", response_model=list[GrupoRead])
def listar(
    ciclo_id: int | None = None,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    if ciclo_id:
        return crud.list_by_ciclo(db, ciclo_id)
    return crud.list(db, limit=500)


@router.post("/", response_model=GrupoRead, status_code=status.HTTP_201_CREATED)
def crear(
    payload: GrupoCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    return crud.create(db, payload)


@router.get("/{id}", response_model=GrupoRead)
def obtener(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    obj = crud.get(db, id)
    if not obj:
        raise NotFoundError("Grupo no encontrado")
    return obj


@router.get("/{id}/alumnos")
def alumnos(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    inscripciones = crud_inscripcion.list_by_grupo(db, id)
    return [
        {"inscripcion_id": i.id, "alumno_id": i.alumno_id, "estado": i.estado}
        for i in inscripciones
    ]


@router.patch("/{id}", response_model=GrupoRead)
def actualizar(
    id: int,
    payload: GrupoUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    obj = crud.get(db, id)
    if not obj:
        raise NotFoundError("Grupo no encontrado")
    return crud.update(db, obj, payload)


@router.post("/{id}/asignar-salon/{salon_id}", response_model=GrupoRead)
def asignar_salon(
    id: int,
    salon_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    obj = crud.get(db, id)
    if not obj:
        raise NotFoundError("Grupo no encontrado")
    return crud.asignar_salon(db, obj, salon_id)


@router.delete("/{id}", response_model=MessageResponse)
def eliminar(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    if not crud.get(db, id):
        raise NotFoundError("Grupo no encontrado")
    crud.remove(db, id)
    return MessageResponse(detail="Grupo eliminado")
