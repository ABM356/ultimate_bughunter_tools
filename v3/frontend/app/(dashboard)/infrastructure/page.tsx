"use client";

import { useState } from "react";
import { Camera, Globe, MonitorSmartphone, Plus, Server, Wifi } from "lucide-react";
import { PageHeader } from "@/components/PageHeader";
import { DataTable, type Column } from "@/components/DataTable";
import { formatDate } from "@/lib/utils";
import { cn } from "@/lib/utils";
import type { Asset } from "@/lib/types";

const ASSETS: Asset[] = [
  { id: "A-1", type: "domain", name: "app.hopeup.io", value: "app.hopeup.io", criticality: "critical", tags: ["production", "saas"], metadata: {}, last_scanned: new Date().toISOString(), created_at: "2024-01-15" },
  { id: "A-2", type: "domain", name: "api.hopeup.io", value: "api.hopeup.io", criticality: "critical", tags: ["production", "api"], metadata: {}, last_scanned: new Date().toISOString(), created_at: "2024-01-15" },
  { id: "A-3", type: "ip", name: "edge-lb-01", value: "203.0.113.42", criticality: "high", tags: ["edge", "lb"], metadata: {}, last_scanned: new Date().toISOString(), created_at: "2024-02-12" },
  { id: "A-4", type: "iot", name: "warehouse-thermostat-3", value: "10.4.5.42", criticality: "low", tags: ["iot", "warehouse"], metadata: { vendor: "Honeywell" }, last_scanned: new Date().toISOString(), created_at: "2024-09-21" },
  { id: "A-5", type: "cctv", name: "cam-lobby-01", value: "10.4.6.118", criticality: "medium", tags: ["physical", "lobby"], metadata: { model: "Hikvision DS-2CD" }, created_at: "2024-09-21" },
  { id: "A-6", type: "endpoint", name: "WIN-DBSRV-04", value: "10.0.4.12", criticality: "critical", tags: ["windows", "db"], metadata: { os: "Windows Server 2022" }, last_scanned: new Date().toISOString(), created_at: "2024-03-04" },
];

const TYPE_ICONS: Record<Asset["type"], React.ComponentType<{ className?: string }>> = {
  domain: Globe,
  ip: Wifi,
  iot: MonitorSmartphone,
  cctv: Camera,
  endpoint: Server,
};

export default function InfrastructurePage() {
  const [typeFilter, setTypeFilter] = useState<string>("");
  const filtered = typeFilter ? ASSETS.filter((a) => a.type === typeFilter) : ASSETS;

  const columns: Column<Asset>[] = [
    {
      key: "name",
      header: "Asset",
      render: (r) => {
        const Icon = TYPE_ICONS[r.type];
        return (
          <div className="flex items-center gap-2">
            <Icon className="h-4 w-4 text-fg-muted flex-shrink-0" />
            <div className="min-w-0">
              <p className="text-sm font-semibold truncate">{r.name}</p>
              <p className="text-xs text-fg-muted font-mono truncate">{r.value}</p>
            </div>
          </div>
        );
      },
      sortable: true,
    },
    {
      key: "type",
      header: "Type",
      render: (r) => <span className="text-xs uppercase">{r.type}</span>,
      sortable: true,
    },
    {
      key: "criticality",
      header: "Criticality",
      render: (r) => (
        <span
          className={cn(
            "inline-block px-2 py-0.5 rounded border text-[10px] uppercase",
            r.criticality === "critical" && "bg-sev-critical/10 text-sev-critical border-sev-critical/30",
            r.criticality === "high" && "bg-sev-high/10 text-sev-high border-sev-high/30",
            r.criticality === "medium" && "bg-sev-medium/10 text-sev-medium border-sev-medium/30",
            r.criticality === "low" && "bg-sev-low/10 text-sev-low border-sev-low/30",
          )}
        >
          {r.criticality}
        </span>
      ),
      sortable: true,
    },
    {
      key: "tags",
      header: "Tags",
      render: (r) => (
        <div className="flex flex-wrap gap-1">
          {r.tags.map((tag) => (
            <span
              key={tag}
              className="px-1.5 py-0.5 text-[10px] rounded bg-bg-secondary border border-border text-fg-muted"
            >
              {tag}
            </span>
          ))}
        </div>
      ),
    },
    {
      key: "last_scanned",
      header: "Last Scanned",
      render: (r) => <span className="text-xs text-fg-muted">{r.last_scanned ? formatDate(r.last_scanned) : "Never"}</span>,
      sortable: true,
    },
  ];

  const types: Asset["type"][] = ["domain", "ip", "iot", "cctv", "endpoint"];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Infrastructure"
        description="Asset inventory across the attack surface"
        action={
          <button type="button" className="btn-primary">
            <Plus className="h-4 w-4" /> Add Asset
          </button>
        }
      />

      <div className="flex flex-wrap items-center gap-2">
        <button
          type="button"
          onClick={() => setTypeFilter("")}
          className={cn(
            "px-3 py-1 text-xs rounded border uppercase",
            !typeFilter ? "bg-accent text-bg border-accent" : "border-border text-fg-muted hover:text-fg",
          )}
        >
          All ({ASSETS.length})
        </button>
        {types.map((t) => {
          const count = ASSETS.filter((a) => a.type === t).length;
          return (
            <button
              key={t}
              type="button"
              onClick={() => setTypeFilter(t)}
              className={cn(
                "px-3 py-1 text-xs rounded border uppercase",
                typeFilter === t
                  ? "bg-accent text-bg border-accent"
                  : "border-border text-fg-muted hover:text-fg",
              )}
            >
              {t} ({count})
            </button>
          );
        })}
      </div>

      <DataTable<Asset> columns={columns} data={filtered} rowKey={(r) => r.id} />
    </div>
  );
}
