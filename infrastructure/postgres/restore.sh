#!/bin/bash
##
# PFP Campaign Manager — PostgreSQL Restore Script
#
# Usage: ./restore.sh <backup_file.sql.gz>
# Example: ./restore.sh /opt/pfp/infrastructure/postgres/backups/daily/pfp_campaign_2026-03-06.sql.gz
#
# ⚠️  WARNING: This will REPLACE the current database contents.
##

set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Usage: $0 <path-to-backup.sql.gz>"
  echo ""
  echo "Available backups:"
  BACKUP_DIR="/opt/pfp/infrastructure/postgres/backups"
  echo "  Daily:"
  ls -lh "$BACKUP_DIR/daily/"*.sql.gz 2>/dev/null || echo "    (none)"
  echo "  Weekly:"
  ls -lh "$BACKUP_DIR/weekly/"*.sql.gz 2>/dev/null || echo "    (none)"
  echo "  Monthly:"
  ls -lh "$BACKUP_DIR/monthly/"*.sql.gz 2>/dev/null || echo "    (none)"
  exit 1
fi

BACKUP_FILE="$1"
COMPOSE_DIR="/opt/pfp"
COMPOSE_CMD="docker compose -f docker-compose.production.yml -f docker-compose.stealth.yml --env-file .env.production"

if [ ! -f "$BACKUP_FILE" ]; then
  echo "ERROR: Backup file not found: $BACKUP_FILE"
  exit 1
fi

echo "⚠️  WARNING: This will REPLACE the current database."
echo "Restoring from: $BACKUP_FILE"
echo ""
read -p "Are you sure? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
  echo "Cancelled."
  exit 0
fi

echo "Stopping application services..."
cd "$COMPOSE_DIR"
$COMPOSE_CMD stop backend celery celery-beat telegram-bot 2>/dev/null

echo "Restoring database..."
gunzip -c "$BACKUP_FILE" | $COMPOSE_CMD exec -T postgres psql \
  -U "${POSTGRES_USER:-pfp_user}" \
  -d "${POSTGRES_DB:-pfp_campaign}" \
  --quiet 2>&1

echo "Restarting application services..."
$COMPOSE_CMD start backend celery celery-beat telegram-bot 2>/dev/null

echo "✅ Database restored from: $(basename "$BACKUP_FILE")"
echo "Please verify the application is working correctly."
