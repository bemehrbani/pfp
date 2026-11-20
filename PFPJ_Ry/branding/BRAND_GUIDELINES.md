# People for Peace & Justice ry — Official Brand Identity Guidelines

**Legal Entity:** People for Peace & Justice ry (Rekisteröity yhdistys)  
**Domicile:** Helsinki, Finland · **PRH Business ID (Y-tunnus):** `3616815-5`  
**Canonical Domain:** `https://peopleforpeace.live` · **Official Contact:** `info@peopleforpeace.live`

---

## 1. Visual Architecture: *The Sovereign Laurel & Equilibrium Dove*

The PFPJ ry visual identity unites both halves of the association's statutory mandate into a calm, Nordic-minimalist institutional mark:

1. **The Soaring Dove & Golden Olive Branch (*Peace & Civilian Dignity*)**: Preserves direct continuity with People for Peace's founding emblem, refined into clean subpixel cubic-Bezier curves with a two-tone separation between the dove (`#F5F3EF` / `#0B1220`) and the golden olive sprig (`#E5B95F` / `#A6761E`).
2. **The Equilibrium Balance Bar & Fulcrum Diamond (*International Legal Accountability*)**: Positioned at `6 o'clock` directly beneath the dove, a level horizontal balance bar poised on a central diamond fulcrum signifies equal measure under international law — *Peace rising upon a level foundation of Justice*.
3. **The Symmetrical Olive Laurel Wreath (*International Law Tradition*)**: Fourteen tangent-hugging olive leaves frame the mark in the classical civic tradition of international courts and multilateral treaty bodies.

---

## 2. Scale-Responsive Mark System

Use the appropriate asset for the target display size so every surface remains crisp and legible:

| Size Range | Recommended Asset | Primary Surfaces |
| :--- | :--- | :--- |
| **`16px – 40px`** | `svg/pfpj-badge-shield.svg` / `svg/pfpj-favicon.svg` | Browser favicons, mobile navbar icons, compact co-organizer poster badges |
| **`48px+` (Icon Only)** | `svg/pfpj-mark-crest-dark.svg` / `svg/pfpj-mark-crest-light.svg` | Social avatars, Telegram bot/channel pictures, slide corner marks |
| **Web & Document Headers** | `svg/pfpj-lockup-horizontal-*.svg` / `svg/pfpj-lockup-compact-*.svg` | Website navigation bar, A4 NGO letterhead, press releases, partner strips |
| **Cover Pages & Cards** | `svg/pfpj-lockup-stacked-*.svg` | Report covers, podium signs, OpenGraph (`1200×630`) share cards |
| **Legal Filings & Stamps** | `svg/pfpj-seal-official-*.svg` / `svg/pfpj-mark-crest-mono-black.svg` | ICC/UN submissions, Universal Jurisdiction dossiers, board resolutions |

> **Zero Font Dependency Guarantee:** All typography inside the `svg/` lockup and seal files has been converted to pure vector `<path>` outlines (`Optima` + `Avenir Next`) with lowercase Finnish `ry` preserved per PRH registration rules. They render identically across browsers, Word, Keynote, Figma, Illustrator, and print shops without installing fonts.

---

## 3. Canonical Color Tokens

| Token Name | Hex | RGB | CMYK (Print Approx.) | Role |
| :--- | :--- | :--- | :--- | :--- |
| **Obsidian Navy** | `#0B1220` | `11, 18, 32` | `86, 76, 52, 74` | Primary dark surface, shield core, light-mode primary ink |
| **Nordic Brass Gold (Dark UI)** | `#E5B95F` | `229, 185, 95` | `11, 28, 71, 2` | Laurel wreath, olive sprig, equilibrium bar & `ry` on dark backgrounds |
| **Archival Bronze Gold (Print/Light)** | `#A6761E` | `166, 118, 30` | `26, 48, 96, 18` | High-contrast metallic gold accent on white paper & light backgrounds |
| **Archival Parchment** | `#F5F3EF` | `245, 243, 239` | `3, 3, 6, 0` | Dove fill & primary typography on dark backgrounds |

---

## 4. Directory Inventory (`PFPJ_Ry/branding/`)

- `svg/` — 14 vector master files (`.svg`, UTF-8 without BOM):
  - `pfpj-mark-crest-dark.svg`, `pfpj-mark-crest-light.svg`, `pfpj-mark-crest-mono-black.svg`, `pfpj-mark-crest-mono-white.svg`
  - `pfpj-badge-shield.svg`, `pfpj-favicon.svg`
  - `pfpj-lockup-horizontal-dark.svg`, `pfpj-lockup-horizontal-light.svg`
  - `pfpj-lockup-compact-dark.svg`, `pfpj-lockup-compact-light.svg`
  - `pfpj-lockup-stacked-dark.svg`, `pfpj-lockup-stacked-light.svg`
  - `pfpj-seal-official-dark.svg`, `pfpj-seal-official-light.svg`
- `png/` — 11 high-resolution raster exports (`.png`):
  - `pfpj-crest-dark-1024.png`, `pfpj-crest-light-1024.png`, `pfpj-badge-shield-1024.png`
  - `pfpj-lockup-horizontal-dark-2240.png`, `pfpj-lockup-horizontal-light-2240.png`
  - `pfpj-seal-official-dark-1200.png`, `pfpj-seal-official-light-1200.png`
  - `pfpj-avatar-social-1024.png` (Telegram / LinkedIn / X profile picture)
  - `pfpj-og-card-1200x630.png` (Website OpenGraph social preview card)
  - `apple-touch-icon-180.png`, `favicon-32.png`
- `letterhead/pfpj-official-letterhead-a4.html` — Print-ready A4 Official NGO Correspondence Letterhead
- `brand-specimen.html` — Interactive Light/Dark Brand Specimen Sheet

---

## 5. Clear Space & Guardrails

- **Minimum Clear Space:** Maintain clear space equal to at least **20% of the mark's height** on all four sides.
- **Finnish Statutory Casing:** Always write `ry` in **lowercase** (`People for Peace & Justice ry` or `PFPJ ry`), never `RY` (except inside all-caps circular seal rings where `ry` remains lowercase for statutory accuracy).
- **Do Not:** Distort aspect ratios, place the light-mode mark on dark backgrounds (or vice versa), add drop shadows to the crest, or place text inside the dove silhouette.
