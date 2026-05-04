"""Report generation service."""

from __future__ import annotations

from typing import Any, Dict, List

from app.services.ai_service import get_ai_service

ROLE_TEMPLATES: Dict[str, str] = {
    "ciso": (
        "<h1>Executive Security Posture</h1>"
        "<p>This report summarizes the organization's risk posture for the CISO.</p>"
    ),
    "cto": (
        "<h1>Technical Security Strategy</h1>"
        "<p>Architecture-level findings and strategic recommendations for the CTO.</p>"
    ),
    "manager": (
        "<h1>Operational Security Report</h1>"
        "<p>Prioritized findings and remediation status for engineering managers.</p>"
    ),
    "engineer": (
        "<h1>Technical Findings</h1>"
        "<p>Detailed reproduction steps and remediation guidance for engineers.</p>"
    ),
    "board": (
        "<h1>Board Briefing</h1>"
        "<p>Business-impact view of cyber risk for board members.</p>"
    ),
    "compliance": (
        "<h1>Compliance Report</h1>"
        "<p>Findings mapped to controls (SOC 2, ISO 27001, NIST CSF).</p>"
    ),
}


class ReportService:
    async def generate(
        self,
        audience_role: str,
        report_type: str,
        findings: List[Dict[str, Any]],
        period: str | None = None,
    ) -> Dict[str, str]:
        ai = get_ai_service()
        result = await ai.generate_report(
            audience_role=audience_role,
            report_type=report_type,
            findings=findings,
            period=period,
        )
        if not result.get("html"):
            preface = ROLE_TEMPLATES.get(audience_role.lower(), "<h1>Security Report</h1>")
            rows = "".join(
                f"<tr><td>{f.get('title', 'Finding')}</td>"
                f"<td>{f.get('severity', 'info')}</td>"
                f"<td>{f.get('remediation', '')}</td></tr>"
                for f in findings
            )
            result["html"] = (
                f"<html><body>{preface}"
                f"<table border='1'><tr><th>Title</th><th>Severity</th><th>Remediation</th></tr>"
                f"{rows}</table></body></html>"
            )
        return result


_service: ReportService | None = None


def get_report_service() -> ReportService:
    global _service
    if _service is None:
        _service = ReportService()
    return _service
