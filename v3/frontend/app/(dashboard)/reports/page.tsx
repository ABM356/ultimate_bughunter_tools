"use client";

import Link from "next/link";
import { useState } from "react";
import { Download, FileText, Filter, Plus } from "lucide-react";
import { toast } from "sonner";
import { PageHeader } from "@/components/PageHeader";
import { DataTable, type Column } from "@/components/DataTable";
import { formatBytes, formatDate } from "@/lib/utils";
import { cn } from "@/lib/utils";
import type { Report } from "@/lib/types";

const ROLE_OPTIONS: Report["role"][] = ["ciso", "cto", "manager", "engineer", "board", "compliance"];

const REPORTS: Report[] = [
  { id: "R-1", title: "Q2 Executive Summary", role: "ciso", generated_at: new Date().toISOString(), generated_by: "ai.bot", format: "pdf", download_url: "#", size_bytes: 824_000 },
  { id: "R-2", title: "Engineering Findings — Web App", role: "engineer", generated_at: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(), generated_by: "alex.k", format: "html", download_url: "#", size_bytes: 1_240_000 },
  { id: "R-3", title: "Board Update — Security Posture", role: "board", generated_at: new Date(Date.now() - 1000 * 60 * 60 * 96).toISOString(), generated_by: "ciso@hopeup.io", format: "pdf", download_url: "#", size_bytes: 442_000 },
  { id: "R-4", title: "SOC 2 Evidence Pack", role: "compliance", generated_at: new Date(Date.now() - 1000 * 60 * 60 * 168).toISOString(), generated_by: "auditor@hopeup.io", format: "pdf", download_url: "#", size_bytes: 4_220_000 },
  { id: "R-5", title: "Technical Architecture Review", role: "cto", generated_at: new Date(Date.now() - 1000 * 60 * 60 * 200).toISOString(), generated_by: "cto@hopeup.io", format: "html", download_url: "#", size_bytes: 720_000 },
  { id: "R-6", title: "Q2 Manager Brief", role: "manager", generated_at: new Date(Date.now() - 1000 * 60 * 60 * 240).toISOString(), generated_by: "ai.bot", format: "pdf", download_url: "#", size_bytes: 612_000 },
];

export default function ReportsPage() {
  const [roleFilter, setRoleFilter] = useState<string>("");
  const filtered = roleFilter ? REPORTS.filter((r) => r.role === roleFilter) : REPORTS;

  const columns: Column<Report>[] = [
    {
      key: "title",
      header: "Title",
      render: (r) => (
        <Link href={`/reports/${r.id}`} className="flex items-center gap-2 text-fg hover:text-accent">
          <FileText className="h-4 w-4 text-fg-muted" />
          {r.title}
        </Link>
      ),
      sortable: true,
    },
    {
      key: "role",
      header: "Audience",
      render: (r) => <span className="text-xs uppercase">{r.role}</span>,
      sortable: true,
    },
    {
      key: "format",
      header: "Format",
      render: (r) => <span className="text-xs uppercase font-mono">{r.format}</span>,
    },
    {
      key: "size_bytes",
      header: "Size",
      render: (r) => <span className="text-xs text-fg-muted">{formatBytes(r.size_bytes)}</span>,
      sortable: true,
    },
    {
      key: "generated_at",
      header: "Generated",
      render: (r) => <span className="text-xs text-fg-muted">{formatDate(r.generated_at)}</span>,
      sortable: true,
    },
    {
      key: "actions",
      header: "",
      render: (r) => (
        <button
          type="button"
          onClick={() => toast.success(`Downloading ${r.title}`)}
          className="p-1 rounded hover:bg-panel-hover text-fg-muted hover:text-accent"
          aria-label="Download"
        >
          <Download className="h-4 w-4" />
        </button>
      ),
      width: "60px",
    },
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Reports"
        description="Role-tailored security reports and evidence"
        action={
          <button
            type="button"
            onClick={() => toast.success("New report queued")}
            className="btn-primary"
          >
            <Plus className="h-4 w-4" /> Generate Report
          </button>
        }
      />

      <div className="panel p-3 flex flex-wrap items-center gap-2">
        <Filter className="h-4 w-4 text-fg-muted" />
        <button
          type="button"
          onClick={() => setRoleFilter("")}
          className={cn(
            "px-3 py-1 text-xs rounded border uppercase",
            !roleFilter ? "bg-accent text-bg border-accent" : "border-border text-fg-muted hover:text-fg",
          )}
        >
          All
        </button>
        {ROLE_OPTIONS.map((r) => (
          <button
            key={r}
            type="button"
            onClick={() => setRoleFilter(r)}
            className={cn(
              "px-3 py-1 text-xs rounded border uppercase",
              roleFilter === r
                ? "bg-accent text-bg border-accent"
                : "border-border text-fg-muted hover:text-fg",
            )}
          >
            {r}
          </button>
        ))}
      </div>

      <DataTable<Report> columns={columns} data={filtered} rowKey={(r) => r.id} />
    </div>
  );
}
