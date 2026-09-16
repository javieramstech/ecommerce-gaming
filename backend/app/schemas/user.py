from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    """Esquema para registro de usuario (Sign Up)."""
    email: EmailStr
    full_name: str
    password: str


class UserLogin(BaseModel):
    """Esquema para inicio de sesión (Log In)."""
    email: EmailStr
    password: str


class UserRead(BaseModel):
    """Esquema de salida para datos de usuario."""
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    is_admin: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Esquema de respuesta de autenticación con JWT."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Payload contenido dentro del token JWT."""
    user_id: Optional[int] = None
    email: Optional[str] = None
