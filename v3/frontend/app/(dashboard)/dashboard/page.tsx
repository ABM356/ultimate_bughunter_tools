"use client";

import {
  Activity,
  AlertTriangle,
  DollarSign,
  Search,
  ShieldAlert,
} from "lucide-react";
import Link from "next/link";
import { PageHeader } from "@/components/PageHeader";
import { StatCard } from "@/components/StatCard";
import { SeverityBadge } from "@/components/SeverityBadge";
import { StatusBadge } from "@/components/StatusBadge";
import { VulnerabilityTrendChart } from "@/components/charts/VulnerabilityTrendChart";
import { SeverityPieChart } from "@/components/charts/SeverityPieChart";
import { formatCurrency, formatNumber, formatRelative } from "@/lib/utils";

const TREND_DATA = [
  { date: "Apr 28", critical: 2, high: 5, medium: 12, low: 18 },
  { date: "Apr 29", critical: 3, high: 6, medium: 14, low: 16 },
  { date: "Apr 30", critical: 1, high: 4, medium: 10, low: 22 },
  { date: "May 01", critical: 4, high: 8, medium: 11, low: 19 },
  { date: "May 02", critical: 2, high: 7, medium: 15, low: 25 },
  { date: "May 03", critical: 5, high: 9, medium: 13, low: 21 },
  { date: "May 04", critical: 3, high: 6, medium: 16, low: 24 },
];

const PIE_DATA = [
  { name: "critical", value: 12 },
  { name: "high", value: 38 },
  { name: "medium", value: 84 },
  { name: "low", value: 142 },
  { name: "info", value: 76 },
];

const RECENT_ALERTS = [
  {
    id: "a-1",
    title: "Brute force on bastion-01",
    severity: "high" as const,
    source: "auth.ssh",
    status: "investigating",
    created_at: new Date(Date.now() - 1000 * 60 * 6).toISOString(),
  },
  {
    id: "a-2",
    title: "S3 bucket made public: marketing-assets",
    severity: "critical" as const,
    source: "aws.cloudtrail",
    status: "new",
    created_at: new Date(Date.now() - 1000 * 60 * 23).toISOString(),
  },
  {
    id: "a-3",
    title: "Suspicious PowerShell on WIN-DBSRV-04",
    severity: "high" as const,
    source: "edr.crowdstrike",
    status: "acknowledged",
    created_at: new Date(Date.now() - 1000 * 60 * 47).toISOString(),
  },
  {
    id: "a-4",
    title: "Outbound C2 beacon to 185.x.x.x",
    severity: "critical" as const,
    source: "ndr.zeek",
    status: "investigating",
    created_at: new Date(Date.now() - 1000 * 60 * 64).toISOString(),
  },
];

const RECENT_SUBMISSIONS = [
  {
    id: "s-1",
    title: "IDOR on /api/v1/users/{id}/billing",
    program: "HopeUp Public",
    hunter: "h4ck3rb33",
    severity: "high" as const,
    status: "triaging",
    submitted_at: new Date(Date.now() - 1000 * 60 * 32).toISOString(),
  },
  {
    id: "s-2",
    title: "Reflected XSS in search header",
    program: "Acme Bank",
    hunter: "redfox42",
    severity: "medium" as const,
    status: "accepted",
    submitted_at: new Date(Date.now() - 1000 * 60 * 95).toISOString(),
  },
  {
    id: "s-3",
    title: "Auth bypass via JWT alg=none",
    program: "HopeUp Public",
    hunter: "n0mad",
    severity: "critical" as const,
    status: "submitted",
    submitted_at: new Date(Date.now() - 1000 * 60 * 18).toISOString(),
  },
];

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="SecOps Dashboard"
        description="Unified view across offensive and defensive operations."
        action={
          <Link href="/scans/new" className="btn-primary">
            <Search className="h-4 w-4" /> New Scan
          </Link>
        }
      />

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Active Scans"
          value={formatNumber(7)}
          icon={Activity}
          delta={12}
          deltaLabel="vs last week"
        />
        <StatCard
          label="Open Vulnerabilities"
          value={formatNumber(352)}
          icon={ShieldAlert}
          delta={-8}
          deltaLabel="vs last week"
          accent="warning"
        />
        <StatCard
          label="Critical Alerts"
          value={formatNumber(12)}
          icon={AlertTriangle}
          delta={4}
          deltaLabel="vs last week"
          accent="critical"
        />
        <StatCard
          label="Monthly Revenue"
          value={formatCurrency(184320)}
          icon={DollarSign}
          delta={18}
          deltaLabel="vs last month"
          accent="success"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="panel lg:col-span-2">
          <div className="px-4 py-3 border-b border-border flex items-center justify-between">
            <h3 className="text-sm font-semibold">Vulnerability Trend</h3>
            <span className="text-xs text-fg-muted">Last 7 days</span>
          </div>
          <div className="p-4">
            <VulnerabilityTrendChart data={TREND_DATA} />
          </div>
        </div>
        <div className="panel">
          <div className="px-4 py-3 border-b border-border">
            <h3 className="text-sm font-semibold">Severity Distribution</h3>
          </div>
          <div className="p-4">
            <SeverityPieChart data={PIE_DATA} />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="panel">
          <div className="px-4 py-3 border-b border-border flex items-center justify-between">
            <h3 className="text-sm font-semibold">Recent Alerts</h3>
            <Link href="/blue-team/alerts" className="text-xs text-accent hover:underline">
              View all
            </Link>
          </div>
          <ul className="divide-y divide-border-subtle">
            {RECENT_ALERTS.map((a) => (
              <li key={a.id} className="px-4 py-3 hover:bg-panel-hover">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-fg truncate">{a.title}</p>
                    <div className="flex items-center gap-2 mt-1 text-xs text-fg-muted">
                      <span className="font-mono">{a.source}</span>
                      <span className="text-fg-subtle">•</span>
                      <span>{formatRelative(a.created_at)}</span>
                    </div>
                  </div>
                  <div className="flex flex-col items-end gap-1">
                    <SeverityBadge severity={a.severity} />
                    <StatusBadge status={a.status} />
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>

        <div className="panel">
          <div className="px-4 py-3 border-b border-border flex items-center justify-between">
            <h3 className="text-sm font-semibold">Recent Submissions</h3>
            <Link href="/bug-bounty/submissions" className="text-xs text-accent hover:underline">
              View all
            </Link>
          </div>
          <ul className="divide-y divide-border-subtle">
            {RECENT_SUBMISSIONS.map((s) => (
              <li key={s.id} className="px-4 py-3 hover:bg-panel-hover">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-fg truncate">{s.title}</p>
                    <div className="flex items-center gap-2 mt-1 text-xs text-fg-muted">
                      <span>{s.program}</span>
                      <span className="text-fg-subtle">•</span>
                      <span className="font-mono">{s.hunter}</span>
                      <span className="text-fg-subtle">•</span>
                      <span>{formatRelative(s.submitted_at)}</span>
                    </div>
                  </div>
                  <div className="flex flex-col items-end gap-1">
                    <SeverityBadge severity={s.severity} />
                    <StatusBadge status={s.status} />
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
