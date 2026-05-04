"""Bug bounty program and submission models."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TenantScopedModel


class BountyProgram(TenantScopedModel):
    __tablename__ = "bounty_programs"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    scope: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    rewards: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    rules: Mapped[str] = mapped_column(Text, nullable=False, default="")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")


class BountySubmission(TenantScopedModel):
    __tablename__ = "bounty_submissions"

    program_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("bounty_programs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    hunter_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    severity: Mapped[str] = mapped_column(String(16), nullable=False, default="medium")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="submitted")
    evidence: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    reward_amount: Mapped[Optional[float]] = mapped_column(Numeric(12, 2), nullable=True)
    paid_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    triaged_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
