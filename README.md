# HopeUp Security Platform

> A complete cybersecurity operating platform with offensive and defensive capabilities, AI-powered analysis, role-based reports, client management, and integrated payments.

**HopeUp** is a tiered cybersecurity service platform that lets you run security assessments for businesses of any size — from startups to critical infrastructure — and deliver professional reports tailored to every stakeholder.

---

## Features

- **85+ Security Tools** — 60+ Red Team (offensive) + 25+ Blue Team (defensive)
- **4 Business Tiers** — Startup, Mid-size, Enterprise, Critical Infrastructure
- **CLI + Web Dashboard** — Run assessments from terminal or browser
- **AI-Powered Analysis** — Claude API integration for intelligent insights
- **Role-Based Reports** — 8 different report views (CISO, CTO, Manager, Engineer, Board, etc.)
- **Client & Invoice Management** — Track clients, generate invoices
- **Payment Integration** — Stripe and PayPal ready
- **Training Academy** — 10 modules covering Red Team, Blue Team, and Deployment
- **Compliance Mapping** — OWASP, PCI-DSS, SOC2, HIPAA, ISO 27001, NIST, FedRAMP, CMMC

---

## Quick Start

### Install Dependencies
```bash
pip3 install -r requirements.txt
```

### CLI
```bash
# Show dashboard
./hopeup dashboard

# Install tools for Tier 2 (Mid-size Business)
./hopeup install --tier 2

# Run a security assessment
./hopeup scan --target example.com --tier 2 --scope red+blue

# View tools
./hopeup tools --team red --tier 3

# View training modules
./hopeup train
```

### Web Dashboard
```bash
python3 webapp/app.py
# Open http://localhost:5000
```

---

## Business Tiers

| Tier | Name | Audience | Tools | Compliance |
|------|------|----------|-------|------------|
| **1** | Startup / Small Business | < 50 employees, single web app | Subset | — |
| **2** | Mid-size Business | 50-500 employees, APIs, SaaS | Most | OWASP, PCI-DSS Basic |
| **3** | Enterprise | 500-5000 employees, multi-cloud | Most + Cloud | SOC2, HIPAA, ISO 27001 |
| **4** | Critical Infrastructure | Government, defense, banks | All | NIST, FedRAMP, CMMC |

---

## Architecture

```
HopeUp Platform/
├── hopeup                   # CLI entry point
├── platform/                # Core engine
│   ├── tools_registry.py    # 85+ tool definitions
│   ├── tiers.py             # Business tier system
│   ├── scanner.py           # Assessment orchestrator
│   ├── report_generator.py  # HTML report generation
│   └── cli.py               # Command-line interface
├── webapp/                  # Web dashboard (Flask)
│   ├── app.py               # Main application
│   ├── ai_engine.py         # Claude API integration
│   ├── role_reports.py      # Multi-audience reports
│   └── templates/           # HTML templates
├── configs/                 # Tier YAML configurations
│   ├── tier1_startup.yaml
│   ├── tier2_midsize.yaml
│   ├── tier3_enterprise.yaml
│   └── tier4_critical.yaml
├── training/                # Training curriculum
│   └── curriculum.py        # 10 modules (Red, Blue, Deployment)
└── docs/
    └── DEPLOYMENT_GUIDE.md  # Full deployment documentation
```

---

## Configuration

Set environment variables to enable AI and payment features:

```bash
# AI Integration (Claude)
export ANTHROPIC_API_KEY=sk-ant-...

# Payment Integration
export STRIPE_SECRET_KEY=sk_live_...
export STRIPE_PUBLISHABLE_KEY=pk_live_...
export PAYPAL_CLIENT_ID=...
export PAYPAL_SECRET=...

# Web App
export HOPEUP_PORT=5000
export HOPEUP_SECRET_KEY=<random-secret>
```

---

## Role-Based Reports

Generate different reports for different audiences from the same assessment:

| Role | Focus |
|------|-------|
| CISO | Business risk, compliance posture, strategic recommendations |
| CTO | Technical architecture, engineering effort, technology stack |
| Manager | High-level summary, timelines, budget, action items |
| Security Engineer | Full technical details, CVEs, tool outputs, code-level fixes |
| Software Engineer | Code vulnerabilities, secure coding, dependency issues |
| Network Engineer | Network findings, firewall rules, IDS/IPS, port exposure |
| Board of Directors | One-page summary, financial exposure, liability |
| Compliance Officer | Regulatory compliance, audit readiness, legal exposure |

---

## Documentation

See [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) for the complete deployment and implementation guide — installation, tier selection, client engagement workflow, and operations.

---

## License

See [LICENSE](LICENSE) for details.
