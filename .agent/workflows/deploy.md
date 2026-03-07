---
description: Deploy PFP to production (SkinScope server)
---

# Deploy PFP to Production

## Quick Deploy (Bare Git Push)

Deploy the current branch to production with a single command:

// turbo
1. Push to the deploy remote:
```bash
cd /Users/mahdifarimani/Documents/PFP && GIT_SSH_COMMAND="ssh -i /Users/mahdifarimani/Documents/PFP/infrastructure/deploy_key -o StrictHostKeyChecking=no" git push deploy main
```

The post-receive hook automatically:
- Checks out code to `/opt/pfp`
- Rebuilds Docker containers
- Runs migrations
- Performs a health check

## Manual SSH Access

// turbo
2. SSH into the server:
```bash
ssh -o StrictHostKeyChecking=no -i /Users/mahdifarimani/Documents/PFP/infrastructure/deploy_key root@65.109.198.200
```

## Check Service Status

// turbo
3. Check service health:
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
