# Script to cleanly replace Chapter 10 with single-quoted here-string (no variable interpolation)
$filePath = 'E:\Papers\PFPJ\Campaigns\minab\justiceForMinab\docs\FACTUAL_DETERMINATION_AND_COMPLAINT_MASTER.md'
$content = [System.IO.File]::ReadAllText($filePath, [System.Text.Encoding]::UTF8)

$startMarker = '<a id="chapter-10"></a>'
$endMarker = '**RENDERED AND SEALED**'

$startIndex = $content.IndexOf($startMarker)
$endIndex = $content.IndexOf($endMarker)

if ($startIndex -ge 0 -and $endIndex -gt $startIndex) {
    $ch10Clean = @'
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

97. **The Legal Standard of State Financial Liability (Restitutio in Integrum):**
Under customary international law, as authoritatively articulated by the Permanent Court of International Justice in the seminal ***Factory at Chorzów (Claim for Indemnity) (Germany v. Poland)*** judgment (1928, P.C.I.J., Ser. A, No. 17, p. 47) and codified in the **International Law Commission's Articles on Responsibility of States for Internationally Wrongful Acts (ILC ARSIWA, 2001, Articles 30–37)**:
> *"The essential principle contained in the actual notion of an illegal act [...] is that reparation must, so far as possible, wipe out all the consequences of the illegal act and re-establish the situation which would, in all probability, have existed if that act had not been committed. Restitution in kind, or, if this is not possible, payment of a sum corresponding to the value which a restitution in kind would bear; the award, if need be, of damages for loss sustained which would not be covered by restitution in kind or payment in place of it—such are the principles which should serve to determine the amount of compensation due for an act contrary to international law."*

97 bis. **Rejection of Discretionary Ex Gratia Condolences in Favor of Binding State Reparations:**
The Panel categorically rejects the model of discretionary, non-binding *ex gratia* condolences exemplified in **Case 05 (*Kabul Drone Strike*)**, where token financial offers were conditioned on the denial of legal liability. Reparation is not a discretionary act of grace; it is an autonomous secondary legal obligation arising automatically from the commission of an internationally wrongful act. This mandatory legal obligation is solidly anchored in bilateral and multilateral state practice:
1.  **The Belgrade Chinese Embassy Settlement (1999, 39 ILM 644 — Case 01 Benchmark):** Following the kinetic destruction of the PRC Embassy in Belgrade, the United States Government accepted formal international legal liability, tendered an official state apology, and paid **$32.5 million** in direct compensation ($28 million in sovereign property restitution to the PRC State and $4.5 million in humanitarian payments to the injured and surviving families);
2.  **UN General Assembly Resolution 51/233 (1997 — Case 09 Benchmark):** Following the shelling of the UNIFIL compound at Qana, the UN General Assembly formally established that the attacking State was legally bound to satisfy the financial damages inflicted on the facility, affirming state financial liability for kinetic bombardment of protected sanctuaries.

97 ter. **Itemized Financial Assessment of State Reparations (Docket PFPJ-2026-IR-001):**
Applying the *Chorzów Factory* standard to the demographic, physical, and medical devastation in Minab, the Panel calculates the minimum financial liability owed by the United States of America as follows:

| Reparation Head | International Legal Basis (ILC ARSIWA) | Factual / Demographic Parameter | Certified Valuation (USD) |
| :--- | :--- | :--- | :--- |
| **Head A: Material Restitution & Educational Reconstruction** | **ARSIWA Art. 35** (*Restitution in kind* / *Restitutio in integrum*) | Complete architectural design, seismic construction, outfitting, and equipment for a replacement state-of-the-art educational campus, including reinforced multi-hazard civil defense shelter, science laboratories, digital library, and sports complex. | **$45,000,000** |
| **Head B: Wrongful Death Compensation** | **ARSIWA Art. 36** (*Compensation for financially assessable damage*) | Direct, irrevocable wrongful death compensation disbursed to the certified legal heirs of all **156 deceased victims** (120 primary schoolgirls, 26 faculty members, 10 custodial staff) at $1,000,000 per victim. | **$156,000,000** |
| **Head C: Pediatric Medical Rehabilitation & Trauma Trust Fund** | **ARSIWA Art. 36** (*Compensation for personal injury and medical care*) | Establishment of an independently managed international trust fund providing lifetime medical, surgical, and prosthetic care for all **95+ wounded survivors** (including 38 pediatric amputees requiring ongoing prosthesis replacement, 24 tympanic trauma cases, and 19 ocular trauma cases), alongside comprehensive clinical trauma psychological therapy. | **$65,000,000** |
| **Head D: Moral Damages & Non-Material Satisfaction** | **ARSIWA Art. 37** (*Satisfaction for moral damage and symbolic redress*) | Endowment for an independent civic memorialization park in Minab, an annual educational scholarship foundation established in perpetuity in the names of the 120 martyred pupils, and funding for independent international research into civilian harm mitigation. | **$34,000,000** |
| **TOTAL STATE FINANCIAL LIABILITY CLAIM** | **ARSIWA Arts. 31, 35–37 (Chorzów Factory Standard)** | **Complete Restitution, Wrongful Death, Medical Trust & Satisfaction** | **$300,000,000 USD** |

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
*   **Mental Element (Mens Rea):** The perpetrators acted with knowledge and intent under Article 30 of the Rome Statute, exhibiting at minimum conditional intent and gross recklessness (*dolus eventualis*) by approving strike coordinates derived from decade-old static databases without conducting contemporaneous visual verification, and failing to execute an abort when terminal sensors revealed children's assembly grounds.

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

'@

    $content = $content.Substring(0, $startIndex) + $ch10Clean + $content.Substring($endIndex)
    [System.IO.File]::WriteAllText($filePath, $content, [System.Text.Encoding]::UTF8)
    Write-Output "Chapter 10 successfully replaced with clean, literal text!"
} else {
    Write-Error "Markers not found! startIndex=$startIndex, endIndex=$endIndex"
}
