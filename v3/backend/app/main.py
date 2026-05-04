"""FastAPI application factory."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import api_router
from app.core.config import settings
from app.core.database import dispose_engine
from app.core.elasticsearch_client import close_es
from app.core.redis_client import close_redis

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Starting %s in %s mode", settings.PROJECT_NAME, settings.ENVIRONMENT)
    try:
        yield
    finally:
        logger.info("Shutting down %s", settings.PROJECT_NAME)
        await dispose_engine()
        await close_redis()
        await close_es()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    @app.get("/health", tags=["health"])
    async def health() -> JSONResponse:
        return JSONResponse(
            {
                "status": "ok",
                "service": settings.PROJECT_NAME,
                "environment": settings.ENVIRONMENT,
            }
        )

    @app.get("/", tags=["root"])
    async def root() -> JSONResponse:
        return JSONResponse(
            {"service": settings.PROJECT_NAME, "docs": "/docs", "health": "/health"}
        )

    return app


app = create_app()
