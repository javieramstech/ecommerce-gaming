from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.db.database import get_session
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository

# Configuración de OAuth2 para recuperar el token del header Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_db() -> Generator[Session, None, None]:
    """Inyección de dependencia para la sesión de base de datos SQLModel."""
    yield from get_session()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db)
) -> User:
    """
    Inyección de dependencia para obtener y validar el usuario actualmente autenticado a partir del Token JWT.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales de autenticación.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception

    payload = decode_access_token(token)
    if not payload:
        raise credentials_exception

    user_id_str = payload.get("sub")
    if not user_id_str:
        raise credentials_exception

    try:
        user_id = int(user_id_str)
    except ValueError:
        raise credentials_exception

    user_repo = UserRepository(session)
    user = user_repo.get_by_id(user_id)
    if not user or not user.is_active:
        raise credentials_exception

    return user


def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """Valida que el usuario autenticado tenga privilegios de administrador."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operación no permitida. Se requieren privilegios de administrador."
        )
    return current_user
