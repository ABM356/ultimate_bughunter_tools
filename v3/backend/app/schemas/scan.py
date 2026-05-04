"""Scan schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.schemas.common import TenantScopedRead


class ScanCreate(BaseModel):
    target: str
    scan_type: str = Field(default="web", description="web|api|network|full")
    scan_level: str = Field(default="fast", description="fast|medium|deep")
    tier: int = Field(default=1, ge=1, le=4)


class ScanUpdate(BaseModel):
    status: Optional[str] = None
    findings_count: Optional[int] = None
    raw_output: Optional[Dict[str, Any]] = None
    tools_used: Optional[List[str]] = None
    error_message: Optional[str] = None


class ScanRead(TenantScopedRead):
    target: str
    scan_type: str
    scan_level: str
    tier: int
    status: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    findings_count: int
    raw_output: Dict[str, Any]
    tools_used: List[str]
    error_message: Optional[str] = None


class ScanFilter(BaseModel):
    status: Optional[str] = None
    scan_type: Optional[str] = None
    scan_level: Optional[str] = None
    target: Optional[str] = None
