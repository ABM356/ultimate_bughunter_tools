#!/bin/bash
# ─────────────────────────────────────────────────────────────
# HopeUp Deployment Script — DigitalOcean Droplet
# Run this on your DigitalOcean Droplet after running setup.sh
# ─────────────────────────────────────────────────────────────

set -euo pipefail

DEPLOY_DIR="/opt/hopeup"
COMPOSE_FILE="docker-compose.production.yml"

cd "$DEPLOY_DIR"

echo "[*] Pulling latest images..."
docker compose -f "$COMPOSE_FILE" pull

echo "[*] Stopping running services..."
docker compose -f "$COMPOSE_FILE" down

echo "[*] Starting services..."
docker compose -f "$COMPOSE_FILE" up -d

echo "[*] Waiting for backend to be healthy..."
for i in {1..30}; do
    if docker compose -f "$COMPOSE_FILE" exec -T backend curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "[+] Backend is healthy"
        break
    fi
    sleep 2
done

echo "[*] Running database migrations..."
docker compose -f "$COMPOSE_FILE" exec -T backend alembic upgrade head

echo "[*] Cleaning up old images..."
docker image prune -f

echo ""
echo "[+] Deployment complete"
echo ""
echo "Services running at:"
echo "  Frontend  →  https://app.hopeuptech.ca"
echo "  API       →  https://api.hopeuptech.ca"
echo "  API Docs  →  https://api.hopeuptech.ca/docs"
echo "  Status    →  https://status.hopeuptech.ca"
echo ""

docker compose -f "$COMPOSE_FILE" ps
