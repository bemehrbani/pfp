# PFP — Kanban Board

> **Source of truth** for the People for Peace memorial website.
> Last updated: March 12, 2026

---

## 🎯 Objective & Key Results (OKR)

**Objective**: Make the Minab School Memorial the definitive, shareable, multilingual resource documenting the lives lost — driving awareness and accountability.

| Key Result | Target | Current | Status |
|------------|--------|---------|--------|
| KR1: Children with complete profiles (photo + age + Farsi name) | 98 / 98 | ~15 / 98 | 🔴 |
| KR2: Social shares (Twitter + Telegram + WhatsApp) in first 2 weeks | 500 | 0 (not launched) | ⚪ |
| KR3: Unique visitors in first month of outreach | 5,000 | — | ⚪ |
| KR4: Evidence page sources with article-specific links | 12 / 12 | 12 / 12 | ✅ |
| KR5: Full Farsi translation of all pages | 100% | ~70% | 🟡 |

---

## ✅ Done

| # | Task | Delivered |
|---|------|-----------|
| 3.1 | OG share card image (1200×630) + `og:image` on all 4 pages | Mar 12 |
| 3.5 | Twitter Card meta tags on all pages | Mar 12 |
| 4.1 | Share buttons (𝕏, Telegram, WhatsApp) on child, memorial, evidence | Mar 12 |
| 3.4 | Story → child profile linking (Amin & Mahdieh → amin-ahmadzade) | Mar 12 |
| — | Dynamic OG image per child (shows child's photo when shared) | Mar 12 |
| — | Article-specific URLs for all 12 media sources on evidence page | Mar 12 |
| — | Children grid (98 photos, clickable → child profiles) | Mar 11 |
| — | Featured children carousel on homepage (5 random) | Mar 11 |
| — | Stories with child face thumbnails | Mar 11 |
| — | Evidence page: timeline, OSINT, debunked claims, media sources | Mar 10 |
| — | Individual child profile pages (`child.html`) | Mar 10 |
| — | Cache-busting query strings on all static assets | Mar 11 |
| — | Photo margin cleanup (101 photos processed) | Mar 10 |
| — | Name-to-photo mapping verified (98 children) | Mar 10 |

---

## 🔨 Sprint 1 — Data Completeness & Engagement

> **Sprint goal**: Fill critical data gaps so every child with a photo has a complete, humanized profile. Add emotional engagement features.

| # | Task | Impact | Effort | Status |
|---|------|--------|--------|--------|
| S1.1 | ~~**Fill 58 missing Farsi names**~~ | ✅ Done | — | `[x]` |
| S1.2 | ~~**Fill missing ages**~~ — Displaying "Elementary school student" for unverified | ✅ Done | — | `[x]` |
| S1.3 | ~~**Memorial candle / tribute**~~ — Light a candle + optional message (localStorage) | ✅ Done | — | `[x]` |
| — | ~~**Bot Name Collection**~~ — Removed manual name collection in bot for 1-click registration | ✅ Done | — | `[x]` |
| S1.4 | **Visitor counter** — Hit counter via backend API showing total views & tributes | Medium — social proof | S | `[ ]` |
| S1.5 | **SEO structured data** — Schema.org `Person` + `Article` JSON-LD on child and evidence pages | Medium — Google discoverability | S | `[ ]` |
| S1.6 | **Verify OG previews** — Twitter Card Validator & Facebook Debugger on production | Medium — ensures shares look right | XS | `[ ]` |

---

## 📋 Backlog — Sprint 2+

### Content Expansion
| # | Task | Impact | Effort |
|---|------|--------|--------|
| B1 | More stories — teachers, first responders, parents' accounts | High | M |
| B2 | Embed actual media in evidence — video clips, satellite images | High | M |
| B3 | Interactive timeline — scrollable, animated, expandable cards | Medium | L |
| B4 | Search / filter children — by name, age, gender on memorial grid | Low | S |

### Multilingual
| # | Task | Impact | Effort |
|---|------|--------|--------|
| B5 | Complete Farsi translation of evidence page — all detail cards | High | M |
| B6 | Arabic translation — full Arabic support for all pages | Medium | L |

### Platform
| # | Task | Impact | Effort |
|---|------|--------|--------|
| B7 | PDF memorial report — downloadable "In Memoriam" for offline | Medium | L |
| B8 | Email subscription — newsletter for campaign updates | Low | M |
| B9 | User-submitted tributes — moderated visitor messages | Low | L |

---

## 📊 Data Health

| Metric | Count | % |
|--------|-------|---|
| Total children in data | 117 | — |
| With photo | 98 | 84% |
| With English name | 117 | 100% |
| With Farsi name | 117 | 100% |
| With known age | 15 | 13% |
| Stories total | 7 | — |
| Stories linked to child profiles | 4 | 57% |

---

*Effort: XS (<1h) · S (1-3h) · M (3-8h) · L (1-2d)*
