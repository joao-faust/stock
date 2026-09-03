from pydantic import BaseModel, EmailStr, Field


class CreateTokenSchema(BaseModel):
    email: EmailStr = Field()
    password: str = Field()
