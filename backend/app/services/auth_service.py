from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.core import security
from app.core.exceptions import (
    UnauthorizedError,
    ForbiddenError,
    BadRequestError,
    ConflictError,
    NotFoundError,
)
from app.crud import usuario as crud_usuario
from app.crud import persona as crud_persona
from app.enum import EstadoUsuario, RolUsuario
from app.models.usuario import Usuario
from app.schemas.auth import LoginRequest, TokenResponse


def autenticar(db: Session, payload: LoginRequest) -> Usuario:
    """Valida credenciales y devuelve el usuario o lanza excepción."""
    user = crud_usuario.get_by_email(db, payload.email)

    if not user:
        raise UnauthorizedError("Credenciales inválidas")

    if user.estado == EstadoUsuario.BLOQUEADO:
        raise ForbiddenError("Usuario bloqueado. Contacte al administrador.")

    if user.estado == EstadoUsuario.INACTIVO:
        raise ForbiddenError("Usuario inactivo")

    if not security.verify_password(payload.password, user.password_hash):
        user.intentos_fallidos = (user.intentos_fallidos or 0) + 1
        # Bloqueo automático tras N intentos
        from app.core.config import settings

        if user.intentos_fallidos >= settings.MAX_LOGIN_ATTEMPTS:
            user.estado = EstadoUsuario.BLOQUEADO
        db.add(user)
        db.commit()
        raise UnauthorizedError("Credenciales inválidas")

    # Reset contador y actualizar último acceso
    user.intentos_fallidos = 0
    user.ultimo_acceso = datetime.now(timezone.utc)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login(db: Session, payload: LoginRequest) -> TokenResponse:
    user = autenticar(db, payload)
    access = security.create_access_token(subject=user.id, rol=user.rol.value)
    return TokenResponse(
        access_token=access,
        token_type="bearer",
        expires_in=3600,
        rol=user.rol,
    )


def refresh_token(db: Session, refresh: str) -> TokenResponse:
    try:
        data = security.decode_token(refresh)
    except ValueError:
        raise UnauthorizedError("Refresh token inválido")

    if data.get("type") != "refresh":
        raise UnauthorizedError("Tipo de token incorrecto")

    user = crud_usuario.get(db, int(data["sub"]))
    if not user or user.estado != EstadoUsuario.ACTIVO:
        raise UnauthorizedError("Usuario no válido")

    access = security.create_access_token(subject=user.id, rol=user.rol.value)
    return TokenResponse(
        access_token=access,
        token_type="bearer",
        expires_in=3600,
        rol=user.rol,
    )


def cambiar_password(
    db: Session, user: Usuario, password_actual: str, password_nueva: str
) -> None:
    if not security.verify_password(password_actual, user.password_hash):
        raise BadRequestError("Contraseña actual incorrecta")

    if password_actual == password_nueva:
        raise BadRequestError("La nueva contraseña debe ser diferente")

    user.password_hash = security.hash_password(password_nueva)
    db.add(user)
    db.commit()


def crear_usuario_con_persona(
    db: Session,
    *,
    rol: RolUsuario,
    email: str,
    password: str,
    nombres: str,
    apellido_paterno: str,
    apellido_materno: str | None = None,
    telefono: str | None = None,
    **extra_persona,
) -> Usuario:
    """Crea Persona + Usuario en una sola operación."""
    if crud_persona.get_by_email(db, email):
        raise ConflictError("Ya existe una persona con ese email")
    if crud_usuario.get_by_email(db, email):
        raise ConflictError("Ya existe un usuario con ese email")

    from app.core.config import settings

    if len(password) < settings.PASSWORD_MIN_LENGTH:
        raise BadRequestError(
            f"La contraseña debe tener al menos {settings.PASSWORD_MIN_LENGTH} caracteres"
        )

    persona = crud_persona.create(
        db,
        {
            "nombres": nombres,
            "apellido_paterno": apellido_paterno,
            "apellido_materno": apellido_materno,
            "email": email,
            "telefono": telefono,
            **extra_persona,
        },
    )
    user = crud_usuario.create(
        db,
        {
            "persona_id": persona.id,
            "email": email,
            "password_hash": security.hash_password(password),
            "rol": rol,
            "estado": EstadoUsuario.ACTIVO,
        },
    )
    return user


def desbloquear(db: Session, usuario_id: int) -> Usuario:
    user = crud_usuario.get(db, usuario_id)
    if not user:
        raise NotFoundError("Usuario no encontrado")
    user.estado = EstadoUsuario.ACTIVO
    user.intentos_fallidos = 0
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
