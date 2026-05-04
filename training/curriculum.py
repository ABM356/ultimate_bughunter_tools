"""
Training curriculum — structured learning paths for bug bounty hunting,
defensive security, and platform deployment.
"""

CURRICULUM = {
    # ─── OFFENSIVE / RED TEAM TRACK ───
    "BH-101": {
        "title": "Bug Bounty Fundamentals",
        "level": "beginner",
        "track": "red",
        "duration_hours": 4,
        "prerequisites": [],
        "description": "Learn the basics of bug bounty hunting, responsible disclosure, and setting up your testing environment.",
        "modules": [
            {
                "title": "Introduction to Bug Bounty Hunting",
                "topics": [
                    "What is bug bounty hunting?",
                    "How bug bounty programs work (HackerOne, Bugcrowd, Intigriti)",
                    "Responsible disclosure vs. full disclosure",
                    "Legal considerations and scope boundaries",
                    "Setting up your testing environment",
                ],
                "lab": {
                    "name": "lab_setup_environment",
                    "description": "Install the platform, configure Tier 1 tools, and verify your setup",
                    "steps": [
                        "Clone the Ultimate BugHunter Platform repository",
                        "Run: ubht install --tier 1",
                        "Run: ubht preflight --tier 1",
                        "Verify all Tier 1 tools show as installed",
                        "Run: ubht dashboard — familiarize yourself with the interface",
                    ],
                },
            },
            {
                "title": "Understanding Web Applications",
                "topics": [
                    "HTTP protocol fundamentals (methods, headers, status codes)",
                    "Client-server architecture",
                    "Cookies, sessions, and authentication mechanisms",
                    "Same-origin policy and CORS",
                    "Common web technologies (REST, GraphQL, WebSockets)",
                ],
                "lab": {
                    "name": "lab_http_basics",
                    "description": "Use curl and httpx to understand HTTP fundamentals",
                    "steps": [
                        "Use curl to send GET/POST requests to a test target",
                        "Inspect HTTP headers and response codes",
                        "Use httpx to probe multiple URLs",
                        "Identify technologies using response headers",
                    ],
                },
            },
            {
                "title": "Your First Bug Bounty Report",
                "topics": [
                    "Choosing your first program",
                    "Understanding program scope and rules",
                    "Writing a clear vulnerability report",
                    "Severity ratings (CVSS basics)",
                    "What makes a good vs. bad report",
                ],
                "lab": {
                    "name": "lab_first_report",
                    "description": "Write a sample bug report for a practice vulnerability",
                    "steps": [
                        "Find a test vulnerability on a practice platform",
                        "Document: title, description, steps to reproduce",
                        "Assign severity using CVSS calculator",
                        "Write remediation recommendations",
                        "Review your report against program guidelines",
                    ],
                },
            },
        ],
    },

    "BH-102": {
        "title": "Reconnaissance Mastery",
        "level": "beginner",
        "track": "red",
        "duration_hours": 6,
        "prerequisites": ["BH-101"],
        "description": "Master the art of reconnaissance — subdomain enumeration, DNS analysis, port scanning, and OSINT.",
        "modules": [
            {
                "title": "Subdomain Enumeration",
                "topics": [
                    "Why subdomains matter in bug bounty",
                    "Passive vs. active enumeration",
                    "Certificate transparency logs",
                    "Using subfinder, amass, assetfinder",
                    "Combining tools for maximum coverage",
                ],
                "lab": {
                    "name": "lab_subdomain_enum",
                    "description": "Enumerate subdomains of a test target using multiple tools",
                    "steps": [
                        "Run subfinder against a test domain",
                        "Run amass in passive mode",
                        "Run assetfinder",
                        "Merge and deduplicate results",
                        "Probe live subdomains with httpx",
                    ],
                },
            },
            {
                "title": "DNS & Network Reconnaissance",
                "topics": [
                    "DNS record types (A, AAAA, CNAME, MX, TXT, NS)",
                    "Zone transfers and misconfigurations",
                    "Port scanning strategies",
                    "Service identification and fingerprinting",
                    "Using dnsx, massdns, naabu",
                ],
                "lab": {
                    "name": "lab_dns_recon",
                    "description": "Perform DNS and port reconnaissance",
                    "steps": [
                        "Use dnsx to resolve discovered subdomains",
                        "Check for zone transfer vulnerabilities",
                        "Run naabu for port discovery",
                        "Identify services on open ports",
                    ],
                },
            },
            {
                "title": "OSINT & Intelligence Gathering",
                "topics": [
                    "Open-source intelligence methodology",
                    "Google dorking for sensitive files",
                    "GitHub/GitLab secret discovery",
                    "Wayback Machine for historical data",
                    "Using theHarvester, gau, waybackurls",
                ],
                "lab": {
                    "name": "lab_osint",
                    "description": "Gather intelligence from public sources",
                    "steps": [
                        "Run theHarvester for email and subdomain discovery",
                        "Use gau and waybackurls to find historical URLs",
                        "Search for exposed credentials with trufflehog",
                        "Use Google dorks to find sensitive files",
                    ],
                },
            },
        ],
    },

    "BH-201": {
        "title": "Web Application Hacking",
        "level": "intermediate",
        "track": "red",
        "duration_hours": 10,
        "prerequisites": ["BH-102"],
        "description": "Deep-dive into OWASP Top 10 vulnerabilities with hands-on exploitation.",
        "modules": [
            {
                "title": "SQL Injection",
                "topics": [
                    "How SQL injection works",
                    "Types: union-based, blind, time-based, error-based",
                    "Using sqlmap for automated detection",
                    "Manual testing techniques",
                    "Post-exploitation: data extraction, file read/write",
                ],
                "lab": {
                    "name": "lab_sqli",
                    "description": "Find and exploit SQL injection vulnerabilities",
                    "steps": [
                        "Identify injection points in a test application",
                        "Test for error-based SQLi manually",
                        "Use sqlmap with --forms flag",
                        "Extract database schema and data",
                        "Write a report with remediation advice",
                    ],
                },
            },
            {
                "title": "Cross-Site Scripting (XSS)",
                "topics": [
                    "Reflected, stored, and DOM-based XSS",
                    "Context-dependent payloads",
                    "Bypassing WAF and filters",
                    "Using XSStrike and Dalfox",
                    "Impact demonstration (cookie theft, keylogging)",
                ],
                "lab": {
                    "name": "lab_xss",
                    "description": "Discover and exploit XSS vulnerabilities",
                    "steps": [
                        "Identify reflection points in a test application",
                        "Test with basic payloads and observe filtering",
                        "Use XSStrike for automated scanning",
                        "Craft a payload that bypasses input validation",
                        "Demonstrate impact with a proof-of-concept",
                    ],
                },
            },
            {
                "title": "SSRF, XXE, LFI, and More",
                "topics": [
                    "Server-Side Request Forgery (SSRF)",
                    "XML External Entity (XXE) injection",
                    "Local/Remote File Inclusion",
                    "CORS misconfigurations",
                    "JWT vulnerabilities",
                    "IDOR and access control flaws",
                ],
                "lab": {
                    "name": "lab_advanced_web",
                    "description": "Test for advanced web vulnerabilities",
                    "steps": [
                        "Test for SSRF in URL parameters and file uploads",
                        "Craft XXE payloads for XML endpoints",
                        "Test for LFI using path traversal",
                        "Check CORS headers with CORStest",
                        "Analyze and attack JWT tokens with jwt_tool",
                    ],
                },
            },
        ],
    },

    "BH-202": {
        "title": "API & Authentication Testing",
        "level": "intermediate",
        "track": "red",
        "duration_hours": 6,
        "prerequisites": ["BH-201"],
        "description": "Test REST and GraphQL APIs, break authentication, and find business logic flaws.",
        "modules": [
            {
                "title": "API Security Testing",
                "topics": [
                    "REST API enumeration and testing",
                    "GraphQL introspection and injection",
                    "Parameter tampering and IDOR",
                    "Rate limiting and abuse prevention testing",
                    "API documentation discovery (Swagger, OpenAPI)",
                ],
                "lab": {
                    "name": "lab_api_testing",
                    "description": "Find vulnerabilities in a test API",
                    "steps": [
                        "Discover API endpoints using katana and Swagger",
                        "Test for IDOR by modifying resource IDs",
                        "Use arjun for hidden parameter discovery",
                        "Test rate limiting on sensitive endpoints",
                        "Check for mass assignment vulnerabilities",
                    ],
                },
            },
            {
                "title": "Authentication & Session Attacks",
                "topics": [
                    "Brute-force and credential stuffing",
                    "OAuth 2.0 and OpenID Connect flaws",
                    "Session fixation and hijacking",
                    "Password reset vulnerabilities",
                    "Multi-factor authentication bypasses",
                ],
                "lab": {
                    "name": "lab_auth_testing",
                    "description": "Test authentication mechanisms for flaws",
                    "steps": [
                        "Test login for brute-force with hydra",
                        "Check for default credentials with changeme",
                        "Analyze session tokens for predictability",
                        "Test password reset flow for vulnerabilities",
                        "Attempt JWT manipulation with jwt_tool",
                    ],
                },
            },
        ],
    },

    "BH-301": {
        "title": "Advanced Exploitation",
        "level": "advanced",
        "track": "red",
        "duration_hours": 12,
        "prerequisites": ["BH-202"],
        "description": "Advanced attack techniques including deserialization, prototype pollution, and race conditions.",
        "modules": [
            {
                "title": "Deserialization Attacks",
                "topics": [
                    "Java deserialization with ysoserial",
                    "PHP object injection with phpggc",
                    "Python pickle exploitation",
                    ".NET deserialization chains",
                    "Identifying deserialization points",
                ],
                "lab": {
                    "name": "lab_deserialization",
                    "description": "Exploit deserialization vulnerabilities",
                    "steps": [
                        "Generate Java payloads with ysoserial",
                        "Generate PHP gadget chains with phpggc",
                        "Test a vulnerable application with crafted payloads",
                        "Achieve remote code execution",
                        "Document the attack chain for the report",
                    ],
                },
            },
            {
                "title": "Race Conditions & Business Logic",
                "topics": [
                    "Time-of-check to time-of-use (TOCTOU) bugs",
                    "Using race-the-web for automated testing",
                    "Payment and transaction manipulation",
                    "Coupon and discount abuse",
                    "Account takeover via logic flaws",
                ],
                "lab": {
                    "name": "lab_race_conditions",
                    "description": "Find and exploit race condition vulnerabilities",
                    "steps": [
                        "Use race-the-web to send concurrent requests",
                        "Test for double-spending in a test payment flow",
                        "Exploit a TOCTOU vulnerability",
                        "Document the business impact",
                    ],
                },
            },
        ],
    },

    "BH-302": {
        "title": "Cloud & Infrastructure Security",
        "level": "advanced",
        "track": "red",
        "duration_hours": 10,
        "prerequisites": ["BH-301"],
        "description": "Cloud security testing for AWS, Azure, and GCP — plus container and Kubernetes attacks.",
        "modules": [
            {
                "title": "AWS Security Testing",
                "topics": [
                    "S3 bucket misconfigurations",
                    "IAM privilege escalation",
                    "Lambda and serverless attacks",
                    "Using pacu and cloudfox",
                    "AWS-specific bug bounty techniques",
                ],
                "lab": {
                    "name": "lab_aws_security",
                    "description": "Test AWS infrastructure for misconfigurations",
                    "steps": [
                        "Use lazys3 to find open S3 buckets",
                        "Enumerate AWS services with cloudfox",
                        "Run ScoutSuite for cloud security audit",
                        "Test IAM policies with pacu",
                        "Check for metadata service exposure (SSRF to 169.254.169.254)",
                    ],
                },
            },
            {
                "title": "Container & Kubernetes Security",
                "topics": [
                    "Docker security misconfigurations",
                    "Container escape techniques",
                    "Kubernetes RBAC and secrets",
                    "Using trivy for container scanning",
                    "Service mesh and network policy testing",
                ],
                "lab": {
                    "name": "lab_container_security",
                    "description": "Assess container and Kubernetes security",
                    "steps": [
                        "Scan container images with trivy",
                        "Check for privileged containers",
                        "Test Kubernetes API access",
                        "Enumerate secrets and ConfigMaps",
                        "Test network policies between pods",
                    ],
                },
            },
        ],
    },

    # ─── DEFENSIVE / BLUE TEAM TRACK ───
    "BD-101": {
        "title": "Blue Team Essentials",
        "level": "beginner",
        "track": "blue",
        "duration_hours": 4,
        "prerequisites": [],
        "description": "Introduction to defensive security, monitoring, and incident detection.",
        "modules": [
            {
                "title": "Defensive Security Foundations",
                "topics": [
                    "Defense-in-depth strategy",
                    "The security operations center (SOC)",
                    "Log sources and their importance",
                    "Common attack patterns to detect",
                    "Introduction to the MITRE ATT&CK framework",
                ],
                "lab": {
                    "name": "lab_blue_setup",
                    "description": "Set up basic defensive monitoring",
                    "steps": [
                        "Install blue team tools: ubht install --tier 1 --team blue",
                        "Run lynis for a baseline system audit",
                        "Review lynis output and understand findings",
                        "Set up gitleaks pre-commit hook",
                        "Configure detect-secrets baseline",
                    ],
                },
            },
            {
                "title": "System Hardening",
                "topics": [
                    "Linux system hardening basics",
                    "Network security configuration",
                    "Service minimization",
                    "File system permissions and integrity",
                    "Using lynis for automated auditing",
                ],
                "lab": {
                    "name": "lab_hardening",
                    "description": "Harden a Linux system based on audit findings",
                    "steps": [
                        "Run lynis audit system",
                        "Address critical findings from the report",
                        "Disable unnecessary services",
                        "Configure firewall rules",
                        "Re-run lynis and compare scores",
                    ],
                },
            },
        ],
    },

    "BD-201": {
        "title": "SIEM & Threat Hunting",
        "level": "intermediate",
        "track": "blue",
        "duration_hours": 8,
        "prerequisites": ["BD-101"],
        "description": "Deploy SIEM, write detection rules, and hunt for threats.",
        "modules": [
            {
                "title": "SIEM Deployment & Configuration",
                "topics": [
                    "SIEM architecture and data flow",
                    "Deploying Wazuh for host monitoring",
                    "Log collection and normalization",
                    "Alert rules and thresholds",
                    "Dashboard creation and visualization",
                ],
                "lab": {
                    "name": "lab_siem_setup",
                    "description": "Deploy and configure a SIEM system",
                    "steps": [
                        "Install Wazuh manager and agent",
                        "Configure log collection from key sources",
                        "Create custom alert rules",
                        "Build a monitoring dashboard",
                        "Generate test alerts and verify detection",
                    ],
                },
            },
            {
                "title": "Threat Hunting with Sigma & YARA",
                "topics": [
                    "Threat hunting methodology",
                    "Writing Sigma detection rules",
                    "Creating YARA rules for malware detection",
                    "Hunting for indicators of compromise (IOCs)",
                    "Using Suricata for network-based detection",
                ],
                "lab": {
                    "name": "lab_threat_hunting",
                    "description": "Write detection rules and hunt for threats",
                    "steps": [
                        "Write a Sigma rule for detecting brute-force attempts",
                        "Write a YARA rule for a known malware sample",
                        "Deploy rules to your SIEM",
                        "Run a simulated attack and verify detection",
                        "Create a threat hunting report",
                    ],
                },
            },
        ],
    },

    "BD-301": {
        "title": "Incident Response & Forensics",
        "level": "advanced",
        "track": "blue",
        "duration_hours": 10,
        "prerequisites": ["BD-201"],
        "description": "Memory forensics, disk analysis, malware triage, and IR playbooks.",
        "modules": [
            {
                "title": "Memory & Disk Forensics",
                "topics": [
                    "Memory acquisition techniques",
                    "Volatility3 for memory analysis",
                    "Disk forensics with Autopsy",
                    "Windows event log analysis with Chainsaw",
                    "Evidence preservation and chain of custody",
                ],
                "lab": {
                    "name": "lab_forensics",
                    "description": "Perform forensic analysis on a compromised system",
                    "steps": [
                        "Acquire a memory dump from a test system",
                        "Analyze processes and network connections with volatility3",
                        "Hunt for malicious artifacts in memory",
                        "Analyze Windows event logs with chainsaw",
                        "Create a forensic timeline of events",
                    ],
                },
            },
            {
                "title": "Incident Response Procedures",
                "topics": [
                    "IR lifecycle (NIST SP 800-61)",
                    "Containment, eradication, and recovery",
                    "Communication and escalation procedures",
                    "Post-incident review and lessons learned",
                    "Building IR playbooks",
                ],
                "lab": {
                    "name": "lab_incident_response",
                    "description": "Execute an incident response scenario",
                    "steps": [
                        "Receive a simulated security alert",
                        "Triage and classify the incident",
                        "Contain the threat and preserve evidence",
                        "Perform root cause analysis",
                        "Write a post-incident report with recommendations",
                    ],
                },
            },
        ],
    },

    # ─── DEPLOYMENT TRACK ───
    "DP-101": {
        "title": "Platform Deployment Guide",
        "level": "beginner",
        "track": "deployment",
        "duration_hours": 3,
        "prerequisites": [],
        "description": "How to install, configure, and deploy this platform for your business or clients.",
        "modules": [
            {
                "title": "Installation & Setup",
                "topics": [
                    "System requirements (OS, RAM, disk, dependencies)",
                    "Installing the platform and all tools",
                    "Tier selection for your business type",
                    "Configuring scan profiles",
                    "Verifying installation with preflight checks",
                ],
                "lab": {
                    "name": "lab_deployment",
                    "description": "Deploy the platform on a fresh system",
                    "steps": [
                        "Clone the repository on a clean Linux system",
                        "Run the full installer for your selected tier",
                        "Verify with ubht preflight",
                        "Run a test scan against a practice target",
                        "Generate and review the assessment report",
                    ],
                },
            },
            {
                "title": "Client Deployment & Operations",
                "topics": [
                    "Assessing client business tier",
                    "Scoping and rules of engagement",
                    "Running assessments for clients",
                    "Interpreting and presenting reports",
                    "Ongoing monitoring and retesting schedules",
                ],
                "lab": {
                    "name": "lab_client_deployment",
                    "description": "Simulate a client engagement from start to finish",
                    "steps": [
                        "Determine client tier based on their business profile",
                        "Create a scope document and rules of engagement",
                        "Run a full assessment at the appropriate tier",
                        "Generate the report and review findings",
                        "Prepare a client presentation with remediation priorities",
                    ],
                },
            },
        ],
    },
}


def get_module(code):
    return CURRICULUM.get(code)


def list_modules(track=None, level=None):
    result = []
    for code, module in CURRICULUM.items():
        if track and module["track"] != track:
            continue
        if level and module["level"] != level:
            continue
        result.append({
            "code": code,
            "title": module["title"],
            "level": module["level"],
            "track": module["track"],
            "duration_hours": module["duration_hours"],
            "prerequisites": module["prerequisites"],
        })
    return result


def get_learning_path(track):
    modules = list_modules(track=track)
    return sorted(modules, key=lambda m: (
        {"beginner": 0, "intermediate": 1, "advanced": 2}[m["level"]],
        m["code"]
    ))
