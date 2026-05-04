"use client";

import { AlertOctagon, ShieldCheck } from "lucide-react";
import { PageHeader } from "@/components/PageHeader";
import { SeverityBadge } from "@/components/SeverityBadge";
import { StatusBadge } from "@/components/StatusBadge";
import { formatDateTime, formatRelative } from "@/lib/utils";
import type { Severity } from "@/lib/types";

interface Incident {
  id: string;
  title: string;
  severity: Severity;
  status: string;
  detected_at: string;
  assignee: string;
  timeline: { time: string; event: string; user: string }[];
}

const INCIDENTS: Incident[] = [
  {
    id: "INC-2025-04",
    title: "Possible data exfiltration via S3 public bucket",
    severity: "critical",
    status: "containment",
    detected_at: new Date(Date.now() - 1000 * 60 * 24).toISOString(),
    assignee: "kanya.s",
    timeline: [
      { time: new Date(Date.now() - 1000 * 60 * 24).toISOString(), event: "Alert triggered: S3 ACL change", user: "siem.bot" },
      { time: new Date(Date.now() - 1000 * 60 * 22).toISOString(), event: "Incident opened", user: "kanya.s" },
      { time: new Date(Date.now() - 1000 * 60 * 18).toISOString(), event: "Blocked anonymous access via bucket policy", user: "kanya.s" },
      { time: new Date(Date.now() - 1000 * 60 * 12).toISOString(), event: "CloudTrail export captured", user: "auto.runbook" },
      { time: new Date(Date.now() - 1000 * 60 * 4).toISOString(), event: "Engaged AWS support", user: "kanya.s" },
    ],
  },
  {
    id: "INC-2025-03",
    title: "Lateral movement attempt - WIN-DBSRV-04",
    severity: "high",
    status: "eradication",
    detected_at: new Date(Date.now() - 1000 * 60 * 110).toISOString(),
    assignee: "jorge.m",
    timeline: [
      { time: new Date(Date.now() - 1000 * 60 * 110).toISOString(), event: "EDR detection: encoded PowerShell", user: "edr.bot" },
      { time: new Date(Date.now() - 1000 * 60 * 96).toISOString(), event: "Host isolated", user: "jorge.m" },
      { time: new Date(Date.now() - 1000 * 60 * 60).toISOString(), event: "Forensic image taken", user: "jorge.m" },
    ],
  },
];

export default function IncidentsPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Incidents"
        description="Active investigations with response timelines"
        breadcrumbs={[{ label: "Blue Team", href: "/blue-team" }, { label: "Incidents" }]}
      />

      <div className="space-y-4">
        {INCIDENTS.map((inc) => (
          <div key={inc.id} className="panel">
            <div className="px-4 py-3 border-b border-border flex items-start justify-between gap-3">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <AlertOctagon className="h-4 w-4 text-sev-critical" />
                  <h3 className="text-sm font-semibold text-fg">{inc.title}</h3>
                </div>
                <div className="flex items-center gap-2 text-xs text-fg-muted">
                  <span className="font-mono">{inc.id}</span>
                  <span className="text-fg-subtle">•</span>
                  <span>Detected {formatRelative(inc.detected_at)}</span>
                  <span className="text-fg-subtle">•</span>
                  <span className="font-mono">{inc.assignee}</span>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <SeverityBadge severity={inc.severity} />
                <StatusBadge status={inc.status} />
              </div>
            </div>
            <div className="p-4">
              <h4 className="text-xs uppercase tracking-wide text-fg-muted font-semibold mb-3">
                Timeline
              </h4>
              <ol className="relative border-l border-border ml-2 space-y-3">
                {inc.timeline.map((evt, idx) => (
                  <li key={idx} className="ml-4">
                    <div className="absolute -left-[5px] mt-1.5 h-2 w-2 rounded-full bg-accent" />
                    <p className="text-sm text-fg">{evt.event}</p>
                    <p className="text-xs text-fg-muted mt-0.5">
                      {formatDateTime(evt.time)} · <span className="font-mono">{evt.user}</span>
                    </p>
                  </li>
                ))}
              </ol>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
