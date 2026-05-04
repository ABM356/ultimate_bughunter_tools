"use client";

import { useState } from "react";
import { Calendar, Pause, Play, Plus, Trash2 } from "lucide-react";
import { toast } from "sonner";
import { PageHeader } from "@/components/PageHeader";
import { DataTable, type Column } from "@/components/DataTable";
import { formatDateTime } from "@/lib/utils";
import { cn } from "@/lib/utils";
import type { ScheduledJob } from "@/lib/types";

const INITIAL_JOBS: ScheduledJob[] = [
  {
    id: "JOB-1",
    name: "Daily web scan: production",
    job_type: "scan",
    cron: "0 2 * * *",
    target: "https://app.hopeup.io",
    next_run: new Date(Date.now() + 1000 * 60 * 60 * 14).toISOString(),
    last_run: new Date(Date.now() - 1000 * 60 * 60 * 10).toISOString(),
    enabled: true,
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 24 * 30).toISOString(),
  },
  {
    id: "JOB-2",
    name: "Weekly threat intel pull (MISP)",
    job_type: "intel_pull",
    cron: "0 5 * * 1",
    next_run: new Date(Date.now() + 1000 * 60 * 60 * 30).toISOString(),
    last_run: new Date(Date.now() - 1000 * 60 * 60 * 24 * 6).toISOString(),
    enabled: true,
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 24 * 60).toISOString(),
  },
  {
    id: "JOB-3",
    name: "Monthly compliance report",
    job_type: "report",
    cron: "0 9 1 * *",
    next_run: new Date(Date.now() + 1000 * 60 * 60 * 24 * 28).toISOString(),
    enabled: false,
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 24 * 90).toISOString(),
  },
];

export default function SchedulePage() {
  const [jobs, setJobs] = useState<ScheduledJob[]>(INITIAL_JOBS);
  const [showForm, setShowForm] = useState(false);
  const [draft, setDraft] = useState({
    name: "",
    job_type: "scan" as ScheduledJob["job_type"],
    cron: "0 2 * * *",
    target: "",
  });

  const toggle = (id: string) => {
    setJobs((prev) => prev.map((j) => (j.id === id ? { ...j, enabled: !j.enabled } : j)));
    toast.success("Job updated");
  };

  const remove = (id: string) => {
    setJobs((prev) => prev.filter((j) => j.id !== id));
    toast("Job removed");
  };

  const addJob = () => {
    if (!draft.name) return;
    const newJob: ScheduledJob = {
      id: `JOB-${Math.floor(Math.random() * 1000)}`,
      name: draft.name,
      job_type: draft.job_type,
      cron: draft.cron,
      target: draft.target || undefined,
      next_run: new Date(Date.now() + 1000 * 60 * 60).toISOString(),
      enabled: true,
      created_at: new Date().toISOString(),
    };
    setJobs((p) => [newJob, ...p]);
    setShowForm(false);
    setDraft({ name: "", job_type: "scan", cron: "0 2 * * *", target: "" });
    toast.success("Job scheduled");
  };

  const columns: Column<ScheduledJob>[] = [
    { key: "name", header: "Name", sortable: true },
    {
      key: "job_type",
      header: "Type",
      render: (r) => <span className="text-xs uppercase">{r.job_type.replace(/_/g, " ")}</span>,
      sortable: true,
    },
    {
      key: "cron",
      header: "Schedule",
      render: (r) => <span className="font-mono text-xs">{r.cron}</span>,
    },
    {
      key: "target",
      header: "Target",
      render: (r) => <span className="font-mono text-xs">{r.target || "-"}</span>,
    },
    {
      key: "next_run",
      header: "Next Run",
      render: (r) => <span className="text-xs">{formatDateTime(r.next_run)}</span>,
      sortable: true,
    },
    {
      key: "enabled",
      header: "Enabled",
      render: (r) => (
        <span
          className={cn(
            "inline-block h-2 w-2 rounded-full",
            r.enabled ? "bg-sev-info animate-pulse" : "bg-fg-subtle",
          )}
        />
      ),
    },
    {
      key: "actions",
      header: "",
      render: (r) => (
        <div className="flex gap-1">
          <button
            type="button"
            onClick={() => toggle(r.id)}
            className="p-1 rounded hover:bg-panel-hover text-fg-muted hover:text-fg"
            aria-label={r.enabled ? "Pause" : "Enable"}
          >
            {r.enabled ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
          </button>
          <button
            type="button"
            onClick={() => remove(r.id)}
            className="p-1 rounded hover:bg-panel-hover text-fg-muted hover:text-sev-critical"
            aria-label="Delete"
          >
            <Trash2 className="h-4 w-4" />
          </button>
        </div>
      ),
      width: "80px",
    },
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Schedule"
        description="Recurring scans, reports, and intel pulls"
        action={
          <button type="button" onClick={() => setShowForm(true)} className="btn-primary">
            <Plus className="h-4 w-4" /> New Job
          </button>
        }
      />

      {showForm && (
        <div className="panel p-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 items-end animate-fade-in">
          <div>
            <label className="label">Name</label>
            <input
              type="text"
              value={draft.name}
              onChange={(e) => setDraft({ ...draft, name: e.target.value })}
              placeholder="Daily web scan"
              className="input"
            />
          </div>
          <div>
            <label className="label">Type</label>
            <select
              value={draft.job_type}
              onChange={(e) =>
                setDraft({ ...draft, job_type: e.target.value as ScheduledJob["job_type"] })
              }
              className="input"
            >
              <option value="scan">Scan</option>
              <option value="report">Report</option>
              <option value="recon">Recon</option>
              <option value="intel_pull">Intel Pull</option>
            </select>
          </div>
          <div>
            <label className="label">Cron</label>
            <div className="flex items-center gap-2">
              <Calendar className="h-4 w-4 text-fg-muted" />
              <input
                type="text"
                value={draft.cron}
                onChange={(e) => setDraft({ ...draft, cron: e.target.value })}
                className="input font-mono"
              />
            </div>
          </div>
          <div>
            <label className="label">Target (optional)</label>
            <input
              type="text"
              value={draft.target}
              onChange={(e) => setDraft({ ...draft, target: e.target.value })}
              placeholder="https://example.com"
              className="input"
            />
          </div>
          <div className="md:col-span-2 lg:col-span-4 flex justify-end gap-2">
            <button type="button" onClick={() => setShowForm(false)} className="btn-secondary">
              Cancel
            </button>
            <button type="button" onClick={addJob} className="btn-primary">
              Schedule
            </button>
          </div>
        </div>
      )}

      <DataTable<ScheduledJob> columns={columns} data={jobs} rowKey={(r) => r.id} />
    </div>
  );
}
