"""Asset schemas."""

from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from app.schemas.common import TenantScopedRead


class AssetCreate(BaseModel):
    name: str
    asset_type: str = Field(default="domain", description="domain|ip|iot|cctv")
    identifier: str
    attributes: Dict[str, Any] = Field(default_factory=dict)
    criticality: int = Field(default=1, ge=1, le=5)
    owner: Optional[str] = None
    status: str = "active"


class AssetUpdate(BaseModel):
    name: Optional[str] = None
    asset_type: Optional[str] = None
    identifier: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
    criticality: Optional[int] = Field(default=None, ge=1, le=5)
    owner: Optional[str] = None
    status: Optional[str] = None


class AssetRead(TenantScopedRead):
    name: str
    asset_type: str
    identifier: str
    attributes: Dict[str, Any]
    criticality: int
    owner: Optional[str] = None
    status: str
