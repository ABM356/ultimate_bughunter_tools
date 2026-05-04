"""Shared Pydantic types and base schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class TimestampedRead(ORMBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    page: int
    page_size: int
    items: List[T]


class MessageResponse(BaseModel):
    message: str


class TenantScopedRead(TimestampedRead):
    tenant_id: Optional[UUID] = None
