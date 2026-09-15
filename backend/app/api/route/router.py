from fastapi import APIRouter
from app.api.v1 import (
    auth,
    ciclos,
    grados,
    grupos,
    salones,
    personas,
    alumnos,
    docentes,
    materias,
    asignaciones,
    inscripciones,
    calificaciones,
    horarios,
    boletas,
    avisos,
    publico,
    reportes,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(publico.router)
api_router.include_router(ciclos.router)
api_router.include_router(grados.router)
api_router.include_router(grupos.router)
api_router.include_router(salones.router)
api_router.include_router(personas.router)
api_router.include_router(alumnos.router)
api_router.include_router(docentes.router)
api_router.include_router(materias.router)
api_router.include_router(asignaciones.router)
api_router.include_router(inscripciones.router)
api_router.include_router(calificaciones.router)
api_router.include_router(horarios.router)
api_router.include_router(boletas.router)
api_router.include_router(avisos.router)
api_router.include_router(reportes.router)
