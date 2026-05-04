"""Blue-team operations: alerts (SSE), incidents, log search."""

from __future__ import annotations

import asyncio
import json
from typing import AsyncGenerator, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.redis_client import get_redis
from app.core.security import enforce_tenant, get_current_user
from app.models.alert import Alert
from app.models.incident import Incident
from app.models.user import User
from app.schemas.alert import AlertCreate, AlertRead, AlertUpdate
from app.schemas.common import MessageResponse
from app.schemas.incident import IncidentCreate, IncidentRead, IncidentUpdate
from app.services.siem_service import get_siem_service

router = APIRouter()

ALERT_CHANNEL = "alerts:stream"


# ---------------------------------------------------------------------------
# Alerts
# ---------------------------------------------------------------------------
@router.post("/alerts", response_model=AlertRead, status_code=status.HTTP_201_CREATED)
async def create_alert(
    payload: AlertCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AlertRead:
    alert = Alert(tenant_id=user.tenant_id, **payload.model_dump())
    db.add(alert)
    await db.commit()
    await db.refresh(alert)
    redis = get_redis()
    await redis.publish(
        ALERT_CHANNEL,
        json.dumps(
            {
                "id": str(alert.id),
                "tenant_id": str(alert.tenant_id) if alert.tenant_id else None,
                "severity": alert.severity,
                "message": alert.message,
            }
        ),
    )
    return AlertRead.model_validate(alert, from_attributes=True)


@router.get("/alerts", response_model=list[AlertRead])
async def list_alerts(
    severity: Optional[str] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[AlertRead]:
    stmt = select(Alert)
    if user.tenant_id is not None:
        stmt = stmt.where(Alert.tenant_id == user.tenant_id)
    if severity:
        stmt = stmt.where(Alert.severity == severity)
    if status_filter:
        stmt = stmt.where(Alert.status == status_filter)
    rows = (await db.execute(stmt.order_by(Alert.created_at.desc()))).scalars().all()
    return [AlertRead.model_validate(a, from_attributes=True) for a in rows]


@router.patch("/alerts/{alert_id}", response_model=AlertRead)
async def update_alert(
    alert_id: UUID,
    payload: AlertUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> AlertRead:
    alert = (
        await db.execute(select(Alert).where(Alert.id == alert_id))
    ).scalar_one_or_none()
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    enforce_tenant(user, alert.tenant_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(alert, field, value)
    await db.commit()
    await db.refresh(alert)
    return AlertRead.model_validate(alert, from_attributes=True)


@router.get("/alerts/stream")
async def alerts_stream(
    user: User = Depends(get_current_user),
) -> StreamingResponse:
    """Server-sent-events stream of new alerts."""

    async def event_generator() -> AsyncGenerator[bytes, None]:
        redis = get_redis()
        pubsub = redis.pubsub()
        await pubsub.subscribe(ALERT_CHANNEL)
        try:
            yield b": connected\n\n"
            while True:
                message = await pubsub.get_message(
                    ignore_subscribe_messages=True, timeout=15.0
                )
                if message is None:
                    yield b": ping\n\n"
                    continue
                data = message.get("data")
                if isinstance(data, bytes):
                    data = data.decode()
                try:
                    parsed = json.loads(data)
                except (TypeError, ValueError):
                    continue
                if user.tenant_id is not None and parsed.get("tenant_id") != str(
                    user.tenant_id
                ):
                    continue
                yield f"data: {json.dumps(parsed)}\n\n".encode()
                await asyncio.sleep(0)
        finally:
            await pubsub.unsubscribe(ALERT_CHANNEL)
            await pubsub.close()

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# ---------------------------------------------------------------------------
# Incidents
# ---------------------------------------------------------------------------
@router.post("/incidents", response_model=IncidentRead, status_code=status.HTTP_201_CREATED)
async def create_incident(
    payload: IncidentCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> IncidentRead:
    incident = Incident(tenant_id=user.tenant_id, **payload.model_dump())
    db.add(incident)
    await db.commit()
    await db.refresh(incident)
    return IncidentRead.model_validate(incident, from_attributes=True)


@router.get("/incidents", response_model=list[IncidentRead])
async def list_incidents(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[IncidentRead]:
    stmt = select(Incident)
    if user.tenant_id is not None:
        stmt = stmt.where(Incident.tenant_id == user.tenant_id)
    rows = (await db.execute(stmt)).scalars().all()
    return [IncidentRead.model_validate(i, from_attributes=True) for i in rows]


@router.get("/incidents/{incident_id}", response_model=IncidentRead)
async def get_incident(
    incident_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> IncidentRead:
    incident = (
        await db.execute(select(Incident).where(Incident.id == incident_id))
    ).scalar_one_or_none()
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    enforce_tenant(user, incident.tenant_id)
    return IncidentRead.model_validate(incident, from_attributes=True)


@router.patch("/incidents/{incident_id}", response_model=IncidentRead)
async def update_incident(
    incident_id: UUID,
    payload: IncidentUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> IncidentRead:
    incident = (
        await db.execute(select(Incident).where(Incident.id == incident_id))
    ).scalar_one_or_none()
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    enforce_tenant(user, incident.tenant_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(incident, field, value)
    await db.commit()
    await db.refresh(incident)
    return IncidentRead.model_validate(incident, from_attributes=True)


@router.delete("/incidents/{incident_id}", response_model=MessageResponse)
async def delete_incident(
    incident_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> MessageResponse:
    incident = (
        await db.execute(select(Incident).where(Incident.id == incident_id))
    ).scalar_one_or_none()
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    enforce_tenant(user, incident.tenant_id)
    await db.delete(incident)
    await db.commit()
    return MessageResponse(message="Incident deleted")


# ---------------------------------------------------------------------------
# Log search
# ---------------------------------------------------------------------------
@router.get("/logs/search")
async def search_logs(
    q: Optional[str] = None,
    size: int = Query(100, ge=1, le=1000),
    user: User = Depends(get_current_user),
) -> list[dict]:
    return await get_siem_service().search_logs(user.tenant_id, query=q, size=size)
