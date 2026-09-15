from app.models.persona import Persona
from app.models.usuario import Usuario
from app.models.directivo import Directivo
from app.models.alumno import Alumno
from app.models.tutor import Tutor
from app.models.tutor_alumno import TutorAlumno
from app.models.docente import Docente
from app.models.materia import Materia
from app.models.plan_estudio import PlanEstudio
from app.models.ciclo_escolar import CicloEscolar
from app.models.grado import Grado
from app.models.grupo import Grupo
from app.models.salon import Salon
from app.models.periodo_evaluacion import PeriodoEvaluacion
from app.models.asignacion_docente import AsignacionDocente
from app.models.inscripcion import Inscripcion
from app.models.calificacion import Calificacion
from app.models.asistencia import Asistencia
from app.models.horario import Horario
from app.models.noticia import Noticia
from app.models.aviso import Aviso
from app.models.boleta import Boleta
from app.models.audit_log import AuditLog

__all__ = [
    "Persona",
    "Usuario",
    "Directivo",
    "Alumno",
    "Tutor",
    "TutorAlumno",
    "Docente",
    "Materia",
    "PlanEstudio",
    "CicloEscolar",
    "Grado",
    "Grupo",
    "Salon",
    "PeriodoEvaluacion",
    "AsignacionDocente",
    "Inscripcion",
    "Calificacion",
    "Asistencia",
    "Horario",
    "Noticia",
    "Aviso",
    "Boleta",
    "AuditLog",
]
