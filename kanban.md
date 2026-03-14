# PFP Telegram Bot — Kanban Board

> **Source of truth** for the People for Peace bot development.
> Last updated: March 14, 2026

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
| Latest deploy | `35313a2` (Mar 14) |

---

*Effort: XS (<1h) · S (1-3h) · M (3-8h) · L (1-2d)*
