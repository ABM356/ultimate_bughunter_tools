# Deployment Guide

This document covers deploying HopeUp two ways: locally with Docker Compose,
and to a Kubernetes cluster (EKS or any conformant k8s).

## Prerequisites

| Tool       | Version  | Purpose                          |
|------------|----------|----------------------------------|
| Docker     | >= 24.0  | local containers                 |
| docker compose | v2   | local orchestration              |
| kubectl    | >= 1.29  | cluster control                  |
| kustomize  | >= 5.3   | overlay generation               |
| helm       | >= 3.13  | optional alternative deployment  |
| aws CLI    | >= 2.x   | EKS auth + ECR push              |
| Terraform  | >= 1.6   | initial infra provisioning       |

## Local development (Docker Compose)

### 1. First-time setup

```bash
cd v3
./scripts/setup.sh
```

This will:
1. Copy `infrastructure/docker/.env.example` to `.env` if missing.
2. Bring up Postgres, Redis, Elasticsearch, Kibana, backend, worker, beat, frontend.
3. Wait for the database to be ready.
4. Run Alembic migrations.
5. Seed an admin user, demo tenant, and training modules.

### 2. Verify

- Frontend: http://localhost:3000
- API docs: http://localhost:8000/docs
- Kibana:   http://localhost:5601
- Postgres: `localhost:5432` (user/db: hopeup)
- Redis:    `localhost:6379`

### 3. Common tasks

```bash
# Tail backend logs
docker compose -f infrastructure/docker/docker-compose.yml logs -f backend

# Re-run migrations after a model change
./scripts/migrate.sh

# Run tests inside the backend container
docker compose -f infrastructure/docker/docker-compose.yml exec backend pytest

# Tear everything down (keeps volumes)
docker compose -f infrastructure/docker/docker-compose.yml down

# Wipe volumes too
docker compose -f infrastructure/docker/docker-compose.yml down -v
```

## Production (Kubernetes via Kustomize)

### 1. Provision infra (one-time)

```bash
cd infrastructure/terraform
terraform init
terraform apply -var-file=envs/production.tfvars
$(terraform output -raw kubeconfig_command)
```

### 2. Install platform add-ons

These run once per cluster:

```bash
# Ingress controller
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace

# cert-manager for Let's Encrypt TLS
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.14.4/cert-manager.yaml

# External Secrets Operator (pulls from AWS Secrets Manager)
helm upgrade --install external-secrets external-secrets \
  --repo https://charts.external-secrets.io \
  --namespace external-secrets --create-namespace
```

### 3. Deploy HopeUp

```bash
# Apply base + production overlay
kubectl apply -k infrastructure/kubernetes/overlays/prod

# Run migrations
kubectl apply -f infrastructure/kubernetes/base/migration-job.yaml -n hopeup
kubectl wait --for=condition=complete -n hopeup job/db-migrate

# Verify
kubectl -n hopeup get pods,svc,ingress
```

Or use the script:
```bash
./scripts/deploy.sh production v1.2.3
```

### 4. Verify

```bash
# Synthetic check
kubectl exec -n hopeup deploy/backend -- curl -fs http://localhost:8000/health

# External
curl -I https://hopeup.example.com/api/health
```

## Production (Kubernetes via Helm)

```bash
cd infrastructure/helm
helm dependency update
helm upgrade --install hopeup . \
  -f values.yaml -f overrides/production.yaml \
  --namespace hopeup --create-namespace
```

## Rolling back

### Compose
```bash
docker compose -f infrastructure/docker/docker-compose.yml up -d backend:previous-tag
```

### Kubernetes
```bash
kubectl -n hopeup rollout undo deployment/backend
kubectl -n hopeup rollout undo deployment/frontend
kubectl -n hopeup rollout history deployment/backend  # check what version you're on
```

## Database migrations

- Auto-applied by the `db-migrate` Job before each deploy in CI.
- Always backwards compatible: deploys must succeed even if both the old
  and new schema versions are running simultaneously (zero-downtime
  rolling updates).
- Pattern for breaking schema changes:
  1. Release N+0: add new column / table, dual-write code path.
  2. Release N+1: backfill, remove old reads.
  3. Release N+2: drop old column.

## Backups

Run `scripts/backup.sh` from a CronJob:
- Postgres: `pg_dump --format=custom` to S3.
- Elasticsearch: `_snapshot` API to S3 repository.

Daily backups, 30-day retention. Tested quarterly with full restore drills.
