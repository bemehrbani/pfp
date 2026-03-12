# PFP Telegram Bot — Kanban Board

> **Source of truth** for the People for Peace bot development.
> Last updated: March 12, 2026

---

## 🎯 Current Objective

**Make the #StopTrumpMadness campaign fully operational via the Telegram bot.**

Core flow: User starts → joins campaign → completes Twitter tasks (tweet, comment, retweet) → submits proof → earns points.

---

## 🐛 Known Bugs

| # | Bug | Severity | Location | Status |
|---|-----|----------|----------|--------|
| B1 | **Leaderboard Markdown parse error** — em dash (`—`) in `*Leaderboard — Top 5*` causes Telegram `Can't parse entities` error | High | `menu.py:177` | Fix staged (switch to HTML parse mode) |
| B2 | **Menu campaigns wrong filter** — was using `is_active=True` instead of `status=ACTIVE` | High | `menu.py:42` | ✅ Fixed in `d525ee8` |
| B3 | **Menu leaderboard wrong field** — ordering by `points` instead of `total_points` | Medium | `menu.py:172` | ✅ Fixed in `d525ee8` |
| B4 | **Menu profile shows 0 points** — uses `user.points` instead of `user.total_points` | Low | `menu.py:138` | TODO |
| B5 | **E2E test task button selector grabs wrong buttons** — `.reply-markup button` in Step 8 clicks "Browse Campaigns" instead of a task button | Low | `test_live_telegram.py` | TODO (test improvement) |
| B6 | **Menu "Available Tasks" simplified view** — shows task list text but no individual task action buttons (View Tasks flow needs to show per-task buttons) | Medium | `menu.py:86-121` | TODO |

---

## 🔥 Sprint — Core Interaction (Priority)

> **Goal**: A user can start the bot, join the campaign, claim a Twitter task, complete it, and submit proof.

| # | Task | Handler | Status |
|---|------|---------|--------|
| C1 | `/start` → welcome + inline menu | `start.py`, `menu.py` | ✅ Working |
| C2 | **Browse Campaigns** inline button → campaign list | `menu.py` → `_handle_campaigns` | ✅ Working |
| C3 | **Join Campaign** via `/campaigns` → "Join" button | `campaigns.py` → `campaign_join_` callback | ✅ Working |
| C4 | **View Campaign Tasks** after joining | `campaigns.py` → `campaign_tasks_` callback | ✅ Working |
| C5 | **Task Detail** — tap task → description + "Start Task" button | `tasks.py` → `task_claim_` → `handle_task_detail` | ✅ Working |
| C6 | **Start Task** — claim + guidance (sample tweets for Twitter tasks) | `tasks.py` → `task_startclaim_` → `handle_task_start_and_guide` | ✅ Working |
| C7 | **Submit Proof** — user sends tweet URL → confirmation prompt | `tasks.py` → `receive_task_proof` (ConversationHandler) | ✅ Working |
| C8 | **Confirm Proof** — "Confirm Submission" → success message | `tasks.py` → `proof_confirm_` → `confirm_proof_submission` | ✅ Working |
| C9 | **E2E Test: Full core flow** — automated test covering C1-C8 | `test_live_telegram.py` | 🔨 In Progress |
| C10 | **Fix B1** — deploy leaderboard HTML parse fix | `menu.py` | 🔨 Fix staged |
| C11 | **Fix B6** — menu tasks view should show per-task action buttons | `menu.py` | TODO |

---

## ⏳ Deferred — Supporting Interactions

> These work but are lower priority. Will address after core flow is fully tested.

| # | Feature | Status | Notes |
|---|---------|--------|-------|
| D1 | My Progress / Profile | ✅ Working (shows 0 points — B4) | Fix points field |
| D2 | Leaderboard | 🔴 Bug B1 | Fix Markdown→HTML |
| D3 | Help | ✅ Working | |
| D4 | Language picker | ✅ Working | |
| D5 | `/mytasks` — user's assigned tasks | ✅ Working | |
| D6 | Invite task type | ✅ Handler exists | Test after core Twitter tasks |

---

## 📋 Backlog

| # | Task | Priority |
|---|------|----------|
| BL1 | Deep-link auto-join (`/start campaign_16`) | Medium — improves onboarding |
| BL2 | Task completion notification to campaign admin | Medium — review workflow |
| BL3 | Points auto-award on proof approval | Medium — gamification |
| BL4 | Campaign progress dashboard in bot | Low |
| BL5 | Rate limiting / cooldown between tasks | Low |
| BL6 | Photo proof download and storage | Low |

---

## 📊 Production Data

| Metric | Value |
|--------|-------|
| Active campaigns | 1 (`#StopTrumpMadness`) |
| Tasks in campaign | 6 (tweet, comment, retweet, content, invite, share) |
| Campaign members | 2 / 100 target |
| Bot username | `@peopleforpeacebot` |
| Server | 65.109.198.200 |
| Latest deploy | `d525ee8` (Mar 12) |

---

*Effort: XS (<1h) · S (1-3h) · M (3-8h) · L (1-2d)*
