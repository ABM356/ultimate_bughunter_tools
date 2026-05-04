# Security

This document describes the security model for HopeUp Security Platform.
Audience: engineers, platform team, customer security reviewers.

## Threat model

We assume the following adversaries:

1. **External attackers** scanning the public ingress. Mitigations: WAF,
   rate limiting, TLS, strict CSP, dependency scanning.
2. **Compromised customer credentials.** Mitigations: 2FA enforcement,
   short-lived JWTs, session revocation, audit logging.
3. **Insider threat (engineer).** Mitigations: least-privilege IAM,
   read-only production access by default, all administrative actions
   audited.
4. **Compromised pod / supply-chain.** Mitigations: image signing,
   non-root containers, NetworkPolicies, runtime monitoring.
5. **Cross-tenant data leakage.** Mitigations: row-level security in
   Postgres, per-tenant index naming in OpenSearch, integration tests
   that explicitly attempt cross-tenant access.

## TLS

- All public traffic terminated at NGINX Ingress with TLS 1.2 / 1.3.
- Certs issued by Let's Encrypt via cert-manager. Auto-renewed.
- HSTS (`max-age=63072000; includeSubDomains; preload`) and CSP enforced
  at the ingress layer.
- Internal traffic between pods is plaintext (within the VPC) by default.
  Add Istio / Linkerd mTLS if regulators require it.
- Database / Redis / OpenSearch require TLS in production (enforced via
  Terraform).

## Secrets management

- Never inline. Every credential loads from a Kubernetes `Secret`.
- Secrets are populated by **External Secrets Operator** from
  AWS Secrets Manager. Plaintext secrets never sit in git.
- `secret.yaml` in this repo holds **placeholders only**.
- Rotation:
  - JWT signing key: rotate quarterly with overlap window.
  - Database password: rotate quarterly via Secrets Manager rotation.
  - Stripe / Anthropic / OpenAI keys: rotate when revealed or on personnel
    changes; otherwise quarterly.

## Network policies

- Namespace `hopeup` runs with a default-deny `NetworkPolicy`.
- Frontend can talk to backend only.
- Backend can talk to Postgres, Redis, Elasticsearch + outbound HTTPS.
- Worker matches backend's egress profile, has no ingress.
- Postgres / Redis / Elasticsearch only accept traffic from authorized
  workloads.
- See `infrastructure/kubernetes/base/network-policy.yaml`.

## Pod security

- All pods run as non-root, with `runAsNonRoot: true`, dropped capabilities,
  `seccompProfile: RuntimeDefault`, and `allowPrivilegeEscalation: false`.
- Frontend uses `readOnlyRootFilesystem: true` with tmpfs mounts for
  writable paths.
- Backend can't be read-only-root (uvicorn writes to /tmp); the rest of the
  filesystem is read-only and the process runs unprivileged.
- Namespace enforces the `baseline` PodSecurity admission standard, with
  `restricted` warnings.

## RBAC

### Kubernetes RBAC
- Each Deployment has its own ServiceAccount with the minimum permissions
  needed (most need none beyond default).
- Platform team has `view` cluster role; only release engineers have
  `edit` in the `hopeup` namespace.

### Application RBAC
- Roles: `super_admin` (platform team), `tenant_admin`, `member`, `viewer`.
- Permissions enforced by FastAPI dependency `require(role)` decorator.
- Every privilege-gated action emits an `audit_log` row containing actor,
  target, action, before/after state, request id.

## Multi-tenancy isolation

- Every data row carries `tenant_id`. Indexes start with `tenant_id`.
- Postgres Row-Level Security policy: `tenant_id = current_setting('app.tenant_id')`.
  Backend sets the session var on each request from the JWT claim, so even
  an ORM query bug can't cross tenants.
- OpenSearch indices namespaced: `scan-{tenant_id}-YYYY.MM`. Aliases are
  created with index filters that pin tenant id.
- S3 keys prefixed by tenant: `s3://hopeup-reports/{tenant_id}/{report_id}.pdf`.
  Pre-signed URL generation enforces the prefix.

## Audit logging

- All write actions append to `audit_log` table.
- Authentication events (login, logout, MFA enroll, password change) are
  always logged.
- Admin actions (impersonation, billing changes, RBAC changes) require a
  reason field and emit a Slack notification.
- Logs streamed to OpenSearch and to a dedicated S3 bucket with object lock
  for tamper-evidence.

## Vulnerability management

- CI runs:
  - Trivy on Dockerfiles + filesystem.
  - `pip-audit` for Python deps.
  - `npm audit` for Node deps.
  - CodeQL on the codebase.
- Critical vulns block merge; high vulns get a 7-day SLA to remediate.
- Cluster nodes patched via managed AMI updates (EKS managed node groups).

## Backups & disaster recovery

- RTO: 4 hours. RPO: 1 hour.
- RDS: PITR enabled (5 minute granularity), 30-day retention, daily snapshots.
- Elasticsearch / OpenSearch: daily `_snapshot` to S3.
- Application: redeploy from container images (immutable, signed).
- Quarterly DR drill restores the most recent backup into a fresh stack
  and runs smoke tests.

## Compliance

Mappings to common controls:

| Control                  | Implementation                                      |
|--------------------------|-----------------------------------------------------|
| SOC 2 CC6.1 (logical access) | RBAC, MFA, least-privilege IAM, audit log    |
| SOC 2 CC7.1 (system monitoring) | Prometheus, OpenSearch logs, Sentry         |
| SOC 2 CC8.1 (change management) | CI/CD with required reviews, immutable images |
| HIPAA Technical Safeguards | TLS in transit, KMS at rest, access controls       |
| GDPR Art. 32 (security)  | Encryption, access logs, data minimization          |

## Reporting issues

Email `security@hopeup.example.com` with PGP key on the website. We
acknowledge within 24 hours and aim for fixes within 7 days for high
severity, 30 for medium.
