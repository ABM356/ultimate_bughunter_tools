"use client";

import { useState } from "react";
import { CheckCircle2, Filter, X } from "lucide-react";
import { toast } from "sonner";
import { PageHeader } from "@/components/PageHeader";
import { DataTable, type Column } from "@/components/DataTable";
import { SeverityBadge } from "@/components/SeverityBadge";
import { StatusBadge } from "@/components/StatusBadge";
import { formatRelative } from "@/lib/utils";
import type { Alert, AlertStatus, Severity } from "@/lib/types";

const ALERTS: Alert[] = [
  {
    id: "AL-9211",
    title: "Brute force on bastion-01",
    description: "182 failed SSH logins from 5.42.x.x in 60s",
    severity: "high",
    source: "auth.ssh",
    status: "investigating",
    category: "credential_access",
    asset: "bastion-01",
    ip_address: "5.42.196.18",
    created_at: new Date(Date.now() - 1000 * 60 * 6).toISOString(),
  },
  {
    id: "AL-9210",
    title: "S3 bucket made public: marketing-assets",
    description: "ACL change to AllUsers READ via console session",
    severity: "critical",
    source: "aws.cloudtrail",
    status: "new",
    category: "exposure",
    asset: "s3://marketing-assets",
    created_at: new Date(Date.now() - 1000 * 60 * 23).toISOString(),
  },
  {
    id: "AL-9209",
    title: "Suspicious PowerShell on WIN-DBSRV-04",
    description: "Encoded base64 payload executed under SYSTEM",
    severity: "high",
    source: "edr.crowdstrike",
    status: "acknowledged",
    category: "execution",
    asset: "WIN-DBSRV-04",
    created_at: new Date(Date.now() - 1000 * 60 * 47).toISOString(),
  },
  {
    id: "AL-9208",
    title: "Outbound C2 beacon to 185.x.x.x",
    description: "Periodic 60s beacon, IDS rule SID 2027345 hit",
    severity: "critical",
    source: "ndr.zeek",
    status: "investigating",
    category: "command_and_control",
    asset: "WIN-DBSRV-04",
    created_at: new Date(Date.now() - 1000 * 60 * 64).toISOString(),
  },
  {
    id: "AL-9201",
    title: "MFA bypass attempt detected",
    description: "Authenticator timestamp drift suggests SIM swap",
    severity: "medium",
    source: "iam.okta",
    status: "resolved",
    category: "credential_access",
    asset: "user@hopeup.io",
    created_at: new Date(Date.now() - 1000 * 60 * 120).toISOString(),
  },
];

const STATUSES: AlertStatus[] = [
  "new",
  "acknowledged",
  "investigating",
  "resolved",
  "false_positive",
];
const SEVERITIES: Severity[] = ["critical", "high", "medium", "low", "info"];

export default function AlertsPage() {
  const [statusFilter, setStatusFilter] = useState<string>("");
  const [severityFilter, setSeverityFilter] = useState<string>("");

  const filtered = ALERTS.filter((a) => {
    if (statusFilter && a.status !== statusFilter) return false;
    if (severityFilter && a.severity !== severityFilter) return false;
    return true;
  });

  const columns: Column<Alert>[] = [
    { key: "id", header: "ID", render: (r) => <span className="font-mono text-xs text-accent">{r.id}</span>, width: "100px" },
    { key: "title", header: "Title", sortable: true },
    { key: "asset", header: "Asset", render: (r) => <span className="font-mono text-xs">{r.asset || "-"}</span>, sortable: true },
    { key: "source", header: "Source", render: (r) => <span className="font-mono text-xs text-fg-muted">{r.source}</span>, sortable: true },
    { key: "severity", header: "Severity", render: (r) => <SeverityBadge severity={r.severity} />, sortable: true },
    { key: "status", header: "Status", render: (r) => <StatusBadge status={r.status} />, sortable: true },
    { key: "created_at", header: "Detected", render: (r) => <span className="text-xs text-fg-muted">{formatRelative(r.created_at)}</span>, sortable: true },
    {
      key: "actions",
      header: "",
      render: (r) => (
        <div className="flex gap-1">
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              toast.success(`Alert ${r.id} acknowledged`);
            }}
            className="p-1 rounded hover:bg-panel-hover text-fg-muted hover:text-sev-info"
            title="Acknowledge"
          >
            <CheckCircle2 className="h-4 w-4" />
          </button>
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              toast(`Alert ${r.id} marked false positive`);
            }}
            className="p-1 rounded hover:bg-panel-hover text-fg-muted hover:text-sev-critical"
            title="False positive"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      ),
      width: "80px",
    },
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Alerts"
        description="All security detections across your environment"
        breadcrumbs={[{ label: "Blue Team", href: "/blue-team" }, { label: "Alerts" }]}
      />

      <div className="panel p-4 flex flex-wrap items-end gap-3">
        <Filter className="h-4 w-4 text-fg-muted mb-2.5" />
        <div className="min-w-[160px]">
          <label className="label">Status</label>
          <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)} className="input">
            <option value="">All</option>
            {STATUSES.map((s) => (
              <option key={s} value={s}>{s.replace(/_/g, " ")}</option>
            ))}
          </select>
        </div>
        <div className="min-w-[160px]">
          <label className="label">Severity</label>
          <select value={severityFilter} onChange={(e) => setSeverityFilter(e.target.value)} className="input">
            <option value="">All</option>
            {SEVERITIES.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>
        <button
          type="button"
          onClick={() => {
            setStatusFilter("");
            setSeverityFilter("");
          }}
          className="btn-ghost"
        >
          Reset
        </button>
      </div>

      <DataTable<Alert> columns={columns} data={filtered} rowKey={(r) => r.id} />
    </div>
  );
}
