# Architecture

## High-level diagram

```
                                    Internet
                                       |
                                       v
                          +---------------------------+
                          |  AWS ALB / NGINX Ingress  |
                          |  TLS termination          |
                          |  Rate limit (100 req/s)   |
                          +-------------+-------------+
                                        |
              +-------------------------+--------------------------+
              |                         |                          |
              v                         v                          v
        +-----------+            +-------------+            +-------------+
        | Frontend  |            |  Backend    |            |  WebSocket  |
        | Next.js   |  /api/*    |  FastAPI    |   /ws/*    |  /api/ws    |
        | (3+ pods) | <--------> |  (3+ pods)  | <--------> |  same pods  |
        +-----------+            +------+------+            +-------------+
                                        |
                  +---------------------+---------------------+
                  |                     |                     |
                  v                     v                     v
            +----------+           +----------+         +-------------+
            | Postgres |           |  Redis   |         |OpenSearch / |
            | RDS M-AZ |           | M-AZ HA  |         |Elasticsearch|
            +----------+           +-----+----+         +-------------+
                                         |                     ^
                                         | tasks               |
                                         v                     |
                                  +-------------+              |
                                  | Celery      |              |
                                  | Workers     | -------------+
                                  | (5-30 pods) |    indexing
                                  +------+------+
                                         ^
                                         | schedule
                                  +------+------+
                                  | Celery Beat |
                                  | (1 pod)     |
                                  +-------------+

                  +---------------------+---------------------+
                  |                                           |
                  v                                           v
            +-----------+                              +-------------+
            |  S3       |                              |  AI providers|
            |  reports  |                              | (Anthropic,  |
            |  scans    |                              |  OpenAI)     |
            |  logs     |                              +-------------+
            +-----------+
```

## Components

### Frontend (Next.js)
- Server-rendered React + client-side hydration.
- Standalone build (`output: 'standalone'`) for small Docker images.
- Talks only to the backend over HTTPS; never holds AI/Stripe keys.
- Stateless, horizontally scaled (HPA 3-15 replicas).

### Backend (FastAPI)
- Python 3.12, async I/O via SQLAlchemy 2.0 + asyncpg.
- Hosts REST API and WebSocket endpoints (live scan progress, notifications).
- Stateless, horizontally scaled (HPA 3-20 replicas).
- Reads secrets from a Kubernetes Secret (mounted via env), populated by
  External Secrets Operator from AWS Secrets Manager.

### Celery workers
- Run heavy tasks: scans, report generation, AI calls, email/notifications.
- Pull jobs from Redis (broker DB 1).
- Scaled by CPU + Redis queue depth (KEDA / Prometheus Adapter).

### Celery Beat
- Singleton scheduler. Stores schedule in Redis (RedBeat) so a restart
  doesn't lose state.
- Triggers periodic jobs: nightly scans, billing reconciliation, cleanups.

### PostgreSQL (RDS Multi-AZ)
- Primary datastore. Schema migrated with Alembic.
- Multi-AZ failover; 30-day automated backups.
- Performance Insights enabled.

### Redis (ElastiCache)
- Three responsibilities:
  - Celery broker (DB 1) and result backend (DB 2)
  - Session / rate-limit storage (DB 0)
  - RedBeat schedule store (DB 3)
- Multi-AZ replication group with automatic failover.

### OpenSearch
- Search + analytics over scan findings, logs, audit events.
- Three master nodes + three data nodes across AZs.
- TLS in transit, KMS at rest.

### S3
- `reports/` - generated PDFs and HTML reports (90d -> IA, 1y -> Glacier).
- `scans/`   - raw scanner JSON (90d retention).
- `logs/`    - long-term log archive (2y for compliance).

## Data flow: a scan

1. User starts scan in the UI -> `POST /api/scans` (frontend -> backend).
2. Backend writes a `Scan` row in Postgres, enqueues a Celery job.
3. Worker picks up the job, runs the scanner, streams progress back over a
   Redis pub/sub channel.
4. Backend's WebSocket handler subscribes to that channel and forwards
   updates to the user.
5. Worker writes findings to Postgres, indexes them in OpenSearch, and
   uploads the report PDF to S3.
6. Frontend polls / listens for completion, then fetches a presigned S3 URL
   for download.

## Multi-tenancy

- Every row is scoped by `tenant_id` (foreign key, indexed).
- Backend middleware extracts tenant from JWT claim and adds a Postgres
  Row-Level Security (RLS) session var, so even an ORM bug can't leak data
  across tenants.
- OpenSearch indexes are namespaced per tenant (`scan-{tenant_id}-YYYY.MM`)
  with an alias for cross-tenant admin queries.

## Observability

- Structured logs (JSON) shipped via Fluent Bit -> CloudWatch / OpenSearch.
- Prometheus metrics scraped on every pod (`/metrics`).
- Distributed tracing via OpenTelemetry -> AWS X-Ray.
- Sentry for application-level error reporting.
