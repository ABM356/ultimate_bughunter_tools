"""
Role-based report generator — creates different report views
for different audiences within the organization.
"""

from datetime import datetime, timezone

REPORT_ROLES = {
    "ciso": {
        "title": "CISO / Chief Information Security Officer",
        "focus": "Business risk, compliance posture, strategic recommendations",
        "sections": [
            "risk_heatmap",
            "compliance_status",
            "business_impact",
            "strategic_recommendations",
            "investment_priorities",
        ],
    },
    "cto": {
        "title": "CTO / VP Engineering",
        "focus": "Technical architecture risks, engineering effort, technology stack",
        "sections": [
            "architecture_findings",
            "technical_debt",
            "engineering_effort",
            "technology_recommendations",
            "security_roadmap",
        ],
    },
    "manager": {
        "title": "Department Manager / Project Manager",
        "focus": "High-level summary, timelines, budget, action items",
        "sections": [
            "executive_summary",
            "risk_overview",
            "remediation_timeline",
            "budget_estimate",
            "action_items",
        ],
    },
    "security_engineer": {
        "title": "Security Engineer / SOC Analyst",
        "focus": "Full technical details, CVEs, tool outputs, code-level fixes",
        "sections": [
            "full_vulnerability_details",
            "tool_outputs",
            "attack_vectors",
            "detection_rules",
            "remediation_code",
        ],
    },
    "software_engineer": {
        "title": "Software Engineer / Developer",
        "focus": "Code-level vulnerabilities, secure coding recommendations, dependency issues",
        "sections": [
            "code_vulnerabilities",
            "dependency_audit",
            "secure_coding_guidelines",
            "fix_examples",
            "ci_cd_recommendations",
        ],
    },
    "network_engineer": {
        "title": "Network Engineer",
        "focus": "Network findings, firewall rules, IDS/IPS, port exposure",
        "sections": [
            "network_findings",
            "exposed_services",
            "firewall_recommendations",
            "ids_ips_rules",
            "network_architecture",
        ],
    },
    "board": {
        "title": "Board of Directors / Executive Board",
        "focus": "One-page risk summary, financial exposure, liability",
        "sections": [
            "one_page_summary",
            "risk_score",
            "financial_exposure",
            "peer_comparison",
            "recommended_investment",
        ],
    },
    "compliance_officer": {
        "title": "Compliance Officer / Legal",
        "focus": "Regulatory compliance, audit readiness, legal exposure",
        "sections": [
            "compliance_matrix",
            "regulatory_gaps",
            "audit_readiness",
            "legal_exposure",
            "remediation_obligations",
        ],
    },
}


def generate_role_report(assessment_data, summary, role):
    role_config = REPORT_ROLES.get(role, REPORT_ROLES["manager"])
    stats = summary.get("stats", {}) if summary else {}
    results = summary.get("results", []) if summary else []

    sections_html = ""
    for section in role_config["sections"]:
        renderer = SECTION_RENDERERS.get(section, _render_placeholder)
        sections_html += renderer(assessment_data, summary, stats, results)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{role_config['title']} Report — {assessment_data.get('id', 'N/A')}</title>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #0a0a0f; color: #e0e0e0; line-height: 1.7; }}
    .container {{ max-width: 1100px; margin: 0 auto; padding: 2rem; }}
    .header {{ background: linear-gradient(135deg, #1a1a2e, #16213e); border: 1px solid #0f3460; border-radius: 12px; padding: 2rem; margin-bottom: 2rem; }}
    .header h1 {{ color: #00d4ff; font-size: 1.6rem; }}
    .header .role-badge {{ display: inline-block; background: #00d4ff; color: #000; padding: 4px 12px; border-radius: 4px; font-size: 0.8rem; font-weight: 700; margin-top: 0.5rem; }}
    .header .meta {{ color: #7f8c8d; font-size: 0.9rem; margin-top: 1rem; }}
    .section {{ background: #111118; border: 1px solid #222; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; }}
    .section h2 {{ color: #00d4ff; font-size: 1.2rem; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid #222; }}
    .metric-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 1rem; }}
    .metric {{ background: rgba(255,255,255,0.05); border-radius: 8px; padding: 1rem; text-align: center; }}
    .metric .number {{ font-size: 2rem; font-weight: 700; color: #00d4ff; }}
    .metric .label {{ font-size: 0.75rem; text-transform: uppercase; color: #7f8c8d; }}
    .risk-high {{ color: #ff1744; }}
    .risk-medium {{ color: #ffc400; }}
    .risk-low {{ color: #00c853; }}
    .bar {{ height: 8px; border-radius: 4px; margin: 0.25rem 0; }}
    .bar-critical {{ background: #ff1744; }}
    .bar-high {{ background: #ff6d00; }}
    .bar-medium {{ background: #ffc400; }}
    .bar-low {{ background: #00c853; }}
    table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; }}
    th {{ text-align: left; padding: 0.75rem; color: #7f8c8d; font-size: 0.8rem; text-transform: uppercase; border-bottom: 2px solid #222; }}
    td {{ padding: 0.75rem; border-bottom: 1px solid #1a1a1a; }}
    .action-item {{ padding: 0.75rem 1rem; margin: 0.5rem 0; background: rgba(0,212,255,0.05); border-left: 3px solid #00d4ff; border-radius: 0 8px 8px 0; }}
    .action-item strong {{ color: #00d4ff; }}
    .footer {{ text-align: center; padding: 2rem; color: #555; font-size: 0.85rem; }}
    .confidential {{ background: #ff1744; color: #fff; text-align: center; padding: 0.5rem; font-weight: 700; letter-spacing: 2px; border-radius: 4px; margin-bottom: 1rem; }}
</style>
</head>
<body>
<div class="container">
    <div class="confidential">CONFIDENTIAL — {role_config['title'].upper()} REPORT</div>

    <div class="header">
        <h1>Security Assessment Report</h1>
        <span class="role-badge">{role_config['title']}</span>
        <div class="meta">
            <p>Assessment: {assessment_data.get('id', 'N/A')} | Target: {assessment_data.get('target', 'N/A')} | Tier: {assessment_data.get('tier', 'N/A')} ({assessment_data.get('tier_name', '')})</p>
            <p>Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} | Focus: {role_config['focus']}</p>
        </div>
    </div>

    {sections_html}

    <div class="footer">
        <p>Generated by Ultimate BugHunter Platform v2.0 | Role: {role_config['title']}</p>
        <p>This report is confidential and intended only for the named recipient role.</p>
    </div>
</div>
</body>
</html>"""


# ─── Section Renderers ───

def _render_executive_summary(assessment, summary, stats, results):
    total = stats.get("total_tools", 0)
    completed = stats.get("completed", 0)
    errors = stats.get("errors", 0)
    return f"""<div class="section">
        <h2>Executive Summary</h2>
        <p>A Tier {assessment.get('tier', 'N/A')} security assessment was conducted against
        <strong>{assessment.get('target', 'N/A')}</strong>. {total} security tools were deployed,
        with {completed} completing successfully and {errors} encountering errors.</p>
        <div class="metric-grid" style="margin-top:1rem;">
            <div class="metric"><div class="number">{total}</div><div class="label">Tools Run</div></div>
            <div class="metric"><div class="number">{completed}</div><div class="label">Completed</div></div>
            <div class="metric"><div class="number">{errors}</div><div class="label">Issues</div></div>
            <div class="metric"><div class="number">{completed}/{total}</div><div class="label">Coverage</div></div>
        </div>
    </div>"""


def _render_risk_overview(assessment, summary, stats, results):
    return f"""<div class="section">
        <h2>Risk Overview</h2>
        <p>Based on the assessment results, the following risk posture has been identified:</p>
        <div class="metric-grid">
            <div class="metric"><div class="number risk-high">0</div><div class="label">Critical</div></div>
            <div class="metric"><div class="number risk-high">0</div><div class="label">High</div></div>
            <div class="metric"><div class="number risk-medium">0</div><div class="label">Medium</div></div>
            <div class="metric"><div class="number risk-low">0</div><div class="label">Low</div></div>
        </div>
        <p style="margin-top:1rem;color:#7f8c8d;">Detailed severity counts are populated from parsed tool outputs. Review the raw findings for specifics.</p>
    </div>"""


def _render_risk_heatmap(assessment, summary, stats, results):
    categories = ["Web App", "Network", "Cloud", "Auth", "Config", "Data", "Compliance"]
    return f"""<div class="section">
        <h2>Risk Heatmap</h2>
        <table>
            <thead><tr><th>Category</th><th>Risk Level</th><th>Findings</th><th>Status</th></tr></thead>
            <tbody>
            {''.join(f'<tr><td>{cat}</td><td><span class="risk-medium">Pending Review</span></td><td>See details</td><td>Assessment complete</td></tr>' for cat in categories)}
            </tbody>
        </table>
    </div>"""


def _render_compliance_status(assessment, summary, stats, results):
    tier = assessment.get("tier", 1)
    from platform.tiers import BUSINESS_TIERS
    compliance = BUSINESS_TIERS.get(tier, {}).get("compliance", [])
    if not compliance:
        return '<div class="section"><h2>Compliance Status</h2><p>No compliance frameworks mapped for this tier.</p></div>'

    rows = "".join(
        f'<tr><td>{c.replace("_", " ")}</td><td>Pending Review</td><td>Run full assessment for compliance mapping</td></tr>'
        for c in compliance
    )
    return f"""<div class="section">
        <h2>Compliance Status</h2>
        <table>
            <thead><tr><th>Framework</th><th>Status</th><th>Notes</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>"""


def _render_action_items(assessment, summary, stats, results):
    items = [
        ("P1 — Critical", "Review all tool outputs for critical/high severity findings"),
        ("P2 — High", f"Install {stats.get('not_installed', 0)} missing tools and rerun"),
        ("P3 — Medium", "Map findings to compliance requirements"),
        ("P4 — Low", "Schedule next assessment cycle"),
    ]
    html = "".join(
        f'<div class="action-item"><strong>{p}</strong>: {desc}</div>'
        for p, desc in items
    )
    return f'<div class="section"><h2>Action Items</h2>{html}</div>'


def _render_remediation_timeline(assessment, summary, stats, results):
    return """<div class="section">
        <h2>Remediation Timeline</h2>
        <table>
            <thead><tr><th>Phase</th><th>Timeline</th><th>Focus</th></tr></thead>
            <tbody>
                <tr><td>Immediate (0-48h)</td><td>Days 1-2</td><td>Critical vulnerabilities, exposed credentials</td></tr>
                <tr><td>Short-term (1-2 weeks)</td><td>Week 1-2</td><td>High severity findings, configuration fixes</td></tr>
                <tr><td>Medium-term (1-3 months)</td><td>Month 1-3</td><td>Architecture improvements, monitoring deployment</td></tr>
                <tr><td>Long-term (3-6 months)</td><td>Month 3-6</td><td>Security program maturation, compliance readiness</td></tr>
            </tbody>
        </table>
    </div>"""


def _render_budget_estimate(assessment, summary, stats, results):
    tier = assessment.get("tier", 1)
    estimates = {
        1: {"remediation": "5,000 - 15,000", "monitoring": "500/mo", "retesting": "2,500/quarter"},
        2: {"remediation": "15,000 - 50,000", "monitoring": "2,000/mo", "retesting": "10,000/quarter"},
        3: {"remediation": "50,000 - 200,000", "monitoring": "5,000/mo", "retesting": "25,000/quarter"},
        4: {"remediation": "200,000 - 1,000,000", "monitoring": "15,000/mo", "retesting": "50,000/quarter"},
    }
    est = estimates.get(tier, estimates[1])
    return f"""<div class="section">
        <h2>Budget Estimate</h2>
        <div class="metric-grid">
            <div class="metric"><div class="number" style="font-size:1.2rem;">${est['remediation']}</div><div class="label">Remediation</div></div>
            <div class="metric"><div class="number" style="font-size:1.2rem;">${est['monitoring']}</div><div class="label">Monitoring</div></div>
            <div class="metric"><div class="number" style="font-size:1.2rem;">${est['retesting']}</div><div class="label">Retesting</div></div>
        </div>
        <p style="margin-top:1rem;color:#7f8c8d;">Estimates based on Tier {tier} assessment scope. Actual costs depend on findings severity and existing infrastructure.</p>
    </div>"""


def _render_tool_outputs(assessment, summary, stats, results):
    if not results:
        return '<div class="section"><h2>Tool Outputs</h2><p>No tool results available. Run the assessment first.</p></div>'

    rows = "".join(
        f'<tr><td>{r.get("tool", "")}</td><td>{r.get("team", "").upper()}</td><td>{r.get("category", "")}</td><td>{r.get("status", "")}</td><td>{r.get("duration_seconds", 0):.1f}s</td><td>{r.get("findings_count", 0)}</td></tr>'
        for r in results
    )
    return f"""<div class="section">
        <h2>Tool Execution Details</h2>
        <table>
            <thead><tr><th>Tool</th><th>Team</th><th>Category</th><th>Status</th><th>Duration</th><th>Findings</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>"""


def _render_one_page_summary(assessment, summary, stats, results):
    total = stats.get("total_tools", 0)
    completed = stats.get("completed", 0)
    return f"""<div class="section">
        <h2>One-Page Executive Summary</h2>
        <p style="font-size:1.1rem;">A Tier {assessment.get('tier', 'N/A')} security assessment of <strong>{assessment.get('target', 'N/A')}</strong>
        was completed using {total} automated security tools. {completed} tools completed successfully.</p>
        <h3 style="color:#00d4ff;margin:1.5rem 0 0.5rem;">Key Takeaway</h3>
        <p>The assessment provides baseline visibility into the organization's security posture. Detailed findings
        require review by the security team to quantify specific risk and financial exposure.</p>
        <h3 style="color:#00d4ff;margin:1.5rem 0 0.5rem;">Recommended Board Action</h3>
        <p>Allocate resources for remediation of identified findings and approve ongoing security monitoring budget.</p>
    </div>"""


def _render_placeholder(assessment, summary, stats, results):
    return '<div class="section"><h2>Section</h2><p>Detailed content populated from assessment findings.</p></div>'


SECTION_RENDERERS = {
    "executive_summary": _render_executive_summary,
    "risk_overview": _render_risk_overview,
    "risk_heatmap": _render_risk_heatmap,
    "compliance_status": _render_compliance_status,
    "compliance_matrix": _render_compliance_status,
    "action_items": _render_action_items,
    "remediation_timeline": _render_remediation_timeline,
    "budget_estimate": _render_budget_estimate,
    "tool_outputs": _render_tool_outputs,
    "full_vulnerability_details": _render_tool_outputs,
    "one_page_summary": _render_one_page_summary,
    "risk_score": _render_risk_overview,
    "business_impact": _render_budget_estimate,
    "strategic_recommendations": _render_action_items,
    "investment_priorities": _render_budget_estimate,
    "architecture_findings": _render_tool_outputs,
    "technical_debt": _render_placeholder,
    "engineering_effort": _render_remediation_timeline,
    "technology_recommendations": _render_action_items,
    "security_roadmap": _render_remediation_timeline,
    "code_vulnerabilities": _render_tool_outputs,
    "dependency_audit": _render_placeholder,
    "secure_coding_guidelines": _render_placeholder,
    "fix_examples": _render_placeholder,
    "ci_cd_recommendations": _render_placeholder,
    "network_findings": _render_tool_outputs,
    "exposed_services": _render_placeholder,
    "firewall_recommendations": _render_placeholder,
    "ids_ips_rules": _render_placeholder,
    "network_architecture": _render_placeholder,
    "financial_exposure": _render_budget_estimate,
    "peer_comparison": _render_placeholder,
    "recommended_investment": _render_budget_estimate,
    "regulatory_gaps": _render_compliance_status,
    "audit_readiness": _render_placeholder,
    "legal_exposure": _render_placeholder,
    "remediation_obligations": _render_action_items,
    "attack_vectors": _render_placeholder,
    "detection_rules": _render_placeholder,
    "remediation_code": _render_placeholder,
}
