"""Threat-intel feed integrations (MISP, AlienVault OTX)."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


async def fetch_otx_pulses(modified_since: Optional[str] = None) -> List[Dict[str, Any]]:
    if not settings.OTX_API_KEY:
        logger.info("OTX_API_KEY not set; returning empty pulses")
        return []
    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    params: Dict[str, Any] = {}
    if modified_since:
        params["modified_since"] = modified_since
    headers = {"X-OTX-API-KEY": settings.OTX_API_KEY}
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
    return resp.json().get("results", [])


async def fetch_misp_events(limit: int = 50) -> List[Dict[str, Any]]:
    if not settings.MISP_URL or not settings.MISP_API_KEY:
        logger.info("MISP not configured; returning empty events")
        return []
    url = f"{settings.MISP_URL.rstrip('/')}/events/restSearch"
    headers = {
        "Authorization": settings.MISP_API_KEY,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=30.0, verify=False) as client:
        resp = await client.post(url, headers=headers, json={"limit": limit})
        resp.raise_for_status()
    return resp.json().get("response", [])
