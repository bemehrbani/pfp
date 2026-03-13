# PFP Platform Guide
## For Admins & Campaign Managers

> **People for Peace** is a volunteer coordination platform that runs peace-building campaigns through a Telegram bot. This guide covers everything you need to create campaigns, design tasks, manage volunteers, and monitor growth.

---

## Table of Contents

1. [Platform Overview](#1-platform-overview)
2. [Getting Started — Admin Panel](#2-getting-started--admin-panel)
3. [Creating a Campaign](#3-creating-a-campaign)
4. [Designing Campaign Tasks](#4-designing-campaign-tasks)
5. [Task Types Reference](#5-task-types-reference)
6. [The Volunteer Experience (Bot)](#6-the-volunteer-experience-bot)
7. [Invite & Referral System](#7-invite--referral-system)
8. [Twitter Storm Campaigns](#8-twitter-storm-campaigns)
9. [Telegram Channel Broadcasting](#9-telegram-channel-broadcasting)
10. [Monitoring & Analytics](#10-monitoring--analytics)
11. [Multilingual Support](#11-multilingual-support)
12. [Best Practices](#12-best-practices)

---

## 1. Platform Overview

PFP consists of three connected components:

| Component | URL | Purpose |
|-----------|-----|---------|
| **Public Website** | [peopleforpeace.live](https://peopleforpeace.live) | Landing page, campaign info, Minab memorial |
| **Admin Panel** | [peopleforpeace.live/admin](https://peopleforpeace.live/admin) | Django admin for managing campaigns, tasks, volunteers |
| **Telegram Bot** | [@peopleforpeacebot](https://t.me/peopleforpeacebot) | Where volunteers register, join campaigns, complete tasks |

### How It Works

```
Admin creates campaign → Creates tasks → Bot shows tasks to volunteers
                                          → Volunteers claim & complete tasks
                                          → Volunteers invite others via deep-links
                                          → Admin monitors progress in admin panel
```

---

## 2. Getting Started — Admin Panel

### Logging In

Go to `https://peopleforpeace.live/admin` and log in with your superuser credentials.

### Key Admin Sections

| Section | Path | What You'll Find |
|---------|------|------------------|
| **Campaigns** | `/admin/campaigns/campaign/` | Create & manage campaigns |
| **Campaign Volunteers** | `/admin/campaigns/campaignvolunteer/` | See who joined which campaign |
| **Tasks** | `/admin/tasks/task/` | Create & manage tasks for campaigns |
| **Task Assignments** | `/admin/tasks/taskassignment/` | See who is doing what, approve completions |
| **Twitter Storms** | `/admin/campaigns/twitterstorm/` | Schedule coordinated Twitter actions |
| **Users** | `/admin/users/user/` | All registered users |

---

## 3. Creating a Campaign

Navigate to **Campaigns → Add Campaign** (`/admin/campaigns/campaign/add/`).

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| **Name** | Campaign title (English) | `#CeaseFireNow — Stop the War` |
| **Description** | Full campaign description | Detailed text about goals and context |
| **Short description** | One-liner for listings | `Join the global movement for peace` |
| **Campaign type** | Regular, Twitter Storm, or Hybrid | `Regular Campaign` |
| **Status** | Must be **Active** for volunteers to see it | `Active` |
| **Created by** | Your admin account | Select from dropdown |

### Campaign Statuses

| Status | Visible to Volunteers? | Description |
|--------|----------------------|-------------|
| **Draft** | ❌ | Still being set up |
| **Active** | ✅ | Open for volunteers to join and do tasks |
| **Paused** | ❌ | Temporarily hidden |
| **Completed** | ❌ | Campaign finished |
| **Archived** | ❌ | Archived for records |

### Goals (Optional)

Set numeric targets to track campaign progress:

- **Target Members** — how many volunteers you want to recruit
- **Target Activities** — how many task completions you want
- **Target Twitter Posts** — for Twitter Storm campaigns

The admin panel auto-calculates a **progress percentage** from these goals.

### Translations

Expand the **Translations (Farsi / Arabic)** section to add:
- `name_fa` / `name_ar` — Campaign name in Farsi & Arabic
- `short_description_fa` / `short_description_ar` — Short description translations

> **Tip:** If you leave translations blank, the English version is shown as fallback.

### Telegram Integration

Optionally link Telegram channel/group IDs for automated broadcasting:
- **Channel ID** — for public announcements (e.g., `@pfp_channel`)
- **Group ID** — for volunteer coordination

---

## 4. Designing Campaign Tasks

Tasks are the **heart of every campaign**. Each task is a specific action you want volunteers to perform.

Navigate to **Tasks → Add Task** (`/admin/tasks/task/add/`).

### Task Fields

| Field | Required | Description |
|-------|----------|-------------|
| **Title** | ✅ | Task name (English). Keep it short and action-oriented. |
| **Description** | ✅ | What is this task about? Context and motivation. |
| **Instructions** | ✅ | Step-by-step guide for volunteers. Be specific! |
| **Task type** | ✅ | See [Task Types Reference](#5-task-types-reference) |
| **Campaign** | ✅ | Which campaign this task belongs to |
| **Created by** | ✅ | Auto-set to your account |
| **Points** | ✅ | Points awarded on completion (default: 10) |
| **Estimated time** | ✅ | Minutes to complete (default: 15) |
| **Max assignments** | ✅ | How many volunteers can do this task (default: 1) |
| **Is active** | ✅ | Must be ✅ checked for task to appear |
| **Is verified** | ❌ | Check this if you've reviewed and approved the task |

### Translations

Each task supports **three languages** — expand "Translations (Farsi / Arabic)" to add:
- `title_fa` / `title_ar`
- `description_fa` / `description_ar`
- `instructions_fa` / `instructions_ar`

### Resources (Optional)

| Field | Purpose | Example |
|-------|---------|---------|
| **Target URL** | Link the volunteer needs to act on | Tweet URL to retweet |
| **Hashtags** | Comma-separated hashtags | `#CeaseFireNow, #StopWar` |
| **Mentions** | Twitter accounts to mention | `@UN, @ICJ_ICJ` |
| **Image URL** | Image to use in the task | URL to a poster image |

### Availability Scheduling

- **Available from** — Task becomes visible to volunteers at this date/time
- **Available until** — Task disappears after this date/time

Leave blank for permanently available tasks.

### Key Tweets (for twitter_comment tasks)

When creating a `Twitter Comment` task, you can add **Key Tweets** inline — these are specific tweets from key figures that volunteers should comment on:

| Field | Example |
|-------|---------|
| **Tweet URL** | `https://x.com/UN/status/12345` |
| **Author name** | `United Nations` |
| **Author handle** | `@UN` |
| **Description** | `UN Secretary-General's statement on ceasefire` |
| **Order** | `1` (lower = shown first) |

---

## 5. Task Types Reference

| Task Type | Icon | Description | What Volunteer Does |
|-----------|------|-------------|---------------------|
| **Twitter Post** | 🐦 | Post an original tweet | Write and post a tweet with hashtags |
| **Twitter Retweet** | 🔁 | Retweet a specific post | Retweet the linked tweet |
| **Twitter Comment** | 💬 | Comment on key tweets | Reply to specified tweets from key figures |
| **Twitter Like** | ❤️ | Like a specific post | Like the linked tweet |
| **Telegram Share** | 📢 | Share content on Telegram | Forward a message to their groups |
| **Telegram Invite** | 👥 | Invite people to join | Share invite link with friends |
| **Content Creation** | ✍️ | Create original content | Write an article, make a video, design a poster |
| **Petition** | 📝 | Sign a petition | Sign the linked petition |
| **Mass Email** | 📧 | Send emails | Send emails to specified recipients |
| **Research** | 🔍 | Research and report | Gather information about a topic |
| **Other** | 📌 | Custom task | Any other campaign action |

### The "Stepped Task" Strategy

Design tasks in three tiers to maximize engagement:

| Tier | Effort | Points | Example |
|------|--------|--------|---------|
| **Quick wins** | Low (2-5 min) | 5-10 | Retweet, sign petition, like a post |
| **Medium effort** | Medium (10-15 min) | 10-15 | Write original tweet, invite a friend |
| **High impact** | High (30+ min) | 25-50 | Create a video, write a 200+ word statement |

> **Tip:** Start with 2-3 quick wins to build momentum, then add medium and high-effort tasks. Volunteers who complete easy tasks first are more likely to attempt harder ones.

---

## 6. The Volunteer Experience (Bot)

Understanding what volunteers see helps you design better campaigns.

### Registration Flow

1. User opens [@peopleforpeacebot](https://t.me/peopleforpeacebot)
2. User taps `/start` → chooses language (🇬🇧 / 🇮🇷 / 🇸🇦)
3. Bot asks for their name → user replies with their name
4. Registration complete → Main Menu shown

### Main Menu

Volunteers see these buttons:

| Button | What It Does |
|--------|-------------|
| 📋 **Browse Campaigns** | See all active campaigns |
| 👤 **Profile** | View their name + list of people who joined via their invites |
| 🌍 **Change Language** | Switch between English, Farsi, Arabic |

### Campaign & Task Flow

```
Browse Campaigns → Select a campaign → See task checklist
                                         → Tap a task → See details + instructions
                                                         → "🚀 Start Task" → 3-stage interaction
                                                         → Submit proof → Task marked complete
```

### Task Checklist View

Volunteers see a **checklist-style** view of tasks:

```
📋 CeaseFireNow — Your Tasks

⬜ 🐦 Post support tweet  (⏱ 5 min)
⬜ 🔁 Retweet UN statement  (⏱ 2 min)
✅ 💬 Comment on key tweets  (⏱ 10 min)
🚧 ✍️ Write a peace statement  (⏱ 30 min)

👆 Tap a task to start
```

- ⬜ = Not started
- 🚧 = In progress
- ✅ = Completed

### The 3-Stage Task Interaction

When a volunteer taps a task:

1. **Task Detail** — Shows description, instructions, estimated time, points
2. **Action** — Volunteer performs the action (posts tweet, signs petition, etc.)
3. **Proof Submission** — Volunteer submits proof (URL, text, or screenshot)

---

## 7. Invite & Referral System

Every volunteer gets a **unique invite link** for each campaign they join.

### How It Works

1. Volunteer taps **"👥 Invite Friends"** on a campaign
2. Picks a **language** for the invite (EN/FA/AR)
3. Picks an **invite style**:
   - **🕊 Memorial** — Sends a memorial image with campaign info
   - **🎬 Video** — Sends the "100 Faces of Peace" lyric video
   - **✉️ Campaign** — Opens Telegram's share dialog with campaign text
4. A personalized **deep-link** is generated: `https://t.me/peopleforpeacebot?start=campaign_17_ref_42`
5. When someone clicks the link and registers → they auto-join the campaign → the inviter gets credit

### Tracking Invites

- **In Profile**: Volunteers can see the names of people who joined via their links
- **After Sending Invite**: A follow-up message shows their total invite count as motivation
- **Admin Panel**: Check `Campaign Volunteers` → filter by campaign → see `invited_by` column

### Deep-Link Format

```
https://t.me/peopleforpeacebot?start=campaign_{CAMPAIGN_ID}_ref_{USER_ID}
```

The `ref_{USER_ID}` part is what tracks the referral.

---

## 8. Twitter Storm Campaigns

Twitter Storms are **coordinated bursts** of Twitter activity. Set campaign type to "Twitter Storm" or "Hybrid."

### Creating a Storm

Navigate to **Campaigns → Twitter Storms → Add** (`/admin/campaigns/twitterstorm/add/`):

| Field | Description |
|-------|-------------|
| **Campaign** | Link to the parent campaign |
| **Title** | Storm name (e.g., "Global Ceasefire Storm #3") |
| **Scheduled at** | Date and time the storm begins |
| **Duration** | How many minutes the storm lasts |
| **Tweet templates** | JSON array of suggested tweets for volunteers to post |
| **Hashtags** | Hashtags to use in tweets |
| **Mentions** | Twitter accounts to mention |
| **Notify 1h / 15m / 5m** | Auto-send Telegram reminders to volunteers before the storm starts |

### Storm Statuses

| Status | Meaning |
|--------|---------|
| **Draft** | Still planning |
| **Scheduled** | Ready — notifications will auto-send at the right times |
| **Active** | Storm is live right now |
| **Completed** | Storm is over |

---

## 9. Telegram Channel Broadcasting

Campaigns can have a linked **Telegram channel** for public updates.

### Setup

1. Create a Telegram channel
2. Add the bot as an **admin** to the channel
3. Get the channel's numeric ID (use [@userinfobot](https://t.me/userinfobot))
4. Enter the ID in Campaign → **Telegram Channel ID**

### What Gets Broadcasted

From the admin panel, go to **Campaign Updates** → create an update → select it → use the **"Push to Telegram Channel"** action.

The system queues the message via Celery for reliable delivery.

---

## 10. Monitoring & Analytics

### Key Admin Views

| What to Check | Where | What It Shows |
|---------------|-------|---------------|
| **Campaign progress** | Campaign list | Members count, activities done, progress % |
| **Who joined** | Campaign Volunteers | List of volunteers, their status, points, join date |
| **Who invited whom** | Campaign Volunteers | `invited_by` field shows the referrer |
| **Task completions** | Task Assignments | Which volunteer did what, status, proof submitted |
| **Points earned** | Campaign Volunteers | Points per volunteer per campaign |
| **Overall user activity** | Users | Full user list with registration date |

### Task Assignment Statuses

| Status | Meaning |
|--------|---------|
| **Assigned** | Volunteer has claimed the task |
| **In Progress** | Working on it |
| **Completed** | Volunteer submitted proof |
| **Verified** | Admin confirmed the work → points awarded |
| **Rejected** | Admin rejected the proof |
| **Cancelled** | Assignment was cancelled |

### Verifying Task Completions

1. Go to **Task Assignments** → filter by `Status = Completed`
2. Click on an assignment → review proof (URL, text, image)
3. Change status to **Verified** → points are auto-awarded
4. Or change to **Rejected** → add a rejection note

---

## 11. Multilingual Support

The platform supports **three languages**: English 🇬🇧, Farsi 🇮🇷, Arabic 🇸🇦.

### How It Works

- Volunteers choose their language when they first register
- They can switch anytime via **🌍 Change Language**
- The bot sends all messages in their preferred language
- **Fallback**: If a translation is missing, English is shown

### What Needs Translations

| Item | Fields to Translate |
|------|---------------------|
| **Campaign** | `name_fa/ar`, `short_description_fa/ar` |
| **Task** | `title_fa/ar`, `description_fa/ar`, `instructions_fa/ar` |

> **Tip:** Always fill in translations for your primary audience. For a Middle East-focused campaign, prioritize Farsi and Arabic. English serves as the universal fallback.

---

## 12. Best Practices

### Campaign Design

- ✅ **Set clear, achievable goals** — use Target Members and Target Activities
- ✅ **Write compelling descriptions** — explain *why* this matters
- ✅ **Start small** — launch with 3-5 tasks, add more as volunteers join
- ✅ **Use the stepped strategy** — mix easy, medium, and hard tasks

### Task Design

- ✅ **Be specific in instructions** — "Go to [this URL] → Click retweet → Come back and paste the link"
- ✅ **Set realistic estimated times** — volunteers trust time estimates
- ✅ **Set `max_assignments` high** for retweet/like tasks (everyone can do these)
- ✅ **Set `max_assignments` low** for content creation (quality over quantity)
- ✅ **Use `available_from` / `available_until`** for time-sensitive tasks

### Growing Your Campaign

- ✅ **Encourage invites** — the referral system is your best growth tool
- ✅ **Create invite-style tasks** — make "invite 3 friends" a task worth points
- ✅ **Use the Video invite** — the "100 Faces" video is very shareable
- ✅ **Broadcast updates** — push campaign updates to your Telegram channel regularly

### Common Mistakes

- ❌ **Setting status to Draft** and wondering why no one sees the campaign
- ❌ **Not filling `instructions`** — volunteers won't know what to do
- ❌ **Setting `max_assignments = 1`** for tasks everyone should do
- ❌ **Forgetting translations** for your non-English audience
- ❌ **Not verifying task completions** — volunteers need their points validated

---

## Quick Reference Card

| Action | Where |
|--------|-------|
| Create a campaign | `/admin/campaigns/campaign/add/` |
| Create a task | `/admin/tasks/task/add/` |
| Verify task completions | `/admin/tasks/taskassignment/` → filter `Completed` |
| See campaign members | `/admin/campaigns/campaignvolunteer/` |
| Push channel update | `/admin/campaigns/campaignupdate/` → action → Push |
| Schedule Twitter Storm | `/admin/campaigns/twitterstorm/add/` |
| View all users | `/admin/users/user/` |

---

*Last updated: March 2026*
