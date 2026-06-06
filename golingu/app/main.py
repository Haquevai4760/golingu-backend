"""
GoLingu - Application Entry Point
Creates and configures the FastAPI application.
"""

import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import get_logger, setup_logging
from app.services.gemini_service import gemini_service

# Initialise logging before anything else
setup_logging()
logger = get_logger("main")


# ---------------------------------------------------------------------------
# Lifespan (startup / shutdown)
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application lifecycle: startup and graceful shutdown."""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION} | env={settings.ENV}")
    try:
        gemini_service.initialize()
        logger.info("All services initialised successfully.")
    except Exception as exc:
        logger.critical(f"Failed to initialise services: {exc}")
        raise

    yield  # Application is running

    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME}.")


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------

def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "GoLingu is a production-ready translation API powered by Google Gemini. "
            "Supports 100+ languages with auto source-language detection."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # -----------------------------------------------------------------------
    # Middleware
    # -----------------------------------------------------------------------

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )

    # Request timing / logging middleware
    @app.middleware("http")
    async def request_logger(request: Request, call_next) -> Response:
        start = time.perf_counter()
        response: Response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            f"{request.method} {request.url.path} | "
            f"status={response.status_code} duration={duration_ms:.1f}ms"
        )
        response.headers["X-Process-Time-Ms"] = f"{duration_ms:.1f}"
        return response

    # -----------------------------------------------------------------------
    # Global Exception Handlers
    # -----------------------------------------------------------------------

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(f"Unhandled exception on {request.url.path}: {exc}")
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred. Please try again later.",
                }
            },
        )

    # -----------------------------------------------------------------------
    # Routers
    # -----------------------------------------------------------------------

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    # Root redirect to docs
    @app.get("/", include_in_schema=False)
    async def root() -> JSONResponse:
        return JSONResponse(
            content={
                "service": settings.APP_NAME,
                "version": settings.APP_VERSION,
                "docs": "/docs",
                "health": f"{settings.API_V1_PREFIX}/health",
            }
        )

    logger.info(
        f"Application configured | "
        f"routes={len(app.routes)} cors_origins={settings.ALLOWED_ORIGINS}"
    )
    return app


# ---------------------------------------------------------------------------
# WSGI / ASGI entry point
# ---------------------------------------------------------------------------

app = create_application()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
