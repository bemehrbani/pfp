#!/bin/bash
##
# PFP Campaign Manager — Health Monitor Script
# Run every 5 minutes via cron. Checks all services and logs failures.
#
# Usage: ./monitor.sh
##

set -euo pipefail

COMPOSE_DIR="/opt/pfp"
COMPOSE_CMD="docker compose -f docker-compose.production.yml -f docker-compose.stealth.yml --env-file .env.production"
LOG_FILE="/opt/pfp/backend/logs/monitor.log"
ALERT_FILE="/opt/pfp/backend/logs/alert.log"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

alert() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ALERT: $1" | tee -a "$LOG_FILE" "$ALERT_FILE"
}

failures=0

# --- Check that critical containers are running ---
check_container() {
  local name="$1"
  local status
  status=$(cd "$COMPOSE_DIR" && $COMPOSE_CMD ps "$name" --format "{{.Status}}" 2>/dev/null | head -1)
  if echo "$status" | grep -q "Up"; then
    return 0
  else
    alert "Container $name is DOWN (status: $status)"
    failures=$((failures + 1))
    return 1
  fi
}

for svc in backend frontend postgres redis celery celery-beat telegram-bot; do
  check_container "$svc"
done

# --- Check backend HTTP endpoint ---
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://localhost:8001/health/simple/ 2>/dev/null || echo "000")
if [ "$HTTP_CODE" != "200" ]; then
  alert "Backend HTTP health check returned $HTTP_CODE"
  failures=$((failures + 1))
fi

# --- Check frontend HTTP endpoint ---
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://localhost:8080/ 2>/dev/null || echo "000")
if [ "$HTTP_CODE" != "200" ]; then
  alert "Frontend HTTP check returned $HTTP_CODE"
  failures=$((failures + 1))
fi

# --- Check disk space (warn at 80%, alert at 90%) ---
DISK_PERCENT=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$DISK_PERCENT" -ge 90 ]; then
  alert "Disk usage CRITICAL: ${DISK_PERCENT}%"
  failures=$((failures + 1))
elif [ "$DISK_PERCENT" -ge 80 ]; then
  log "WARN: Disk usage high: ${DISK_PERCENT}%"
fi

# --- Summary ---
if [ "$failures" -eq 0 ]; then
  log "OK: All checks passed (disk: ${DISK_PERCENT}%)"
else
  log "FAIL: $failures check(s) failed"
fi
