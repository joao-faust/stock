from pydantic import BaseModel, ConfigDict, Field

from app.models.movements import MovementType


class CreateMovementSchema(BaseModel):
    product_id: int = Field()
    quantity: int = Field(gt=0)
    type: MovementType = Field()


class MovementResponseBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    type: MovementType


class MovementListResponseSchema(BaseModel):
    movements: list[MovementResponseBaseSchema]
