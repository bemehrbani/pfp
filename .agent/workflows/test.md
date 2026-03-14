---
description: How to run tests and find testing resources for PFP
---

# PFP Testing Workflow

## Key Files & Locations

| What | Path | Description |
|------|------|-------------|
| **Testing Docs** | `TESTING.md` | Comprehensive test suite documentation |
| **E2E Smoke Test** | `test_playwright.py` | Quick Playwright smoke test for the dashboard |
| **Telegram E2E Suite** | `telegram-bot/test_live_telegram.py` | Full Playwright suite automating Telegram Web |
| **Landing Page Tests** | `telegram-bot/test_landing_page.py` | Playwright tests for the public landing page |
| **E2E Report** | `e2e-report/index.html` | Pre-built HTML report from the last E2E run |
| **E2E Screenshots** | `e2e-report/media/` | Screenshots captured during E2E tests |
| **Test Runner Script** | `run_tests.sh` | Shell script to run Django unit tests |
| **Backend Unit Tests** | `backend/apps/*/tests.py` | Django unit tests (5 apps: users, campaigns, tasks, analytics, telegram) |

## Before Any Testing Task

> **ALWAYS read `TESTING.md` and review the files above before planning any test-related work.**
> Do NOT create new test scripts if existing ones already cover the need.

## Running Django Unit Tests

```bash
# All tests (Docker)
docker-compose exec backend python manage.py test

# Specific app
docker-compose exec backend python manage.py test apps.campaigns

# With coverage
docker-compose exec backend coverage run manage.py test
docker-compose exec backend coverage report
```

## Running E2E Playwright Tests

### Prerequisites
- Python 3.10+ with `playwright` installed (`pip install playwright`)
- Playwright browsers installed (`playwright install chromium`)
- A valid Telegram session at `telegram-bot/telegram_session.json` (for Telegram E2E)

### Telegram Bot E2E (Full Suite)
```bash
cd telegram-bot
python test_live_telegram.py
```
This automates the full volunteer journey through Telegram Web:
registration → language selection → campaign browsing → joining → task viewing → proof submission.

Screenshots are saved to `test_screenshots/` and compiled into `e2e-report/`.

### Dashboard Smoke Test
```bash
python test_playwright.py
```
Quick check that `peopleforpeace.live/dashboard` loads. Screenshot saved to `/tmp/pfp_home.png`.

## Generating E2E Reports

The existing `e2e-report/index.html` is a styled dark-theme HTML report with:
- Test suites grouped by feature area (Registration, Navigation, Tasks, Proof, etc.)
- Expandable cards with descriptions and screenshots
- Stats bar (total/passed/failed/bugs fixed)

To create a campaign-specific report, duplicate and modify this template.
