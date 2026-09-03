from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import DecodedToken, decode_jwt
from app.schemas.products import (
    CreateProductSchema,
    ProductListResponseSchema,
    ProductResponseSchema,
    UpdateProductSchema,
    UpdateProductStatusSchema,
)
from app.services.products import ProductServiceABC, get_product_service

products_router = APIRouter(prefix="/products", dependencies=[Depends(decode_jwt)])


@products_router.post("/", status_code=201)
async def create_product(
    data: CreateProductSchema,
    product_service: Annotated[ProductServiceABC, Depends(get_product_service)],
    decoded_token: Annotated[DecodedToken, Depends(decode_jwt)],
):
    product = product_service.create(data, decoded_token)
    
    return {"id": product.id}


@products_router.get("/", response_model=ProductListResponseSchema)
async def list_products(
    product_service: Annotated[ProductServiceABC, Depends(get_product_service)],
):
    return {"products": product_service.list()}


@products_router.get("/low-stock", response_model=ProductListResponseSchema)
async def list_low_stock_products(
    product_service: Annotated[ProductServiceABC, Depends(get_product_service)],
):
    return {"products": product_service.list_low_stock()}


@products_router.get("/{id}", response_model=ProductResponseSchema)
async def get_product_by_id(
    id: int,
    product_service: Annotated[ProductServiceABC, Depends(get_product_service)],
):
    return {"product": product_service.get_by_id(id)}


@products_router.put("/{id}", status_code=204)
async def update_product_by_id(
    id: int,
    data: UpdateProductSchema,
    product_service: Annotated[ProductServiceABC, Depends(get_product_service)],
):
    product_service.update_by_id(id, data)


@products_router.put("/{id}/status", status_code=204)
async def update_product_status_by_id(
    id: int,
    data: UpdateProductStatusSchema,
    product_service: Annotated[ProductServiceABC, Depends(get_product_service)],
):
    product_service.update_status_by_id(id, data)


@products_router.delete("/{id}", status_code=204)
async def delete_product_by_id(
    id: int,
    product_service: Annotated[ProductServiceABC, Depends(get_product_service)],
):
    product_service.delete_by_id(id)
