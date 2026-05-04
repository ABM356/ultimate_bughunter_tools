"use client";

import { useState } from "react";
import { Loader2, Map, Search } from "lucide-react";
import { PageHeader } from "@/components/PageHeader";
import { EmptyState } from "@/components/EmptyState";
import { formatRelative } from "@/lib/utils";

interface Surface {
  type: "subdomain" | "port" | "service" | "endpoint";
  value: string;
  metadata: string;
  discovered_at: string;
}

const MOCK_RESULTS: Surface[] = [
  { type: "subdomain", value: "api-staging.target.com", metadata: "A: 35.x.x.x, no WAF", discovered_at: new Date().toISOString() },
  { type: "subdomain", value: "internal.target.com", metadata: "CNAME → corp-vpn", discovered_at: new Date().toISOString() },
  { type: "port", value: "203.0.113.42:8080", metadata: "Apache Tomcat 9.0.83", discovered_at: new Date().toISOString() },
  { type: "port", value: "203.0.113.42:9200", metadata: "Elasticsearch 7.x (no auth)", discovered_at: new Date().toISOString() },
  { type: "service", value: "smtp.target.com", metadata: "Postfix, no STARTTLS", discovered_at: new Date().toISOString() },
  { type: "endpoint", value: "/api/v2/admin/users", metadata: "401 (visible from /robots.txt)", discovered_at: new Date().toISOString() },
];

export default function ReconPage() {
  const [target, setTarget] = useState("");
  const [running, setRunning] = useState(false);
  const [results, setResults] = useState<Surface[]>([]);

  const handleStart = async () => {
    if (!target.trim()) return;
    setRunning(true);
    setResults([]);
    setTimeout(() => {
      setResults(MOCK_RESULTS);
      setRunning(false);
    }, 1200);
  };

  const grouped: Record<string, Surface[]> = {};
  for (const r of results) {
    grouped[r.type] = grouped[r.type] || [];
    grouped[r.type].push(r);
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Reconnaissance"
        description="Map the attack surface — subdomains, ports, services, endpoints."
        breadcrumbs={[{ label: "Red Team", href: "/red-team" }, { label: "Recon" }]}
      />

      <div className="panel p-4">
        <label className="label">Target</label>
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="example.com or 10.0.0.0/24"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            className="input flex-1"
          />
          <button type="button" onClick={handleStart} disabled={running || !target} className="btn-primary">
            {running ? <Loader2 className="h-4 w-4 animate-spin" /> : <Search className="h-4 w-4" />}
            {running ? "Scanning" : "Start Recon"}
          </button>
        </div>
      </div>

      {results.length === 0 && !running && (
        <EmptyState icon={Map} title="No surface mapped yet" description="Enter a target and start reconnaissance to see results here." />
      )}

      {results.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Object.entries(grouped).map(([type, items]) => (
            <div key={type} className="panel">
              <div className="px-4 py-3 border-b border-border flex items-center justify-between">
                <h3 className="text-sm font-semibold capitalize">{type}s</h3>
                <span className="text-xs text-fg-muted">{items.length}</span>
              </div>
              <ul className="divide-y divide-border-subtle">
                {items.map((item, idx) => (
                  <li key={idx} className="px-4 py-3">
                    <p className="text-sm font-mono text-fg break-all">{item.value}</p>
                    <p className="text-xs text-fg-muted mt-1">{item.metadata}</p>
                    <p className="text-[10px] text-fg-subtle mt-1">{formatRelative(item.discovered_at)}</p>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
