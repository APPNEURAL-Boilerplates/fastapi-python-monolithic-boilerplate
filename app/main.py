from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.common.exception_handlers import register_exception_handlers
from app.common.middleware.request_id import RequestIdMiddleware
from app.common.middleware.security_headers import SecurityHeadersMiddleware
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.modules.health.router import router as health_router
from app.modules.root.router import router as root_router
from app.modules.users.repository import InMemoryUserRepository
from app.modules.users.service import UserService


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        docs_url=f"{settings.api_prefix}/docs",
        redoc_url=f"{settings.api_prefix}/redoc",
        openapi_url=f"{settings.api_prefix}/openapi.json",
    )

    # Application-scoped dependencies. Replace with real database-backed services later.
    app.state.user_service = UserService(InMemoryUserRepository())

    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

    register_exception_handlers(app)

    app.include_router(root_router)
    app.include_router(health_router)
    app.include_router(api_router, prefix=settings.api_prefix)

    return app


app = create_app()
