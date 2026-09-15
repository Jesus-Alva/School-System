from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_admin_o_directivo
from app.core.exceptions import NotFoundError, ConflictError, BadRequestError
from app.crud import (
    grado as crud,
    ciclo_escolar as crud_ciclo,
    plan_estudio as crud_plan,
)
from app.enum import NivelEducativo
from app.schemas.common import MessageResponse
from app.schemas.grado import GradoCreate, GradoRead, GradoUpdate
from app.schemas.plan_estudio import PlanEstudioRead

router = APIRouter(prefix="/grados", tags=["Grados"])


# ------------------------------------------------------------------
# Listados
# ------------------------------------------------------------------
@router.get("/", response_model=list[GradoRead])
def listar(
    ciclo_id: int | None = None,
    nivel: NivelEducativo | None = None,
    skip: int = 0,
    limit: int = 200,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    """Lista grados. Filtra por ciclo y/o nivel si se indica."""
    if ciclo_id:
        return crud.list_by_ciclo(db, ciclo_id, nivel)
    return crud.list(db, skip=skip, limit=limit)


# ------------------------------------------------------------------
# CRUD
# ------------------------------------------------------------------
@router.post("/", response_model=GradoRead, status_code=status.HTTP_201_CREATED)
def crear(
    payload: GradoCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    """Crea un grado dentro de un ciclo escolar."""
    ciclo = crud_ciclo.get(db, payload.ciclo_id)
    if not ciclo:
        raise NotFoundError("Ciclo escolar no encontrado")

    # Validar duplicado (ciclo + nivel + nombre)
    existente = crud.get_by(
        db,
        ciclo_id=payload.ciclo_id,
        nivel=payload.nivel,
        nombre=payload.nombre,
    )
    if existente:
        raise ConflictError(f"Ya existe el grado {payload.nombre} en ese ciclo y nivel")

    return crud.create(db, payload)


@router.get("/{id}", response_model=GradoRead)
def obtener(
    id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    obj = crud.get(db, id)
    if not obj:
        raise NotFoundError("Grado no encontrado")
    return obj


@router.patch("/{id}", response_model=GradoRead)
def actualizar(
    id: int,
    payload: GradoUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    obj = crud.get(db, id)
    if not obj:
        raise NotFoundError("Grado no encontrado")

    # Si cambia el nombre o nivel, validar que no choque con otro
    nuevo_nombre = payload.nombre or obj.nombre
    nuevo_nivel = payload.nivel or obj.nivel
    if nuevo_nombre != obj.nombre or nuevo_nivel != obj.nivel:
        existente = crud.get_by(
            db,
            ciclo_id=obj.ciclo_id,
            nivel=nuevo_nivel,
            nombre=nuevo_nombre,
        )
        if existente and existente.id != obj.id:
            raise ConflictError(
                f"Ya existe el grado {nuevo_nombre} en ese ciclo y nivel"
            )

    return crud.update(db, obj, payload)


@router.delete("/{id}", response_model=MessageResponse)
def eliminar(
    id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    obj = crud.get(db, id)
    if not obj:
        raise NotFoundError("Grado no encontrado")

    # Validar que no tenga grupos asociados
    from app.crud import grupo as crud_grupo

    grupos = crud_grupo.list_by_grado(db, id)
    if grupos:
        raise BadRequestError(
            f"No se puede eliminar: el grado tiene {len(grupos)} grupo(s) asociado(s)"
        )

    # Validar que no tenga plan de estudios
    planes = crud_plan.list_by_grado(db, id)
    if planes:
        raise BadRequestError(
            "No se puede eliminar: el grado tiene plan de estudios asignado"
        )

    crud.remove(db, id)
    return MessageResponse(detail="Grado eliminado")


# ------------------------------------------------------------------
# Endpoints de relación
# ------------------------------------------------------------------
@router.get("/{id}/plan-estudios", response_model=list[PlanEstudioRead])
def plan_estudios(
    id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    """Devuelve el plan de estudios (materias) del grado."""
    if not crud.get(db, id):
        raise NotFoundError("Grado no encontrado")
    return crud_plan.list_by_grado(db, id)


@router.get("/{id}/grupos")
def grupos(
    id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    """Lista los grupos del grado."""
    from app.crud import grupo as crud_grupo

    if not crud.get(db, id):
        raise NotFoundError("Grado no encontrado")
    return crud_grupo.list_by_grado(db, id)
