from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class ValidationError(Exception): ...


class NotFoundError(Exception): ...


class UnauthorizedError(Exception): ...


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, error: ValidationError):
        return JSONResponse(status_code=422, content={"detail": str(error)})

    @app.exception_handler(NotFoundError)
    async def not_found_error_handler(request: Request, error: NotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(error)})

    @app.exception_handler(UnauthorizedError)
    async def unauthorized_error_handler(request: Request, error: UnauthorizedError):
        return JSONResponse(status_code=401, content={"detail": str(error)})

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, error: Exception):
        return JSONResponse(status_code=500, content={"detail": "Internal error"})
