# HopeUp Security Platform - v3

Enterprise cybersecurity SaaS platform. This directory contains the source for
the v3 stack and all infrastructure-as-code needed to run it locally or in
production.

## Components

- **frontend/** - Next.js 14 application (TypeScript, Tailwind).
- **backend/** - FastAPI backend (Python 3.12, async SQLAlchemy).
- **ai-services/** - Internal services that wrap LLM providers.
- **infrastructure/** - Docker Compose, Kubernetes (Kustomize + Helm), Terraform.
- **scripts/** - Setup, deploy, migrate, seed, backup helpers.
- **docs/** - Architecture, deployment, API, security, scaling docs.

```
v3/
├── frontend/                 Next.js app
├── backend/                  FastAPI app + Celery workers
├── ai-services/              AI provider integrations
├── infrastructure/
│   ├── docker/               docker-compose stack + nginx
│   ├── kubernetes/           Kustomize base + dev/prod overlays
│   ├── helm/                 Helm chart (alternative to Kustomize)
│   └── terraform/            AWS provisioning (EKS, RDS, OpenSearch, S3)
├── scripts/                  setup / deploy / migrate / seed / backup
├── docs/                     architecture, deployment, api, security, scaling
└── .github/workflows/        CI + Deploy GitHub Actions
```

## Quickstart

### Local development (Docker Compose)

```bash
cd v3
./scripts/setup.sh
```

Brings up the full stack and seeds an admin user. Then:

- Frontend: http://localhost:3000
- API:      http://localhost:8000/docs
- Kibana:   http://localhost:5601

Default admin login: `admin@hopeup.local` / `changeme123!` — change on first login.

### Kubernetes (Kustomize, dev overlay)

```bash
# Configure kubectl for your cluster, then:
kubectl apply -k infrastructure/kubernetes/overlays/dev
kubectl -n hopeup-dev get pods
```

### Kubernetes (Helm)

```bash
cd infrastructure/helm
helm dependency update
helm upgrade --install hopeup . -f values.yaml \
  --namespace hopeup --create-namespace
```

### Cloud provisioning (Terraform)

```bash
cd infrastructure/terraform
terraform init
terraform apply -var-file=envs/production.tfvars
```

This builds:

- VPC across 3 AZs with NAT-gateway HA
- EKS cluster with system + workload node groups (autoscaling 3-20)
- RDS PostgreSQL Multi-AZ
- ElastiCache Redis with multi-AZ failover
- Managed OpenSearch (3 master + 3 data nodes)
- S3 buckets for reports / scans / logs (KMS-encrypted)
- IAM roles for IRSA-bound pods

See [docs/deployment.md](docs/deployment.md) for the full deploy guide.

## Documentation

- [Architecture](docs/architecture.md) — high-level diagram + component descriptions.
- [Deployment](docs/deployment.md) — step-by-step for Compose and Kubernetes.
- [API](docs/api.md) — auth flow, endpoints, error format.
- [Security](docs/security.md) — TLS, secrets, RBAC, multi-tenancy isolation.
- [Scaling](docs/scaling.md) — bottleneck analysis and limits.

## CI / CD

GitHub Actions:

- `.github/workflows/ci.yml` — lint (ruff/eslint), test (pytest/jest),
  security scan (trivy), build + push Docker images on `main`.
- `.github/workflows/deploy.yml` — deploys `kustomize build` output to the
  selected environment, runs migrations, then waits for rollout.

## Backup / DR

`scripts/backup.sh` runs from a CronJob: full Postgres dump and Elasticsearch
snapshot, both pushed to S3. RPO 1 hour, RTO 4 hours, drilled quarterly.

## Repository conventions

- Production images live in ECR; dev / preview tags can be pushed by any
  contributor, but `latest` and `vN.N.N` only push from CI.
- All infra changes flow through `infrastructure/` and ship via the
  Deploy workflow. No `kubectl apply` from a laptop except for break-glass.
- Secrets never live in git. Use AWS Secrets Manager + External Secrets
  Operator.
- Every Kubernetes resource gets the `app`, `tier`, and `version` labels.

## Reporting issues

- Security issues: email security@hopeup.example.com.
- Bugs / feature requests: open a GitHub issue.
