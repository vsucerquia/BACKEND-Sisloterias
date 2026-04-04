from pydantic import BaseModel
from typing import Any, Optional


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None


class ApiErrorDetail(BaseModel):
    error: str
    detail: Optional[Any] = None


def success_response(message: str, data: Any = None):
    return {
        "success": True,
        "message": message,
        "data": data
    }


def error_response(message: str, detail: Any = None):
    return {
        "success": False,
        "message": message,
        "detail": detail
    }