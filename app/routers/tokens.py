from typing import Annotated

from fastapi import APIRouter, Depends

from app.schemas.tokens import CreateTokenSchema
from app.services.tokens import TokenServiceABC, get_token_service

tokens_router = APIRouter(prefix="/tokens")


@tokens_router.post("/")
async def create_token(
    data: CreateTokenSchema,
    token_service: Annotated[TokenServiceABC, Depends(get_token_service)],
):
    return {"token": token_service.create(data)}
