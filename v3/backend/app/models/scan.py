"""Scan model."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TenantScopedModel


class Scan(TenantScopedModel):
    __tablename__ = "scans"

    target: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    scan_type: Mapped[str] = mapped_column(String(32), nullable=False, default="web")
    scan_level: Mapped[str] = mapped_column(String(16), nullable=False, default="fast")
    tier: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="queued")
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    findings_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    raw_output: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    tools_used: Mapped[list[str]] = mapped_column(
        ARRAY(String), nullable=False, default=list
    )
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
