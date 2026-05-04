"use client";

import { Activity, Wifi, WifiOff } from "lucide-react";
import Link from "next/link";
import { useLiveAlerts } from "@/lib/hooks/useAlerts";
import { formatRelative } from "@/lib/utils";
import { SeverityBadge } from "./SeverityBadge";
import { EmptyState } from "./EmptyState";

interface AlertFeedProps {
  maxAlerts?: number;
}

export function AlertFeed({ maxAlerts = 25 }: AlertFeedProps) {
  const { alerts, connected } = useLiveAlerts(maxAlerts);

  return (
    <div className="panel">
      <div className="flex items-center justify-between px-4 py-3 border-b border-border">
        <div className="flex items-center gap-2">
          <Activity className="h-4 w-4 text-accent" />
          <h3 className="text-sm font-semibold text-fg">Live Alert Feed</h3>
        </div>
        <span className="flex items-center gap-1.5 text-xs text-fg-muted">
          {connected ? (
            <>
              <Wifi className="h-3 w-3 text-sev-info" />
              <span>Connected</span>
            </>
          ) : (
            <>
              <WifiOff className="h-3 w-3 text-fg-subtle" />
              <span>Reconnecting</span>
            </>
          )}
        </span>
      </div>
      <ul className="divide-y divide-border-subtle max-h-[480px] overflow-y-auto">
        {alerts.length === 0 ? (
          <li>
            <EmptyState
              icon={Activity}
              title="Awaiting alerts"
              description="Live security events will stream in here as they're detected."
            />
          </li>
        ) : (
          alerts.map((alert) => (
            <li key={alert.id} className="px-4 py-3 hover:bg-panel-hover transition-colors">
              <div className="flex items-start gap-3">
                <SeverityBadge severity={alert.severity} />
                <div className="flex-1 min-w-0">
                  <Link
                    href={`/blue-team/alerts?id=${alert.id}`}
                    className="text-sm text-fg hover:text-accent truncate block"
                  >
                    {alert.title}
                  </Link>
                  <div className="flex items-center gap-2 text-xs text-fg-muted mt-1">
                    <span className="font-mono">{alert.source}</span>
                    <span className="text-fg-subtle">•</span>
                    <span>{formatRelative(alert.created_at)}</span>
                  </div>
                </div>
              </div>
            </li>
          ))
        )}
      </ul>
    </div>
  );
}
