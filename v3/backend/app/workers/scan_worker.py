"""Celery tasks for executing scans asynchronously."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from typing import Any, Dict
from uuid import UUID

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.scan import Scan
from app.services.scanner_service import get_scanner_service
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


async def _run(scan_id: str) -> Dict[str, Any]:
    sid = UUID(scan_id)
    async with AsyncSessionLocal() as db:
        scan = (await db.execute(select(Scan).where(Scan.id == sid))).scalar_one_or_none()
        if scan is None:
            return {"error": "scan not found"}
        scan.status = "running"
        scan.started_at = datetime.now(timezone.utc)
        scan.tools_used = get_scanner_service().tools_for_level(scan.scan_level)
        await db.commit()

        try:
            result = await get_scanner_service().execute(
                scan_id=scan.id,
                scan_type=scan.scan_type,
                scan_level=scan.scan_level,
                target=scan.target,
            )
            scan.raw_output = result
            scan.findings_count = sum(
                len(v.get("findings", [])) if isinstance(v, dict) else 0
                for v in result.get("results", {}).values()
            )
            scan.status = "completed"
        except Exception as exc:
            logger.exception("Scan failed")
            scan.status = "failed"
            scan.error_message = str(exc)
        scan.completed_at = datetime.now(timezone.utc)
        await db.commit()
        return {"scan_id": scan_id, "status": scan.status}


@celery_app.task(name="scan.run", bind=True, max_retries=2)
def run_scan(self, scan_id: str) -> Dict[str, Any]:  # type: ignore[override]
    return asyncio.run(_run(scan_id))
