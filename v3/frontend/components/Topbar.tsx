"use client";

import { Bell, Menu, Search, User } from "lucide-react";
import { useState } from "react";

interface TopbarProps {
  onMenuClick: () => void;
}

export function Topbar({ onMenuClick }: TopbarProps) {
  const [notifOpen, setNotifOpen] = useState(false);
  const [userOpen, setUserOpen] = useState(false);

  return (
    <header className="h-14 bg-panel border-b border-border flex items-center justify-between px-4 lg:px-6 sticky top-0 z-20">
      <div className="flex items-center gap-3 flex-1 min-w-0">
        <button
          type="button"
          onClick={onMenuClick}
          className="lg:hidden text-fg-muted hover:text-fg"
          aria-label="Open menu"
        >
          <Menu className="h-5 w-5" />
        </button>
        <div className="hidden md:flex items-center gap-2 bg-bg-secondary border border-border rounded-md px-3 py-1.5 max-w-md flex-1">
          <Search className="h-4 w-4 text-fg-subtle" />
          <input
            type="text"
            placeholder="Search assets, scans, alerts..."
            className="bg-transparent outline-none text-sm text-fg placeholder:text-fg-subtle flex-1"
          />
          <kbd className="hidden lg:inline-flex text-[10px] text-fg-subtle border border-border-strong rounded px-1.5 py-0.5">
            cmd K
          </kbd>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <div className="relative">
          <button
            type="button"
            onClick={() => setNotifOpen((o) => !o)}
            className="relative p-2 rounded-md text-fg-muted hover:text-fg hover:bg-panel-hover"
            aria-label="Notifications"
          >
            <Bell className="h-4 w-4" />
            <span className="absolute top-1.5 right-1.5 h-2 w-2 bg-sev-critical rounded-full ring-2 ring-panel" />
          </button>
          {notifOpen && (
            <div className="absolute right-0 mt-2 w-80 panel shadow-panel animate-fade-in">
              <div className="px-4 py-3 border-b border-border">
                <p className="text-sm font-semibold">Notifications</p>
              </div>
              <ul className="max-h-80 overflow-y-auto">
                <li className="px-4 py-3 border-b border-border-subtle hover:bg-panel-hover cursor-pointer">
                  <p className="text-sm text-fg">Critical alert: SQL injection on api.example.com</p>
                  <p className="text-xs text-fg-muted mt-1">2 minutes ago</p>
                </li>
                <li className="px-4 py-3 border-b border-border-subtle hover:bg-panel-hover cursor-pointer">
                  <p className="text-sm text-fg">Scan #4421 completed: 12 findings</p>
                  <p className="text-xs text-fg-muted mt-1">8 minutes ago</p>
                </li>
                <li className="px-4 py-3 hover:bg-panel-hover cursor-pointer">
                  <p className="text-sm text-fg">New submission for HopeUp public program</p>
                  <p className="text-xs text-fg-muted mt-1">21 minutes ago</p>
                </li>
              </ul>
            </div>
          )}
        </div>

        <div className="relative">
          <button
            type="button"
            onClick={() => setUserOpen((o) => !o)}
            className="flex items-center gap-2 p-1.5 pr-3 rounded-md text-fg-muted hover:text-fg hover:bg-panel-hover"
            aria-label="User menu"
          >
            <span className="h-7 w-7 rounded-full bg-accent/10 text-accent flex items-center justify-center">
              <User className="h-4 w-4" />
            </span>
            <span className="hidden md:inline text-sm">Account</span>
          </button>
          {userOpen && (
            <div className="absolute right-0 mt-2 w-56 panel shadow-panel animate-fade-in">
              <div className="px-4 py-3 border-b border-border">
                <p className="text-sm font-semibold text-fg">Signed in</p>
                <p className="text-xs text-fg-muted truncate">user@hopeup.io</p>
              </div>
              <div className="py-1">
                <a href="/settings" className="block px-4 py-2 text-sm text-fg hover:bg-panel-hover">
                  Settings
                </a>
                <a href="/training" className="block px-4 py-2 text-sm text-fg hover:bg-panel-hover">
                  Training
                </a>
                <button
                  type="button"
                  onClick={() => {
                    if (typeof window !== "undefined") {
                      window.localStorage.removeItem("hopeup_token");
                      window.location.href = "/login";
                    }
                  }}
                  className="w-full text-left block px-4 py-2 text-sm text-sev-critical hover:bg-panel-hover"
                >
                  Logout
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
