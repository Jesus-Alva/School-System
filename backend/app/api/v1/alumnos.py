from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_admin_o_directivo, require_any
from app.core.exceptions import NotFoundError
from app.crud import alumno as crud, inscripcion as crud_inscripcion
from app.schemas.alumno import AlumnoCreate, AlumnoRead, AlumnoUpdate
from app.schemas.common import MessageResponse

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])


@router.get("/", response_model=list[AlumnoRead])
def listar(
    skip: int = 0,
    limit: int = 100,
    estado: str | None = None,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    return crud.list_con_persona(db, skip=skip, limit=limit, estado=estado)


@router.post("/", response_model=AlumnoRead, status_code=status.HTTP_201_CREATED)
def crear(
    payload: AlumnoCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    return crud.create(db, payload)


@router.get("/{id}", response_model=AlumnoRead)
def obtener(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    obj = crud.get(db, id)
    if not obj:
        raise NotFoundError("Alumno no encontrado")
    return obj


@router.patch("/{id}", response_model=AlumnoRead)
def actualizar(
    id: int,
    payload: AlumnoUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    obj = crud.get(db, id)
    if not obj:
        raise NotFoundError("Alumno no encontrado")
    return crud.update(db, obj, payload)


@router.get("/{id}/inscripciones")
def inscripciones(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    from app.crud import inscripcion as crud_insc
    from sqlalchemy import select
    from app.models.inscripcion import Inscripcion

    stmt = select(Inscripcion).where(
        Inscripcion.alumno_id == id, Inscripcion.deleted_at.is_(None)
    )
    return list(db.execute(stmt).scalars().all())


@router.delete("/{id}", response_model=MessageResponse)
def eliminar(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    if not crud.get(db, id):
        raise NotFoundError("Alumno no encontrado")
    crud.remove(db, id)
    return MessageResponse(detail="Alumno eliminado")
