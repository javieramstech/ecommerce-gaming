import bcrypt
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from jose import JWTError, jwt
from app.core.config import settings


def _pre_hash_password(password: str) -> bytes:
    """
    Pre-hashea la contraseña con SHA-256 para garantizar una longitud fija (32 bytes)
    y evitar el límite de 72 bytes de bcrypt así como incompatibilidades de passlib con bcrypt 5.
    """
    return hashlib.sha256(password.encode("utf-8")).digest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña coincide con el hash bcrypt almacenado."""
    try:
        password_bytes = _pre_hash_password(plain_password)
        hashed_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Genera un hash bcrypt seguro a partir de la contraseña."""
    password_bytes = _pre_hash_password(password)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def create_access_token(subject: str | Any, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token de acceso JWT con el 'sub' (ID de usuario) y fecha de expiración.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict[str, Any]]:
    """
    Decodifica y valida la firma del token JWT. Devuelve el payload si es válido.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
