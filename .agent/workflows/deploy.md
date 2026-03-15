---
description: Deploy PFP to production (SkinScope server)
---

# Deploy PFP to Production

## Quick Deploy (Push to GitHub + Server)

Deploy the current branch to **both** GitHub and production in one command:

// turbo
1. Push to origin and deploy:
```bash
cd /Users/mahdifarimani/Documents/PFP && git push origin main && GIT_SSH_COMMAND="ssh -i /Users/mahdifarimani/Documents/PFP/infrastructure/deploy_key -o StrictHostKeyChecking=no" git push deploy main
```

The post-receive hook automatically:
- **💾 Takes a pre-deploy database backup** (keeps last 5 in `backups/pre-deploy/`)
- Checks out code to `/opt/pfp`
- Rebuilds Docker containers
- Runs migrations
- Performs a health check

> **Automated backups** run every 12 hours (2 AM and 2 PM UTC) via cron.
> Backup retention: 7 daily, 4 weekly, 12 monthly in `infrastructure/postgres/backups/`.

> [!IMPORTANT]
> **Always use this workflow to deploy.** Never push to only one remote.
> If you only push to `origin`, the live site will NOT update.

## Check Deploy Drift

// turbo
2. Check if server is behind GitHub:
```bash
SSH_KEY="/Users/mahdifarimani/Documents/PFP/infrastructure/deploy_key" && DEPLOYED=$(ssh -o StrictHostKeyChecking=no -i "$SSH_KEY" root@65.109.198.200 "cd /opt/pfp && git rev-parse --short HEAD") && LOCAL=$(cd /Users/mahdifarimani/Documents/PFP && git rev-parse --short origin/main) && echo "Deployed: $DEPLOYED | GitHub: $LOCAL" && [ "$DEPLOYED" = "$LOCAL" ] && echo "✅ In sync" || echo "⚠️ DRIFT DETECTED — run /deploy"
```

## Manual SSH Access

// turbo
3. SSH into the server:
```bash
ssh -o StrictHostKeyChecking=no -i /Users/mahdifarimani/Documents/PFP/infrastructure/deploy_key root@65.109.198.200
```

## Check Service Status

// turbo
4. Check service health:
```bash
SSH_KEY="/Users/mahdifarimani/Documents/PFP/infrastructure/deploy_key" && ssh -o StrictHostKeyChecking=no -i "$SSH_KEY" root@65.109.198.200 "curl -sf http://localhost:8001/health/simple/ && echo ' OK' && cd /opt/pfp && docker compose -f docker-compose.production.yml -f docker-compose.stealth.yml ps --format 'table {{.Name}}\t{{.Status}}'"
```

## Server Details

- **Server**: SkinScope (`65.109.198.200`)
- **SSH Key**: `infrastructure/deploy_key`
- **Project Path**: `/opt/pfp`
- **Bare Repo**: `/opt/pfp.git`
- **Backend**: port 8001
- **Frontend**: port 8080
