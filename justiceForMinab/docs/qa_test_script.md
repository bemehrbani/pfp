# 🧪 QA Test Script — PFP Telegram Bot

> **For**: QA Tester
> **Bot**: [@peopleforpeacebot](https://t.me/peopleforpeacebot?start=campaign_18)
> **Time needed**: ~30 min
> **Goal**: Test the full volunteer journey, report friction, suggest improvements.

---

## 📋 Instructions

1. Follow each test case below **in order** (they build on each other)
2. For each step, note: ✅ Pass / ❌ Fail / ⚠️ Friction
3. Write your **raw thoughts** in the "Notes" column — what confused you, what felt wrong, what was great
4. Screenshot anything broken or confusing
5. Test in **both English and Farsi** if you can

---

## Test Cases

### TC1: First Contact & Onboarding
| Step | Action | Expected | Result | Notes |
|------|--------|----------|--------|-------|
| 1.1 | Open [this link](https://t.me/peopleforpeacebot?start=campaign_18) | Bot opens in Telegram | | |
| 1.2 | Tap **Start** | Bot sends welcome message | | |
| 1.3 | Read the welcome message | Should explain: what happened, what we're doing, how you help | | |
| 1.4 | Enter your name when asked | Bot confirms name, shows campaign card | | |
| 1.5 | Tap **Join** on the campaign card | Should auto-join and show campaign info with resources | | |

**Key questions to answer:**
- Did you understand the cause within 10 seconds?
- Did you know what to do next?
- Was anything confusing or unclear?

---

### TC2: Task List & Priority
| Step | Action | Expected | Result | Notes |
|------|--------|----------|--------|-------|
| 2.1 | View the task list after joining | Tasks should appear sorted easiest first | | |
| 2.2 | Check the first task | Should have ⭐ badge — this is the "Start Here" task | | |
| 2.3 | Read task names | Should be clear, not truncated mid-word | | |
| 2.4 | Check time/points display | Each task shows ⏱ X min · Y pts | | |

**Key questions:**
- Is it obvious which task to start with?
- Do the task names make sense without clicking into them?
- Does the list feel overwhelming or manageable?

---

### TC3: Sign the Petition (Easiest Task)
| Step | Action | Expected | Result | Notes |
|------|--------|----------|--------|-------|
| 3.1 | Tap the petition task | Should show instructions + petition link | | |
| 3.2 | Open the petition link | Should go to ECCHR petition page | | |
| 3.3 | Sign the petition | Petition form should work | | |
| 3.4 | Come back to bot | Bot should be waiting for proof | | |
| 3.5 | Send proof (screenshot or URL) | Bot should confirm + offer next task | | |

**Key questions:**
- Was it clear what "proof" means?
- Did the bot guide you through it?
- How long did the whole thing take?

---

### TC4: Amplify Reports (Dual-Path)
| Step | Action | Expected | Result | Notes |
|------|--------|----------|--------|-------|
| 4.1 | Start the Amplify task | Should show Option A (Twitter) AND Option B (Telegram) | | |
| 4.2 | **Path A**: Tap "Find Tweets" | Should open Twitter search with hashtags | | |
| 4.3 | **Path B**: Tap "Get Forwardable Message" | Bot should send a clean, forwardable message | | |
| 4.4 | Try forwarding that message | Should forward cleanly (no broken formatting) | | |
| 4.5 | Send proof (screenshot or "done") | Bot should accept it | | |

**Key questions:**
- Was the dual-path choice clear?
- Did the forwardable message look good when forwarded?
- Would you actually forward it to a real group?

---

### TC5: Share a Child's Story (Twitter Post)
| Step | Action | Expected | Result | Notes |
|------|--------|----------|--------|-------|
| 5.1 | Start the "Share a Child's Story" task | Should show child picker or story options | | |
| 5.2 | Pick a child | Bot should send their photo + story + ready tweet | | |
| 5.3 | Tap tweet intent link | Should open Twitter with pre-filled tweet | | |
| 5.4 | Come back and paste tweet URL | Bot should confirm | | |

**Key questions:**
- Was the child's story emotionally impactful?
- Did the tweet link work correctly?
- Would you actually post this on your real Twitter?

---

### TC6: Content Creation (Artist Task)
| Step | Action | Expected | Result | Notes |
|------|--------|----------|--------|-------|
| 6.1 | Start content creation task | Should show instructions with content ideas | | |
| 6.2 | Check resource links | Memorial + Evidence buttons should work | | |
| 6.3 | Read the content ideas | Should list: illustration, poem, video, photo collage, music | | |

**Key questions:**
- Are the instructions inspiring or daunting?
- Would an artist know what to create?
- Is 30 min realistic?

---

### TC7: Navigation & Recovery
| Step | Action | Expected | Result | Notes |
|------|--------|----------|--------|-------|
| 7.1 | Try /cancel mid-task | Should cancel current task | | |
| 7.2 | Try /tasks from anywhere | Should show task list | | |
| 7.3 | Try /start again | Should not create duplicate account | | |
| 7.4 | Try the menu button (☰) | Should show available commands | | |

---

### TC8: Language (Farsi)
| Step | Action | Expected | Result | Notes |
|------|--------|----------|--------|-------|
| 8.1 | Change language to Farsi | All messages should switch to FA | | |
| 8.2 | Repeat TC1-TC3 in Farsi | All text should be natural, not machine-translated | | |
| 8.3 | Check RTL rendering | Text should render correctly right-to-left | | |

---

## 📝 Overall Feedback Template

Please fill this out after completing all tests:

```
## Summary
- Time to complete all tests: ___ min
- Overall impression (1-5 stars): ⭐⭐⭐⭐⭐
- Would you recommend this bot to a friend? Yes / No / Maybe

## Top 3 Friction Points
1.
2.
3.

## Top 3 Things That Worked Well
1.
2.
3.

## Bugs Found
- [ ] Bug 1:
- [ ] Bug 2:

## Suggestions
1.
2.
3.

## Screenshots
(Attach any screenshots of issues or great UX moments)
```

---

## ℹ️ Context for the Tester

- This bot helps volunteers support the **Justice for Minab Children** campaign
- 168 children were killed in a school attack — we're building awareness and demanding accountability
- The bot gives volunteers small tasks (2-5 min each): tweet, retweet, sign petition, create art
- Our target audience: Iranian diaspora, international activists, artists
- Many users are **Telegram-native** (no active Twitter) — that's why we added the Telegram forwarding path
- Current biggest challenge: making the flow clear enough that a first-time volunteer can complete a task without asking anyone for help
