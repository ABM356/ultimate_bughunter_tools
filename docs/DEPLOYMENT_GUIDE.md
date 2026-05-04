# HopeUp Security Platform — Deployment & Implementation Guide

## Table of Contents

1. [System Requirements](#1-system-requirements)
2. [Installation](#2-installation)
3. [Platform Overview](#3-platform-overview)
4. [Business Tier Selection](#4-business-tier-selection)
5. [Running Your First Assessment](#5-running-your-first-assessment)
6. [Understanding Reports](#6-understanding-reports)
7. [Client Deployment Guide](#7-client-deployment-guide)
8. [Red Team Operations](#8-red-team-operations)
9. [Blue Team Operations](#9-blue-team-operations)
10. [Compliance & Frameworks](#10-compliance--frameworks)
11. [Training & Certification](#11-training--certification)
12. [Troubleshooting](#12-troubleshooting)

---

## 1. System Requirements

### Minimum Requirements
| Component | Tier 1-2 | Tier 3-4 |
|-----------|----------|----------|
| OS | Ubuntu 22.04+ / Kali Linux | Ubuntu 22.04+ / Kali Linux |
| RAM | 8 GB | 16 GB+ |
| Disk | 50 GB | 100 GB+ |
| CPU | 4 cores | 8+ cores |
| Network | Broadband | Dedicated line |

### Software Prerequisites
- Python 3.10+
- Go 1.21+
- Git 2.30+
- Node.js 18+ (for some tools)
- Ruby 3.0+ (for wpscan)
- Rust/Cargo (for feroxbuster, rustscan, chainsaw)

---

## 2. Installation

### Quick Start (Tier 1)
```bash
# Clone the repository
git clone https://github.com/your-org/HopeUp.git
cd HopeUp

# Make the CLI executable
chmod +x hopeup

# Install Tier 1 tools (Startup/Small Business)
./hopeup install --tier 1

# Verify installation
./hopeup preflight --tier 1
```

### Full Installation (All Tiers)
```bash
# Install all tools for maximum capability
./hopeup install --tier 4

# Install only red team tools
./hopeup install --tier 3 --team red

# Install only blue team tools
./hopeup install --tier 3 --team blue
```

### Verify Installation
```bash
# Check what's installed and what's missing
./hopeup preflight --tier 2

# View the full dashboard
./hopeup dashboard
```

---

## 3. Platform Overview

### Architecture
```
┌─────────────────────────────────────────────────────────┐
│                  HopeUp CLI (hopeup)                        │
├─────────────┬─────────────┬─────────────┬───────────────┤
│  Dashboard  │   Scanner   │   Report    │   Training    │
│             │   Engine    │  Generator  │   Module      │
├─────────────┴─────────────┴─────────────┴───────────────┤
│                   Tier System                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │
│  │ Tier 1   │ │ Tier 2   │ │ Tier 3   │ │  Tier 4   │  │
│  │ Startup  │ │ Mid-size │ │Enterprise│ │ Critical  │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────┘  │
├─────────────────────────────────────────────────────────┤
│                   Tool Registry                         │
│  ┌──────────────────────┐ ┌──────────────────────────┐  │
│  │    RED TEAM (60+)    │ │    BLUE TEAM (25+)       │  │
│  │ Recon, Exploit, Web  │ │ SIEM, IDS, Forensics     │  │
│  └──────────────────────┘ └──────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Commands
| Command | Description |
|---------|-------------|
| `hopeup dashboard` | Show platform overview and status |
| `hopeup tools` | List all security tools with install status |
| `hopeup tiers` | Show business tier details |
| `hopeup scan` | Run a security assessment |
| `hopeup preflight` | Check tool readiness for a tier |
| `hopeup install` | Install tools for a specific tier |
| `hopeup train` | Access training modules |
| `hopeup report` | View or regenerate assessment reports |

---

## 4. Business Tier Selection

### How to Choose the Right Tier

#### Tier 1 — Startup / Small Business
**Choose this if:**
- Company has fewer than 50 employees
- Single web application or website
- No API endpoints or minimal APIs
- No compliance requirements yet
- Budget-conscious, need basic security validation

**What you get:**
- Surface-level scanning (subdomain, DNS, HTTP probing)
- Basic vulnerability scanning (nuclei, nikto)
- Common web attacks (SQLi, XSS)
- SSL/TLS validation
- Host hardening audit
- Secrets detection

---

#### Tier 2 — Mid-size Business
**Choose this if:**
- Company has 50-500 employees
- Multiple web applications and APIs
- Processes payments (PCI-DSS considerations)
- Growing attack surface with cloud services
- Need comprehensive OWASP Top 10 testing

**What you get:**
- Everything in Tier 1, plus:
- Full OWASP Top 10 testing (SSRF, XXE, LFI, CORS, JWT, etc.)
- Port scanning and service enumeration
- OSINT and credential exposure checks
- Subdomain takeover testing
- Cloud bucket enumeration
- IDS configuration and SIEM readiness checks
- Compliance mapping: OWASP Top 10, PCI-DSS Basic

---

#### Tier 3 — Enterprise
**Choose this if:**
- Company has 500-5000 employees
- Complex, multi-region infrastructure
- Cloud-native (AWS, Azure, GCP)
- Regulated industry (finance, healthcare)
- Need deep security assessment with compliance

**What you get:**
- Everything in Tier 2, plus:
- Exploitation framework scans
- Cloud offensive security (AWS, Azure, GCP)
- Mobile application testing
- Container and Kubernetes security
- Advanced forensics and threat intelligence
- Full compliance mapping: SOC2, HIPAA, ISO 27001, PCI-DSS

---

#### Tier 4 — Critical Infrastructure / Government
**Choose this if:**
- Government agency or defense contractor
- Critical infrastructure (energy, telecom, transport)
- 5000+ employees
- Need red team simulation with full attack chains
- Strictest compliance requirements (NIST, FedRAMP, CMMC)

**What you get:**
- ALL tools and capabilities
- Multi-phase red team simulation
- Full blue team defensive audit
- Malware analysis capabilities
- Maximum compliance coverage
- 72-hour assessment window

---

## 5. Running Your First Assessment

### Step 1: Select Your Tier
```bash
./hopeup tiers  # Review all tiers and pick the right one
```

### Step 2: Check Readiness
```bash
./hopeup preflight --tier 2  # Check if tools are installed
```

### Step 3: Run the Assessment
```bash
# Full assessment (red + blue team)
./hopeup scan --target example.com --tier 2

# Red team only
./hopeup scan --target example.com --tier 2 --scope red

# Blue team only
./hopeup scan --target example.com --tier 1 --scope blue

# Quick scan mode
./hopeup scan --target example.com --tier 1 --mode quick

# Specific categories only
./hopeup scan --target example.com --tier 2 --categories "recon_subdomain,vuln_scanning"
```

### Step 4: Review the Report
```bash
./hopeup report  # Shows most recent assessment
./hopeup report --scan-dir ~/hopeup_reports/ASM-20260504-120000/
```

Reports are generated as HTML files in `~/hopeup_reports/`.

---

## 6. Understanding Reports

### Report Sections by Tier

| Section | T1 | T2 | T3 | T4 |
|---------|:--:|:--:|:--:|:--:|
| Executive Summary | ✓ | ✓ | ✓ | ✓ |
| Vulnerability Findings | ✓ | ✓ | ✓ | ✓ |
| Risk Ratings | ✓ | ✓ | ✓ | ✓ |
| Attack Surface Map | | ✓ | ✓ | ✓ |
| Attack Chain Analysis | | | ✓ | ✓ |
| Red Team Narrative | | | | ✓ |
| Remediation Steps | ✓ | ✓ | ✓ | ✓ |
| Compliance Checklist | | ✓ | ✓ | ✓ |
| Threat Modeling | | | ✓ | ✓ |
| Zero-Day Assessment | | | | ✓ |
| Supply Chain Analysis | | | | ✓ |
| Blue Team Recommendations | | | ✓ | ✓ |
| IR Readiness | | | | ✓ |
| Security Architecture Review | | | | ✓ |

### Severity Ratings
- **CRITICAL** — Immediate exploitation possible, full system compromise
- **HIGH** — Significant impact, exploitation likely
- **MEDIUM** — Moderate impact, exploitation requires specific conditions
- **LOW** — Minor impact, limited exploitation potential
- **INFO** — Informational finding, no direct security impact

---

## 7. Client Deployment Guide

### Pre-Engagement Checklist
1. **Determine Client Tier** — Use the tier selection guide above
2. **Define Scope** — Document target domains, IPs, applications, and exclusions
3. **Get Authorization** — Obtain written permission (rules of engagement)
4. **Set Timeline** — Align assessment duration with tier profile
5. **Communication Plan** — Establish reporting channels for critical findings

### Running a Client Assessment
```bash
# 1. Install tools for client's tier
./hopeup install --tier 3

# 2. Verify readiness
./hopeup preflight --tier 3

# 3. Run the assessment
./hopeup scan --target client-domain.com --tier 3 --scope red+blue

# 4. Generate report
./hopeup report
```

### Delivering Results
1. Share the HTML report with the client
2. Schedule a findings walkthrough meeting
3. Prioritize remediation by severity (Critical → High → Medium)
4. Agree on retesting timeline
5. Schedule follow-up assessment

---

## 8. Red Team Operations

### Methodology (follows PTES — Penetration Testing Execution Standard)

1. **Pre-engagement** — Scoping, authorization, rules of engagement
2. **Intelligence Gathering** — Passive and active reconnaissance
3. **Threat Modeling** — Identify likely attack vectors
4. **Vulnerability Analysis** — Systematic vulnerability discovery
5. **Exploitation** — Controlled exploitation of confirmed vulnerabilities
6. **Post-Exploitation** — Impact assessment and lateral movement checks
7. **Reporting** — Detailed findings with evidence and remediation

### Key Red Team Tools by Phase
| Phase | Tools |
|-------|-------|
| Recon | subfinder, amass, httpx, naabu, katana, gau |
| Vuln Scan | nuclei, nikto, wpscan, trivy |
| Web Attack | sqlmap, xsstrike, dalfox, commix, jwt_tool |
| Brute Force | ffuf, gobuster, hydra |
| Exploitation | searchsploit, sn1per |
| Cloud | cloudfox, pacu, scoutsuite |

---

## 9. Blue Team Operations

### Defensive Security Stack

1. **Host Hardening** — lynis, openscap
2. **Secrets Detection** — gitleaks, detect-secrets, trufflehog
3. **Network Monitoring** — suricata, zeek, ntopng
4. **SIEM & Log Analysis** — wazuh, ossec
5. **Threat Intelligence** — yara, sigma
6. **Incident Response** — volatility3, chainsaw
7. **Cloud Security** — prowler, cloudsplaining
8. **Container Security** — falco, trivy, grype
9. **WAF** — modsecurity

### Blue Team Deployment Order
```bash
# Phase 1: Baseline (Day 1)
./hopeup install --tier 1 --team blue  # lynis, gitleaks, detect-secrets

# Phase 2: Monitoring (Week 1)
./hopeup install --tier 2 --team blue  # Add suricata, wazuh, ossec

# Phase 3: Advanced (Month 1)
./hopeup install --tier 3 --team blue  # Add forensics, threat intel, cloud defense

# Phase 4: Full Capability
./hopeup install --tier 4 --team blue  # Add malware analysis, full stack
```

---

## 10. Compliance & Frameworks

### Supported Compliance Mappings

| Framework | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|-----------|:------:|:------:|:------:|:------:|
| OWASP Top 10 | | ✓ | ✓ | ✓ |
| PCI-DSS | | Basic | Full | Full |
| SOC 2 | | | ✓ | ✓ |
| HIPAA | | | ✓ | ✓ |
| ISO 27001 | | | ✓ | ✓ |
| NIST 800-53 | | | | ✓ |
| NIST CSF | | | | ✓ |
| FedRAMP | | | | ✓ |
| CMMC | | | | ✓ |

---

## 11. Training & Certification

### Learning Paths

#### Path 1: Offensive Security (Red Team)
```
BH-101 → BH-102 → BH-201 → BH-202 → BH-301 → BH-302
  4h       6h       10h       6h       12h       10h    = 48 hours
```

#### Path 2: Defensive Security (Blue Team)
```
BD-101 → BD-201 → BD-301
  4h       8h       10h    = 22 hours
```

#### Path 3: Platform Deployment
```
DP-101
  3h    = 3 hours
```

### Access Training
```bash
./hopeup train                          # List all modules
./hopeup train --module BH-101          # Start a specific module
```

---

## 12. Troubleshooting

### Common Issues

**Tools not installing:**
```bash
# Check if Go is installed
go version

# Check if pip is available
pip3 --version

# Install missing system dependencies
sudo apt-get update && sudo apt-get install -y build-essential git python3-pip golang-go
```

**Permission denied errors:**
```bash
# Some tools need sudo for installation
sudo ./hopeup install --tier 2

# Scanner doesn't need sudo (runs tools in user space)
./hopeup scan --target example.com --tier 1
```

**Tools timeout during scan:**
```bash
# Use quick mode for faster scans
./hopeup scan --target example.com --tier 1 --mode quick

# Run specific categories only
./hopeup scan --target example.com --tier 2 --categories "recon_subdomain,vuln_scanning"
```

**Report not generating:**
```bash
# Check if output directory exists
ls ~/hopeup_reports/

# Regenerate report from existing scan
./hopeup report --scan-dir ~/hopeup_reports/ASM-20260504-120000/
```

---

## Quick Reference Card

```
┌──────────────────────────────────────────────────────┐
│           HOPEUP SECURITY PLATFORM v2.0           │
├──────────────────────────────────────────────────────┤
│                                                      │
│  INSTALL:  ./hopeup install --tier [1-4]               │
│  CHECK:    ./hopeup preflight --tier [1-4]             │
│  SCAN:     ./hopeup scan -t <target> --tier [1-4]      │
│  REPORT:   ./hopeup report                             │
│  TRAIN:    ./hopeup train                              │
│  TOOLS:    ./hopeup tools [--team red|blue]            │
│  TIERS:    ./hopeup tiers                              │
│                                                      │
│  TIERS:                                              │
│   1 = Startup    │ 2 = Mid-size                      │
│   3 = Enterprise │ 4 = Critical/Gov                  │
│                                                      │
│  SCOPES:  --scope red | blue | red+blue              │
│  MODES:   --mode quick | full | deep                 │
│                                                      │
└──────────────────────────────────────────────────────┘
```
