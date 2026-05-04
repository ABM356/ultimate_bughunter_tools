"""Scheduled jobs endpoints."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import enforce_tenant, get_current_user
from app.models.job import ScheduledJob
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.job import ScheduledJobCreate, ScheduledJobRead, ScheduledJobUpdate

router = APIRouter()


def _validate_cron(expr: str) -> None:
    parts = expr.split()
    if len(parts) != 5:
        raise HTTPException(
            status_code=400, detail="Cron expression must have 5 fields"
        )


@router.post("/jobs", response_model=ScheduledJobRead, status_code=status.HTTP_201_CREATED)
async def create_job(
    payload: ScheduledJobCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ScheduledJobRead:
    _validate_cron(payload.cron_expression)
    job = ScheduledJob(tenant_id=user.tenant_id, **payload.model_dump())
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return ScheduledJobRead.model_validate(job, from_attributes=True)


@router.get("/jobs", response_model=list[ScheduledJobRead])
async def list_jobs(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[ScheduledJobRead]:
    stmt = select(ScheduledJob)
    if user.tenant_id is not None:
        stmt = stmt.where(ScheduledJob.tenant_id == user.tenant_id)
    rows = (await db.execute(stmt)).scalars().all()
    return [ScheduledJobRead.model_validate(j, from_attributes=True) for j in rows]


@router.patch("/jobs/{job_id}", response_model=ScheduledJobRead)
async def update_job(
    job_id: UUID,
    payload: ScheduledJobUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ScheduledJobRead:
    job = (
        await db.execute(select(ScheduledJob).where(ScheduledJob.id == job_id))
    ).scalar_one_or_none()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    enforce_tenant(user, job.tenant_id)
    if payload.cron_expression is not None:
        _validate_cron(payload.cron_expression)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(job, field, value)
    await db.commit()
    await db.refresh(job)
    return ScheduledJobRead.model_validate(job, from_attributes=True)


@router.delete("/jobs/{job_id}", response_model=MessageResponse)
async def delete_job(
    job_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> MessageResponse:
    job = (
        await db.execute(select(ScheduledJob).where(ScheduledJob.id == job_id))
    ).scalar_one_or_none()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    enforce_tenant(user, job.tenant_id)
    await db.delete(job)
    await db.commit()
    return MessageResponse(message="Job deleted")


@router.post("/jobs/{job_id}/trigger", response_model=ScheduledJobRead)
async def trigger_job(
    job_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ScheduledJobRead:
    job = (
        await db.execute(select(ScheduledJob).where(ScheduledJob.id == job_id))
    ).scalar_one_or_none()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    enforce_tenant(user, job.tenant_id)
    job.last_run = datetime.now(timezone.utc)
    job.last_result = "manual_trigger"
    await db.commit()
    await db.refresh(job)
    return ScheduledJobRead.model_validate(job, from_attributes=True)
