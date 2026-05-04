"""Report schemas."""

from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from app.schemas.common import TenantScopedRead


class ReportCreate(BaseModel):
    title: str
    report_type: str = Field(
        default="executive", description="executive|technical|compliance"
    )
    audience_role: str = Field(
        default="ciso",
        description="ciso|cto|manager|engineer|board|compliance",
    )
    parameters: Dict[str, Any] = Field(default_factory=dict)


class ReportUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    summary: Optional[str] = None
    generated_html: Optional[str] = None
    generated_pdf_url: Optional[str] = None


class ReportRead(TenantScopedRead):
    title: str
    report_type: str
    audience_role: str
    status: str
    summary: Optional[str] = None
    generated_pdf_url: Optional[str] = None
    parameters: Dict[str, Any]
