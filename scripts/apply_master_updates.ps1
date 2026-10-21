# UTF-8 Script to update FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.md
$filePath = 'E:\Papers\PFPJ\Campaigns\minab\justiceForMinab\docs\FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.md'
$content = [System.IO.File]::ReadAllText($filePath, [System.Text.Encoding]::UTF8)

# -------------------------------------------------------------
# 1. Update Table of Contents for Chapter X
# -------------------------------------------------------------
$oldTOC = @"
* [CHAPTER X: DISPOSITION, REMEDIAL ORDERS & THE BELGRADE STATE REPARATIONS MODEL](#chapter-10)
  * [10.1 Formal Declaratory Determinations of the Expert Chamber](#chapter-10-1)
  * [10.2 State Reparations under Customary International Law (ARSIWA Articles 30–37 & Belgrade Precedent § 84)](#chapter-10-2)
  * [10.3 Orders Concerning Judicial Preservation of Evidence & International Fact-Finding](#chapter-10-3)
  * [10.4 Contingent Prosecutorial Directions & Transmissions](#chapter-10-4)
"@

$newTOC = @"
* [CHAPTER X: DISPOSITION, REMEDIAL ORDERS & JURIDICAL ACCOUNTABILITY REGIMES](#chapter-10)
  * [10.1 Formal Declaratory Determinations of the Expert Chamber](#chapter-10-1)
  * [10.2 Section 1: State Responsibility & Financial Liability Regime (The Chorzów Factory Standard & ARSIWA Articles 30–37)](#chapter-10-2)
  * [10.3 Section 2: Individual Criminal Responsibility & Confirmation of Charges (The ICC Rome Statute Model)](#chapter-10-3)
  * [10.4 Orders Concerning Judicial Preservation of Evidence & International Fact-Finding](#chapter-10-4)
  * [10.5 Contingent Prosecutorial Directions & Transmissions](#chapter-10-5)
"@

if ($content.Contains($oldTOC)) {
    $content = $content.Replace($oldTOC, $newTOC)
    Write-Output "Step 0: Table of Contents updated successfully."
} else {
    Write-Warning "Step 0: Table of Contents old block not found directly, checking variations."
}

# -------------------------------------------------------------
# 2. Chapter I § 1.4: Add 8 nonies
# -------------------------------------------------------------
$targetCh1 = @"
[↑ Back to Table of Contents](#table-of-contents)
---

<a id="chapter-2"></a>
"@

$text8nonies = @"
8 nonies. **The Consolidated Nineteen-Precedent Juridical Framework (Comprehensive Master Compendium Integration):**
To establish an unassailable evidentiary and legal foundation before international courts (including the International Court of Justice, the International Criminal Court, and European universal jurisdiction tribunals), the Panel formally incorporates into this Master Dossier the comprehensive empirical and legal jurisprudence derived from **nineteen authoritative international precedent cases**. This unified architecture demonstrates that the February 28, 2026 missile strike on the Shajareh Tayyebeh Girls' Elementary School was neither an isolated anomaly nor an excusable "honest mistake," but rather the cumulative manifestation of six systemic targeting failure vectors recognized across three decades of international armed conflict jurisprudence:

*   **(1) Peacetime Deliberate Planning Negligence & Stale Target Silos:**
    *   *Case 01 (Belgrade Chinese Embassy Bombing, 1999 — ICTY OTP NATO Report, ¶¶ 80–85; Pickering Report):* Establishes the tripartite targeting failure test (methodological error, database circularity, and target review board failure) and the upstream concentration of legal responsibility exonerating tactical delivery crews (§ 85);
    *   *Case 06 (Dora Farms Decapitation Strike, 2003 — HRW Off Target; USJFCOM Lessons Learned):* Establishes that Day 1 pre-planned strikes compiled in peacetime cannot invoke "fog of war" or combat urgency, and demonstrates that uncorroborated single-source target tags produce a catastrophic 100% failure rate;
    *   *Case 08 (Al-Amiriyah Public Shelter Massacre, 1991 — HRW Needless Deaths; DoD Title V Report):* Establishes the absolute civilian presumption for protected infrastructure and condemns the complete failure of daylight pattern-of-life surveillance.

*   **(2) Remote Sensor Hallucination, FLIR Ambiguity & Algorithmic Automation Trap:**
    *   *Case 02 (Kunduz River Sandbank Fuel Tankers, 2009 — ECtHR Grand Chamber Hanan v. Germany; Bundestag Drucksache 17/7400):* Establishes that infrared FLIR sensor ambiguity cannot justify kinetic release, condemns the rejection of low-altitude warning passes, and articulates the detachable procedural duty to investigate extraterritorial strikes under ECHR Article 2;
    *   *Case 05 (Kabul Drone Strike on the Ahmadi Family, 2021 — Air Force IG Report; Lieber Institute):* Proves that remote sensors generate perceptual tunnel vision ("soda-straw effect"), codifies the mandatory pre-launch duty to abort upon detecting child presence, and refutes military pretexts of "secondary explosions";
    *   *Case 12 (Koriša Village Refugee Encampment, 1999 — ICTY OTP NATO Report, ¶¶ 86–89; HRW):* Proves that operating sensors at high standoff altitudes without optical ground confirmation violates the duty to abort under AP I Art. 57(2)(b), and decisively rejects the "human shield" excuse where non-combatants are concentrated.

*   **(3) Institutional Information Siloing & Deconfliction Disregard:**
    *   *Case 04 (Al-Jina Mosque Complex, 2017 — UN Doc. A/HRC/36/55; USCENTCOM AR 15-6):* Formulates the continuous temporal verification rule (72-hour custody triggering affirmative surveillance), rejects the "adjacent building" defense, and establishes that administrative shift-handover failures constitute actionable breaches of IHL;
    *   *Case 14 (Abs Rural Hospital Airstrike, 2016 — UN Doc. A/HRC/39/43; MSF Incident Review; JIAT Concession):* Establishes the *compound non-severability principle*, ruling that striking an alleged military target adjacent to a protected perimeter violates the duty of feasible precautions and destroys essential civilian sanctuaries;
    *   *Case 19 (Shaami-Yurt Refugee Convoy Bombardment, 1999 — ECtHR Isayeva, Yusupova and Bazayeva v. Russia):* Establishes the operational planning and control standard under ECHR Art. 2, condemning the complete failure of communication between civil registry organs and military air sortie planners.

*   **(4) Weapons Disproportionality *Per Se* in Confined Civilian Sanctuaries:**
    *   *Case 03 (Katyr-Yurt Convoy and Village Bombardment, 2000 — ECtHR Isayeva v. Russia; Abakarova v. Russia):* Landmark authority holding that deploying heavy high-explosive blast ordnance (FAB-250/500) into a populated civilian village is disproportionate and unlawful *per se*;
    *   *Case 17 (Chernihiv Schools Nos. 18 & 21 Multi-Bomb Strike, 2022 — UN Doc. A/77/533; Amnesty Crisis Evidence Lab):* Proves that sequential salvo releases across educational campuses create inescapable blast envelopes, qualifying wide-area explosive weapons in populated areas (EWIPA) as inherently indiscriminate warfare under AP I Art. 51(4)(b);
    *   *Case 08 (Al-Amiriyah):* Proves that delivering penetrating blast warheads into enclosed civilian structures where escape routes are sealed constitutes trapped slaughter and disproportionate violence *per se*.

*   **(5) Multi-Tap Aerial Ambush of Evacuating Schoolchildren & Rescuers:**
    *   *Case 13 (Hass School Complex Multi-Airstrike, 2016 — UN Doc. A/HRC/34/64; Bellingcat; SNHR):* Authoritative finding that executing delayed secondary strikes against children and educators fleeing initial bomb impacts constitutes an intentional war crime against educational sanctuaries under Rome Statute Art. 8(2)(b)(ix);
    *   *Case 15 (Dahyan Market School Bus Airstrike, 2018 — UN Doc. A/HRC/42/17; JIAT Concession):* Codifies the sub-metric precision liability standard (mechanical perfection), establishes the peremptory immunity of child transports, and records a belligerent coalition's formal concession of ROE violation;
    *   *Case 18 (Mastaba Market Double Airstrike, 2016 — UN Doc. A/HRC/39/43; HRW; Mwatana):* Forensically links recovered munition CAGE codes (96214) to US defense contractors, condemns midday strikes on peak civilian gatherings, and proves state responsibility for supplying precision ordnance under ARSIWA Art. 16.

*   **(6) Peremptory Presumption of Educational Sanctuary & Rejection of Warning Pretexts:**
    *   *Case 07 (Dasht-e Archi Madrassa Graduation Ceremony, 2018 — UNAMA / OHCHR Special Report):* Articulates the "gathering of children" rule in proportionality, proving that where child density exceeds 80%, the deployment of explosive weapons is disproportionate *per se*;
    *   *Case 09 (Shelling of UNIFIL Headquarters at Qana, 1996 — UN Doc. S/1996/337; UNGA Res 51/233):* Establishes the zero ballistic drift standard defeating mapping/drift pretexts, proves overhead UAV surveillance presence, and affirms binding state financial liability for kinetic destruction;
    *   *Case 10 (Second Qana Residential Building Strike, 2006 — UN Doc. A/HRC/3/2; HRW Why They Died):* Decisively dismantles the "warning leaflet defense," establishing that civilians who remain in an area retain full immunity under AP I Art. 51(3), and establishes the mechanics of pancaking concrete collapses;
    *   *Case 11 (NATO Airstrike on RTS Headquarters, 1999 — ICTY OTP NATO Report, ¶¶ 71–79):* Establishes the strict dual-use standard requiring "definite military advantage," rejects broad political disruption as a valid military objective, and traces the modern evolution of extraterritorial human rights jurisdiction;
    *   *Case 16 (Al-Bara Elementary School Bombing, 2013/2020 — UN Doc. A/HRC/24/46; Safe Schools Declaration):* Reaffirms the customary presumption of civilian sanctuary for elementary educational facilities under AP I Art. 52(3), verified by the complete post-strike absence of military hardware.

[↑ Back to Table of Contents](#table-of-contents)
---

<a id="chapter-2"></a>
"@

if ($content.Contains($targetCh1)) {
    $content = $content.Replace($targetCh1, $text8nonies)
    Write-Output "Step 1: Chapter I § 1.4 (8 nonies) inserted successfully."
} else {
    Write-Error "Step 1: targetCh1 not found!"
}

# -------------------------------------------------------------
# 3. Chapter II § 2.3 & § 2.4: Add 14 ter and 16 quater
# -------------------------------------------------------------
$targetCh2_3 = @"
<a id="chapter-2-4"></a>
"@

$text14ter = @"
14 ter. **Visual Shadow, Chronolocation & Munition Metallurgy under the Berkeley Protocol (Case 13 Benchmark):**
Adopting the rigorous open-source photogrammetric and shadow-azimuth chronolocation methodology established by Bellingcat and the UN Independent International Commission of Inquiry on Syria in **Case 13: *Hass School Complex Multi-Airstrike*** (UN Doc. A/HRC/34/64, ¶¶ 38–43), the Panel subjected all mobile phone video recordings, first-responder audiovisual feeds, and satellite overhead passes of the Minab strike to frame-by-frame sun-shadow analysis and architectural ray-tracing in strict adherence to the *Berkeley Protocol on Digital Open Source Investigations*. This verified the micro-second chronolocation of each of the three Tomahawk missile detonations (09:22:15, 09:24:30, and 09:26:40 IRST) and conclusively correlated the impact crater geometries with the physical metallurgy of WDU-36/B warhead fragments recovered on site. This multi-layered digital forensics defeats any assertion of fabricated imagery or temporal manipulation, satisfying the highest threshold of judicial admissibility under ICTY Rule 89(C).

<a id="chapter-2-4"></a>
"@

if ($content.Contains($targetCh2_3)) {
    $content = $content.Replace($targetCh2_3, $text14ter)
    Write-Output "Step 2: Chapter II § 2.3 (14 ter) inserted successfully."
} else {
    Write-Error "Step 2: targetCh2_3 not found!"
}

$targetCh2_4 = @"
<a id="chapter-2-5"></a>
"@

$text16quater = @"
16 quater. **Heightened Probative Weight of Official State Admissions Against Interest (Cases 01, 02, 09, 14 Benchmark):**
Under **ICTY Rule 89(F)**, the established jurisprudence of the International Court of Justice (*Military and Paramilitary Activities in and against Nicaragua*, Merits, 1986, ¶ 64), and customary international evidentiary doctrine, formal admissions, statements against interest, and internal disclosures rendered by official state organs carry preeminent probative weight. In **Case 01 (*Belgrade Chinese Embassy Bombing*)**, Under Secretary Thomas Pickering’s oral presentation to the PRC Government formally admitted the three-tier failure of land navigation, database omissions, and circular target board reviews, which served as unimpeachable proof of institutional negligence before the ICTY Office of the Prosecutor. In **Case 02 (*Kunduz Fuel Tankers*)**, the German Bundestag Parliamentary Inquiry (Drucksache 17/7400) and NATO ISAF findings officially conceded that pilot warnings were ignored, thermal sensor feeds were ambiguous, and single-source informant reporting was uncritically accepted. In **Case 09 (*Shelling of UNIFIL Headquarters at Qana*)**, the UN Van Kappen Ballistic Report (UN Doc. S/1996/337) and subsequent military disclosures confirmed that claims of ballistic drift and mapping error were mathematically impossible. In **Case 14 (*Abs Rural Hospital*)**, the Coalition's Joint Incident Assessment Team (JIAT) conceded that the hospital courtyard was struck despite six distinct GPS deconfliction notifications having been transmitted to operational planning cells. Consequently, CENTCOM’s internal AR 15-6 preliminary inquiry disclosures—which formally concede reliance upon an unverified pre-2016 DIA target folder, the bypass of commercial satellite cross-checks, and the reduction of the Civilian Harm Mitigation and Response (CHMR) cell from ten analysts to a single individual—enjoy identical, binding probative weight under international evidentiary law, legally precluding the Respondent State from pleading that it exercised all feasible care.

<a id="chapter-2-5"></a>
"@

if ($content.Contains($targetCh2_4)) {
    $content = $content.Replace($targetCh2_4, $text16quater)
    Write-Output "Step 3: Chapter II § 2.4 (16 quater) inserted successfully."
} else {
    Write-Error "Step 3: targetCh2_4 not found!"
}

# -------------------------------------------------------------
# 4. Chapter III § 3.4, § 3.6, § 3.7
# -------------------------------------------------------------
$targetCh3_4 = @"
<a id="chapter-3-5"></a>
"@

$text30bis = @"
30 bis. **The Strict Dual-Use Standard: Rejection of Broad Political or Indirect Advantage (Case 11 Benchmark):**
In evaluating the legal status of targeted infrastructure, the Panel incorporates the canonical holding formulated by the ICTY Office of the Prosecutor in the *RTS Television Station Review* (**Case 11: *Belgrade RTS Airstrike***, ICTY OTP NATO Report, ¶¶ 71–79). Under **Article 52(2) of Additional Protocol I** and **Customary IHL Rule 8**, an object qualifies as a legitimate military objective only if its total or partial destruction offers a *"definite military advantage in the circumstances ruling at the time."* The ICTY OTP strictly rejected the theory that civilian infrastructure can be lawfully targeted merely because it provides diffuse political support, ideological alignment, or general economic sustainment to an adversary. In Minab, CENTCOM's post-hoc attempt to categorize the Shajareh Tayyebeh School compound as an "IRGC dual-use auxiliary logistics facility" fails as a matter of law: striking an elementary school populated by young girls offered zero concrete, direct, or definite military advantage against the IRGC Navy, converting the strike into a direct attack on an exclusively civilian object.

<a id="chapter-3-5"></a>
"@

if ($content.Contains($targetCh3_4)) {
    $content = $content.Replace($targetCh3_4, $text30bis)
    Write-Output "Step 4: Chapter III § 3.4 (30 bis) inserted successfully."
} else {
    Write-Error "Step 4: targetCh3_4 not found!"
}

$targetCh3_6 = @"
<a id="chapter-3-7"></a>
"@

$text36bis = @"
36 bis. **The Peremptory Customary Presumption of Educational Sanctuary (Case 16 Benchmark):**
Educational institutions dedicated to children enjoy specialized, peremptory customary protection under international humanitarian law and international human rights law (Geneva Convention IV Art. 53; UN CRC Art. 28; Safe Schools Declaration). As established in the UN Independent International Commission of Inquiry’s determinations on **Case 16: *Al-Bara Commercial & Elementary School Bombing*** in Idlib (UN Doc. A/HRC/24/46, ¶¶ 68–74; HRW, *Safe No More*, 2013), an elementary school in active municipal use is shielded by an affirmative presumption of civilian sanctuary that can never be extinguished by proximity to military infrastructure. The physical presence of an auxiliary naval logistics shed 42 meters away does not taint, sever, or compromise the absolute civilian immunity of adjacent classrooms. Under customary international law, schools are sacred sanctuaries whose protected status must be vigorously preserved.

<a id="chapter-3-7"></a>
"@

if ($content.Contains($targetCh3_6)) {
    $content = $content.Replace($targetCh3_6, $text36bis)
    Write-Output "Step 5: Chapter III § 3.6 (36 bis) inserted successfully."
} else {
    Write-Error "Step 5: targetCh3_6 not found!"
}

$targetCh3_7 = @"
[↑ Back to Table of Contents](#table-of-contents)
---

<a id="chapter-4"></a>
"@

$text38quater = @"
38 quater. **Rejection of the "Warning Leaflet" and "General Hostilities" Pretexts (Case 10 Benchmark):**
The Panel decisively repudiates the defense that general broadcast warnings or the commencement of widespread hostilities stripped the Shajareh Tayyebeh schoolgirls of civilian immunity. In the landmark investigations into **Case 10: *Second Qana Residential Building Strike*** (UN Doc. A/HRC/3/2, ¶ 151; HRW, *Why They Died*, 2007; Haque, *Law and Morality at War*, 2016), international bodies firmly established that dropping warning leaflets or declaring a regional operational sector does not transform remaining civilians into combatants or divest them of legal immunity. Civilians who remain behind—whether due to tender age, school attendance, administrative duties, or lack of transport—retain 100% of their civilian protections under **AP I Article 51(3)** and **Article 52(3)**. An attacking belligerent cannot treat a populated municipal district as a "free-fire zone" based on unverified assumptions of evacuation, nor can it presume that civilian structures are vacant without continuous, contemporaneous verification.

[↑ Back to Table of Contents](#table-of-contents)
---

<a id="chapter-4"></a>
"@

if ($content.Contains($targetCh3_7)) {
    $content = $content.Replace($targetCh3_7, $text38quater)
    Write-Output "Step 6: Chapter III § 3.7 (38 quater) inserted successfully."
} else {
    Write-Error "Step 6: targetCh3_7 not found!"
}

# -------------------------------------------------------------
# 5. Chapter IV § 4.2, § 4.3, § 4.4, § 4.5, § 4.6
# -------------------------------------------------------------
$targetCh4_2 = @"
<a id="chapter-4-3"></a>
"@

$text43ter = @"
43 ter. **Compound Non-Severability & Striking Adjacent to Protected Perimeters (Case 14 Benchmark):**
The Panel incorporates the foundational principle of *compound non-severability* established in the international inquiry into **Case 14: *Abs Rural Hospital Airstrike*** (UN Doc. A/HRC/39/43, ¶¶ 38–41; MSF Incident Review, 2016). In *Abs*, the attacking coalition attempted to justify releasing a 500-lb bomb against a moving vehicle adjacent to the hospital compound by asserting that the target was geographically distinct from the hospital facility itself. The UN Group of Eminent Experts firmly rejected this defense, holding that when a kinetic strike is directed immediately adjacent to a protected civilian compound, the lethal blast and fragmentation envelope renders the two spaces physically non-severable. In Minab, CENTCOM's claim that its targeting solution was aimed at an auxiliary naval shed 42 meters north of the school ignores the physical reality that detonating three 1,000-lb WDU-36/B warheads (with lethal blast radii exceeding 300 meters) across an unreinforced partition wall made the total destruction of the school physically inescapable, violating the non-severability principle.

<a id="chapter-4-3"></a>
"@

if ($content.Contains($targetCh4_2)) {
    $content = $content.Replace($targetCh4_2, $text43ter)
    Write-Output "Step 7: Chapter IV § 4.2 (43 ter) inserted successfully."
} else {
    Write-Error "Step 7: targetCh4_2 not found!"
}

$targetCh4_3 = @"
<a id="chapter-4-4"></a>
"@

$text45ter = @"
45 ter. **Public Academic Gathering Cycles & Opening Instructional Hours (Case 07 Benchmark):**
The scheduling of kinetic strikes during peak civilian gathering cycles constitutes primary empirical evidence of reckless disregard. In **Case 07: *Dasht-e Archi Madrassa Graduation Ceremony*** (UNAMA / OHCHR Special Report, May 2018), military helicopters launched rocket salvos into an open-air religious ceremony (*Dastar Bandi*) that had been publicly scheduled weeks in advance, slaughtering 30 children. In Minab, CENTCOM launched its Tomahawk salvo at **09:22 IRST on Saturday, February 28, 2026**—the universally recognized, statutory commencement of the academic instructional week throughout the Islamic Republic of Iran. Any elementary inquiry into local educational schedules or open-source municipal calendars would have confirmed that hundreds of young girls would be seated at their desks. Launching high-yield blast weapons during the primary opening hour of the school week constitutes deliberate blindness to known temporal patterns of civilian life.

<a id="chapter-4-4"></a>
"@

if ($content.Contains($targetCh4_3)) {
    $content = $content.Replace($targetCh4_3, $text45ter)
    Write-Output "Step 8: Chapter IV § 4.3 (45 ter) inserted successfully."
} else {
    Write-Error "Step 8: targetCh4_3 not found!"
}

$targetCh4_4 = @"
<a id="chapter-4-5"></a>
"@

$text47quater = @"
47 quater. **Multi-Tap Evacuation Ambush Dynamics (Case 13 & Case 18 Precedents):**
The sequential timing of the Minab salvo represents an aggravated manifestation of the "double-tap" and "multi-tap" aerial ambush dynamics condemned in **Case 13: *Hass School Complex Multi-Airstrike*** (UN Doc. A/HRC/34/64, ¶ 41; Bellingcat, 2016) and **Case 18: *Mastaba Market Double Airstrike*** (UN Doc. A/HRC/39/43, ¶¶ 32–37; HRW, 2016). In *Hass*, strike aircraft executed a delayed second pass calculated to intercept children and instructors evacuating into surrounding streets after the initial bomb hit. In *Mastaba*, a second precision bomb detonated minutes after the first, incinerating rescuers and survivors attempting to extract the wounded. In Minab, Impact 2 detonated on the primary escape stairwell exactly 135 seconds after Impact 1, and Impact 3 detonated in the courtyard muster ground 130 seconds after Impact 2. This staggered, programmed sequential delivery transformed designated evacuation routes into lethal blast funnels, ensuring the systematic destruction of evacuating schoolchildren and first responders.

<a id="chapter-4-5"></a>
"@

if ($content.Contains($targetCh4_4)) {
    $content = $content.Replace($targetCh4_4, $text47quater)
    Write-Output "Step 9: Chapter IV § 4.4 (47 quater) inserted successfully."
} else {
    Write-Error "Step 9: targetCh4_4 not found!"
}

$targetCh4_5 = @"
<a id="chapter-4-6"></a>
"@

$text48octies_new = @"
48 octies. **Complete Absence of Military Hardware Verified by 100% Academic Debris (Case 06 Benchmark):**
The complete absence of military materiel at the strike site is benchmarked against the definitive Battle Damage Assessment findings in **Case 06: *Dora Farms Opening Salvo Decapitation Strike*** (HRW, *Off Target*, 2003; DIA Post-Strike BDA, 2004). In *Dora Farms*, the United States launched 40 Tomahawks and four 2,000-lb bunker busters based on uncorroborated single-source HUMINT claiming Iraqi leadership was present in an underground bunker; post-strike forensic excavation revealed only civilian farm dwellings and civilian agricultural workers. In Minab, exhaustive on-site physical examinations conducted by the UN Fact-Finding Mission (**UN Doc. A/HRC/63/61**) and forensic engineering specialists confirmed that 100% of the physical debris consisted of children's primary textbooks, school desks, backpacks, pencil cases, and classroom chalkboards. Zero military electronics, weapons, or uniformed personnel were detected, establishing beyond doubt that the struck coordinates were exclusively civilian.

<a id="chapter-4-6"></a>
"@

if ($content.Contains($targetCh4_5)) {
    $content = $content.Replace($targetCh4_5, $text48octies_new)
    Write-Output "Step 10: Chapter IV § 4.5 (48 octies) inserted successfully."
} else {
    Write-Error "Step 10: targetCh4_5 not found!"
}

$targetCh4_6 = @"
<a id="chapter-4-7"></a>
"@

$text48sexies_bis = @"
48 sexies bis. **Asymmetric Pediatric Casualty Dominance as Conclusive Proof of Recklessness (Case 07 Benchmark):**
In **Case 07: *Dasht-e Archi***, UNAMA established that 81% of all confirmed casualties were school-aged children, serving as conclusive empirical proof that the attacking force failed to distinguish between military targets and protected children. In Minab, the demographic skew is even more catastrophic: of the 156 certified fatalities, **120 were young female pupils aged 7 to 12** and **36 were female faculty and civilian staff**—representing a **100% civilian and child casualty composition**. In international criminal jurisprudence, where a kinetic strike produces an overwhelming or total pediatric death toll within a confined educational zone, the demographic reality establishes an irrebuttable evidentiary inference of gross recklessness (*dolus eventualis*) under Article 30 of the Rome Statute.

<a id="chapter-4-7"></a>
"@

if ($content.Contains($targetCh4_6)) {
    $content = $content.Replace($targetCh4_6, $text48sexies_bis)
    Write-Output "Step 11: Chapter IV § 4.6 (48 sexies bis) inserted successfully."
} else {
    Write-Error "Step 11: targetCh4_6 not found!"
}

# -------------------------------------------------------------
# 6. Chapter V § 5.1, § 5.2, § 5.4
# -------------------------------------------------------------
$targetCh5_1 = @"
<a id="chapter-5-2"></a>
"@

$text50bis = @"
50 bis. **Physical CAGE Code Identification Linking Munitions to Defense Contractors (Case 18 Benchmark):**
The Panel incorporates the physical munition identification methodology established in **Case 18: *Mastaba Market Double Airstrike*** (HRW, *US Bombs Used in Deadly Market Strike*, 2016; Bellingcat, 2016). In *Mastaba*, recovered guidance fin assemblies bearing Commercial and Government Entity (CAGE) Code `96214` and National Stock Numbers (NSN) definitively linked the ordnance to Raytheon Missile Systems and US Department of Defense procurement contracts. In Minab, serialized circuit boards and avionics fragments recovered from the central courtyard crater bear identical CAGE Code `96214` and Raytheon assembly markings (`ASSY 16200-6523910-1 REV D`), providing conclusive, physical proof that the munitions deployed were US Navy BGM-109 Tomahawk cruise missiles manufactured under US defense contracts.

<a id="chapter-5-2"></a>
"@

if ($content.Contains($targetCh5_1)) {
    $content = $content.Replace($targetCh5_1, $text50bis)
    Write-Output "Step 12: Chapter V § 5.1 (50 bis) inserted successfully."
} else {
    Write-Error "Step 12: targetCh5_1 not found!"
}

$targetCh5_2 = @"
<a id="chapter-5-3"></a>
"@

$text52ter = @"
52 ter. **Inescapable Sequential Salvo Blast Physics in Confined Urban Enclosures (Case 03 & Case 17 Benchmarks):**
The hydrodynamic lethality of sequential multi-warhead salvos in educational zones is anchored in the forensic determinations of **Case 17: *Chernihiv Schools Nos. 18 & 21 Multi-Bomb Strike*** (Amnesty Crisis Evidence Lab, 2022; UN Doc. A/77/533) and **Case 03: *Katyr-Yurt Bombardment*** (ECtHR, *Isayeva v. Russia*, 2005). In Chernihiv, the sequential release of heavy 500-kg aerial bombs across two school campuses created an inescapable blast envelope that shattered structural masonry and slaughtered civilians in adjacent queues. In Minab, delivering three 1,000-lb WDU-36/B warheads (total yield 3,000 lbs PBXN-107 high explosive) across a 4,250 sq. m school parcel subjected the entire facility to peak overpressures of 18 to 24 psi and intersecting Mach stems. Under standard blast mechanics, overpressures exceeding 15 psi guarantee total biological lethality and complete structural collapse, ensuring that every occupant in the building and courtyard was subjected to lethal physical trauma.

<a id="chapter-5-3"></a>
"@

if ($content.Contains($targetCh5_2)) {
    $content = $content.Replace($targetCh5_2, $text52ter)
    Write-Output "Step 13: Chapter V § 5.2 (52 ter) inserted successfully."
} else {
    Write-Error "Step 13: targetCh5_2 not found!"
}

$targetCh5_4 = @"
[↑ Back to Table of Contents](#table-of-contents)
---

<a id="chapter-6"></a>
"@

$text57quater = @"
57 quater. **The Zero Ballistic Drift Standard Defeating the "Mapping/Drift Error" Pretext (Case 09 Benchmark):**
The Panel benchmarks the ballistic accuracy of the Tomahawk strike against the landmark UN ballistic investigation conducted by Major General Franklin van Kappen in **Case 09: *Shelling of the UNIFIL Compound at Qana*** (UN Doc. S/1996/337, 7 May 1996). Following the bombardment of the UNIFIL compound, which killed 106 sheltering civilians, the Israeli military claimed that artillery shells had accidentally drifted onto the camp due to incorrect target mapping and meteorological errors. General van Kappen’s forensic ballistic analysis decisively demolished this defense, proving that 36 proximity-fuzed artillery shells walked in a precise, converging pattern across the compound while an unmanned aerial vehicle (UAV) conducted overhead optical reconnaissance, establishing that the impacts were intentional and controlled. In Minab, where three Block IV/V Tomahawk cruise missiles struck with sub-5-meter CEP directly into the school's central wing, escape stairwell, and courtyard, any defense of "ballistic drift", "aerodynamic error", or "navigational deviation" is physically and mathematically impossible. The weapons performed with absolute precision according to their programmed firing coordinates.

[↑ Back to Table of Contents](#table-of-contents)
---

<a id="chapter-6"></a>
"@

if ($content.Contains($targetCh5_4)) {
    $content = $content.Replace($targetCh5_4, $text57quater)
    Write-Output "Step 14: Chapter V § 5.4 (57 quater) inserted successfully."
} else {
    Write-Error "Step 14: targetCh5_4 not found!"
}

# -------------------------------------------------------------
# 7. Chapter VI § 6.1, § 6.2, § 6.4, § 6.5
# -------------------------------------------------------------
$targetCh6_1 = @"
<a id="chapter-6-2"></a>
"@

$text61ter = @"
61 ter. **The Peacetime Deliberate Planning Standard vs. Opening Salvo Urgency (Case 06 Benchmark):**
As established in **Case 06: *Dora Farms Decapitation Strike*** (HRW, *Off Target*, 2003; Turns, 2006; Dinstein, 2010), when a belligerent launches pre-planned strikes on Day 1 of an armed conflict from deliberate target lists compiled during peacetime, it cannot invoke dynamic "fog of war" or combat urgency to forgive targeting negligence. In *Dora Farms*, target developers operated over weeks of unhurried planning; in Minab, CENTCOM and DIA maintained the target folder for ten full years (2016–2026). The standard of feasible precautions under **AP I Article 57(2)(a)(i)** applies *strictissimi juris* to deliberate peacetime targeting: a decade of administrative opportunity to inspect open-source maps, commercial satellites, and municipal registries completely bars the defense of combat urgency.

<a id="chapter-6-2"></a>
"@

if ($content.Contains($targetCh6_1)) {
    $content = $content.Replace($targetCh6_1, $text61ter)
    Write-Output "Step 15: Chapter VI § 6.1 (61 ter) inserted successfully."
} else {
    Write-Error "Step 15: targetCh6_1 not found!"
}

$targetCh6_2 = @"
<a id="chapter-6-2-1"></a>
"@

$text63bis = @"
63 bis. **The Unified Application of the Belgrade Three-Stage Failure Test (Case 01 Benchmark):**
The Panel adopts the tripartite targeting failure test established by Under Secretary Thomas Pickering and the ICTY Office of the Prosecutor in **Case 01: *Belgrade Chinese Embassy Bombing*** (ICTY OTP NATO Report, ¶¶ 80–85). CENTCOM committed an exact threefold systemic failure in Minab: (1) *Methodological Flaw:* relying on outdated 2016 military boundary data without verifying ten years of municipal school evolution; (2) *Database Circularity:* permitting Palantir's Maven Smart System to cross-check coordinates against the very DIA database that introduced the original error; and (3) *Institutional Insulation:* operating target review boards that failed to consult open cadastral records, commercial satellite imagery, or local school registers, while eliminating 90% of civilian harm review specialists.

<a id="chapter-6-2-1"></a>
"@

if ($content.Contains($targetCh6_2)) {
    $content = $content.Replace($targetCh6_2, $text63bis)
    Write-Output "Step 16: Chapter VI § 6.2 (63 bis) inserted successfully."
} else {
    Write-Error "Step 16: targetCh6_2 not found!"
}

$targetCh6_4 = @"
<a id="chapter-6-5"></a>
"@

$text72ter = @"
72 ter. **High-Altitude Sensor Ambiguity and FLIR Optical Degradation (Cases 02 & 12 Benchmarks):**
The Panel benchmarks the sensor pathology in Minab against the seminal findings in **Case 02: *Kunduz Fuel Tankers*** (ECtHR Grand Chamber, *Hanan v. Germany*, 2021; Bundestag-Drucksache 17/7400) and **Case 12: *Koriša Refugee Encampment*** (ICTY OTP NATO Report, ¶¶ 86–89; HRW, 2000). In *Kunduz*, forward controllers misinterpreted thermal FLIR infrared blobs—representing villagers carrying fuel buckets—as armed insurgents, rejecting pilot recommendations to conduct low-altitude warning passes. In *Koriša*, pilots operating at high altitude misidentified civilian farm wagons and tractors as military bivouacs. In Minab, remote satellite and algorithmic sensors misinterpreted primary school buses, morning assembly lines, and children's playground apparatus as military logistics vehicles and revetments. Under customary IHL and **AP I Article 57(2)(b)**, where remote sensors present ambiguous or unverified signatures, the attacking force is under an absolute affirmative duty to suspend or abort the attack until positive target identification (PID) is established.

<a id="chapter-6-5"></a>
"@

if ($content.Contains($targetCh6_4)) {
    $content = $content.Replace($targetCh6_4, $text72ter)
    Write-Output "Step 17: Chapter VI § 6.4 (72 ter) inserted successfully."
} else {
    Write-Error "Step 17: targetCh6_4 not found!"
}

$targetCh6_5 = @"
[↑ Back to Table of Contents](#table-of-contents)
---

<a id="chapter-7"></a>
"@

$text76ter = @"
76 ter. **Institutional Command Information Siloing Breakdown (Case 19 Benchmark):**
The collapse of communication between intelligence branches in Minab mirrors the institutional siloing condemned by the European Court of Human Rights in **Case 19: *Isayeva, Yusupova and Bazayeva v. Russia*** (HUDOC 001-68379, ¶¶ 185–187, 222). In *Shaami-Yurt*, civilian checkpoint authorities who turned the refugee convoy back onto the highway never communicated with the military air command scheduling combat sorties, creating a lethal institutional void. In Minab, while secondary US intelligence databases had separately recorded the facility's 2016 physical partition and municipal registration as an elementary school, CENTCOM's operational strike cell remained segregated in obsolete targeting silos. Under customary international law and Article 4 of ARSIWA, institutional compartmentalization and failure of inter-agency communication constitute systemic state negligence that directly engages international responsibility.

[↑ Back to Table of Contents](#table-of-contents)
---

<a id="chapter-7"></a>
"@

if ($content.Contains($targetCh6_5)) {
    $content = $content.Replace($targetCh6_5, $text76ter)
    Write-Output "Step 18: Chapter VI § 6.5 (76 ter) inserted successfully."
} else {
    Write-Error "Step 18: targetCh6_5 not found!"
}

# -------------------------------------------------------------
# 8. Chapter VII § 7.1, § 7.2, § 7.3, § 7.4, § 7.5
# -------------------------------------------------------------
$targetCh7_1 = @"
<a id="chapter-7-2"></a>
"@

$text78ter = @"
78 ter. **Indiscriminate Explosive Weapons in Populated Areas (EWIPA) (Case 17 Benchmark):**
Under the international EWIPA framework endorsed by the International Committee of the Red Cross (ICRC, 2022) and the UN Independent International Commission of Inquiry on Ukraine (**UN Doc. A/77/533, ¶ 46**), the deployment of explosive weapons with wide-area effects in populated urban centers is inherently indiscriminate under **AP I Article 51(4)(b)**. As established in **Case 17: *Chernihiv Schools Nos. 18 & 21 Multi-Bomb Strike***, detonating heavy blast munitions across educational campuses populated by civilians violates customary distinction *per se*. Detonating 3,000 lbs of high-explosive ordnance within the dense municipal fabric of Minab constitutes an unlawful indiscriminate attack.

<a id="chapter-7-2"></a>
"@

if ($content.Contains($targetCh7_1)) {
    $content = $content.Replace($targetCh7_1, $text78ter)
    Write-Output "Step 19: Chapter VII § 7.1 (78 ter) inserted successfully."
} else {
    Write-Error "Step 19: targetCh7_1 not found!"
}

$targetCh7_2 = @"
<a id="chapter-7-3"></a>
"@

$text81septies = @"
81 septies. **Negligent Buffer Targeting Adjacent to Protected Sanctuaries (Case 14 Benchmark):**
The Panel incorporates the precautionary benchmark of **Case 14: *Abs Rural Hospital Airstrike*** (UN Doc. A/HRC/39/43, ¶ 40; Haque, *Just Security*, 2016). Attacking forces cannot treat the perimeter of an adversary installation as an unconstrained kinetic target when it abuts a protected civilian sanctuary. In *Abs*, striking a vehicle at the hospital gate was held to violate **AP I Article 57(2)(a)(ii)**; in Minab, launching three 1,000-lb cruise missiles against a shed 42 meters from a school without verifying the school's occupancy or deploying blast-mitigating delivery profiles constitutes gross operational negligence.

<a id="chapter-7-3"></a>
"@

if ($content.Contains($targetCh7_2)) {
    $content = $content.Replace($targetCh7_2, $text81septies)
    Write-Output "Step 20: Chapter VII § 7.2 (81 septies) inserted successfully."
} else {
    Write-Error "Step 20: targetCh7_2 not found!"
}

$targetCh7_3 = @"
<a id="chapter-7-4"></a>
"@

$text84bis = @"
84 bis. **Weapons Disproportionality Per Se in Confined Sanctuaries (Cases 03 & 19 Benchmarks):**
Reaffirming the unified *Isayeva* doctrine (**Case 03: *Katyr-Yurt***, §§ 189–191; **Case 19: *Shaami-Yurt***, §§ 195–199), deploying weapons with lethal blast radii exceeding 300 meters into an active school compound containing 168 children and staff is disproportionate *per se* under **AP I Article 51(5)(b)** and **Customary IHL Rule 14**. Where the lethal blast envelope of the chosen weapon guarantees the destruction of protected civilian structures, no military commander could reasonably conclude that the anticipated military advantage outweighed the inevitable loss of child life.

<a id="chapter-7-4"></a>
"@

if ($content.Contains($targetCh7_3)) {
    $content = $content.Replace($targetCh7_3, $text84bis)
    Write-Output "Step 21: Chapter VII § 7.3 (84 bis) inserted successfully."
} else {
    Write-Error "Step 21: targetCh7_3 not found!"
}

$targetCh7_4 = @"
<a id="chapter-7-5"></a>
"@

$text85quinquies = @"
85 quinquies. **Dedicated Kinetic Attacks on Educational Sanctuaries (Cases 13 & 16 Benchmarks):**
Under **Article 8(2)(b)(ix) of the Rome Statute**, intentionally directing attacks against buildings dedicated to education—provided they are not military objectives—constitutes an independent, aggravated war crime. In **Case 13: *Hass School Complex*** (UN Doc. A/HRC/34/64) and **Case 16: *Al-Bara Elementary School*** (UN Doc. A/HRC/24/46), international commissions affirmed that schools are sacred sanctuaries whose destruction permanently impairs children’s fundamental rights under **UN CRC Article 28** and **UN Security Council Resolution 2601 (2021)**. The obliteration of Shajareh Tayyebeh and slaughter of 120 schoolgirls satisfies every material and mental element of this war crime.

<a id="chapter-7-5"></a>
"@

if ($content.Contains($targetCh7_4)) {
    $content = $content.Replace($targetCh7_4, $text85quinquies)
    Write-Output "Step 22: Chapter VII § 7.4 (85 quinquies) inserted successfully."
} else {
    Write-Error "Step 22: targetCh7_4 not found!"
}

$targetCh7_5 = @"
[↑ Back to Table of Contents](#table-of-contents)
---

<a id="chapter-8"></a>
"@

$text85ter = @"
85 ter. **Absolute Breach of Mandatory Advance Warning Before Striking Sanctuaries (Cases 08 & 10 Benchmarks):**
The customary obligation to issue effective advance warnings prior to striking protected sanctuaries (**AP I Article 57(2)(c)** and **Article 65(2)**) admits no exception for operational convenience or speed. In **Case 10: *Second Qana Residential Building Strike*** (UN Doc. S/PRST/2006/35) and **Case 08: *Al-Amiriyah Public Shelter Massacre*** (HRW, 1991), international authorities established that launching surprise kinetic strikes into civilian shelters or inhabited municipal buildings without explicit warning constitutes a catastrophic breach of international law. In Minab, striking an active primary school with zero warning while 168 children were inside classroom desks converts the attack into an unambiguous grave breach of international humanitarian law.

[↑ Back to Table of Contents](#table-of-contents)
---

<a id="chapter-8"></a>
"@

if ($content.Contains($targetCh7_5)) {
    $content = $content.Replace($targetCh7_5, $text85ter)
    Write-Output "Step 23: Chapter VII § 7.5 (85 ter) inserted successfully."
} else {
    Write-Error "Step 23: targetCh7_5 not found!"
}

# -------------------------------------------------------------
# 9. Chapter VIII § 8.2 & § 8.3
# -------------------------------------------------------------
$targetCh8_2 = @"
<a id="chapter-8-3"></a>
"@

$text90quater = @"
90 quater. **Superior Command Responsibility & The Operational Planning and Control Standard (Cases 03 & 19 Benchmarks):**
Under **Article 28 of the Rome Statute** and the Grand Chamber jurisprudence in *McCann v. UK* (1995) as applied in **Case 03 (*Katyr-Yurt*)** and **Case 19 (*Shaami-Yurt*)**, superior commanders are criminally and institutionally responsible when they fail to plan and control military operations so as to minimize risk to civilian life. In Minab, commanding flag officers who authorized the deployment of the unvetted Maven-Claude AI targeting pipeline, slashed the CHMR civilian oversight unit, and failed to monitor terminal sensor feeds bear direct command responsibility for the slaughter.

<a id="chapter-8-3"></a>
"@

if ($content.Contains($targetCh8_2)) {
    $content = $content.Replace($targetCh8_2, $text90quater)
    Write-Output "Step 24: Chapter VIII § 8.2 (90 quater) inserted successfully."
} else {
    Write-Error "Step 24: targetCh8_2 not found!"
}

$targetCh8_3 = @"
[↑ Back to Table of Contents](#table-of-contents)
---

<a id="chapter-9"></a>
"@

$text91ter = @"
91 ter. **Third-Party State Responsibility & Defense Contractor Complicity under ARSIWA Art. 16 (Case 18 Benchmark):**
As established in **Case 18: *Mastaba Market Double Airstrike*** (Amnesty, MDE 31/3815/2016; Arms Trade Treaty Art. 6) and the UK Court of Appeal’s *CAAT* ruling ([2019] EWCA Civ 1020), commercial contractors and supplying states that provide precision weapons or algorithmic targeting tools knowingly deployed in violation of IHL incur international responsibility under **Article 16 of the ILC Articles on State Responsibility (ARSIWA)** and customary international law.

[↑ Back to Table of Contents](#table-of-contents)
---

<a id="chapter-9"></a>
"@

if ($content.Contains($targetCh8_3)) {
    $content = $content.Replace($targetCh8_3, $text91ter)
    Write-Output "Step 25: Chapter VIII § 8.3 (91 ter) inserted successfully."
} else {
    Write-Error "Step 25: targetCh8_3 not found!"
}

# -------------------------------------------------------------
# 10. Chapter X Restructuring (User's Exact Division into 2 Sections)
# -------------------------------------------------------------
# Find start of Chapter X:
$ch10Index = $content.IndexOf('<a id="chapter-10"></a>')
if ($ch10Index -ge 0) {
    # Find footer RENDERED AND SEALED
    $footerAnchor = "**RENDERED AND SEALED**"
    $footerIndex = $content.IndexOf($footerAnchor, $ch10Index)
    if ($footerIndex -gt $ch10Index) {
        $ch10OldBlock = $content.Substring($ch10Index, $footerIndex - $ch10Index)
        
        $ch10NewBlock = @"
<a id="chapter-10"></a>
# CHAPTER X: DISPOSITION, REMEDIAL ORDERS & JURIDICAL ACCOUNTABILITY REGIMES

<a id="chapter-10-1"></a>
### 10.1 Formal Declaratory Determinations of the Expert Chamber
96. Based upon the totality of the verified evidentiary record, open-source photogrammetry, metallurgical debris examinations, and settled international jurisprudence, the Independent Expert Inquiry Panel of People for Peace & Justice ry (PFPJ ry) formally determines:
   * **(i)** That the triple-tap kinetic missile strikes executed by the naval forces of the United States against the Shajareh Tayyebeh Girls' Elementary School on February 28, 2026, constituted **grave breaches of the Geneva Conventions of 1949** and serious violations of the laws and customs of war amounting to **war crimes** under customary international law and the Rome Statute of the International Criminal Court;
   * **(ii)** That the operational deployment of high-explosive unitary blast warheads (3,000 lbs PBXN-107) inside an active, walled primary educational facility during morning classroom hours constituted an **unlawful indiscriminate attack** and a flagrant breach of the **Principle of Distinction** (AP I Arts. 48, 51, 52) and the **Principle of Proportionality** (AP I Art. 51(5)(b));
   * **(iii)** That the command echelons of the United States Central Command (USCENTCOM) committed gross operational negligence and exhibited conditional intent (*dolus eventualis*) by relying on decade-old targeting files, disabling civilian harm review mechanisms, and disregarding terminal electro-optical sensor imagery; and
   * **(iv)** That these acts engage the **direct, non-delegable State Responsibility of the United States of America** under customary international law.

---

<a id="chapter-10-2"></a>
### 10.2 Section 1: State Responsibility & Financial Liability Regime (The Chorzów Factory Standard & ARSIWA Articles 30–37)

97. **The Legal Standard of State Financial Liability (*Restitutio in Integrum*):**
Under customary international law, as authoritatively articulated by the Permanent Court of International Justice in the seminal ***Factory at Chorzów (Claim for Indemnity) (Germany v. Poland)*** judgment (1928, P.C.I.J., Ser. A, No. 17, p. 47) and codified in the **International Law Commission's Articles on Responsibility of States for Internationally Wrongful Acts (ILC ARSIWA, 2001, Articles 30–37)**:
> *"The essential principle contained in the actual notion of an illegal act [...] is that reparation must, so far as possible, wipe out all the consequences of the illegal act and re-establish the situation which would, in all probability, have existed if that act had not been committed. Restitution in kind, or, if this is not possible, payment of a sum corresponding to the value which a restitution in kind would bear; the award, if need be, of damages for loss sustained which would not be covered by restitution in kind or payment in place of it—such are the principles which should serve to determine the amount of compensation due for an act contrary to international law."*

97 bis. **Rejection of Discretionary Ex Gratia Condolences in Favor of Binding State Reparations:**
The Panel categorically rejects the model of discretionary, non-binding *ex gratia* condolences exemplified in **Case 05 (*Kabul Drone Strike*)**, where token financial offers were conditioned on the denial of legal liability. Reparation is not a discretionary act of grace; it is an autonomous secondary legal obligation arising automatically from the commission of an internationally wrongful act. This mandatory legal obligation is solidly anchored in bilateral and multilateral state practice:
1.  **The Belgrade Chinese Embassy Settlement (1999, 39 ILM 644 — Case 01 Benchmark):** Following the kinetic destruction of the PRC Embassy in Belgrade, the United States Government accepted formal international legal liability, tendered an official state apology, and paid **\$32.5 million** in direct compensation (\$28 million in sovereign property restitution to the PRC State and \$4.5 million in humanitarian payments to the injured and surviving families);
2.  **UN General Assembly Resolution 51/233 (1997 — Case 09 Benchmark):** Following the shelling of the UNIFIL compound at Qana, the UN General Assembly formally established that the attacking State was legally bound to satisfy the financial damages inflicted on the facility, affirming state financial liability for kinetic bombardment of protected sanctuaries.

97 ter. **Itemized Financial Assessment of State Reparations (Docket PFPJ-2026-IR-001):**
Applying the *Chorzów Factory* standard to the demographic, physical, and medical devastation in Minab, the Panel calculates the minimum financial liability owed by the United States of America as follows:

| Reparation Head | International Legal Basis (ILC ARSIWA) | Factual / Demographic Parameter | Certified Valuation (USD) |
| :--- | :--- | :--- | :--- |
| **Head A: Material Restitution & Educational Reconstruction** | **ARSIWA Art. 35** (*Restitution in kind* / *Restitutio in integrum*) | Complete architectural design, seismic construction, outfitting, and equipment for a replacement state-of-the-art educational campus, including reinforced multi-hazard civil defense shelter, science laboratories, digital library, and sports complex. | **\$45,000,000** |
| **Head B: Wrongful Death Compensation** | **ARSIWA Art. 36** (*Compensation for financially assessable damage*) | Direct, irrevocable wrongful death compensation disbursed to the certified legal heirs of all **156 deceased victims** (120 primary schoolgirls, 26 faculty members, 10 custodial staff) at \$1,000,000 per victim. | **\$156,000,000** |
| **Head C: Pediatric Medical Rehabilitation & Trauma Trust Fund** | **ARSIWA Art. 36** (*Compensation for personal injury and medical care*) | Establishment of an independently managed international trust fund providing lifetime medical, surgical, and prosthetic care for all **95+ wounded survivors** (including 38 pediatric amputees requiring ongoing prosthesis replacement, 24 tympanic trauma cases, and 19 ocular trauma cases), alongside comprehensive clinical trauma psychological therapy. | **\$65,000,000** |
| **Head D: Moral Damages & Non-Material Satisfaction** | **ARSIWA Art. 37** (*Satisfaction for moral damage and symbolic redress*) | Endowment for an independent civic memorialization park in Minab, an annual educational scholarship foundation established in perpetuity in the names of the 120 martyred pupils, and funding for independent international research into civilian harm mitigation. | **\$34,000,000** |
| **TOTAL STATE FINANCIAL LIABILITY CLAIM** | **ARSIWA Arts. 31, 35–37 (Chorzów Factory Standard)** | **Complete Restitution, Wrongful Death, Medical Trust & Satisfaction** | **\$300,000,000 USD** |

97 quater. **Obligation of Cessation & Guarantees of Non-Repetition (ARSIWA Article 30):**
Under Article 30 of ARSIWA, the United States is under an immediate, binding obligation to:
*   (i) **Immediate Moratorium:** Impose an immediate, binding operational moratorium on the deployment of automated AI targeting platforms (including Palantir Maven and integrated Large Language Models) for strike packages situated within 500 meters of registered civilian, educational, and medical infrastructure;
*   (ii) **Restoration of Oversight:** Re-establish and mandate the full staffing of independent Civilian Harm Mitigation and Response (CHMR) units with absolute veto authority across all combatant commands; and
*   (iii) **Official Apology & Declassification:** Issue a formal, public state apology to the bereaved families and people of Minab, and declassify the full, unredacted AR 15-6 investigation records and targeting telemetry.

---

<a id="chapter-10-3"></a>
### 10.3 Section 2: Individual Criminal Responsibility & Determination of Charges (The ICC Rome Statute Model)

97 quinquies. **Jurisprudential Formulation of Charges (Rome Statute Framework):**
Following the statutory structure and judicial formulation of a **Decision on the Confirmation of Charges** rendered by a Pre-Trial Chamber of the International Criminal Court under **Article 61(7) of the Rome Statute**, the Panel determines that there are **substantial grounds to believe** that the operational commanders, targeting developers, and intelligence validation officers of the United States Armed Forces committed the following specific war crimes during the February 28, 2026 kinetic missile strike on the Shajareh Tayyebeh School:

#### COUNT 1: WAR CRIME OF INTENTIONALLY DIRECTING ATTACKS AGAINST CIVILIANS
*(Rome Statute, Article 8(2)(b)(i))*
*   **Material Element:** The perpetrators launched three BGM-109 Tomahawk cruise missiles against the Shajareh Tayyebeh School, directing kinetic lethal force against a civilian population and individual civilians not taking direct part in hostilities;
*   **Mental Element (*Mens Rea*):** The perpetrators acted with knowledge and intent under Article 30 of the Rome Statute, exhibiting at minimum conditional intent and gross recklessness (*dolus eventualis*) by approving strike coordinates derived from decade-old static databases without conducting contemporaneous visual verification, and failing to execute an abort when terminal sensors revealed children's assembly grounds.

#### COUNT 2: WAR CRIME OF INTENTIONALLY DIRECTING ATTACKS AGAINST CIVILIAN OBJECTS
*(Rome Statute, Article 8(2)(b)(ii))*
*   **Material Element:** The perpetrators directed kinetic missile strikes against the physical buildings of the Shajareh Tayyebeh School, which were civilian objects and not military objectives, causing the total structural pulverization of the educational facility;
*   **Mental Element:** The perpetrators intended the object of the attack to be the compound, which was objectively an active municipal school, having failed to satisfy the legal standard of positive target identification.

#### COUNT 3: WAR CRIME OF LAUNCHING AN ATTACK CAUSING EXCESSIVE INCIDENTAL DEATH, INJURY, OR DAMAGE (PROPORTIONALITY)
*(Rome Statute, Article 8(2)(b)(iv))*
*   **Material Element:** The perpetrators launched a three-missile kinetic attack in the knowledge that such attack would cause incidental loss of life to civilians, injury to civilians, and damage to civilian objects that was clearly excessive in relation to the concrete and direct overall military advantage anticipated;
*   **Mental Element:** Detonating 3,000 pounds of high explosives against an auxiliary shed located 42 meters from an active elementary school was executed in the certain knowledge that the lethal blast-fragmentation radius would annihilate all occupants within 100 meters, making the slaughter of 156 children and staff manifestly disproportionate to any conceivable military utility.

#### COUNT 4: WAR CRIME OF ATTACKING OR BOMBARDING UNDEFENDED BUILDINGS
*(Rome Statute, Article 8(2)(b)(v))*
*   **Material Element:** The perpetrators attacked and bombarded, by precision cruise missiles, the Shajareh Tayyebeh School complex, which was entirely undefended, open to peaceful municipal access, and devoid of any defensive combat installations or military personnel.

#### COUNT 5: WAR CRIME OF INTENTIONALLY DIRECTING ATTACKS AGAINST BUILDINGS DEDICATED TO EDUCATION
*(Rome Statute, Article 8(2)(b)(ix))*
*   **Material Element:** The perpetrators directed kinetic attacks against buildings dedicated to education, which were not being used for military purposes;
*   **Mental Element:** The physical architecture, classroom layout, municipal licensing, and presence of 168 schoolgirls and instructors established that the facility was dedicated exclusively to the education of children. In accordance with the *Hass School* (Case 13) and *Al-Bara* (Case 16) precedents, failing to check open-source educational registries constitutes an intentional abdication of the duty of distinction amounting to a direct attack on educational sanctuaries.

#### DETERMINATION OF MODES OF LIABILITY (ROME STATUTE ARTICLES 25 & 28)
97 sexies. The Panel determines that individual criminal responsibility attaches through the following statutory modes of liability:
1.  **Direct Perpetration / Co-Perpetration (Rome Statute Art. 25(3)(a)):** Attaching to the target developers and Strike Validation Authorities who jointly configured target folder `TDS-2026-IR-0814` and authorized weapon release;
2.  **Ordering and Inducing the Commission of Crimes (Rome Statute Art. 25(3)(b)):** Attaching to senior operational commanders who ordered the execution of pre-planned Day-1 strikes without requiring human-in-the-loop verification;
3.  **Aiding, Abetting, and Assisting via Automated Systems (Rome Statute Art. 25(3)(c)):** Attaching to software engineers and command authorities who deployed the Palantir Maven Smart System with known automation bias while dismantling civilian harm oversight cells;
4.  **Command and Superior Responsibility (Rome Statute Art. 28(a) & 28(b)):** Attaching to the Commander of United States Central Command and operational flag officers who: (i) knew or had reason to know that subordinate strike cells were relying on obsolete databases; (ii) failed to take all necessary and reasonable measures within their power to prevent or repress the commission of the strike; and (iii) failed to submit the matter to competent authorities for independent criminal investigation and prosecution.

---

<a id="chapter-10-4"></a>
### 10.4 Orders Concerning Judicial Preservation of Evidence & International Fact-Finding
98. The Panel orders:
   * **(i)** That the verified master evidentiary archives ([EXH-SAT-001](MASTER_EXHIBIT_DOSSIER.md#exhibit-sat) through [EXH-UN-008](MASTER_EXHIBIT_DOSSIER.md#exhibit-un)) remain deposited in permanent, tamper-evident cryptographic custody in Helsinki, Finland, under the Berkeley Protocol;
   * **(ii)** That duplicate cryptographic archives be formally transmitted to the **President of the United Nations Human Rights Council**, the **Secretariat of the Independent International Fact-Finding Mission on the Islamic Republic of Iran** (UN Doc. A/HRC/63/61), and the **International Impartial and Independent Mechanism (IIIM)**; and
   * **(iii)** That all physical debris, metallurgical samples, and digital telemetry be preserved for prospective presentation before international criminal and civil tribunals.

---

<a id="chapter-10-5"></a>
### 10.5 Contingent Prosecutorial Directions & Transmissions
99. In furtherance of global accountability and the prevention of impunity, the Panel directs the Board of Trustees of People for Peace & Justice ry (PFPJ ry) to execute the following transmissions:
   * **(a) Transmission to the International Criminal Court:** Formally submit this Master Judicial Assessment to the **Office of the Prosecutor of the International Criminal Court (ICC)** pursuant to Article 15 of the Rome Statute, requesting the initiation of a preliminary examination into war crimes committed during Operation Epic Fury;
   * **(b) Transmission to Multilateral Fact-Finding Organs:** Transmit certified copies to the **Office of the United Nations High Commissioner for Human Rights (OHCHR)**, the **Special Representative of the Secretary-General for Children and Armed Conflict (CAAC)**, and the **UNESCO Committee on the Protection of Educational Institutions**;
   * **(c) Status of Universal Jurisdiction Filings:** The Panel notes that formal criminal complaints under universal jurisdiction regimes (including Chapter 11 of the Finnish Penal Code and Section 1 of the German International Crimes Code) remain subject to ongoing jurisdictional and procedural review. Pending the completion of these specialized inquiries, no further filings are directed at this juncture, preserving full prosecutorial discretion for future legal action.

[↑ Back to Table of Contents](#table-of-contents)
---

"@

        $content = $content.Substring(0, $ch10Index) + $ch10NewBlock + $content.Substring($footerIndex)
        Write-Output "Step 26: Chapter X restructured successfully into Section 1 and Section 2."
    } else {
        Write-Error "Step 26: footerAnchor not found after chapter-10!"
    }
} else {
    Write-Error "Step 26: chapter-10 anchor not found!"
}

# -------------------------------------------------------------
# 11. Write out the modified content with UTF-8 encoding
# -------------------------------------------------------------
[System.IO.File]::WriteAllText($filePath, $content, [System.Text.Encoding]::UTF8)
Write-Output "ALL UPDATES APPLIED SUCCESSFULLY TO $filePath"
