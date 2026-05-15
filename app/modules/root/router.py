from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.common.responses import success_response
from app.core.config import get_settings

router = APIRouter(tags=["root"])


@router.get("/")
def root(request: Request) -> JSONResponse:
    settings = get_settings()
    return success_response(
        request,
        data={
            "name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "docs": f"{settings.api_prefix}/docs",
            "health": "/health",
        },
    )
