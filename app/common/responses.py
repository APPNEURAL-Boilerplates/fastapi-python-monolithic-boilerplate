from typing import Any

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def request_id_from(request: Request) -> str | None:
    return getattr(request.state, "request_id", None)


def success_response(
    request: Request,
    data: Any = None,
    *,
    status_code: int = status.HTTP_200_OK,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(
            {
                "ok": True,
                "data": data,
                "requestId": request_id_from(request),
            }
        ),
    )


def error_response(
    request: Request,
    *,
    code: str,
    message: str,
    status_code: int,
    details: Any = None,
) -> JSONResponse:
    body: dict[str, Any] = {
        "ok": False,
        "error": {
            "code": code,
            "message": message,
        },
        "requestId": request_id_from(request),
    }
    if details is not None:
        body["error"]["details"] = details

    return JSONResponse(status_code=status_code, content=jsonable_encoder(body))
