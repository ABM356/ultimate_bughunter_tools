"""Async Elasticsearch client for log/alert aggregation."""

from __future__ import annotations

from typing import Optional

from elasticsearch import AsyncElasticsearch

from app.core.config import settings

_client: Optional[AsyncElasticsearch] = None


def get_es() -> AsyncElasticsearch:
    """Return a shared AsyncElasticsearch client instance."""
    global _client
    if _client is None:
        kwargs: dict = {"hosts": [settings.ELASTICSEARCH_URL]}
        if settings.ELASTICSEARCH_USERNAME and settings.ELASTICSEARCH_PASSWORD:
            kwargs["basic_auth"] = (
                settings.ELASTICSEARCH_USERNAME,
                settings.ELASTICSEARCH_PASSWORD,
            )
        _client = AsyncElasticsearch(**kwargs)
    return _client


async def close_es() -> None:
    global _client
    if _client is not None:
        await _client.close()
        _client = None
