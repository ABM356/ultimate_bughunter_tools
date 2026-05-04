#!/usr/bin/env bash
# Apply Alembic migrations.
#
# Local dev: runs against the docker-compose backend container.
# CI/Prod:   set DATABASE_URL or run inside a kubectl exec on a backend pod.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ "${USE_LOCAL_COMPOSE:-1}" = "1" ] && command -v docker >/dev/null && docker compose -f "$REPO_ROOT/infrastructure/docker/docker-compose.yml" ps -q backend >/dev/null 2>&1; then
  echo ">> Running alembic upgrade head in backend container"
  docker compose -f "$REPO_ROOT/infrastructure/docker/docker-compose.yml" exec -T backend alembic upgrade head
elif [ -n "${DATABASE_URL:-}" ]; then
  echo ">> Running alembic upgrade head against $DATABASE_URL"
  cd "$REPO_ROOT/backend"
  alembic upgrade head
elif command -v kubectl >/dev/null 2>&1; then
  NAMESPACE="${NAMESPACE:-hopeup}"
  POD=$(kubectl get pods -n "$NAMESPACE" -l app=backend -o jsonpath='{.items[0].metadata.name}')
  echo ">> Running alembic upgrade head in pod $POD"
  kubectl exec -n "$NAMESPACE" "$POD" -- alembic upgrade head
else
  echo "No way to run migrations. Set DATABASE_URL or start docker-compose." >&2
  exit 1
fi

echo ">> Migrations complete"
