"""AI service schemas."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ClassifyVulnRequest(BaseModel):
    title: str
    description: str
    evidence: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class ClassifyVulnResponse(BaseModel):
    severity: str
    cwe: Optional[str] = None
    cvss_base: float
    confidence: float
    rationale: str


class RiskScoreRequest(BaseModel):
    vulnerabilities: List[Dict[str, Any]] = Field(default_factory=list)
    asset_criticality: int = 1
    environmental_factors: Optional[Dict[str, Any]] = None


class RiskScoreResponse(BaseModel):
    risk_score: float
    risk_level: str
    drivers: List[str]


class GenerateReportRequest(BaseModel):
    audience_role: str
    report_type: str = "executive"
    findings: List[Dict[str, Any]] = Field(default_factory=list)
    period: Optional[str] = None


class GenerateReportResponse(BaseModel):
    html: str
    summary: str


class ThreatPatternRequest(BaseModel):
    events: List[Dict[str, Any]] = Field(default_factory=list)
    window_hours: int = 24


class ThreatPatternResponse(BaseModel):
    patterns: List[Dict[str, Any]]
    indicators_of_compromise: List[str]
    recommendation: str
