"""Infrastructure asset model."""

from __future__ import annotations

from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TenantScopedModel


class Asset(TenantScopedModel):
    __tablename__ = "assets"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    asset_type: Mapped[str] = mapped_column(String(32), nullable=False, default="domain")
    identifier: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    attributes: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    criticality: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    owner: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
