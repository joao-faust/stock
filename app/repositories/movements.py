from abc import ABC, abstractmethod
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.movements import Movement
from app.models.products import Product


class MovementRepositoryABC(ABC):
    @abstractmethod
    def create(self, movement: Movement, product: Product) -> Movement: ...

    @abstractmethod
    def list_by_product_id(self, product_id: int) -> Sequence[Movement]: ...


class MovementRepository(MovementRepositoryABC):
    def __init__(self, db: Session):
        self.db = db

    def create(self, movement: Movement, product: Product):
        self.db.add(movement)
        self.db.merge(product)
        self.db.commit()
        self.db.refresh(movement)

        return movement

    def list_by_product_id(self, product_id: int):
        stmt = select(Movement).where(Movement.product_id == product_id)

        return self.db.scalars(stmt).all()


def get_movement_repository():
    return MovementRepository(next(get_db()))
