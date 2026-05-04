"use client";

import Link from "next/link";
import { CheckCircle2, DollarSign, ExternalLink } from "lucide-react";
import { PageHeader } from "@/components/PageHeader";
import { StatCard } from "@/components/StatCard";
import { DataTable, type Column } from "@/components/DataTable";
import { SeverityBadge } from "@/components/SeverityBadge";
import { StatusBadge } from "@/components/StatusBadge";
import { formatCurrency, formatDate, formatNumber } from "@/lib/utils";
import type { Severity, SubmissionStatus } from "@/lib/types";

interface ProgramSubmission {
  id: string;
  title: string;
  hunter: string;
  severity: Severity;
  status: SubmissionStatus;
  reward: number | null;
  submitted_at: string;
}

const SUBMISSIONS: ProgramSubmission[] = [
  {
    id: "S-2451",
    title: "Auth bypass via JWT alg=none",
    hunter: "n0mad",
    severity: "critical",
    status: "triaging",
    reward: null,
    submitted_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
  },
  {
    id: "S-2447",
    title: "IDOR on /api/v1/users/{id}/billing",
    hunter: "h4ck3rb33",
    severity: "high",
    status: "accepted",
    reward: 4500,
    submitted_at: new Date(Date.now() - 1000 * 60 * 60 * 30).toISOString(),
  },
  {
    id: "S-2441",
    title: "Stored XSS on profile bio",
    hunter: "panda",
    severity: "medium",
    status: "fixed",
    reward: 1200,
    submitted_at: new Date(Date.now() - 1000 * 60 * 60 * 60).toISOString(),
  },
  {
    id: "S-2438",
    title: "Open redirect in /go endpoint",
    hunter: "redfox42",
    severity: "low",
    status: "paid",
    reward: 250,
    submitted_at: new Date(Date.now() - 1000 * 60 * 60 * 90).toISOString(),
  },
];

export default function ProgramDetailPage({ params }: { params: { id: string } }) {
  const columns: Column<ProgramSubmission>[] = [
    {
      key: "id",
      header: "ID",
      render: (r) => (
        <Link
          href={`/bug-bounty/submissions?id=${r.id}`}
          className="font-mono text-xs text-accent hover:underline"
        >
          {r.id}
        </Link>
      ),
      width: "100px",
    },
    { key: "title", header: "Title", sortable: true },
    {
      key: "hunter",
      header: "Hunter",
      render: (r) => <span className="font-mono text-xs">{r.hunter}</span>,
      sortable: true,
    },
    {
      key: "severity",
      header: "Severity",
      render: (r) => <SeverityBadge severity={r.severity} />,
      sortable: true,
    },
    {
      key: "status",
      header: "Status",
      render: (r) => <StatusBadge status={r.status} />,
      sortable: true,
    },
    {
      key: "reward",
      header: "Reward",
      render: (r) => (r.reward ? formatCurrency(r.reward) : "-"),
      sortable: true,
    },
    {
      key: "submitted_at",
      header: "Submitted",
      render: (r) => <span className="text-xs text-fg-muted">{formatDate(r.submitted_at)}</span>,
      sortable: true,
    },
  ];

  const totalReward = SUBMISSIONS.reduce((s, r) => s + (r.reward || 0), 0);

  return (
    <div className="space-y-6">
      <PageHeader
        title={`Program ${params.id}`}
        description="HopeUp Public — main production environment scope"
        breadcrumbs={[
          { label: "Bug Bounty", href: "/bug-bounty" },
          { label: params.id },
        ]}
        action={
          <button type="button" className="btn-secondary">
            <ExternalLink className="h-4 w-4" /> Public Page
          </button>
        }
      />

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <StatCard label="Submissions" value={formatNumber(SUBMISSIONS.length)} />
        <StatCard
          label="Resolved"
          value={formatNumber(SUBMISSIONS.filter((s) => s.status === "fixed" || s.status === "paid").length)}
          icon={CheckCircle2}
          accent="success"
        />
        <StatCard label="Total Paid" value={formatCurrency(totalReward)} icon={DollarSign} accent="success" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="panel lg:col-span-2">
          <div className="px-4 py-3 border-b border-border">
            <h3 className="text-sm font-semibold">Scope</h3>
          </div>
          <div className="p-4 space-y-4">
            <div>
              <p className="label">In Scope</p>
              <ul className="space-y-1 text-sm font-mono">
                <li className="text-fg">*.hopeup.io</li>
                <li className="text-fg">api.hopeup.io</li>
                <li className="text-fg">app.hopeup.io</li>
                <li className="text-fg">Mobile iOS / Android apps</li>
              </ul>
            </div>
            <div>
              <p className="label">Out of Scope</p>
              <ul className="space-y-1 text-sm font-mono text-fg-muted">
                <li>marketing.hopeup.io</li>
                <li>blog.hopeup.io</li>
                <li>Third-party SaaS subdomains</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="panel">
          <div className="px-4 py-3 border-b border-border">
            <h3 className="text-sm font-semibold">Reward Tiers</h3>
          </div>
          <div className="p-4 space-y-3">
            {[
              { label: "Critical", amount: 25000, color: "text-sev-critical" },
              { label: "High", amount: 7500, color: "text-sev-high" },
              { label: "Medium", amount: 1500, color: "text-sev-medium" },
              { label: "Low", amount: 250, color: "text-sev-low" },
            ].map((tier) => (
              <div key={tier.label} className="flex items-center justify-between">
                <span className={`text-sm font-semibold ${tier.color}`}>{tier.label}</span>
                <span className="text-sm font-mono">{formatCurrency(tier.amount)}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <DataTable<ProgramSubmission>
        columns={columns}
        data={SUBMISSIONS}
        rowKey={(r) => r.id}
      />
    </div>
  );
}
