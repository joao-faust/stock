from pydantic import BaseModel, EmailStr, Field


class RegisterSchema(BaseModel):
    name: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8)
    confirm_password: str = Field()


class DeleteSchema(BaseModel):
    password: str = Field()


class UpdateUserSchema(BaseModel):
    name: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
    password: str = Field()
