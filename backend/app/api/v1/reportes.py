from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, require_admin_o_directivo
from app.services import reporte_service

router = APIRouter(prefix="/reportes", tags=["Reportes"])


@router.get("/grupo/{grupo_id}/materia/{materia_id}")
def promedio_grupo_materia(
    grupo_id: int,
    materia_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    return reporte_service.promedio_por_grupo_materia(db, grupo_id, materia_id)


@router.get("/grupo/{grupo_id}/materia/{materia_id}/aprobacion")
def aprobacion(
    grupo_id: int,
    materia_id: int,
    minimo: float = 6.0,
    db: Session = Depends(get_db),
    _=Depends(require_admin_o_directivo),
):
    return reporte_service.aprobados_reprobados(db, grupo_id, materia_id, minimo)


@router.get("/grupo/{grupo_id}/concentrado")
def concentrado(
    grupo_id: int, db: Session = Depends(get_db), _=Depends(require_admin_o_directivo)
):
    return reporte_service.concentrado_grupo(db, grupo_id)
