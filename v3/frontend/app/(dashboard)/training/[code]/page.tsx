"use client";

import { CheckCircle2, FlaskConical, Play } from "lucide-react";
import { toast } from "sonner";
import { PageHeader } from "@/components/PageHeader";
import { cn } from "@/lib/utils";

const MODULE = {
  code: "BB-L2",
  name: "Auth & Access Control Bugs",
  level: "L2",
  duration_hours: 8,
  description: "Master authentication and authorization flaws — IDOR, broken access control, JWT issues, OAuth misconfigurations.",
  topics: [
    "JWT vulnerabilities (alg=none, key confusion)",
    "Insecure direct object references (IDOR)",
    "Broken access control patterns",
    "OAuth 2.0 redirect URI validation",
    "Privilege escalation chains",
    "Session fixation and token theft",
  ],
  labs: [
    { id: "lab-1", name: "JWT alg=none bypass", difficulty: "easy", estimated_minutes: 30, completed: true },
    { id: "lab-2", name: "IDOR in REST API", difficulty: "easy", estimated_minutes: 45, completed: true },
    { id: "lab-3", name: "OAuth open redirect chain", difficulty: "medium", estimated_minutes: 60, completed: false },
    { id: "lab-4", name: "Privilege escalation via mass assignment", difficulty: "medium", estimated_minutes: 75, completed: false },
    { id: "lab-5", name: "Cross-tenant data access exploit", difficulty: "hard", estimated_minutes: 120, completed: false },
  ],
};

export default function ModuleDetailPage({ params }: { params: { code: string } }) {
  return (
    <div className="space-y-6">
      <PageHeader
        title={MODULE.name}
        description={MODULE.description}
        breadcrumbs={[
          { label: "Training", href: "/training" },
          { label: params.code },
        ]}
      />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="panel p-4">
          <p className="label">Module</p>
          <p className="text-sm font-mono">{MODULE.code}</p>
        </div>
        <div className="panel p-4">
          <p className="label">Level</p>
          <p className="text-sm font-bold text-accent">{MODULE.level}</p>
        </div>
        <div className="panel p-4">
          <p className="label">Duration</p>
          <p className="text-sm">{MODULE.duration_hours} hours</p>
        </div>
      </div>

      <div className="panel">
        <div className="px-4 py-3 border-b border-border">
          <h3 className="text-sm font-semibold">Topics</h3>
        </div>
        <ul className="divide-y divide-border-subtle">
          {MODULE.topics.map((topic, idx) => (
            <li key={idx} className="px-4 py-3 flex items-center gap-2">
              <span className="text-xs font-mono text-fg-subtle w-6">{String(idx + 1).padStart(2, "0")}</span>
              <span className="text-sm">{topic}</span>
            </li>
          ))}
        </ul>
      </div>

      <div className="panel">
        <div className="px-4 py-3 border-b border-border flex items-center justify-between">
          <h3 className="text-sm font-semibold">Labs</h3>
          <span className="text-xs text-fg-muted">
            {MODULE.labs.filter((l) => l.completed).length}/{MODULE.labs.length} complete
          </span>
        </div>
        <ul className="divide-y divide-border-subtle">
          {MODULE.labs.map((lab) => (
            <li key={lab.id} className="px-4 py-3 flex items-center justify-between gap-3">
              <div className="flex items-center gap-3 flex-1 min-w-0">
                <FlaskConical
                  className={cn("h-4 w-4 flex-shrink-0", lab.completed ? "text-sev-info" : "text-fg-muted")}
                />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold">{lab.name}</p>
                  <p className="text-xs text-fg-muted mt-0.5">
                    <span
                      className={cn(
                        "uppercase tracking-wide font-medium",
                        lab.difficulty === "easy" && "text-sev-info",
                        lab.difficulty === "medium" && "text-sev-medium",
                        lab.difficulty === "hard" && "text-sev-critical",
                      )}
                    >
                      {lab.difficulty}
                    </span>
                    {" · "}
                    {lab.estimated_minutes} min
                  </p>
                </div>
              </div>
              {lab.completed ? (
                <span className="inline-flex items-center gap-1.5 text-xs text-sev-info">
                  <CheckCircle2 className="h-4 w-4" />
                  Complete
                </span>
              ) : (
                <button
                  type="button"
                  onClick={() => toast.success(`Launching ${lab.name}`)}
                  className="btn-primary"
                >
                  <Play className="h-4 w-4" /> Start Lab
                </button>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
