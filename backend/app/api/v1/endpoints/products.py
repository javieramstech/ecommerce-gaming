from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query
from sqlmodel import Session
from app.api.v1.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductRead,
    ProductFilterParams
)
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["CRUD Productos & Filtros"])


@router.get("", response_model=List[ProductRead])
def list_products(
    category: Optional[str] = Query(default=None, description="Categoría (hardware, notebooks, software, servicios)"),
    type: Optional[str] = Query(default=None, description="Tipo (producto, servicio)"),
    search: Optional[str] = Query(default=None, description="Término de búsqueda en título o descripción"),
    min_price: Optional[float] = Query(default=None, description="Precio mínimo"),
    max_price: Optional[float] = Query(default=None, description="Precio máximo"),
    sort_by: Optional[str] = Query(default="created_at_desc", description="Ordenamiento (price_asc, price_desc, title_asc, created_at_desc)"),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: Session = Depends(get_db)
):
    """
    Obtiene el catálogo de productos aplicando filtros dinámicos por categoría, tipo, precio y texto.
    """
    params = ProductFilterParams(
        category=category,
        type=type,
        search=search,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by,
        limit=limit,
        offset=offset
    )
    product_service = ProductService(session)
    return product_service.list_products(params)


@router.get("/{product_id}", response_model=ProductRead)
def get_product(
    product_id: int,
    session: Session = Depends(get_db)
):
    """
    Obtiene el detalle de un producto o servicio por su ID.
    """
    product_service = ProductService(session)
    return product_service.get_product_by_id(product_id)


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """
    Crea un nuevo producto o servicio en el catálogo (Requiere estar autenticado).
    """
    product_service = ProductService(session)
    return product_service.create_product(product_in)


@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """
    Actualiza parcialmente un producto o servicio existente (Requiere estar autenticado).
    """
    product_service = ProductService(session)
    return product_service.update_product(product_id, product_in)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """
    Elimina un producto o servicio del catálogo (Requiere estar autenticado).
    """
    product_service = ProductService(session)
    product_service.delete_product(product_id)
    return None
