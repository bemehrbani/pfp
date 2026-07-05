#!/bin/bash
# PFP Server Health Report
# Sends a comprehensive Telegram report every 6 hours
#
# Cron: 0 */6 * * * /opt/pfp/infrastructure/scripts/server-health-report.sh
#
# Server layout:
#   /opt/pfp.git  — bare repo (contains git data, NO remotes configured)
#   /opt/pfp      — work tree (no .git dir, just checked-out files)
#   All git commands must use: git --git-dir=/opt/pfp.git --work-tree=/opt/pfp
#
# Note: Server cannot reach GitHub (private repo, no SSH/HTTPS keys).
#       Drift detection relies on the deploy workflow always pushing to both
#       remotes. This report shows current deploy state only.

set -euo pipefail

PROJECT_DIR="/opt/pfp"
GIT_DIR="/opt/pfp.git"
GIT="git --git-dir=${GIT_DIR} --work-tree=${PROJECT_DIR}"
COMPOSE_FILES="-f docker-compose.production.yml -f docker-compose.stealth.yml"
BOT_TOKEN="8743296270:AAFny3S8Cp3WtcqpROlcPMfbFptLtUlI3Lc"
ALERT_CHAT_ID="23932283"

cd "$PROJECT_DIR"

# ─── 1. Deploy Status ───
DEPLOYED=$($GIT rev-parse --short HEAD 2>/dev/null || echo "unknown")
DEPLOYED_MSG=$($GIT log -1 --format='%s' 2>/dev/null | head -c 50 || echo "unknown")
DEPLOY_DATE=$($GIT log -1 --format='%cd' --date=format:'%Y-%m-%d %H:%M' 2>/dev/null || echo "unknown")
DEPLOY_AGO=$($GIT log -1 --format='%cr' 2>/dev/null || echo "unknown")

# ─── 2. Service Health ───
ALL_HEALTHY=true
SERVICE_COUNT=0
DOWN_LIST=""
while IFS= read -r line; do
  NAME=$(echo "$line" | awk '{print $1}' | sed 's/pfp-//;s/-1//')
  STATUS=$(echo "$line" | cut -d' ' -f2-)
  SERVICE_COUNT=$((SERVICE_COUNT + 1))
  if ! echo "$STATUS" | grep -qi "up"; then
    DOWN_LIST="${DOWN_LIST}  - ${NAME}\n"
    ALL_HEALTHY=false
  fi
done < <(docker compose $COMPOSE_FILES ps --format '{{.Name}} {{.Status}}' 2>/dev/null)

if [ "$ALL_HEALTHY" = true ]; then
  SERVICE_LINE="All ${SERVICE_COUNT} services up"
else
  SERVICE_LINE="Issues:\n${DOWN_LIST}"
fi

# ─── 3. Backend Health Check ───
HEALTH_RAW=$(curl -sf --max-time 5 http://localhost:8001/health/simple/ 2>/dev/null || echo "")
if echo "$HEALTH_RAW" | grep -q "ok"; then
  HEALTH_LINE="OK"
else
  HEALTH_LINE="FAILED"
fi

# ─── 4. Backup Status ───
BACKUP_DIR="$PROJECT_DIR/infrastructure/postgres/backups"

LATEST_DAILY=$(ls -t "$BACKUP_DIR/daily/" 2>/dev/null | head -1)
if [ -n "$LATEST_DAILY" ]; then
  DAILY_SIZE=$(du -h "$BACKUP_DIR/daily/$LATEST_DAILY" | cut -f1)
  DAILY_LINE="${LATEST_DAILY} (${DAILY_SIZE})"
else
  DAILY_LINE="None found!"
fi

LATEST_PREDEPLOY=$(ls -t "$BACKUP_DIR/pre-deploy/" 2>/dev/null | head -1)
if [ -n "$LATEST_PREDEPLOY" ]; then
  PREDEPLOY_SIZE=$(du -h "$BACKUP_DIR/pre-deploy/$LATEST_PREDEPLOY" | cut -f1)
  PREDEPLOY_LINE="${LATEST_PREDEPLOY} (${PREDEPLOY_SIZE})"
else
  PREDEPLOY_LINE="None"
fi

DAILY_COUNT=$(ls "$BACKUP_DIR/daily/" 2>/dev/null | wc -l | tr -d ' ')
WEEKLY_COUNT=$(ls "$BACKUP_DIR/weekly/" 2>/dev/null | wc -l | tr -d ' ')
MONTHLY_COUNT=$(ls "$BACKUP_DIR/monthly/" 2>/dev/null | wc -l | tr -d ' ')

# ─── 5. App Statistics ───
STATS=$(docker compose $COMPOSE_FILES exec -T backend python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
from apps.campaigns.models import Campaign, CampaignVolunteer
from apps.tasks.models import TaskAssignment
from django.utils import timezone
from datetime import timedelta
day_ago = timezone.now() - timedelta(days=1)
print(f'users={User.objects.count()}')
print(f'volunteers={CampaignVolunteer.objects.count()}')
print(f'campaigns={Campaign.objects.count()}')
print(f'assignments={TaskAssignment.objects.count()}')
print(f'new_users_24h={User.objects.filter(date_joined__gte=day_ago).count()}')
" 2>/dev/null | grep '=' || echo "")

USERS=$(echo "$STATS" | grep '^users=' | cut -d= -f2)
VOLUNTEERS=$(echo "$STATS" | grep '^volunteers=' | cut -d= -f2)
CAMPAIGNS=$(echo "$STATS" | grep '^campaigns=' | cut -d= -f2)
ASSIGNMENTS=$(echo "$STATS" | grep '^assignments=' | cut -d= -f2)
NEW_USERS=$(echo "$STATS" | grep '^new_users_24h=' | cut -d= -f2)

# ─── 6. Server Resources ───
DISK_USAGE=$(df -h / | tail -1 | awk '{print $5}')
DISK_AVAIL=$(df -h / | tail -1 | awk '{print $4}')
MEM_TOTAL=$(free -h | awk '/Mem:/{print $2}')
MEM_USED=$(free -h | awk '/Mem:/{print $3}')
UPTIME_STR=$(uptime -p | sed 's/up //')

# ─── Build Message (plain text, no Markdown) ───
TIMESTAMP=$(date '+%b %d, %H:%M UTC')

read -r -d '' MESSAGE << MSGEOF || true
📊 PFP Health Report — ${TIMESTAMP}

🚀 Deploy
  ${DEPLOYED} — ${DEPLOYED_MSG}
  Deployed: ${DEPLOY_DATE} (${DEPLOY_AGO})

🐳 Services: ${SERVICE_LINE}
🏥 API: ${HEALTH_LINE}

💾 Backups
  Latest: ${DAILY_LINE}
  Kept: ${DAILY_COUNT} daily / ${WEEKLY_COUNT} weekly / ${MONTHLY_COUNT} monthly
  Pre-deploy: ${PREDEPLOY_LINE}

👥 Stats
  Users: ${USERS:-?} (new 24h: ${NEW_USERS:-0})
  Volunteers: ${VOLUNTEERS:-?}
  Campaigns: ${CAMPAIGNS:-?}
  Tasks claimed: ${ASSIGNMENTS:-?}

💻 Server
  Disk: ${DISK_USAGE} used (${DISK_AVAIL} free)
  RAM: ${MEM_USED} / ${MEM_TOTAL}
  Uptime: ${UPTIME_STR}
MSGEOF

# ─── Send via Telegram ───
curl -sf -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  --data-urlencode "chat_id=${ALERT_CHAT_ID}" \
  --data-urlencode "text=${MESSAGE}" \
  > /dev/null 2>&1

echo "[$(date '+%Y-%m-%d %H:%M')] Health report sent"
