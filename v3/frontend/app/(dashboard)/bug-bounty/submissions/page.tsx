"use client";

import Link from "next/link";
import { useState } from "react";
import { Filter, Plus } from "lucide-react";
import { PageHeader } from "@/components/PageHeader";
import { DataTable, type Column } from "@/components/DataTable";
import { SeverityBadge } from "@/components/SeverityBadge";
import { StatusBadge } from "@/components/StatusBadge";
import { formatCurrency, formatRelative } from "@/lib/utils";
import type { Severity, SubmissionStatus } from "@/lib/types";

interface SubmissionRow {
  id: string;
  program: string;
  title: string;
  hunter: string;
  severity: Severity;
  status: SubmissionStatus;
  reward: number | null;
  submitted_at: string;
}

const ALL_SUBMISSIONS: SubmissionRow[] = [
  {
    id: "S-2451",
    program: "HopeUp Public",
    title: "Auth bypass via JWT alg=none",
    hunter: "n0mad",
    severity: "critical",
    status: "triaging",
    reward: null,
    submitted_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
  },
  {
    id: "S-2447",
    program: "HopeUp Public",
    title: "IDOR on /api/v1/users/{id}/billing",
    hunter: "h4ck3rb33",
    severity: "high",
    status: "accepted",
    reward: 4500,
    submitted_at: new Date(Date.now() - 1000 * 60 * 60 * 30).toISOString(),
  },
  {
    id: "S-2441",
    program: "Acme Bank",
    title: "Stored XSS on profile bio",
    hunter: "panda",
    severity: "medium",
    status: "fixed",
    reward: 1200,
    submitted_at: new Date(Date.now() - 1000 * 60 * 60 * 60).toISOString(),
  },
  {
    id: "S-2438",
    program: "Northwind",
    title: "Open redirect in /go endpoint",
    hunter: "redfox42",
    severity: "low",
    status: "paid",
    reward: 250,
    submitted_at: new Date(Date.now() - 1000 * 60 * 60 * 90).toISOString(),
  },
  {
    id: "S-2401",
    program: "HopeUp Public",
    title: "SSRF via webhook configurator",
    hunter: "ghost",
    severity: "high",
    status: "duplicate",
    reward: null,
    submitted_at: new Date(Date.now() - 1000 * 60 * 60 * 200).toISOString(),
  },
];

const STATUSES: SubmissionStatus[] = [
  "submitted",
  "triaging",
  "accepted",
  "duplicate",
  "rejected",
  "fixed",
  "paid",
];
const SEVERITIES: Severity[] = ["critical", "high", "medium", "low", "info"];

export default function AllSubmissionsPage() {
  const [statusFilter, setStatusFilter] = useState<string>("");
  const [severityFilter, setSeverityFilter] = useState<string>("");
  const [hunterFilter, setHunterFilter] = useState<string>("");

  const filtered = ALL_SUBMISSIONS.filter((row) => {
    if (statusFilter && row.status !== statusFilter) return false;
    if (severityFilter && row.severity !== severityFilter) return false;
    if (hunterFilter && !row.hunter.toLowerCase().includes(hunterFilter.toLowerCase())) return false;
    return true;
  });

  const columns: Column<SubmissionRow>[] = [
    {
      key: "id",
      header: "ID",
      render: (r) => <span className="font-mono text-xs text-accent">{r.id}</span>,
      width: "90px",
    },
    { key: "program", header: "Program", sortable: true },
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
    { key: "status", header: "Status", render: (r) => <StatusBadge status={r.status} />, sortable: true },
    {
      key: "reward",
      header: "Reward",
      render: (r) => (r.reward ? formatCurrency(r.reward) : "-"),
      sortable: true,
    },
    {
      key: "submitted_at",
      header: "Submitted",
      render: (r) => <span className="text-xs text-fg-muted">{formatRelative(r.submitted_at)}</span>,
      sortable: true,
    },
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title="All Submissions"
        description="Across every active program"
        action={
          <Link href="/bug-bounty/submissions/new" className="btn-primary">
            <Plus className="h-4 w-4" /> New Submission
          </Link>
        }
      />

      <div className="panel p-4 flex flex-wrap items-end gap-3">
        <Filter className="h-4 w-4 text-fg-muted mb-2.5" />
        <div className="min-w-[160px]">
          <label className="label">Status</label>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="input"
          >
            <option value="">All</option>
            {STATUSES.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
        </div>
        <div className="min-w-[140px]">
          <label className="label">Severity</label>
          <select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            className="input"
          >
            <option value="">All</option>
            {SEVERITIES.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
        </div>
        <div className="min-w-[180px] flex-1">
          <label className="label">Hunter</label>
          <input
            type="text"
            placeholder="Search by handle"
            value={hunterFilter}
            onChange={(e) => setHunterFilter(e.target.value)}
            className="input"
          />
        </div>
        <button
          type="button"
          onClick={() => {
            setStatusFilter("");
            setSeverityFilter("");
            setHunterFilter("");
          }}
          className="btn-ghost"
        >
          Reset
        </button>
      </div>

      <DataTable<SubmissionRow> columns={columns} data={filtered} rowKey={(r) => r.id} />
    </div>
  );
}
