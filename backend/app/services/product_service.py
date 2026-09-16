import json
from typing import List, Optional
from fastapi import HTTPException, status
from sqlmodel import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductRead, ProductFilterParams
from app.repositories.product_repository import ProductRepository


class ProductService:
    """
    Servicio desacoplado para gestión de catálogo de Productos y Servicios.
    """

    def __init__(self, session: Session):
        self.product_repo = ProductRepository(session)

    def _to_read_schema(self, product: Product) -> ProductRead:
        """Convierte una entidad Product SQLModel a su esquema DTO Pydantic."""
        try:
            specs_list = json.loads(product.specs_json) if product.specs_json else []
        except Exception:
            specs_list = []

        return ProductRead(
            id=product.id,
            title=product.title,
            category=product.category,
            type=product.type,
            price=product.price,
            badge=product.badge,
            image=product.image,
            short_desc=product.short_desc,
            full_desc=product.full_desc,
            specs=specs_list,
            stock=product.stock,
            is_active=product.is_active,
            created_at=product.created_at,
        )

    def create_product(self, product_in: ProductCreate) -> ProductRead:
        """Crea un nuevo producto en el catálogo."""
        specs_json_str = json.dumps(product_in.specs)
        db_product = Product(
            title=product_in.title.strip(),
            category=product_in.category.lower().strip(),
            type=product_in.type.lower().strip(),
            price=product_in.price,
            badge=product_in.badge.strip() if product_in.badge else None,
            image=product_in.image.strip(),
            short_desc=product_in.short_desc.strip(),
            full_desc=product_in.full_desc.strip(),
            specs_json=specs_json_str,
            stock=product_in.stock,
            is_active=True
        )
        saved_product = self.product_repo.create(db_product)
        return self._to_read_schema(saved_product)

    def get_product_by_id(self, product_id: int) -> ProductRead:
        """Obtiene un producto por su ID."""
        product = self.product_repo.get_by_id(product_id)
        if not product or not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El producto con ID {product_id} no fue encontrado."
            )
        return self._to_read_schema(product)

    def list_products(self, params: ProductFilterParams) -> List[ProductRead]:
        """Obtiene una lista de productos aplicando los filtros solicitados."""
        products = self.product_repo.get_filtered(params)
        return [self._to_read_schema(p) for p in products]

    def update_product(self, product_id: int, product_in: ProductUpdate) -> ProductRead:
        """Actualiza un producto existente de forma parcial."""
        db_product = self.product_repo.get_by_id(product_id)
        if not db_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El producto con ID {product_id} no fue encontrado."
            )

        update_dict = product_in.model_dump(exclude_unset=True)
        if "specs" in update_dict and update_dict["specs"] is not None:
            update_dict["specs_json"] = json.dumps(update_dict.pop("specs"))

        updated_product = self.product_repo.update(db_product, update_dict)
        return self._to_read_schema(updated_product)

    def delete_product(self, product_id: int) -> bool:
        """Elimina un producto por ID."""
        db_product = self.product_repo.get_by_id(product_id)
        if not db_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El producto con ID {product_id} no fue encontrado."
            )
        return self.product_repo.delete(product_id)
