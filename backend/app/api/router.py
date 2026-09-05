"""Main API router."""

from fastapi import APIRouter
from app.api.v1.api_router import api_router as v1_router

api_router = APIRouter()


@api_router.get("/health", tags=["health"])
@api_router.get("/api/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "AI Finance Controller"}


api_router.include_router(v1_router, prefix="/api")
