"""Training and lab schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import TenantScopedRead


class TrainingModuleCreate(BaseModel):
    title: str
    description: str = ""
    difficulty: str = "beginner"
    duration_minutes: int = 30
    content: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)


class TrainingModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[str] = None
    duration_minutes: Optional[int] = None
    content: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None


class TrainingModuleRead(TenantScopedRead):
    title: str
    description: str
    difficulty: str
    duration_minutes: int
    content: Dict[str, Any]
    tags: List[str]


class UserProgressCreate(BaseModel):
    module_id: UUID


class UserProgressUpdate(BaseModel):
    status: Optional[str] = None
    progress_pct: Optional[int] = Field(default=None, ge=0, le=100)
    score: Optional[int] = None
    completed_at: Optional[datetime] = None


class UserProgressRead(TenantScopedRead):
    user_id: UUID
    module_id: UUID
    status: str
    progress_pct: int
    completed_at: Optional[datetime] = None
    score: Optional[int] = None


class LabSessionCreate(BaseModel):
    module_id: UUID


class LabSessionRead(TenantScopedRead):
    user_id: UUID
    module_id: UUID
    container_id: Optional[str] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    status: str
