"use client";

import { Globe, Hash, Mail, Shield } from "lucide-react";
import { PageHeader } from "@/components/PageHeader";
import { formatRelative } from "@/lib/utils";

const FEEDS = [
  { name: "MISP - hopeup-default", count: 14_812, last_pull: new Date(Date.now() - 1000 * 60 * 5).toISOString() },
  { name: "AlienVault OTX", count: 9_402, last_pull: new Date(Date.now() - 1000 * 60 * 12).toISOString() },
  { name: "AbuseIPDB", count: 88_211, last_pull: new Date(Date.now() - 1000 * 60 * 32).toISOString() },
  { name: "VirusTotal Premium", count: 421_006, last_pull: new Date(Date.now() - 1000 * 60 * 45).toISOString() },
];

const RECENT_IOCS = [
  { type: "ip", value: "185.220.101.45", threat: "Tor exit / C2", confidence: 92, source: "MISP", first_seen: "2026-04-22" },
  { type: "domain", value: "secure-logon-update.com", threat: "Phishing kit", confidence: 88, source: "OTX", first_seen: "2026-05-01" },
  { type: "hash", value: "9b51cb04eb5...", threat: "Cobalt Strike beacon", confidence: 99, source: "VT", first_seen: "2026-04-30" },
  { type: "url", value: "https://cdn.fakejquery.io/jquery.min.js", threat: "Skimmer", confidence: 95, source: "MISP", first_seen: "2026-05-02" },
  { type: "email", value: "billing@invoice-update.io", threat: "BEC", confidence: 76, source: "OTX", first_seen: "2026-04-29" },
];

const ICONS: Record<string, React.ComponentType<{ className?: string }>> = {
  ip: Globe,
  domain: Globe,
  hash: Hash,
  url: Globe,
  email: Mail,
};

export default function ThreatIntelPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Threat Intelligence"
        description="External feeds and IOCs enriched into your detections"
        breadcrumbs={[{ label: "Blue Team", href: "/blue-team" }, { label: "Threat Intel" }]}
      />

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {FEEDS.map((feed) => (
          <div key={feed.name} className="panel p-4">
            <div className="flex items-center gap-2 mb-2">
              <Shield className="h-4 w-4 text-accent" />
              <p className="text-xs uppercase text-fg-muted font-medium tracking-wide">Feed</p>
            </div>
            <p className="text-sm font-semibold text-fg">{feed.name}</p>
            <p className="text-2xl font-bold tabular-nums mt-2">{feed.count.toLocaleString()}</p>
            <p className="text-xs text-fg-muted mt-1">Last sync: {formatRelative(feed.last_pull)}</p>
          </div>
        ))}
      </div>

      <div className="panel">
        <div className="px-4 py-3 border-b border-border">
          <h3 className="text-sm font-semibold">Recent IOCs</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-bg-secondary border-b border-border">
              <tr>
                <th className="text-left px-4 py-2 text-xs uppercase text-fg-muted">Type</th>
                <th className="text-left px-4 py-2 text-xs uppercase text-fg-muted">Indicator</th>
                <th className="text-left px-4 py-2 text-xs uppercase text-fg-muted">Threat</th>
                <th className="text-left px-4 py-2 text-xs uppercase text-fg-muted">Confidence</th>
                <th className="text-left px-4 py-2 text-xs uppercase text-fg-muted">Source</th>
                <th className="text-left px-4 py-2 text-xs uppercase text-fg-muted">First Seen</th>
              </tr>
            </thead>
            <tbody>
              {RECENT_IOCS.map((ioc, idx) => {
                const Icon = ICONS[ioc.type] || Globe;
                return (
                  <tr key={idx} className="table-row">
                    <td className="px-4 py-3">
                      <span className="inline-flex items-center gap-1.5 text-xs font-mono uppercase text-fg-muted">
                        <Icon className="h-3 w-3" />
                        {ioc.type}
                      </span>
                    </td>
                    <td className="px-4 py-3 font-mono text-xs text-accent break-all">{ioc.value}</td>
                    <td className="px-4 py-3">{ioc.threat}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <div className="h-1.5 w-16 bg-bg-secondary rounded-full overflow-hidden">
                          <div className="h-full bg-accent" style={{ width: `${ioc.confidence}%` }} />
                        </div>
                        <span className="text-xs font-mono">{ioc.confidence}%</span>
                      </div>
                    </td>
                    <td className="px-4 py-3 text-xs font-mono text-fg-muted">{ioc.source}</td>
                    <td className="px-4 py-3 text-xs text-fg-muted">{ioc.first_seen}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
