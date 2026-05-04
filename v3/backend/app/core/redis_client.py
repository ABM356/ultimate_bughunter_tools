"""Async Redis connection pool."""

from __future__ import annotations

from typing import Optional

from redis.asyncio import ConnectionPool, Redis

from app.core.config import settings

_pool: Optional[ConnectionPool] = None


def get_pool() -> ConnectionPool:
    global _pool
    if _pool is None:
        _pool = ConnectionPool.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            max_connections=50,
        )
    return _pool


def get_redis() -> Redis:
    """Return a Redis client backed by the shared pool."""
    return Redis(connection_pool=get_pool())


async def close_redis() -> None:
    global _pool
    if _pool is not None:
        await _pool.disconnect(inuse_connections=True)
        _pool = None
