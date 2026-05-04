"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { clearToken, decodeJWT, getToken, isTokenExpired, setToken } from "@/lib/auth";
import { api, getApiError, poster } from "@/lib/api";
import type { AuthTokens, LoginRequest, RegisterRequest, User } from "@/lib/types";

export function useAuth() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (!token || isTokenExpired(token)) {
      setLoading(false);
      return;
    }

    api
      .get<User>("/auth/me")
      .then((res) => setUser(res.data))
      .catch(() => {
        const decoded = decodeJWT(token);
        if (decoded) {
          setUser({
            id: decoded.sub,
            email: decoded.email || "",
            name: decoded.email?.split("@")[0] || "User",
            role: (decoded.role as User["role"]) || "engineer",
            tenant_id: decoded.tenant_id || "",
            created_at: new Date().toISOString(),
          });
        }
      })
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback(
    async (credentials: LoginRequest) => {
      try {
        const tokens = await poster<AuthTokens, LoginRequest>("/auth/login", credentials);
        setToken(tokens.access_token);
        const me = await api.get<User>("/auth/me");
        setUser(me.data);
        router.push("/dashboard");
        return { ok: true as const };
      } catch (err) {
        return { ok: false as const, error: getApiError(err) };
      }
    },
    [router],
  );

  const register = useCallback(
    async (data: RegisterRequest) => {
      try {
        await poster("/auth/register", data);
        return await login({ email: data.email, password: data.password });
      } catch (err) {
        return { ok: false as const, error: getApiError(err) };
      }
    },
    [login],
  );

  const logout = useCallback(() => {
    clearToken();
    setUser(null);
    router.push("/login");
  }, [router]);

  return {
    user,
    loading,
    isAuthenticated: !!user,
    login,
    register,
    logout,
  };
}
