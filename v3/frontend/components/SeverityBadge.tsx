import { cn, severityBg } from "@/lib/utils";
import type { Severity } from "@/lib/types";

interface SeverityBadgeProps {
  severity: Severity;
  className?: string;
  size?: "sm" | "md";
}

export function SeverityBadge({ severity, className, size = "sm" }: SeverityBadgeProps) {
  const sizeClasses = size === "sm" ? "px-2 py-0.5 text-[10px]" : "px-2.5 py-1 text-xs";
  return (
    <span
      className={cn(
        "inline-flex items-center font-semibold uppercase tracking-wide rounded border",
        sizeClasses,
        severityBg(severity),
        className,
      )}
    >
      {severity}
    </span>
  );
}
