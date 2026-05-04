"use client";

import { useState } from "react";
import { Copy, Eye, EyeOff, Key, MessageSquare, Plus, Slack, Trash2 } from "lucide-react";
import { toast } from "sonner";
import { PageHeader } from "@/components/PageHeader";
import { cn } from "@/lib/utils";

interface Integration {
  id: string;
  name: string;
  type: string;
  icon: React.ComponentType<{ className?: string }>;
  status: "connected" | "disconnected";
  description: string;
}

const INTEGRATIONS: Integration[] = [
  {
    id: "stripe",
    name: "Stripe",
    type: "billing",
    icon: () => (
      <span className="font-bold text-sm">$</span>
    ),
    status: "connected",
    description: "Payments & invoicing",
  },
  {
    id: "slack",
    name: "Slack",
    type: "notifications",
    icon: Slack,
    status: "connected",
    description: "Alerts & incident channels",
  },
  {
    id: "misp",
    name: "MISP",
    type: "threat_intel",
    icon: MessageSquare,
    status: "connected",
    description: "Threat intelligence sharing",
  },
];

interface ApiKey {
  id: string;
  name: string;
  prefix: string;
  created_at: string;
  last_used: string;
}

const INITIAL_KEYS: ApiKey[] = [
  { id: "k-1", name: "CI/CD Production", prefix: "hu_live_8a31...", created_at: "2025-12-04", last_used: "2026-05-04" },
  { id: "k-2", name: "Local development", prefix: "hu_test_4f9c...", created_at: "2026-02-19", last_used: "2026-05-03" },
];

export default function SettingsPage() {
  const [tab, setTab] = useState<"tenant" | "integrations" | "keys">("tenant");
  const [showKey, setShowKey] = useState<Record<string, boolean>>({});
  const [keys, setKeys] = useState<ApiKey[]>(INITIAL_KEYS);

  return (
    <div className="space-y-6">
      <PageHeader title="Settings" description="Tenant configuration, integrations, and API keys" />

      <div className="flex gap-1 border-b border-border overflow-x-auto">
        {[
          { id: "tenant", label: "Tenant" },
          { id: "integrations", label: "Integrations" },
          { id: "keys", label: "API Keys" },
        ].map((t) => (
          <button
            key={t.id}
            type="button"
            onClick={() => setTab(t.id as typeof tab)}
            className={cn(
              "px-4 py-2 text-sm border-b-2 transition-colors whitespace-nowrap",
              tab === t.id
                ? "border-accent text-accent"
                : "border-transparent text-fg-muted hover:text-fg",
            )}
          >
            {t.label}
          </button>
        ))}
      </div>

      {tab === "tenant" && (
        <div className="panel p-4 space-y-4">
          <div>
            <label className="label">Tenant Name</label>
            <input type="text" defaultValue="HopeUp Internal" className="input" />
          </div>
          <div>
            <label className="label">Slug</label>
            <input type="text" defaultValue="hopeup" className="input font-mono" />
          </div>
          <div>
            <label className="label">Tier</label>
            <select className="input" defaultValue="enterprise">
              <option value="starter">Starter</option>
              <option value="pro">Pro</option>
              <option value="enterprise">Enterprise</option>
            </select>
          </div>
          <div>
            <label className="label">Default Time Zone</label>
            <select className="input" defaultValue="UTC">
              <option value="UTC">UTC</option>
              <option value="America/Los_Angeles">America/Los_Angeles</option>
              <option value="America/New_York">America/New_York</option>
              <option value="Europe/London">Europe/London</option>
            </select>
          </div>
          <div className="flex justify-end">
            <button
              type="button"
              onClick={() => toast.success("Settings saved")}
              className="btn-primary"
            >
              Save Changes
            </button>
          </div>
        </div>
      )}

      {tab === "integrations" && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {INTEGRATIONS.map((i) => {
            const Icon = i.icon;
            return (
              <div key={i.id} className="panel p-4">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <span className="h-9 w-9 rounded-md bg-bg-secondary border border-border flex items-center justify-center text-accent">
                      <Icon className="h-5 w-5" />
                    </span>
                    <div>
                      <p className="text-sm font-semibold">{i.name}</p>
                      <p className="text-xs text-fg-muted capitalize">{i.type.replace(/_/g, " ")}</p>
                    </div>
                  </div>
                  <span
                    className={cn(
                      "h-2 w-2 rounded-full mt-2",
                      i.status === "connected" ? "bg-sev-info animate-pulse" : "bg-fg-subtle",
                    )}
                  />
                </div>
                <p className="text-xs text-fg-muted mb-3">{i.description}</p>
                <button
                  type="button"
                  onClick={() => toast(`${i.status === "connected" ? "Disconnecting" : "Connecting"} ${i.name}`)}
                  className={cn(
                    "btn w-full",
                    i.status === "connected"
                      ? "bg-panel-hover border border-border text-fg hover:border-sev-critical/40 hover:text-sev-critical"
                      : "btn-primary",
                  )}
                >
                  {i.status === "connected" ? "Disconnect" : "Connect"}
                </button>
              </div>
            );
          })}
        </div>
      )}

      {tab === "keys" && (
        <div className="space-y-4">
          <div className="panel">
            <div className="px-4 py-3 border-b border-border flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Key className="h-4 w-4 text-accent" />
                <h3 className="text-sm font-semibold">API Keys</h3>
              </div>
              <button
                type="button"
                onClick={() => {
                  const newKey: ApiKey = {
                    id: `k-${Math.floor(Math.random() * 1000)}`,
                    name: "New Key",
                    prefix: `hu_live_${Math.random().toString(36).slice(2, 10)}...`,
                    created_at: new Date().toISOString().slice(0, 10),
                    last_used: "Never",
                  };
                  setKeys((prev) => [newKey, ...prev]);
                  toast.success("API key created");
                }}
                className="btn-primary"
              >
                <Plus className="h-4 w-4" /> Create Key
              </button>
            </div>
            <ul className="divide-y divide-border-subtle">
              {keys.map((k) => (
                <li key={k.id} className="px-4 py-3 flex items-center justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-semibold">{k.name}</p>
                    <p className="text-xs font-mono text-fg-muted mt-0.5">
                      {showKey[k.id] ? k.prefix.replace("...", "abcd1234efgh5678") : k.prefix}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-fg-muted">Last used: {k.last_used}</span>
                    <button
                      type="button"
                      onClick={() =>
                        setShowKey((prev) => ({ ...prev, [k.id]: !prev[k.id] }))
                      }
                      className="p-1.5 rounded hover:bg-panel-hover text-fg-muted hover:text-fg"
                      aria-label="Toggle visibility"
                    >
                      {showKey[k.id] ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        if (typeof navigator !== "undefined") {
                          navigator.clipboard.writeText(k.prefix);
                        }
                        toast.success("Key copied");
                      }}
                      className="p-1.5 rounded hover:bg-panel-hover text-fg-muted hover:text-fg"
                      aria-label="Copy"
                    >
                      <Copy className="h-4 w-4" />
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setKeys((prev) => prev.filter((x) => x.id !== k.id));
                        toast("Key revoked");
                      }}
                      className="p-1.5 rounded hover:bg-panel-hover text-fg-muted hover:text-sev-critical"
                      aria-label="Revoke"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
