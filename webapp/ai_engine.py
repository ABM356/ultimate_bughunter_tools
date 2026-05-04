"""
AI Engine — Provides intelligent analysis, recommendations,
and automated insights across all assessment data.
"""

import json
import os
from datetime import datetime, timezone


class AIEngine:
    """
    AI-powered analysis engine for security assessments.
    Integrates with Claude API when ANTHROPIC_API_KEY is set,
    falls back to rule-based analysis otherwise.
    """

    def __init__(self):
        self.api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        self.model = "claude-sonnet-4-6"

    def _has_api(self):
        return bool(self.api_key)

    def analyze_results(self, summary, tier):
        if self._has_api():
            return self._ai_analyze(summary, tier)
        return self._rule_based_analyze(summary, tier)

    def generate_recommendations(self, findings, tier):
        if self._has_api():
            return self._ai_recommendations(findings, tier)
        return self._rule_based_recommendations(findings, tier)

    def generate_executive_brief(self, summary, tier, audience="ciso"):
        if self._has_api():
            return self._ai_executive_brief(summary, tier, audience)
        return self._rule_based_executive_brief(summary, tier, audience)

    # ─── Claude API Integration ───

    def _ai_analyze(self, summary, tier):
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)

            prompt = f"""Analyze this security assessment summary and provide:
1. Overall risk rating (Critical/High/Medium/Low)
2. Top 3 most concerning findings
3. Attack surface analysis
4. Recommended immediate actions

Assessment Tier: {tier}
Summary: {json.dumps(summary, indent=2)}

Respond in JSON format with keys: risk_rating, top_concerns, attack_surface, immediate_actions"""

            message = client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )
            text = message.content[0].text
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return {"analysis": text, "source": "ai"}

        except Exception as e:
            return {**self._rule_based_analyze(summary, tier), "ai_error": str(e)}

    def _ai_recommendations(self, findings, tier):
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)

            prompt = f"""Based on these security findings from a Tier {tier} assessment,
provide prioritized remediation recommendations. Group by severity and include
estimated effort for each fix.

Findings: {json.dumps(findings, indent=2)}

Respond in JSON format: a list of objects with keys: priority, title, description, effort, severity"""

            message = client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )
            text = message.content[0].text
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return [{"title": "AI Analysis", "description": text}]

        except Exception as e:
            return self._rule_based_recommendations(findings, tier)

    def _ai_executive_brief(self, summary, tier, audience):
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)

            audience_context = {
                "ciso": "Write for a CISO: focus on business risk, compliance gaps, and strategic recommendations. Use business language, not technical jargon.",
                "cto": "Write for a CTO: focus on technical architecture risks, engineering effort for fixes, and technology stack concerns.",
                "manager": "Write for a non-technical manager: focus on high-level risk summary, budget implications, and timeline for remediation.",
                "engineer": "Write for a security engineer: include technical details, specific CVEs, tool output references, and code-level fixes.",
                "network_engineer": "Write for a network engineer: focus on network-level findings, firewall rules, IDS/IPS gaps, and network architecture issues.",
                "board": "Write for a board of directors: 1-page summary with risk heat map, financial exposure, and recommended investments.",
            }

            prompt = f"""{audience_context.get(audience, audience_context['manager'])}

Generate an executive brief for this security assessment.

Assessment Tier: {tier}
Summary: {json.dumps(summary, indent=2)}

Format as a professional report section in HTML."""

            message = client.messages.create(
                model=self.model,
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}],
            )
            return message.content[0].text

        except Exception as e:
            return self._rule_based_executive_brief(summary, tier, audience)

    # ─── Rule-Based Fallback ───

    def _rule_based_analyze(self, summary, tier):
        stats = summary.get("stats", {})
        total = stats.get("total_tools", 0)
        completed = stats.get("completed", 0)
        errors = stats.get("errors", 0)

        completion_rate = completed / max(total, 1) * 100
        error_rate = errors / max(total, 1) * 100

        if error_rate > 50:
            risk = "Unknown — Too many tool failures"
        elif tier >= 3 and completion_rate < 50:
            risk = "High — Incomplete enterprise-level assessment"
        elif completion_rate > 80:
            risk = "Assessment Complete — Review findings for risk determination"
        else:
            risk = "Medium — Partial assessment, some tools failed"

        return {
            "risk_rating": risk,
            "completion_rate": f"{completion_rate:.0f}%",
            "error_rate": f"{error_rate:.0f}%",
            "top_concerns": [
                "Review all completed tool outputs for vulnerability findings",
                "Install missing tools and rerun failed scans",
                "Cross-reference findings against compliance requirements",
            ],
            "immediate_actions": [
                "Address any critical/high severity findings immediately",
                f"Install {stats.get('not_installed', 0)} missing tools",
                "Schedule a follow-up assessment after remediation",
            ],
            "source": "rule_based",
        }

    def _rule_based_recommendations(self, findings, tier):
        recommendations = []

        recommendations.append({
            "priority": 1,
            "title": "Install All Required Tools",
            "description": "Ensure all tools for your tier are installed for comprehensive coverage",
            "effort": "1-2 hours",
            "severity": "high",
        })

        if tier >= 2:
            recommendations.append({
                "priority": 2,
                "title": "Enable Continuous Monitoring",
                "description": "Deploy blue team tools (Wazuh, Suricata) for ongoing threat detection",
                "effort": "4-8 hours",
                "severity": "high",
            })

        if tier >= 3:
            recommendations.append({
                "priority": 3,
                "title": "Implement Cloud Security Posture Management",
                "description": "Run Prowler/ScoutSuite regularly against cloud infrastructure",
                "effort": "8-16 hours",
                "severity": "medium",
            })

        recommendations.append({
            "priority": len(recommendations) + 1,
            "title": "Schedule Regular Reassessments",
            "description": f"As a Tier {tier} organization, reassess quarterly at minimum",
            "effort": "Ongoing",
            "severity": "medium",
        })

        return recommendations

    def _rule_based_executive_brief(self, summary, tier, audience):
        stats = summary.get("stats", {}) if summary else {}
        target = summary.get("target", "Unknown") if summary else "Unknown"

        return f"""
        <div class="executive-brief">
            <h3>Executive Brief — {audience.upper()}</h3>
            <p><strong>Target:</strong> {target}</p>
            <p><strong>Assessment Level:</strong> Tier {tier}</p>
            <p><strong>Tools Executed:</strong> {stats.get('total_tools', 0)}</p>
            <p><strong>Completed:</strong> {stats.get('completed', 0)}</p>
            <p><strong>Errors:</strong> {stats.get('errors', 0)}</p>
            <hr>
            <p>A comprehensive AI-powered analysis is available when ANTHROPIC_API_KEY is configured.
            Set this environment variable to enable intelligent risk scoring, prioritized recommendations,
            and audience-specific executive briefs.</p>
        </div>
        """
