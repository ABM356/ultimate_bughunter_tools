"use client";

import Link from "next/link";
import { Bug, CheckCircle, DollarSign, FileText, Plus } from "lucide-react";
import { PageHeader } from "@/components/PageHeader";
import { StatCard } from "@/components/StatCard";
import { formatCurrency, formatNumber } from "@/lib/utils";

const PROGRAMS = [
  {
    id: "p-1",
    name: "HopeUp Public",
    status: "active",
    submissions: 218,
    triaged: 162,
    paid: 84,
    payout: 142500,
    bounty_range: "$50 — $25,000",
  },
  {
    id: "p-2",
    name: "Acme Bank Production",
    status: "active",
    submissions: 96,
    triaged: 71,
    paid: 32,
    payout: 78400,
    bounty_range: "$100 — $40,000",
  },
  {
    id: "p-3",
    name: "Northwind Internal API",
    status: "private",
    submissions: 41,
    triaged: 38,
    paid: 19,
    payout: 26900,
    bounty_range: "$75 — $15,000",
  },
];

export default function BugBountyPage() {
  const totals = PROGRAMS.reduce(
    (acc, p) => ({
      submissions: acc.submissions + p.submissions,
      triaged: acc.triaged + p.triaged,
      paid: acc.paid + p.paid,
      payout: acc.payout + p.payout,
    }),
    { submissions: 0, triaged: 0, paid: 0, payout: 0 },
  );

  return (
    <div className="space-y-6">
      <PageHeader
        title="Bug Bounty"
        description="Manage public and private vulnerability disclosure programs."
        action={
          <Link href="/bug-bounty/submissions/new" className="btn-primary">
            <Plus className="h-4 w-4" /> New Submission
          </Link>
        }
      />

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Total Submissions" value={formatNumber(totals.submissions)} icon={FileText} />
        <StatCard label="Triaged" value={formatNumber(totals.triaged)} icon={CheckCircle} accent="warning" />
        <StatCard label="Paid Out" value={formatNumber(totals.paid)} icon={Bug} accent="success" />
        <StatCard label="Total Payout" value={formatCurrency(totals.payout)} icon={DollarSign} accent="success" />
      </div>

      <div className="panel">
        <div className="px-4 py-3 border-b border-border">
          <h3 className="text-sm font-semibold">Programs</h3>
        </div>
        <div className="divide-y divide-border-subtle">
          {PROGRAMS.map((p) => (
            <Link
              key={p.id}
              href={`/bug-bounty/programs/${p.id}`}
              className="block px-4 py-4 hover:bg-panel-hover transition-colors"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <h4 className="text-base font-semibold text-fg">{p.name}</h4>
                    <span
                      className={`text-[10px] px-2 py-0.5 rounded border uppercase ${
                        p.status === "active"
                          ? "bg-sev-info/10 text-sev-info border-sev-info/30"
                          : "bg-fg-muted/10 text-fg-muted border-fg-muted/30"
                      }`}
                    >
                      {p.status}
                    </span>
                  </div>
                  <p className="text-xs text-fg-muted mt-1">Bounty range: {p.bounty_range}</p>
                </div>
                <div className="grid grid-cols-4 gap-6 text-center">
                  <div>
                    <p className="text-xs text-fg-muted">Subs</p>
                    <p className="text-lg font-bold text-fg tabular-nums">
                      {formatNumber(p.submissions)}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-fg-muted">Triaged</p>
                    <p className="text-lg font-bold text-fg tabular-nums">
                      {formatNumber(p.triaged)}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-fg-muted">Paid</p>
                    <p className="text-lg font-bold text-sev-info tabular-nums">
                      {formatNumber(p.paid)}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-fg-muted">Payout</p>
                    <p className="text-lg font-bold text-accent tabular-nums">
                      {formatCurrency(p.payout)}
                    </p>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
