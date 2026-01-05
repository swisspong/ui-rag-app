from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.shared.errors import BaseError


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(BaseError)
    async def base_error_handler(
        request: Request,
        exc: BaseError
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error_code": exc.error_code,
                "message": exc.message,
            },
        )

    @app.exception_handler(Exception)
    async def unexpected_error_handler(
        request: Request,
        exc: Exception
    ):
        return JSONResponse(
            status_code=500,
            content={
                "error_code": "UNEXPECTED_ERROR",
                "message": "Unexpected server error",
            },
        )
