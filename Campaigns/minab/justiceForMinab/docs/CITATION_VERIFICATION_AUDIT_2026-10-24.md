# CITATION, PARAGRAPH & FACTUAL VERIFICATION AUDIT REPORT (DRAFT v0.1 GATE)

**Docket No.:** `PFPJ-2026-IR-001`  
**Audit Date:** October 24, 2026  
**Target Instruments Audited:**
1. `Campaigns/minab/justiceForMinab/docs/FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.md` (Chapters I–X)
2. `Campaigns/minab/justiceForMinab/docs/MASTER_EXHIBIT_DOSSIER.md` (Annex Exhibits I–VIII)
3. `Campaigns/minab/legal_benchmarks/COMPREHENSIVE_BENCHMARKING_REMAINING_15_CASES.md`
4. `Campaigns/minab/legal_benchmarks/benchmarked_facts_cases_01_to_19.md` and `Campaigns/minab/legal_benchmarks/full_reports/case_*.md`

---

## 1. Executive Summary

Prior to sealing **Draft v0.1** (`2026-10-24` release) of the Minab Judicial Determination Dossier, People for Peace & Justice ry (PFPJ ry) conducted a systematic line-by-line audit of all United Nations document numbers, ICTY / ECtHR / ICJ / PCIJ / ICC case citations, statutory and treaty provisions, paragraph identifiers (`¶` / `§`), and technical ordnance identifiers across Chapters I through X of `FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.md`.

All nineteen benchmark cases (**Cases 01–19**), all twenty-five newly integrated benchmark clauses (`¶ 8 nonies`, `¶ 14 ter`, `¶ 16 quater`, `¶ 30 bis`, `¶ 36 bis`, `¶ 38 quater`, `¶ 43 ter`, `¶ 45 ter`, `¶ 47 quater`, `¶ 48 octies`, `¶ 48 sexies bis`, `¶ 50 bis`, `¶ 52 ter`, `¶ 57 quater`, `¶ 61 ter`, `¶ 63 bis`, `¶ 72 ter`, `¶ 76 ter`, `¶ 78 ter`, `¶ 81 septies`, `¶ 84 bis`, `¶ 85 quinquies`, `¶ 85 ter`, `¶ 90 quater`, `¶ 91 ter`), and the restructured **Chapter X (`§§ 10.1–10.5`)** were cross-checked directly against the primary benchmark dossiers in `Campaigns/minab/legal_benchmarks/`.

**Audit Outcome:** **PASS (100% Verified after 8 Targeted Corrections).** Zero fabricated citations, zero unverified UN document symbols, and zero UTF-8 mojibake remain.

---

## 2. Itemized Log of Corrections Applied

| # | File & Location | Discrepancy Identified | Correction Applied |
| :--- | :--- | :--- | :--- |
| **1** | `FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.md` (`¶ 48 octies (bis)` in § 4.7, `¶ 50 bis` in § 5.1) & `MASTER_EXHIBIT_DOSSIER.md` (`EXH-MUN-002.2`) | **DLA CAGE Code Discrepancy (`96214` vs. `05047`):** `¶ 50 bis` and `¶ 48 octies` cited CAGE Code `96214` (from Case 18 *Mastaba Market*, which is registered to Texas Instruments Inc. / Raytheon Defense Systems in Dallas/McKinney, TX for Paveway guidance kits) as identical to the Minab Tomahawk circuit board CAGE Code, whereas `¶ 8 ter`, `¶ 8 octies`, and `¶ 57 ter` correctly cited **`05047`** (**Raytheon Missile Systems, Tucson, Arizona**). | Harmonized all Minab Tomahawk DSMAC circuit board references (`ASSY 16200-6523910-1 REV D`, `EXH-MUN-002.2`) to CAGE Code **`05047`** (**Raytheon Missile Systems, Tucson, Arizona**), while explicitly distinguishing Case 18 (*Mastaba Market*) CAGE Code **`96214`** (Texas Instruments / Raytheon Defense Systems Paveway guidance fin/seeker assembly) in `¶ 50 bis`. |
| **2** | `benchmarked_facts_cases_01_to_19.md` (Case 15, line 253) | **CAGE Code Digit Transposition (`94271` vs. `94117`):** Line 253 transposed the last two digits of Lockheed Martin's CAGE code (`94271`), whereas `case_15_dahyan_school_bus_un_gee_full_report.md` and `FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.md` (`¶ 8 ter`, `¶ 8 octies`, `¶ 57 ter`, `¶ 91 bis`) correctly cite **`94117`** (Lockheed Martin Missiles and Fire Control, Orlando, FL). | Corrected `94271` → `94117` in `benchmarked_facts_cases_01_to_19.md`. |
| **3** | `FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.md` (`¶ 8 quater` (3), line 155) | **Explosive Fill Typo (`PBXN-109` vs. `PBXN-107`):** Line 155 referred to the WDU-36/B warhead explosive fill as `PBXN-109`, whereas `¶ 48 octies (bis)`, `¶ 51`, `¶ 52 bis`, `¶ 52 ter`, `¶ 83 bis`, `¶ 96(ii)`, and `EXH-MUN-002.4` all specify **`PBXN-107`**. | Corrected `PBXN-109` → `PBXN-107` in `¶ 8 quater` (3). |
| **4** | `FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.md` (§ 4.5 vs. § 4.7, lines 450 & 455) | **Duplicate Paragraph Identifiers (`48 septies` & `48 octies`):** Both § 4.5 (lines 421, 423) and § 4.7 (lines 450, 455) used the numbers `48 septies` and `48 octies`. | Retained `48 septies` (Case 05 benchmark) and `48 octies` (Case 06 benchmark) in § 4.5, and disambiguated the § 4.7 eyewitness and physical debris clauses as `48 septies (bis)` and `48 octies (bis)`. |
| **5** | `FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.md` (§ 6.4, lines 561–566) | **Out-of-Sequence Paragraph (`72 ter`):** `¶ 72 ter` (Cases 02 & 12 sensor ambiguity benchmark) was positioned after `¶ 73` and `¶ 73 bis`. | Repositioned `¶ 72 ter` immediately after `¶ 72 bis` and prior to `¶ 73` and `¶ 73 bis` to restore strict numerical progression (`71`, `72`, `72 bis`, `72 ter`, `73`, `73 bis`). |
| **6** | `FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.md` (`¶ 8 ter` Row XII, line 147 & `¶ 8 octies` (8), line 190) | **Internal Cross-Reference Alignment:** `¶ 8 octies` (8) referenced `Chapter II, § 2.3 [¶ 18 bis]` (whereas § 2.3 contains `¶¶ 13–14 ter` and `¶ 18` is in Chapter III § 3.1); `¶ 8 ter` Row XII referenced `¶¶ 97–97 ter` (whereas § 10.2 spans `¶¶ 97–97 quater`). | Updated cross-references to `(Chapter II, § 2.3 [¶¶ 14–14 ter])` and `[Chapter X, § 10.2 (¶¶ 97–97 quater)](#chapter-10-2)`. |
| **7** | `FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.md` (`¶ 85 ter` in § 7.5 & `¶ 90 quater` in § 8.2) | **Citation Completeness:** `¶ 85 ter` cited only `UN Doc. S/PRST/2006/35` for Case 10 (*Second Qana*); `¶ 90 quater` cited shorthand `*McCann v. UK* (1995)` without application number or paragraphs. | Added `UN Doc. A/HRC/3/2, ¶¶ 147–158; HRW, *Fatal Strikes*, 2006` to `¶ 85 ter`, and expanded `¶ 90 quater` to `*McCann and Others v. United Kingdom* (App. no. 18984/91, Grand Chamber Judgment of 27 September 1995, §§ 149–150, 194)` as applied in Case 03 (§§ 171, 189–191) and Case 19 (§§ 171, 195–199). |
| **8** | `FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.md` (Table of Contents, lines 83–84) | **TOC Heading Parity:** Line 83 used ASCII `Chorzow` and `30-37`; line 84 read `Confirmation of Charges` while the § 10.3 heading read `Determination of Charges`. | Synchronized TOC lines 83–84 (`Chorzów`, `30–37`, `Determination of Charges`) with the exact section headings in Chapter X. |

---

## 3. Verification Matrix: Newly Integrated 19-Case Benchmark Clauses

Every newly added clause and Chapter X section required under Issue #60 has been verified against its primary benchmark source dossier:

| Dossier Clause | Section | Benchmark Case(s) | Verified Primary Citations & Paragraph Numbers | Status |
| :--- | :--- | :--- | :--- | :--- |
| **`¶ 8 nonies`** | § 1.4 | Cases 01–19 (Master Synthesis) | Six systemic failure vectors synthesizing all 19 benchmark cases across ICTY, ECtHR, UN COI/GEE/UNAMA, and DoD/CENTCOM inquiries | **VERIFIED** |
| **`¶ 14 ter`** | § 2.3 | Cases 04, 13, 17, 18 | UN COI Syria (`UN Doc. A/HRC/36/55`, `UN Doc. A/HRC/34/64`); Amnesty Crisis Evidence Lab (2022); Bellingcat & HRW (2016); ICTY Rule 89(C); Berkeley Protocol (OHCHR, 2020) | **VERIFIED** |
| **`¶ 16 quater`** | § 2.4 | Cases 05, 07, 15 | UNAMA *Dasht-e Archi* Special Report (May 2018); UN GEE Yemen (`UN Doc. A/HRC/42/17, ¶ 25`; `A/HRC/42/CRP.1, ¶¶ 449–450, 896–905`); JIAT (1 Sept 2018); US CENTCOM / Air Force IG (Nov 2021) | **VERIFIED** |
| **`¶ 30 bis`** | § 3.3 | Case 14 (*Abs Hospital*) | UN COI/GEE Yemen (`UN Doc. A/HRC/39/43, ¶ 40`); MSF Abs Incident Review (2016); JIAT Case 29 Concession (Dec 2016); AP I Art. 57(2)(a)(ii) | **VERIFIED** |
| **`¶ 36 bis`** | § 3.6 | Cases 13, 16, 17 | UN COI Syria (`UN Doc. A/HRC/34/64, ¶¶ 35–42`); UN Secretary-General Panel of Inquiry (`UN Doc. S/2020/303`); HRW *Death from the Sky* (2013); UN COI Ukraine (`UN Doc. A/77/533`) | **VERIFIED** |
| **`¶ 38 quater`** | § 3.7 | Cases 09, 10, 12 | UN Report on Qana (`UN Doc. S/1996/337`); UN COI Lebanon (`UN Doc. A/HRC/3/2, ¶¶ 147–158`); HRW *Fatal Strikes* (2006); ICTY OTP NATO Report (`¶¶ 86–89`); AP I Arts. 50(3), 51(8) | **VERIFIED** |
| **`¶ 43 ter`** | § 4.2 | Cases 07, 13, 15, 16 | UNAMA (2018); Bellingcat & Atlantic Council *Breaking Aleppo* (2017); UN GEE (`UN Doc. A/HRC/42/17`); HRW (2013) | **VERIFIED** |
| **`¶ 45 ter`** | § 4.3 | Cases 01, 08, 13, 15 | ICTY OTP NATO Report (`¶ 80`); DoD Title V Gulf War Final Report (1992, App. O); Bellingcat (2016); JIAT (2018) | **VERIFIED** |
| **`¶ 47 quater`** | § 4.4 | Cases 11, 13, 14, 18 | MSF *Kunduz Trauma Centre Internal Review* (Nov 2015); USCENTCOM AR 15-6 Kunduz Report (April 2016); UNSC Res. 2286 (2016); `UN Doc. A/HRC/34/64`; HRW & Amnesty (`MDE 31/3815/2016`) | **VERIFIED** |
| **`¶ 48 octies`** | § 4.5 | Case 06 (*Dora Farms*) | HRW *Off Target: The Conduct of the War and Civilian Casualties in Iraq* (2003, pp. 22–26); DIA Post-Strike BDA (2004); `UN Doc. A/HRC/63/61` | **VERIFIED** |
| **`¶ 48 sexies bis`** | § 4.6 | Case 07 (*Dasht-e Archi*) | UNAMA Special Report on the Airstrike in Dasht-e Archi District (May 2018, 81% child casualty verification); Rome Statute Art. 30 | **VERIFIED** |
| **`¶ 50 bis`** | § 5.1 | Case 18 (*Mastaba Market*) | HRW *US Bombs Used in Deadly Market Strike* (April 2016); Bellingcat (2016); DLA CAGE Code `96214` (TI/Raytheon Paveway in Mastaba) vs. CAGE Code `05047` (Raytheon Missile Systems in Minab, `ASSY 16200-6523910-1 REV D`) | **VERIFIED** |
| **`¶ 52 ter`** | § 5.2 | Cases 03, 17 | Amnesty Crisis Evidence Lab *Chernihiv* (March 2022); `UN Doc. A/77/533`; ECtHR *Isayeva v. Russia* (App. no. 57950/00, 2005) | **VERIFIED** |
| **`¶ 57 quater`** | § 5.4 | Case 09 (*Qana UNIFIL*) | Report of the UN Secretary-General's Military Adviser Maj. Gen. Franklin van Kappen (`UN Doc. S/1996/337`, 7 May 1996) | **VERIFIED** |
| **`¶ 61 ter`** | § 6.1 | Case 06 (*Dora Farms*) | HRW *Off Target* (2003); David Turns (2006); Yoram Dinstein *Conduct of Hostilities* (2010); AP I Art. 57(2)(a)(i) | **VERIFIED** |
| **`¶ 63 bis`** | § 6.2 | Case 01 (*Belgrade Embassy*) | ICTY OTP *Final Report to the Prosecutor by the Committee Established to Review the NATO Bombing Campaign* (2000, `¶¶ 80–85`); Pickering Briefing (1999) | **VERIFIED** |
| **`¶ 72 ter`** | § 6.4 | Cases 02, 12 | ECtHR Grand Chamber *Hanan v. Germany* (App. no. 4871/16, 2021); *Deutscher Bundestag Drucksache* 17/7400 (2011); ICTY OTP NATO Report (`¶¶ 86–89`); AP I Art. 57(2)(b) | **VERIFIED** |
| **`¶ 76 ter`** | § 6.5 | Case 19 (*Shaami-Yurt*) | ECtHR *Isayeva, Yusupova and Bazayeva v. Russia* (Apps. nos. 57947/00–57949/00, HUDOC `001-68379`, `§§ 185–187, 222`); ILC ARSIWA Art. 4 | **VERIFIED** |
| **`¶ 78 ter`** | § 7.1 | Case 17 (*Chernihiv*) | ICRC EWIPA Report (2022); UN COI Ukraine (`UN Doc. A/77/533, ¶ 46`); AP I Art. 51(4)(b) | **VERIFIED** |
| **`¶ 81 septies`** | § 7.2 | Case 14 (*Abs Hospital*) | `UN Doc. A/HRC/39/43, ¶ 40`; Adil Ahmad Haque (*Just Security*, 2016); AP I Art. 57(2)(a)(ii) | **VERIFIED** |
| **`¶ 84 bis`** | § 7.3 | Cases 03, 19 | ECtHR *Isayeva v. Russia* (`§§ 189–191`); *Isayeva, Yusupova and Bazayeva v. Russia* (`§§ 195–199`); AP I Art. 51(5)(b); Customary IHL Rule 14 | **VERIFIED** |
| **`¶ 85 quinquies`** | § 7.4 | Cases 13, 16 | Rome Statute Art. 8(2)(b)(ix); `UN Doc. A/HRC/34/64` (*Hass School*); `UN Doc. A/HRC/24/46` (*Al-Bara*); UN CRC Art. 28; UNSC Res. 2601 (2021) | **VERIFIED** |
| **`¶ 85 ter`** | § 7.5 | Cases 08, 10 | `UN Doc. S/PRST/2006/35`; `UN Doc. A/HRC/3/2, ¶¶ 147–158`; HRW *Fatal Strikes* (2006); HRW *Needless Deaths in the Gulf War* (1991); AP I Arts. 57(2)(c), 65(2) | **VERIFIED** |
| **`¶ 90 quater`** | § 8.2 | Cases 03, 19 | Rome Statute Art. 28; ECtHR *McCann and Others v. United Kingdom* [GC] (App. no. 18984/91, 1995, `§§ 149–150, 194`); Case 03 (`§§ 171, 189–191`); Case 19 (`§§ 171, 195–199`) | **VERIFIED** |
| **`¶ 91 ter`** | § 8.3 | Case 18 (*Mastaba Market*) | Amnesty International (`MDE 31/3815/2016`); Arms Trade Treaty Art. 6; *R (CAAT) v. Secretary of State for International Trade* (`[2019] EWCA Civ 1020`); ILC ARSIWA Art. 16 | **VERIFIED** |
| **`§§ 10.1–10.5`** | Ch. X | PCIJ *Chorzów Factory*, Cases 01, 05, 08, 09, 13, 16 & ICC Model | *Factory at Chorzów* (1928, P.C.I.J., Ser. A, No. 17, p. 47); ILC ARSIWA Arts. 30–37; Belgrade Settlement (`39 ILM 644`, $32.5M); `UNGA Res. 51/233` (1997); $300,000,000 USD Itemized Reparations Schedule; ICC Rome Statute Art. 61(7) Counts 1–5 (Arts. 8(2)(b)(i), (ii), (iv), (v), (ix)) & Modes of Liability (Arts. 25(3)(a)–(c), 28(a)–(b)) | **VERIFIED** |

---

## 4. Complete Case-by-Case Verification Registry (Cases 01–19)

1. **Case 01 — Belgrade Chinese Embassy Bombing (7 May 1999):** ICTY OTP Final Report (13 June 2000, 39 ILM 1257), `¶¶ 80–85`; Under Secretary Thomas Pickering Briefing (17 June 1999); US-PRC Memoranda of Understanding (`39 ILM 644`, 1999, $4.5M humanitarian + $28M property = $32.5M). **Verified.**
2. **Case 02 — Kunduz River Sandbank Fuel Tankers Airstrike (4 Sept 2009):** ECtHR Grand Chamber, *Hanan v. Germany*, App. no. 4871/16, Judgment of 16 Feb 2021, `§§ 132–145, 200–235`; German Federal Prosecutor General (*Generalbundesanwalt*) Decision of 16 April 2010 (`3 BJs 6/10-4`); *Deutscher Bundestag*, 17. Wahlperiode, *Drucksache* 17/7400 (25 Oct 2011). **Verified.**
3. **Case 03 — Katyr-Yurt Convoy and Village Bombardment (4–7 Feb 2000):** ECtHR, *Isayeva v. Russia*, App. no. 57950/00, Judgment of 24 Feb 2005 (HUDOC `001-68381`), `§§ 171, 180–191, 200`; *Abakarova v. Russia*, App. no. 16664/07 (2015). **Verified.**
4. **Case 04 — Al-Jina Mosque Complex Airstrike (16 March 2017):** UN COI Syria, `UN Doc. A/HRC/36/55` (8 Aug 2017), `¶¶ 53–61` & Annex III `¶¶ 12–17`; USCENTCOM AR 15-6 Briefing (Maj. Gen. Patrick Roberson, 7 June 2017); Bellingcat (March 2017); HRW (April 2017). **Verified.**
5. **Case 05 — Kabul Drone Strike on the Ahmadi Family (29 Aug 2021):** USCENTCOM Statement (Gen. Kenneth F. McKenzie Jr., 17 Sept 2021); Department of the Air Force Inspector General Review (Lt. Gen. Sami D. Said, 3 Nov 2021); *The New York Times* Visual Investigation (10 Sept 2021). **Verified.**
6. **Case 06 — Dora Farms Decapitation Strike, Baghdad (19 March 2003):** HRW, *Off Target: The Conduct of the War and Civilian Casualties in Iraq* (Dec 2003), pp. 22–26; DIA Post-Strike BDA (2004). **Verified.**
7. **Case 07 — Dasht-e Archi Religious School (Madrassa) Airstrike, Kunduz (2 April 2018):** UNAMA Special Report, *Airstrikes in Dasht-e Archi District, Kunduz Province, 2 April 2018* (May 2018, 107 casualties, 81% children). **Verified.**
8. **Case 08 — Al-Amiriyah Public Shelter No. 25 Massacre, Baghdad (13 Feb 1991):** Middle East Watch / HRW, *Needless Deaths in the Gulf War* (1991), Chs. 3 & 7; US DoD *Conduct of the Persian Gulf War: Final Report to Congress* (Title V, April 1992, Appendix O); USAF *Gulf War Air Power Survey* (GWAPS Vol. II, Part I, pp. 340–344, 1993). **Verified.**
9. **Case 09 — Shelling of the UNIFIL Compound at Qana (18 April 1996):** Report of the UN Secretary-General's Military Adviser (Maj. Gen. Franklin van Kappen), `UN Doc. S/1996/337` (7 May 1996); `UNGA Res. 51/233` (13 June 1997). **Verified.**
10. **Case 10 — Second Qana Residential Building Airstrike (30 July 2006):** UN COI Lebanon, `UN Doc. A/HRC/3/2` (23 Nov 2006), `¶¶ 147–158`; UNSC Presidential Statement `S/PRST/2006/35`; HRW, *Fatal Strikes* (Aug 2006). **Verified.**
11. **Case 11 — Kunduz MSF Trauma Centre Aerial Bombardment (3 Oct 2015):** USCENTCOM Declassified AR 15-6 Report (29 April 2016); MSF *Internal Review: Kunduz* (Nov 2015); `UNSC Res. 2286` (3 May 2016). **Verified.**
12. **Case 12 — Koriša Village Refugee Encampment Bombing (13 May 1999):** ICTY OTP NATO Review Committee Report (2000), `¶¶ 86–89`; HRW *Civilian Deaths in the NATO Air Campaign* (Feb 2000). **Verified.**
13. **Case 13 — Hass School Complex ("Kamal Qari") Airstrike, Idlib (26 Oct 2016):** UN COI Syria, `UN Doc. A/HRC/34/64` (Feb 2017), `¶¶ 35–42`; UN Board of Inquiry Summary, `UN Doc. S/2020/303` (April 2020); Bellingcat & HRW (Nov 2016). **Verified.**
14. **Case 14 — Abs Rural Hospital Airstrike, Hajjah (15 Aug 2016):** UN GEE Yemen, `UN Doc. A/HRC/39/43` (Aug 2018), `¶ 40`; MSF Abs Investigation Report (27 Sept 2016); JIAT Case 29 Statement (Dec 2016). **Verified.**
15. **Case 15 — Dahyan Market School Bus Airstrike, Sa'ada (9 Aug 2018):** UN GEE Yemen, `UN Doc. A/HRC/42/17` (Aug 2019), `¶ 25` & `UN Doc. A/HRC/42/CRP.1`, `¶¶ 449–450, 896–905`; UN Secretary-General CAAC Report, `UN Doc. A/73/907–S/2019/509`, `¶¶ 176–192`; JIAT Press Release (1 Sept 2018); Bellingcat & HRW (Aug–Sept 2018, Lockheed Martin CAGE Code `94117`). **Verified.**
16. **Case 16 — Al-Bara Elementary School Bombing, Idlib (Oct 2013):** HRW, *Death from the Sky: Deliberate and Indiscriminate Airstrikes on Civilians by Syrian Armed Forces* (2013); UN COI Syria, `UN Doc. A/HRC/24/46` (2013). **Verified.**
17. **Case 17 — Chernihiv Schools Nos. 18 & 21 Multi-Bomb Strike (3 March 2022):** UN COI Ukraine, `UN Doc. A/77/533` (Oct 2022), `¶ 46`; Amnesty International Crisis Evidence Lab (9 March 2022). **Verified.**
18. **Case 18 — Mastaba Market Double Airstrike, Hajjah (15 March 2016):** HRW, *Yemen: US Bombs Used in Deadly Market Strike* (7 April 2016); Amnesty International, `MDE 31/3815/2016`; Bellingcat (2016, Paveway CAGE Code `96214`); `UN Doc. A/HRC/39/43`. **Verified.**
19. **Case 19 — Shaami-Yurt Refugee Convoy Bombardment (29 Oct 1999):** ECtHR, *Isayeva, Yusupova and Bazayeva v. Russia*, Apps. nos. 57947/00, 57948/00, and 57949/00, Judgment of 24 Feb 2005 (HUDOC `001-68379`), `§§ 171, 185–199, 208–225`. **Verified.**

---
**CERTIFIED** by the Legal Quality Assurance Gate of People for Peace & Justice ry (PFPJ ry), Helsinki, Finland.
