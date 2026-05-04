"""Bounty programs and submissions."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import enforce_tenant, get_current_user
from app.models.bounty import BountyProgram, BountySubmission
from app.models.user import User
from app.schemas.bounty import (
    BountyPayment,
    BountyProgramCreate,
    BountyProgramRead,
    BountyProgramUpdate,
    BountyStatusTransition,
    BountySubmissionCreate,
    BountySubmissionRead,
    BountySubmissionUpdate,
)
from app.schemas.common import MessageResponse

router = APIRouter()

ALLOWED_TRANSITIONS = {"submitted", "triaged", "accepted", "duplicate", "rejected", "paid"}


# ---------------------------------------------------------------------------
# Programs
# ---------------------------------------------------------------------------
@router.post(
    "/programs", response_model=BountyProgramRead, status_code=status.HTTP_201_CREATED
)
async def create_program(
    payload: BountyProgramCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> BountyProgramRead:
    program = BountyProgram(tenant_id=user.tenant_id, **payload.model_dump())
    db.add(program)
    await db.commit()
    await db.refresh(program)
    return BountyProgramRead.model_validate(program, from_attributes=True)


@router.get("/programs", response_model=list[BountyProgramRead])
async def list_programs(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[BountyProgramRead]:
    stmt = select(BountyProgram)
    if user.tenant_id is not None:
        stmt = stmt.where(BountyProgram.tenant_id == user.tenant_id)
    rows = (await db.execute(stmt)).scalars().all()
    return [BountyProgramRead.model_validate(r, from_attributes=True) for r in rows]


@router.get("/programs/{program_id}", response_model=BountyProgramRead)
async def get_program(
    program_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> BountyProgramRead:
    program = (
        await db.execute(select(BountyProgram).where(BountyProgram.id == program_id))
    ).scalar_one_or_none()
    if program is None:
        raise HTTPException(status_code=404, detail="Program not found")
    enforce_tenant(user, program.tenant_id)
    return BountyProgramRead.model_validate(program, from_attributes=True)


@router.patch("/programs/{program_id}", response_model=BountyProgramRead)
async def update_program(
    program_id: UUID,
    payload: BountyProgramUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> BountyProgramRead:
    program = (
        await db.execute(select(BountyProgram).where(BountyProgram.id == program_id))
    ).scalar_one_or_none()
    if program is None:
        raise HTTPException(status_code=404, detail="Program not found")
    enforce_tenant(user, program.tenant_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(program, field, value)
    await db.commit()
    await db.refresh(program)
    return BountyProgramRead.model_validate(program, from_attributes=True)


@router.delete("/programs/{program_id}", response_model=MessageResponse)
async def delete_program(
    program_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> MessageResponse:
    program = (
        await db.execute(select(BountyProgram).where(BountyProgram.id == program_id))
    ).scalar_one_or_none()
    if program is None:
        raise HTTPException(status_code=404, detail="Program not found")
    enforce_tenant(user, program.tenant_id)
    await db.delete(program)
    await db.commit()
    return MessageResponse(message="Program deleted")


# ---------------------------------------------------------------------------
# Submissions
# ---------------------------------------------------------------------------
@router.post(
    "/submissions",
    response_model=BountySubmissionRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_submission(
    payload: BountySubmissionCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> BountySubmissionRead:
    program = (
        await db.execute(select(BountyProgram).where(BountyProgram.id == payload.program_id))
    ).scalar_one_or_none()
    if program is None:
        raise HTTPException(status_code=404, detail="Program not found")
    submission = BountySubmission(
        tenant_id=program.tenant_id,
        hunter_id=user.id,
        **payload.model_dump(),
    )
    db.add(submission)
    await db.commit()
    await db.refresh(submission)
    return BountySubmissionRead.model_validate(submission, from_attributes=True)


@router.get("/submissions", response_model=list[BountySubmissionRead])
async def list_submissions(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[BountySubmissionRead]:
    stmt = select(BountySubmission)
    if user.tenant_id is not None:
        stmt = stmt.where(BountySubmission.tenant_id == user.tenant_id)
    rows = (await db.execute(stmt)).scalars().all()
    return [BountySubmissionRead.model_validate(r, from_attributes=True) for r in rows]


@router.get("/submissions/{submission_id}", response_model=BountySubmissionRead)
async def get_submission(
    submission_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> BountySubmissionRead:
    submission = (
        await db.execute(
            select(BountySubmission).where(BountySubmission.id == submission_id)
        )
    ).scalar_one_or_none()
    if submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    enforce_tenant(user, submission.tenant_id)
    return BountySubmissionRead.model_validate(submission, from_attributes=True)


@router.patch("/submissions/{submission_id}", response_model=BountySubmissionRead)
async def update_submission(
    submission_id: UUID,
    payload: BountySubmissionUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> BountySubmissionRead:
    submission = (
        await db.execute(
            select(BountySubmission).where(BountySubmission.id == submission_id)
        )
    ).scalar_one_or_none()
    if submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    enforce_tenant(user, submission.tenant_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(submission, field, value)
    await db.commit()
    await db.refresh(submission)
    return BountySubmissionRead.model_validate(submission, from_attributes=True)


@router.post(
    "/submissions/{submission_id}/transition", response_model=BountySubmissionRead
)
async def transition_submission(
    submission_id: UUID,
    payload: BountyStatusTransition,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> BountySubmissionRead:
    if payload.new_status not in ALLOWED_TRANSITIONS:
        raise HTTPException(status_code=400, detail="Invalid status")
    submission = (
        await db.execute(
            select(BountySubmission).where(BountySubmission.id == submission_id)
        )
    ).scalar_one_or_none()
    if submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    enforce_tenant(user, submission.tenant_id)
    submission.status = payload.new_status
    if payload.new_status == "triaged":
        submission.triaged_at = datetime.now(timezone.utc)
    if payload.new_status == "paid":
        submission.paid_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(submission)
    return BountySubmissionRead.model_validate(submission, from_attributes=True)


@router.post("/submissions/{submission_id}/payment", response_model=BountySubmissionRead)
async def record_payment(
    submission_id: UUID,
    payload: BountyPayment,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> BountySubmissionRead:
    submission = (
        await db.execute(
            select(BountySubmission).where(BountySubmission.id == submission_id)
        )
    ).scalar_one_or_none()
    if submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    enforce_tenant(user, submission.tenant_id)
    submission.reward_amount = payload.amount
    submission.status = "paid"
    submission.paid_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(submission)
    return BountySubmissionRead.model_validate(submission, from_attributes=True)
