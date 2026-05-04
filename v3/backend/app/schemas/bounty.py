"""Bounty program / submission schemas."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TenantScopedRead


class BountyProgramCreate(BaseModel):
    name: str
    description: str = ""
    scope: Dict[str, Any] = Field(default_factory=dict)
    rewards: Dict[str, Any] = Field(default_factory=dict)
    rules: str = ""
    status: str = "draft"


class BountyProgramUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    scope: Optional[Dict[str, Any]] = None
    rewards: Optional[Dict[str, Any]] = None
    rules: Optional[str] = None
    status: Optional[str] = None


class BountyProgramRead(TenantScopedRead):
    name: str
    description: str
    scope: Dict[str, Any]
    rewards: Dict[str, Any]
    rules: str
    status: str


class BountySubmissionCreate(BaseModel):
    program_id: UUID
    title: str
    description: str = ""
    severity: str = "medium"
    evidence: Dict[str, Any] = Field(default_factory=dict)


class BountySubmissionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None
    evidence: Optional[Dict[str, Any]] = None
    reward_amount: Optional[Decimal] = None


class BountySubmissionRead(TenantScopedRead):
    program_id: UUID
    hunter_id: Optional[UUID] = None
    title: str
    description: str
    severity: str
    status: str
    evidence: Dict[str, Any]
    reward_amount: Optional[Decimal] = None
    paid_at: Optional[datetime] = None
    triaged_at: Optional[datetime] = None


class BountyStatusTransition(BaseModel):
    new_status: str = Field(
        description="One of: submitted, triaged, accepted, duplicate, rejected, paid"
    )
    note: Optional[str] = None


class BountyPayment(BaseModel):
    amount: Decimal
    note: Optional[str] = None
