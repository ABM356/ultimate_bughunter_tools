"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { toast } from "sonner";
import { Globe, Loader2, Network, Shield, Zap } from "lucide-react";
import { useRouter } from "next/navigation";
import { PageHeader } from "@/components/PageHeader";
import { cn } from "@/lib/utils";
import { getApiError, poster } from "@/lib/api";
import type { ScanType, ScanLevel, Tier } from "@/lib/types";

const TYPES: { value: ScanType; label: string; icon: React.ComponentType<{ className?: string }>; description: string }[] = [
  { value: "web", label: "Web Application", icon: Globe, description: "OWASP Top 10, JS analysis, auth flaws" },
  { value: "api", label: "API", icon: Zap, description: "REST/GraphQL endpoints, schema, auth" },
  { value: "network", label: "Network", icon: Network, description: "Ports, services, vulnerable hosts" },
  { value: "full", label: "Full Stack", icon: Shield, description: "All scan types combined" },
];

const LEVELS: { value: ScanLevel; label: string; description: string }[] = [
  { value: "fast", label: "Fast", description: "5-15 min, top vulnerabilities only" },
  { value: "medium", label: "Medium", description: "30-60 min, balanced coverage" },
  { value: "deep", label: "Deep", description: "2-6 hours, full enumeration" },
];

const schema = z.object({
  target: z.string().min(3, "Target required"),
  scan_type: z.enum(["web", "api", "network", "full"]),
  scan_level: z.enum(["fast", "medium", "deep"]),
  tier: z.enum(["starter", "pro", "enterprise"]),
});

type FormValues = z.infer<typeof schema>;

export default function NewScanPage() {
  const router = useRouter();
  const [scanType, setScanType] = useState<ScanType>("web");
  const [scanLevel, setScanLevel] = useState<ScanLevel>("medium");
  const [tier, setTier] = useState<Tier>("pro");
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setValue,
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { scan_type: "web", scan_level: "medium", tier: "pro" },
  });

  const onSubmit = async (values: FormValues) => {
    try {
      const result = await poster<{ id: string }, FormValues>("/scans", values);
      toast.success("Scan queued");
      router.push(`/scans/${result.id || "new"}`);
    } catch (err) {
      toast.error(getApiError(err));
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="New Scan"
        breadcrumbs={[{ label: "Scans", href: "/scans" }, { label: "New" }]}
      />

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div className="panel p-4">
          <label className="label">Target</label>
          <input
            type="text"
            placeholder="https://example.com or 10.0.0.0/24"
            className="input"
            {...register("target")}
          />
          {errors.target && <p className="text-xs text-sev-critical mt-1">{errors.target.message}</p>}
        </div>

        <div className="panel p-4">
          <label className="label">Scan Type</label>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
            {TYPES.map((type) => {
              const Icon = type.icon;
              const active = scanType === type.value;
              return (
                <button
                  key={type.value}
                  type="button"
                  onClick={() => {
                    setScanType(type.value);
                    setValue("scan_type", type.value);
                  }}
                  className={cn(
                    "text-left rounded-md border p-4 transition-colors",
                    active
                      ? "border-accent bg-accent/5"
                      : "border-border bg-bg-secondary hover:border-border-strong",
                  )}
                >
                  <Icon className={cn("h-5 w-5 mb-2", active ? "text-accent" : "text-fg-muted")} />
                  <p className="text-sm font-semibold">{type.label}</p>
                  <p className="text-xs text-fg-muted mt-1">{type.description}</p>
                </button>
              );
            })}
          </div>
        </div>

        <div className="panel p-4">
          <label className="label">Scan Level</label>
          <div className="grid grid-cols-3 gap-2">
            {LEVELS.map((level) => {
              const active = scanLevel === level.value;
              return (
                <button
                  key={level.value}
                  type="button"
                  onClick={() => {
                    setScanLevel(level.value);
                    setValue("scan_level", level.value);
                  }}
                  className={cn(
                    "rounded-md border p-4 text-center transition-colors",
                    active
                      ? "border-accent bg-accent/5 text-accent"
                      : "border-border bg-bg-secondary text-fg hover:border-border-strong",
                  )}
                >
                  <p className="text-sm font-semibold uppercase">{level.label}</p>
                  <p className="text-xs text-fg-muted mt-1">{level.description}</p>
                </button>
              );
            })}
          </div>
        </div>

        <div className="panel p-4">
          <label className="label">Tier</label>
          <div className="flex gap-2">
            {(["starter", "pro", "enterprise"] as Tier[]).map((t) => (
              <button
                key={t}
                type="button"
                onClick={() => {
                  setTier(t);
                  setValue("tier", t);
                }}
                className={cn(
                  "px-4 py-2 rounded-md border text-sm capitalize transition-colors",
                  tier === t
                    ? "border-accent bg-accent text-bg"
                    : "border-border text-fg-muted hover:text-fg hover:border-border-strong",
                )}
              >
                {t}
              </button>
            ))}
          </div>
        </div>

        <div className="flex justify-end gap-2">
          <button type="button" onClick={() => router.back()} className="btn-secondary">
            Cancel
          </button>
          <button type="submit" className="btn-primary" disabled={isSubmitting}>
            {isSubmitting ? <Loader2 className="h-4 w-4 animate-spin" /> : "Start Scan"}
          </button>
        </div>
      </form>
    </div>
  );
}
