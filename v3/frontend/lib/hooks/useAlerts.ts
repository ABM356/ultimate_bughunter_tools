"use client";

import { useEffect, useRef, useState } from "react";
import useSWR from "swr";
import { fetcher } from "@/lib/api";
import { getToken } from "@/lib/auth";
import type { Alert, PaginatedResponse } from "@/lib/types";

interface UseAlertsOptions {
  status?: string;
  severity?: string;
  refreshInterval?: number;
}

export function useAlerts(options: UseAlertsOptions = {}) {
  const { status, severity, refreshInterval = 10000 } = options;
  const params = new URLSearchParams();
  if (status) params.set("status", status);
  if (severity) params.set("severity", severity);

  const key = `/alerts?${params.toString()}`;
  const { data, error, isLoading, mutate } = useSWR<PaginatedResponse<Alert>>(key, fetcher, {
    refreshInterval,
    revalidateOnFocus: true,
  });

  return {
    alerts: data?.items || [],
    total: data?.total || 0,
    isLoading,
    error,
    refresh: mutate,
  };
}

export function useLiveAlerts(maxAlerts = 50) {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [connected, setConnected] = useState(false);
  const sourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    const token = getToken();
    if (!token) return;
    const baseURL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
    const url = `${baseURL}/alerts/stream?token=${encodeURIComponent(token)}`;

    let es: EventSource;
    try {
      es = new EventSource(url);
      sourceRef.current = es;

      es.onopen = () => setConnected(true);
      es.onerror = () => setConnected(false);

      es.onmessage = (event) => {
        try {
          const alert = JSON.parse(event.data) as Alert;
          setAlerts((prev) => [alert, ...prev].slice(0, maxAlerts));
        } catch {
          // Ignore malformed events
        }
      };
    } catch {
      setConnected(false);
    }

    return () => {
      sourceRef.current?.close();
      sourceRef.current = null;
    };
  }, [maxAlerts]);

  return { alerts, connected };
}
