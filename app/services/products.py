from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.core.exceptions import NotFoundError, ValidationError
from app.core.security import DecodedToken
from app.models.products import Product
from app.repositories.products import ProductRepositoryABC, get_product_repository
from app.schemas.products import (
    CreateProductSchema,
    UpdateProductSchema,
    UpdateProductStatusSchema,
)


class ProductServiceABC(ABC):
    @abstractmethod
    def create(self, data: CreateProductSchema, decoded_token: DecodedToken) -> Product: ...

    @abstractmethod
    def list(self) -> Sequence[Product]: ...

    @abstractmethod
    def list_low_stock(self) -> Sequence[Product]: ...

    @abstractmethod
    def get_by_id(self, id: int) -> Product: ...

    @abstractmethod
    def update_by_id(self, id: int, data: UpdateProductSchema) -> None: ...

    @abstractmethod
    def delete_by_id(self, id: int) -> None: ...

    @abstractmethod
    def update_status_by_id(self, id: int, data: UpdateProductStatusSchema) -> None: ...


class ProductService(ProductServiceABC):
    def __init__(self, product_repository: ProductRepositoryABC):
        self.product_repository = product_repository

    def create(self, data: CreateProductSchema, decoded_token: DecodedToken):
        product = Product(**data.model_dump())
        product.user_id = decoded_token.id

        return self.product_repository.create(product)

    def list(self):
        return self.product_repository.list()

    def list_low_stock(self):
        return self.product_repository.list_low_stock()

    def get_by_id(self, id: int):
        product = self.product_repository.get_by_id(id)

        if product is None:
            raise NotFoundError("Product not found")

        return product

    def update_by_id(self, id: int, data: UpdateProductSchema):
        product = self.get_by_id(id)

        product.name = data.name
        product.minimum_quantity = data.minimum_quantity

        self.product_repository.update(product)

    def delete_by_id(self, id: int):
        product = self.get_by_id(id)

        if product and len(product.movements) > 0:
            raise ValidationError("Product has movements")

        self.product_repository.delete(product)

    def update_status_by_id(self, id: int, data: UpdateProductStatusSchema):
        product = self.get_by_id(id)

        product.is_active = data.is_active

        self.product_repository.update(product)


def get_product_service():
    return ProductService(get_product_repository())
