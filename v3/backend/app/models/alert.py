"""Blue-team alert model."""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TenantScopedModel


class Alert(TenantScopedModel):
    __tablename__ = "alerts"

    severity: Mapped[str] = mapped_column(String(16), nullable=False, default="medium")
    source: Mapped[str] = mapped_column(String(64), nullable=False, default="siem")
    message: Mapped[str] = mapped_column(Text, nullable=False, default="")
    ip: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    user_identifier: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="new")
    correlation_id: Mapped[Optional[UUID]] = mapped_column(
        PG_UUID(as_uuid=True), nullable=True, index=True
    )
    raw_event: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
