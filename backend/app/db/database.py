from typing import Generator
from sqlmodel import SQLModel, Session, create_engine
from app.core.config import settings

# Conexión SQLite 3 habilitando soporte multihilo para desarrollo
connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
engine = create_engine(settings.DATABASE_URL, echo=False, connect_args=connect_args)


def init_db() -> None:
    """Crea las tablas en la base de datos si no existen."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Generador de sesión de SQLModel con cierre automático garantizado.
    Ideal para inyección de dependencias en FastAPI.
    """
    with Session(engine) as session:
        yield session
