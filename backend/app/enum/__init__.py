from enum import Enum


class RolUsuario(str, Enum):
    DIRECTIVO = "directivo"
    DOCENTE = "docente"
    ALUMNO = "alumno"
    ADMIN = "admin"


class EstadoUsuario(str, Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    BLOQUEADO = "bloqueado"


class Sexo(str, Enum):
    M = "M"
    F = "F"
    OTRO = "O"


class NivelEducativo(str, Enum):
    PREESCOLAR = "preescolar"
    PRIMARIA = "primaria"
    SECUNDARIA = "secundaria"
    PREPARATORIA = "preparatoria"


class EstadoAlumno(str, Enum):
    ACTIVO = "activo"
    EGRESADO = "egresado"
    BAJA_TEMPORAL = "baja_temporal"
    BAJA_DEFINITIVA = "baja_definitiva"


class EstadoDocente(str, Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    LICENCIA = "licencia"


class RolDocente(str, Enum):
    TITULAR = "titular"
    AUXILIAR = "auxiliar"


class EstadoCalificacion(str, Enum):
    BORRADOR = "borrador"
    ENVIADA = "enviada"
    BLOQUEADA = "bloqueada"
    PUBLICADA = "publicada"


class EstadoAsistencia(str, Enum):
    PRESENTE = "presente"
    AUSENTE = "ausente"
    RETARDO = "retardo"
    JUSTIFICADO = "justificado"


class EstadoInscripcion(str, Enum):
    ACTIVO = "activo"
    BAJA = "baja"
    EGRESADO = "egresado"


class DiaSemana(str, Enum):
    LUNES = "lunes"
    MARTES = "martes"
    MIERCOLES = "miercoles"
    JUEVES = "jueves"
    VIERNES = "viernes"


class AlcanceAviso(str, Enum):
    GENERAL = "general"
    ROL = "rol"
    GRUPO = "grupo"
    MATERIA = "materia"