"""
GoLingu - API v1 Router
Combines all v1 endpoint routers.
"""

from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.translation import router as translation_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(translation_router)
