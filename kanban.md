# PFP Telegram Bot — Kanban Board

> **Source of truth** for the People for Peace bot development.
> Last updated: March 15, 2026

---

## 🎯 Current Objective

**Make Twitter tasks as easy as possible for normal, non-technical users.**

Core flow: User starts → joins campaign → picks a tweet → 1-tap posts on Twitter → pastes URL → done.

---

## 🔥 Sprint — Gamified Activist UX (Priority Order)

> **Goal**: Activists can see, do, and feel the impact of each task — with social proof and progress tracking.

| # | Task | Description | Effort | Status |
|---|------|-------------|--------|--------|
| T1 | **1-tap tweet deep links** | `twitter.com/intent/tweet?text=...` buttons | XS | ✅ `3b3f583` |
| T2 | **Sample tweets as buttons** | Numbered visual list + "📲 Post This Tweet" per tweet | S | ✅ `3b3f583` |
| T3 | **Guided 3-step flow** | "① Pick tweet → ② Post → ③ Paste URL" | S | ✅ `3b3f583` |
| T4 | **"Next Task" after proof** | 🎯 "Do Another Task" button after confirmation | XS | ✅ `3b3f583` |
| T5 | **Back navigation** | "↩️ Back to Tasks" button on detail/guidance | XS | ✅ `3b3f583` |
| G1 | **2-click flow** | Skip task detail — claim+guide on first tap | S | ✅ `1639f67` |
| G2 | **Task checklist** | ✅/⬜/🚧 status per user + progress bar | S | ✅ `1639f67` |
| G3 | **Community pulse** | "27 activists active · 847 total actions" after proof | XS | ✅ `1639f67` |
| E1 | **Copy E2E Report Media** | Copy Suite 7-11 WebPs and PNGs to `e2e-report/media/` | XS | ⬜ TODO |
| E2 | **Update E2E HTML Report** | Add Suite 7-11 markup and video sections to `index.html` | S | ⬜ TODO |
| E3 | **Update E2E Documentation** | Log final suite outcomes in `walkthrough.md` and `task.md` | XS | ⬜ TODO |
| L1 | **Deploy Leaderboard/Points Removal** | Commit, push, deploy, and verify the removal of leaderboard and points UI | S | TODO |
| OG1 | **Page-specific OG images** | Memorial, evidence, landing OG cards + data.html OG tags added | XS | ✅ |
| V1 | **Show description in retweet flow** | `twitter_retweet` handler now shows `localized_description()` above 3-step instructions | XS | ✅ `35313a2` |
| V2 | **Resource link button after accept** | Adds `📚 View Report Library` button (uses `target_url`) in retweet guided flow | XS | ✅ `35313a2` |
| V3 | **Update Task #16 Admin fields** | Set `instructions` + `target_url` in Django Admin for Amplify Investigative Reports | XS | ✅ |
| V4 | **T1 interactive child picker** | Volunteer picks child → bot sends photo + ready tweet + 1-tap intent link | M | ✅ `cfcc777` |

---

## 📢 Epic — Pinned Campaign Dashboard Message

> **Goal**: Send a rich, auto-updating "campaign dashboard" message to the `@people4peace` Telegram channel. The message shows the campaign definition, objectives, key results with live statistics, available tasks, and a **Join** button. It gets **pinned** and **edited in-place every hour** with the latest data — so the channel always has a single, up-to-date campaign overview.

### Architecture

- **Compose**: Build a branded HTML message using `brand_constants.py` and live data from `Campaign` model + `_db_get_campaign_pulse()`.
- **Post & Pin**: Send the message via the bot, pin it, and persist the `telegram_message_id` to the `Campaign` model (new field: `pinned_dashboard_message_id`).
- **Auto-refresh**: A Celery Beat periodic task runs every hour, re-queries stats, and calls `bot.edit_message_text()` on the stored message ID.
- **Manual trigger**: Admin command `/refresh_dashboard` to force an immediate update.

### Message Content Layout

```
🕊️ People for Peace
━━━━━━━━━━━━━━━━━━━

📢 Justice for Minab Children

On Feb 28, 2026, 168 children aged 7-12 were killed
in a US cruise missile strike on their school in Minab, Iran.
We demand accountability. Your voice matters.

━━━━━━━━━━━━━━━━━━━
📊 Objectives & Key Results
━━━━━━━━━━━━━━━━━━━

🎯 Volunteers:  ██████████░  45/100
📝 Actions:     ████░░░░░░░  87/500
🐦 Tweets:      ███░░░░░░░░  34/200

📈 Overall progress: 33%

━━━━━━━━━━━━━━━━━━━
🎯 Available Tasks
━━━━━━━━━━━━━━━━━━━

🐦 Share a Child's Story  (5 min)
🔁 Amplify Investigative Reports  (3 min)
💬 Comment on Key Tweets  (5 min)
✍️ Create Original Content  (30 min)
✍️ Sign the Petition  (2 min)

━━━━━━━━━━━━━━━━━━━
🔗 Resources
🕯 Memorial — peopleforpeace.live
📄 Evidence — peopleforpeace.live/evidence.html
📊 Data — peopleforpeace.live/data.html

🕊️ People for Peace · peopleforpeace.live
🔄 Last updated: 12:00 PM · Mar 15, 2026
```

[➕ Join the Campaign]  ← InlineKeyboardButton (deep-link)

### Tasks

| # | Task | Description | Effort | Status |
|---|------|-------------|--------|--------|
| P1 | **Add `pinned_dashboard_message_id` field** | New `BigIntegerField` on `Campaign` model to store the Telegram message ID of the pinned dashboard. Migration required. | XS | ✅ Done |
| P2 | **`compose_dashboard_message()` helper** | Pure function that takes a campaign + pulse stats and returns `(html_text, inline_keyboard)`. Builds branded HTML with OKR progress bars (Unicode block chars), task list, resource links, timestamp, and a "Join" deep-link button. Lives in `telegram-bot/utils/dashboard.py`. | M | ✅ Done |
| P3 | **`/post_dashboard` admin command** | Bot command (admin-only) that calls `compose_dashboard_message()`, sends it to the channel, pins it, and saves the `telegram_message_id` back to `Campaign.pinned_dashboard_message_id`. | S | ✅ Done |
| P4 | **`/refresh_dashboard` admin command** | Bot command (admin-only) that re-composes and calls `bot.edit_message_text()` on the stored pinned message. Useful for manual refresh after content changes. | XS | ✅ Done |
| P5 | **Celery Beat periodic task** | Register `update_campaign_dashboards` in Celery Beat schedule (every 60 min). The task instantiates a Bot client, loads active campaigns with a `pinned_dashboard_message_id`, re-composes, and edits each message. | M | ✅ Done |
| ~~P6~~ | ~~**Bilingual support (EN/FA)**~~ | ~~Dropped — English-only per campaign decision.~~ | — | ⏭ Skipped |
| P7 | **Progress bar rendering** | Unicode progress bar util (`█░` chars) that takes `(current, target)` and returns a 10-char visual bar + percentage. Reusable across bot messages. | XS | ✅ Done |
| P8 | **Deploy & verify** | Deploy to production, run `/post_dashboard` in bot, verify message appears in `@people4peace`, pin it, then wait 1 hour to confirm auto-refresh edits the message. | S | ✅ Done `e198dc3` |
| P9 | **Bot profile improvements** | Updated BotFather settings: new botpic (dove avatar), improved About text, structured Description with task list, registered 8 slash commands. | XS | ✅ Done |

---

## 🎨 Epic — Art for Peace (Content Creation Viral Loop)

> **Goal**: Turn content creation into a viral flywheel — artists create for the cause, art is showcased on a gallery page, volunteers share it on Twitter, and new artists/volunteers join. Leverages existing NFT artist network.

### The Flywheel

```
Artists create → Submit via bot → Gallery + Channel post → Volunteers share on X → New visitors → New artists & volunteers → Repeat
```

### Tasks

| # | Task | Description | Effort | Status |
|---|------|-------------|--------|--------|
| A1 | **Improve T4 task** | Update instructions, points (10→30), add gallery link + content ideas. Django Admin fields. | XS | ⬜ TODO |
| A2 | **Build `gallery.html`** | Showcase page matching `amplify.html` design. Masonry grid, artist credit, share-on-X buttons, "Create Your Own" CTA. | M | ⬜ TODO |
| A3 | **Bot artwork submission flow** | Credit prompt (named/anon) → media upload → save `ArtworkSubmission` → channel post → artist confirmation. | M | ⬜ TODO |
| A4 | **`ArtworkSubmission` model + migration** | New model in `tasks/models.py`: media file ID, artist info, credit flag, publish state, channel message ID. | S | ⬜ TODO |
| A5 | **Admin gallery commands** | `/gallery_list`, `/gallery_remove <id>` — admin bot commands for moderation-after. | XS | ⬜ TODO |
| A6 | **Artist outreach email** | Template email for NFT artist network. Cause context + how to submit + two credit options. | XS | ⬜ TODO |
| A7 | **Update translations** | New keys: credit prompt, submission success, gallery button labels (EN/FA/AR). | S | ⬜ TODO |
| A8 | **Deploy & verify** | Push, migrate, test full loop: submit art → channel post → gallery page. | S | ⬜ TODO |

---

## 🐛 Known Bugs

| # | Bug | Severity | Status |
|---|-----|----------|--------|
| B1 | Leaderboard Markdown parse error (em dash) | High | Fix staged (switch to HTML) |
| B2 | Menu campaigns wrong filter (`is_active` → `status=ACTIVE`) | High | ✅ Fixed |
| B3 | Menu leaderboard wrong field (`points` → `total_points`) | Medium | ✅ Fixed |
| B4 | Profile shows 0 points (`user.points` → `user.total_points`) | Low | TODO |
| B6 | Menu "Available Tasks" no per-task buttons | Medium | Deferred |
| B7 | **Channel broadcasts silent fail** — `telegram_channel_id` NULL on production campaigns; all broadcasts silently return | High | ✅ Fixed (warning logs + `resolve_channel_id` command) |

---

## ✅ Completed (This Sprint)

| # | Task | Status |
|---|------|--------|
| C1 | `/start` → welcome + inline menu | ✅ |
| C2 | Browse Campaigns → campaign list | ✅ |
| C3 | Campaign detail view (`campaign_{id}` callback) | ✅ `a23b7d9` |
| C4 | Join Campaign → inline "View Tasks" button | ✅ `a23b7d9` |
| C5 | View Campaign Tasks → task list with buttons | ✅ |
| C6 | Task Detail → "Start Task" button | ✅ |
| C7 | Start Task → claim + guidance (sample tweets) | ✅ |
| C8 | Submit Proof → confirmation prompt | ✅ |
| C9 | Confirm Proof → success message | ✅ |
| C10 | Core flow E2E test (10 steps, 0 failures) | ✅ `a23b7d9` |

---

## ⏳ Deferred

| # | Feature | Priority | Notes |
|---|---------|----------|-------|
| T6 | Fix profile points (B4) | Low | `menu.py:138` |
| T7 | Deploy leaderboard HTML fix (B1) | Low | Already staged |
| D0 | **Fix Duplicate Migrations (Data Loss Prevention)** | High | ✅ Fixed |
| D2 | Deep-link auto-join (`/start campaign_18`) | Medium | ✅ Implemented & deployed |
| D2 | Task completion notification to admin | Medium | Review workflow |
| D3 | Points auto-award on proof approval | Medium | Gamification |
| D4 | Invite task type testing | Low | After Twitter tasks stable |
| D5 | Campaign progress dashboard | Low | |
| D6 | Publish Platform Guide for Campaign Managers | Medium | **Options**: 1) Password-protected page on main site, 2) Behind campaign manager login wall. Needs technical decision. |

---

## 📊 Production Data

| Metric | Value |
|--------|-------|
| Active campaigns | 1 (`Justice for Minab Children`) |
| Tasks in campaign | 5 (tweet post, retweet, comment, content creation, petition) |
| Campaign members | growing |
| Bot username | `@peopleforpeacebot` |
| Server | 65.109.198.200 |
| Latest deploy | `e198dc3` (Mar 15 — pinned dashboard + bot profile) |

---

*Effort: XS (<1h) · S (1-3h) · M (3-8h) · L (1-2d)*
