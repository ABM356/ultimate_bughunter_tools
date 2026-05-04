"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";
import { Shield } from "lucide-react";

export default function RootPage() {
  const router = useRouter();

  useEffect(() => {
    const token = getToken();
    if (token) {
      router.replace("/dashboard");
    } else {
      router.replace("/login");
    }
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-bg">
      <div className="flex flex-col items-center gap-4">
        <Shield className="h-12 w-12 text-accent animate-pulse-accent" />
        <p className="text-fg-muted text-sm">Loading HopeUp Platform...</p>
      </div>
    </div>
  );
}
