"""
Scanner engine — orchestrates tool execution for security assessments.
Runs tools based on tier profile, collects output, and feeds the report generator.
"""

import os
import subprocess
import json
import time
import shutil
from datetime import datetime, timezone
from pathlib import Path

from platform.tools_registry import TOOL_REGISTRY, get_tools_by_team, CATEGORIES
from platform.tiers import get_tier, get_tier_tools


INSTALL_DIR = os.path.join(os.path.expanduser("~"), "hopeup")
OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "hopeup_reports")


class ScanResult:
    def __init__(self, tool_name, category, team):
        self.tool_name = tool_name
        self.category = category
        self.team = team
        self.status = "pending"
        self.output = ""
        self.findings = []
        self.start_time = None
        self.end_time = None
        self.duration_seconds = 0
        self.severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}

    def to_dict(self):
        return {
            "tool": self.tool_name,
            "category": self.category,
            "team": self.team,
            "status": self.status,
            "findings_count": len(self.findings),
            "severity_counts": self.severity_counts,
            "duration_seconds": self.duration_seconds,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }


class Assessment:
    def __init__(self, target, tier_num, mode="full", scope=None):
        self.id = f"ASM-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        self.target = target
        self.tier_num = tier_num
        self.tier = get_tier(tier_num)
        self.mode = mode
        self.scope = scope or "red+blue"
        self.status = "initialized"
        self.results = []
        self.start_time = None
        self.end_time = None
        self.output_dir = os.path.join(OUTPUT_DIR, self.id)

    def get_tools(self):
        tier_tools = get_tier_tools(self.tier_num, TOOL_REGISTRY)
        if self.scope == "red":
            return {k: v for k, v in tier_tools.items() if v["team"] in ("red", "both")}
        elif self.scope == "blue":
            return {k: v for k, v in tier_tools.items() if v["team"] in ("blue", "both")}
        return tier_tools

    def preflight_check(self):
        missing = []
        available = []
        tools = self.get_tools()

        for name, tool in tools.items():
            if tool["install"] == "go":
                binary = name.replace("-", "").replace("_", "")
                if shutil.which(binary) or shutil.which(name):
                    available.append(name)
                else:
                    missing.append(name)
            elif tool["install"] == "pip":
                try:
                    subprocess.run(
                        ["python3", "-c", f"import {name.replace('-', '_')}"],
                        capture_output=True, timeout=5,
                    )
                    available.append(name)
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    if shutil.which(name):
                        available.append(name)
                    else:
                        missing.append(name)
            elif tool["install"] == "git":
                tool_path = os.path.join(INSTALL_DIR, name)
                if os.path.isdir(tool_path):
                    available.append(name)
                else:
                    missing.append(name)
            else:
                if shutil.which(name):
                    available.append(name)
                else:
                    missing.append(name)

        return {
            "available": available,
            "missing": missing,
            "ready_pct": len(available) / max(len(tools), 1) * 100,
        }

    def prepare(self):
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "raw"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "parsed"), exist_ok=True)

        meta = {
            "assessment_id": self.id,
            "target": self.target,
            "tier": self.tier_num,
            "tier_name": self.tier["name"],
            "mode": self.mode,
            "scope": self.scope,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        with open(os.path.join(self.output_dir, "meta.json"), "w") as f:
            json.dump(meta, f, indent=2)

        self.status = "prepared"
        return self.output_dir

    def run_tool(self, tool_name, tool_config, extra_args=None):
        result = ScanResult(tool_name, tool_config["category"], tool_config["team"])
        result.start_time = datetime.now(timezone.utc).isoformat()

        cmd = self._build_command(tool_name, tool_config, extra_args)
        if not cmd:
            result.status = "skipped"
            result.output = f"No run command configured for {tool_name}"
            self.results.append(result)
            return result

        try:
            max_time = self.tier["scan_profile"]["max_duration_hours"] * 3600
            tool_timeout = min(600, max_time)

            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=tool_timeout,
                cwd=self.output_dir,
            )
            result.output = proc.stdout
            if proc.returncode == 0:
                result.status = "completed"
            else:
                result.status = "error"
                result.output += f"\nSTDERR: {proc.stderr}"

        except subprocess.TimeoutExpired:
            result.status = "timeout"
            result.output = f"Tool timed out after {tool_timeout}s"
        except FileNotFoundError:
            result.status = "not_installed"
            result.output = f"{tool_name} is not installed or not in PATH"
        except Exception as e:
            result.status = "error"
            result.output = str(e)

        result.end_time = datetime.now(timezone.utc).isoformat()
        if result.start_time and result.end_time:
            start = datetime.fromisoformat(result.start_time)
            end = datetime.fromisoformat(result.end_time)
            result.duration_seconds = (end - start).total_seconds()

        raw_file = os.path.join(self.output_dir, "raw", f"{tool_name}.txt")
        with open(raw_file, "w") as f:
            f.write(result.output)

        self.results.append(result)
        return result

    def _build_command(self, tool_name, tool_config, extra_args=None):
        target = self.target
        tool_commands = {
            "subfinder": ["subfinder", "-d", target, "-silent"],
            "amass": ["amass", "enum", "-passive", "-d", target],
            "assetfinder": ["assetfinder", "--subs-only", target],
            "httpx": ["httpx", "-u", target, "-silent", "-status-code", "-title"],
            "dnsx": ["dnsx", "-d", target, "-silent"],
            "naabu": ["naabu", "-host", target, "-silent"],
            "nuclei": ["nuclei", "-u", target, "-silent", "-severity", "critical,high,medium"],
            "nikto": ["nikto", "-h", target, "-Format", "json"],
            "ffuf": ["ffuf", "-u", f"https://{target}/FUZZ", "-w", "/usr/share/seclists/Discovery/Web-Content/common.txt", "-mc", "200,301,302,403"],
            "gobuster": ["gobuster", "dir", "-u", f"https://{target}", "-w", "/usr/share/seclists/Discovery/Web-Content/common.txt", "-q"],
            "sqlmap": ["sqlmap", "-u", f"https://{target}", "--batch", "--level=1", "--risk=1", "--forms"],
            "xsstrike": ["python3", "-m", "xsstrike", "-u", f"https://{target}", "--crawl"],
            "dalfox": ["dalfox", "url", f"https://{target}", "--silence"],
            "wpscan": ["wpscan", "--url", f"https://{target}", "--enumerate", "vp,vt,u"],
            "testssl": ["testssl.sh", "--quiet", "--json", target],
            "sslyze": ["sslyze", target],
            "katana": ["katana", "-u", target, "-silent"],
            "gau": ["gau", target],
            "waybackurls": ["waybackurls", target],
            "dirsearch": ["dirsearch", "-u", f"https://{target}", "-q"],
            "lynis": ["lynis", "audit", "system", "--quick", "--no-colors"],
            "gitleaks": ["gitleaks", "detect", "--source", ".", "--no-banner"],
            "detect-secrets": ["detect-secrets", "scan"],
            "hydra": ["hydra", "-L", "users.txt", "-P", "pass.txt", target, "ssh", "-t", "4"],
            "commix": ["commix", "-u", f"https://{target}", "--batch"],
        }

        cmd = tool_commands.get(tool_name)
        if cmd and extra_args:
            cmd.extend(extra_args)
        return cmd

    def run_assessment(self, categories=None):
        self.start_time = datetime.now(timezone.utc).isoformat()
        self.status = "running"
        tools = self.get_tools()

        print(f"\n{'='*60}")
        print(f"  ASSESSMENT: {self.id}")
        print(f"  Target:     {self.target}")
        print(f"  Tier:       {self.tier_num} — {self.tier['name']}")
        print(f"  Scope:      {self.scope}")
        print(f"  Tools:      {len(tools)}")
        print(f"{'='*60}\n")

        for name, config in tools.items():
            if categories and config["category"] not in categories:
                continue

            team_label = f"[{'RED' if config['team'] == 'red' else 'BLUE' if config['team'] == 'blue' else 'RED+BLUE'}]"
            print(f"  {team_label} Running {name} ({config['description'][:50]})")

            result = self.run_tool(name, config)
            status_icon = {
                "completed": "+", "error": "!", "timeout": "~",
                "not_installed": "-", "skipped": "."
            }.get(result.status, "?")
            print(f"    [{status_icon}] {result.status} ({result.duration_seconds:.1f}s)")

        self.end_time = datetime.now(timezone.utc).isoformat()
        self.status = "completed"
        self._save_summary()
        return self.results

    def _save_summary(self):
        summary = {
            "assessment_id": self.id,
            "target": self.target,
            "tier": self.tier_num,
            "scope": self.scope,
            "status": self.status,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "results": [r.to_dict() for r in self.results],
            "stats": {
                "total_tools": len(self.results),
                "completed": len([r for r in self.results if r.status == "completed"]),
                "errors": len([r for r in self.results if r.status == "error"]),
                "not_installed": len([r for r in self.results if r.status == "not_installed"]),
                "timeouts": len([r for r in self.results if r.status == "timeout"]),
            }
        }
        with open(os.path.join(self.output_dir, "summary.json"), "w") as f:
            json.dump(summary, f, indent=2)

    def get_summary(self):
        return {
            "id": self.id,
            "target": self.target,
            "tier": f"Tier {self.tier_num} — {self.tier['name']}",
            "total_tools_run": len(self.results),
            "completed": len([r for r in self.results if r.status == "completed"]),
            "findings": sum(len(r.findings) for r in self.results),
        }
