"""Alert correlation and notification dispatch."""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict
from uuid import UUID

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.alert import Alert
from app.services.notification_service import get_notification_service
from app.services.siem_service import get_siem_service
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


async def _correlate(tenant_id: str | None) -> Dict[str, Any]:
    async with AsyncSessionLocal() as db:
        stmt = select(Alert).where(Alert.status == "new").limit(500)
        if tenant_id is not None:
            stmt = stmt.where(Alert.tenant_id == UUID(tenant_id))
        rows = (await db.execute(stmt)).scalars().all()
        events = [{"id": str(a.id), "ip": a.ip, "message": a.message} for a in rows]
        corr_id = get_siem_service().correlate(events)
        if corr_id is None:
            return {"correlated": 0}
        for a in rows:
            a.correlation_id = corr_id
        await db.commit()
        return {"correlated": len(rows), "correlation_id": str(corr_id)}


async def _dispatch(alert_id: str, message: str) -> Dict[str, Any]:
    ok = await get_notification_service().send_slack(message)
    return {"alert_id": alert_id, "slack_sent": ok}


@celery_app.task(name="alert.correlate")
def correlate_alerts_task(tenant_id: str | None = None) -> Dict[str, Any]:
    return asyncio.run(_correlate(tenant_id))


@celery_app.task(name="alert.notify")
def notify_alert_task(alert_id: str, message: str) -> Dict[str, Any]:
    return asyncio.run(_dispatch(alert_id, message))
