from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import DecodedToken, decode_jwt
from app.schemas.users import DeleteSchema, RegisterSchema, UpdateUserSchema
from app.services.users import UsersServiceABC, get_user_service

users_router = APIRouter(prefix="/users")


@users_router.post("/", status_code=201)
async def create(
    data: RegisterSchema,
    user_service: Annotated[UsersServiceABC, Depends(get_user_service)],
):
    user = user_service.create(data)

    return {"id": user.id}


@users_router.put("/", status_code=204)
async def update(
    data: UpdateUserSchema,
    user_service: Annotated[UsersServiceABC, Depends(get_user_service)],
    decoded_token: Annotated[DecodedToken, Depends(decode_jwt)],
):
    user_service.update(data, decoded_token)


@users_router.delete("/", status_code=204)
async def delete(
    data: DeleteSchema,
    user_service: Annotated[UsersServiceABC, Depends(get_user_service)],
    decoded_token: Annotated[DecodedToken, Depends(decode_jwt)],
):
    user_service.delete(data, decoded_token)
