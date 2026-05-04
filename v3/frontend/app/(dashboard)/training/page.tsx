"use client";

import Link from "next/link";
import { Bug, ShieldCheck, Swords } from "lucide-react";
import { PageHeader } from "@/components/PageHeader";
import { cn } from "@/lib/utils";

const TRACKS = [
  {
    code: "BB",
    name: "Bug Bounty",
    icon: Bug,
    description: "From recon to PoCs, real-world bug hunting playbooks",
    progress: 45,
    color: "text-sev-medium border-sev-medium/30",
    modules: [
      { code: "BB-L0", name: "Bug Bounty Foundations", level: "L0", duration: 4, completed: true, progress: 100 },
      { code: "BB-L1", name: "Web Recon Mastery", level: "L1", duration: 6, completed: true, progress: 100 },
      { code: "BB-L2", name: "Auth & Access Control Bugs", level: "L2", duration: 8, completed: false, progress: 60 },
      { code: "BB-L3", name: "Server-side Request Forgery", level: "L3", duration: 10, completed: false, progress: 0 },
      { code: "BB-L4", name: "Advanced Chained Exploits", level: "L4", duration: 14, completed: false, progress: 0 },
    ],
  },
  {
    code: "RT",
    name: "Red Team",
    icon: Swords,
    description: "Adversary simulation, lateral movement, persistence",
    progress: 22,
    color: "text-sev-critical border-sev-critical/30",
    modules: [
      { code: "RT-L0", name: "Red Team Foundations", level: "L0", duration: 4, completed: true, progress: 100 },
      { code: "RT-L1", name: "Initial Access Tradecraft", level: "L1", duration: 6, completed: false, progress: 50 },
      { code: "RT-L2", name: "Active Directory Attacks", level: "L2", duration: 8, completed: false, progress: 0 },
      { code: "RT-L3", name: "C2 Frameworks", level: "L3", duration: 10, completed: false, progress: 0 },
      { code: "RT-L4", name: "Operational Security & Evasion", level: "L4", duration: 14, completed: false, progress: 0 },
    ],
  },
  {
    code: "BT",
    name: "Blue Team",
    icon: ShieldCheck,
    description: "Detection engineering, IR, threat intel",
    progress: 68,
    color: "text-sev-info border-sev-info/30",
    modules: [
      { code: "BT-L0", name: "SOC Foundations", level: "L0", duration: 4, completed: true, progress: 100 },
      { code: "BT-L1", name: "Detection Engineering", level: "L1", duration: 6, completed: true, progress: 100 },
      { code: "BT-L2", name: "Incident Response Workflow", level: "L2", duration: 8, completed: true, progress: 100 },
      { code: "BT-L3", name: "Threat Hunting", level: "L3", duration: 10, completed: false, progress: 40 },
      { code: "BT-L4", name: "Adversary Emulation Defense", level: "L4", duration: 14, completed: false, progress: 0 },
    ],
  },
];

export default function TrainingPage() {
  return (
    <div className="space-y-6">
      <PageHeader title="Training" description="Skill up across offensive and defensive tracks" />

      {TRACKS.map((track) => {
        const Icon = track.icon;
        return (
          <div key={track.code} className="panel">
            <div className="px-4 py-4 border-b border-border flex items-start justify-between gap-4">
              <div className="flex items-start gap-3">
                <span className={cn("p-2 rounded-md border", track.color, "bg-bg-secondary")}>
                  <Icon className="h-5 w-5" />
                </span>
                <div>
                  <h3 className="text-base font-semibold">{track.name}</h3>
                  <p className="text-xs text-fg-muted">{track.description}</p>
                </div>
              </div>
              <div className="text-right min-w-[180px]">
                <p className="text-xs text-fg-muted mb-1">{track.progress}% complete</p>
                <div className="h-1.5 bg-bg-secondary rounded-full overflow-hidden">
                  <div className="h-full bg-accent" style={{ width: `${track.progress}%` }} />
                </div>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 p-4">
              {track.modules.map((m) => (
                <Link
                  key={m.code}
                  href={`/training/${m.code}`}
                  className={cn(
                    "block bg-bg-secondary border rounded-md p-3 hover:border-accent/40 transition-colors",
                    m.completed ? "border-sev-info/30" : "border-border",
                  )}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-mono text-fg-muted">{m.code}</span>
                    <span className="text-[10px] uppercase font-bold text-accent">{m.level}</span>
                  </div>
                  <p className="text-sm font-semibold">{m.name}</p>
                  <p className="text-xs text-fg-muted mt-1">{m.duration}h</p>
                  <div className="mt-3 h-1 bg-bg rounded-full overflow-hidden">
                    <div
                      className={cn("h-full", m.completed ? "bg-sev-info" : "bg-accent")}
                      style={{ width: `${m.progress}%` }}
                    />
                  </div>
                </Link>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}
