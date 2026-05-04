import type { LucideIcon } from "lucide-react";
import { ArrowDown, ArrowUp } from "lucide-react";
import { cn } from "@/lib/utils";

interface StatCardProps {
  label: string;
  value: string | number;
  icon?: LucideIcon;
  delta?: number;
  deltaLabel?: string;
  accent?: "default" | "critical" | "success" | "warning";
  className?: string;
}

export function StatCard({
  label,
  value,
  icon: Icon,
  delta,
  deltaLabel,
  accent = "default",
  className,
}: StatCardProps) {
  const accentColors: Record<string, string> = {
    default: "text-accent",
    critical: "text-sev-critical",
    success: "text-sev-info",
    warning: "text-sev-medium",
  };

  return (
    <div className={cn("panel p-5 panel-hover", className)}>
      <div className="flex items-start justify-between">
        <div className="flex-1 min-w-0">
          <p className="text-xs text-fg-muted uppercase tracking-wide font-medium">{label}</p>
          <p className="mt-2 text-3xl font-bold text-fg tabular-nums">{value}</p>
          {typeof delta === "number" && (
            <div className="mt-2 flex items-center gap-1 text-xs">
              {delta >= 0 ? (
                <ArrowUp className="h-3 w-3 text-sev-info" />
              ) : (
                <ArrowDown className="h-3 w-3 text-sev-critical" />
              )}
              <span className={delta >= 0 ? "text-sev-info" : "text-sev-critical"}>
                {Math.abs(delta)}%
              </span>
              {deltaLabel && <span className="text-fg-subtle">{deltaLabel}</span>}
            </div>
          )}
        </div>
        {Icon && (
          <div className={cn("p-2 rounded-md bg-bg-secondary", accentColors[accent])}>
            <Icon className="h-5 w-5" />
          </div>
        )}
      </div>
    </div>
  );
}
