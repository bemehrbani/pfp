# Project Context: PFP (People for Peace) Campaign Manager

> **Canonical reference for all AI agents operating in this workspace.**
> Last updated: March 12, 2026

---

## Project Overview

PFP is a **Campaign Manager Platform** for coordinating peace-building campaigns. It enables Campaign Managers to create campaigns, define social-media tasks (Twitter Storms), recruit volunteers via a Telegram bot, and track progress through an admin dashboard.

### Two Main Components

1. **Web Portal (React + Django)**: Admin dashboard at `http://65.109.198.200:8001/admin/login/?next=/admin/` for managing campaigns, tasks, analytics, and users.
2. **Telegram Bot (`@peopleforpeacebot`)**: Volunteer-facing interface for joining campaigns, claiming tasks, submitting proof, and earning points.
   - Direct link: `https://t.me/peopleforpeacebot`

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 4.2, Django REST Framework, Celery, PostgreSQL 15, Redis 7 |
| **Bot Engine** | `python-telegram-bot` integrated async with Django ORM |
| **Frontend** | React 18 + TypeScript + Tailwind CSS + TanStack Query |
| **Infrastructure** | Docker Compose, Nginx, Traefik (production), Gunicorn |
| **Auth** | JWT (djangorestframework-simplejwt) |
| **Testing** | Django TestCase (backend), Playwright (E2E), pytest |

---

## Project Structure

```
PFP/
├── backend/                     # Django backend
│   ├── apps/
│   │   ├── users/               # Auth, user profiles, roles
│   │   ├── campaigns/           # Campaign CRUD, volunteers, updates
│   │   ├── tasks/               # Task management, assignments, proofs
│   │   ├── analytics/           # ActivityLog, dashboard stats
│   │   └── telegram/            # Telegram session/message models
│   └── config/                  # Django settings (dev/prod)
├── telegram-bot/                # Standalone Telegram bot service
│   ├── bot.py                   # Entry point (polling/webhook modes)
│   ├── handlers/
│   │   ├── start.py             # /start + deep-link auto-join
│   │   ├── registration.py      # 1-click registration flow
│   │   ├── campaigns.py         # Campaign browsing/joining
│   │   ├── tasks.py             # Task claiming, proof submission
│   │   ├── menu.py              # Main menu handler
│   │   ├── profile.py           # User profile display
│   │   ├── leaderboard.py       # Points leaderboard
│   │   ├── storms.py            # Twitter storm coordination
│   │   └── db.py                # Direct DB access helpers
│   ├── keyboards/               # Inline keyboard builders
│   ├── states/                  # Conversation state definitions
│   ├── utils/                   # Shared utilities
│   └── simulator/               # Bot simulator for testing
├── frontend/                    # React admin dashboard
│   └── src/
│       ├── pages/
│       │   ├── Dashboard.tsx
│       │   ├── Login.tsx
│       │   ├── Campaigns.tsx
│       │   ├── CampaignCreate.tsx   # Campaign creation form
│       │   ├── Tasks.tsx
│       │   ├── TaskCreate.tsx       # Task creation form
│       │   └── Analytics.tsx
│       ├── components/          # Reusable UI components
│       ├── hooks/               # Custom React hooks
│       ├── api/                 # Axios API client
│       ├── types/               # TypeScript type definitions
│       └── utils/               # Utility functions
├── infrastructure/              # Deployment configs
│   ├── traefik/                 # Reverse proxy + SSL
│   ├── postgres/                # DB configs
│   ├── monitoring/              # System monitoring
│   └── scripts/                 # Deployment scripts
├── e2e-report/                  # Playwright E2E test HTML report & screenshots
│   ├── index.html               # Styled dark-theme report
│   └── media/                   # Captured screenshots
├── minab/                       # Justice for Minab campaign assets
├── justiceForMinab/             # Minab campaign docs & action plan
├── TESTING.md                   # Comprehensive test suite documentation
├── test_playwright.py           # Playwright smoke test for dashboard
├── kanban.md                    # Development task board
├── campaign.md                  # Campaign & content task board
├── docker-compose.yml           # Dev environment (6 services)
├── docker-compose.production.yml
├── Makefile                     # Dev shortcuts
├── deploy.sh                    # Production deploy script
├── kanban.md                    # Sprint board (source of truth)
└── .agent/
    ├── Context.md               # ← THIS FILE
    └── workflows/
        └── deploy.md            # Production deployment steps
```

---

## Services & Ports (Development)

| Service | Port | Description |
|---------|------|-------------|
| `postgres` | `5433:5432` | PostgreSQL 15 (DB: `pfp_campaign`, User: `pfp_user`) |
| `redis` | `6380:6379` | Redis 7 (Celery broker + cache) |
| `backend` | `8001:8000` | Django API + Admin (`/admin/`, `/swagger/`, `/api/`) |
| `celery` | — | Background task worker |
| `celery-beat` | — | Periodic task scheduler |
| `telegram-bot` | — | Bot in polling mode |
| `frontend` | `3000:80` | React dashboard |

---

## Key Behaviors & Architecture

### Registration Flow (1-Click)
The bot auto-registers users by persisting their Telegram `first_name`/`last_name`. Users simply choose a language and immediately receive the main menu. No manual name entry required.

### Deep-Linking & Auto-Join
Supports query payloads (e.g., `?start=campaign_16`) to auto-enroll members upon first `/start`.

### Referral System
`CampaignVolunteer` model tracks `referred_by` for invite link attribution. Points awarded to inviter when a new user joins via referral link.

### UI State Management
Controlled by `ConversationStateManager` tracking DB fields within the `CampaignUser` model.

### User Roles
- **Admin**: Full platform access, user management, system analytics
- **Campaign Manager**: Create/manage campaigns and tasks, coordinate volunteers
- **Volunteer**: Join campaigns, claim tasks, submit proofs, earn points

---

## Production Environment

| Detail | Value |
|--------|-------|
| **Domain** | `https://peopleforpeace.live` |
| **Server** | `65.109.198.200` (SkinScope Server) |
| **Frontend** | `https://peopleforpeace.live` (port 8080 behind Traefik) |
| **Bot username** | `@peopleforpeacebot` |
| **Deploy method** | `deploy.sh` → Docker Compose + Traefik + Let's Encrypt SSL |
| **Active campaigns** | `#StopTrumpMadness` (Campaign 1); `#IstandwithIran🇮🇷` (Campaign 2 — pending) |
| **Admin credentials** | `admin` / `admin123` (default from `deploy.sh`) |
| **Latest deploy** | `3b3f583` (Mar 12, 2026) |

---

## Common Commands

```bash
# Start dev environment
make up            # or: docker-compose up -d

# View logs
make logs          # or: docker-compose logs -f

# Database
make migrate       # Run migrations
make makemigrations
make shell         # Django shell

# Testing
make test          # Backend unit tests
./run_tests.sh --coverage  # With coverage

# Production deploy
./deploy.sh        # or: see .agent/workflows/deploy.md
```

---

## API Endpoints (Key)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/login/` | POST | JWT login → `{ access, refresh }` |
| `/api/campaigns/` | GET/POST | List/create campaigns |
| `/api/campaigns/{id}/` | GET/PUT/DELETE | Campaign detail |
| `/api/campaigns/{id}/join/` | POST | Volunteer joins campaign |
| `/api/tasks/` | GET/POST | List/create tasks |
| `/api/tasks/{id}/assign/` | POST | Claim a task |
| `/api/tasks/{id}/submit/` | POST | Submit proof |
| `/api/analytics/dashboard-stats/` | GET | Dashboard analytics |
| `/admin/` | — | Django admin panel |
| `/swagger/` | — | Interactive API docs |

---

## Agent Instructions & Rules

> [!CAUTION]
> **DO NOT HALLUCINATE CONSTANTS.** The bot username is `peopleforpeacebot`. ALWAYS check existing `.env`, source code, or `translations.py`/`i18n.js` files instead of guessing values for domains, usernames, or tokens.

- **Always** refer to this file for baseline orientation when starting new work.
- **Check `kanban.md`** for current sprint status and known bugs before starting feature work.
- **Check `TESTING.md`** for test suite conventions before writing tests.
- **Check `ONBOARDING.md`** for user-facing flow descriptions.
- **Never commit or push** without the user's explicit permission.
- The `.env` file in the project root contains the **local dev** bot token. The telegram-bot service has its own `.env` file at `telegram-bot/.env`.
