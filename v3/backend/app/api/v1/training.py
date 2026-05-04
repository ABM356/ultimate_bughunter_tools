"""Training endpoints."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import enforce_tenant, get_current_user
from app.models.training import LabSession, TrainingModule, UserProgress
from app.models.user import User
from app.schemas.training import (
    LabSessionCreate,
    LabSessionRead,
    TrainingModuleCreate,
    TrainingModuleRead,
    UserProgressCreate,
    UserProgressRead,
    UserProgressUpdate,
)

router = APIRouter()


# Modules ----------------------------------------------------------------
@router.get("/modules", response_model=list[TrainingModuleRead])
async def list_modules(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[TrainingModuleRead]:
    stmt = select(TrainingModule)
    if user.tenant_id is not None:
        stmt = stmt.where(TrainingModule.tenant_id == user.tenant_id)
    rows = (await db.execute(stmt)).scalars().all()
    return [TrainingModuleRead.model_validate(r, from_attributes=True) for r in rows]


@router.post(
    "/modules", response_model=TrainingModuleRead, status_code=status.HTTP_201_CREATED
)
async def create_module(
    payload: TrainingModuleCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TrainingModuleRead:
    module = TrainingModule(tenant_id=user.tenant_id, **payload.model_dump())
    db.add(module)
    await db.commit()
    await db.refresh(module)
    return TrainingModuleRead.model_validate(module, from_attributes=True)


# Enrollment / progress --------------------------------------------------
@router.post(
    "/enroll", response_model=UserProgressRead, status_code=status.HTTP_201_CREATED
)
async def enroll(
    payload: UserProgressCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> UserProgressRead:
    module = (
        await db.execute(
            select(TrainingModule).where(TrainingModule.id == payload.module_id)
        )
    ).scalar_one_or_none()
    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")
    progress = UserProgress(
        tenant_id=user.tenant_id,
        user_id=user.id,
        module_id=payload.module_id,
        status="enrolled",
    )
    db.add(progress)
    await db.commit()
    await db.refresh(progress)
    return UserProgressRead.model_validate(progress, from_attributes=True)


@router.get("/progress", response_model=list[UserProgressRead])
async def list_progress(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[UserProgressRead]:
    rows = (
        await db.execute(select(UserProgress).where(UserProgress.user_id == user.id))
    ).scalars().all()
    return [UserProgressRead.model_validate(r, from_attributes=True) for r in rows]


@router.patch("/progress/{progress_id}", response_model=UserProgressRead)
async def update_progress(
    progress_id: UUID,
    payload: UserProgressUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> UserProgressRead:
    progress = (
        await db.execute(select(UserProgress).where(UserProgress.id == progress_id))
    ).scalar_one_or_none()
    if progress is None or progress.user_id != user.id:
        raise HTTPException(status_code=404, detail="Progress not found")
    enforce_tenant(user, progress.tenant_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(progress, field, value)
    if payload.progress_pct == 100 and progress.completed_at is None:
        progress.completed_at = datetime.now(timezone.utc)
        progress.status = "completed"
    await db.commit()
    await db.refresh(progress)
    return UserProgressRead.model_validate(progress, from_attributes=True)


# Lab sessions -----------------------------------------------------------
@router.post(
    "/labs", response_model=LabSessionRead, status_code=status.HTTP_201_CREATED
)
async def start_lab(
    payload: LabSessionCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> LabSessionRead:
    session = LabSession(
        tenant_id=user.tenant_id,
        user_id=user.id,
        module_id=payload.module_id,
        status="provisioning",
        started_at=datetime.now(timezone.utc),
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return LabSessionRead.model_validate(session, from_attributes=True)


@router.get("/labs", response_model=list[LabSessionRead])
async def list_labs(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[LabSessionRead]:
    rows = (
        await db.execute(select(LabSession).where(LabSession.user_id == user.id))
    ).scalars().all()
    return [LabSessionRead.model_validate(r, from_attributes=True) for r in rows]
