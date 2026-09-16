from fastapi import HTTPException, status
from sqlmodel import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token
from app.repositories.user_repository import UserRepository
from app.core.security import get_password_hash, verify_password, create_access_token


class AuthService:
    """
    Servicio encargado de la lógica de negocio de autenticación y usuarios.
    """

    def __init__(self, session: Session):
        self.user_repo = UserRepository(session)

    def register_user(self, user_in: UserCreate) -> User:
        """Registra un nuevo usuario en el sistema verificando que el email sea único."""
        existing_user = self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya se encuentra registrado."
            )

        hashed_pwd = get_password_hash(user_in.password)
        db_user = User(
            email=user_in.email.lower().strip(),
            full_name=user_in.full_name.strip(),
            hashed_password=hashed_pwd,
            is_active=True,
            is_admin=False
        )
        return self.user_repo.create(db_user)

    def authenticate_user(self, credentials: UserLogin) -> User:
        """Autentica las credenciales de usuario."""
        user = self.user_repo.get_by_email(credentials.email)
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo electrónico o contraseña incorrectos.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La cuenta de usuario se encuentra inactiva."
            )
        return user

    def generate_token(self, user: User) -> Token:
        """Genera un token JWT de acceso para el usuario especificado."""
        token_str = create_access_token(subject=str(user.id))
        return Token(access_token=token_str, token_type="bearer")
