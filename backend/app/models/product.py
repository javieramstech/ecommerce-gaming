from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    """
    Modelo de datos para la entidad Producto / Servicio en SQLite 3.
    """
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, nullable=False)
    category: str = Field(index=True, nullable=False)  # hardware, notebooks, software, servicios
    type: str = Field(index=True, nullable=False)      # producto, servicio
    price: float = Field(nullable=False, ge=0.0)
    badge: Optional[str] = Field(default=None)
    image: str = Field(nullable=False)
    short_desc: str = Field(nullable=False)
    full_desc: str = Field(nullable=False)
    specs_json: Optional[str] = Field(default="[]")     # Lista de especificaciones en JSON string
    stock: int = Field(default=10, nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
