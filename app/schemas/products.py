from pydantic import BaseModel, ConfigDict, Field


class CreateProductSchema(BaseModel):
    name: str = Field(min_length=5, max_length=255)
    minimum_quantity: int = Field(gt=0)


class UpdateProductSchema(BaseModel):
    name: str = Field(min_length=5, max_length=255)
    minimum_quantity: int = Field(gt=0)


class UpdateProductStatusSchema(BaseModel):
    is_active: bool


class ProductResponseBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    is_active: bool
    quantity: int
    minimum_quantity: int


class ProductResponseSchema(BaseModel):
    product: ProductResponseBaseSchema


class ProductListResponseSchema(BaseModel):
    products: list[ProductResponseBaseSchema]
