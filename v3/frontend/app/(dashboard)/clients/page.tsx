"use client";

import { Building2, Plus, Users } from "lucide-react";
import { toast } from "sonner";
import { PageHeader } from "@/components/PageHeader";
import { DataTable, type Column } from "@/components/DataTable";
import { formatDate, formatNumber } from "@/lib/utils";
import { cn } from "@/lib/utils";
import type { Tenant } from "@/lib/types";

const TENANTS: Tenant[] = [
  { id: "t-1", name: "HopeUp Internal", slug: "hopeup", tier: "enterprise", created_at: "2024-01-15", user_count: 42, active: true },
  { id: "t-2", name: "Acme Bank", slug: "acme", tier: "enterprise", created_at: "2024-04-08", user_count: 18, active: true },
  { id: "t-3", name: "Northwind Logistics", slug: "northwind", tier: "pro", created_at: "2025-01-22", user_count: 9, active: true },
  { id: "t-4", name: "Globex Corp", slug: "globex", tier: "pro", created_at: "2025-08-30", user_count: 6, active: true },
  { id: "t-5", name: "Initech (trial)", slug: "initech", tier: "starter", created_at: "2026-04-12", user_count: 3, active: true },
  { id: "t-6", name: "Pied Piper", slug: "piedpiper", tier: "pro", created_at: "2025-09-10", user_count: 12, active: false },
];

export default function ClientsPage() {
  const columns: Column<Tenant>[] = [
    {
      key: "name",
      header: "Tenant",
      render: (r) => (
        <div className="flex items-center gap-2">
          <span className="h-7 w-7 rounded bg-accent/10 text-accent flex items-center justify-center">
            <Building2 className="h-3.5 w-3.5" />
          </span>
          <div>
            <p className="text-sm font-semibold">{r.name}</p>
            <p className="text-xs text-fg-muted font-mono">{r.slug}</p>
          </div>
        </div>
      ),
      sortable: true,
    },
    {
      key: "tier",
      header: "Tier",
      render: (r) => (
        <span
          className={cn(
            "inline-block px-2 py-0.5 rounded border text-[10px] uppercase",
            r.tier === "enterprise" && "bg-accent/10 text-accent border-accent/30",
            r.tier === "pro" && "bg-sev-low/10 text-sev-low border-sev-low/30",
            r.tier === "starter" && "bg-fg-muted/10 text-fg-muted border-fg-muted/30",
          )}
        >
          {r.tier}
        </span>
      ),
      sortable: true,
    },
    {
      key: "user_count",
      header: "Users",
      render: (r) => (
        <span className="inline-flex items-center gap-1 text-fg-muted">
          <Users className="h-3 w-3" />
          {formatNumber(r.user_count)}
        </span>
      ),
      sortable: true,
    },
    {
      key: "created_at",
      header: "Created",
      render: (r) => <span className="text-xs text-fg-muted">{formatDate(r.created_at)}</span>,
      sortable: true,
    },
    {
      key: "active",
      header: "Status",
      render: (r) => (
        <span
          className={cn(
            "inline-block px-2 py-0.5 rounded border text-[10px] uppercase",
            r.active
              ? "bg-sev-info/10 text-sev-info border-sev-info/30"
              : "bg-fg-muted/10 text-fg-muted border-fg-muted/30",
          )}
        >
          {r.active ? "Active" : "Inactive"}
        </span>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <PageHeader
        title="Clients"
        description="Multi-tenant administration"
        action={
          <button type="button" onClick={() => toast("Creating tenant...")} className="btn-primary">
            <Plus className="h-4 w-4" /> New Tenant
          </button>
        }
      />

      <DataTable<Tenant> columns={columns} data={TENANTS} rowKey={(r) => r.id} />
    </div>
  );
}
