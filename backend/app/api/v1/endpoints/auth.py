from typing import Optional
from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlmodel import Session
from app.api.v1.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserRead, Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticación (Log In / Sign Up)"])


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(
    user_in: UserCreate,
    session: Session = Depends(get_db)
):
    """
    Registro de un nuevo usuario en la plataforma JMSHOP.
    """
    auth_service = AuthService(session)
    user = auth_service.register_user(user_in)
    return user


@router.post("/login", response_model=Token)
async def login(
    request: Request,
    session: Session = Depends(get_db)
):
    """
    Inicio de sesión flexible compatible tanto con JSON (email + password)
    como con el botón 'Authorize' de Swagger UI (Form Data).
    """
    auth_service = AuthService(session)
    email: str = ""
    password: str = ""

    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        try:
            body = await request.json()
            email = str(body.get("email", "")).strip()
            password = str(body.get("password", ""))
        except Exception:
            pass
    elif "x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        try:
            form = await request.form()
            email = str(form.get("username") or form.get("email") or "").strip()
            password = str(form.get("password", ""))
        except Exception:
            pass
    else:
        try:
            body = await request.json()
            email = str(body.get("email", "")).strip()
            password = str(body.get("password", ""))
        except Exception:
            pass

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe proporcionar 'email' (o 'username') y 'password'."
        )

    credentials = UserLogin(email=email, password=password)
    user = auth_service.authenticate_user(credentials)
    return auth_service.generate_token(user)


@router.get("/me", response_model=UserRead)
def read_current_user(
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene los datos del usuario actualmente autenticado mediante el Token JWT.
    """
    return current_user
