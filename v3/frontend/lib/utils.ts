import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import type { Severity } from "./types";

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

export function formatDate(date: string | Date | undefined): string {
  if (!date) return "-";
  const d = typeof date === "string" ? new Date(date) : date;
  if (Number.isNaN(d.getTime())) return "-";
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(d);
}

export function formatDateTime(date: string | Date | undefined): string {
  if (!date) return "-";
  const d = typeof date === "string" ? new Date(date) : date;
  if (Number.isNaN(d.getTime())) return "-";
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(d);
}

export function formatRelative(date: string | Date | undefined): string {
  if (!date) return "-";
  const d = typeof date === "string" ? new Date(date) : date;
  if (Number.isNaN(d.getTime())) return "-";
  const seconds = Math.floor((Date.now() - d.getTime()) / 1000);
  if (seconds < 60) return `${seconds}s ago`;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  if (days < 7) return `${days}d ago`;
  return formatDate(d);
}

export function formatCurrency(amount: number, currency = "USD"): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

export function formatNumber(value: number): string {
  return new Intl.NumberFormat("en-US").format(value);
}

export function formatBytes(bytes: number): string {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB", "TB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
}

export function severityColor(severity: Severity): string {
  const map: Record<Severity, string> = {
    critical: "text-sev-critical",
    high: "text-sev-high",
    medium: "text-sev-medium",
    low: "text-sev-low",
    info: "text-sev-info",
  };
  return map[severity];
}

export function severityBg(severity: Severity): string {
  const map: Record<Severity, string> = {
    critical: "bg-sev-critical/10 text-sev-critical border-sev-critical/30",
    high: "bg-sev-high/10 text-sev-high border-sev-high/30",
    medium: "bg-sev-medium/10 text-sev-medium border-sev-medium/30",
    low: "bg-sev-low/10 text-sev-low border-sev-low/30",
    info: "bg-sev-info/10 text-sev-info border-sev-info/30",
  };
  return map[severity];
}

export function severityWeight(severity: Severity): number {
  const map: Record<Severity, number> = {
    critical: 5,
    high: 4,
    medium: 3,
    low: 2,
    info: 1,
  };
  return map[severity];
}

export function statusColor(status: string): string {
  const colors: Record<string, string> = {
    completed: "bg-sev-info/10 text-sev-info border-sev-info/30",
    running: "bg-accent/10 text-accent border-accent/30",
    queued: "bg-sev-low/10 text-sev-low border-sev-low/30",
    pending: "bg-fg-muted/10 text-fg-muted border-fg-muted/30",
    failed: "bg-sev-critical/10 text-sev-critical border-sev-critical/30",
    cancelled: "bg-fg-subtle/10 text-fg-subtle border-fg-subtle/30",
    new: "bg-sev-medium/10 text-sev-medium border-sev-medium/30",
    acknowledged: "bg-sev-low/10 text-sev-low border-sev-low/30",
    investigating: "bg-accent/10 text-accent border-accent/30",
    resolved: "bg-sev-info/10 text-sev-info border-sev-info/30",
    false_positive: "bg-fg-subtle/10 text-fg-subtle border-fg-subtle/30",
    submitted: "bg-sev-medium/10 text-sev-medium border-sev-medium/30",
    triaging: "bg-accent/10 text-accent border-accent/30",
    accepted: "bg-sev-low/10 text-sev-low border-sev-low/30",
    fixed: "bg-sev-info/10 text-sev-info border-sev-info/30",
    paid: "bg-sev-info/10 text-sev-info border-sev-info/30",
    rejected: "bg-sev-critical/10 text-sev-critical border-sev-critical/30",
    duplicate: "bg-fg-subtle/10 text-fg-subtle border-fg-subtle/30",
  };
  return colors[status] || "bg-fg-muted/10 text-fg-muted border-fg-muted/30";
}

export function truncate(str: string, len = 64): string {
  if (str.length <= len) return str;
  return `${str.slice(0, len)}...`;
}

export function pluralize(count: number, singular: string, plural?: string): string {
  if (count === 1) return `${count} ${singular}`;
  return `${count} ${plural || `${singular}s`}`;
}

export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}
