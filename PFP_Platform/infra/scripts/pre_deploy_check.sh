#!/usr/bin/env bash
#
# Pre-deploy migration safety check for PFP.
# Run this BEFORE deploying to catch destructive migrations.
#
# Usage:
#   ./infrastructure/scripts/pre_deploy_check.sh          # local docker-compose
#   ./infrastructure/scripts/pre_deploy_check.sh --prod   # against production
#
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

COMPOSE_CMD="docker compose"
PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

if [[ "${1:-}" == "--prod" ]]; then
    COMPOSE_FILE="-f docker-compose.production.yml"
    echo -e "${YELLOW}🔍 Running pre-deploy check against PRODUCTION config${NC}"
else
    COMPOSE_FILE=""
    echo -e "🔍 Running pre-deploy check against local dev..."
fi

cd "$PROJECT_DIR"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  1. Checking for migration conflicts"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check for unapplied migrations
PLAN=$($COMPOSE_CMD $COMPOSE_FILE exec -T backend python manage.py showmigrations --plan 2>/dev/null || echo "ERROR")

if echo "$PLAN" | grep -q "ERROR"; then
    echo -e "${RED}❌ Could not connect to backend container. Is it running?${NC}"
    exit 1
fi

UNAPPLIED=$(echo "$PLAN" | grep -c "\\[ \\]" || true)
if [[ "$UNAPPLIED" -gt 0 ]]; then
    echo -e "${YELLOW}⚠️  Found $UNAPPLIED unapplied migration(s):${NC}"
    echo "$PLAN" | grep "\\[ \\]"
else
    echo -e "${GREEN}✅ All migrations are applied.${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  2. Checking for destructive operations"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Scan migration files for destructive operations
DESTRUCTIVE_FOUND=0
MIGRATION_FILES=$(find backend/apps/*/migrations/ -name "*.py" -not -name "__init__.py" 2>/dev/null)

for file in $MIGRATION_FILES; do
    if grep -qE "RemoveField|DeleteModel|RunSQL.*DROP|AlterField.*null=False" "$file" 2>/dev/null; then
        # Only warn about unapplied destructive migrations
        migration_name=$(basename "$file" .py)
        app_name=$(echo "$file" | sed 's|backend/apps/\([^/]*\)/.*|\1|')

        if echo "$PLAN" | grep -q "\\[ \\].*$app_name.*$migration_name"; then
            echo -e "${RED}⚠️  DESTRUCTIVE: $file${NC}"
            grep -nE "RemoveField|DeleteModel|RunSQL.*DROP|AlterField.*null=False" "$file" | head -5
            DESTRUCTIVE_FOUND=1
        fi
    fi
done

if [[ "$DESTRUCTIVE_FOUND" -eq 0 ]]; then
    echo -e "${GREEN}✅ No destructive operations in pending migrations.${NC}"
else
    echo ""
    echo -e "${RED}╔══════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  ⚠️  DESTRUCTIVE MIGRATIONS DETECTED!         ║${NC}"
    echo -e "${RED}║  Review the above before deploying.          ║${NC}"
    echo -e "${RED}║  Consider: python manage.py dbbackup first   ║${NC}"
    echo -e "${RED}╚══════════════════════════════════════════════╝${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  3. Database backup status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

BACKUP_DIR="infrastructure/postgres/backups"
if [[ -d "$BACKUP_DIR" ]]; then
    LATEST=$(ls -t "$BACKUP_DIR"/*.sql.gz 2>/dev/null | head -1)
    if [[ -n "$LATEST" ]]; then
        echo -e "${GREEN}✅ Latest backup: $(basename "$LATEST")${NC}"
        echo "   Size: $(du -h "$LATEST" | cut -f1)"
    else
        echo -e "${YELLOW}⚠️  No backups found in $BACKUP_DIR${NC}"
    fi
else
    echo -e "${YELLOW}ℹ️  Backup directory not present locally (normal — backups are on server)${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [[ "$DESTRUCTIVE_FOUND" -eq 1 ]]; then
    echo -e "${RED}❌ DEPLOY BLOCKED — Review destructive migrations above.${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Safe to deploy.${NC}"
    exit 0
fi
