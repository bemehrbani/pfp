# Project Context: PFP (People for Peace) Campaign Manager

## Project Overview
PFP is a Campaign Manager Platform with two main components:
1. **Frontend / Web Portal**: Trilingual (EN/FA/AR) landing pages (e.g. at `peopleforpeace.live`) to advocate, display evidence, provide campaign guides, and direct users to the Telegram bot.
2. **Backend & Telegram Bot (Django)**: Built with Django and `python-telegram-bot`, utilizing background Celery tasks. Organizes peace-building operations (like Twitter Storms), volunteer participation, and user tracking.

## Technical Stack
- **Backend**: Django, Django REST Framework, Celery, PostgreSQL, Redis.
- **Bot Engine**: `python-telegram-bot` integrated asynchronously into Django ORM.
- **Frontend**: HTML/JS/CSS public landing pages + React admin dashboard.
- **Deployment**: Docker Compose, Nginx, typically deployed to a VPS (e.g., SkinScope Server) via post-receive git hook.
- **Testing**: Playwright for frontend & E2E tests, Django test suit for backend APIs.

## Key Architectures & Behaviors
- **Telegram Bot Username**: `@peopleforpeacebot` 
  - Direct Link: `https://t.me/peopleforpeacebot`
- **Registration Flow (1-Click)**: The bot automatically registers users by persisting their Telegram first/last names. The old requirement for typing names manually has been removed. They simply choose a language, and immediately receive the main menu.
- **Deep-linking & Auto-Join**: Supports query payloads (e.g., `?start=campaign_16`) to auto-enroll members upon first start.
- **UI State**: Controlled by `ConversationStateManager` tracking DB fields within the `CampaignUser` model.

## Agent Instructions & Rules
- **DO NOT HALLUCINATE CONSTANTS**: The bot username is `peopleforpeacebot`. ALWAYS check existing `.env`, source code constants, or `translations.py`/`i18n.js` files instead of guessing values for domains or usernames. 
- ALWAYS refer to this file for baseline orientation when starting new E2E tests or backend architecture updates.
