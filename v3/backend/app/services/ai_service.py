"""AI service layer wrapping Anthropic Claude (with fallback)."""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

from app.core.config import settings

logger = logging.getLogger(__name__)


SEVERITY_BY_CVSS = [
    (9.0, "critical"),
    (7.0, "high"),
    (4.0, "medium"),
    (0.1, "low"),
]


def cvss_to_severity(cvss: float) -> str:
    for threshold, label in SEVERITY_BY_CVSS:
        if cvss >= threshold:
            return label
    return "info"


class AIService:
    """Async AI service. Uses Anthropic when configured, otherwise rule-based fallback."""

    def __init__(self) -> None:
        self._client = None
        if settings.ANTHROPIC_API_KEY:
            try:
                from anthropic import AsyncAnthropic

                self._client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
            except Exception as exc:  # pragma: no cover
                logger.warning("Anthropic client init failed: %s", exc)
                self._client = None

    @property
    def is_ai_enabled(self) -> bool:
        return self._client is not None

    async def _claude_json(self, system: str, user: str) -> Dict[str, Any]:
        """Run Claude and parse a JSON response. Raises on parse failure."""
        assert self._client is not None
        msg = await self._client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=2048,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        text = "".join(
            block.text for block in msg.content if getattr(block, "type", None) == "text"
        )
        # Best-effort JSON extraction.
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            start = text.find("{")
            end = text.rfind("}")
            if start >= 0 and end > start:
                return json.loads(text[start : end + 1])
            raise

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    async def classify_vulnerability(
        self,
        title: str,
        description: str,
        evidence: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if not self.is_ai_enabled:
            return self._fallback_classify(title, description)
        system = (
            "You are a senior application security engineer. "
            "Return a strict JSON object with keys: severity, cwe, cvss_base, "
            "confidence, rationale."
        )
        user = json.dumps(
            {
                "title": title,
                "description": description,
                "evidence": evidence,
                "context": context or {},
            }
        )
        try:
            return await self._claude_json(system, user)
        except Exception as exc:
            logger.warning("classify_vulnerability fallback: %s", exc)
            return self._fallback_classify(title, description)

    async def risk_score(
        self,
        vulnerabilities: List[Dict[str, Any]],
        asset_criticality: int = 1,
        environmental_factors: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if not self.is_ai_enabled:
            return self._fallback_risk(vulnerabilities, asset_criticality)
        system = (
            "You are a risk-quantification expert. Return JSON: "
            "{risk_score: 0-100, risk_level: low|medium|high|critical, drivers: []}"
        )
        user = json.dumps(
            {
                "vulnerabilities": vulnerabilities,
                "asset_criticality": asset_criticality,
                "environmental_factors": environmental_factors or {},
            }
        )
        try:
            return await self._claude_json(system, user)
        except Exception as exc:
            logger.warning("risk_score fallback: %s", exc)
            return self._fallback_risk(vulnerabilities, asset_criticality)

    async def generate_report(
        self,
        audience_role: str,
        report_type: str,
        findings: List[Dict[str, Any]],
        period: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not self.is_ai_enabled:
            return self._fallback_report(audience_role, report_type, findings, period)
        system = self._report_system_prompt(audience_role, report_type)
        user = json.dumps(
            {
                "audience_role": audience_role,
                "report_type": report_type,
                "findings": findings,
                "period": period,
            }
        )
        try:
            data = await self._claude_json(
                system + " Return JSON: {html, summary}.", user
            )
            return {"html": data.get("html", ""), "summary": data.get("summary", "")}
        except Exception as exc:
            logger.warning("generate_report fallback: %s", exc)
            return self._fallback_report(audience_role, report_type, findings, period)

    async def threat_pattern_analysis(
        self,
        events: List[Dict[str, Any]],
        window_hours: int = 24,
    ) -> Dict[str, Any]:
        if not self.is_ai_enabled:
            return self._fallback_pattern(events)
        system = (
            "You are a threat-hunting analyst. Identify attack patterns and IOCs. "
            "Return JSON: {patterns: [], indicators_of_compromise: [], recommendation: str}."
        )
        user = json.dumps({"events": events, "window_hours": window_hours})
        try:
            return await self._claude_json(system, user)
        except Exception as exc:
            logger.warning("pattern fallback: %s", exc)
            return self._fallback_pattern(events)

    # ------------------------------------------------------------------
    # Fallbacks (rule-based)
    # ------------------------------------------------------------------
    def _fallback_classify(self, title: str, description: str) -> Dict[str, Any]:
        text = f"{title} {description}".lower()
        if any(k in text for k in ("rce", "remote code", "command injection")):
            cvss = 9.8
            cwe = "CWE-78"
        elif "sql" in text and "inject" in text:
            cvss = 9.0
            cwe = "CWE-89"
        elif "xss" in text or "cross-site script" in text:
            cvss = 6.1
            cwe = "CWE-79"
        elif "csrf" in text:
            cvss = 6.5
            cwe = "CWE-352"
        elif "ssrf" in text:
            cvss = 8.6
            cwe = "CWE-918"
        else:
            cvss = 4.0
            cwe = "CWE-200"
        return {
            "severity": cvss_to_severity(cvss),
            "cwe": cwe,
            "cvss_base": cvss,
            "confidence": 0.5,
            "rationale": "Rule-based classification (no AI key configured).",
        }

    def _fallback_risk(
        self, vulnerabilities: List[Dict[str, Any]], asset_criticality: int
    ) -> Dict[str, Any]:
        if not vulnerabilities:
            return {"risk_score": 0.0, "risk_level": "low", "drivers": []}
        severity_to_cvss = {"critical": 9.5, "high": 7.5, "medium": 5.0, "low": 2.5, "info": 0.5}

        def to_cvss(v: Dict[str, Any]) -> float:
            cvss = float(v.get("cvss_base", 0) or 0)
            if cvss > 0:
                return cvss
            return severity_to_cvss.get(str(v.get("severity", "info")).lower(), 0.5)

        max_cvss = max(to_cvss(v) for v in vulnerabilities)
        score = min(100.0, max_cvss * 10 * (1 + (asset_criticality - 1) * 0.1))
        if score >= 80:
            level = "critical"
        elif score >= 60:
            level = "high"
        elif score >= 30:
            level = "medium"
        else:
            level = "low"
        return {
            "risk_score": round(score, 2),
            "risk_level": level,
            "drivers": [f"max_cvss={max_cvss}", f"criticality={asset_criticality}"],
        }

    def _fallback_report(
        self,
        audience_role: str,
        report_type: str,
        findings: List[Dict[str, Any]],
        period: Optional[str],
    ) -> Dict[str, Any]:
        rows = "".join(
            f"<tr><td>{f.get('title', 'Finding')}</td>"
            f"<td>{f.get('severity', 'info')}</td></tr>"
            for f in findings
        )
        html = (
            f"<html><body><h1>{report_type.title()} Report</h1>"
            f"<p>Audience: {audience_role}</p><p>Period: {period or 'N/A'}</p>"
            f"<table border='1'><tr><th>Title</th><th>Severity</th></tr>"
            f"{rows}</table></body></html>"
        )
        summary = f"{len(findings)} findings for {audience_role} ({report_type})."
        return {"html": html, "summary": summary}

    def _fallback_pattern(
        self, events: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        ips: Dict[str, int] = {}
        for ev in events:
            ip = ev.get("ip")
            if ip:
                ips[ip] = ips.get(ip, 0) + 1
        suspicious = [ip for ip, c in ips.items() if c >= 5]
        return {
            "patterns": [{"type": "high_volume_source", "sources": suspicious}],
            "indicators_of_compromise": suspicious,
            "recommendation": (
                "Investigate high-volume sources and apply rate limiting."
                if suspicious
                else "No anomalies detected."
            ),
        }

    def _report_system_prompt(self, audience_role: str, report_type: str) -> str:
        tone_map = {
            "ciso": "executive risk-focused",
            "cto": "technical strategic",
            "manager": "operational and prioritized",
            "engineer": "technical with remediation steps",
            "board": "high-level business-impact",
            "compliance": "control-mapped, audit-ready",
        }
        tone = tone_map.get(audience_role.lower(), "balanced")
        return (
            f"You are generating a {report_type} security report for the {audience_role}. "
            f"Use a {tone} tone. Include findings, risk, and next steps."
        )


_ai_service: Optional[AIService] = None


def get_ai_service() -> AIService:
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
