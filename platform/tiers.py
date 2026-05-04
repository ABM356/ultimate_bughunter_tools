"""
Business tier definitions for the cybersecurity platform.
Each tier maps to a business profile with specific tools, scan depth, and compliance needs.
"""

BUSINESS_TIERS = {
    1: {
        "name": "Startup / Small Business",
        "label": "TIER-1-STARTER",
        "description": "Basic security assessment for startups and small businesses with web presence",
        "target_audience": [
            "Startups with < 50 employees",
            "Small e-commerce shops",
            "Personal blogs / portfolios",
            "Small SaaS products",
        ],
        "scan_profile": {
            "depth": "surface",
            "max_duration_hours": 2,
            "concurrent_tools": 3,
            "rate_limit": "conservative",
        },
        "red_team_focus": [
            "recon_subdomain",
            "recon_dns",
            "recon_http",
            "vuln_scanning",
            "brute_dir",
            "web_sqli",
            "web_xss",
            "ssl_tls",
        ],
        "blue_team_focus": [
            "hardening",
            "secrets_detection",
        ],
        "compliance": [],
        "report_sections": [
            "executive_summary",
            "vulnerability_findings",
            "risk_ratings",
            "remediation_steps",
        ],
    },

    2: {
        "name": "Mid-size Business",
        "label": "TIER-2-BUSINESS",
        "description": "Comprehensive security testing for growing businesses with APIs and multiple services",
        "target_audience": [
            "Companies with 50-500 employees",
            "SaaS platforms with APIs",
            "E-commerce with payment processing",
            "Regional service providers",
        ],
        "scan_profile": {
            "depth": "moderate",
            "max_duration_hours": 8,
            "concurrent_tools": 5,
            "rate_limit": "moderate",
        },
        "red_team_focus": [
            "recon_subdomain",
            "recon_dns",
            "recon_http",
            "recon_crawl",
            "recon_ports",
            "recon_osint",
            "recon_screenshot",
            "vuln_scanning",
            "web_sqli",
            "web_xss",
            "web_ssrf",
            "web_xxe",
            "web_lfi",
            "web_cors",
            "web_jwt",
            "web_cmdi",
            "brute_dir",
            "brute_password",
            "takeover",
            "cloud_s3",
            "git_recon",
            "ssl_tls",
            "automation",
        ],
        "blue_team_focus": [
            "hardening",
            "secrets_detection",
            "ids_ips",
            "siem",
        ],
        "compliance": ["OWASP_TOP_10", "PCI_DSS_BASIC"],
        "report_sections": [
            "executive_summary",
            "vulnerability_findings",
            "risk_ratings",
            "attack_surface_map",
            "remediation_steps",
            "compliance_checklist",
            "retesting_recommendations",
        ],
    },

    3: {
        "name": "Enterprise",
        "label": "TIER-3-ENTERPRISE",
        "description": "Deep security assessment for enterprise organizations with complex infrastructure",
        "target_audience": [
            "Companies with 500-5000 employees",
            "Multi-region deployments",
            "Cloud-native organizations",
            "Financial services & healthcare",
        ],
        "scan_profile": {
            "depth": "deep",
            "max_duration_hours": 24,
            "concurrent_tools": 10,
            "rate_limit": "aggressive",
        },
        "red_team_focus": [
            "recon_subdomain",
            "recon_dns",
            "recon_http",
            "recon_crawl",
            "recon_ports",
            "recon_osint",
            "recon_screenshot",
            "vuln_scanning",
            "web_sqli",
            "web_xss",
            "web_ssrf",
            "web_xxe",
            "web_lfi",
            "web_cors",
            "web_jwt",
            "web_cmdi",
            "web_deserialization",
            "brute_dir",
            "brute_password",
            "exploit",
            "network",
            "cloud_offensive",
            "cloud_s3",
            "mobile",
            "takeover",
            "git_recon",
            "dorking",
            "wordlists",
            "automation",
            "ssl_tls",
        ],
        "blue_team_focus": [
            "hardening",
            "secrets_detection",
            "ids_ips",
            "siem",
            "forensics",
            "threat_intel",
            "container_security",
            "cloud_defensive",
            "network_monitoring",
            "waf",
        ],
        "compliance": [
            "OWASP_TOP_10",
            "PCI_DSS",
            "SOC2",
            "HIPAA",
            "ISO_27001",
        ],
        "report_sections": [
            "executive_summary",
            "vulnerability_findings",
            "risk_ratings",
            "attack_surface_map",
            "attack_chain_analysis",
            "remediation_steps",
            "compliance_checklist",
            "threat_modeling",
            "retesting_recommendations",
            "blue_team_recommendations",
        ],
    },

    4: {
        "name": "Critical Infrastructure / Government",
        "label": "TIER-4-CRITICAL",
        "description": "Maximum-depth assessment for critical infrastructure, government, and defense organizations",
        "target_audience": [
            "Government agencies",
            "Critical infrastructure (energy, telecom, transport)",
            "Defense contractors",
            "Organizations with 5000+ employees",
            "Financial institutions (tier-1 banks)",
        ],
        "scan_profile": {
            "depth": "maximum",
            "max_duration_hours": 72,
            "concurrent_tools": 15,
            "rate_limit": "full",
        },
        "red_team_focus": "ALL",
        "blue_team_focus": "ALL",
        "compliance": [
            "OWASP_TOP_10",
            "PCI_DSS",
            "SOC2",
            "HIPAA",
            "ISO_27001",
            "NIST_800_53",
            "NIST_CSF",
            "FedRAMP",
            "CMMC",
        ],
        "report_sections": [
            "executive_summary",
            "vulnerability_findings",
            "risk_ratings",
            "attack_surface_map",
            "attack_chain_analysis",
            "red_team_narrative",
            "remediation_steps",
            "compliance_checklist",
            "threat_modeling",
            "zero_day_assessment",
            "supply_chain_analysis",
            "retesting_recommendations",
            "blue_team_recommendations",
            "incident_response_readiness",
            "security_architecture_review",
        ],
    },
}


def get_tier(tier_num):
    return BUSINESS_TIERS.get(tier_num)


def get_tier_tools(tier_num, registry):
    tier = BUSINESS_TIERS[tier_num]
    tools = {}

    for name, tool in registry.items():
        if tool["tier"] > tier_num:
            continue

        if tier["red_team_focus"] == "ALL" or tier["blue_team_focus"] == "ALL":
            tools[name] = tool
            continue

        if tool["team"] in ("red", "both") and tool["category"] in tier["red_team_focus"]:
            tools[name] = tool
        elif tool["team"] in ("blue", "both") and tool["category"] in tier["blue_team_focus"]:
            tools[name] = tool

    return tools


def list_tiers():
    result = []
    for num, tier in BUSINESS_TIERS.items():
        result.append({
            "tier": num,
            "name": tier["name"],
            "label": tier["label"],
            "description": tier["description"],
        })
    return result
