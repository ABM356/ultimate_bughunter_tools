"""Lightweight import smoke test."""

from __future__ import annotations


def test_app_import() -> None:
    from app.main import app

    assert app.title


def test_models_register() -> None:
    from app.models import Base
    from app.models import (  # noqa: F401
        Alert,
        Asset,
        BountyProgram,
        BountySubmission,
        Incident,
        LabSession,
        Report,
        Scan,
        ScheduledJob,
        Tenant,
        TrainingModule,
        User,
        UserProgress,
        Vulnerability,
    )

    assert "tenants" in Base.metadata.tables
    assert "users" in Base.metadata.tables
    assert "scans" in Base.metadata.tables
