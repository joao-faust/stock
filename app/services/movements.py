from abc import ABC, abstractmethod
from collections.abc import Sequence

from app.core.exceptions import ValidationError
from app.models.movements import Movement, MovementType
from app.repositories.movements import MovementRepositoryABC, get_movement_repository
from app.schemas.movements import CreateMovementSchema
from app.services.products import ProductServiceABC, get_product_service


class MovementServiceABC(ABC):
    @abstractmethod
    def create(self, data: CreateMovementSchema) -> Movement: ...

    @abstractmethod
    def list_by_product_id(self, product_id: int) -> Sequence[Movement]: ...


class MovementService(MovementServiceABC):
    def __init__(
        self,
        movement_repository: MovementRepositoryABC,
        product_service: ProductServiceABC,
    ):
        self.movement_repository = movement_repository
        self.product_service = product_service

    def create(self, data: CreateMovementSchema):
        product = self.product_service.get_by_id(data.product_id)

        if not product.is_active:
            raise ValidationError("Product inactive")
        if data.type == MovementType.OUT and product.quantity < data.quantity:
            raise ValidationError("Insufficient stock")

        if data.type == MovementType.OUT:
            product.quantity -= data.quantity
        else:
            product.quantity += data.quantity

        movement = Movement(**data.model_dump())
        movement.quantity = data.quantity

        return self.movement_repository.create(movement, product)

    def list_by_product_id(self, product_id: int):
        return self.movement_repository.list_by_product_id(product_id)


def get_movement_service():
    return MovementService(get_movement_repository(), get_product_service())
