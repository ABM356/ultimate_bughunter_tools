"""AI endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User
from app.schemas.ai import (
    ClassifyVulnRequest,
    ClassifyVulnResponse,
    GenerateReportRequest,
    GenerateReportResponse,
    RiskScoreRequest,
    RiskScoreResponse,
    ThreatPatternRequest,
    ThreatPatternResponse,
)
from app.services.ai_service import get_ai_service

router = APIRouter()


@router.post("/classify-vulnerability", response_model=ClassifyVulnResponse)
async def classify_vulnerability(
    payload: ClassifyVulnRequest,
    _: User = Depends(get_current_user),
) -> ClassifyVulnResponse:
    result = await get_ai_service().classify_vulnerability(
        title=payload.title,
        description=payload.description,
        evidence=payload.evidence,
        context=payload.context,
    )
    return ClassifyVulnResponse(
        severity=result["severity"],
        cwe=result.get("cwe"),
        cvss_base=float(result.get("cvss_base", 0.0)),
        confidence=float(result.get("confidence", 0.5)),
        rationale=result.get("rationale", ""),
    )


@router.post("/risk-score", response_model=RiskScoreResponse)
async def risk_score(
    payload: RiskScoreRequest,
    _: User = Depends(get_current_user),
) -> RiskScoreResponse:
    result = await get_ai_service().risk_score(
        vulnerabilities=payload.vulnerabilities,
        asset_criticality=payload.asset_criticality,
        environmental_factors=payload.environmental_factors,
    )
    return RiskScoreResponse(
        risk_score=float(result.get("risk_score", 0.0)),
        risk_level=str(result.get("risk_level", "low")),
        drivers=list(result.get("drivers", [])),
    )


@router.post("/generate-report", response_model=GenerateReportResponse)
async def generate_report(
    payload: GenerateReportRequest,
    _: User = Depends(get_current_user),
) -> GenerateReportResponse:
    result = await get_ai_service().generate_report(
        audience_role=payload.audience_role,
        report_type=payload.report_type,
        findings=payload.findings,
        period=payload.period,
    )
    return GenerateReportResponse(
        html=result.get("html", ""),
        summary=result.get("summary", ""),
    )


@router.post("/threat-pattern-analysis", response_model=ThreatPatternResponse)
async def threat_pattern_analysis(
    payload: ThreatPatternRequest,
    _: User = Depends(get_current_user),
) -> ThreatPatternResponse:
    result = await get_ai_service().threat_pattern_analysis(
        events=payload.events,
        window_hours=payload.window_hours,
    )
    return ThreatPatternResponse(
        patterns=list(result.get("patterns", [])),
        indicators_of_compromise=list(result.get("indicators_of_compromise", [])),
        recommendation=str(result.get("recommendation", "")),
    )
