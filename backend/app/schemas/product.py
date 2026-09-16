from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    """Atributos comunes del producto."""
    title: str
    category: str
    type: str
    price: float = Field(..., ge=0.0)
    badge: Optional[str] = None
    image: str
    short_desc: str
    full_desc: str
    specs: List[str] = Field(default_factory=list)
    stock: int = Field(default=10, ge=0)


class ProductCreate(ProductBase):
    """Esquema para crear un nuevo producto o servicio."""
    pass


class ProductUpdate(BaseModel):
    """Esquema para actualización parcial (PUT/PATCH)."""
    title: Optional[str] = None
    category: Optional[str] = None
    type: Optional[str] = None
    price: Optional[float] = Field(default=None, ge=0.0)
    badge: Optional[str] = None
    image: Optional[str] = None
    short_desc: Optional[str] = None
    full_desc: Optional[str] = None
    specs: Optional[List[str]] = None
    stock: Optional[int] = Field(default=None, ge=0)
    is_active: Optional[bool] = None


class ProductRead(ProductBase):
    """Esquema de salida para respuesta API."""
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductFilterParams(BaseModel):
    """Filtros disponibles para la consulta de catálogo."""
    category: Optional[str] = None
    type: Optional[str] = None
    search: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    sort_by: Optional[str] = "created_at_desc" # price_asc, price_desc, title_asc, created_at_desc
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
