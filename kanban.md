# PFP Telegram Bot — Kanban Board

> **Source of truth** for the People for Peace bot development.
> Last updated: March 12, 2026

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

---

## 🐛 Known Bugs

| # | Bug | Severity | Status |
|---|-----|----------|--------|
| B1 | Leaderboard Markdown parse error (em dash) | High | Fix staged (switch to HTML) |
| B2 | Menu campaigns wrong filter (`is_active` → `status=ACTIVE`) | High | ✅ Fixed |
| B3 | Menu leaderboard wrong field (`points` → `total_points`) | Medium | ✅ Fixed |
| B4 | Profile shows 0 points (`user.points` → `user.total_points`) | Low | TODO |
| B6 | Menu "Available Tasks" no per-task buttons | Medium | Deferred |

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
| D1 | Deep-link auto-join (`/start campaign_16`) | Medium | Onboarding improvement |
| D2 | Task completion notification to admin | Medium | Review workflow |
| D3 | Points auto-award on proof approval | Medium | Gamification |
| D4 | Invite task type testing | Low | After Twitter tasks stable |
| D5 | Campaign progress dashboard | Low | |

---

## 📊 Production Data

| Metric | Value |
|--------|-------|
| Active campaigns | 1 (`#StopTrumpMadness`) |
| Tasks in campaign | 6 (tweet, comment, retweet + 3 more) |
| Campaign members | 3 / 100 target |
| Bot username | `@peopleforpeacebot` |
| Server | 65.109.198.200 |
| Latest deploy | `3b3f583` (Mar 12) |

---

*Effort: XS (<1h) · S (1-3h) · M (3-8h) · L (1-2d)*
