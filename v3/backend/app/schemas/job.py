"""Scheduled job schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from app.schemas.common import TenantScopedRead


class ScheduledJobCreate(BaseModel):
    name: str
    description: str = ""
    cron_expression: str = Field(description="Standard 5-field cron expression")
    job_type: str = "scan"
    payload: Dict[str, Any] = Field(default_factory=dict)


class ScheduledJobUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    cron_expression: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class ScheduledJobRead(TenantScopedRead):
    name: str
    description: str
    cron_expression: str
    job_type: str
    payload: Dict[str, Any]
    status: str
    next_run: Optional[datetime] = None
    last_run: Optional[datetime] = None
    last_result: Optional[str] = None
