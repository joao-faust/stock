from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import decode_jwt
from app.schemas.movements import CreateMovementSchema, MovementListResponseSchema
from app.services.movements import MovementServiceABC, get_movement_service

movements_router = APIRouter(prefix="/movements", dependencies=[Depends(decode_jwt)])


@movements_router.post("/", status_code=201)
async def create_movement(
    data: CreateMovementSchema,
    movement_service: Annotated[MovementServiceABC, Depends(get_movement_service)],
):
    movement = movement_service.create(data)

    return {"id": movement.id}


@movements_router.get("/products/{product_id}", response_model=MovementListResponseSchema)
async def list_movements_by_product_id(
    product_id: int,
    movement_service: Annotated[MovementServiceABC, Depends(get_movement_service)],
):
    return {"movements": movement_service.list_by_product_id(product_id)}
