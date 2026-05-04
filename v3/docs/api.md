# API Overview

The HopeUp API is a JSON REST API plus a small set of WebSocket endpoints
for live progress.

- Base URL: `https://hopeup.example.com/api`
- WebSocket base: `wss://hopeup.example.com/ws`
- All requests must be authenticated unless noted otherwise.
- All responses are JSON encoded UTF-8.

## Authentication flow

```
+------+                             +---------+                 +----------+
| User |                             | Frontend |                 | Backend  |
+--+---+                             +----+----+                 +----+-----+
   |  POST /api/auth/login                |                          |
   |  { email, password, totp_code? }     |                          |
   |  -------------------------------->   |  POST /api/auth/login    |
   |                                      |  ----------------------> |
   |                                      |                          |  verify password
   |                                      |                          |  verify TOTP
   |                                      |  200 { access, refresh } |
   |                                      |  <---------------------- |
   |  Set-Cookie: refresh (httpOnly)      |                          |
   |  <------------------------------     |                          |
   |                                      |                          |
   |  Authorization: Bearer <access>      |                          |
   |  -------------------------------->   |  -----------------------> |
   |                                      |                          |
   |  on 401:                             |                          |
   |  POST /api/auth/refresh              |                          |
   |  (cookie carried)                    |                          |
   |  -------------------------------->   |  -----------------------> |
   |  200 { access }                      |                          |
   |  <----------------------------       |                          |
```

- Access tokens: short-lived JWT (15 min), `HS256` signed with `JWT_SECRET`.
- Refresh tokens: 14-day rotation, stored httpOnly + SameSite=Strict cookie.
- 2FA: TOTP enrollment is mandatory for admins, optional for users (configurable).
- Rate limit: 5 login attempts / minute / IP.

## Common headers

| Header           | Required | Notes                                  |
|------------------|----------|----------------------------------------|
| `Authorization`  | yes      | `Bearer <jwt>`                         |
| `X-Tenant-Id`    | optional | Multi-tenant override (admin only)     |
| `X-Request-Id`   | optional | Echoed in logs for tracing             |
| `Content-Type`   | yes      | `application/json` for body requests   |

## Error format

```json
{
  "error": {
    "code": "validation_error",
    "message": "title: must not be empty",
    "request_id": "8f3c2e1b...",
    "details": [
      { "field": "title", "issue": "must not be empty" }
    ]
  }
}
```

Standard HTTP statuses; `4xx` always includes the JSON shape above.

## Key endpoints

### Auth

| Method | Path                       | Description                       |
|--------|----------------------------|-----------------------------------|
| POST   | `/api/auth/register`       | Create tenant + first admin       |
| POST   | `/api/auth/login`          | Email + password (+ TOTP)         |
| POST   | `/api/auth/refresh`        | Rotate access token               |
| POST   | `/api/auth/logout`         | Revoke refresh token              |
| GET    | `/api/auth/me`             | Current user                      |
| POST   | `/api/auth/2fa/enroll`     | TOTP enrollment (returns QR)      |
| POST   | `/api/auth/2fa/verify`     | Confirm a TOTP code               |

### Users / Tenants

| Method | Path                       | Description                       |
|--------|----------------------------|-----------------------------------|
| GET    | `/api/tenant`              | Current tenant                    |
| GET    | `/api/users`               | List users (admin)                |
| POST   | `/api/users`               | Invite a user                     |
| PATCH  | `/api/users/{id}`          | Update role / status              |

### Scans

| Method | Path                          | Description                       |
|--------|-------------------------------|-----------------------------------|
| GET    | `/api/scans`                  | List scans (filtered, paginated)  |
| POST   | `/api/scans`                  | Start a new scan                  |
| GET    | `/api/scans/{id}`             | Scan details                      |
| GET    | `/api/scans/{id}/findings`    | List findings                     |
| GET    | `/api/scans/{id}/report`      | Pre-signed S3 URL for the report  |
| DELETE | `/api/scans/{id}`             | Cancel / delete                   |

### Findings

| Method | Path                                    | Description           |
|--------|-----------------------------------------|-----------------------|
| GET    | `/api/findings`                         | Cross-scan listing    |
| PATCH  | `/api/findings/{id}`                    | Update status / notes |
| POST   | `/api/findings/{id}/comments`           | Add comment           |

### Training

| Method | Path                          | Description                       |
|--------|-------------------------------|-----------------------------------|
| GET    | `/api/training/modules`       | Available modules                 |
| POST   | `/api/training/enroll`        | Enroll user in module             |
| GET    | `/api/training/progress`      | Progress for current user         |

### Billing

| Method | Path                          | Description                       |
|--------|-------------------------------|-----------------------------------|
| GET    | `/api/billing/subscription`   | Current plan + status             |
| POST   | `/api/billing/checkout`       | Stripe checkout session           |
| POST   | `/api/billing/webhook`        | Stripe webhook (signature-verified)|

### Admin (platform team only)

| Method | Path                       | Description                       |
|--------|----------------------------|-----------------------------------|
| GET    | `/api/admin/tenants`       | All tenants                       |
| GET    | `/api/admin/usage`         | Aggregated usage metrics          |
| POST   | `/api/admin/feature-flags` | Toggle features per tenant        |

### Health

| Method | Path        | Description                                    |
|--------|-------------|------------------------------------------------|
| GET    | `/health`   | Liveness; returns 200 with `{"status":"ok"}`.  |
| GET    | `/ready`    | Readiness; verifies DB + Redis + ES.           |
| GET    | `/metrics`  | Prometheus metrics.                            |

## WebSocket endpoints

| Path                        | Description                                |
|-----------------------------|--------------------------------------------|
| `/ws/scans/{id}/progress`   | Streaming progress events for a scan.      |
| `/ws/notifications`         | User-scoped notification stream.           |

Auth: subprotocol token `Authorization, Bearer <jwt>`, or query string
`?token=<jwt>` (last resort).

## Rate limiting

- Default: 600 req / minute / user (configurable per tenant).
- Login + password reset: 5 / minute / IP.
- Bulk endpoints (scan create, large queries) have separate buckets.
- 429 responses include `Retry-After`.

## Versioning

- API versioning is **path-based** (`/api/v1/...`) once the first breaking
  change ships. Until then, all routes live under `/api/`.
- Backwards-compatible additions never bump the version.

## OpenAPI / Swagger

- `/api/docs` (Swagger UI)
- `/api/redoc` (ReDoc)
- `/api/openapi.json` (raw spec, for codegen)
