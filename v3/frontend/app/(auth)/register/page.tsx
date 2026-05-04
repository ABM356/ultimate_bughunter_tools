"use client";

import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { toast } from "sonner";
import { Loader2 } from "lucide-react";
import { useAuth } from "@/lib/hooks/useAuth";
import type { UserRole } from "@/lib/types";

const ROLES: { value: UserRole; label: string }[] = [
  { value: "engineer", label: "Security Engineer" },
  { value: "analyst", label: "SOC Analyst" },
  { value: "hunter", label: "Bug Bounty Hunter" },
  { value: "manager", label: "Security Manager" },
  { value: "ciso", label: "CISO" },
  { value: "cto", label: "CTO" },
  { value: "auditor", label: "Auditor" },
];

const schema = z.object({
  name: z.string().min(2, "Name is required"),
  email: z.string().email("Enter a valid email"),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Must contain an uppercase letter")
    .regex(/[0-9]/, "Must contain a digit"),
  role: z.enum([
    "engineer",
    "analyst",
    "hunter",
    "manager",
    "ciso",
    "cto",
    "auditor",
    "admin",
  ]),
});

type FormValues = z.infer<typeof schema>;

export default function RegisterPage() {
  const { register: registerUser } = useAuth();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { name: "", email: "", password: "", role: "engineer" },
  });

  const onSubmit = async (values: FormValues) => {
    const result = await registerUser(values);
    if (!result.ok) {
      toast.error(result.error || "Registration failed");
    } else {
      toast.success("Account created");
    }
  };

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-xl font-bold text-fg">Create account</h1>
        <p className="text-sm text-fg-muted mt-1">
          Spin up a new tenant or join an existing one with an invite.
        </p>
      </div>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label htmlFor="name" className="label">
            Name
          </label>
          <input id="name" type="text" placeholder="Jane Doe" className="input" {...register("name")} />
          {errors.name && <p className="text-xs text-sev-critical mt-1">{errors.name.message}</p>}
        </div>
        <div>
          <label htmlFor="email" className="label">
            Work email
          </label>
          <input
            id="email"
            type="email"
            placeholder="jane@company.com"
            className="input"
            {...register("email")}
          />
          {errors.email && <p className="text-xs text-sev-critical mt-1">{errors.email.message}</p>}
        </div>
        <div>
          <label htmlFor="password" className="label">
            Password
          </label>
          <input
            id="password"
            type="password"
            placeholder="8+ chars, uppercase + digit"
            className="input"
            {...register("password")}
          />
          {errors.password && (
            <p className="text-xs text-sev-critical mt-1">{errors.password.message}</p>
          )}
        </div>
        <div>
          <label htmlFor="role" className="label">
            Role
          </label>
          <select id="role" className="input" {...register("role")}>
            {ROLES.map((r) => (
              <option key={r.value} value={r.value}>
                {r.label}
              </option>
            ))}
          </select>
          {errors.role && <p className="text-xs text-sev-critical mt-1">{errors.role.message}</p>}
        </div>
        <button type="submit" className="btn-primary w-full" disabled={isSubmitting}>
          {isSubmitting ? <Loader2 className="h-4 w-4 animate-spin" /> : "Create account"}
        </button>
      </form>
      <p className="text-center text-sm text-fg-muted mt-6">
        Already a user?{" "}
        <Link href="/login" className="text-accent hover:underline">
          Sign in
        </Link>
      </p>
    </div>
  );
}
