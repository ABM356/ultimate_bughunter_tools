"use client";

import useSWR from "swr";
import { fetcher } from "@/lib/api";
import type { PaginatedResponse, Scan } from "@/lib/types";

interface UseScansOptions {
  status?: string;
  page?: number;
  pageSize?: number;
  refreshInterval?: number;
}

export function useScans(options: UseScansOptions = {}) {
  const { status, page = 1, pageSize = 20, refreshInterval = 5000 } = options;
  const params = new URLSearchParams();
  params.set("page", page.toString());
  params.set("page_size", pageSize.toString());
  if (status) params.set("status", status);

  const key = `/scans?${params.toString()}`;
  const { data, error, isLoading, mutate } = useSWR<PaginatedResponse<Scan>>(key, fetcher, {
    refreshInterval,
    revalidateOnFocus: false,
  });

  return {
    scans: data?.items || [],
    total: data?.total || 0,
    isLoading,
    error,
    refresh: mutate,
  };
}

export function useScan(id: string | undefined, refreshInterval = 2000) {
  const { data, error, isLoading, mutate } = useSWR<Scan>(
    id ? `/scans/${id}` : null,
    fetcher,
    {
      refreshInterval: (latest) =>
        latest && (latest.status === "completed" || latest.status === "failed") ? 0 : refreshInterval,
    },
  );

  return {
    scan: data,
    isLoading,
    error,
    refresh: mutate,
  };
}
