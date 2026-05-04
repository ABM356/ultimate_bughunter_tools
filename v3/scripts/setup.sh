#!/usr/bin/env bash
# HopeUp Security Platform - local dev setup
#
# Bootstraps a working local stack:
#   1. Copies .env.example to .env if missing
#   2. Brings up the docker-compose stack
#   3. Waits for postgres to accept connections
#   4. Runs alembic migrations
#   5. Seeds initial data (admin user, sample tenant, training modules)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCKER_DIR="$REPO_ROOT/infrastructure/docker"
ENV_FILE="$DOCKER_DIR/.env"

green() { printf "\033[32m%s\033[0m\n" "$*"; }
yellow() { printf "\033[33m%s\033[0m\n" "$*"; }
red() { printf "\033[31m%s\033[0m\n" "$*" >&2; }

require() {
  command -v "$1" >/dev/null 2>&1 || { red "Missing dependency: $1"; exit 1; }
}

require docker
require docker-compose 2>/dev/null || true

green "[1/5] Preparing environment file"
if [ ! -f "$ENV_FILE" ]; then
  cp "$DOCKER_DIR/.env.example" "$ENV_FILE"
  yellow "Created $ENV_FILE from .env.example. Edit secrets before continuing."
fi

green "[2/5] Starting docker-compose stack"
cd "$DOCKER_DIR"
docker compose up -d

green "[3/5] Waiting for PostgreSQL"
for i in $(seq 1 60); do
  if docker compose exec -T postgres pg_isready -U "${POSTGRES_USER:-hopeup}" >/dev/null 2>&1; then
    break
  fi
  sleep 2
  if [ "$i" -eq 60 ]; then
    red "Postgres did not become ready in time"
    docker compose logs postgres
    exit 1
  fi
done

green "[4/5] Running migrations"
"$REPO_ROOT/scripts/migrate.sh"

green "[5/5] Seeding initial data"
"$REPO_ROOT/scripts/seed.sh"

green "Done. Visit:"
echo "  Frontend: http://localhost:3000"
echo "  API:      http://localhost:8000/docs"
echo "  Kibana:   http://localhost:5601"
