from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_current_user, get_db
from app.models.usuario import Usuario
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.common import MessageResponse
from app.schemas.usuario import UsuarioChangePassword
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login(db, payload)


@router.post("/refresh", response_model=TokenResponse)
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    return auth_service.refresh_token(db, refresh_token)


@router.post("/cambiar-password", response_model=MessageResponse)
def cambiar_password(
    payload: UsuarioChangePassword,
    db: Session = Depends(get_db),
    user: Usuario = Depends(get_current_user),
):
    auth_service.cambiar_password(
        db, user, payload.password_actual, payload.password_nueva
    )
    return MessageResponse(detail="Contraseña actualizada")


@router.get("/me")
def me(user: Usuario = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "rol": user.rol,
        "persona_id": user.persona_id,
    }
