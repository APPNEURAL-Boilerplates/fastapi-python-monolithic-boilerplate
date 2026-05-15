from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.common.responses import success_response
from app.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check(request: Request) -> JSONResponse:
    settings = get_settings()
    return success_response(
        request,
        data={
            "status": "healthy",
            "service": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
        },
    )
