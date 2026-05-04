"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import {
  Activity,
  Bot,
  BookOpen,
  Bug,
  Building2,
  Calendar,
  ChevronLeft,
  ChevronRight,
  FileText,
  LayoutDashboard,
  LogOut,
  Network,
  Search,
  Settings,
  Shield,
  ShieldAlert,
  ShieldCheck,
  Swords,
  Users,
  X,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";
import { clearToken } from "@/lib/auth";

interface NavItem {
  label: string;
  href: string;
  icon: LucideIcon;
}

interface NavSection {
  label: string;
  items: NavItem[];
}

const SECTIONS: NavSection[] = [
  {
    label: "Operations",
    items: [
      { label: "SecOps Dashboard", href: "/dashboard", icon: LayoutDashboard },
      { label: "Bug Bounty", href: "/bug-bounty", icon: Bug },
      { label: "Red Team", href: "/red-team", icon: Swords },
      { label: "Blue Team", href: "/blue-team", icon: ShieldCheck },
    ],
  },
  {
    label: "Automation",
    items: [
      { label: "Scans", href: "/scans", icon: Search },
      { label: "Schedule", href: "/schedule", icon: Calendar },
      { label: "AI Assistant", href: "/ai", icon: Bot },
    ],
  },
  {
    label: "Business",
    items: [
      { label: "Clients", href: "/clients", icon: Building2 },
      { label: "Reports", href: "/reports", icon: FileText },
      { label: "Infrastructure", href: "/infrastructure", icon: Network },
    ],
  },
  {
    label: "Learning",
    items: [{ label: "Training", href: "/training", icon: BookOpen }],
  },
  {
    label: "Account",
    items: [{ label: "Settings", href: "/settings", icon: Settings }],
  },
];

interface SidebarProps {
  mobileOpen: boolean;
  onClose: () => void;
}

export function Sidebar({ mobileOpen, onClose }: SidebarProps) {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

  const isActive = (href: string) => {
    if (href === "/dashboard") return pathname === href;
    return pathname.startsWith(href);
  };

  const handleLogout = () => {
    clearToken();
    if (typeof window !== "undefined") {
      window.location.href = "/login";
    }
  };

  return (
    <>
      {mobileOpen && (
        <div
          className="fixed inset-0 z-30 bg-bg/80 backdrop-blur-sm lg:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}
      <aside
        className={cn(
          "fixed lg:static inset-y-0 left-0 z-40 flex flex-col bg-panel border-r border-border transition-all duration-200",
          collapsed ? "w-16" : "w-60",
          mobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0",
        )}
      >
        <div className="flex items-center justify-between h-14 px-4 border-b border-border">
          <Link href="/dashboard" className="flex items-center gap-2 min-w-0">
            <ShieldAlert className="h-6 w-6 text-accent flex-shrink-0" />
            {!collapsed && (
              <span className="font-bold text-fg whitespace-nowrap">HopeUp</span>
            )}
          </Link>
          <button
            type="button"
            onClick={onClose}
            className="lg:hidden text-fg-muted hover:text-fg"
            aria-label="Close menu"
          >
            <X className="h-5 w-5" />
          </button>
          <button
            type="button"
            onClick={() => setCollapsed((c) => !c)}
            className="hidden lg:inline-flex text-fg-muted hover:text-fg"
            aria-label="Toggle sidebar"
          >
            {collapsed ? (
              <ChevronRight className="h-4 w-4" />
            ) : (
              <ChevronLeft className="h-4 w-4" />
            )}
          </button>
        </div>

        <nav className="flex-1 overflow-y-auto py-4 px-2">
          {SECTIONS.map((section) => (
            <div key={section.label} className="mb-6">
              {!collapsed && (
                <p className="px-3 mb-1.5 text-[10px] font-bold uppercase tracking-wider text-fg-subtle">
                  {section.label}
                </p>
              )}
              <ul className="space-y-0.5">
                {section.items.map((item) => {
                  const Icon = item.icon;
                  const active = isActive(item.href);
                  return (
                    <li key={item.href}>
                      <Link
                        href={item.href}
                        onClick={onClose}
                        title={collapsed ? item.label : undefined}
                        className={cn(
                          "flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors",
                          collapsed && "justify-center",
                          active
                            ? "bg-accent/10 text-accent border-l-2 border-accent"
                            : "text-fg-muted hover:text-fg hover:bg-panel-hover",
                        )}
                      >
                        <Icon className="h-4 w-4 flex-shrink-0" />
                        {!collapsed && <span className="truncate">{item.label}</span>}
                      </Link>
                    </li>
                  );
                })}
              </ul>
            </div>
          ))}
        </nav>

        <div className="border-t border-border p-2">
          <button
            type="button"
            onClick={handleLogout}
            title={collapsed ? "Logout" : undefined}
            className={cn(
              "w-full flex items-center gap-3 px-3 py-2 rounded-md text-sm text-fg-muted hover:text-sev-critical hover:bg-panel-hover transition-colors",
              collapsed && "justify-center",
            )}
          >
            <LogOut className="h-4 w-4 flex-shrink-0" />
            {!collapsed && <span>Logout</span>}
          </button>
        </div>
      </aside>
    </>
  );
}
