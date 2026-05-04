"use client";

import { useState } from "react";
import { Calendar, Loader2, Search } from "lucide-react";
import { PageHeader } from "@/components/PageHeader";
import { cn } from "@/lib/utils";

interface LogRow {
  id: string;
  timestamp: string;
  source: string;
  level: "debug" | "info" | "warn" | "error" | "critical";
  message: string;
}

const SAMPLE_LOGS: LogRow[] = [
  { id: "1", timestamp: "2026-05-04T13:04:18Z", source: "auth.ssh", level: "warn", message: "Failed password for root from 5.42.196.18 port 41152" },
  { id: "2", timestamp: "2026-05-04T13:04:11Z", source: "nginx.access", level: "info", message: 'GET /api/v1/users 200 12ms ip=10.0.4.17' },
  { id: "3", timestamp: "2026-05-04T13:03:58Z", source: "edr.crowdstrike", level: "error", message: "Encoded PowerShell payload blocked on WIN-DBSRV-04" },
  { id: "4", timestamp: "2026-05-04T13:03:42Z", source: "aws.cloudtrail", level: "critical", message: 'PutBucketAcl AllUsers:READ on s3://marketing-assets' },
  { id: "5", timestamp: "2026-05-04T13:03:21Z", source: "iam.okta", level: "info", message: "User jane@hopeup.io logged in via SSO" },
  { id: "6", timestamp: "2026-05-04T13:02:55Z", source: "k8s.audit", level: "warn", message: "exec into pod kube-system/coredns by user dev-engineer" },
];

const LEVELS = ["debug", "info", "warn", "error", "critical"];

export default function LogsPage() {
  const [query, setQuery] = useState('source:"edr.*" AND level:error');
  const [timeRange, setTimeRange] = useState("15m");
  const [levelFilter, setLevelFilter] = useState<string>("");
  const [searching, setSearching] = useState(false);
  const [results, setResults] = useState<LogRow[]>(SAMPLE_LOGS);

  const handleSearch = () => {
    setSearching(true);
    setTimeout(() => {
      const filtered = SAMPLE_LOGS.filter((row) =>
        levelFilter ? row.level === levelFilter : true,
      );
      setResults(filtered);
      setSearching(false);
    }, 600);
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Log Search"
        description="Query across all collected sources"
        breadcrumbs={[{ label: "Blue Team", href: "/blue-team" }, { label: "Logs" }]}
      />

      <div className="panel p-4 space-y-3">
        <div className="flex items-center gap-2">
          <Search className="h-4 w-4 text-fg-muted" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            placeholder='source:"auth.*" AND level:warn'
            className="input flex-1 font-mono"
          />
          <button type="button" onClick={handleSearch} className="btn-primary" disabled={searching}>
            {searching ? <Loader2 className="h-4 w-4 animate-spin" /> : "Search"}
          </button>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2 text-xs text-fg-muted">
            <Calendar className="h-3.5 w-3.5" />
            <span>Time range</span>
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="input py-1 text-xs"
            >
              <option value="5m">Last 5 min</option>
              <option value="15m">Last 15 min</option>
              <option value="1h">Last 1 hour</option>
              <option value="24h">Last 24 hours</option>
              <option value="7d">Last 7 days</option>
            </select>
          </div>
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-xs text-fg-muted">Level:</span>
            <button
              type="button"
              onClick={() => setLevelFilter("")}
              className={cn(
                "px-2 py-0.5 text-[10px] rounded border uppercase",
                !levelFilter
                  ? "bg-accent text-bg border-accent"
                  : "border-border text-fg-muted hover:border-border-strong",
              )}
            >
              All
            </button>
            {LEVELS.map((l) => (
              <button
                key={l}
                type="button"
                onClick={() => setLevelFilter(l)}
                className={cn(
                  "px-2 py-0.5 text-[10px] rounded border uppercase",
                  levelFilter === l
                    ? "bg-accent text-bg border-accent"
                    : "border-border text-fg-muted hover:border-border-strong",
                )}
              >
                {l}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="panel">
        <div className="px-4 py-2 border-b border-border flex items-center justify-between text-xs text-fg-muted">
          <span>{results.length} events</span>
          <span>auto-refresh off</span>
        </div>
        <div className="font-mono text-xs">
          {results.map((row) => (
            <div
              key={row.id}
              className="px-4 py-2 border-b border-border-subtle hover:bg-panel-hover flex gap-4 items-start"
            >
              <span className="text-fg-subtle whitespace-nowrap">{row.timestamp}</span>
              <span
                className={cn(
                  "uppercase font-bold w-16 flex-shrink-0",
                  row.level === "critical" && "text-sev-critical",
                  row.level === "error" && "text-sev-high",
                  row.level === "warn" && "text-sev-medium",
                  row.level === "info" && "text-sev-info",
                  row.level === "debug" && "text-fg-subtle",
                )}
              >
                {row.level}
              </span>
              <span className="text-accent w-32 flex-shrink-0 truncate">{row.source}</span>
              <span className="text-fg flex-1 break-all">{row.message}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
