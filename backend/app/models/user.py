from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """
    Modelo de datos para la entidad Usuario en SQLite 3.
    """
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    full_name: str = Field(nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    is_admin: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
