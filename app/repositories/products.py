from abc import ABC, abstractmethod
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.products import Product


class ProductRepositoryABC(ABC):
    @abstractmethod
    def create(self, product: Product) -> Product: ...

    @abstractmethod
    def list(self) -> Sequence[Product]: ...

    @abstractmethod
    def list_low_stock(self) -> Sequence[Product]: ...

    @abstractmethod
    def get_by_id(self, id: int) -> Product | None: ...

    @abstractmethod
    def update(self, product: Product) -> None: ...

    @abstractmethod
    def delete(self, product: Product) -> None: ...



class ProductRepository(ProductRepositoryABC):
    def __init__(self, db: Session):
        self.db = db

    def create(self, product: Product):
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)

        return product

    def list(self):
        stmt = select(Product)

        return self.db.scalars(stmt).all()

    def list_low_stock(self):
        stmt = (
            select(Product)
            .where(Product.quantity <= Product.minimum_quantity)
            .where(Product.is_active.is_(True))
        )

        return self.db.scalars(stmt).all()

    def get_by_id(self, id: int):
        return self.db.get(Product, id)

    def update(self, product: Product):
        self.db.merge(product)
        self.db.commit()

    def delete(self, product: Product):
        self.db.delete(product)
        self.db.commit()


def get_product_repository():
    return ProductRepository(next(get_db()))
