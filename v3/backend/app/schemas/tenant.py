"""Tenant schemas."""

from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import TimestampedRead


class TenantCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=2, max_length=64, pattern=r"^[a-z0-9-]+$")
    tier: int = Field(default=1, ge=1, le=4)
    billing_email: Optional[EmailStr] = None
    settings: Dict[str, Any] = Field(default_factory=dict)


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    tier: Optional[int] = Field(default=None, ge=1, le=4)
    status: Optional[str] = None
    billing_email: Optional[EmailStr] = None
    stripe_customer_id: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class TenantRead(TimestampedRead):
    name: str
    slug: str
    tier: int
    status: str
    billing_email: Optional[EmailStr] = None
    stripe_customer_id: Optional[str] = None
    settings: Dict[str, Any] = Field(default_factory=dict)
