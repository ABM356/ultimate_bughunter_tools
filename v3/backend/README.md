# HopeUp Security Platform - Backend

Production-quality, multi-tenant FastAPI backend for the HopeUp enterprise
cybersecurity SaaS platform. Twelve functional modules: auth/tenants, bounty,
red team, blue team, scans, AI, reports, training, infrastructure, scheduling,
plus billing and observability hooks.

## Stack

- FastAPI + async SQLAlchemy 2.0 + asyncpg
- PostgreSQL (primary store), Redis (cache/pubsub/Celery broker), Elasticsearch (logs/SIEM)
- Celery workers for scans, AI, alert correlation
- Anthropic Claude + OpenAI integrations (graceful fallback to rule-based)
- Alembic for migrations, Pydantic v2 schemas

## Layout

```
app/
  api/v1/         # FastAPI routers (one file per module)
  core/           # config, db, security, redis, elasticsearch
  models/         # SQLAlchemy models
  schemas/        # Pydantic v2 request/response models
  services/       # Business logic (AI, scanner, SIEM, reports, notifications)
  integrations/   # External tools (nmap, ZAP, nuclei, threat intel)
  workers/        # Celery app + tasks
alembic/          # Async Alembic migrations
tests/
```

## Setup

```bash
cd v3/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env with your DB/Redis/ES URLs and secrets
```

## Database migrations

```bash
alembic upgrade head
# create a new revision after model changes:
alembic revision -m "add new column" --autogenerate
```

## Run the API (development)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

OpenAPI docs at http://localhost:8000/docs, health at /health.

## Run Celery workers

```bash
celery -A app.workers.celery_app.celery_app worker --loglevel=info
celery -A app.workers.celery_app.celery_app beat   --loglevel=info
```

## Docker

```bash
docker build -t hopeup-backend .
docker run --rm -p 8000:8000 --env-file .env hopeup-backend
```

## Multi-tenancy

Every tenant-scoped table carries a `tenant_id` column. All endpoints enforce
isolation: non-admin users can only read/write rows where
`tenant_id == current_user.tenant_id`. Super-admins (admin role with
`tenant_id IS NULL`) may operate across tenants.

## AI fallbacks

If `ANTHROPIC_API_KEY` is unset, the AI service silently switches to
deterministic rule-based fallbacks so the platform stays usable for
development and air-gapped deployments.
