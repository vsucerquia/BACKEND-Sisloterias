from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from core.exceptions import AppException


async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.message,
        },
    )


async def integrity_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=409,
        content={
            "success": False,
            "error": "Conflicto de integridad en la base de datos",
        },
    )


async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Error interno del servidor",
        },
    )
