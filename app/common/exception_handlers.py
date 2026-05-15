import logging
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.common.errors import AppException
from app.common.responses import error_response
from app.core.config import get_settings

logger = logging.getLogger(__name__)

_STATUS_CODES: dict[int, str] = {
    status.HTTP_400_BAD_REQUEST: "BAD_REQUEST",
    status.HTTP_401_UNAUTHORIZED: "UNAUTHORIZED",
    status.HTTP_403_FORBIDDEN: "FORBIDDEN",
    status.HTTP_404_NOT_FOUND: "NOT_FOUND",
    status.HTTP_405_METHOD_NOT_ALLOWED: "METHOD_NOT_ALLOWED",
    status.HTTP_409_CONFLICT: "CONFLICT",
    status.HTTP_422_UNPROCESSABLE_CONTENT: "VALIDATION_ERROR",
    status.HTTP_500_INTERNAL_SERVER_ERROR: "INTERNAL_ERROR",
}


def _string_detail(detail: Any, fallback: str) -> str:
    if isinstance(detail, str):
        return detail
    return fallback


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return error_response(
        request,
        code=exc.code,
        message=exc.message,
        status_code=exc.status_code,
        details=exc.details,
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    code = _STATUS_CODES.get(exc.status_code, "HTTP_ERROR")
    message = _string_detail(exc.detail, "HTTP error")

    if exc.status_code == status.HTTP_404_NOT_FOUND:
        message = "The requested endpoint was not found."
    elif exc.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
        message = "Method not allowed for this endpoint."

    return error_response(request, code=code, message=message, status_code=exc.status_code)


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = exc.errors()
    is_invalid_json = any(error.get("type") == "json_invalid" for error in errors)

    if is_invalid_json:
        return error_response(
            request,
            code="INVALID_JSON",
            message="Request body contains invalid JSON.",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=errors,
        )

    return error_response(
        request,
        code="VALIDATION_ERROR",
        message="Request validation failed.",
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        details=errors,
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled application error", exc_info=exc)
    settings = get_settings()
    message = str(exc) if settings.debug else "Internal server error."
    return error_response(
        request,
        code="INTERNAL_ERROR",
        message=message,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)  # type: ignore[arg-type]
