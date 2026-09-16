import sys
import os
from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

# Añadir ruta del backend al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.api.v1.deps import get_db

# Engine de prueba en memoria SQLite 3 transaccional
TEST_DATABASE_URL = "sqlite:///:memory:"
engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture(name="session")
def session_fixture() -> Generator[Session, None, None]:
    """
    Crea las tablas en memoria antes de cada test y destruye la BD después de ejecutarse.
    """
    SQLModel.metadata.create_all(engine_test)
    with Session(engine_test) as session:
        yield session
    SQLModel.metadata.drop_all(engine_test)


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    """
    TestClient de FastAPI configurado con la sesión en memoria inyectada.
    """
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
