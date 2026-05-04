"use client";

import { Activity, AlertTriangle, ShieldCheck, Timer } from "lucide-react";
import { PageHeader } from "@/components/PageHeader";
import { StatCard } from "@/components/StatCard";
import { AlertFeed } from "@/components/AlertFeed";
import { cn } from "@/lib/utils";

const HEAT_MAP_HOURS = Array.from({ length: 24 }, (_, i) => i);
const HEAT_MAP_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

function intensity(d: number, h: number): number {
  const seed = (d * 31 + h * 17) % 100;
  return seed / 100;
}

function severityForIntensity(value: number): string {
  if (value > 0.85) return "bg-sev-critical";
  if (value > 0.7) return "bg-sev-high";
  if (value > 0.5) return "bg-sev-medium";
  if (value > 0.3) return "bg-sev-low";
  if (value > 0.1) return "bg-sev-info/40";
  return "bg-bg-secondary";
}

export default function BlueTeamPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Blue Team SOC"
        description="Real-time detections, incident response, threat intel."
      />

      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <StatCard label="Active Alerts" value={128} icon={AlertTriangle} accent="warning" />
        <StatCard label="Open Incidents" value={6} icon={Activity} accent="critical" />
        <StatCard label="MTTR (avg)" value="42m" icon={Timer} />
        <StatCard label="Detections (24h)" value={3214} icon={ShieldCheck} accent="success" />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
        <div className="xl:col-span-2 panel">
          <div className="px-4 py-3 border-b border-border flex items-center justify-between">
            <h3 className="text-sm font-semibold">Severity Heat Map</h3>
            <span className="text-xs text-fg-muted">7 days, hourly</span>
          </div>
          <div className="p-4 overflow-x-auto">
            <div className="min-w-[680px]">
              <div className="grid grid-cols-[60px_repeat(24,1fr)] gap-0.5">
                <div></div>
                {HEAT_MAP_HOURS.map((h) => (
                  <div key={h} className="text-[9px] text-fg-subtle text-center">
                    {h % 6 === 0 ? `${h}h` : ""}
                  </div>
                ))}
                {HEAT_MAP_DAYS.map((day, dIdx) => (
                  <div key={day} className="contents">
                    <div className="text-xs text-fg-muted py-1">{day}</div>
                    {HEAT_MAP_HOURS.map((h) => {
                      const v = intensity(dIdx, h);
                      return (
                        <div
                          key={`${day}-${h}`}
                          className={cn("aspect-square rounded-sm", severityForIntensity(v))}
                          title={`${day} ${h}h - ${Math.round(v * 100)}%`}
                        />
                      );
                    })}
                  </div>
                ))}
              </div>
              <div className="flex items-center justify-end gap-2 mt-3 text-[10px] text-fg-muted">
                <span>Less</span>
                <div className="h-2 w-3 rounded-sm bg-bg-secondary" />
                <div className="h-2 w-3 rounded-sm bg-sev-info/40" />
                <div className="h-2 w-3 rounded-sm bg-sev-low" />
                <div className="h-2 w-3 rounded-sm bg-sev-medium" />
                <div className="h-2 w-3 rounded-sm bg-sev-high" />
                <div className="h-2 w-3 rounded-sm bg-sev-critical" />
                <span>More</span>
              </div>
            </div>
          </div>

          <div className="border-t border-border px-4 py-3">
            <h4 className="text-sm font-semibold mb-3">MTTR by Severity</h4>
            <div className="space-y-2">
              {[
                { label: "Critical", time: "12m", pct: 100, color: "bg-sev-critical" },
                { label: "High", time: "34m", pct: 72, color: "bg-sev-high" },
                { label: "Medium", time: "1h 18m", pct: 48, color: "bg-sev-medium" },
                { label: "Low", time: "4h 22m", pct: 24, color: "bg-sev-low" },
              ].map((row) => (
                <div key={row.label} className="flex items-center gap-3">
                  <span className="text-xs text-fg-muted w-16">{row.label}</span>
                  <div className="flex-1 h-1.5 bg-bg-secondary rounded-full overflow-hidden">
                    <div className={cn("h-full", row.color)} style={{ width: `${row.pct}%` }} />
                  </div>
                  <span className="text-xs font-mono text-fg-muted w-16 text-right">{row.time}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <AlertFeed maxAlerts={20} />
      </div>
    </div>
  );
}
