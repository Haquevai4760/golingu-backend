"""
GoLingu - Health Endpoint
GET /health — liveness probe for load balancers and orchestrators.
"""

from fastapi import APIRouter, status

from app.core.config import settings
from app.schemas.translation import HealthResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Returns the API status. Used by load balancers and uptime monitors.",
)
async def health() -> HealthResponse:
    """Liveness probe — always returns 200 when the service is running."""
    return HealthResponse(
        status="ok",
        version=settings.APP_VERSION,
        service=settings.APP_NAME,
    )
