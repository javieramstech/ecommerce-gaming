from typing import Optional
from sqlmodel import Session, select
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repositorio especializado para la entidad User.
    """

    def __init__(self, session: Session):
        super().__init__(User, session)

    def get_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por su dirección de correo electrónico (insensible a mayúsculas)."""
        statement = select(User).where(User.email == email.lower().strip())
        return self.session.exec(statement).first()
