"""User schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import TimestampedRead


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(default="", max_length=255)
    role: str = Field(default="client")
    tenant_id: Optional[UUID] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    tenant_id: Optional[UUID] = None


class UserRead(TimestampedRead):
    email: EmailStr
    full_name: str
    role: str
    tenant_id: Optional[UUID] = None
    is_active: bool
    last_login_at: Optional[datetime] = None
