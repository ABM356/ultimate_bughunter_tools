"""Incident schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field

from app.schemas.common import TenantScopedRead


class IncidentCreate(BaseModel):
    title: str
    description: str = ""
    severity: str = "medium"
    affected_assets: List[Any] = Field(default_factory=list)


class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    timeline: Optional[List[Any]] = None
    affected_assets: Optional[List[Any]] = None
    response_actions: Optional[List[Any]] = None
    detected_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None


class IncidentRead(TenantScopedRead):
    title: str
    description: str
    severity: str
    status: str
    timeline: List[Any]
    affected_assets: List[Any]
    response_actions: List[Any]
    detected_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
