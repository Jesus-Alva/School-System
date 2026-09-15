from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core import security
from app.core.config import settings
from app.core.dependencies import get_db
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.crud import usuario as crud_usuario
from app.enum import EstadoUsuario, RolUsuario
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> Usuario:
    try:
        payload = security.decode_token(token)
    except ValueError:
        raise UnauthorizedError("Token inválido o expirado")

    if payload.get("type") != "access":
        raise UnauthorizedError("Tipo de token incorrecto")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedError("Token sin sujeto")

    user = crud_usuario.get(db, int(user_id))
    if not user:
        raise UnauthorizedError("Usuario no encontrado")

    if user.estado != EstadoUsuario.ACTIVO:
        raise ForbiddenError("Usuario no activo")

    return user


def get_current_persona(user: Usuario = Depends(get_current_user)):
    return user.persona


def require_roles(*roles: RolUsuario):
    """Factory de dependencia para exigir uno o varios roles."""

    def _checker(user: Usuario = Depends(get_current_user)) -> Usuario:
        if user.rol not in roles:
            raise ForbiddenError(
                f"Requiere uno de estos roles: {[r.value for r in roles]}"
            )
        return user

    return _checker


# Shortcuts
require_admin_o_directivo = require_roles(RolUsuario.ADMIN, RolUsuario.DIRECTIVO)
require_docente = require_roles(RolUsuario.DOCENTE)
require_alumno = require_roles(RolUsuario.ALUMNO)
require_any = require_roles(
    RolUsuario.ADMIN, RolUsuario.DIRECTIVO, RolUsuario.DOCENTE, RolUsuario.ALUMNO
)


def get_client_ip(request: Request) -> str:
    if request.client:
        return request.client.host
    return "unknown"