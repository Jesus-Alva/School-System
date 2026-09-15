from app.crud.persona import persona
from app.crud.usuario import usuario
from app.crud.directivo import directivo
from app.crud.alumno import alumno
from app.crud.tutor import tutor
from app.crud.tutor_alumno import tutor_alumno
from app.crud.docente import docente
from app.crud.materia import materia
from app.crud.plan_estudio import plan_estudio
from app.crud.ciclo_escolar import ciclo_escolar
from app.crud.grado import grado
from app.crud.grupo import grupo
from app.crud.salon import salon
from app.crud.periodo_evaluacion import periodo_evaluacion
from app.crud.asignacion_docente import asignacion_docente
from app.crud.inscripcion import inscripcion
from app.crud.calificacion import calificacion
from app.crud.asistencia import asistencia
from app.crud.horario import horario
from app.crud.noticia import noticia
from app.crud.aviso import aviso
from app.crud.boleta import boleta
from app.crud.audit_log import audit_log

__all__ = [
    "persona",
    "usuario",
    "directivo",
    "alumno",
    "tutor",
    "tutor_alumno",
    "docente",
    "materia",
    "plan_estudio",
    "ciclo_escolar",
    "grado",
    "grupo",
    "salon",
    "periodo_evaluacion",
    "asignacion_docente",
    "inscripcion",
    "calificacion",
    "asistencia",
    "horario",
    "noticia",
    "aviso",
    "boleta",
    "audit_log",
]
