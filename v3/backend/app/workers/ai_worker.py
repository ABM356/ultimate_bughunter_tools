"""Background AI processing tasks."""

from __future__ import annotations

import asyncio
from typing import Any, Dict, List

from app.services.ai_service import get_ai_service
from app.workers.celery_app import celery_app


async def _classify(payload: Dict[str, Any]) -> Dict[str, Any]:
    return await get_ai_service().classify_vulnerability(
        title=payload["title"],
        description=payload.get("description", ""),
        evidence=payload.get("evidence"),
        context=payload.get("context"),
    )


async def _risk(payload: Dict[str, Any]) -> Dict[str, Any]:
    return await get_ai_service().risk_score(
        vulnerabilities=payload.get("vulnerabilities", []),
        asset_criticality=payload.get("asset_criticality", 1),
        environmental_factors=payload.get("environmental_factors"),
    )


async def _patterns(payload: Dict[str, Any]) -> Dict[str, Any]:
    return await get_ai_service().threat_pattern_analysis(
        events=payload.get("events", []),
        window_hours=payload.get("window_hours", 24),
    )


@celery_app.task(name="ai.classify_vulnerability")
def classify_vulnerability_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    return asyncio.run(_classify(payload))


@celery_app.task(name="ai.risk_score")
def risk_score_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    return asyncio.run(_risk(payload))


@celery_app.task(name="ai.threat_pattern_analysis")
def threat_pattern_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    return asyncio.run(_patterns(payload))
