from typing import List, Optional
from sqlmodel import Session, select, or_, col
from app.models.product import Product
from app.schemas.product import ProductFilterParams
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """
    Repositorio especializado para consultas y filtrado dinámico de Productos y Servicios.
    """

    def __init__(self, session: Session):
        super().__init__(Product, session)

    def get_filtered(self, params: ProductFilterParams) -> List[Product]:
        """
        Aplica filtros dinámicos por categoría, tipo, búsqueda por palabras clave,
        rango de precios, ordenamiento y paginación.
        """
        statement = select(Product).where(Product.is_active == True)

        # Filtro por Categoría
        if params.category and params.category.lower() != "all":
            statement = statement.where(Product.category == params.category.lower())

        # Filtro por Tipo (producto / servicio)
        if params.type and params.type.lower() != "all":
            statement = statement.where(Product.type == params.type.lower())

        # Búsqueda libre en título o descripción
        if params.search and params.search.strip():
            search_pattern = f"%{params.search.strip()}%"
            statement = statement.where(
                or_(
                    col(Product.title).ilike(search_pattern),
                    col(Product.short_desc).ilike(search_pattern),
                    col(Product.full_desc).ilike(search_pattern),
                )
            )

        # Rango de Precios
        if params.min_price is not None:
            statement = statement.where(Product.price >= params.min_price)
        if params.max_price is not None:
            statement = statement.where(Product.price <= params.max_price)

        # Ordenamiento
        if params.sort_by == "price_asc":
            statement = statement.order_by(Product.price.asc())
        elif params.sort_by == "price_desc":
            statement = statement.order_by(Product.price.desc())
        elif params.sort_by == "title_asc":
            statement = statement.order_by(Product.title.asc())
        else:
            # Por defecto: del más reciente al más antiguo
            statement = statement.order_by(Product.created_at.desc())

        # Paginación
        statement = statement.offset(params.offset).limit(params.limit)

        return list(self.session.exec(statement).all())
