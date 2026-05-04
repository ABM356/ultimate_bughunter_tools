"use client";

import Link from "next/link";
import { useState } from "react";
import { Filter, Plus } from "lucide-react";
import { PageHeader } from "@/components/PageHeader";
import { DataTable, type Column } from "@/components/DataTable";
import { ScanProgress } from "@/components/ScanProgress";
import { formatRelative } from "@/lib/utils";
import type { Scan, ScanStatus } from "@/lib/types";

const SCANS: Scan[] = [
  {
    id: "SC-4421",
    target: "https://api.example.com",
    scan_type: "api",
    scan_level: "deep",
    tier: "enterprise",
    status: "running",
    progress: 64,
    findings_count: 12,
    started_at: new Date(Date.now() - 1000 * 60 * 22).toISOString(),
    created_by: "alex.k",
    tenant_id: "t-1",
  },
  {
    id: "SC-4420",
    target: "10.0.4.0/24",
    scan_type: "network",
    scan_level: "medium",
    tier: "pro",
    status: "running",
    progress: 38,
    findings_count: 4,
    started_at: new Date(Date.now() - 1000 * 60 * 11).toISOString(),
    created_by: "kanya.s",
    tenant_id: "t-1",
  },
  {
    id: "SC-4418",
    target: "https://app.example.com",
    scan_type: "web",
    scan_level: "fast",
    tier: "pro",
    status: "completed",
    progress: 100,
    findings_count: 27,
    started_at: new Date(Date.now() - 1000 * 60 * 90).toISOString(),
    completed_at: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
    duration_seconds: 1742,
    created_by: "jorge.m",
    tenant_id: "t-1",
  },
  {
    id: "SC-4416",
    target: "https://staging.example.com",
    scan_type: "full",
    scan_level: "deep",
    tier: "enterprise",
    status: "failed",
    progress: 12,
    findings_count: 0,
    started_at: new Date(Date.now() - 1000 * 60 * 240).toISOString(),
    created_by: "alex.k",
    tenant_id: "t-1",
  },
];

const STATUS_OPTIONS: ScanStatus[] = ["pending", "queued", "running", "completed", "failed", "cancelled"];

export default function ScansPage() {
  const [statusFilter, setStatusFilter] = useState<string>("");
  const [typeFilter, setTypeFilter] = useState<string>("");

  const filtered = SCANS.filter((s) => {
    if (statusFilter && s.status !== statusFilter) return false;
    if (typeFilter && s.scan_type !== typeFilter) return false;
    return true;
  });

  const columns: Column<Scan>[] = [
    {
      key: "id",
      header: "ID",
      render: (r) => (
        <Link href={`/scans/${r.id}`} className="font-mono text-xs text-accent hover:underline">
          {r.id}
        </Link>
      ),
      width: "100px",
    },
    {
      key: "target",
      header: "Target",
      render: (r) => <span className="font-mono text-xs break-all">{r.target}</span>,
      sortable: true,
    },
    {
      key: "scan_type",
      header: "Type",
      render: (r) => <span className="text-xs uppercase font-medium">{r.scan_type}</span>,
      sortable: true,
    },
    {
      key: "scan_level",
      header: "Depth",
      render: (r) => <span className="text-xs capitalize">{r.scan_level}</span>,
      sortable: true,
    },
    {
      key: "progress",
      header: "Progress",
      render: (r) => <ScanProgress status={r.status} progress={r.progress} />,
      width: "200px",
    },
    {
      key: "findings_count",
      header: "Findings",
      render: (r) => <span className="font-mono tabular-nums">{r.findings_count}</span>,
      sortable: true,
    },
    {
      key: "started_at",
      header: "Started",
      render: (r) => <span className="text-xs text-fg-muted">{formatRelative(r.started_at)}</span>,
      sortable: true,
    },
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Scans"
        description="Vulnerability scanning across web, API, and network targets"
        action={
          <Link href="/scans/new" className="btn-primary">
            <Plus className="h-4 w-4" /> New Scan
          </Link>
        }
      />

      <div className="panel p-4 flex flex-wrap items-end gap-3">
        <Filter className="h-4 w-4 text-fg-muted mb-2.5" />
        <div className="min-w-[160px]">
          <label className="label">Status</label>
          <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)} className="input">
            <option value="">All</option>
            {STATUS_OPTIONS.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>
        <div className="min-w-[160px]">
          <label className="label">Type</label>
          <select value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)} className="input">
            <option value="">All</option>
            <option value="web">Web</option>
            <option value="api">API</option>
            <option value="network">Network</option>
            <option value="full">Full</option>
          </select>
        </div>
        <button
          type="button"
          onClick={() => {
            setStatusFilter("");
            setTypeFilter("");
          }}
          className="btn-ghost"
        >
          Reset
        </button>
      </div>

      <DataTable<Scan> columns={columns} data={filtered} rowKey={(r) => r.id} />
    </div>
  );
}
