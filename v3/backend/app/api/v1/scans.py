"""Scan endpoints."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import enforce_tenant, get_current_user
from app.models.scan import Scan
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.scan import ScanCreate, ScanRead
from app.services.scanner_service import get_scanner_service

router = APIRouter()


@router.post("", response_model=ScanRead, status_code=status.HTTP_201_CREATED)
async def trigger_scan(
    payload: ScanCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ScanRead:
    scan = Scan(
        tenant_id=user.tenant_id,
        target=payload.target,
        scan_type=payload.scan_type,
        scan_level=payload.scan_level,
        tier=payload.tier,
        status="queued",
    )
    db.add(scan)
    await db.commit()
    await db.refresh(scan)
    try:
        await get_scanner_service().queue_scan(db, scan)
    except Exception:
        # Broker unavailable; scan remains queued for retry by scheduler.
        pass
    return ScanRead.model_validate(scan, from_attributes=True)


@router.get("", response_model=list[ScanRead])
async def list_scans(
    status_filter: Optional[str] = Query(None, alias="status"),
    scan_type: Optional[str] = None,
    scan_level: Optional[str] = None,
    target: Optional[str] = None,
    limit: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[ScanRead]:
    stmt = select(Scan)
    if user.tenant_id is not None:
        stmt = stmt.where(Scan.tenant_id == user.tenant_id)
    if status_filter:
        stmt = stmt.where(Scan.status == status_filter)
    if scan_type:
        stmt = stmt.where(Scan.scan_type == scan_type)
    if scan_level:
        stmt = stmt.where(Scan.scan_level == scan_level)
    if target:
        stmt = stmt.where(Scan.target.ilike(f"%{target}%"))
    stmt = stmt.order_by(Scan.created_at.desc()).limit(limit)
    rows = (await db.execute(stmt)).scalars().all()
    return [ScanRead.model_validate(s, from_attributes=True) for s in rows]


@router.get("/{scan_id}", response_model=ScanRead)
async def get_scan(
    scan_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ScanRead:
    scan = (
        await db.execute(select(Scan).where(Scan.id == scan_id))
    ).scalar_one_or_none()
    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    enforce_tenant(user, scan.tenant_id)
    return ScanRead.model_validate(scan, from_attributes=True)


@router.post("/{scan_id}/cancel", response_model=ScanRead)
async def cancel_scan(
    scan_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ScanRead:
    scan = (
        await db.execute(select(Scan).where(Scan.id == scan_id))
    ).scalar_one_or_none()
    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    enforce_tenant(user, scan.tenant_id)
    if scan.status in {"completed", "failed", "cancelled"}:
        raise HTTPException(status_code=400, detail="Scan is already terminal")
    scan.status = "cancelled"
    scan.completed_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(scan)
    return ScanRead.model_validate(scan, from_attributes=True)


@router.delete("/{scan_id}", response_model=MessageResponse)
async def delete_scan(
    scan_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> MessageResponse:
    scan = (
        await db.execute(select(Scan).where(Scan.id == scan_id))
    ).scalar_one_or_none()
    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    enforce_tenant(user, scan.tenant_id)
    await db.delete(scan)
    await db.commit()
    return MessageResponse(message="Scan deleted")
