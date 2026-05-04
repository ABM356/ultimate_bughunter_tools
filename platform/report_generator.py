"""
Report generator — produces HTML reports from assessment results.
Supports all tier-level report sections with severity-coded findings.
"""

import json
import os
from datetime import datetime, timezone


def generate_report(assessment, output_path=None):
    tier = assessment.tier
    results = assessment.results
    output_path = output_path or os.path.join(assessment.output_dir, "report.html")

    stats = _compute_stats(results)
    findings_html = _render_findings(results)
    tools_html = _render_tool_summary(results)
    compliance_html = _render_compliance(tier)
    recommendations_html = _render_recommendations(results, tier)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Security Assessment Report — {assessment.id}</title>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #0a0a0f; color: #e0e0e0; line-height: 1.6; }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem; }}
    .header {{ background: linear-gradient(135deg, #1a1a2e, #16213e); border: 1px solid #0f3460; border-radius: 12px; padding: 2rem; margin-bottom: 2rem; }}
    .header h1 {{ color: #00d4ff; font-size: 1.8rem; margin-bottom: 0.5rem; }}
    .header .subtitle {{ color: #7f8c8d; font-size: 0.95rem; }}
    .meta-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1.5rem; }}
    .meta-card {{ background: rgba(255,255,255,0.05); border-radius: 8px; padding: 1rem; }}
    .meta-card .label {{ color: #7f8c8d; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }}
    .meta-card .value {{ color: #fff; font-size: 1.3rem; font-weight: 600; margin-top: 0.25rem; }}
    .section {{ background: #111118; border: 1px solid #222; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; }}
    .section h2 {{ color: #00d4ff; font-size: 1.3rem; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid #222; }}
    .severity-badge {{ display: inline-block; padding: 2px 10px; border-radius: 4px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; }}
    .severity-critical {{ background: #ff1744; color: #fff; }}
    .severity-high {{ background: #ff6d00; color: #fff; }}
    .severity-medium {{ background: #ffc400; color: #000; }}
    .severity-low {{ background: #00c853; color: #fff; }}
    .severity-info {{ background: #2979ff; color: #fff; }}
    .stats-row {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; margin-bottom: 1.5rem; }}
    .stat-box {{ text-align: center; padding: 1rem; border-radius: 8px; }}
    .stat-box.critical {{ background: rgba(255,23,68,0.15); border: 1px solid #ff1744; }}
    .stat-box.high {{ background: rgba(255,109,0,0.15); border: 1px solid #ff6d00; }}
    .stat-box.medium {{ background: rgba(255,196,0,0.15); border: 1px solid #ffc400; }}
    .stat-box.low {{ background: rgba(0,200,83,0.15); border: 1px solid #00c853; }}
    .stat-box.info {{ background: rgba(41,121,255,0.15); border: 1px solid #2979ff; }}
    .stat-number {{ font-size: 2rem; font-weight: 700; }}
    .stat-label {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.25rem; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th {{ text-align: left; padding: 0.75rem; color: #7f8c8d; font-size: 0.8rem; text-transform: uppercase; border-bottom: 2px solid #222; }}
    td {{ padding: 0.75rem; border-bottom: 1px solid #1a1a1a; }}
    .status-completed {{ color: #00c853; }}
    .status-error {{ color: #ff1744; }}
    .status-timeout {{ color: #ffc400; }}
    .status-not_installed {{ color: #7f8c8d; }}
    .team-red {{ color: #ff1744; }}
    .team-blue {{ color: #2979ff; }}
    .team-both {{ color: #aa00ff; }}
    .compliance-item {{ padding: 0.75rem; margin: 0.5rem 0; background: rgba(255,255,255,0.03); border-radius: 6px; border-left: 3px solid #00d4ff; }}
    .recommendation {{ padding: 1rem; margin: 0.5rem 0; background: rgba(0,212,255,0.05); border-radius: 8px; border-left: 3px solid #00d4ff; }}
    .recommendation h4 {{ color: #00d4ff; margin-bottom: 0.25rem; }}
    .footer {{ text-align: center; padding: 2rem; color: #555; font-size: 0.85rem; }}
    .footer a {{ color: #00d4ff; text-decoration: none; }}
</style>
</head>
<body>
<div class="container">

    <div class="header">
        <h1>Security Assessment Report</h1>
        <div class="subtitle">Assessment ID: {assessment.id} | Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</div>
        <div class="meta-grid">
            <div class="meta-card">
                <div class="label">Target</div>
                <div class="value">{assessment.target}</div>
            </div>
            <div class="meta-card">
                <div class="label">Business Tier</div>
                <div class="value">Tier {assessment.tier_num}</div>
            </div>
            <div class="meta-card">
                <div class="label">Tier Profile</div>
                <div class="value">{tier['name']}</div>
            </div>
            <div class="meta-card">
                <div class="label">Scope</div>
                <div class="value">{assessment.scope.upper()}</div>
            </div>
            <div class="meta-card">
                <div class="label">Tools Run</div>
                <div class="value">{stats['total']}</div>
            </div>
            <div class="meta-card">
                <div class="label">Completed</div>
                <div class="value">{stats['completed']}</div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>Executive Summary</h2>
        <p>This security assessment was conducted at <strong>Tier {assessment.tier_num} ({tier['name']})</strong> level
        against <strong>{assessment.target}</strong>. A total of <strong>{stats['total']}</strong> security tools
        were executed, with <strong>{stats['completed']}</strong> completing successfully.
        The assessment covered {assessment.scope.replace('+', ' and ').upper()} team operations.</p>

        <div class="stats-row" style="margin-top: 1.5rem;">
            <div class="stat-box critical">
                <div class="stat-number">{stats['severity']['critical']}</div>
                <div class="stat-label">Critical</div>
            </div>
            <div class="stat-box high">
                <div class="stat-number">{stats['severity']['high']}</div>
                <div class="stat-label">High</div>
            </div>
            <div class="stat-box medium">
                <div class="stat-number">{stats['severity']['medium']}</div>
                <div class="stat-label">Medium</div>
            </div>
            <div class="stat-box low">
                <div class="stat-number">{stats['severity']['low']}</div>
                <div class="stat-label">Low</div>
            </div>
            <div class="stat-box info">
                <div class="stat-number">{stats['severity']['info']}</div>
                <div class="stat-label">Info</div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>Tool Execution Summary</h2>
        {tools_html}
    </div>

    <div class="section">
        <h2>Findings</h2>
        {findings_html}
    </div>

    {compliance_html}

    <div class="section">
        <h2>Recommendations</h2>
        {recommendations_html}
    </div>

    <div class="footer">
        <p>Generated by <strong>Ultimate BugHunter Platform v2.0</strong></p>
        <p>This report is confidential. Unauthorized distribution is prohibited.</p>
    </div>

</div>
</body>
</html>"""

    with open(output_path, "w") as f:
        f.write(html)

    return output_path


def _compute_stats(results):
    severity = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for r in results:
        for k in severity:
            severity[k] += r.severity_counts.get(k, 0)

    return {
        "total": len(results),
        "completed": len([r for r in results if r.status == "completed"]),
        "errors": len([r for r in results if r.status == "error"]),
        "timeouts": len([r for r in results if r.status == "timeout"]),
        "not_installed": len([r for r in results if r.status == "not_installed"]),
        "severity": severity,
    }


def _render_tool_summary(results):
    rows = ""
    for r in results:
        team_class = f"team-{r.team}"
        status_class = f"status-{r.status}"
        rows += f"""<tr>
            <td><span class="{team_class}">{r.team.upper()}</span></td>
            <td>{r.tool_name}</td>
            <td>{r.category}</td>
            <td><span class="{status_class}">{r.status}</span></td>
            <td>{r.duration_seconds:.1f}s</td>
            <td>{len(r.findings)}</td>
        </tr>"""

    return f"""<table>
        <thead><tr><th>Team</th><th>Tool</th><th>Category</th><th>Status</th><th>Duration</th><th>Findings</th></tr></thead>
        <tbody>{rows}</tbody>
    </table>"""


def _render_findings(results):
    findings_with_data = [r for r in results if r.findings]
    if not findings_with_data:
        return "<p>Detailed findings will be populated once raw tool outputs are parsed. See the <code>raw/</code> directory for individual tool outputs.</p>"

    html = ""
    for r in findings_with_data:
        for f in r.findings:
            sev = f.get("severity", "info")
            html += f"""<div style="padding: 1rem; margin: 0.5rem 0; background: rgba(255,255,255,0.03); border-radius: 8px;">
                <span class="severity-badge severity-{sev}">{sev}</span>
                <strong style="margin-left: 0.5rem;">{f.get('title', 'Finding')}</strong>
                <span style="color: #7f8c8d; margin-left: 0.5rem;">via {r.tool_name}</span>
                <p style="margin-top: 0.5rem; color: #aaa;">{f.get('description', '')}</p>
            </div>"""
    return html


def _render_compliance(tier):
    if not tier.get("compliance"):
        return ""

    items = ""
    for standard in tier["compliance"]:
        display_name = standard.replace("_", " ")
        items += f'<div class="compliance-item"><strong>{display_name}</strong> — Assessment mapped to this framework</div>'

    return f"""<div class="section">
        <h2>Compliance Mapping</h2>
        <p>This assessment tier includes mapping to the following compliance frameworks:</p>
        {items}
    </div>"""


def _render_recommendations(results, tier):
    recs = []

    not_installed = [r for r in results if r.status == "not_installed"]
    if not_installed:
        tool_names = ", ".join(r.tool_name for r in not_installed[:10])
        recs.append({
            "title": "Install Missing Tools",
            "body": f"The following tools were not found: {tool_names}. Run the platform installer to set them up.",
        })

    errors = [r for r in results if r.status == "error"]
    if errors:
        tool_names = ", ".join(r.tool_name for r in errors[:10])
        recs.append({
            "title": "Investigate Tool Errors",
            "body": f"These tools encountered errors: {tool_names}. Check raw output files for details.",
        })

    recs.append({
        "title": "Schedule Regular Assessments",
        "body": f"As a {tier['name']}-tier organization, schedule assessments at regular intervals to catch new vulnerabilities.",
    })

    if tier.get("compliance"):
        recs.append({
            "title": "Review Compliance Gaps",
            "body": "Cross-reference findings with the compliance frameworks listed above and prioritize remediation of non-compliant items.",
        })

    recs.append({
        "title": "Implement Blue Team Monitoring",
        "body": "Deploy continuous monitoring using the defensive tools in this platform to detect threats between assessments.",
    })

    html = ""
    for r in recs:
        html += f"""<div class="recommendation">
            <h4>{r['title']}</h4>
            <p>{r['body']}</p>
        </div>"""
    return html
