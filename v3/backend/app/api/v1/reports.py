"""Report endpoints."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import enforce_tenant, get_current_user
from app.models.report import Report
from app.models.user import User
from app.schemas.report import ReportCreate, ReportRead
from app.services.report_service import get_report_service

router = APIRouter()


@router.post("", response_model=ReportRead, status_code=status.HTTP_201_CREATED)
async def generate_report(
    payload: ReportCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ReportRead:
    findings = list(payload.parameters.get("findings", []))
    period = payload.parameters.get("period")
    result = await get_report_service().generate(
        audience_role=payload.audience_role,
        report_type=payload.report_type,
        findings=findings,
        period=period,
    )

    report = Report(
        tenant_id=user.tenant_id,
        title=payload.title,
        report_type=payload.report_type,
        audience_role=payload.audience_role,
        status="ready",
        parameters=payload.parameters,
        generated_html=result.get("html"),
        summary=result.get("summary"),
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return ReportRead.model_validate(report, from_attributes=True)


@router.get("", response_model=list[ReportRead])
async def list_reports(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[ReportRead]:
    stmt = select(Report)
    if user.tenant_id is not None:
        stmt = stmt.where(Report.tenant_id == user.tenant_id)
    rows = (await db.execute(stmt.order_by(Report.created_at.desc()))).scalars().all()
    return [ReportRead.model_validate(r, from_attributes=True) for r in rows]


@router.get("/{report_id}", response_model=ReportRead)
async def get_report(
    report_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ReportRead:
    report = (
        await db.execute(select(Report).where(Report.id == report_id))
    ).scalar_one_or_none()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    enforce_tenant(user, report.tenant_id)
    return ReportRead.model_validate(report, from_attributes=True)


@router.get("/{report_id}/html", response_class=HTMLResponse)
async def download_report_html(
    report_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Response:
    report = (
        await db.execute(select(Report).where(Report.id == report_id))
    ).scalar_one_or_none()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    enforce_tenant(user, report.tenant_id)
    return HTMLResponse(content=report.generated_html or "<html><body></body></html>")


@router.get("/{report_id}/pdf")
async def download_report_pdf(
    report_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Response:
    report = (
        await db.execute(select(Report).where(Report.id == report_id))
    ).scalar_one_or_none()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    enforce_tenant(user, report.tenant_id)
    if not report.generated_pdf_url:
        raise HTTPException(status_code=404, detail="PDF not yet generated")
    return RedirectResponse(report.generated_pdf_url)
