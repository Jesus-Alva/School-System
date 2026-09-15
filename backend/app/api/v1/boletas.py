from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, require_admin_o_directivo
from app.models.usuario import Usuario
from app.schemas.boleta import BoletaRead
from app.schemas.common import MessageResponse
from app.services import boleta_service

router = APIRouter(prefix="/boletas", tags=["Boletas"])


@router.post("/generar", response_model=BoletaRead, status_code=status.HTTP_201_CREATED)
def generar(
    inscripcion_id: int,
    ciclo_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    return boleta_service.generar_para_inscripcion(db, inscripcion_id, ciclo_id)


@router.post("/{id}/publicar", response_model=BoletaRead)
def publicar(
    id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    return boleta_service.publicar(db, id)


@router.get("/{id}", response_model=BoletaRead)
def obtener(
    id: int, db: Session = Depends(get_db), user: Usuario = Depends(get_current_user)
):
    from app.crud import boleta as crud
    from app.core.exceptions import NotFoundError, ForbiddenError
    from app.enum import RolUsuario

    boleta = crud.get(db, id)
    if not boleta:
        raise NotFoundError("Boleta no encontrada")

    # Alumno solo ve las propias y publicadas
    if user.rol == RolUsuario.ALUMNO and not boleta.publicada:
        raise ForbiddenError("Boleta no publicada")

    return boleta
