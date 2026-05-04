"""Alert schemas."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TenantScopedRead


class AlertCreate(BaseModel):
    severity: str = "medium"
    source: str = "siem"
    message: str = ""
    ip: Optional[str] = None
    user_identifier: Optional[str] = None
    raw_event: Dict[str, Any] = Field(default_factory=dict)


class AlertUpdate(BaseModel):
    severity: Optional[str] = None
    status: Optional[str] = None
    correlation_id: Optional[UUID] = None
    raw_event: Optional[Dict[str, Any]] = None


class AlertRead(TenantScopedRead):
    severity: str
    source: str
    message: str
    ip: Optional[str] = None
    user_identifier: Optional[str] = None
    status: str
    correlation_id: Optional[UUID] = None
    raw_event: Dict[str, Any]
