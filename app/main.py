from fastapi import FastAPI

from app.core.exceptions import register_exception_handlers
from app.routers.tokens import tokens_router
from app.routers.movements import movements_router
from app.routers.products import products_router
from app.routers.users import users_router

app = FastAPI()

register_exception_handlers(app)
app.include_router(products_router)
app.include_router(movements_router)
app.include_router(users_router)
app.include_router(tokens_router)
