from app.schemas.common import (
    ORMBase,
    MessageResponse,
    PaginationParams,
    PaginatedResponse,
)
from app.schemas.persona import PersonaCreate, PersonaUpdate, PersonaRead
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioRead,
    UsuarioChangePassword,
    UsuarioConPersona,
)
from app.schemas.directivo import DirectivoCreate, DirectivoUpdate, DirectivoRead
from app.schemas.alumno import (
    AlumnoCreate,
    AlumnoUpdate,
    AlumnoRead,
    AlumnoConPersona,
)
from app.schemas.tutor import (
    TutorCreate,
    TutorUpdate,
    TutorRead,
    TutorConPersona,
)
from app.schemas.tutor_alumno import (
    TutorAlumnoCreate,
    TutorAlumnoUpdate,
    TutorAlumnoRead,
)
from app.schemas.materia import MateriaCreate, MateriaUpdate, MateriaRead
from app.schemas.docente import (
    DocenteCreate,
    DocenteUpdate,
    DocenteRead,
    DocenteConPersona,
)
from app.schemas.plan_estudio import (
    PlanEstudioCreate,
    PlanEstudioUpdate,
    PlanEstudioRead,
)
from app.schemas.ciclo_escolar import (
    CicloEscolarCreate,
    CicloEscolarUpdate,
    CicloEscolarRead,
)
from app.schemas.grado import GradoCreate, GradoUpdate, GradoRead
from app.schemas.grupo import GrupoCreate, GrupoUpdate, GrupoRead
from app.schemas.salon import SalonCreate, SalonUpdate, SalonRead
from app.schemas.periodo_evaluacion import (
    PeriodoEvaluacionCreate,
    PeriodoEvaluacionUpdate,
    PeriodoEvaluacionRead,
)
from app.schemas.asignacion_docente import (
    AsignacionDocenteCreate,
    AsignacionDocenteUpdate,
    AsignacionDocenteRead,
)
from app.schemas.inscripcion import (
    InscripcionCreate,
    InscripcionUpdate,
    InscripcionRead,
)
from app.schemas.calificacion import (
    CalificacionCreate,
    CalificacionUpdate,
    CalificacionRead,
    CalificacionCambioEstado,
    CalificacionMasiva,
)
from app.schemas.asistencia import (
    AsistenciaCreate,
    AsistenciaUpdate,
    AsistenciaRead,
    AsistenciaMasiva,
)
from app.schemas.horario import HorarioCreate, HorarioUpdate, HorarioRead
from app.schemas.noticia import NoticiaCreate, NoticiaUpdate, NoticiaRead
from app.schemas.aviso import AvisoCreate, AvisoUpdate, AvisoRead
from app.schemas.boleta import BoletaCreate, BoletaUpdate, BoletaRead
from app.schemas.audit_log import AuditLogCreate, AuditLogRead
from app.schemas.auth import LoginRequest, TokenResponse, TokenPayload

# Resolver forward refs
from app.schemas.persona import PersonaRead

UsuarioConPersona.model_rebuild()
TutorConPersona.model_rebuild()
AlumnoConPersona.model_rebuild()
DocenteConPersona.model_rebuild()
