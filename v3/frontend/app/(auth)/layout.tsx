import Link from "next/link";
import { ShieldAlert } from "lucide-react";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <main className="min-h-screen flex items-center justify-center bg-bg grid-bg p-4">
      <div className="w-full max-w-md">
        <Link href="/" className="flex items-center justify-center gap-2 mb-8">
          <ShieldAlert className="h-8 w-8 text-accent" />
          <span className="text-xl font-bold text-fg">HopeUp Platform</span>
        </Link>
        <div className="panel p-8 shadow-panel">{children}</div>
        <p className="text-center text-xs text-fg-subtle mt-6">
          Secured by HopeUp. SOC 2 Type II compliant.
        </p>
      </div>
    </main>
  );
}
