#!/usr/bin/env bash
# Seed initial data for a fresh HopeUp install:
#   - admin user
#   - sample tenant
#   - default training modules
#
# Idempotent: safe to run repeatedly. Uses the backend `python -m app.scripts.seed`
# entrypoint which deduplicates by email/slug.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

ADMIN_EMAIL="${ADMIN_EMAIL:-admin@hopeup.local}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-changeme123!}"
TENANT_NAME="${TENANT_NAME:-Acme Inc}"
TENANT_SLUG="${TENANT_SLUG:-acme}"

if [ "${USE_LOCAL_COMPOSE:-1}" = "1" ] && command -v docker >/dev/null && docker compose -f "$REPO_ROOT/infrastructure/docker/docker-compose.yml" ps -q backend >/dev/null 2>&1; then
  EXEC="docker compose -f $REPO_ROOT/infrastructure/docker/docker-compose.yml exec -T backend"
elif command -v kubectl >/dev/null 2>&1; then
  NAMESPACE="${NAMESPACE:-hopeup}"
  POD=$(kubectl get pods -n "$NAMESPACE" -l app=backend -o jsonpath='{.items[0].metadata.name}')
  EXEC="kubectl exec -n $NAMESPACE $POD --"
else
  EXEC="python -m"
fi

echo ">> Seeding admin user, tenant, training modules"
$EXEC python -m app.scripts.seed \
  --admin-email "$ADMIN_EMAIL" \
  --admin-password "$ADMIN_PASSWORD" \
  --tenant-name "$TENANT_NAME" \
  --tenant-slug "$TENANT_SLUG"

echo ">> Done"
echo "Admin login: $ADMIN_EMAIL / $ADMIN_PASSWORD"
echo "Change the password on first login."
