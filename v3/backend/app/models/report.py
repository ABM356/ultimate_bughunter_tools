"""Report model."""

from __future__ import annotations

from typing import Optional

from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TenantScopedModel


class Report(TenantScopedModel):
    __tablename__ = "reports"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    report_type: Mapped[str] = mapped_column(
        String(32), nullable=False, default="executive"
    )
    audience_role: Mapped[str] = mapped_column(String(32), nullable=False, default="ciso")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    generated_html: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    generated_pdf_url: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    parameters: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
