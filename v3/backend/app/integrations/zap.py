"""OWASP ZAP API wrapper."""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, Optional

import httpx

logger = logging.getLogger(__name__)

ZAP_BASE_URL = os.getenv("ZAP_BASE_URL", "http://localhost:8080")
ZAP_API_KEY = os.getenv("ZAP_API_KEY", "")


def _get(path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    url = f"{ZAP_BASE_URL}{path}"
    p = dict(params or {})
    if ZAP_API_KEY:
        p["apikey"] = ZAP_API_KEY
    try:
        resp = httpx.get(url, params=p, timeout=30.0)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        logger.warning("ZAP request failed: %s", exc)
        return {"error": str(exc)}


def spider(target: str) -> Dict[str, Any]:
    return _get("/JSON/spider/action/scan/", {"url": target})


def active_scan(target: str) -> Dict[str, Any]:
    return _get("/JSON/ascan/action/scan/", {"url": target})


def alerts(base_url: str) -> Dict[str, Any]:
    return _get("/JSON/core/view/alerts/", {"baseurl": base_url})
