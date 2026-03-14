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
| E1 | **Rich auto-join message** — Add cause context, resource links (memorial/evidence/data/channel), hashtags | 🔲 | ⭐⭐⭐ |
| E2 | **Enriched campaign detail** — Add resource links + full description | 🔲 | ⭐⭐ |
| E3 | **Enriched join welcome** — Same resource block as E1 | 🔲 | ⭐⭐ |
| E4 | **"About Campaign" button** on task checklist → shows full context | 🔲 | ⭐ |
| E5 | **Campaign description update** — Emotional narrative on production | 🔲 | ⭐⭐⭐ |
| E6 | **Resource link translation keys** — Centralized i18n for all links | 🔲 | ⭐⭐ |
| E7 | **Richer invite share** — Include cause context + hashtags in invite message | 🔲 | ⭐⭐ |

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

## ✅ Completed (Recent)
- [x] **Strategy:** Developed comprehensive 4-phase action plan and top-3 focused strategy for Minab accountability.
- [x] **Research:** Comprehensive legal research into 10 possible pathways for prosecuting Trump for the Minab strike.
- [x] **Data Gathering:** Extracted and split 100 children's photos from the Minab memorial image.
- [x] **Names Verification:** All 100 children verified and live at memorial.html and data.html.
- [x] **Content Deployment:** Interactive mosaic deployed to peopleforpeace.live.
- [x] **Evidence Page:** Fact sheet with OSINT, media sources, official statements, and debunked claims.
