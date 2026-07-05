#!/bin/bash
##
# PFP Campaign Manager — PostgreSQL Backup Script
# Run daily via cron on the production server.
#
# Usage: ./backup.sh
# Retention: 7 daily, 4 weekly (Sunday), 12 monthly (1st of month)
##

set -euo pipefail

# --- Configuration ---
COMPOSE_DIR="/opt/pfp"
COMPOSE_CMD="docker compose -f docker-compose.production.yml -f docker-compose.stealth.yml --env-file .env.production"
BACKUP_DIR="/opt/pfp/infrastructure/postgres/backups"
LOG_FILE="/opt/pfp/backend/logs/backup.log"
DATE=$(date +%Y-%m-%d)
DAY_OF_WEEK=$(date +%u)  # 1=Mon, 7=Sun
DAY_OF_MONTH=$(date +%d)

# Retention counts
DAILY_KEEP=7
WEEKLY_KEEP=4
MONTHLY_KEEP=12

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# --- Ensure backup directory structure ---
mkdir -p "$BACKUP_DIR"/{daily,weekly,monthly}

# --- Generate backup filename ---
BACKUP_FILE="pfp_campaign_${DATE}.sql.gz"

log "Starting backup..."

# --- Run pg_dump inside the postgres container ---
cd "$COMPOSE_DIR"
$COMPOSE_CMD exec -T postgres pg_dump \
  -U "${POSTGRES_USER:-pfp_user}" \
  -d "${POSTGRES_DB:-pfp_campaign}" \
  --clean --if-exists --no-owner \
  2>>"$LOG_FILE" | gzip > "$BACKUP_DIR/daily/$BACKUP_FILE"

BACKUP_SIZE=$(du -h "$BACKUP_DIR/daily/$BACKUP_FILE" | cut -f1)
log "Daily backup created: $BACKUP_FILE ($BACKUP_SIZE)"

# --- Weekly backup (copy Sunday's daily to weekly/) ---
if [ "$DAY_OF_WEEK" -eq 7 ]; then
  cp "$BACKUP_DIR/daily/$BACKUP_FILE" "$BACKUP_DIR/weekly/$BACKUP_FILE"
  log "Weekly backup copied: $BACKUP_FILE"
fi

# --- Monthly backup (copy 1st of month to monthly/) ---
if [ "$DAY_OF_MONTH" -eq "01" ]; then
  cp "$BACKUP_DIR/daily/$BACKUP_FILE" "$BACKUP_DIR/monthly/$BACKUP_FILE"
  log "Monthly backup copied: $BACKUP_FILE"
fi

# --- Retention cleanup ---
cleanup() {
  local dir="$1"
  local keep="$2"
  local label="$3"
  local count
  count=$(find "$dir" -name "*.sql.gz" -type f 2>/dev/null | wc -l)
  if [ "$count" -gt "$keep" ]; then
    local to_remove=$((count - keep))
    find "$dir" -name "*.sql.gz" -type f -printf '%T@ %p\n' 2>/dev/null | \
      sort -n | head -n "$to_remove" | awk '{print $2}' | \
      xargs -r rm -f
    log "Cleaned $to_remove old $label backup(s)"
  fi
}

cleanup "$BACKUP_DIR/daily" "$DAILY_KEEP" "daily"
cleanup "$BACKUP_DIR/weekly" "$WEEKLY_KEEP" "weekly"
cleanup "$BACKUP_DIR/monthly" "$MONTHLY_KEEP" "monthly"

# --- Summary ---
DAILY_COUNT=$(find "$BACKUP_DIR/daily" -name "*.sql.gz" -type f | wc -l)
WEEKLY_COUNT=$(find "$BACKUP_DIR/weekly" -name "*.sql.gz" -type f | wc -l)
MONTHLY_COUNT=$(find "$BACKUP_DIR/monthly" -name "*.sql.gz" -type f | wc -l)

log "Backup complete. Retention: ${DAILY_COUNT} daily, ${WEEKLY_COUNT} weekly, ${MONTHLY_COUNT} monthly"
