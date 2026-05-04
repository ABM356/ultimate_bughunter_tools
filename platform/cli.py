#!/usr/bin/env python3
"""
HopeUp Security Platform — Main CLI Interface
Unified command-line interface for offensive and defensive security operations.
"""

import argparse
import sys
import os
import json
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from platform.tools_registry import TOOL_REGISTRY, CATEGORIES, get_tools_by_team, get_tools_by_tier, get_tool_count
from platform.tiers import BUSINESS_TIERS, list_tiers, get_tier, get_tier_tools
from platform.scanner import Assessment, INSTALL_DIR, OUTPUT_DIR
from platform.report_generator import generate_report


# ─── Colors ───
class C:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


BANNER = f"""
{C.CYAN}{C.BOLD}
    ██╗  ██╗ ██████╗ ██████╗ ███████╗██╗   ██╗██████╗
    ██║  ██║██╔═══██╗██╔══██╗██╔════╝██║   ██║██╔══██╗
    ███████║██║   ██║██████╔╝█████╗  ██║   ██║██████╔╝
    ██╔══██║██║   ██║██╔═══╝ ██╔══╝  ██║   ██║██╔═══╝
    ██║  ██║╚██████╔╝██║     ███████╗╚██████╔╝██║
    ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝

    ███████╗███████╗ ██████╗██╗   ██╗██████╗ ██╗████████╗██╗   ██╗
    ██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██║╚══██╔══╝╚██╗ ██╔╝
    ███████╗█████╗  ██║     ██║   ██║██████╔╝██║   ██║    ╚████╔╝
    ╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██║   ██║     ╚██╔╝
    ███████║███████╗╚██████╗╚██████╔╝██║  ██║██║   ██║      ██║
    ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝
{C.RESET}
{C.DIM}    ──────────────────────────────────────────────────────────────────{C.RESET}
{C.WHITE}        HopeUp Security Platform v2.0 — Offensive & Defensive Ops{C.RESET}
{C.DIM}    ──────────────────────────────────────────────────────────────────{C.RESET}
"""


def cmd_dashboard(args):
    print(BANNER)
    counts = get_tool_count()
    print(f"  {C.BOLD}Platform Status{C.RESET}")
    print(f"  ├── Total Tools:    {C.CYAN}{counts['total']}{C.RESET}")
    print(f"  ├── {C.RED}Red Team:{C.RESET}      {counts['red_team']} offensive tools")
    print(f"  ├── {C.BLUE}Blue Team:{C.RESET}     {counts['blue_team']} defensive tools")
    print(f"  └── {C.MAGENTA}Shared:{C.RESET}        {counts['shared']} dual-use tools")
    print()

    print(f"  {C.BOLD}Business Tiers{C.RESET}")
    for t in list_tiers():
        tools = get_tier_tools(t["tier"], TOOL_REGISTRY)
        print(f"  ├── {C.YELLOW}Tier {t['tier']}{C.RESET} — {t['name']} ({len(tools)} tools)")
    print()

    print(f"  {C.BOLD}Quick Commands{C.RESET}")
    print(f"  ├── {C.GREEN}hopeup scan{C.RESET}       — Run a security assessment")
    print(f"  ├── {C.GREEN}hopeup tools{C.RESET}      — List all tools")
    print(f"  ├── {C.GREEN}hopeup tiers{C.RESET}      — Show business tier details")
    print(f"  ├── {C.GREEN}hopeup install{C.RESET}    — Install tools for a tier")
    print(f"  ├── {C.GREEN}hopeup preflight{C.RESET}  — Check tool readiness")
    print(f"  ├── {C.GREEN}hopeup train{C.RESET}      — Launch training modules")
    print(f"  └── {C.GREEN}hopeup report{C.RESET}     — Generate report from last scan")
    print()


def cmd_tools(args):
    team_filter = getattr(args, "team", None)
    tier_filter = getattr(args, "tier", None)
    category_filter = getattr(args, "category", None)

    tools = TOOL_REGISTRY
    if team_filter:
        tools = {k: v for k, v in tools.items() if v["team"] in (team_filter, "both")}
    if tier_filter:
        tools = {k: v for k, v in tools.items() if v["tier"] <= tier_filter}
    if category_filter:
        tools = {k: v for k, v in tools.items() if v["category"] == category_filter}

    print(f"\n  {C.BOLD}Tools Registry{C.RESET} ({len(tools)} tools)\n")

    by_category = {}
    for name, tool in sorted(tools.items()):
        cat = tool["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append((name, tool))

    all_cats = {**CATEGORIES.get("red", {}), **CATEGORIES.get("blue", {}), **CATEGORIES.get("shared", {})}

    for cat, cat_tools in sorted(by_category.items()):
        cat_display = all_cats.get(cat, cat)
        print(f"  {C.CYAN}{C.BOLD}{cat_display}{C.RESET}")
        for name, tool in cat_tools:
            team_color = C.RED if tool["team"] == "red" else C.BLUE if tool["team"] == "blue" else C.MAGENTA
            installed = "+" if shutil.which(name) or os.path.isdir(os.path.join(INSTALL_DIR, name)) else "-"
            installed_color = C.GREEN if installed == "+" else C.DIM
            print(f"    {installed_color}[{installed}]{C.RESET} {team_color}{'RED' if tool['team']=='red' else 'BLU' if tool['team']=='blue' else 'R+B'}{C.RESET} T{tool['tier']}  {C.WHITE}{name:25s}{C.RESET} {C.DIM}{tool['description'][:55]}{C.RESET}")
        print()


def cmd_tiers(args):
    print(f"\n  {C.BOLD}Business Tier System{C.RESET}\n")

    for num, tier in BUSINESS_TIERS.items():
        tools = get_tier_tools(num, TOOL_REGISTRY)
        red_tools = {k: v for k, v in tools.items() if v["team"] in ("red", "both")}
        blue_tools = {k: v for k, v in tools.items() if v["team"] in ("blue", "both")}

        print(f"  {C.YELLOW}{C.BOLD}{'━'*60}{C.RESET}")
        print(f"  {C.YELLOW}{C.BOLD}TIER {num}: {tier['name'].upper()}{C.RESET}")
        print(f"  {C.YELLOW}{C.BOLD}{'━'*60}{C.RESET}")
        print(f"  {C.DIM}Label:{C.RESET} {tier['label']}")
        print(f"  {C.DIM}Description:{C.RESET} {tier['description']}")
        print()
        print(f"  {C.DIM}Target Audience:{C.RESET}")
        for audience in tier["target_audience"]:
            print(f"    • {audience}")
        print()
        print(f"  {C.DIM}Scan Profile:{C.RESET}")
        sp = tier["scan_profile"]
        print(f"    • Depth: {sp['depth']} | Max Duration: {sp['max_duration_hours']}h | Concurrency: {sp['concurrent_tools']} | Rate: {sp['rate_limit']}")
        print()
        print(f"  {C.RED}Red Team Tools:{C.RESET} {len(red_tools)}")
        print(f"  {C.BLUE}Blue Team Tools:{C.RESET} {len(blue_tools)}")
        print(f"  {C.WHITE}Total Tools:{C.RESET} {len(tools)}")
        print()
        if tier["compliance"]:
            print(f"  {C.DIM}Compliance:{C.RESET} {', '.join(c.replace('_', ' ') for c in tier['compliance'])}")
        print()


def cmd_scan(args):
    target = args.target
    tier = args.tier
    scope = args.scope or "red+blue"
    mode = args.mode or "full"

    if not target:
        print(f"  {C.RED}Error: --target is required{C.RESET}")
        sys.exit(1)

    print(BANNER)
    print(f"  {C.BOLD}Initializing Assessment{C.RESET}")
    print(f"  Target: {C.CYAN}{target}{C.RESET}")
    print(f"  Tier:   {C.YELLOW}{tier}{C.RESET} — {BUSINESS_TIERS[tier]['name']}")
    print(f"  Scope:  {scope.upper()}")
    print()

    assessment = Assessment(target, tier, mode=mode, scope=scope)

    print(f"  {C.BOLD}Preflight Check{C.RESET}")
    check = assessment.preflight_check()
    print(f"  Available: {C.GREEN}{len(check['available'])}{C.RESET}")
    print(f"  Missing:   {C.RED}{len(check['missing'])}{C.RESET}")
    print(f"  Readiness: {C.CYAN}{check['ready_pct']:.0f}%{C.RESET}")
    print()

    if check["ready_pct"] < 20 and not args.force:
        print(f"  {C.YELLOW}Warning: Less than 20% of tools are installed.{C.RESET}")
        print(f"  Run {C.GREEN}hopeup install --tier {tier}{C.RESET} first, or use {C.GREEN}--force{C.RESET} to proceed anyway.")
        return

    assessment.prepare()
    print(f"  Output: {C.DIM}{assessment.output_dir}{C.RESET}")
    print()

    categories = None
    if args.categories:
        categories = [c.strip() for c in args.categories.split(",")]

    assessment.run_assessment(categories=categories)

    report_path = generate_report(assessment)
    summary = assessment.get_summary()

    print(f"\n  {'='*60}")
    print(f"  {C.BOLD}{C.GREEN}Assessment Complete{C.RESET}")
    print(f"  ID:       {summary['id']}")
    print(f"  Tools:    {summary['total_tools_run']} run, {summary['completed']} completed")
    print(f"  Report:   {C.CYAN}{report_path}{C.RESET}")
    print(f"  {'='*60}\n")


def cmd_preflight(args):
    tier = args.tier or 1
    assessment = Assessment("preflight-check", tier, scope=args.scope or "red+blue")
    check = assessment.preflight_check()

    print(f"\n  {C.BOLD}Preflight Check — Tier {tier}{C.RESET}\n")
    print(f"  Readiness: {C.CYAN}{check['ready_pct']:.0f}%{C.RESET}\n")

    if check["available"]:
        print(f"  {C.GREEN}Available ({len(check['available'])}):{C.RESET}")
        for t in sorted(check["available"]):
            print(f"    [+] {t}")
        print()

    if check["missing"]:
        print(f"  {C.RED}Missing ({len(check['missing'])}):{C.RESET}")
        for t in sorted(check["missing"]):
            print(f"    [-] {t}")
        print()

    print(f"  Run {C.GREEN}hopeup install --tier {tier}{C.RESET} to install missing tools.\n")


def cmd_install(args):
    tier = args.tier or 1
    team = args.team
    tools = get_tier_tools(tier, TOOL_REGISTRY)
    if team:
        tools = {k: v for k, v in tools.items() if v["team"] in (team, "both")}

    print(f"\n  {C.BOLD}Installing Tier {tier} Tools ({len(tools)} tools){C.RESET}\n")

    os.makedirs(INSTALL_DIR, exist_ok=True)

    for name, config in tools.items():
        method = config["install"]
        print(f"  [{C.CYAN}*{C.RESET}] Installing {name} (via {method})...", end=" ", flush=True)

        try:
            if method == "git":
                target = os.path.join(INSTALL_DIR, name)
                if os.path.isdir(target):
                    print(f"{C.YELLOW}exists{C.RESET}")
                    continue
                import subprocess
                subprocess.run(["git", "clone", "--depth=1", config["repo"], target],
                             capture_output=True, timeout=120)
                print(f"{C.GREEN}done{C.RESET}")

            elif method == "go":
                import subprocess
                subprocess.run(config["install_cmd"].split(), capture_output=True, timeout=120)
                print(f"{C.GREEN}done{C.RESET}")

            elif method == "pip":
                import subprocess
                subprocess.run(config["install_cmd"].split(), capture_output=True, timeout=120)
                print(f"{C.GREEN}done{C.RESET}")

            elif method == "npm":
                import subprocess
                subprocess.run(config["install_cmd"].split(), capture_output=True, timeout=120)
                print(f"{C.GREEN}done{C.RESET}")

            elif method == "gem":
                import subprocess
                subprocess.run(config["install_cmd"].split(), capture_output=True, timeout=120)
                print(f"{C.GREEN}done{C.RESET}")

            elif method == "cargo":
                import subprocess
                subprocess.run(config["install_cmd"].split(), capture_output=True, timeout=300)
                print(f"{C.GREEN}done{C.RESET}")

            elif method == "apt":
                import subprocess
                subprocess.run(config["install_cmd"].split(), capture_output=True, timeout=120)
                print(f"{C.GREEN}done{C.RESET}")

            elif method == "script":
                print(f"{C.YELLOW}manual — run: {config['install_cmd']}{C.RESET}")

            else:
                print(f"{C.YELLOW}unknown method{C.RESET}")

        except Exception as e:
            print(f"{C.RED}failed ({e}){C.RESET}")

    print(f"\n  {C.GREEN}Installation complete.{C.RESET}")
    print(f"  Tools directory: {INSTALL_DIR}\n")


def cmd_train(args):
    print(f"\n  {C.BOLD}Training Modules{C.RESET}\n")
    modules = [
        ("BH-101", "Bug Bounty Fundamentals", "beginner", "Learn the basics of bug bounty hunting, responsible disclosure, and setting up your environment."),
        ("BH-102", "Reconnaissance Mastery", "beginner", "Master subdomain enumeration, DNS recon, port scanning, and OSINT techniques."),
        ("BH-201", "Web Application Hacking", "intermediate", "Deep-dive into OWASP Top 10: SQLi, XSS, SSRF, XXE, IDOR, and more."),
        ("BH-202", "API & Authentication Testing", "intermediate", "Test REST/GraphQL APIs, JWT attacks, OAuth flaws, and session management."),
        ("BH-301", "Advanced Exploitation", "advanced", "Deserialization attacks, race conditions, prototype pollution, and template injection."),
        ("BH-302", "Cloud & Infrastructure", "advanced", "AWS/Azure/GCP security testing, container escape, and Kubernetes pentesting."),
        ("BD-101", "Blue Team Essentials", "beginner", "Introduction to defensive security, monitoring, and incident detection."),
        ("BD-201", "SIEM & Threat Hunting", "intermediate", "Deploy and configure SIEM, write detection rules, and hunt threats."),
        ("BD-301", "Incident Response & Forensics", "advanced", "Memory forensics, disk analysis, malware triage, and IR playbooks."),
        ("DP-101", "Platform Deployment Guide", "beginner", "How to install, configure, and deploy this platform for your business or clients."),
    ]

    for code, title, level, desc in modules:
        level_color = C.GREEN if level == "beginner" else C.YELLOW if level == "intermediate" else C.RED
        print(f"  {C.CYAN}{code}{C.RESET}  {level_color}[{level.upper():12s}]{C.RESET}  {C.WHITE}{title}{C.RESET}")
        print(f"         {C.DIM}{desc}{C.RESET}")
        print()

    print(f"  Run {C.GREEN}hopeup train --module <CODE>{C.RESET} to start a module.\n")


def cmd_report(args):
    scan_dir = args.scan_dir
    if not scan_dir:
        if os.path.isdir(OUTPUT_DIR):
            scans = sorted(os.listdir(OUTPUT_DIR), reverse=True)
            if scans:
                scan_dir = os.path.join(OUTPUT_DIR, scans[0])
            else:
                print(f"  {C.RED}No scans found in {OUTPUT_DIR}{C.RESET}")
                return
        else:
            print(f"  {C.RED}No scans directory found. Run a scan first.{C.RESET}")
            return

    meta_file = os.path.join(scan_dir, "meta.json")
    summary_file = os.path.join(scan_dir, "summary.json")

    if not os.path.isfile(summary_file):
        print(f"  {C.RED}No summary.json found in {scan_dir}{C.RESET}")
        return

    with open(summary_file) as f:
        summary = json.load(f)

    print(f"\n  {C.BOLD}Assessment Report{C.RESET}")
    print(f"  ID:     {summary['assessment_id']}")
    print(f"  Target: {summary['target']}")
    print(f"  Tier:   {summary['tier']}")
    print(f"  Status: {summary['status']}")
    print(f"\n  {C.BOLD}Stats:{C.RESET}")
    for k, v in summary["stats"].items():
        print(f"    {k}: {v}")

    report_path = os.path.join(scan_dir, "report.html")
    if os.path.isfile(report_path):
        print(f"\n  Report: {C.CYAN}{report_path}{C.RESET}")
    print()


def main():
    parser = argparse.ArgumentParser(
        prog="hopeup",
        description="HopeUp Security Platform — Offensive & Defensive Operations",
    )
    subparsers = parser.add_subparsers(dest="command")

    # dashboard
    subparsers.add_parser("dashboard", help="Show platform dashboard")

    # tools
    p_tools = subparsers.add_parser("tools", help="List all security tools")
    p_tools.add_argument("--team", choices=["red", "blue"], help="Filter by team")
    p_tools.add_argument("--tier", type=int, choices=[1, 2, 3, 4], help="Filter by max tier")
    p_tools.add_argument("--category", help="Filter by category")

    # tiers
    subparsers.add_parser("tiers", help="Show business tier details")

    # scan
    p_scan = subparsers.add_parser("scan", help="Run a security assessment")
    p_scan.add_argument("--target", "-t", required=True, help="Target domain or IP")
    p_scan.add_argument("--tier", type=int, choices=[1, 2, 3, 4], default=1, help="Business tier (1-4)")
    p_scan.add_argument("--scope", choices=["red", "blue", "red+blue"], default="red+blue", help="Assessment scope")
    p_scan.add_argument("--mode", choices=["quick", "full", "deep"], default="full", help="Scan mode")
    p_scan.add_argument("--categories", help="Comma-separated list of categories to run")
    p_scan.add_argument("--force", action="store_true", help="Run even if tool readiness is low")

    # preflight
    p_pre = subparsers.add_parser("preflight", help="Check tool readiness")
    p_pre.add_argument("--tier", type=int, choices=[1, 2, 3, 4], default=1)
    p_pre.add_argument("--scope", choices=["red", "blue", "red+blue"], default="red+blue")

    # install
    p_inst = subparsers.add_parser("install", help="Install tools for a tier")
    p_inst.add_argument("--tier", type=int, choices=[1, 2, 3, 4], default=1)
    p_inst.add_argument("--team", choices=["red", "blue"])

    # train
    p_train = subparsers.add_parser("train", help="Launch training modules")
    p_train.add_argument("--module", help="Module code to start")

    # report
    p_report = subparsers.add_parser("report", help="View or regenerate a report")
    p_report.add_argument("--scan-dir", help="Path to scan output directory")

    args = parser.parse_args()

    commands = {
        "dashboard": cmd_dashboard,
        "tools": cmd_tools,
        "tiers": cmd_tiers,
        "scan": cmd_scan,
        "preflight": cmd_preflight,
        "install": cmd_install,
        "train": cmd_train,
        "report": cmd_report,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        cmd_dashboard(args)


if __name__ == "__main__":
    main()
