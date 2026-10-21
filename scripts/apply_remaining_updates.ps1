# Script to apply remaining updates
$filePath = 'E:\Papers\PFPJ\Campaigns\minab\justiceForMinab\docs\FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.md'
$lines = [System.Collections.Generic.List[string]](Get-Content -Path $filePath -Encoding UTF8)

# 1. Update Table of Contents (around lines 81-85)
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -like '*[CHAPTER X: DISPOSITION, REMEDIAL ORDERS*') {
        $lines[$i] = '* [CHAPTER X: DISPOSITION, REMEDIAL ORDERS & JURIDICAL ACCOUNTABILITY REGIMES](#chapter-10)'
        $lines[$i+1] = '  * [10.1 Formal Declaratory Determinations of the Expert Chamber](#chapter-10-1)'
        $lines[$i+2] = '  * [10.2 Section 1: State Responsibility & Financial Liability Regime (The Chorzow Factory Standard & ARSIWA Articles 30-37)](#chapter-10-2)'
        $lines[$i+3] = '  * [10.3 Section 2: Individual Criminal Responsibility & Confirmation of Charges (The ICC Rome Statute Model)](#chapter-10-3)'
        $lines[$i+4] = '  * [10.4 Orders Concerning Judicial Preservation of Evidence & International Fact-Finding](#chapter-10-4)'
        $lines.Insert($i+5, '  * [10.5 Contingent Prosecutorial Directions & Transmissions](#chapter-10-5)')
        Write-Output "Step 0: TOC updated at index $i"
        break
    }
}

# 2. Insert 8 nonies before <a id="chapter-2"></a>
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
"@

for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '^<a id="chapter-2"></a>') {
        $targetIdx = $i - 3
        $lines.Insert($targetIdx, $text8nonies)
        $lines.Insert($targetIdx + 1, "")
        Write-Output "Step 1: 8 nonies inserted before chapter-2 at index $targetIdx"
        break
    }
}

# 3. Insert 38 quater before <a id="chapter-4"></a>
$text38quater = @"
38 quater. **Rejection of the "Warning Leaflet" and "General Hostilities" Pretexts (Case 10 Benchmark):**
The Panel decisively repudiates the defense that general broadcast warnings or the commencement of widespread hostilities stripped the Shajareh Tayyebeh schoolgirls of civilian immunity. In the landmark investigations into **Case 10: *Second Qana Residential Building Strike*** (UN Doc. A/HRC/3/2, ¶ 151; HRW, *Why They Died*, 2007; Haque, *Law and Morality at War*, 2016), international bodies firmly established that dropping warning leaflets or declaring a regional operational sector does not transform remaining civilians into combatants or divest them of legal immunity. Civilians who remain behind—whether due to tender age, school attendance, administrative duties, or lack of transport—retain 100% of their civilian protections under **AP I Article 51(3)** and **Article 52(3)**. An attacking belligerent cannot treat a populated municipal district as a "free-fire zone" based on unverified assumptions of evacuation, nor can it presume that civilian structures are vacant without continuous, contemporaneous verification.
"@

for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '^<a id="chapter-4"></a>') {
        $targetIdx = $i - 3
        $lines.Insert($targetIdx, $text38quater)
        $lines.Insert($targetIdx + 1, "")
        Write-Output "Step 6: 38 quater inserted before chapter-4 at index $targetIdx"
        break
    }
}

# 4. Insert 57 quater before <a id="chapter-6"></a>
$text57quater = @"
57 quater. **The Zero Ballistic Drift Standard Defeating the "Mapping/Drift Error" Pretext (Case 09 Benchmark):**
The Panel benchmarks the ballistic accuracy of the Tomahawk strike against the landmark UN ballistic investigation conducted by Major General Franklin van Kappen in **Case 09: *Shelling of the UNIFIL Compound at Qana*** (UN Doc. S/1996/337, 7 May 1996). Following the bombardment of the UNIFIL compound, which killed 106 sheltering civilians, the Israeli military claimed that artillery shells had accidentally drifted onto the camp due to incorrect target mapping and meteorological errors. General van Kappen’s forensic ballistic analysis decisively demolished this defense, proving that 36 proximity-fuzed artillery shells walked in a precise, converging pattern across the compound while an unmanned aerial vehicle (UAV) conducted overhead optical reconnaissance, establishing that the impacts were intentional and controlled. In Minab, where three Block IV/V Tomahawk cruise missiles struck with sub-5-meter CEP directly into the school's central wing, escape stairwell, and courtyard, any defense of "ballistic drift", "aerodynamic error", or "navigational deviation" is physically and mathematically impossible. The weapons performed with absolute precision according to their programmed firing coordinates.
"@

for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '^<a id="chapter-6"></a>') {
        $targetIdx = $i - 3
        $lines.Insert($targetIdx, $text57quater)
        $lines.Insert($targetIdx + 1, "")
        Write-Output "Step 14: 57 quater inserted before chapter-6 at index $targetIdx"
        break
    }
}

# 5. Insert 76 ter before <a id="chapter-7"></a>
$text76ter = @"
76 ter. **Institutional Command Information Siloing Breakdown (Case 19 Benchmark):**
The collapse of communication between intelligence branches in Minab mirrors the institutional siloing condemned by the European Court of Human Rights in **Case 19: *Isayeva, Yusupova and Bazayeva v. Russia*** (HUDOC 001-68379, ¶¶ 185–187, 222). In *Shaami-Yurt*, civilian checkpoint authorities who turned the refugee convoy back onto the highway never communicated with the military air command scheduling combat sorties, creating a lethal institutional void. In Minab, while secondary US intelligence databases had separately recorded the facility's 2016 physical partition and municipal registration as an elementary school, CENTCOM's operational strike cell remained segregated in obsolete targeting silos. Under customary international law and Article 4 of ARSIWA, institutional compartmentalization and failure of inter-agency communication constitute systemic state negligence that directly engages international responsibility.
"@

for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '^<a id="chapter-7"></a>') {
        $targetIdx = $i - 3
        $lines.Insert($targetIdx, $text76ter)
        $lines.Insert($targetIdx + 1, "")
        Write-Output "Step 18: 76 ter inserted before chapter-7 at index $targetIdx"
        break
    }
}

# 6. Insert 85 ter before <a id="chapter-8"></a>
$text85ter = @"
85 ter. **Absolute Breach of Mandatory Advance Warning Before Striking Sanctuaries (Cases 08 & 10 Benchmarks):**
The customary obligation to issue effective advance warnings prior to striking protected sanctuaries (**AP I Article 57(2)(c)** and **Article 65(2)**) admits no exception for operational convenience or speed. In **Case 10: *Second Qana Residential Building Strike*** (UN Doc. S/PRST/2006/35) and **Case 08: *Al-Amiriyah Public Shelter Massacre*** (HRW, 1991), international authorities established that launching surprise kinetic strikes into civilian shelters or inhabited municipal buildings without explicit warning constitutes a catastrophic breach of international law. In Minab, striking an active primary school with zero warning while 168 children were inside classroom desks converts the attack into an unambiguous grave breach of international humanitarian law.
"@

for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '^<a id="chapter-8"></a>') {
        $targetIdx = $i - 3
        $lines.Insert($targetIdx, $text85ter)
        $lines.Insert($targetIdx + 1, "")
        Write-Output "Step 23: 85 ter inserted before chapter-8 at index $targetIdx"
        break
    }
}

# 7. Insert 91 ter before <a id="chapter-9"></a>
$text91ter = @"
91 ter. **Third-Party State Responsibility & Defense Contractor Complicity under ARSIWA Art. 16 (Case 18 Benchmark):**
As established in **Case 18: *Mastaba Market Double Airstrike*** (Amnesty, MDE 31/3815/2016; Arms Trade Treaty Art. 6) and the UK Court of Appeal’s *CAAT* ruling ([2019] EWCA Civ 1020), commercial contractors and supplying states that provide precision weapons or algorithmic targeting tools knowingly deployed in violation of IHL incur international responsibility under **Article 16 of the ILC Articles on State Responsibility (ARSIWA)** and customary international law.
"@

for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '^<a id="chapter-9"></a>') {
        $targetIdx = $i - 3
        $lines.Insert($targetIdx, $text91ter)
        $lines.Insert($targetIdx + 1, "")
        Write-Output "Step 25: 91 ter inserted before chapter-9 at index $targetIdx"
        break
    }
}

[System.IO.File]::WriteAllLines($filePath, $lines, [System.Text.Encoding]::UTF8)
Write-Output "ALL REMAINING UPDATES APPLIED! New total lines: $($lines.Count)"
