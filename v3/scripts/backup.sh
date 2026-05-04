#!/usr/bin/env bash
# HopeUp backup utility.
#
# Performs a point-in-time backup of:
#   - PostgreSQL (pg_dump) -> S3 bucket / local
#   - Elasticsearch (snapshot API) -> S3 repo
#
# Designed to be invoked from a CronJob or beat-scheduled task.
# Retention is enforced by the bucket lifecycle (see s3.tf).
set -euo pipefail

TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP_DIR="${BACKUP_DIR:-/var/backups/hopeup/$TIMESTAMP}"
S3_BUCKET="${S3_BUCKET:-}"
ENVIRONMENT="${ENVIRONMENT:-dev}"

mkdir -p "$BACKUP_DIR"

green() { printf "\033[32m%s\033[0m\n" "$*"; }
red()   { printf "\033[31m%s\033[0m\n" "$*" >&2; }

require() { command -v "$1" >/dev/null 2>&1 || { red "Missing: $1"; exit 1; }; }
require pg_dump
require curl
require jq

# ----- Postgres -----
green ">> Backing up Postgres"
PG_DUMP_FILE="$BACKUP_DIR/postgres-${ENVIRONMENT}-${TIMESTAMP}.sql.gz"
PGPASSWORD="${POSTGRES_PASSWORD:?missing POSTGRES_PASSWORD}" \
  pg_dump \
    --host="${POSTGRES_HOST:-postgres}" \
    --port="${POSTGRES_PORT:-5432}" \
    --username="${POSTGRES_USER:-hopeup}" \
    --dbname="${POSTGRES_DB:-hopeup}" \
    --format=custom \
    --no-owner \
    --no-acl \
    --verbose \
  | gzip -9 > "$PG_DUMP_FILE"

green ">> Postgres dump: $(du -h "$PG_DUMP_FILE" | awk '{print $1}')"

# ----- Elasticsearch -----
ES_HOST="${ELASTICSEARCH_HOST:-elasticsearch}"
ES_PORT="${ELASTICSEARCH_PORT:-9200}"
ES_AUTH="${ELASTICSEARCH_USERNAME:-elastic}:${ELASTICSEARCH_PASSWORD:-}"
ES_REPO="${ELASTICSEARCH_REPO:-hopeup-snapshots}"
ES_SNAPSHOT="snapshot-${ENVIRONMENT}-${TIMESTAMP}"

green ">> Triggering Elasticsearch snapshot $ES_SNAPSHOT"
curl -fsS -u "$ES_AUTH" -X PUT \
  "http://$ES_HOST:$ES_PORT/_snapshot/$ES_REPO/$ES_SNAPSHOT?wait_for_completion=true" \
  -H 'Content-Type: application/json' \
  -d '{"indices": "*", "ignore_unavailable": true, "include_global_state": false}' \
  | jq '.' > "$BACKUP_DIR/es-snapshot-${TIMESTAMP}.json"

# ----- Upload to S3 (if configured) -----
if [ -n "$S3_BUCKET" ]; then
  require aws
  green ">> Uploading to s3://$S3_BUCKET/backups/$ENVIRONMENT/$TIMESTAMP/"
  aws s3 cp --recursive "$BACKUP_DIR" "s3://$S3_BUCKET/backups/$ENVIRONMENT/$TIMESTAMP/"
fi

green ">> Backup complete: $BACKUP_DIR"
