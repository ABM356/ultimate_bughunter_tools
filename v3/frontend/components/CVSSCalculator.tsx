"use client";

import { useEffect, useMemo, useState } from "react";
import { cn } from "@/lib/utils";

type MetricKey =
  | "AV"
  | "AC"
  | "PR"
  | "UI"
  | "S"
  | "C"
  | "I"
  | "A";

interface MetricOption {
  value: string;
  label: string;
  weight: number;
  weightChanged?: number;
}

const METRICS: { key: MetricKey; label: string; options: MetricOption[] }[] = [
  {
    key: "AV",
    label: "Attack Vector",
    options: [
      { value: "N", label: "Network", weight: 0.85 },
      { value: "A", label: "Adjacent", weight: 0.62 },
      { value: "L", label: "Local", weight: 0.55 },
      { value: "P", label: "Physical", weight: 0.2 },
    ],
  },
  {
    key: "AC",
    label: "Attack Complexity",
    options: [
      { value: "L", label: "Low", weight: 0.77 },
      { value: "H", label: "High", weight: 0.44 },
    ],
  },
  {
    key: "PR",
    label: "Privileges Required",
    options: [
      { value: "N", label: "None", weight: 0.85 },
      { value: "L", label: "Low", weight: 0.62, weightChanged: 0.68 },
      { value: "H", label: "High", weight: 0.27, weightChanged: 0.5 },
    ],
  },
  {
    key: "UI",
    label: "User Interaction",
    options: [
      { value: "N", label: "None", weight: 0.85 },
      { value: "R", label: "Required", weight: 0.62 },
    ],
  },
  {
    key: "S",
    label: "Scope",
    options: [
      { value: "U", label: "Unchanged", weight: 0 },
      { value: "C", label: "Changed", weight: 1 },
    ],
  },
  {
    key: "C",
    label: "Confidentiality",
    options: [
      { value: "H", label: "High", weight: 0.56 },
      { value: "L", label: "Low", weight: 0.22 },
      { value: "N", label: "None", weight: 0 },
    ],
  },
  {
    key: "I",
    label: "Integrity",
    options: [
      { value: "H", label: "High", weight: 0.56 },
      { value: "L", label: "Low", weight: 0.22 },
      { value: "N", label: "None", weight: 0 },
    ],
  },
  {
    key: "A",
    label: "Availability",
    options: [
      { value: "H", label: "High", weight: 0.56 },
      { value: "L", label: "Low", weight: 0.22 },
      { value: "N", label: "None", weight: 0 },
    ],
  },
];

interface CVSSCalculatorProps {
  value?: { vector: string; score: number };
  onChange?: (result: { vector: string; score: number; severity: string }) => void;
  className?: string;
}

const DEFAULT_SELECTION: Record<MetricKey, string> = {
  AV: "N",
  AC: "L",
  PR: "N",
  UI: "N",
  S: "U",
  C: "N",
  I: "N",
  A: "N",
};

function severityFor(score: number): string {
  if (score >= 9.0) return "Critical";
  if (score >= 7.0) return "High";
  if (score >= 4.0) return "Medium";
  if (score > 0) return "Low";
  return "None";
}

export function CVSSCalculator({ onChange, className }: CVSSCalculatorProps) {
  const [selection, setSelection] = useState<Record<MetricKey, string>>(DEFAULT_SELECTION);

  const { vector, score, severity } = useMemo(() => {
    const findOpt = (key: MetricKey, val: string): MetricOption | undefined =>
      METRICS.find((m) => m.key === key)?.options.find((o) => o.value === val);

    const av = findOpt("AV", selection.AV)?.weight ?? 0;
    const ac = findOpt("AC", selection.AC)?.weight ?? 0;
    const ui = findOpt("UI", selection.UI)?.weight ?? 0;
    const c = findOpt("C", selection.C)?.weight ?? 0;
    const i = findOpt("I", selection.I)?.weight ?? 0;
    const a = findOpt("A", selection.A)?.weight ?? 0;
    const sChanged = selection.S === "C";
    const prOpt = findOpt("PR", selection.PR);
    const pr = sChanged ? prOpt?.weightChanged ?? prOpt?.weight ?? 0 : prOpt?.weight ?? 0;

    const iss = 1 - (1 - c) * (1 - i) * (1 - a);
    const impact = sChanged ? 7.52 * (iss - 0.029) - 3.25 * Math.pow(iss - 0.02, 15) : 6.42 * iss;
    const exploitability = 8.22 * av * ac * pr * ui;

    let baseScore = 0;
    if (impact > 0) {
      const raw = sChanged
        ? Math.min(1.08 * (impact + exploitability), 10)
        : Math.min(impact + exploitability, 10);
      baseScore = Math.ceil(raw * 10) / 10;
    }

    const vec = `CVSS:3.1/AV:${selection.AV}/AC:${selection.AC}/PR:${selection.PR}/UI:${selection.UI}/S:${selection.S}/C:${selection.C}/I:${selection.I}/A:${selection.A}`;
    return { vector: vec, score: baseScore, severity: severityFor(baseScore) };
  }, [selection]);

  useEffect(() => {
    onChange?.({ vector, score, severity });
  }, [vector, score, severity, onChange]);

  return (
    <div className={cn("panel", className)}>
      <div className="px-4 py-3 border-b border-border flex items-center justify-between">
        <h3 className="text-sm font-semibold text-fg">CVSS 3.1 Calculator</h3>
        <div className="flex items-center gap-3">
          <span className="text-xs text-fg-muted">{severity}</span>
          <span
            className={cn(
              "text-2xl font-bold tabular-nums",
              score >= 9 && "text-sev-critical",
              score >= 7 && score < 9 && "text-sev-high",
              score >= 4 && score < 7 && "text-sev-medium",
              score > 0 && score < 4 && "text-sev-low",
              score === 0 && "text-fg-muted",
            )}
          >
            {score.toFixed(1)}
          </span>
        </div>
      </div>
      <div className="p-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
        {METRICS.map((metric) => (
          <div key={metric.key}>
            <p className="label">{metric.label}</p>
            <div className="flex flex-wrap gap-1">
              {metric.options.map((opt) => {
                const active = selection[metric.key] === opt.value;
                return (
                  <button
                    key={opt.value}
                    type="button"
                    onClick={() =>
                      setSelection((prev) => ({ ...prev, [metric.key]: opt.value }))
                    }
                    className={cn(
                      "px-2.5 py-1 text-xs rounded border transition-colors",
                      active
                        ? "bg-accent text-bg border-accent"
                        : "bg-bg-secondary border-border text-fg-muted hover:text-fg hover:border-border-strong",
                    )}
                  >
                    {opt.label}
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>
      <div className="px-4 py-3 border-t border-border bg-bg-secondary">
        <p className="text-[10px] text-fg-subtle uppercase tracking-wide font-medium mb-1">Vector</p>
        <code className="text-xs text-fg font-mono break-all">{vector}</code>
      </div>
    </div>
  );
}
