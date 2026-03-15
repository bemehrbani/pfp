# PFP Campaign & Content Operations
> Project board for all non-technical, campaign, content, and partnership tasks.
> For technical development, see `kanban.md`.

## 🚨 Immediate Priorities (This Week)
- [x] **Minab Names Verification:** ✅ Live at [memorial.html](https://peopleforpeace.live/memorial.html) and [data.html](https://peopleforpeace.live/data.html).
- [x] **Campaign Setup:** Create `#JusticeForMinab` campaign in Django Admin with initial tasks (`twitter_post`, `twitter_retweet`, etc.).
- [x] **Content Deployment:** ✅ Interactive mosaic live at [peopleforpeace.live/memorial.html](https://peopleforpeace.live/memorial.html).
- [ ] **First Outreach:** Follow DAWN, ECCHR, CJA, and HRW on Twitter and LinkedIn. Begin engaging with their public posts.

---

## 📅 Scheduled Events
- **Mar 28, 2026:** One-Month Anniversary Twitter Storm (`#OneMonthMinab`). Requires scheduled TweetStorm in backend.

---

## 📝 Content Creation & Resources
### In Progress
- [ ] **Memorial Cards:** Generate spotlight cards for the first batch of verified children from Minab.
- [ ] **Audio Production:** Record Farsi and Arabic songs based on existing lyrics.

### Backlog
- [ ] **Educational Material:** Create simple graphics explaining "Command Responsibility" and "Article 12(3)" for activists.
- [ ] **Email Templates:** Draft template for `mass_email` tasks directed at UN representatives.

---

## 🤝 Partnerships & Legal Action
### In Progress
- [ ] **DAWN Outreach Prep:** Prepare the digital asset package (names, mosaic link, Twitter engagement stats) before sending the cold email draft.

### Backlog
- [ ] **ECCHR Legal Filing Prep:** Organize the Minab media archive (satellite imagery, news reports) into a structured folder for the German legal complaint.
- [ ] **UNHRC Member Targets:** Compile list of email addresses and contact forms for rotating members of the UN Human Rights Council.

---

## 🌐 Live Assets (Published URLs)

| Page | URL | Purpose |
|------|-----|---------|
| **Landing Page** | https://peopleforpeace.live/ | Main entry point, org overview |
| **Memorial** | https://peopleforpeace.live/memorial.html | Interactive photo mosaic of 100 children |
| **Evidence** | https://peopleforpeace.live/evidence.html | Fact sheet: OSINT, media sources, debunked claims |
| **Data** | https://peopleforpeace.live/data.html | Verified names and data for the 100 children |
| **Amplify** | https://peopleforpeace.live/amplify.html | Curated library of 33+ investigative reports + RT templates |
| **Bot** | https://t.me/peopleforpeacebot | Telegram campaign bot |
| **Bot Deep-link** | https://t.me/peopleforpeacebot?start=campaign_18 | Auto-join Minab campaign |
| **Channel** | https://t.me/people4peace | Telegram updates channel |

---

## 🚀 Campaign UX Epic — First Impression & Resource Discovery

> Goal: When a user joins via deep-link, they should feel the weight of the cause and have immediate access to all campaign resources.

### What's Missing Today
- Auto-join message is generic — no cause context, no links, no hashtags
- Campaign detail view has no resource links
- Task checklist has no "About" button to revisit campaign info
- Invite share message is a bare bot link with no emotional context

### Tasks

| # | Task | Status | Impact |
|---|------|--------|--------|
| E1 | **Rich auto-join message** — Add cause context, resource links (memorial/evidence/data/channel), hashtags | ✅ | ⭐⭐⭐ |
| E2 | **Enriched campaign detail** — Add resource links + full description | ✅ | ⭐⭐ |
| E3 | **Enriched join welcome** — Same resource block as E1 | ✅ | ⭐⭐ |
| E4 | **"About Campaign" button** on task checklist → shows full context | ✅ | ⭐ |
| E5 | **Campaign description update** — Emotional narrative on production | ✅ | ⭐⭐⭐ |
| E6 | **Resource link translation keys** — Centralized i18n for all links | ✅ | ⭐⭐ |
| E7 | **Richer invite share** — Include cause context + hashtags in invite message | ✅ | ⭐⭐ |

### Resource Links to Surface

| Resource | URL | Label |
|----------|-----|-------|
| Memorial | https://peopleforpeace.live | 🕯 Memorial Page |
| Evidence | https://peopleforpeace.live/evidence.html | 📄 Evidence & Facts |
| Data | https://peopleforpeace.live/data.html | 📊 Verified Data |
| Channel | https://t.me/people4peace | 📢 Follow Updates |

### Proposed Auto-Join Message (EN)

```
🎉 *You've joined Justice for Minab Children!*

On Feb 28, 2026, 168 children aged 7-12 were killed  
in a strike on their school in Minab, Iran.

We demand justice. Your voice matters.

👥 X volunteers joined · 🎯 Y tasks available

━━━━━━━━━━━━━━━━━━━
🔗 *Resources:*
🕯 Memorial Page — peopleforpeace.live
📄 Evidence & Facts — peopleforpeace.live/evidence.html
📊 Verified Data — peopleforpeace.live/data.html
📢 Follow Updates — @people4peace
━━━━━━━━━━━━━━━━━━━

#️⃣ #JusticeForMinab #168Children #MinabSchoolMassacre

Tap a task below to get started! 👇
```

---

## 📝 Task Content Quality Epic — Production-Ready Tasks

> Goal: Every task should have clear, actionable instructions with real links, specific targets, and emotional context so a first-time volunteer knows exactly what to do.

### Quality Standards
- **Title:** Action-oriented verb + specific outcome
- **Description:** Why this matters (1-2 sentences connecting to the cause)
- **Instructions:** Numbered steps with real URLs, search queries, or targets
- **Trilingual:** EN/FA/AR — natural, not machine-translated
- **Points/Time:** Realistic estimates

### Current Issues
- Instructions say "search for..." without giving specific links or search queries
- No target accounts/tweets for comment tasks
- "Content library" referenced but doesn't exist yet
- Descriptions are generic — don't connect action to impact

---

### T1: Share a Child's Story (ID 15 · `twitter_post`)

| Field | Current | Improve |
|-------|---------|---------|
| Description | "Post a spotlight card..." | ✅ Updated — interactive child picker with memorial links |
| Instructions | "Download from content library" | ✅ Updated — step-by-step with memorial URL |
| Points/Time | 10pts / 5min | ✅ OK |

**Subtasks:**
- [x] T1.1: Add memorial page link to instructions (`peopleforpeace.live/memorial.html`)
- [x] T1.2: Interactive child picker — volunteer picks child, bot sends photo + ready tweet
- [x] T1.3: 5 featured children with documented stories (Hami, Sobhan, Niyayesh, Amin, Reza)
- [x] T1.4: Update FA translation (captions, tweets, buttons all bilingual)

---

### T2: Amplify Investigative Reports (ID 16 · `twitter_retweet`)

| Field | Current | Improve |
|-------|---------|---------|
| Description | "Retweet NYT, BBC..." | ✅ Good — add "why" context |
| Instructions | "Search for reports..." | ❌ No search links! Add Twitter search URL |
| Points/Time | 10pts / 3min | ✅ OK |

**Subtasks:**
- [x] T2.1: Add Twitter/X search link for `#MinabSchoolMassacre` or `Minab school`
- [x] T2.2: List 3-5 specific report tweet URLs (BBC, NYT, WaPo, etc.)
- [x] T2.3: Add evidence page link (`peopleforpeace.live/evidence.html`)
- [ ] T2.4: Update FA translation (still generic)

---

### T3: Comment on Key Tweets (ID 17 · `twitter_comment`)

| Field | Current | Improve |
|-------|---------|---------|
| Description | "Reply to US officials..." | ✅ Good |
| Instructions | "Reply to ICC, UN, HRW..." | ❌ No specific accounts or tweet links |
| Points/Time | 10pts / 5min | ✅ OK |

**Subtasks:**
- [x] T3.1: List 5+ target accounts (@IntlCrimCourt, @UNHumanRights, @hraborz, @StateDept, etc.)
- [x] T3.2: Provide 2-3 sample reply templates (factual, respectful)
- [x] T3.3: Add link to evidence page for fact-checking before commenting
- [x] T3.4: Update FA translation

---

### T4: Create Original Content (ID 21 · `content_creation`)

| Field | Current | Improve |
|-------|---------|---------|
| Description | "Create video, art, poem..." | ✅ Good |
| Instructions | "Use content library..." | ❌ No library link! Add ideas + resources |
| Points/Time | 10pts / 30min | ⚠️ Points too low for 30min effort |

**Subtasks:**
- [ ] T4.1: Add memorial + evidence URLs as source material
- [ ] T4.2: Add 3-4 content ideas (thread, poem, comparison graphic, short video)
- [ ] T4.3: Increase points to 25-50 (highest effort task)
- [ ] T4.4: Update FA translation

---

### T5: Sign the Petition (ID 24 · `petition`)

| Field | Current | Improve |
|-------|---------|---------|
| Description | Detailed, good quality | ✅ Good |
| Instructions | Numbered steps with link | ✅ Good |
| Points/Time | 10pts / 5min | ⚠️ Time could be 2min |

**Subtasks:**
- [ ] T5.1: Reduce estimated time to 2 min
- [ ] T5.2: Add AR (Arabic) translations
- [ ] T5.3: Add context linking petition to Minab specifically

## ✅ Completed (Recent)
- [x] **Pinned Campaign Dashboard:** Auto-updating dashboard message in `@people4peace` channel with OKR progress bars, task list, and join button. Hourly Celery Beat refresh. Deploy `e198dc3`.
- [x] **Bot Profile Improvements:** Updated botpic (dove avatar), About text, Description with task breakdown + resource links, registered 8 slash commands in BotFather.
- [x] **Campaign UX Epic (E1-E7):** All 7 UX improvements deployed — rich messages, about button, resource links, enriched invites.
- [x] **Amplify Page:** Curated library of 33+ investigative reports live at amplify.html.
- [x] **Petition Task (ID 24):** New petition task created and active in bot.
- [x] **Content Creation Whitelist:** `content_creation` task type now visible in bot checklist.
- [x] **T1 Content Update:** "Share a Child's Story" — interactive child picker with photo delivery, tweet intents, bilingual support. Deploy `cfcc777`.
- [x] **T2 Content Update:** "Amplify Investigative Reports" — enriched with specific sources, amplify.html link, and report library button.
- [x] **T3 Content Update:** "Comment on Key Tweets" — improved with search URLs, target accounts, sample replies.
- [x] **Strategy:** Developed comprehensive 4-phase action plan and top-3 focused strategy for Minab accountability.
- [x] **Research:** Comprehensive legal research into 10 possible pathways for prosecuting Trump for the Minab strike.
- [x] **Data Gathering:** Extracted and split 100 children's photos from the Minab memorial image.
- [x] **Names Verification:** All 100 children verified and live at memorial.html and data.html.
- [x] **Content Deployment:** Interactive mosaic deployed to peopleforpeace.live.
- [x] **Evidence Page:** Fact sheet with OSINT, media sources, official statements, and debunked claims.
