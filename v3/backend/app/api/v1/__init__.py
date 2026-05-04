"""Combined v1 API router."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1 import (
    ai,
    auth,
    blue_team,
    bounty,
    infrastructure,
    red_team,
    reports,
    scans,
    scheduling,
    tenants,
    training,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
api_router.include_router(bounty.router, prefix="/bounty", tags=["bounty"])
api_router.include_router(red_team.router, prefix="/red-team", tags=["red-team"])
api_router.include_router(blue_team.router, prefix="/blue-team", tags=["blue-team"])
api_router.include_router(scans.router, prefix="/scans", tags=["scans"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(training.router, prefix="/training", tags=["training"])
api_router.include_router(
    infrastructure.router, prefix="/infrastructure", tags=["infrastructure"]
)
api_router.include_router(scheduling.router, prefix="/scheduling", tags=["scheduling"])
