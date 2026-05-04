# HopeUp Security Platform — Frontend

Next.js 14 (App Router) frontend for the HopeUp enterprise cybersecurity SaaS platform. Connects to a FastAPI backend at `http://localhost:8000/api/v1` by default.

## Stack

- Next.js 14 (App Router, Server + Client components)
- React 18, TypeScript 5 (strict)
- Tailwind CSS 3 with a custom dark theme
- Recharts (charts)
- SWR (data fetching, with auto-refresh for scans)
- Axios (with JWT injection + 401 redirect interceptors)
- React Hook Form + Zod (forms & validation)
- Sonner (toasts)
- lucide-react (icons)

## Getting started

```bash
cp .env.local.example .env.local
npm install
npm run dev
```

App runs at `http://localhost:3000`.

## Environment

- `NEXT_PUBLIC_API_URL` — base URL for the FastAPI backend. Defaults to `http://localhost:8000/api/v1`.

## Scripts

- `npm run dev` — start dev server with HMR
- `npm run build` — production build
- `npm run start` — start production server (after build)
- `npm run lint` — run ESLint
- `npm run typecheck` — TypeScript only check (no emit)

## Project layout

```
app/
  (auth)/              login, register
  (dashboard)/         protected SecOps surface
    dashboard/
    bug-bounty/
    red-team/
    blue-team/
    scans/
    ai/
    schedule/
    clients/
    reports/
    training/
    infrastructure/
    settings/
components/            reusable UI primitives
  charts/              recharts wrappers
lib/
  api.ts               axios + interceptors
  auth.ts              token storage helpers
  types.ts             shared API contracts
  utils.ts             cn(), formatters, severity helpers
  hooks/               useAuth, useScans, useAlerts (SSE/SWR)
middleware.ts          route normalization
```

## Auth

JWTs are stored in `localStorage` (key: `hopeup_token`) and injected into Axios requests automatically. On a 401 response, the user is redirected to `/login`. Route protection for `(dashboard)` runs client-side because tokens live in browser storage.

## Theming

Dark-only theme defined in `tailwind.config.ts` and `app/globals.css`. Severity tokens map to consistent colors:

- `critical` `#ff1744`
- `high` `#ff6b35`
- `medium` `#ffc400`
- `low` `#2979ff`
- `info` `#00c853`
- `accent` `#00d4ff`

## Docker

```bash
docker build --build-arg NEXT_PUBLIC_API_URL=https://api.example.com/api/v1 -t hopeup-frontend .
docker run -p 3000:3000 hopeup-frontend
```

## Notes

- All pages render with mock data when the backend is unavailable; live data hooks (`useScans`, `useAlerts`, `useLiveAlerts`) connect once the API is reachable.
- The live alert feed uses Server-Sent Events at `${API_URL}/alerts/stream`. Falls back gracefully when disconnected.
