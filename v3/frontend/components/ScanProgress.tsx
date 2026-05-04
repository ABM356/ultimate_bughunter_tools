"use client";

import { CheckCircle2, Loader2, XCircle } from "lucide-react";
import { cn } from "@/lib/utils";
import type { ScanStatus } from "@/lib/types";

interface ScanProgressProps {
  status: ScanStatus;
  progress: number;
  className?: string;
}

export function ScanProgress({ status, progress, className }: ScanProgressProps) {
  const pct = Math.min(100, Math.max(0, progress));
  const fillColor =
    status === "failed"
      ? "bg-sev-critical"
      : status === "completed"
        ? "bg-sev-info"
        : "bg-accent";

  return (
    <div className={cn("flex items-center gap-3", className)}>
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between mb-1">
          <span className="text-xs font-medium text-fg-muted capitalize flex items-center gap-1.5">
            {status === "running" && <Loader2 className="h-3 w-3 animate-spin text-accent" />}
            {status === "completed" && <CheckCircle2 className="h-3 w-3 text-sev-info" />}
            {status === "failed" && <XCircle className="h-3 w-3 text-sev-critical" />}
            {status}
          </span>
          <span className="text-xs font-mono text-fg-muted tabular-nums">{pct}%</span>
        </div>
        <div className="h-1.5 bg-bg-secondary rounded-full overflow-hidden">
          <div
            className={cn(
              "h-full transition-all duration-500",
              fillColor,
              status === "running" && "animate-pulse-accent",
            )}
            style={{ width: `${pct}%` }}
          />
        </div>
      </div>
    </div>
  );
}
