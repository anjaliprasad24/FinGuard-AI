"""API v1 router assembly."""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, transactions, ocr, policies, goals, copilot, audit

api_router = APIRouter(prefix="/v1")

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(ocr.router, prefix="/ocr", tags=["ocr"])
api_router.include_router(policies.router, prefix="/policies", tags=["policies"])
api_router.include_router(goals.router, prefix="/goals", tags=["goals"])
api_router.include_router(copilot.router, prefix="/copilot", tags=["copilot"])
api_router.include_router(audit.router, prefix="/audit", tags=["audit"])
