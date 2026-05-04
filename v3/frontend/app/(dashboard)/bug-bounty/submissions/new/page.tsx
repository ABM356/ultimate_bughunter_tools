"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { toast } from "sonner";
import { Loader2 } from "lucide-react";
import { useRouter } from "next/navigation";
import { PageHeader } from "@/components/PageHeader";
import { CVSSCalculator } from "@/components/CVSSCalculator";
import { poster, getApiError } from "@/lib/api";

const PROGRAMS = [
  { id: "p-1", name: "HopeUp Public" },
  { id: "p-2", name: "Acme Bank" },
  { id: "p-3", name: "Northwind Internal" },
];

const schema = z.object({
  program_id: z.string().min(1, "Program required"),
  title: z.string().min(8, "Provide a clear title"),
  affected_url: z.string().url("Must be a valid URL"),
  description: z.string().min(40, "Add at least 40 characters of detail"),
  proof_of_concept: z.string().min(20, "PoC required"),
  remediation: z.string().optional(),
});

type FormValues = z.infer<typeof schema>;

export default function NewSubmissionPage() {
  const router = useRouter();
  const [cvss, setCvss] = useState<{ vector: string; score: number; severity: string }>({
    vector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N",
    score: 0,
    severity: "None",
  });
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (values: FormValues) => {
    try {
      await poster("/submissions", { ...values, cvss_vector: cvss.vector, cvss_score: cvss.score });
      toast.success("Submission created");
      router.push("/bug-bounty/submissions");
    } catch (err) {
      toast.error(getApiError(err));
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="New Submission"
        breadcrumbs={[
          { label: "Bug Bounty", href: "/bug-bounty" },
          { label: "Submissions", href: "/bug-bounty/submissions" },
          { label: "New" },
        ]}
      />

      <form onSubmit={handleSubmit(onSubmit)} className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="space-y-4 lg:col-span-2">
          <div className="panel p-4 space-y-4">
            <div>
              <label className="label">Program</label>
              <select className="input" {...register("program_id")}>
                <option value="">Select a program</option>
                {PROGRAMS.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name}
                  </option>
                ))}
              </select>
              {errors.program_id && (
                <p className="text-xs text-sev-critical mt-1">{errors.program_id.message}</p>
              )}
            </div>
            <div>
              <label className="label">Title</label>
              <input
                type="text"
                className="input"
                placeholder="Stored XSS in /profile bio renders unsanitized HTML"
                {...register("title")}
              />
              {errors.title && (
                <p className="text-xs text-sev-critical mt-1">{errors.title.message}</p>
              )}
            </div>
            <div>
              <label className="label">Affected URL</label>
              <input
                type="url"
                className="input"
                placeholder="https://app.example.com/profile"
                {...register("affected_url")}
              />
              {errors.affected_url && (
                <p className="text-xs text-sev-critical mt-1">{errors.affected_url.message}</p>
              )}
            </div>
            <div>
              <label className="label">Description</label>
              <textarea
                className="input min-h-[120px]"
                placeholder="Walk through the bug, attack chain and impact"
                {...register("description")}
              />
              {errors.description && (
                <p className="text-xs text-sev-critical mt-1">{errors.description.message}</p>
              )}
            </div>
            <div>
              <label className="label">Proof of Concept</label>
              <textarea
                className="input min-h-[120px] font-mono"
                placeholder="curl -X POST https://... \n--data '<script>...</script>'"
                {...register("proof_of_concept")}
              />
              {errors.proof_of_concept && (
                <p className="text-xs text-sev-critical mt-1">{errors.proof_of_concept.message}</p>
              )}
            </div>
            <div>
              <label className="label">Suggested Remediation</label>
              <textarea
                className="input min-h-[80px]"
                placeholder="Encode HTML output in profile renderer; enforce CSP"
                {...register("remediation")}
              />
            </div>
          </div>

          <div className="flex items-center justify-end gap-2">
            <button
              type="button"
              onClick={() => router.back()}
              className="btn-secondary"
              disabled={isSubmitting}
            >
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={isSubmitting}>
              {isSubmitting ? <Loader2 className="h-4 w-4 animate-spin" /> : "Create Submission"}
            </button>
          </div>
        </div>

        <div className="lg:col-span-1">
          <CVSSCalculator onChange={setCvss} />
        </div>
      </form>
    </div>
  );
}
