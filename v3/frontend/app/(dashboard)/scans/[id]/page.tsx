"use client";

import { useState } from "react";
import { Download, Pause, RefreshCw } from "lucide-react";
import { PageHeader } from "@/components/PageHeader";
import { ScanProgress } from "@/components/ScanProgress";
import { SeverityBadge } from "@/components/SeverityBadge";
import { StatCard } from "@/components/StatCard";
import { cn, formatDateTime } from "@/lib/utils";
import type { Severity, Vulnerability } from "@/lib/types";

const SCAN = {
  id: "SC-4421",
  target: "https://api.example.com",
  scan_type: "api" as const,
  scan_level: "deep" as const,
  status: "running" as const,
  progress: 64,
  started_at: new Date(Date.now() - 1000 * 60 * 22).toISOString(),
  created_by: "alex.k",
};

const FINDINGS: Vulnerability[] = [
  {
    id: "V-1",
    title: "SQL Injection in /search?q=",
    description: "Time-based blind SQLi in the q parameter",
    severity: "critical",
    cvss_score: 9.4,
    cwe: "CWE-89",
    affected_url: "https://api.example.com/search?q=1",
    remediation: "Use parameterized queries; validate input.",
    status: "open",
    discovered_at: new Date().toISOString(),
  },
  {
    id: "V-2",
    title: "IDOR in /users/{id}/billing",
    description: "Authenticated user can access any billing record by ID",
    severity: "high",
    cvss_score: 8.1,
    cwe: "CWE-639",
    affected_url: "https://api.example.com/users/{id}/billing",
    remediation: "Enforce ownership check at controller layer.",
    status: "open",
    discovered_at: new Date().toISOString(),
  },
  {
    id: "V-3",
    title: "Verbose error messages",
    description: "Stack traces leak framework version and DB schema",
    severity: "medium",
    cvss_score: 5.3,
    cwe: "CWE-209",
    remediation: "Disable debug mode in production.",
    status: "open",
    discovered_at: new Date().toISOString(),
  },
  {
    id: "V-4",
    title: "Missing security headers",
    description: "X-Frame-Options, CSP and HSTS are not set",
    severity: "low",
    cvss_score: 3.7,
    cwe: "CWE-693",
    remediation: "Add CSP, HSTS, X-Frame-Options headers.",
    status: "open",
    discovered_at: new Date().toISOString(),
  },
];

const SEVERITIES: Severity[] = ["critical", "high", "medium", "low", "info"];

export default function ScanDetailPage({ params }: { params: { id: string } }) {
  const [tab, setTab] = useState<"all" | Severity>("all");

  const filtered = tab === "all" ? FINDINGS : FINDINGS.filter((f) => f.severity === tab);
  const counts = SEVERITIES.reduce<Record<string, number>>(
    (acc, s) => ({ ...acc, [s]: FINDINGS.filter((f) => f.severity === s).length }),
    { all: FINDINGS.length },
  );

  return (
    <div className="space-y-6">
      <PageHeader
        title={`Scan ${params.id}`}
        description={SCAN.target}
        breadcrumbs={[{ label: "Scans", href: "/scans" }, { label: params.id }]}
        action={
          <div className="flex gap-2">
            <button type="button" className="btn-secondary">
              <RefreshCw className="h-4 w-4" /> Refresh
            </button>
            {SCAN.status === "running" && (
              <button type="button" className="btn-secondary">
                <Pause className="h-4 w-4" /> Pause
              </button>
            )}
            <button type="button" className="btn-primary">
              <Download className="h-4 w-4" /> Export
            </button>
          </div>
        }
      />

      <div className="panel p-4 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <p className="label">Target</p>
          <p className="text-sm font-mono break-all">{SCAN.target}</p>
        </div>
        <div>
          <p className="label">Type / Depth</p>
          <p className="text-sm uppercase">
            {SCAN.scan_type} · <span className="capitalize">{SCAN.scan_level}</span>
          </p>
        </div>
        <div>
          <p className="label">Started</p>
          <p className="text-sm">{formatDateTime(SCAN.started_at)}</p>
        </div>
        <div className="md:col-span-3">
          <ScanProgress status={SCAN.status} progress={SCAN.progress} />
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
        {SEVERITIES.map((sev) => (
          <StatCard
            key={sev}
            label={sev}
            value={counts[sev] || 0}
            accent={sev === "critical" || sev === "high" ? "critical" : sev === "medium" ? "warning" : "default"}
          />
        ))}
      </div>

      <div className="panel">
        <div className="px-4 py-3 border-b border-border flex items-center gap-2 overflow-x-auto">
          {(["all", ...SEVERITIES] as const).map((t) => (
            <button
              key={t}
              type="button"
              onClick={() => setTab(t)}
              className={cn(
                "px-3 py-1 text-xs uppercase rounded border whitespace-nowrap",
                tab === t
                  ? "bg-accent text-bg border-accent"
                  : "border-border text-fg-muted hover:text-fg hover:border-border-strong",
              )}
            >
              {t} <span className="ml-1 font-mono">{counts[t] || 0}</span>
            </button>
          ))}
        </div>
        <ul className="divide-y divide-border-subtle">
          {filtered.map((f) => (
            <li key={f.id} className="p-4 hover:bg-panel-hover">
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <SeverityBadge severity={f.severity} />
                    <span className="text-xs font-mono text-fg-muted">{f.cwe}</span>
                    <span className="text-xs font-mono text-fg-muted">CVSS {f.cvss_score.toFixed(1)}</span>
                  </div>
                  <p className="text-sm font-semibold">{f.title}</p>
                  <p className="text-xs text-fg-muted mt-1">{f.description}</p>
                  {f.affected_url && (
                    <p className="text-xs font-mono text-accent mt-1 break-all">{f.affected_url}</p>
                  )}
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>

      <div className="panel">
        <div className="px-4 py-3 border-b border-border flex items-center justify-between">
          <h3 className="text-sm font-semibold">Raw Output</h3>
          <button type="button" className="text-xs text-accent hover:underline">Expand</button>
        </div>
        <pre className="bg-bg-secondary p-4 text-xs font-mono text-fg-muted overflow-x-auto max-h-64">
          {`[*] starting scan ${params.id}
[*] target: ${SCAN.target}
[*] mode: ${SCAN.scan_type} (depth=${SCAN.scan_level})
[*] crawler enumerating endpoints...
[+] discovered 84 endpoints
[*] running rule pack: owasp-api-top10
[+] hit: SQLi at /search?q= (sleep payload)
[+] hit: IDOR at /users/{id}/billing
[+] hit: verbose-error at /admin/debug
[*] generating report...
`}
        </pre>
      </div>
    </div>
  );
}
