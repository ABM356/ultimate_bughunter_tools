"use client";

import Link from "next/link";
import { Crosshair, Map, Swords, Target } from "lucide-react";
import { PageHeader } from "@/components/PageHeader";
import { StatCard } from "@/components/StatCard";
import { StatusBadge } from "@/components/StatusBadge";
import { formatRelative } from "@/lib/utils";

const SIMULATIONS = [
  { id: "RT-101", name: "Phishing Campaign — Q2", status: "running", target: "Finance dept (140)", progress: 62 },
  { id: "RT-098", name: "Credential Stuffing", status: "completed", target: "VPN portal", progress: 100 },
  { id: "RT-097", name: "Linux LPE Chain", status: "running", target: "build-runner-04", progress: 33 },
  { id: "RT-091", name: "Domain Privesc — Kerberoast", status: "queued", target: "corp.local", progress: 0 },
];

const RECON_RESULTS = [
  { type: "subdomain", value: "internal-staging.acme.com", discovered_at: new Date(Date.now() - 1000 * 60 * 12).toISOString() },
  { type: "service", value: "10.0.4.5:9092 (Kafka, no auth)", discovered_at: new Date(Date.now() - 1000 * 60 * 24).toISOString() },
  { type: "endpoint", value: "/api/internal/admin/debug", discovered_at: new Date(Date.now() - 1000 * 60 * 41).toISOString() },
  { type: "credential", value: "BUILD\\\\jenkins:Spring2024!", discovered_at: new Date(Date.now() - 1000 * 60 * 92).toISOString() },
];

const EXPLOITS = [
  { id: "E-31", target: "10.0.4.5", phase: "exploitation", status: "successful" },
  { id: "E-30", target: "vpn.acme.com", phase: "delivery", status: "running" },
  { id: "E-29", target: "build-runner-04", phase: "installation", status: "successful" },
  { id: "E-28", target: "DC01.corp.local", phase: "command_control", status: "detected" },
];

export default function RedTeamPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Red Team Operations"
        description="Adversary simulation, recon and exploitation tracking."
        action={
          <Link href="/red-team/recon" className="btn-primary">
            <Map className="h-4 w-4" /> Start Recon
          </Link>
        }
      />

      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <StatCard label="Active Simulations" value={SIMULATIONS.filter((s) => s.status === "running").length} icon={Swords} />
        <StatCard label="Recon Findings" value={RECON_RESULTS.length} icon={Map} accent="warning" />
        <StatCard label="Successful Exploits" value={EXPLOITS.filter((e) => e.status === "successful").length} icon={Target} accent="critical" />
        <StatCard label="Detected" value={EXPLOITS.filter((e) => e.status === "detected").length} icon={Crosshair} accent="warning" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="panel">
          <div className="px-4 py-3 border-b border-border flex items-center justify-between">
            <h3 className="text-sm font-semibold">Attack Simulations</h3>
            <Link href="/red-team/exploits" className="text-xs text-accent hover:underline">View kill chain</Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 p-4">
            {SIMULATIONS.map((s) => (
              <div key={s.id} className="bg-bg-secondary border border-border rounded-md p-3 hover:border-border-strong transition-colors">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono text-fg-muted">{s.id}</span>
                  <StatusBadge status={s.status} />
                </div>
                <p className="text-sm font-semibold mt-2 text-fg">{s.name}</p>
                <p className="text-xs text-fg-muted mt-1">Target: {s.target}</p>
                <div className="mt-3">
                  <div className="h-1 bg-bg rounded-full overflow-hidden">
                    <div className="h-full bg-accent" style={{ width: `${s.progress}%` }} />
                  </div>
                  <p className="text-xs text-fg-muted mt-1 tabular-nums">{s.progress}%</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <div className="px-4 py-3 border-b border-border flex items-center justify-between">
            <h3 className="text-sm font-semibold">Recon Results</h3>
            <Link href="/red-team/recon" className="text-xs text-accent hover:underline">All findings</Link>
          </div>
          <ul className="divide-y divide-border-subtle">
            {RECON_RESULTS.map((r, idx) => (
              <li key={idx} className="px-4 py-3 hover:bg-panel-hover">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-mono text-fg truncate">{r.value}</p>
                    <p className="text-xs text-fg-muted mt-1 capitalize">{r.type}</p>
                  </div>
                  <span className="text-xs text-fg-muted flex-shrink-0">{formatRelative(r.discovered_at)}</span>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="panel">
        <div className="px-4 py-3 border-b border-border flex items-center justify-between">
          <h3 className="text-sm font-semibold">Exploitation Tracker</h3>
          <Link href="/red-team/exploits" className="text-xs text-accent hover:underline">Open kill chain</Link>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-bg-secondary border-b border-border">
              <tr>
                <th className="text-left px-4 py-2 text-xs uppercase text-fg-muted">ID</th>
                <th className="text-left px-4 py-2 text-xs uppercase text-fg-muted">Target</th>
                <th className="text-left px-4 py-2 text-xs uppercase text-fg-muted">Kill Chain Phase</th>
                <th className="text-left px-4 py-2 text-xs uppercase text-fg-muted">Status</th>
              </tr>
            </thead>
            <tbody>
              {EXPLOITS.map((e) => (
                <tr key={e.id} className="table-row">
                  <td className="px-4 py-3 font-mono text-xs text-accent">{e.id}</td>
                  <td className="px-4 py-3 font-mono">{e.target}</td>
                  <td className="px-4 py-3 capitalize">{e.phase.replace(/_/g, " ")}</td>
                  <td className="px-4 py-3"><StatusBadge status={e.status} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
