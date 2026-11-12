/**
 * Minab School 3D Spatial Reconstruction, Verified Interior Walkthrough & Accountability Vow Engine
 * Developed for People for Peace & Justice ry (PFPJ ry) — Helsinki, Finland
 * Reconstructs the exact two-floor interior rooms, rainbow staircase, courtyard markings,
 * and camera-projected archive photos/videos verified in Forensic Architecture Investigation 121.
 */

// --- TRILINGUAL LOCALIZATION DICTIONARY ---
const I18N_DATA = {
  en: {
    pageTitle: "3D Spatial Reconstruction — Minab Primary School",
    navEvidence: "← Back to Evidence",
    heroTitle: "Shajareh Tayyebeh Primary School",
    heroCoords: "27°08'43\"N 57°05'02\"E · Minab, Hormozgan · Strike: Feb 28, 2026",
    signVowBtn: "Sign Accountability Vow",
    guidedTourBtn: "🎧 Walk Inside & Listen: 8-Stop Tour",
    cutawayBtn: "🏠 Floorplan Cutaway: All Floors",
    walkModeBtn: "🚶 Walk Inside (WASD)",
    presetBoysArch: "🌹 Boys' Ceremony Room",
    presetStairs: "🌈 Rainbow Staircase",
    presetGirlsHall: "👧 Girls' Upper Hall",
    presetClassGallery: "🖼️ 145 Portraits & 28 Drawings Inside Rooms",
    presetCrater: "💥 5m Impact Crater",
    enterVrBtn: "🥽 Enter WebXR VR",
    preStrikeBtn: "☀ Before Strike (School Full of Life)",
    postStrikeBtn: "💥 After Strike (Extent of Damage & 5m Crater)",
    hotspotsCount: "8 Stations + 145 3D Portraits & 28 Rubble Drawings Mounted Inside Rooms",
    evidenceBadge: "Forensic Architecture Camera-Aligned Spot",
    forensicLabel: "Spatial Verification & Legal Determination",
    viewInEvidencePortal: "Full Memorial Registry →",
    wingPortraitsTitle: "Schoolchildren & Educators of This Wing (Dataset v3.0.0 Studio Portraits)",
    wingDrawingsTitle: "Classroom Drawings & Homework Pulled from This Wing's Rubble",
    wingDrawingsHint: "Click to inspect high-res scan",
    controlsHelp: "Click \"🏠 Floorplan Cutaway\" or \"🖼️ 145 Portraits\" to look inside rooms · Click any 3D portrait or rubble drawing on the classroom walls to inspect",
    vowBadge: "Global Accountability Petition & Civic Vow",
    vowTitle: "The Minab Accountability Vow",
    vowSubtitle: "November 20 World Children's Day · People for Peace & Justice ry",
    vowPledgeText: "\"Bearing witness to the verified forensic record of Shajareh Tayyebeh Primary School and the lives of the 120+ schoolchildren and 26 educators taken on February 28, 2026, I solemnly vow to stand ready and participate in every lawful civic, investigative, financial, and judicial endeavor to hold every person in the chain of command accountable for this atrocity.\"",
    vowNameLabel: "Full Name *",
    vowEmailLabel: "Email Address *",
    vowTgLabel: "Telegram Username (Optional — for Action Mobilization)",
    vowPhoneLabel: "Phone / Signal / WhatsApp (Optional — for Action Mobilization)",
    vowCityLabel: "City & Country *",
    vowHowLabel: "How I Will Take Action for Accountability *",
    vowHowHint: "Select one or more ways you wish to contribute",
    vowSelectError: "Please select at least one way to take action.",
    vowSubmitError: "Could not save your Accountability Vow right now. Please check your connection and try again.",
    vowSuccessMsg: "✓ Thank you, {name}. Your Accountability Vow{count} has been recorded.",
    vowOptPetitioner: "Public Petitioner & Global Campaigner — Amplify the case & join collective actions",
    vowOptFinancial: "Financial Support for the Legal Prosecution Campaign — Fund court filings & forensic experts",
    vowOptLegal: "Legal, Human Rights & Judicial Action — Pro bono counsel & universal jurisdiction",
    vowOptMedia: "Media, Journalism & Public Amplification — Investigative reporting & translations",
    vowOptEvent: "Host or Join a Nov 20 World Children's Day Action — Vigil, university panel, or exhibition",
    vowOptResearch: "Forensic, OSINT & Archival Research — Evidence verification & witness documentation",
    vowMessageLabel: "Personal Message of Remembrance or Commitment (Optional)",
    vowConsentText: "I affirm this vow and consent to be contacted by People for Peace & Justice ry when collective legal, parliamentary, financial, or civic actions are mobilized.",
    vowSubmitBtn: "✍️ Sign the Vow & Join the Accountability Registry",
    hotspots: {
      courtyard_lines: {
        title: "1. Courtyard Morning Assembly Lines & 4-Column Portico",
        category: "Exterior Courtyard · Verified from Satellite & School Archive (00:35)",
        desc: "Right outside the east wing and the 4-column front porch portico are six yellow parallel morning assembly lines with standing circles inside a green border, alongside a circular play mark and football pitch. The perimeter wall is painted in pastel yellow, mint green, white, and light blue panels.",
        testimonyQuote: "\"At the moment of the first strike, teacher Ms. Shahriari had been in the yard. When the first missile hit, she ran toward a classroom to bring her students out, and then the second missile hit and unfortunately she was killed.\"",
        testimonyAuthor: "— Wajiheh Zakari, Teacher at Shajareh Tayyebeh School",
        finding: "Chronological satellite analysis (2015–2026) and school photos confirm playground markings, football pitch, and children assembling in the yard.",
        evidenceRef: "FA-121 / 01_reconstruction.mp4 (00:25–00:40) & 02_progression.mp4",
        videoFile: "media/fa/clips/spot_01_courtyard.mp4",
        videoStart: 15,
        spotImg: "images/fa_spots/spot_assembly_lines.jpg",
        spotCaption: "Camera-matched courtyard assembly lines & pastel perimeter wall"
      },
      boys_flower_arch: {
        title: "2. Ground Floor: Boys' Ceremony Room (Red Rose Arches)",
        category: "Ground Floor Interior · Camera-Aligned School Photo (01:12)",
        desc: "Inside the ground-floor boys' school room—identifiable by its teal-blue walls and pink window security grilles—school photographs show 12 young boys in royal blue school uniforms standing proudly beneath two red rose floral arches during a school celebration.",
        testimonyQuote: "\"At the time of the strikes, a boys' school and a pre-school occupied the ground floor of the building... hosting Mother's Day celebrations, book fairs, and award ceremonies.\"",
        testimonyAuthor: "— Forensic Architecture Investigation 121 (Interior Reconstruction)",
        finding: "Camera-frustum alignment locks the exact room dimensions, window grille bars, and teal/pink wall colors on the ground floor.",
        evidenceRef: "FA-121 / 01_reconstruction.mp4 (01:02–01:28)",
        videoFile: "media/fa/clips/spot_02_boys_arch.mp4",
        videoStart: 62,
        spotImg: "images/fa_spots/spot_boys_flower_arch.jpg",
        spotCaption: "Boys in blue school uniforms under red rose arches (Ground Floor)"
      },
      boys_classroom: {
        title: "3. Ground Floor: Boys' Classroom (Children Clapping & Singing)",
        category: "Ground Floor Classroom · Camera-Aligned Video Footage (01:55)",
        desc: "In this ground-floor classroom with sky-blue upper walls, cream lower walls, and paper cutouts of hot-air balloons and crayons, pre-strike footage shows over 35 elementary schoolboys sitting together on green patterned carpets, clapping and singing.",
        testimonyQuote: "\"Several of those images and videos were captured in the months prior to the attack, including January 2026, providing a near-contemporaneous record of the school and the children's activities.\"",
        testimonyAuthor: "— Forensic Architecture Investigation 121",
        finding: "Establishes active, high-density elementary classroom occupancy on the ground floor immediately prior to February 28, 2026.",
        evidenceRef: "FA-121 / 01_reconstruction.mp4 (01:48–02:02)",
        videoFile: "media/fa/clips/spot_03_boys_classroom.mp4",
        videoStart: 108,
        spotImg: "images/fa_spots/spot_boys_classroom.jpg",
        spotCaption: "35+ boys clapping and singing inside the ground-floor classroom"
      },
      rainbow_staircase: {
        title: "4. The Rainbow Staircase & Purple Classroom Doors",
        category: "Central Stairwell & Rear Entrance · Redmi Note 11 Pro Photo (02:45)",
        desc: "Connecting the ground-floor and first-floor central assembly halls is a staircase painted in bright rainbow steps (yellow, blue, pink, green, red) flanked by purple classroom doors and paper flower decorations. A pre-strike photo shows teachers welcoming girls at the foot of these stairs.",
        testimonyQuote: "\"When the first strike hit and made that terrifying sound, I remember Ms. Sangarzadeh, the principal of our school, fell downstairs. Then I stretched out my hand to pull my books toward myself. But then the second strike hit and I was thrown under the rubble.\"",
        testimonyAuthor: "— Parastesh Zaeri (Age 11, Survivor; her 8-year-old brother Ali Asghar was killed)",
        finding: "This exact rainbow staircase and central hall connection sat directly on the boundary of the 11:22 AM blast collapse zone.",
        evidenceRef: "FA-121 / 01_reconstruction.mp4 (02:32–02:50)",
        videoFile: "media/fa/clips/spot_04_rainbow_stairs.mp4",
        videoStart: 152,
        spotImg: "images/fa_spots/spot_rainbow_stairs.jpg",
        spotCaption: "Teachers and students at the rainbow staircase & purple doors"
      },
      girls_upper_hall: {
        title: "5. First Floor: Girls' School Assembly Hall & Pink/Green Classrooms",
        category: "First Floor Interior · Camera-Aligned Photo (03:22)",
        desc: "Upstairs on the first floor (the girls' school), classrooms were painted bright pink and sage green. In the large west assembly room with a green floor and pink/purple double doors, a pre-strike photo shows over 80 young girls in white hijabs seated on carpets together.",
        testimonyQuote: "\"The first floor housed the girls' primary school... The classroom walls were painted blue, green, and pink, and decorated with paper art.\"",
        testimonyAuthor: "— Forensic Architecture Investigation 121",
        finding: "This exact upper-floor girls' assembly room and adjacent classrooms fell completely inside the collapsed west/central blast zone.",
        evidenceRef: "FA-121 / 01_reconstruction.mp4 (02:55–03:35)",
        videoFile: "media/fa/clips/spot_05_girls_hall.mp4",
        videoStart: 175,
        spotImg: "images/fa_spots/spot_girls_assembly.jpg",
        spotCaption: "80+ schoolgirls seated together in the first-floor assembly hall"
      },
      crater_damage: {
        title: "6. 11:22 AM Strike: 5m Impact Crater & Extent of Collapse",
        category: "Post-Strike Drone Photogrammetry (March 4 Footage)",
        desc: "Comparing the pre-strike 3D floorplan with photogrammetry from March 4 drone footage reveals that the entire west wing and central assembly hall—both the upper girls' hall and ground-floor boys' rooms—were obliterated, leaving a 5-meter crater in the center of the assembly hall.",
        testimonyQuote: "\"Comparison of the building's pre-strike condition with post-strike imagery indicates that the 5m impact crater falls directly within the school's central assembly hall.\"",
        testimonyAuthor: "— Forensic Architecture Investigation 121 (Impact Crater Analysis)",
        finding: "Obliteration of the two-story west wing and central atrium accounts for the mass casualty toll of 121+ children and 26 teachers.",
        evidenceRef: "FA-121 / 07_impact_crater.mp4 & 01_reconstruction.mp4 (04:40)",
        videoFile: "media/fa/clips/spot_06_crater.mp4",
        videoStart: 0,
        spotImg: "images/fa_spots/spot_crater_photo.jpg",
        spotCaption: "Post-strike drone photogrammetry aligned with the 5m assembly hall crater"
      },
      second_wave: {
        title: "7. 2:30 PM Second Strike Wave & US Tomahawk Missile Evidence",
        category: "Shadow Analysis, Rescue Operations & Munitions Forensics",
        desc: "While 1,000–1,500 bereaved mothers, families, and Red Crescent rescuers searched the rubble (over 45 minutes after news reports broadcast that a girls' school had been hit), a second wave of US RGM/UGM-109 Tomahawk cruise missiles struck the adjacent clinic at 2:30 PM.",
        testimonyQuote: "\"All the mothers and families were still there, and the schoolyard was extremely crowded. Suddenly there was smoke and dust everywhere... Red Crescent members grabbed my hand saying we had to move because the area was being targeted again.\"",
        testimonyAuthor: "— Khadija Ahmedizadeh, Bereaved Mother of 9-year-old Mohammad Taha Jafari",
        finding: "Bellingcat and the Open Source Munitions Portal (OSMP / Airwars / ARES) positively identified the RGM/UGM-109 Tomahawk missile and fragments.",
        evidenceRef: "FA-121 / 04_bomb_cloud.mp4 & 05_shadow_cars.mp4",
        videoFile: "media/fa/clips/spot_07_second_wave.mp4",
        videoStart: 10,
        spotImg: "images/fa_spots/spot_damage_extent.jpg",
        spotCaption: "Extent of structural destruction across the school and neighborhood"
      },
      vow_shrine: {
        title: "8. The Accountability Vow Shrine & 100 Faces Memorial Walk",
        category: "Global Civic & Judicial Action · World Children's Day (Nov 20)",
        desc: "Alongside the 24 portrait steles of the children in the courtyard stands the Accountability Vow Shrine. Sign the vow to join our international roster of citizens, lawyers, researchers, and organizers committed to holding every perpetrator in the chain of command responsible.",
        testimonyQuote: "\"We vow never to let the names of the children of Minab be erased, and to stand ready for every lawful endeavor to hold every person in the chain of command accountable.\"",
        testimonyAuthor: "— The Minab Accountability Vow (People for Peace & Justice ry)",
        finding: "120+ children and 26 educators documented in the PFPJ ry Master Casualty Registry.",
        evidenceRef: "PFPJ-VOW-2026 / 06_before_after.mp4",
        videoFile: "media/fa/clips/spot_08_cutaway_damage.mp4",
        videoStart: 0,
        spotImg: "images/fa_spots/spot_floorplan_cutaway.jpg",
        spotCaption: "Full 3D cutaway of the reconstructed school rooms"
      }
    }
  },
  fi: {
    pageTitle: "3D-tilan rekonstruktio — Minabin peruskoulu",
    navEvidence: "← Takaisin todisteisiin",
    heroTitle: "Shajareh Tayyebehin peruskoulu",
    heroCoords: "27°08'43\"N 57°05'02\"E · Minab, Hormozgan · Isku: 28.2.2026",
    signVowBtn: "Allekirjoita vastuulupaus",
    guidedTourBtn: "🎧 Kävele sisällä & kuuntele: 8 pisteen kierros",
    cutawayBtn: "🏠 Pohjapiirrosleikkaus: Kerrokset",
    walkModeBtn: "🚶 Kävele sisällä (WASD)",
    presetBoysArch: "🌹 Poikien juhlahuone",
    presetStairs: "🌈 Sateenkaariportaikko",
    presetGirlsHall: "👧 Tyttöjen yläsali",
    presetClassGallery: "🖼️ 145 muotokuvaa & 28 piirustusta luokissa",
    presetCrater: "💥 5m iskukraatteri",
    enterVrBtn: "🥽 Avaa WebXR VR",
    preStrikeBtn: "☀ Ennen iskua (Koulu täynnä elämää)",
    postStrikeBtn: "💥 Iskun jälkeen (Tuhot & 5m kraatteri)",
    hotspotsCount: "8 pistettä + 145 muotokuvaa ja 28 piirustusta luokkahuoneiden seinillä",
    evidenceBadge: "Forensic Architecture -kamerasovitettu piste",
    forensicLabel: "Tilallinen varmennus & oikeudellinen johtopäätös",
    viewInEvidencePortal: "Avaa koko muistorekisteri →",
    wingPortraitsTitle: "Tämän siiven oppilaat ja opettajat (Dataset v3.0.0 muotokuvat)",
    wingDrawingsTitle: "Tämän siiven raunioista pelastetut piirustukset ja koulutehtävät",
    wingDrawingsHint: "Klikkaa nähdäksesi suurennettu kuva",
    controlsHelp: "Klikkaa \"🏠 Pohjapiirrosleikkaus\" tai \"🖼️ 145 muotokuvaa\" · Klikkaa mitä tahansa 3D-muotokuvaa tai piirustusta luokkien seinillä",
    vowBadge: "Kansainvälinen vetoomus & vastuulupaus",
    vowTitle: "Minabin vastuulupaus",
    vowSubtitle: "20. marraskuuta — Lapsen oikeuksien päivä · People for Peace & Justice ry",
    vowPledgeText: "\"Todistaen Shajareh Tayyebehin peruskoulun vahvistetun forensisen aineiston ja 28.2.2026 surmattujen yli 120 koululaisen ja 26 opettajan kohtalon, lupaan olla valmis osallistumaan kaikkiin laillisiin kansalais-, tutkinta-, rahoitus- ja oikeustoimiin, jotta jokainen komentoketjussa vastuussa oleva saatetaan oikeudenkäyntiin.\"",
    vowNameLabel: "Koko nimi *",
    vowEmailLabel: "Sähköpostiosoite *",
    vowTgLabel: "Telegram-käyttäjänimi (Valinnainen — toiminnan koordinointiin)",
    vowPhoneLabel: "Puhelin / Signal / WhatsApp (Valinnainen — toiminnan koordinointiin)",
    vowCityLabel: "Kaupunki & Maa *",
    vowHowLabel: "Miten osallistun oikeudelliseen vastuuseen saattamiseen *",
    vowHowHint: "Voit valita yhden tai useamman osallistumistavan",
    vowSelectError: "Valitse vähintään yksi osallistumistapa.",
    vowSubmitError: "Tallennus epäonnistui. Tarkista verkkoyhteys ja yritä uudelleen.",
    vowSuccessMsg: "✓ Kiitos, {name}. Vastuulupauksesi{count} on tallennettu.",
    vowOptPetitioner: "Julkinen vetoomuksen allekirjoittaja & kampanjoija — Jaa tietoa ja osallistu yhteisiin toimiin",
    vowOptFinancial: "Taloudellinen tuki oikeudenkäyntikampanjalle — Tue kansainvälisiä tuomioistuinmaksuja ja asiantuntijoita",
    vowOptLegal: "Oikeudellinen & ihmisoikeustyö — Juridinen asiantuntijuus, yleinen toimivalta ja päättäjävaikuttaminen",
    vowOptMedia: "Media, journalismi & viestintä — Tutkiva journalismi, dokumentointi ja käännökset",
    vowOptEvent: "Järjestä tai liity 20.11. Lapsen oikeuksien päivän tapahtumaan — Muistotilaisuus tai paneeli",
    vowOptResearch: "Forensinen & OSINT-tutkimus — Todisteiden verifiointi ja arkistointi",
    vowMessageLabel: "Henkilökohtainen muistoviesti tai sitoumus (Valinnainen)",
    vowConsentText: "Vahvistan tämän lupauksen ja suostun siihen, että People for Peace & Justice ry ottaa minuun yhteyttä oikeudellisten, taloudellisten tai kansalaistoimien käynnistyessä.",
    vowSubmitBtn: "✍️ Allekirjoita lupaus & liity rekisteriin",
    hotspots: {
      courtyard_lines: {
        title: "1. Koulupihan keltaiset aamurivit & 4 pylvään kuisti",
        category: "Koulupiha · Varmennettu satelliitti- ja arkistokuvista (00:35)",
        desc: "Koulun edustalla on neljän pylvään katettu sisäänkäynti ja kuusi keltaista aamukokoontumisviivaa, joille lapset järjestäytyivät joka aamu ennen oppitunteja.",
        testimonyQuote: "\"Ensimmäisen iskun hetkellä opettaja Shahriari oli pihalla. Kun ensimmäinen ohjus osui, hän juoksi luokkaan pelastamaan oppilaitaan, jolloin toinen ohjus osui.\"",
        testimonyAuthor: "— Wajiheh Zakari, koulun opettaja",
        finding: "Satelliittikuvat (2015–2026) ja koulun valokuvat vahvistavat pihan leikkimerkinnät ja jalkapallokentän.",
        evidenceRef: "FA-121 / 01_reconstruction.mp4 & 02_progression.mp4",
        videoFile: "media/fa/clips/spot_01_courtyard.mp4",
        videoStart: 15,
        spotImg: "images/fa_spots/spot_assembly_lines.jpg",
        spotCaption: "Koulupihan keltaiset kokoontumisviivat ja pastellisävyinen muuri"
      },
      boys_flower_arch: {
        title: "2. Alakerta: Poikien juhlahuone (Punaiset ruusukaaret)",
        category: "Alakerran sisätila · Kamerasovitettu valokuva (01:12)",
        desc: "Alakerran turkoosiseinäisessä huoneessa otetussa kuvassa 12 sinisiin koulupukuihin pukeutunutta poikaa seisoo kahden punaisen ruusukaaren alla koulun juhlassa.",
        testimonyQuote: "\"Alakerrassa toimi poikien koulu ja esikoulu... saleissa järjestettiin äitienpäiväjuhlia, kirjamessuja ja palkintojenjakoja.\"",
        testimonyAuthor: "— Forensic Architecture -tutkinta 121",
        finding: "Kamerasovitus vahvistaa huoneen tarkat mitat, ikkunakalterit ja seinävärit.",
        evidenceRef: "FA-121 / 01_reconstruction.mp4 (01:02–01:28)",
        videoFile: "media/fa/clips/spot_02_boys_arch.mp4",
        videoStart: 62,
        spotImg: "images/fa_spots/spot_boys_flower_arch.jpg",
        spotCaption: "Koulupojat punaisten ruusukaarten alla alakerrassa"
      },
      boys_classroom: {
        title: "3. Alakerta: Poikien luokkahuone (Taputtavat ja laulavat lapset)",
        category: "Alakerran luokka · Kamerasovitettu video (01:55)",
        desc: "Vaaleansinisessä alakerran luokkahuoneessa yli 35 pientä koulupoikaa istuu vihreällä matolla taputtaen ja laulaen tammikuussa 2026 kuvatulla videolla.",
        testimonyQuote: "\"Kuvat ja videot on otettu kuukausina ennen iskua, mukaan lukien tammikuussa 2026.\"",
        testimonyAuthor: "— Forensic Architecture -tutkinta 121",
        finding: "Todistaa aktiivisen perusopetuksen alakerran luokissa.",
        evidenceRef: "FA-121 / 01_reconstruction.mp4 (01:48–02:02)",
        videoFile: "media/fa/clips/spot_03_boys_classroom.mp4",
        videoStart: 108,
        spotImg: "images/fa_spots/spot_boys_classroom.jpg",
        spotCaption: "Yli 35 poikaa laulamassa alakerran luokkahuoneessa"
      },
      rainbow_staircase: {
        title: "4. Sateenkaariportaikko & violetit luokkien ovet",
        category: "Keskusportaikko · Redmi Note 11 Pro -valokuva (02:45)",
        desc: "Alakerran ja yläkerran keskussaleja yhdisti sateenkaaren värein maalattu portaikko ja violetit ovet. Kuvassa opettajat ottavat tyttöjä vastaan portaikon juurella.",
        testimonyQuote: "\"Kun ensimmäinen isku osui, muistan rehtorimme Ms. Sangarzadehin kaatuneen portaissa... sitten toinen isku osui ja jäin raunioiden alle.\"",
        testimonyAuthor: "— Parastesh Zaeri (11-vuotias selviytyjä)",
        finding: "Sateenkaariportaikko sijaitsi suoraan romahtaneen keskussalin reunalla.",
        evidenceRef: "FA-121 / 01_reconstruction.mp4 (02:32–02:50)",
        videoFile: "media/fa/clips/spot_04_rainbow_stairs.mp4",
        videoStart: 152,
        spotImg: "images/fa_spots/spot_rainbow_stairs.jpg",
        spotCaption: "Opettajat ja oppilaat sateenkaariportaikon juurella"
      },
      girls_upper_hall: {
        title: "5. Yläkerta: Tyttöjen suuri sali & pinkki-vihreät luokat",
        category: "Yläkerran sisätila · Kamerasovitettu valokuva (03:22)",
        desc: "Yläkerran tyttökoulun luokat oli maalattu vaaleanpunaisiksi ja vihreiksi. Suuressa länsisiiven salissa yli 80 valkohuivista koulutyttöä istuu yhdessä matoilla.",
        testimonyQuote: "\"Yläkerrassa sijaitsi tyttöjen peruskoulu, jonka seinät oli koristeltu paperitaiteella.\"",
        testimonyAuthor: "— Forensic Architecture -tutkinta 121",
        finding: "Koko tämä yläkerran länsisiipi romahti täydellisesti klo 11.22 ohjusiskussa.",
        evidenceRef: "FA-121 / 01_reconstruction.mp4 (02:55–03:35)",
        videoFile: "media/fa/clips/spot_05_girls_hall.mp4",
        videoStart: 175,
        spotImg: "images/fa_spots/spot_girls_assembly.jpg",
        spotCaption: "Yli 80 koulutyttöä kokoontuneena yläkerran salissa"
      },
      crater_damage: {
        title: "6. Klo 11.22 isku: 5 metrin kraatteri & tuhoutunut siipi",
        category: "Drone-fotogrammetria (4.3.2026 kuvamateriaali)",
        desc: "Ennen iskua ja iskun jälkeen tehtyjen 3D-mallien vertailu osoittaa, että koko länsisiipi ja keskussali tuhoutuivat täysin, jättäen 5 metrin kraatterin keskelle juhlasalia.",
        testimonyQuote: "\"5 metrin iskukraatteri sijaitsee suoraan koulun keskussalissa.\"",
        testimonyAuthor: "— Forensic Architecture -tutkinta 121",
        finding: "Selittää yli 121 lapsen ja 26 opettajan menehtymisen.",
        evidenceRef: "FA-121 / 07_impact_crater.mp4",
        videoFile: "media/fa/clips/spot_06_crater.mp4",
        videoStart: 0,
        spotImg: "images/fa_spots/spot_crater_photo.jpg",
        spotCaption: "Drone-fotogrammetria sovitettuna 5 metrin kraatteriin"
      },
      second_wave: {
        title: "7. Klo 14.30 toinen iskuaalto & Tomahawk-todisteet",
        category: "Varjoanalyysi, pelastustyöt & asetutkinta",
        desc: "Kun 1 000–1 500 äitiä ja pelastajaa etsi lapsia raunioista, toinen USA:n RGM/UGM-109 Tomahawk -ohjusten aalto iski klo 14.30.",
        testimonyQuote: "\"Kaikki äidit ja perheet olivat yhä pihalla... Punaisen Puolikuun työntekijät vetivät minut turvaan.\"",
        testimonyAuthor: "— Khadija Ahmedizadeh, 9-vuotiaan Mohammad Taha Jafarin äiti",
        finding: "Bellingcat ja OSMP vahvistivat RGM/UGM-109 Tomahawk -ohjuksen.",
        evidenceRef: "FA-121 / 04_bomb_cloud.mp4",
        videoFile: "media/fa/clips/spot_07_second_wave.mp4",
        videoStart: 10,
        spotImg: "images/fa_spots/spot_damage_extent.jpg",
        spotCaption: "Tuhoutuneen alueen laajuus koulurakennuksessa"
      },
      vow_shrine: {
        title: "8. Vastuulupauksen muistomerkki & 100 lapsen muotokuvat",
        category: "Kansainvälinen kansalais- ja oikeustoimi (20.11.)",
        desc: "Allekirjoita Minabin vastuulupaus pihan keskellä. Jokainen allekirjoitus tallennetaan rekisteriimme kansainvälisten oikeustoimien tueksi.",
        testimonyQuote: "\"Sitoudumme saattamaan jokaisen vastuullisen oikeuden eteen.\"",
        testimonyAuthor: "— Minabin vastuulupaus (People for Peace & Justice ry)",
        finding: "Suora kansalaisrekisteri — People for Peace & Justice ry (3616815-5).",
        evidenceRef: "PFPJ-VOW-2026 / 06_before_after.mp4",
        videoFile: "media/fa/clips/spot_08_cutaway_damage.mp4",
        videoStart: 0,
        spotImg: "images/fa_spots/spot_floorplan_cutaway.jpg",
        spotCaption: "Koulun molempien kerrosten 3D-pohjapiirros"
      }
    }
  },
  fa: {
    pageTitle: "بازسازی سه‌بعدی اتاق‌ها و مستندات دبستان شجره طیبه میناب",
    navEvidence: "← بازگشت به پرونده اسناد",
    heroTitle: "دبستان شجره طیبه میناب",
    heroCoords: "۲۷°۰۸'۴۳\" شمالی ۵۷°۰۵'۰۲\" شرقی · هرمزگان، میناب · ۹ اسفند ۱۴۰۴",
    signVowBtn: "امضای میثاق دادخواهی",
    guidedTourBtn: "🎧 قدم زدن در اتاق‌ها و شنیدن روایت (۸ ایستگاه)",
    cutawayBtn: "🏠 برش طبقات: مشاهده داخل اتاق‌ها",
    walkModeBtn: "🚶 قدم زدن در مدرسه (WASD)",
    presetBoysArch: "🌹 اتاق جشن پسران (همکف)",
    presetStairs: "🌈 راه‌پله رنگین‌کمان",
    presetGirlsHall: "👧 سالن دختران (طبقه اول)",
    presetClassGallery: "🖼️ ۱۴۵ تصویر شهدا و ۲۸ نقاشی داخل کلاس‌ها",
    presetCrater: "💥 گودال ۵ متری انفجار",
    enterVrBtn: "🥽 ورود به واقعیت مجازی VR",
    preStrikeBtn: "☀ پیش از حمله (مدرسه و کلاس‌های پر از زندگی)",
    postStrikeBtn: "💥 پس از حمله (محدوده تخریب و گودال ۵ متری)",
    hotspotsCount: "۸ ایستگاه + ۱۴۵ قاب تصویر دانش‌آموزان و معلمان و ۲۸ نقاشی روی دیوار کلاس‌ها",
    evidenceBadge: "نقطه منطبق‌شده در مدل سه‌بعدی فورنزیک آرکیتکچر",
    forensicLabel: "تطبیق فضایی و مستندات حقوقی",
    viewInEvidencePortal: "مشاهده کامل یادبود شهدا →",
    wingPortraitsTitle: "دانش‌آموزان و آموزگاران شهید این بخش از مدرسه (آرشیو نسخه ۳.۰)",
    wingDrawingsTitle: "نقاشی‌ها و تکالیف بیرون کشیده شده از زیر آوار این کلاس‌ها",
    wingDrawingsHint: "برای بزرگ‌نمایی روی هر نقاشی کلیک کنید",
    controlsHelp: "روی «🏠 برش طبقات» یا «🖼️ ۱۴۵ تصویر شهدا» کلیک کنید · روی هر قاب عکس یا نقاشی داخل کلاس‌های سه‌بعدی کلیک کنید",
    vowBadge: "پتیشن جهانی و میثاق دادخواهی میناب",
    vowTitle: "میثاق دادخواهی کودکان میناب",
    vowSubtitle: "۲۰ نوامبر (روز جهانی کودک) · انجمن صلح و عدالت فنلاند (PFPJ ry)",
    vowPledgeText: "«با گواهی بر مستندات راستی‌آزمایی‌شده دبستان شجره طیبه میناب و به یاد بیش از ۱۲۰ کودک دانش‌آموز و ۲۶ آموزگار که در ۹ اسفند ۱۴۰۴ جان باختند، صمیمانه پیمان می‌بندم که در هر تلاش قانونی، مدنی، تحقیقاتی، مالی و قضایی برای پاسخگو کردن تمامی آمران و عاملان این جنایت در سلسله‌مراتب فرماندهی مشارکت و همراهی کنم.»",
    vowNameLabel: "نام و نام خانوادگی *",
    vowEmailLabel: "آدرس ایمیل *",
    vowTgLabel: "شناسه تلگرام (اختیاری — جهت هماهنگی اقدامات دادخواهی)",
    vowPhoneLabel: "شماره تماس / سیگنال / واتس‌اپ (اختیاری — جهت هماهنگی اقدامات)",
    vowCityLabel: "شهر و کشور محل سکونت *",
    vowHowLabel: "نحوه همراهی و اقدام من در کارزار دادخواهی *",
    vowHowHint: "می‌توانید یک یا چند مورد را هم‌زمان انتخاب کنید",
    vowSelectError: "لطفاً دست‌کم یک مورد از روش‌های همراهی را انتخاب کنید.",
    vowSubmitError: "ثبت امضا با خطا روبه‌رو شد. لطفاً اتصال اینترنت را بررسی کرده و دوباره تلاش کنید.",
    vowSuccessMsg: "✓ سپاسگزاریم {name}؛ امضای شما در میثاق دادخواهی{count} با موفقیت ثبت شد.",
    vowOptPetitioner: "امضاکننده عمومی و کنشگر کارزار جهانی — بازنشر مستندات و همراهی در اقدامات جمعی",
    vowOptFinancial: "حمایت مالی از کارزار پیگرد قضایی بین‌المللی — تأمین هزینه‌های ثبت دادخواست و کارشناسان رسمی",
    vowOptLegal: "همکاری حقوقی، قضایی و حقوق بشری — وکالت، صلاحیت قضایی جهانی و رایزنی پارلمانی",
    vowOptMedia: "رسانه، روزنامه‌نگاری و روایت‌گری عمومی — پوشش خبری، مستندسازی و ترجمه",
    vowOptEvent: "برگزاری یا مشارکت در رویداد ۲۰ نوامبر (روز جهانی کودک) — تجمع، پنل دانشگاهی یا نمایشگاه",
    vowOptResearch: "پژوهش فنی، اطلاعات متن‌باز (OSINT) و مستندسازی — راستی‌آزمایی شواهد و ثبت شهادت‌ها",
    vowMessageLabel: "پیام یادبود یا تعهد شخصی (اختیاری)",
    vowConsentText: "این میثاق را تأیید می‌کنم و موافقم در زمان آغاز اقدامات جمعی حقوقی، پارلمانی، مالی و مدنی با من تماس گرفته شود.",
    vowSubmitBtn: "✍️ ثبت امضا و پیوستن به کارزار جهانی دادخواهی",
    hotspots: {
      courtyard_lines: {
        title: "۱. خطوط زرد صف صبحگاهی در حیاط و ایوان ۴ ستونه",
        category: "حیاط مدرسه · منطبق بر تصاویر ماهواره‌ای و آرشیو مدرسه (۰۰:۳۵)",
        desc: "در مقابل ایوان ورودی چهارستونه و بال شرقی مدرسه، ۶ خط موازی زردرنگ به همراه دایره‌های ایستادن دانش‌آموزان در کادر سبز، زمین فوتبال و نقش‌های بازی کودکان قرار دارد و دیوار دور حیاط با رنگ‌های شاد زرد، سبز، سفید و آبی رنگ‌آمیزی شده است.",
        testimonyQuote: "«در لحظه اصابت موشک اول، خانم شهریاری در حیاط بود. وقتی موشک اول به مدرسه خورد، او به سمت کلاس دوید تا شاگردانش را بیرون بیاورد که موشک دوم اصابت کرد و به شهادت رسید.»",
        testimonyAuthor: "— وجیهه ذاکری، معلم دبستان شجره طیبه",
        finding: "بررسی تصاویر ماهواره‌ای (۲۰۱۵ تا ۲۰۲۶) و عکس‌های مدرسه، خطوط صف صبحگاهی و حضور روزانه کودکان در حیاط را اثبات می‌کند.",
        evidenceRef: "FA-121 / 01_reconstruction.mp4 & 02_progression.mp4",
        videoFile: "media/fa/clips/spot_01_courtyard.mp4",
        videoStart: 15,
        spotImg: "images/fa_spots/spot_assembly_lines.jpg",
        spotCaption: "تطبیق سه‌بعدی خطوط زرد صف صبحگاهی در حیاط مدرسه"
      },
      boys_flower_arch: {
        title: "۲. طبقه همکف: اتاق جشن پسران (طاق گل‌های رز سرخ)",
        category: "داخل طبقه همکف · عکس منطبق‌شده در فضای سه‌بعدی (۰۱:۱۲)",
        desc: "در اتاق جشن طبقه همکف با دیوارهای سبزآبی و حفاظ پنجره صورتی، عکس‌های آرشیو مدرسه ۱۲ دانش‌آموز پسر با لباس فرم آبی را نشان می‌دهد که در جریان یکی از جشن‌های مدرسه زیر دو طاق گل رز قرمز ایستاده‌اند.",
        testimonyQuote: "«در زمان حمله، پیش‌دبستانی و دبستان پسرانه در طبقه همکف قرار داشت و سالن‌های مدرسه میزبان جشن روز مادر، نمایشگاه کتاب و اهدای جوایز بود.»",
        testimonyAuthor: "— گزارش ۱۲۱ فورنزیک آرکیتکچر",
        finding: "تطبیق زاویه دوربین، ابعاد دقیق اتاق، حفاظ پنجره و رنگ دیوارهای طبقه همکف را تثبیت می‌کند.",
        evidenceRef: "FA-121 / 01_reconstruction.mp4 (01:02–01:28)",
        videoFile: "media/fa/clips/spot_02_boys_arch.mp4",
        videoStart: 62,
        spotImg: "images/fa_spots/spot_boys_flower_arch.jpg",
        spotCaption: "دانش‌آموزان پسر زیر طاق گل‌های رز در طبقه همکف"
      },
      boys_classroom: {
        title: "۳. طبقه همکف: کلاس درس پسران (دست زدن و هم‌خوانی کودکان)",
        category: "کلاس طبقه همکف · ویدیوی منطبق‌شده در فضای سه‌بعدی (۰۱:۵۵)",
        desc: "در این کلاس طبقه همکف با دیوارهای آبی آسمانی و کاردستی‌های بالن و مدادرنگی روی دیوار، ویدیوی ضبط‌شده پیش از حمله بیش از ۳۵ دانش‌آموز پسر را نشان می‌دهد که روی فرش‌های سبز نشسته و با شادی دست می‌زنند و سرود می‌خوانند.",
        testimonyQuote: "«چندین تصویر و ویدیو در ماه‌های منتهی به حمله از جمله دی‌ماه ۱۴۰۴ ثبت شده‌اند و گواهی زنده از فعالیت کودکان در این اتاق‌ها هستند.»",
        testimonyAuthor: "— گزارش ۱۲۱ فورنزیک آرکیتکچر",
        finding: "اثبات تراکم بالای دانش‌آموزان خردسال در کلاس‌های طبقه همکف.",
        evidenceRef: "FA-121 / 01_reconstruction.mp4 (01:48–02:02)",
        videoFile: "media/fa/clips/spot_03_boys_classroom.mp4",
        videoStart: 108,
        spotImg: "images/fa_spots/spot_boys_classroom.jpg",
        spotCaption: "بیش از ۳۵ دانش‌آموز پسر در حال دست زدن و شادی در کلاس همکف"
      },
      rainbow_staircase: {
        title: "۴. راه‌پله رنگین‌کمان و درهای بنفش کلاس‌ها",
        category: "راه‌پله مرکزی · عکس ثبت‌شده با Redmi Note 11 Pro (۰۲:۴۵)",
        desc: "راه‌پله‌ای که سالن مرکزی طبقه همکف (پسرانه) و طبقه اول (دخترانه) را به هم متصل می‌کرد با پله‌های رنگین‌کمانی (زرد، آبی، صورتی، سبز، قرمز) و گل‌های کاغذی روی دیوار تزئین شده بود و درهای کلاس‌ها به رنگ بنفش بودند.",
        testimonyQuote: "«وقتی موشک اول با آن صدای وحشتناک اصابت کرد، یادم می‌آید خانم سنگرزاده مدیر مدرسه‌مان از پله‌ها پرت شد پایین... بعد موشک دوم خورد و زیر آوار رفتم.»",
        testimonyAuthor: "— پرستش زائری (دانش‌آموز ۱۱ ساله بازمانده)",
        finding: "این راه‌پله رنگین‌کمانی دقیقاً در مرز بخش فروریخته سالن اجتماعات مرکزی قرار داشت.",
        evidenceRef: "FA-121 / 01_reconstruction.mp4 (02:32–02:50)",
        videoFile: "media/fa/clips/spot_04_rainbow_stairs.mp4",
        videoStart: 152,
        spotImg: "images/fa_spots/spot_rainbow_stairs.jpg",
        spotCaption: "معلمان و دانش‌آموزان دختر در پای راه‌پله رنگین‌کمان"
      },
      girls_upper_hall: {
        title: "۵. طبقه اول: سالن بزرگ دختران و کلاس‌های صورتی و سبز",
        category: "داخل طبقه اول · عکس منطبق‌شده در فضای سه‌بعدی (۰۳:۲۲)",
        desc: "در طبقه اول (دبستان دخترانه)، دیوار کلاس‌ها به رنگ صورتی و سبز روشن بود. در سالن بزرگ بال غربی با کف سبز و درهای دوقلوی صورتی و بنفش، عکس پیش از حمله بیش از ۸۰ دانش‌آموز دختر با مقنعه سفید را در کنار هم نشان می‌دهد.",
        testimonyQuote: "«طبقه اول ساختمان به دبستان دخترانه اختصاص داشت و دیوارها با کاردستی‌های کاغذی دانش‌آموزان تزئین شده بود.»",
        testimonyAuthor: "— گزارش ۱۲۱ فورنزیک آرکیتکچر",
        finding: "تمام این سالن بزرگ دختران در طبقه اول و کلاس‌های مجاورش در حمله ساعت ۱۱:۲۲ به‌طور کامل فرو ریخت.",
        evidenceRef: "FA-121 / 01_reconstruction.mp4 (02:55–03:35)",
        videoFile: "media/fa/clips/spot_05_girls_hall.mp4",
        videoStart: 175,
        spotImg: "images/fa_spots/spot_girls_assembly.jpg",
        spotCaption: "بیش از ۸۰ دانش‌آموز دختر در سالن اجتماعات طبقه اول"
      },
      crater_damage: {
        title: "۶. حمله ساعت ۱۱:۲۲: گودال ۵ متری و محدوده کامل تخریب",
        category: "فتوگرامتری پهپادی پس از حمله (تصاویر ۱۳ اسفند)",
        desc: "مقایسه پلان سه‌بعدی پیش از حمله با مدل فتوگرامتری پهپادی نشان می‌دهد که کل بال غربی و سالن اجتماعات مرکزی در هر دو طبقه کاملاً منهدم شده و گودالی به قطر ۵ متر درست در مرکز سالن اجتماعات ایجاد شده است.",
        testimonyQuote: "«مقایسه وضعیت پیش و پس از حمله نشان می‌دهد گودال انفجار ۵ متری دقیقاً در مرکز سالن اجتماعات مدرسه قرار دارد.»",
        testimonyAuthor: "— گزارش ۱۲۱ فورنزیک آرکیتکچر",
        finding: "فرو ریختن سقف طبقه اول و همکف در این محدوده عامل اصلی شهادت بیش از ۱۲۱ کودک و ۲۶ آموزگار بود.",
        evidenceRef: "FA-121 / 07_impact_crater.mp4",
        videoFile: "media/fa/clips/spot_06_crater.mp4",
        videoStart: 0,
        spotImg: "images/fa_spots/spot_crater_photo.jpg",
        spotCaption: "انطباق فتوگرامتری پهپادی با گودال ۵ متری در مرکز سالن مدرسه"
      },
      second_wave: {
        title: "۷. موج دوم حملات در ساعت ۱۴:۳۰ و شواهد موشک تاماهاک آمریکا",
        category: "تحلیل سایه‌ها، عملیات امداد و جرم‌شناسی تسلیحات",
        desc: "در حالی که ۱۰۰۰ تا ۱۵۰۰ مادر، خانواده و امدادگر هلال‌احمر مشغول جستجوی کودکان زیر آوار بودند، موج دوم موشک‌های کروز تاماهاک آمریکا در ساعت ۱۴:۳۰ به درمانگاه مجاور اصابت کرد.",
        testimonyQuote: "«همه مادرها و خانواده‌ها هنوز آنجا بودند و حیاط مدرسه به‌شدت شلوغ بود... نیروهای هلال‌احمر دستم را گرفتند و گفتند باید به پشت مدرسه برویم چون منطقه دوباره هدف قرار گرفته است.»",
        testimonyAuthor: "— خدیجه احمدی‌زاده، مادر داغدار دانش‌آموز ۹ ساله محمدطه جعفری",
        finding: "بلینگ‌کت و پرتال مهمات متن‌باز (OSMP / Airwars) موشک RGM/UGM-109 Tomahawk ارتش آمریکا را تأیید کردند.",
        evidenceRef: "FA-121 / 04_bomb_cloud.mp4",
        videoFile: "media/fa/clips/spot_07_second_wave.mp4",
        videoStart: 10,
        spotImg: "images/fa_spots/spot_damage_extent.jpg",
        spotCaption: "محدوده دقیق تخریب سازه مدرسه (کادر زردرنگ)"
      },
      vow_shrine: {
        title: "۸. یادمان میثاق دادخواهی و دیوار یادبود ۱۰۰ چهره کودکان",
        category: "اقدام مشترک مدنی و حقوقی · روز جهانی کودک (۲۰ نوامبر)",
        desc: "در کنار ۲۴ تابلوی تصاویر کودکان در حیاط مدرسه، یادمان میثاق دادخواهی قرار دارد. با امضای این میثاق، آمادگی خود را برای مشارکت در هر اقدام قانونی و بین‌المللی جهت محاکمه آمران و عاملان این جنایت ثبت کنید.",
        testimonyQuote: "«پیمان می‌بندیم که نام کودکان میناب هرگز فراموش نشود و برای پاسخگو کردن تک‌تک آمران و عاملان این جنایت آماده باشیم.»",
        testimonyAuthor: "— میثاق دادخواهی میناب (انجمن صلح و عدالت PFPJ ry)",
        finding: "ثبت رسمی در سامانه انجمن صلح و عدالت هلسینکی (3616815-5).",
        evidenceRef: "PFPJ-VOW-2026 / 06_before_after.mp4",
        videoFile: "media/fa/clips/spot_08_cutaway_damage.mp4",
        videoStart: 0,
        spotImg: "images/fa_spots/spot_floorplan_cutaway.jpg",
        spotCaption: "نمای برش‌خورده سه‌بعدی اتاق‌های هر دو طبقه مدرسه"
      }
    }
  }
};

// --- 8-STOP GUIDED INTERIOR & COURTYARD TOUR SEQUENCE ---
const GUIDED_TOUR_STOPS = [
  {
    hotspotId: 'courtyard_lines',
    temporal: 0.0,
    cutawayMode: 0,
    camPos: [4.5, 3.2, 14.5],
    lookAt: [20.0, 1.8, 6.5],
    waypoints: [
      { camPos: [4.5, 3.2, 14.5], lookAt: [20.0, 1.8, 6.5] },
      { camPos: [7.2, 2.1, 9.5], lookAt: [26.0, 1.7, 5.8] },
      { camPos: [3.5, 2.2, 11.0], lookAt: [-1.0, 2.4, 1.2] }
    ],
    shortBadge: { en: "01 / 08", fi: "01 / 08", fa: "۰۱ / ۰۸" },
    badge: { en: "STOP 1 OF 8 · COURTYARD YELLOW ASSEMBLY LINES", fi: "PISTE 1/8 · KOULUPIHAN AAMURIVIT", fa: "ایستگاه ۱ از ۸ · خطوط زرد صف صبحگاهی در حیاط" }
  },
  {
    hotspotId: 'boys_flower_arch',
    temporal: 0.0,
    cutawayMode: 2,
    camPos: [1.5, 2.45, -4.3],
    lookAt: [4.5, 1.85, -7.8],
    waypoints: [
      { camPos: [1.5, 2.45, -4.3], lookAt: [4.5, 1.85, -7.8] },
      { camPos: [3.8, 2.1, -4.3], lookAt: [4.2, 1.85, -7.8] },
      { camPos: [6.1, 2.15, -4.6], lookAt: [1.5, 1.85, -6.8] }
    ],
    shortBadge: { en: "02 / 08", fi: "02 / 08", fa: "۰۲ / ۰۸" },
    badge: { en: "STOP 2 OF 8 · GROUND FLOOR: BOYS' CEREMONY ROOM (ROSE ARCHES)", fi: "PISTE 2/8 · ALAKERTA: POIKIEN JUHLAHUONE", fa: "ایستگاه ۲ از ۸ · طبقه همکف: اتاق جشن پسران (طاق گل رز)" }
  },
  {
    hotspotId: 'boys_classroom',
    temporal: 0.0,
    cutawayMode: 2,
    camPos: [-13.3, 2.35, 1.6],
    lookAt: [-17.8, 1.65, -1.6],
    waypoints: [
      { camPos: [-13.3, 2.35, 1.6], lookAt: [-17.8, 1.65, -1.6] },
      { camPos: [-13.5, 2.15, 0.2], lookAt: [-18.0, 1.65, -1.2] },
      { camPos: [-14.2, 2.10, -1.4], lookAt: [-18.2, 1.65, 0.8] }
    ],
    shortBadge: { en: "03 / 08", fi: "03 / 08", fa: "۰۳ / ۰۸" },
    badge: { en: "STOP 3 OF 8 · GROUND FLOOR: BOYS' CLASSROOM (CLAPPING & SINGING)", fi: "PISTE 3/8 · ALAKERTA: POIKIEN LUOKKAHUONE", fa: "ایستگاه ۳ از ۸ · طبقه همکف: کلاس درس پسران" }
  },
  {
    hotspotId: 'rainbow_staircase',
    temporal: 0.0,
    cutawayMode: 2,
    camPos: [-1.8, 2.35, -1.5],
    lookAt: [-1.8, 2.0, -9.5],
    waypoints: [
      { camPos: [-1.8, 2.35, -1.5], lookAt: [-1.8, 2.0, -9.5] },
      { camPos: [-1.8, 2.15, -4.2], lookAt: [-1.6, 2.1, -10.2] },
      { camPos: [-4.6, 2.25, -5.2], lookAt: [-0.5, 2.0, -8.5] }
    ],
    shortBadge: { en: "04 / 08", fi: "04 / 08", fa: "۰۴ / ۰۸" },
    badge: { en: "STOP 4 OF 8 · THE RAINBOW STAIRCASE & PURPLE DOORS", fi: "PISTE 4/8 · SATEENKAARIPORTAIKKO", fa: "ایستگاه ۴ از ۸ · راه‌پله رنگین‌کمان و درهای بنفش" }
  },
  {
    hotspotId: 'girls_upper_hall',
    temporal: 0.0,
    cutawayMode: 1,
    camPos: [-12.3, 5.95, 1.4],
    lookAt: [-16.5, 5.25, -8.5],
    waypoints: [
      { camPos: [-12.3, 5.95, 1.4], lookAt: [-16.5, 5.25, -8.5] },
      { camPos: [-12.4, 5.65, -2.5], lookAt: [-17.5, 5.30, -9.2] },
      { camPos: [-13.2, 5.55, -6.2], lookAt: [-18.5, 5.30, -6.5] }
    ],
    shortBadge: { en: "05 / 08", fi: "05 / 08", fa: "۰۵ / ۰۸" },
    badge: { en: "STOP 5 OF 8 · FIRST FLOOR: GIRLS' ASSEMBLY HALL & PINK/GREEN ROOMS", fi: "PISTE 5/8 · YLÄKERTA: TYTTÖJEN SALI", fa: "ایستگاه ۵ از ۸ · طبقه اول: سالن بزرگ دختران و کلاس‌های صورتی/سبز" }
  },
  {
    hotspotId: 'crater_damage',
    temporal: 1.0,
    cutawayMode: 0,
    camPos: [-22.0, 15.5, 14.0],
    lookAt: [-2.0, 2.2, -5.5],
    waypoints: [
      { camPos: [-22.0, 15.5, 14.0], lookAt: [-2.0, 2.2, -5.5] },
      { camPos: [-13.5, 6.8, -2.5], lookAt: [2.0, 2.5, -5.8] },
      { camPos: [-8.8, 2.5, -5.5], lookAt: [3.5, 2.4, -5.5] }
    ],
    shortBadge: { en: "06 / 08", fi: "06 / 08", fa: "۰۶ / ۰۸" },
    badge: { en: "STOP 6 OF 8 · 11:22 AM STRIKE: 5M CRATER & EXTENT OF COLLAPSE", fi: "PISTE 6/8 · KLO 11.22 ISKU: 5M KRAATTERI", fa: "ایستگاه ۶ از ۸ · ساعت ۱۱:۲۲: گودال ۵ متری و محدوده تخریب" }
  },
  {
    hotspotId: 'second_wave',
    temporal: 1.0,
    cutawayMode: 0,
    camPos: [8.0, 7.0, 16.0],
    lookAt: [-1.0, 2.5, -3.0],
    waypoints: [
      { camPos: [8.0, 7.0, 16.0], lookAt: [-1.0, 2.5, -3.0] },
      { camPos: [18.5, 8.5, 15.5], lookAt: [4.0, 2.2, 1.5] },
      { camPos: [26.0, 10.5, 14.0], lookAt: [6.0, 2.4, -2.0] }
    ],
    shortBadge: { en: "07 / 08", fi: "07 / 08", fa: "۰۷ / ۰۸" },
    badge: { en: "STOP 7 OF 8 · 2:30 PM SECOND WAVE & TOMAHAWK EVIDENCE", fi: "PISTE 7/8 · KLO 14.30 TOINEN ISKUAALTO", fa: "ایستگاه ۷ از ۸ · ساعت ۱۴:۳۰: موج دوم حملات و شواهد تاماهاک" }
  },
  {
    hotspotId: 'vow_shrine',
    temporal: 0.0,
    cutawayMode: 1,
    camPos: [-1.5, 2.85, 26.2],
    lookAt: [-1.5, 1.95, 13.5],
    waypoints: [
      { camPos: [-1.5, 2.85, 26.2], lookAt: [-1.5, 1.95, 13.5] },
      { camPos: [-1.5, 2.35, 18.8], lookAt: [-1.5, 2.10, 10.5] },
      { camPos: [-1.5, 2.15, 14.8], lookAt: [-1.5, 2.15, 10.5] }
    ],
    shortBadge: { en: "08 / 08", fi: "08 / 08", fa: "۰۸ / ۰۸" },
    badge: { en: "STOP 8 OF 8 · THE ACCOUNTABILITY VOW SHRINE", fi: "PISTE 8/8 · VASTUULUPAUKSEN MUISTOMERKKI", fa: "ایستگاه ۸ از ۸ · یادمان میثاق دادخواهی — ثبت پیمان جهانی" }
  }
];

// --- APPLICATION STATE ---
let currentLang = 'en';
let scene, camera, renderer, controls;
let terrainGroup, preStrikeModelGroup, postStrikeModelGroup, memorialBoardsGroup, markersGroup;
let groundFloorGroup, firstFloorGroup, roofGroup;
let cutawayState = 0; // 0 = Full Building, 1 = Roof Off (First Floor Open), 2 = First Floor Off (Ground Floor Open)
let damageSliderValue = 0.0;
let activeHotspotId = null;
let isAnimatingCamera = false;
let animationTarget = { pos: null, lookAt: null };
let clock;
let childrenList = [];
let teachersList = [];
let drawingsList = [];
let clickable3DArtifacts = [];
let raycaster, pointerNDC;
let pointerDownPos = { x: 0, y: 0 };
let isWalkMode = false;
let isGuidedTour = false;
let currentTourIndex = 0;
let voiceNarrationEnabled = true;
const moveKeys = { forward: false, backward: false, left: false, right: false };
const VOW_BADGE_THRESHOLD = 100;
let vowSignatoryCount = 0;

// --- INITIALIZATION ---
function startReconstructionApp() {
  if (typeof THREE === 'undefined') {
    setTimeout(startReconstructionApp, 100);
    return;
  }
  try { localStorage.removeItem('pfp_vow_count'); } catch (_) {}
  clock = new THREE.Clock();
  updateVowBadge();
  fetchRealVowCount();
  initI18n();
  initWalkthroughPipManifest();
  initThreeEngine();
  buildEnvironmentAndTerrain();
  buildProceduralSchoolModels();
  loadChildrenAndBuildInWorldMemorial();
  init3DPortraitRaycaster();
  initHotspots();
  initUIControls();
  initKeyboardWalkControls();
  animate();
}

if (document.readyState === 'loading') {
  window.addEventListener('DOMContentLoaded', startReconstructionApp);
} else {
  startReconstructionApp();
}

function updateVowBadge() {
  window.vowSignatoryCount = vowSignatoryCount;
  const badge = document.getElementById('vowCountBadge');
  if (!badge) return;
  if (vowSignatoryCount >= VOW_BADGE_THRESHOLD) {
    badge.textContent = vowSignatoryCount.toLocaleString();
    badge.style.display = 'inline-block';
  } else {
    badge.textContent = '';
    badge.style.display = 'none';
  }
}

async function fetchRealVowCount() {
  let statsUrl = '/api/telegram/vow-stats/';
  if (window.location.protocol === 'file:' || window.location.port === '8090') {
    statsUrl = 'http://localhost:8000/api/telegram/vow-stats/';
  }
  try {
    const resp = await fetch(statsUrl, { cache: 'no-store' });
    if (resp.ok) {
      const data = await resp.json();
      if (typeof data.count === 'number') {
        vowSignatoryCount = data.count;
        updateVowBadge();
      }
    }
  } catch (_) {
    updateVowBadge();
  }
}

// --- LOCALIZATION HANDLER ---
function initI18n() {
  const params = new URLSearchParams(window.location.search);
  const urlVoice = params.get('voice');
  const urlLang = params.get('lang');
  const saved = localStorage.getItem('pfp_lang');

  if (urlVoice && NARRATOR_PROFILES[urlVoice]) {
    activeVoiceProfile = urlVoice;
    preferredVoiceByLang[NARRATOR_PROFILES[urlVoice].lang] = urlVoice;
    currentLang = NARRATOR_PROFILES[urlVoice].lang;
  } else if (urlLang && ['en', 'fi', 'fa'].includes(urlLang)) {
    currentLang = urlLang;
    activeVoiceProfile = currentLang === 'fa' ? preferredVoiceByLang.fa : preferredVoiceByLang.en;
  } else if (saved && ['en', 'fi', 'fa'].includes(saved)) {
    currentLang = saved;
    activeVoiceProfile = currentLang === 'fa' ? preferredVoiceByLang.fa : preferredVoiceByLang.en;
  }
  applyTranslations();
  updateNarratorButtonsUI();
}

function setLanguage(lang) {
  currentLang = lang;
  localStorage.setItem('pfp_lang', lang);
  const targetLangBucket = lang === 'fa' ? 'fa' : 'en';
  if (!NARRATOR_PROFILES[activeVoiceProfile] || NARRATOR_PROFILES[activeVoiceProfile].lang !== targetLangBucket) {
    activeVoiceProfile = preferredVoiceByLang[targetLangBucket];
  }
  applyTranslations();
  updateNarratorButtonsUI();
  updateHotspotLabels();
  if (activeHotspotId) {
    showHotspotModal(activeHotspotId);
  }
  if (isGuidedTour) {
    renderGuidedTourStep(currentTourIndex, true);
  }
}

function applyTranslations() {
  const t = I18N_DATA[currentLang] || I18N_DATA.en;
  document.documentElement.lang = currentLang;
  document.documentElement.dir = (currentLang === 'fa') ? 'rtl' : 'ltr';
  document.body.dir = (currentLang === 'fa') ? 'rtl' : 'ltr';

  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (t[key]) el.textContent = t[key];
  });

  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-lang') === currentLang);
  });
}

// --- THREE.JS ENGINE CORE ---
function initThreeEngine() {
  const container = document.getElementById('canvasContainer');
  const width = container.clientWidth || window.innerWidth;
  const height = container.clientHeight || window.innerHeight;

  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0e17);
  scene.fog = new THREE.FogExp2(0x0a0e17, 0.0055);

  camera = new THREE.PerspectiveCamera(48, width / height, 0.25, 1000);
  camera.position.set(28, 22, 34);

  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: "high-performance" });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.22;
  if (renderer.xr) {
    renderer.xr.enabled = true;
  }
  container.appendChild(renderer.domElement);

  controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.06;
  controls.maxPolarAngle = Math.PI / 2 - 0.01;
  controls.minDistance = 0.8;
  controls.maxDistance = 140;
  controls.target.set(0, 3.0, -3);
  controls.addEventListener('start', () => {
    if (isGuidedTour) {
      tourManualCameraOverride = true;
      isAnimatingCamera = false;
    }
  });

  const hemiLight = new THREE.HemisphereLight(0xfff9f0, 0x263042, 0.88);
  hemiLight.position.set(0, 55, 0);
  scene.add(hemiLight);

  const sunLight = new THREE.DirectionalLight(0xfff3db, 1.35);
  sunLight.position.set(28, 58, 24);
  sunLight.castShadow = true;
  sunLight.shadow.mapSize.width = 2048;
  sunLight.shadow.mapSize.height = 2048;
  sunLight.shadow.camera.near = 10;
  sunLight.shadow.camera.far = 150;
  sunLight.shadow.camera.left = -45;
  sunLight.shadow.camera.right = 45;
  sunLight.shadow.camera.top = 45;
  sunLight.shadow.camera.bottom = -45;
  sunLight.shadow.bias = -0.0005;
  scene.add(sunLight);

  terrainGroup = new THREE.Group();
  terrainGroup.name = "Minab_Courtyard_And_Boundary";
  preStrikeModelGroup = new THREE.Group();
  preStrikeModelGroup.name = "Shajareh_Tayyebeh_School_PreStrike";
  postStrikeModelGroup = new THREE.Group();
  postStrikeModelGroup.name = "Shajareh_Tayyebeh_School_PostStrike";
  memorialBoardsGroup = new THREE.Group();
  memorialBoardsGroup.name = "InWorld_Children_Portraits_And_Vow_Shrine";
  markersGroup = new THREE.Group();

  scene.add(terrainGroup);
  scene.add(preStrikeModelGroup);
  scene.add(postStrikeModelGroup);
  scene.add(memorialBoardsGroup);
  scene.add(markersGroup);

  postStrikeModelGroup.visible = false;

  window.addEventListener('resize', onWindowResize, false);
}

function onWindowResize() {
  const container = document.getElementById('canvasContainer');
  const width = container.clientWidth || window.innerWidth;
  const height = container.clientHeight || window.innerHeight;
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  renderer.setSize(width, height);
}

// --- HELPER: CREATE CAMERA FRUSTUM + ALIGNED PHOTO PLANE IN 3D ROOM ---
function createCameraAlignedPhotoInSpace(parentGroup, photoUrl, camPos, photoPos, rotY, width, height) {
  const group = new THREE.Group();
  const loader = new THREE.TextureLoader();

  const yellowLineMat = new THREE.LineBasicMaterial({ color: 0xe5e059 });
  const hw = width / 2;
  const hh = height / 2;

  const corners = [
    new THREE.Vector3(-hw, -hh, 0),
    new THREE.Vector3(hw, -hh, 0),
    new THREE.Vector3(hw, hh, 0),
    new THREE.Vector3(-hw, hh, 0)
  ];

  const frameGroup = new THREE.Group();
  frameGroup.position.set(photoPos[0], photoPos[1], photoPos[2]);
  frameGroup.rotation.y = rotY;
  frameGroup.userData = { photoUrl, feature: 'camera_aligned_photo' };

  const borderPts = [...corners, corners[0]];
  const borderGeo = new THREE.BufferGeometry().setFromPoints(borderPts);
  frameGroup.add(new THREE.Line(borderGeo, yellowLineMat));

  // Compute true camera apex in local space of frameGroup
  const worldDelta = new THREE.Vector3(
    camPos[0] - photoPos[0],
    camPos[1] - photoPos[1],
    camPos[2] - photoPos[2]
  );
  const localCam = worldDelta.applyAxisAngle(new THREE.Vector3(0, 1, 0), -rotY);
  if (localCam.lengthSq() < 0.25) {
    localCam.set(0, 0, 2.2);
  }

  const rayPts = [];
  corners.forEach(c => {
    rayPts.push(localCam, c);
  });
  const rayGeo = new THREE.BufferGeometry().setFromPoints(rayPts);
  frameGroup.add(new THREE.LineSegments(rayGeo, yellowLineMat));

  loader.load(photoUrl, (tex) => {
    const mat = new THREE.MeshBasicMaterial({
      map: tex,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.92
    });
    const mesh = new THREE.Mesh(new THREE.PlaneGeometry(width, height), mat);
    frameGroup.add(mesh);
  });

  group.add(frameGroup);
  parentGroup.add(group);
  return frameGroup;
}

// --- PROCEDURAL SCHOOL MURALS & SURFACE TEXTURES (MATCHING ON-SITE ARCHIVE FOOTAGE) ---
let cachedMuralTextures = null;
function getSchoolMuralTextures() {
  if (cachedMuralTextures) return cachedMuralTextures;

  // 1. East Wing Front Dado Mural: Boy reading on flying carpet + red/yellow tulips + butterflies (Mehr News / Abbas Zakeri)
  const eastCanvas = document.createElement('canvas');
  eastCanvas.width = 1024;
  eastCanvas.height = 384;
  const ec = eastCanvas.getContext('2d');
  const skyGrad = ec.createLinearGradient(0, 0, 0, 384);
  skyGrad.addColorStop(0, '#89c0d6');
  skyGrad.addColorStop(0.68, '#9fd0c4');
  skyGrad.addColorStop(1, '#4f9160');
  ec.fillStyle = skyGrad;
  ec.fillRect(0, 0, 1024, 384);

  // Meadow grass blades along bottom
  ec.fillStyle = '#3b7a4c';
  for (let gx = 0; gx < 1024; gx += 12) {
    ec.beginPath();
    ec.moveTo(gx, 384);
    ec.lineTo(gx + 6, 336 - (gx % 24));
    ec.lineTo(gx + 12, 384);
    ec.fill();
  }

  // Tulips on left & right
  const tulipSpots = [55, 115, 175, 240, 310, 385, 455, 855, 925, 980];
  const tulipColors = ['#d9383a', '#e86f88', '#eab308', '#d9383a', '#ec4899', '#eab308', '#d9383a', '#f59e0b', '#d9383a', '#ec4899'];
  tulipSpots.forEach((tx, idx) => {
    const stemTop = 250 + (idx % 3) * 18;
    ec.strokeStyle = '#2d6a3e';
    ec.lineWidth = 6;
    ec.beginPath();
    ec.moveTo(tx, 380);
    ec.quadraticCurveTo(tx - 6, 320, tx, stemTop);
    ec.stroke();

    ec.fillStyle = tulipColors[idx % tulipColors.length];
    ec.beginPath();
    ec.arc(tx, stemTop - 6, 18, 0, Math.PI, false);
    ec.lineTo(tx - 18, stemTop - 26);
    ec.lineTo(tx - 6, stemTop - 14);
    ec.lineTo(tx, stemTop - 28);
    ec.lineTo(tx + 6, stemTop - 14);
    ec.lineTo(tx + 18, stemTop - 26);
    ec.closePath();
    ec.fill();
  });

  // Golden patterned reading carpet (right-center)
  ec.save();
  ec.translate(685, 295);
  ec.rotate(-0.12);
  ec.fillStyle = '#d97706';
  ec.strokeStyle = '#fef3c7';
  ec.lineWidth = 5;
  ec.beginPath();
  ec.moveTo(-110, 20);
  ec.lineTo(95, -5);
  ec.lineTo(125, 42);
  ec.lineTo(-85, 62);
  ec.closePath();
  ec.fill();
  ec.stroke();
  ec.restore();

  // Child in yellow shirt kneeling & reading open book
  ec.fillStyle = '#64748b'; // trousers
  ec.beginPath();
  ec.ellipse(705, 286, 36, 18, -0.1, 0, Math.PI * 2);
  ec.fill();
  ec.fillStyle = '#eab308'; // yellow shirt
  ec.beginPath();
  ec.roundRect(675, 205, 54, 68, 14);
  ec.fill();
  ec.fillStyle = '#f6d5b0'; // face
  ec.beginPath();
  ec.arc(702, 168, 34, 0, Math.PI * 2);
  ec.fill();
  ec.fillStyle = '#4a2e1b'; // hair
  ec.beginPath();
  ec.arc(702, 156, 35, Math.PI * 0.95, Math.PI * 2.05);
  ec.fill();
  // Open white book on lectern/hands
  ec.fillStyle = '#ffffff';
  ec.strokeStyle = '#475569';
  ec.lineWidth = 3;
  ec.beginPath();
  ec.moveTo(640, 245);
  ec.lineTo(682, 255);
  ec.lineTo(682, 282);
  ec.lineTo(640, 272);
  ec.closePath();
  ec.fill();
  ec.stroke();

  // White & golden butterflies
  [[585, 130, '#f59e0b'], [775, 145, '#f8fafc'], [625, 92, '#fde047'], [825, 195, '#fb923c']].forEach(([bx, by, bCol]) => {
    ec.fillStyle = bCol;
    ec.strokeStyle = '#334155';
    ec.lineWidth = 2;
    ec.beginPath();
    ec.ellipse(bx - 12, by - 6, 14, 10, -0.4, 0, Math.PI * 2);
    ec.ellipse(bx + 12, by - 6, 14, 10, 0.4, 0, Math.PI * 2);
    ec.fill();
    ec.stroke();
  });
  const eastMuralTex = new THREE.CanvasTexture(eastCanvas);

  // 2. Yellow Courtyard Dividing Wall Panel with Large Red Tulip (x = +19..+23.6)
  const tulipCanvas = document.createElement('canvas');
  tulipCanvas.width = 512;
  tulipCanvas.height = 384;
  const tc = tulipCanvas.getContext('2d');
  tc.fillStyle = '#e0c53a';
  tc.fillRect(0, 0, 512, 384);
  tc.strokeStyle = '#3f7d3c';
  tc.lineWidth = 10;
  tc.beginPath();
  tc.moveTo(350, 384);
  tc.quadraticCurveTo(332, 265, 348, 175);
  tc.stroke();
  tc.fillStyle = '#4d8b44';
  tc.beginPath();
  tc.ellipse(376, 295, 36, 16, -0.6, 0, Math.PI * 2);
  tc.fill();
  tc.fillStyle = '#c92a2a';
  tc.beginPath();
  tc.arc(348, 155, 42, 0, Math.PI, false);
  tc.lineTo(306, 105);
  tc.lineTo(334, 130);
  tc.lineTo(348, 96);
  tc.lineTo(362, 130);
  tc.lineTo(390, 105);
  tc.closePath();
  tc.fill();
  const yellowTulipTex = new THREE.CanvasTexture(tulipCanvas);

  // 3. Main Gate Mint Wall with Colored Pencils & Persian Letters (pip01b_01)
  const gateCanvas = document.createElement('canvas');
  gateCanvas.width = 512;
  gateCanvas.height = 512;
  const gc = gateCanvas.getContext('2d');
  gc.fillStyle = '#bfe3d0';
  gc.fillRect(0, 0, 512, 512);
  // Left brick quoins
  for (let by = 16; by < 496; by += 76) {
    gc.fillStyle = '#c84b31';
    gc.fillRect(10, by, 34, 52);
  }
  // Colored pencils
  function drawPencil(x, y, ang, bodyHex) {
    gc.save();
    gc.translate(x, y);
    gc.rotate(ang);
    gc.fillStyle = bodyHex;
    gc.strokeStyle = '#1e293b';
    gc.lineWidth = 4;
    gc.fillRect(-22, -70, 44, 140);
    gc.strokeRect(-22, -70, 44, 140);
    gc.fillStyle = '#fde68a';
    gc.beginPath();
    gc.moveTo(-22, -70);
    gc.lineTo(0, -118);
    gc.lineTo(22, -70);
    gc.closePath();
    gc.fill();
    gc.stroke();
    gc.fillStyle = bodyHex;
    gc.beginPath();
    gc.moveTo(-8, -100);
    gc.lineTo(0, -118);
    gc.lineTo(8, -100);
    gc.closePath();
    gc.fill();
    gc.restore();
  }
  drawPencil(165, 315, 0.52, '#60a5fa');
  drawPencil(305, 165, -0.68, '#f472b6');
  drawPencil(410, 330, -0.25, '#facc15');
  gc.fillStyle = '#eab308';
  gc.strokeStyle = '#1e293b';
  gc.lineWidth = 4;
  gc.font = 'bold 92px Tahoma, sans-serif';
  gc.fillText('آ ب', 235, 390);
  gc.strokeText('آ ب', 235, 390);
  const pencilGateTex = new THREE.CanvasTexture(gateCanvas);

  // 4. Portico Column Texture: White upper + subtle Iranian tricolor diagonal bands on lower half
  const colCanvas = document.createElement('canvas');
  colCanvas.width = 256;
  colCanvas.height = 512;
  const cc = colCanvas.getContext('2d');
  cc.fillStyle = '#edeff2';
  cc.fillRect(0, 0, 256, 512);
  cc.save();
  cc.beginPath();
  cc.rect(0, 230, 256, 282);
  cc.clip();
  cc.fillStyle = '#3b8c58';
  cc.beginPath();
  cc.moveTo(0, 250);
  cc.lineTo(256, 195);
  cc.lineTo(256, 290);
  cc.lineTo(0, 345);
  cc.closePath();
  cc.fill();
  cc.fillStyle = '#f8fafc';
  cc.beginPath();
  cc.moveTo(0, 345);
  cc.lineTo(256, 290);
  cc.lineTo(256, 395);
  cc.lineTo(0, 450);
  cc.closePath();
  cc.fill();
  cc.fillStyle = '#c43e3e';
  cc.beginPath();
  cc.moveTo(0, 450);
  cc.lineTo(256, 395);
  cc.lineTo(256, 512);
  cc.lineTo(0, 512);
  cc.closePath();
  cc.fill();
  // Small red emblem mark in white band
  cc.fillStyle = '#b91c1c';
  cc.beginPath();
  cc.arc(128, 368, 15, 0, Math.PI * 2);
  cc.fill();
  cc.restore();
  const porticoColTex = new THREE.CanvasTexture(colCanvas);

  // 5. Rear Dinosaur Height-Chart Mural (hd/f_051.jpg)
  const dinoCanvas = document.createElement('canvas');
  dinoCanvas.width = 512;
  dinoCanvas.height = 384;
  const dc = dinoCanvas.getContext('2d');
  dc.fillStyle = '#e5c4d3';
  dc.fillRect(0, 0, 512, 384);
  // Height chart ruler
  dc.fillStyle = '#f4a4b8';
  dc.fillRect(390, 60, 44, 290);
  dc.strokeStyle = '#9d174d';
  dc.lineWidth = 3;
  for (let ry = 75; ry < 340; ry += 22) {
    dc.beginPath();
    dc.moveTo(390, ry);
    dc.lineTo(414, ry);
    dc.stroke();
  }
  // Friendly green brontosaurus silhouette
  dc.fillStyle = '#2f855a';
  dc.beginPath();
  dc.ellipse(275, 290, 62, 36, 0, 0, Math.PI * 2);
  dc.fill();
  dc.lineWidth = 26;
  dc.strokeStyle = '#2f855a';
  dc.lineCap = 'round';
  dc.beginPath();
  dc.moveTo(322, 275);
  dc.quadraticCurveTo(350, 170, 355, 95);
  dc.stroke();
  dc.beginPath();
  dc.ellipse(372, 92, 24, 16, 0.1, 0, Math.PI * 2);
  dc.fill();
  dc.beginPath();
  dc.moveTo(215, 292);
  dc.quadraticCurveTo(165, 285, 148, 245);
  dc.stroke();
  dc.fillRect(235, 315, 18, 48);
  dc.fillRect(300, 315, 18, 48);
  const dinoWallTex = new THREE.CanvasTexture(dinoCanvas);

  // 6. East Perimeter Pastel Yellow Tree Mural (pip01a_03)
  const treeMuralCanvas = document.createElement('canvas');
  treeMuralCanvas.width = 512;
  treeMuralCanvas.height = 384;
  const tmc = treeMuralCanvas.getContext('2d');
  tmc.fillStyle = '#dfd688';
  tmc.fillRect(0, 0, 512, 384);
  tmc.fillStyle = '#6b4f35';
  tmc.fillRect(242, 220, 28, 130);
  tmc.fillStyle = '#4d7c58';
  tmc.beginPath();
  tmc.arc(256, 165, 78, 0, Math.PI * 2);
  tmc.fill();
  const eastTreeMuralTex = new THREE.CanvasTexture(treeMuralCanvas);

  // 7. Post-Strike Window Smoke Scorch Plume (pip03b_01)
  const scorchCanvas = document.createElement('canvas');
  scorchCanvas.width = 256;
  scorchCanvas.height = 256;
  const sc = scorchCanvas.getContext('2d');
  const sGrad = sc.createRadialGradient(128, 175, 12, 128, 115, 115);
  sGrad.addColorStop(0, 'rgba(20, 20, 22, 0.85)');
  sGrad.addColorStop(0.55, 'rgba(38, 36, 34, 0.45)');
  sGrad.addColorStop(1, 'rgba(38, 36, 34, 0.0)');
  sc.fillStyle = sGrad;
  sc.fillRect(0, 0, 256, 256);
  const scorchTex = new THREE.CanvasTexture(scorchCanvas);

  cachedMuralTextures = {
    eastMuralTex,
    yellowTulipTex,
    pencilGateTex,
    porticoColTex,
    dinoWallTex,
    eastTreeMuralTex,
    scorchTex
  };
  return cachedMuralTextures;
}

// --- TERRAIN, 3 WALLED COURTYARDS, 90°-ALIGNED ASSEMBLY LINES, STRIPED SHED & VOW SHRINE ---
function buildEnvironmentAndTerrain() {
  const murals = getSchoolMuralTextures();

  // Outer surroundings plane
  const groundGeo = new THREE.PlaneGeometry(190, 165, 16, 16);
  const groundMat = new THREE.MeshStandardMaterial({ color: 0x20242b, roughness: 0.92, metalness: 0.06 });
  const ground = new THREE.Mesh(groundGeo, groundMat);
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  terrainGroup.add(ground);

  // 1) SE Main Boys' Courtyard Asphalt (X: -8.4..+42.5, Z: +2.4..+30.0)
  const boysYard = new THREE.Mesh(
    new THREE.PlaneGeometry(50.9, 27.6),
    new THREE.MeshStandardMaterial({ color: 0x3b4049, roughness: 0.84 })
  );
  boysYard.rotation.x = -Math.PI / 2;
  boysYard.position.set(17.05, 0.02, 16.2);
  boysYard.receiveShadow = true;
  terrainGroup.add(boysYard);

  // 2) SW Girls' School Yard Surface (X: -34.0..-8.4, Z: -19.5..+30.0)
  const girlsYard = new THREE.Mesh(
    new THREE.PlaneGeometry(25.6, 49.5),
    new THREE.MeshStandardMaterial({ color: 0x464a42, roughness: 0.86 })
  );
  girlsYard.rotation.x = -Math.PI / 2;
  girlsYard.position.set(-21.2, 0.02, 5.25);
  girlsYard.receiveShadow = true;
  terrainGroup.add(girlsYard);

  // 3) NE Walled Pre-School Yard Surface (X: +19.0..+42.5, Z: -18.5..+2.4)
  const preSchoolYard = new THREE.Mesh(
    new THREE.PlaneGeometry(23.5, 20.9),
    new THREE.MeshStandardMaterial({ color: 0x4b5347, roughness: 0.86 })
  );
  preSchoolYard.rotation.x = -Math.PI / 2;
  preSchoolYard.position.set(30.75, 0.02, -8.05);
  preSchoolYard.receiveShadow = true;
  terrainGroup.add(preSchoolYard);

  // 4) NW Rear Staircase & Shade Alley (X: -19.0..+19.0, Z: -19.5..-12.8)
  const rearAlley = new THREE.Mesh(
    new THREE.PlaneGeometry(38.0, 6.8),
    new THREE.MeshStandardMaterial({ color: 0x353a42, roughness: 0.86 })
  );
  rearAlley.rotation.x = -Math.PI / 2;
  rearAlley.position.set(0, 0.02, -16.1);
  rearAlley.receiveShadow = true;
  terrainGroup.add(rearAlley);

  // ========================================================
  // VERIFIED COURTYARD MARKINGS (FA 01_reconstruction & Real Archive Footage)
  // Six Parallel Yellow Morning Assembly Lines running ALONG +X (parallel to front facade),
  // with 6 yellow standing circles on the -X (portico-facing) edge inside a green border!
  // ========================================================
  const assemblyGroup = new THREE.Group();
  assemblyGroup.name = "Courtyard_Assembly_Lines";
  assemblyGroup.position.set(16.5, 0.04, 8.25);

  const greenBorderMat = new THREE.MeshBasicMaterial({ color: 0x346747, side: THREE.DoubleSide });
  const yellowMarkMat = new THREE.MeshBasicMaterial({ color: 0xdccf4e, side: THREE.DoubleSide });

  const boxW = 14.8; // along X (x = 9.1..23.9)
  const boxD = 8.6;  // along Z (z = 3.95..12.55)
  const bNorth = new THREE.Mesh(new THREE.PlaneGeometry(boxW, 0.22), greenBorderMat);
  bNorth.rotation.x = -Math.PI / 2; bNorth.position.set(0, 0, -boxD / 2);
  assemblyGroup.add(bNorth);
  const bSouth = new THREE.Mesh(new THREE.PlaneGeometry(boxW, 0.22), greenBorderMat);
  bSouth.rotation.x = -Math.PI / 2; bSouth.position.set(0, 0, boxD / 2);
  assemblyGroup.add(bSouth);
  const bWest = new THREE.Mesh(new THREE.PlaneGeometry(0.22, boxD), greenBorderMat);
  bWest.rotation.x = -Math.PI / 2; bWest.position.set(-boxW / 2, 0, 0);
  assemblyGroup.add(bWest);
  const bEast = new THREE.Mesh(new THREE.PlaneGeometry(0.22, boxD), greenBorderMat);
  bEast.rotation.x = -Math.PI / 2; bEast.position.set(boxW / 2, 0, 0);
  assemblyGroup.add(bEast);

  for (let i = 0; i < 6; i++) {
    const lz = -3.5 + i * 1.40;
    const yLine = new THREE.Mesh(new THREE.PlaneGeometry(13.4, 0.19), yellowMarkMat);
    yLine.rotation.x = -Math.PI / 2;
    yLine.position.set(0.35, 0.005, lz);
    yLine.userData = { feature: 'assembly_yellow_line' };
    assemblyGroup.add(yLine);

    // Standing circle at the -X (portico-facing) head of each line
    const yDot = new THREE.Mesh(new THREE.CircleGeometry(0.30, 24), yellowMarkMat);
    yDot.rotation.x = -Math.PI / 2;
    yDot.position.set(-6.65, 0.006, lz);
    assemblyGroup.add(yDot);
  }
  terrainGroup.add(assemblyGroup);

  // SW Girls' Yard White Circular Play Marking with Inner Cross/Star
  const whiteLineMat = new THREE.MeshBasicMaterial({ color: 0xcbd5e1, side: THREE.DoubleSide });
  const playGroup = new THREE.Group();
  playGroup.position.set(-16.0, 0.04, 12.5);
  const playRing = new THREE.Mesh(new THREE.RingGeometry(2.75, 2.92, 40), whiteLineMat);
  playRing.rotation.x = -Math.PI / 2;
  playGroup.add(playRing);
  for (let a = 0; a < 4; a++) {
    const spoke = new THREE.Mesh(new THREE.PlaneGeometry(5.5, 0.11), whiteLineMat);
    spoke.rotation.x = -Math.PI / 2;
    spoke.rotation.z = (a * Math.PI) / 4;
    playGroup.add(spoke);
  }
  terrainGroup.add(playGroup);

  // SE White-Lined Mini Football Pitch + 2 Goalposts (X: 27.2..40.2, Z: 14.2..26.8)
  const pitchGroup = new THREE.Group();
  pitchGroup.position.set(33.7, 0.04, 20.5);
  pitchGroup.userData = { feature: 'football_pitch' };
  const pW = 12.6, pD = 12.2;
  [
    [pW, 0.12, 0, -pD / 2],
    [pW, 0.12, 0, pD / 2],
    [0.12, pD, -pW / 2, 0],
    [0.12, pD, pW / 2, 0],
    [pW, 0.10, 0, 0]
  ].forEach(([w, d, px, pz]) => {
    const ln = new THREE.Mesh(new THREE.PlaneGeometry(w, d), whiteLineMat);
    ln.rotation.x = -Math.PI / 2;
    ln.position.set(px, 0, pz);
    pitchGroup.add(ln);
  });
  const pitchCircle = new THREE.Mesh(new THREE.RingGeometry(1.65, 1.77, 32), whiteLineMat);
  pitchCircle.rotation.x = -Math.PI / 2;
  pitchGroup.add(pitchCircle);

  const goalMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.4, metalness: 0.4 });
  [-pD / 2, pD / 2].forEach((gz) => {
    const gPostL = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 1.85, 8), goalMat);
    gPostL.position.set(-1.35, 0.92, gz);
    const gPostR = gPostL.clone();
    gPostR.position.set(1.35, 0.92, gz);
    const gBar = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 2.75, 8), goalMat);
    gBar.rotation.z = Math.PI / 2;
    gBar.position.set(0, 1.85, gz);
    pitchGroup.add(gPostL, gPostR, gBar);
  });
  terrainGroup.add(pitchGroup);

  // Central White/Mint-Curbed Planted Tree Island (X: 5.2..24.5, Z: 15.2..26.8)
  const planterGroup = new THREE.Group();
  planterGroup.position.set(14.85, 0, 21.0);
  planterGroup.userData = { feature: 'curbed_tree_island' };
  const curbOuter = new THREE.Mesh(
    new THREE.BoxGeometry(19.2, 0.28, 11.4),
    new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.75 })
  );
  curbOuter.position.set(0, 0.14, 0);
  curbOuter.receiveShadow = true;
  planterGroup.add(curbOuter);

  const planterSoil = new THREE.Mesh(
    new THREE.BoxGeometry(18.5, 0.30, 10.7),
    new THREE.MeshStandardMaterial({ color: 0x3b4d3b, roughness: 0.95 })
  );
  planterSoil.position.set(0, 0.15, 0);
  planterSoil.receiveShadow = true;
  planterGroup.add(planterSoil);

  const trunkMat = new THREE.MeshStandardMaterial({ color: 0x5c4033, roughness: 0.9 });
  const canopyFoliageMat = new THREE.MeshStandardMaterial({ color: 0x3f6a49, roughness: 0.85 });
  [[-6.2, -2.5, 1.0], [0.8, -3.0, 1.15], [6.4, -0.5, 0.95], [-2.5, 3.0, 1.05]].forEach(([tx, tz, sc]) => {
    const tGrp = new THREE.Group();
    tGrp.position.set(tx, 0.28, tz);
    const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.18 * sc, 0.26 * sc, 2.2 * sc, 8), trunkMat);
    trunk.position.y = 1.1 * sc;
    trunk.castShadow = true;
    tGrp.add(trunk);
    const crown = new THREE.Mesh(new THREE.DodecahedronGeometry(1.55 * sc, 1), canopyFoliageMat);
    crown.position.y = 2.85 * sc;
    crown.scale.set(1.15, 0.82, 1.15);
    crown.castShadow = true;
    tGrp.add(crown);
    planterGroup.add(tGrp);
  });
  terrainGroup.add(planterGroup);

  // ========================================================
  // COURTYARD DIVIDING & PERIMETER WALLS
  // ========================================================
  const wallMat = new THREE.MeshStandardMaterial({ color: 0xe2e6ec, roughness: 0.85 });
  const wallH = 2.65;
  const wallT = 0.36;

  function addCourtyardWall(w, h, d, x, y, z, mat, featureTag, isSolid = true) {
    const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat || wallMat);
    m.position.set(x, y, z);
    m.castShadow = true;
    m.receiveShadow = true;
    m.userData = { isSolidWall: isSolid };
    if (featureTag) m.userData.feature = featureTag;
    terrainGroup.add(m);
    return m;
  }

  // 1. Co-Linear +X Pastel Dividing Wall (Z = +2.4, X = +19.0..+42.0) separating Boys' Yard & NE Pre-School Yard
  addCourtyardWall(23.0, wallH, wallT, 30.5, wallH / 2, 2.4, wallMat, 'plus_x_pastel_wall', true);
  const plusXPanelMats = [
    new THREE.MeshStandardMaterial({ map: murals.yellowTulipTex, roughness: 0.78 }),
    new THREE.MeshStandardMaterial({ color: 0x9ec4a5, roughness: 0.78 }),
    new THREE.MeshStandardMaterial({ color: 0xf1f5f9, roughness: 0.78 }),
    new THREE.MeshStandardMaterial({ color: 0x9ec4a5, roughness: 0.78 }),
    new THREE.MeshStandardMaterial({ color: 0xf1f5f9, roughness: 0.78 })
  ];
  for (let i = 0; i < 5; i++) {
    const px = 21.3 + i * 4.55;
    const panel = new THREE.Mesh(new THREE.BoxGeometry(4.35, 2.35, 0.06), plusXPanelMats[i]);
    panel.position.set(px, 1.25, 2.60);
    terrainGroup.add(panel);
  }

  // 2. NE Pre-School Yard Rear (-Z = -18.5) & East (+X = +42.5) Walls + Open Double Mint Gates
  addCourtyardWall(7.2, wallH, wallT, 22.6, wallH / 2, -18.5, wallMat, null, true);
  addCourtyardWall(12.1, wallH, wallT, 36.45, wallH / 2, -18.5, wallMat, null, true);
  const mintGateMat = new THREE.MeshStandardMaterial({ color: 0x9ec4a5, roughness: 0.55, metalness: 0.25 });
  const preGateL = new THREE.Mesh(new THREE.BoxGeometry(2.05, 2.45, 0.10), mintGateMat);
  preGateL.position.set(26.2, 1.25, -19.4);
  preGateL.rotation.y = Math.PI / 2.2;
  const preGateR = new THREE.Mesh(new THREE.BoxGeometry(2.05, 2.45, 0.10), mintGateMat);
  preGateR.position.set(30.4, 1.25, -19.4);
  preGateR.rotation.y = -Math.PI / 2.2;
  terrainGroup.add(preGateL, preGateR);
  addCourtyardWall(wallT, wallH, 20.9, 42.5, wallH / 2, -8.05, wallMat, null, true);

  // 3. Red & White Horizontally Striped 4-Door Washroom / Drinking-Fountain Shed at East end of +X wall (facing -X)
  const shedGroup = new THREE.Group();
  shedGroup.position.set(41.3, 0, 5.5);
  shedGroup.userData = { feature: 'striped_washroom_shed', isSolidWall: true };
  const shedRedMat = new THREE.MeshStandardMaterial({ color: 0xc23b2b, roughness: 0.72 });
  const shedWhiteMat = new THREE.MeshStandardMaterial({ color: 0xf1f5f9, roughness: 0.72 });
  const shedDarkDoor = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.8 });

  const shedBody = new THREE.Mesh(new THREE.BoxGeometry(2.4, 2.85, 6.1), shedRedMat);
  shedBody.position.set(0, 1.425, 0);
  shedBody.castShadow = true;
  shedBody.receiveShadow = true;
  shedBody.userData = { isSolidWall: true };
  shedGroup.add(shedBody);

  const shedRoof = new THREE.Mesh(new THREE.BoxGeometry(2.7, 0.30, 6.3), shedWhiteMat);
  shedRoof.position.set(-0.08, 2.98, 0);
  shedGroup.add(shedRoof);

  // Horizontal white stripes across -X front face
  [0.65, 1.45, 2.25].forEach((sy) => {
    const stripe = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.16, 6.12), shedWhiteMat);
    stripe.position.set(-1.21, sy, 0);
    shedGroup.add(stripe);
  });
  // 4 recessed doorways facing -X down the yellow assembly lines
  [-2.1, -0.7, 0.7, 2.1].forEach((dz) => {
    const doorRecess = new THREE.Mesh(new THREE.BoxGeometry(0.10, 2.05, 0.76), shedDarkDoor);
    doorRecess.position.set(-1.22, 1.05, dz);
    const doorFrame = new THREE.Mesh(new THREE.BoxGeometry(0.08, 2.18, 0.90), shedWhiteMat);
    doorFrame.position.set(-1.20, 1.10, dz);
    shedGroup.add(doorFrame, doorRecess);
  });
  terrainGroup.add(shedGroup);

  // 4. East Boys' Courtyard Perimeter Wall (X = +42.5, Z = +8.5..+30.0) with Sky-Blue, Mint & Tree-Mural Panels
  addCourtyardWall(wallT, wallH, 21.5, 42.5, wallH / 2, 19.25, wallMat, null, true);
  const eastPerimMats = [
    new THREE.MeshStandardMaterial({ color: 0x4b93b8, roughness: 0.78 }),
    new THREE.MeshStandardMaterial({ color: 0x8ec3b0, roughness: 0.78 }),
    new THREE.MeshStandardMaterial({ map: murals.eastTreeMuralTex, roughness: 0.78 }),
    new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.78 })
  ];
  for (let i = 0; i < 4; i++) {
    const ep = new THREE.Mesh(new THREE.BoxGeometry(0.06, 2.35, 4.9), eastPerimMats[i]);
    ep.position.set(42.28, 1.25, 11.4 + i * 5.1);
    terrainGroup.add(ep);
  }

  // 5. SW Girls' Yard Dividing Wall (X = -8.4, Z = +2.4..+30.0) + Concrete Entry Canopy (projecting into SW Girls' Yard)
  addCourtyardWall(wallT, wallH, 27.6, -8.4, wallH / 2, 16.2, wallMat, 'sw_girls_dividing_wall', true);
  const swCanopy = new THREE.Mesh(
    new THREE.BoxGeometry(3.2, 0.16, 3.2),
    new THREE.MeshStandardMaterial({ color: 0xdbe2ea, roughness: 0.75 })
  );
  swCanopy.position.set(-10.0, 2.72, 4.0);
  swCanopy.castShadow = true;
  terrainGroup.add(swCanopy);

  // 6. South Perimeter Wall (Z = +30.0) & Main Gate with Colored-Pencil Mural (X = -4.2..+1.0 open entrance)
  addCourtyardWall(29.8, wallH, wallT, -19.1, wallH / 2, 30.0, wallMat, null, true);
  addCourtyardWall(41.5, wallH, wallT, 21.75, wallH / 2, 30.0, wallMat, null, true);

  const pencilGatePanel = new THREE.Mesh(
    new THREE.BoxGeometry(3.6, 2.65, 0.44),
    new THREE.MeshStandardMaterial({ map: murals.pencilGateTex, roughness: 0.72 })
  );
  pencilGatePanel.position.set(2.8, 1.35, 30.0);
  pencilGatePanel.userData = { feature: 'pencil_main_gate', isSolidWall: true };
  terrainGroup.add(pencilGatePanel);

  // Y-shaped security light post atop main gate pier (pip01b_01)
  const poleMat = new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.5 });
  const gPole = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.95, 8), poleMat);
  gPole.position.set(1.25, 3.15, 30.0);
  terrainGroup.add(gPole);

  // 7. Outer West Wall (X = -34.0) & North-West Rear Alley Wall (Z = -19.5, X = -34.0..+19.0)
  addCourtyardWall(wallT, wallH, 49.5, -34.0, wallH / 2, 5.25, wallMat, null, true);
  addCourtyardWall(53.0, wallH, wallT, -7.5, wallH / 2, -19.5, wallMat, null, true);

  // ==========================================
  // CENTRAL ACCOUNTABILITY VOW SHRINE / OBELISK (Aligned on Central Portico & Gate Axis X = -1.5)
  // ==========================================
  const shrineX = -1.5;
  const shrineZ = 10.5;
  const shrinePedestal = new THREE.Mesh(
    new THREE.CylinderGeometry(1.85, 2.25, 0.42, 24),
    new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.4, metalness: 0.5 })
  );
  shrinePedestal.position.set(shrineX, 0.21, shrineZ);
  memorialBoardsGroup.add(shrinePedestal);

  const goldRing = new THREE.Mesh(
    new THREE.RingGeometry(1.95, 2.20, 32),
    new THREE.MeshBasicMaterial({ color: 0xd4a853, side: THREE.DoubleSide })
  );
  goldRing.rotation.x = -Math.PI / 2;
  goldRing.position.set(shrineX, 0.05, shrineZ);
  memorialBoardsGroup.add(goldRing);

  const obelisk = new THREE.Mesh(
    new THREE.CylinderGeometry(0.30, 0.58, 3.4, 8),
    new THREE.MeshStandardMaterial({
      color: 0xd4a853,
      emissive: 0xd4a853,
      emissiveIntensity: 0.28,
      metalness: 0.75,
      roughness: 0.25
    })
  );
  obelisk.position.set(shrineX, 2.1, shrineZ);
  obelisk.castShadow = true;
  memorialBoardsGroup.add(obelisk);
}

// --- IN-WORLD 3D CLASSROOM PORTRAITS (119 STUDENTS + 26 EDUCATORS) & 28 RUBBLE DRAWINGS ---
function createNameplateTexture(line1Fa, line2En, line3Meta, accentHex) {
  const canvas = document.createElement('canvas');
  canvas.width = 256;
  canvas.height = 76;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#0d1322';
  ctx.fillRect(0, 0, 256, 76);
  ctx.strokeStyle = accentHex || '#d4a853';
  ctx.lineWidth = 3;
  ctx.strokeRect(2, 2, 252, 72);

  ctx.textAlign = 'center';
  ctx.fillStyle = '#fef3c7';
  ctx.font = 'bold 17px Tahoma, sans-serif';
  ctx.fillText((line1Fa || line2En || '').slice(0, 26), 128, 25);

  ctx.fillStyle = '#e2e8f0';
  ctx.font = '600 13px Inter, sans-serif';
  ctx.fillText((line2En || '').slice(0, 28), 128, 46);

  ctx.fillStyle = accentHex || '#d4a853';
  ctx.font = 'bold 12px Inter, sans-serif';
  ctx.fillText((line3Meta || '').slice(0, 32), 128, 65);

  const tex = new THREE.CanvasTexture(canvas);
  tex.needsUpdate = true;
  return tex;
}

function createWingBannerIn3D(parentGroup, titleEn, titleFa, x, y, z, rotY, width, bgHex, borderHex) {
  const canvas = document.createElement('canvas');
  canvas.width = 768;
  canvas.height = 110;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = bgHex || 'rgba(13, 19, 34, 0.94)';
  ctx.fillRect(0, 0, 768, 110);
  ctx.strokeStyle = borderHex || '#d4a853';
  ctx.lineWidth = 5;
  ctx.strokeRect(3, 3, 762, 104);

  ctx.textAlign = 'center';
  ctx.fillStyle = '#fde68a';
  ctx.font = 'bold 26px Tahoma, sans-serif';
  ctx.fillText(titleFa, 384, 44);

  ctx.fillStyle = '#f8fafc';
  ctx.font = 'bold 20px Inter, sans-serif';
  ctx.fillText(titleEn, 384, 82);

  const tex = new THREE.CanvasTexture(canvas);
  const mat = new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide });
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(width, width * (110 / 768)), mat);
  mesh.position.set(x, y, z);
  mesh.rotation.y = rotY;
  parentGroup.add(mesh);
}

function create3DFramedPortraitOnWall(parentGroup, loader, item, x, y, z, rotY, frameW, frameH, borderHex, cutawayMode, wingLabel, focusDist) {
  const holder = new THREE.Group();
  holder.position.set(x, y, z);
  holder.rotation.y = rotY;

  const backing = new THREE.Mesh(
    new THREE.BoxGeometry(frameW, frameH, 0.04),
    new THREE.MeshBasicMaterial({ color: borderHex || 0xd4a853 })
  );
  holder.add(backing);

  const innerMat = new THREE.MeshBasicMaterial({ color: 0x1e293b, side: THREE.DoubleSide });
  const portraitH = frameH * 0.76;
  const portraitW = frameW * 0.90;
  const portraitPlane = new THREE.Mesh(new THREE.PlaneGeometry(portraitW, portraitH), innerMat);
  portraitPlane.position.set(0, frameH * 0.09, 0.026);
  holder.add(portraitPlane);

  const imgUrl = item.photoPath || item.photo_path || (item.photoGrid ? `images/children/child_${item.photoGrid}.jpg` : null);
  if (imgUrl) {
    loader.load(imgUrl, (tex) => {
      portraitPlane.material = new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide });
      portraitPlane.material.needsUpdate = true;
    });
  }

  const metaText = item.category === 'teacher'
    ? (item.role || 'Educator')
    : `Grade ${item.grade || '?'} · Age ${item.age || '?'}`;
  const labelTex = createNameplateTexture(
    item.nameFa || item.full_name_fa,
    item.name || item.full_name_en,
    metaText,
    borderHex === 0xf472b6 ? '#f472b6' : '#d4a853'
  );
  const labelPlane = new THREE.Mesh(
    new THREE.PlaneGeometry(portraitW, frameH * 0.20),
    new THREE.MeshBasicMaterial({ map: labelTex, side: THREE.DoubleSide })
  );
  labelPlane.position.set(0, -frameH * 0.38, 0.026);
  holder.add(labelPlane);

  const dist = typeof focusDist === 'number' ? focusDist : 1.85;
  const normal = new THREE.Vector3(0, 0, 1).applyAxisAngle(new THREE.Vector3(0, 1, 0), rotY);
  const focusCam = new THREE.Vector3(x, y + 0.08, z).add(normal.clone().multiplyScalar(dist));
  const lookAt = new THREE.Vector3(x, y, z);

  const artifactData = {
    artifactType: 'victim',
    item,
    wingLabel: wingLabel || 'Reconstructed School Interior',
    focusCam,
    lookAt,
    cutawayMode: typeof cutawayMode === 'number' ? cutawayMode : 2
  };
  portraitPlane.userData = artifactData;
  backing.userData = artifactData;
  labelPlane.userData = artifactData;
  clickable3DArtifacts.push(portraitPlane, backing, labelPlane);

  parentGroup.add(holder);
}

function create3DRubbleDrawingOnWall(parentGroup, loader, drw, x, y, z, rotY, frameW, frameH, cutawayMode, wingLabel, focusDist) {
  const holder = new THREE.Group();
  holder.position.set(x, y, z);
  holder.rotation.y = rotY;

  const borderColor = drw.hasBlastDamage ? 0xef4444 : 0xd4a853;
  const backing = new THREE.Mesh(
    new THREE.BoxGeometry(frameW, frameH, 0.04),
    new THREE.MeshBasicMaterial({ color: borderColor })
  );
  holder.add(backing);

  const imgH = frameH * 0.76;
  const imgW = frameW * 0.91;
  const artPlane = new THREE.Mesh(
    new THREE.PlaneGeometry(imgW, imgH),
    new THREE.MeshBasicMaterial({ color: 0x1e293b, side: THREE.DoubleSide })
  );
  artPlane.position.set(0, frameH * 0.09, 0.026);
  holder.add(artPlane);

  loader.load(drw.thumb || drw.image, (tex) => {
    artPlane.material = new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide });
    artPlane.material.needsUpdate = true;
  });

  const labelTex = createNameplateTexture(
    drw.studentNameFa || 'نقاشی زیر آوار',
    (drw.title && drw.title.en) ? drw.title.en : drw.id,
    drw.dateOnPage || 'Rubble Artifact',
    drw.hasBlastDamage ? '#f87171' : '#fcd34d'
  );
  const labelPlane = new THREE.Mesh(
    new THREE.PlaneGeometry(imgW, frameH * 0.20),
    new THREE.MeshBasicMaterial({ map: labelTex, side: THREE.DoubleSide })
  );
  labelPlane.position.set(0, -frameH * 0.38, 0.026);
  holder.add(labelPlane);

  const dist = typeof focusDist === 'number' ? focusDist : 1.95;
  const normal = new THREE.Vector3(0, 0, 1).applyAxisAngle(new THREE.Vector3(0, 1, 0), rotY);
  const focusCam = new THREE.Vector3(x, y + 0.08, z).add(normal.clone().multiplyScalar(dist));
  const lookAt = new THREE.Vector3(x, y, z);

  const artifactData = {
    artifactType: 'drawing',
    item: drw,
    wingLabel: wingLabel || 'Classroom Rubble Artifact',
    focusCam,
    lookAt,
    cutawayMode: typeof cutawayMode === 'number' ? cutawayMode : 1
  };
  artPlane.userData = artifactData;
  backing.userData = artifactData;
  labelPlane.userData = artifactData;
  clickable3DArtifacts.push(artPlane, backing, labelPlane);

  parentGroup.add(holder);
}

function createClassroomDeskWithDrawing(parentGroup, loader, drw, x, yBase, z, cutawayMode) {
  const deskGroup = new THREE.Group();
  deskGroup.position.set(x, yBase, z);
  deskGroup.userData = { feature: 'classroom_desk' };

  const woodMat = new THREE.MeshStandardMaterial({ color: 0x8b5a2b, roughness: 0.75 });
  const frameMetalMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.55, metalness: 0.4 });

  const top = new THREE.Mesh(new THREE.BoxGeometry(1.12, 0.05, 0.58), woodMat);
  top.position.set(0, 0.68, 0);
  top.castShadow = true;
  deskGroup.add(top);

  // 4 Desk Frame Legs + Book Shelf
  [[-0.50, -0.23], [0.50, -0.23], [-0.50, 0.23], [0.50, 0.23]].forEach(([lx, lz]) => {
    const leg = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.66, 0.045), frameMetalMat);
    leg.position.set(lx, 0.33, lz);
    leg.castShadow = true;
    deskGroup.add(leg);
  });

  const bench = new THREE.Mesh(new THREE.BoxGeometry(1.12, 0.045, 0.32), woodMat);
  bench.position.set(0, 0.40, 0.50);
  bench.castShadow = true;
  deskGroup.add(bench);

  // 2 Bench Legs + Stretcher
  [-0.48, 0.48].forEach((bx) => {
    const bLeg = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.39, 0.28), frameMetalMat);
    bLeg.position.set(bx, 0.195, 0.50);
    deskGroup.add(bLeg);
  });

  if (drw) {
    const sheet = new THREE.Mesh(
      new THREE.PlaneGeometry(0.46, 0.34),
      new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide })
    );
    sheet.rotation.x = -Math.PI / 2;
    sheet.position.set(0, 0.712, 0);
    deskGroup.add(sheet);

    loader.load(drw.thumb || drw.image, (tex) => {
      sheet.material = new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide });
      sheet.material.needsUpdate = true;
    });

    const artifactData = {
      artifactType: 'drawing',
      item: drw,
      wingLabel: 'Ground Floor Classroom Desk (Recovered from Rubble)',
      focusCam: new THREE.Vector3(x, yBase + 1.75, z + 1.25),
      lookAt: new THREE.Vector3(x, yBase + 0.7, z),
      cutawayMode: cutawayMode || 2
    };
    sheet.userData = artifactData;
    clickable3DArtifacts.push(sheet);
  }

  parentGroup.add(deskGroup);
}

function populate3DSchoolPortraitsAndDrawings() {
  const loader = new THREE.TextureLoader();
  clickable3DArtifacts = [];

  // 1. COURTYARD MEMORIAL AVENUE (24 Double-Sided Steles flanking the Central Vow Shrine Walk at X = -5.2 & X = +2.2)
  const portraitSample = childrenList.filter(c => c.photoPath).slice(0, 24);
  portraitSample.forEach((child, idx) => {
    const isLeft = idx < 12;
    const slot = isLeft ? idx : idx - 12;
    const x = isLeft ? -5.2 : 2.2;
    const z = 13.0 + slot * 1.20;
    const rotY = isLeft ? Math.PI / 2 : -Math.PI / 2;
    const imgUrl = child.photoPath;

    const post = new THREE.Mesh(
      new THREE.BoxGeometry(0.96, 1.88, 0.10),
      new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.5 })
    );
    post.position.set(x, 1.08, z);
    post.rotation.y = rotY;
    post.castShadow = true;
    memorialBoardsGroup.add(post);

    const border = new THREE.Mesh(
      new THREE.BoxGeometry(1.02, 1.94, 0.07),
      new THREE.MeshBasicMaterial({ color: 0xd4a853 })
    );
    post.add(border);

    const labelTex = createNameplateTexture(
      child.nameFa,
      child.name,
      `Grade ${child.grade || '?'} · Age ${child.age || '?'}`,
      '#d4a853'
    );
    const frontLabel = new THREE.Mesh(
      new THREE.PlaneGeometry(0.88, 0.30),
      new THREE.MeshBasicMaterial({ map: labelTex, side: THREE.DoubleSide })
    );
    frontLabel.position.set(0, -0.68, 0.065);
    post.add(frontLabel);

    const backLabel = frontLabel.clone();
    backLabel.position.set(0, -0.68, -0.065);
    backLabel.rotation.y = Math.PI;
    post.add(backLabel);

    const steleArtifact = {
      artifactType: 'victim',
      item: child,
      wingLabel: 'Courtyard 100 Faces Memorial Walk',
      focusCam: new THREE.Vector3(-1.5, 1.45, z),
      lookAt: new THREE.Vector3(x, 1.15, z),
      cutawayMode: 0
    };
    post.userData = steleArtifact;
    clickable3DArtifacts.push(post);

    if (imgUrl) {
      loader.load(imgUrl, (tex) => {
        const portraitMesh = new THREE.Mesh(
          new THREE.PlaneGeometry(0.88, 1.32),
          new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide })
        );
        portraitMesh.position.set(0, 0.18, 0.065);
        portraitMesh.userData = steleArtifact;
        post.add(portraitMesh);
        clickable3DArtifacts.push(portraitMesh);

        const backMesh = portraitMesh.clone();
        backMesh.position.set(0, 0.18, -0.065);
        backMesh.rotation.y = Math.PI;
        backMesh.userData = steleArtifact;
        post.add(backMesh);
        clickable3DArtifacts.push(backMesh);
      });
    }
  });

  if (!groundFloorGroup || !firstFloorGroup) return;

  // =========================================================================
  // 2. GROUND FLOOR WEST WING: BOYS OF GRADES 1, 2 & 3 (55 BOYS ON PARTITION-SAFE WALLS)
  // =========================================================================
  const boysGrades1to3 = childrenList.filter(c => c.gender === 'boy' && (c.grade || 1) <= 3 && c.photoPath);
  createWingBannerIn3D(
    groundFloorGroup,
    `GROUND FLOOR WEST CLASSROOMS · BOYS GRADES 1–3 (${boysGrades1to3.length} STUDENTS)`,
    `کلاس‌های طبقه همکف (بال غربی) · ۵۵ دانش‌آموز پسر پایه‌های اول تا سوم`,
    -15.8, 3.25, -2.30, 0, 5.8, '#0d1b2a', '#38bdf8'
  );

  let bIdx = 0;
  // A) Mid-West Classroom North & South Interior Partitions (X: -18.3..-13.3, Z = -7.38 facing +Z & Z = -2.72 facing -Z): 24 portraits
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 6; col++) {
      if (bIdx >= boysGrades1to3.length) break;
      const px = -18.1 + col * 0.94;
      const py = 1.22 + row * 1.12;
      create3DFramedPortraitOnWall(
        groundFloorGroup, loader, boysGrades1to3[bIdx++],
        px, py, -7.38, 0, 0.80, 0.98, 0x38bdf8, 2,
        'Ground Floor West Wing · Boys Classrooms (Grades 1–3)', 1.75
      );
    }
  }
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 6; col++) {
      if (bIdx >= boysGrades1to3.length) break;
      const px = -18.1 + col * 0.94;
      const py = 1.22 + row * 1.12;
      create3DFramedPortraitOnWall(
        groundFloorGroup, loader, boysGrades1to3[bIdx++],
        px, py, -2.72, Math.PI, 0.80, 0.98, 0x38bdf8, 2,
        'Ground Floor West Wing · Boys Classrooms (Grades 1–3)', 1.75
      );
    }
  }
  // B) SW Singing Boys' Classroom North Partition (Z = -2.28 facing +Z, X: -18.1..-13.4): 12 portraits
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 6; col++) {
      if (bIdx >= boysGrades1to3.length) break;
      const px = -18.1 + col * 0.94;
      const py = 1.22 + row * 1.12;
      create3DFramedPortraitOnWall(
        groundFloorGroup, loader, boysGrades1to3[bIdx++],
        px, py, -2.28, 0, 0.80, 0.98, 0x38bdf8, 2,
        'Ground Floor South-West Classroom · Boys Grades 1–2', 1.75
      );
    }
  }
  // C) NW Classroom North Wall (Z = -12.72 facing +Z, X: -18.1..-13.4) & South-Inner Classroom Wall (X = -6.72 facing -X): remaining 19 portraits
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 6; col++) {
      if (bIdx >= boysGrades1to3.length) break;
      const px = -18.1 + col * 0.94;
      const py = 1.22 + row * 1.12;
      create3DFramedPortraitOnWall(
        groundFloorGroup, loader, boysGrades1to3[bIdx++],
        px, py, -12.72, 0, 0.80, 0.98, 0x38bdf8, 2,
        'Ground Floor North-West Classroom · Boys Grades 1–3', 1.75
      );
    }
  }
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 6; col++) {
      if (bIdx >= boysGrades1to3.length) break;
      const pz = -5.0 + col * 1.12;
      const py = 1.22 + row * 1.12;
      create3DFramedPortraitOnWall(
        groundFloorGroup, loader, boysGrades1to3[bIdx++],
        -6.72, py, pz, -Math.PI / 2, 0.80, 0.98, 0x38bdf8, 2,
        'Ground Floor South-Inner Classroom · Boys Grades 2–3', 1.65
      );
    }
  }

  // Add 6 Legged Classroom Desks with 1st-Grade Rubble Drawings inside Mid-West Classroom (X: -18.8..-12.8, Z: -7.4..-2.7)
  const groundDeskDrawings = drawingsList.slice(0, 6);
  for (let d = 0; d < 6; d++) {
    const dx = -17.3 + (d % 3) * 1.65;
    const dz = -5.9 + Math.floor(d / 3) * 1.85;
    createClassroomDeskWithDrawing(groundFloorGroup, loader, groundDeskDrawings[d], dx, 0.2, dz, 2);
  }

  // =========================================================================
  // 3. GROUND FLOOR EAST WING: BOYS OF GRADES 4, 5 & 6 (17 BOYS IN CEREMONY & EAST ROOMS)
  // =========================================================================
  const boysGrades4to6 = childrenList.filter(c => c.gender === 'boy' && (c.grade || 1) >= 4 && c.photoPath);
  createWingBannerIn3D(
    groundFloorGroup,
    `GROUND FLOOR EAST WING · BOYS GRADES 4–6 & CEREMONY ROOM (${boysGrades4to6.length} STUDENTS)`,
    `طبقه همکف (بال شرقی) · دانش‌آموزان پسر پایه‌های چهارم تا ششم و اتاق جشن`,
    3.75, 3.25, -8.18, 0, 6.4, '#0d1b2a', '#d4a853'
  );

  let b4Idx = 0;
  // Mount along South & East Interior Partitions of Ceremony Room (X: 0.6..6.8, Z = -3.82 facing -Z) & SE Classroom Partition (Z = -2.98 facing +Z)
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 6; col++) {
      if (b4Idx >= boysGrades4to6.length) break;
      const px = 0.95 + col * 1.05;
      const py = 1.22 + row * 1.12;
      create3DFramedPortraitOnWall(
        groundFloorGroup, loader, boysGrades4to6[b4Idx++],
        px, py, -3.82, Math.PI, 0.84, 1.02, 0xd4a853, 2,
        'Ground Floor East Wing · Boys Grades 4–6 & Ceremony Room', 1.75
      );
    }
  }
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 5; col++) {
      if (b4Idx >= boysGrades4to6.length) break;
      const px = 12.2 + col * 1.25;
      const py = 1.22 + row * 1.12;
      create3DFramedPortraitOnWall(
        groundFloorGroup, loader, boysGrades4to6[b4Idx++],
        px, py, -2.98, 0, 0.84, 1.02, 0xd4a853, 2,
        'Ground Floor East Wing · Boys Grades 4–6 Classroom', 1.75
      );
    }
  }

  // =========================================================================
  // 4. CENTRAL HALL & RAINBOW STAIRCASE: ALL 26 MARTYRED FEMALE EDUCATORS
  // =========================================================================
  createWingBannerIn3D(
    groundFloorGroup,
    `CENTRAL HALL & RAINBOW STAIRCASE · THE 26 MARTYRED FEMALE EDUCATORS`,
    `سالن مرکزی و راه‌پله رنگین‌کمان · ۲۶ معلم و مدیر شهیده دبستان شجره طیبه`,
    -1.9, 3.30, -8.02, 0, 5.6, '#1f122b', '#f472b6'
  );

  // Mount 13 educators on West Central Hall walls (X = -6.28, Z = -3.9..-7.6 & X = -3.38, Z = -0.3..-2.9)
  // and 13 educators on East Central Hall wall (X = -0.18, Z = -0.2..-7.5), avoiding all purple doors
  const leftHallSlots = [
    [-3.38, -0.5], [-3.38, -1.5], [-3.38, -2.5],
    [-6.28, -4.1], [-6.28, -5.1], [-6.28, -6.1], [-6.28, -7.2]
  ];
  const rightHallZ = [-0.4, -1.45, -2.5, -4.4, -5.45, -6.5, -7.45];

  teachersList.forEach((teacher, idx) => {
    const isLeft = idx < 13;
    const localIdx = isLeft ? idx : idx - 13;
    const row = Math.floor(localIdx / 7);
    const col = localIdx % 7;
    const py = 1.22 + row * 1.12;
    if (isLeft) {
      const [lx, lz] = leftHallSlots[col] || [-6.28, -4.5];
      create3DFramedPortraitOnWall(
        groundFloorGroup, loader, teacher,
        lx, py, lz, Math.PI / 2, 0.82, 0.98, 0xf472b6, 2,
        'Central Assembly Hall & Rainbow Staircase · 26 Martyred Female Educators', 1.55
      );
    } else {
      const rz = rightHallZ[col] || -4.5;
      create3DFramedPortraitOnWall(
        groundFloorGroup, loader, teacher,
        -0.18, py, rz, -Math.PI / 2, 0.82, 0.98, 0xf472b6, 2,
        'Central Assembly Hall & Rainbow Staircase · 26 Martyred Female Educators', 1.55
      );
    }
  });

  // =========================================================================
  // 5. FIRST FLOOR WEST GIRLS' ASSEMBLY HALL: ALL 47 MARTYRED SCHOOLGIRLS (X: -19.0..-11.5, Z: +2.4..-13.0)
  // =========================================================================
  const y1 = 3.6;
  const girlsAll = childrenList.filter(c => c.gender === 'girl' && c.photoPath);
  createWingBannerIn3D(
    firstFloorGroup,
    `FIRST FLOOR GIRLS' ASSEMBLY HALL · ALL ${girlsAll.length} MARTYRED SCHOOLGIRLS (GRADES 1–6)`,
    `طبقه اول (سالن بزرگ دختران) · ۴۷ دانش‌آموز دختر شهیده در پایه‌های اول تا ششم`,
    -15.25, y1 + 3.22, -12.70, 0, 6.8, '#2b1222', '#f472b6'
  );

  let gIdx = 0;
  // East Hall Partition (X = -11.72 facing -X into Hall, avoiding pink double doors at Z = -5.8): 10 slots x 2 rows = 20 portraits
  const girlsEastZ = [-12.0, -10.9, -9.8, -8.7, -7.6, -3.9, -2.8, -1.7, -0.6, 0.6, 1.6];
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < girlsEastZ.length; col++) {
      if (gIdx >= girlsAll.length) break;
      create3DFramedPortraitOnWall(
        firstFloorGroup, loader, girlsAll[gIdx++],
        -11.72, y1 + 1.22 + row * 1.12, girlsEastZ[col], -Math.PI / 2, 0.82, 0.98, 0xf472b6, 1,
        'First Floor West Wing · Girls\' Assembly Hall (Grades 1–6)', 2.1
      );
    }
  }
  // West Wall window-free bays (X = -18.72 facing +X, Z = -9.6..-4.4 & -1.8..0.0) + North/South walls below high slits: remaining 25 portraits
  const girlsWestZ = [-9.6, -8.6, -6.9, -5.9, -4.9, -1.6, -0.6];
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < girlsWestZ.length; col++) {
      if (gIdx >= girlsAll.length) break;
      create3DFramedPortraitOnWall(
        firstFloorGroup, loader, girlsAll[gIdx++],
        -18.72, y1 + 1.22 + row * 1.12, girlsWestZ[col], Math.PI / 2, 0.82, 0.98, 0xf472b6, 1,
        'First Floor West Wing · Girls\' Assembly Hall (Grades 1–6)', 2.1
      );
    }
  }
  for (let col = 0; col < 6; col++) {
    if (gIdx >= girlsAll.length) break;
    create3DFramedPortraitOnWall(
      firstFloorGroup, loader, girlsAll[gIdx++],
      -17.8 + col * 1.05, y1 + 1.15, -12.72, 0, 0.82, 0.96, 0xf472b6, 1,
      'First Floor Girls\' Hall · North Wall Gallery', 2.1
    );
  }
  for (let col = 0; col < 6; col++) {
    if (gIdx >= girlsAll.length) break;
    create3DFramedPortraitOnWall(
      firstFloorGroup, loader, girlsAll[gIdx++],
      -17.8 + col * 1.05, y1 + 1.15, 2.12, Math.PI, 0.82, 0.96, 0xf472b6, 1,
      'First Floor Girls\' Hall · South Wall Gallery', 2.1
    );
  }

  // =========================================================================
  // 6. FIRST FLOOR NE CLASSROOM: ALL 28 DRAWINGS & HOMEWORK PULLED FROM RUBBLE (X: +8.5..+19.0, Z: -7.4..-13.0)
  // =========================================================================
  createWingBannerIn3D(
    firstFloorGroup,
    `FIRST FLOOR CLASSROOMS · 28 DRAWINGS & HOMEWORK PULLED FROM THE RUBBLE`,
    `کلاس‌های طبقه اول · ۲۸ برگ نقاشی و مشق بیرون کشیده شده از زیر آوار مدرسه`,
    13.75, y1 + 3.22, -7.64, Math.PI, 7.4, '#1e1b18', '#fcd34d'
  );

  let dIdx = 0;
  // South Partition of NE Archive Classroom (Z = -7.64 facing -Z into NE room, X = 9.3..18.1): 2 rows x 9 cols = 18 drawings
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 9; col++) {
      if (dIdx >= drawingsList.length) break;
      const dx = 9.35 + col * 1.06;
      const dy = y1 + 1.18 + row * 1.08;
      create3DRubbleDrawingOnWall(
        firstFloorGroup, loader, drawingsList[dIdx++],
        dx, dy, -7.64, Math.PI, 0.92, 0.98, 1,
        'First Floor North-East Classroom · Rubble Drawings & Homework Archive', 1.95
      );
    }
  }
  // West Partition of NE Archive Classroom (X = +8.72 facing +X into NE room, Z = -8.2..-12.2): 2 rows x 5 cols = 10 drawings
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 5; col++) {
      if (dIdx >= drawingsList.length) break;
      const dz = -8.25 - col * 0.96;
      const dy = y1 + 1.18 + row * 1.08;
      create3DRubbleDrawingOnWall(
        firstFloorGroup, loader, drawingsList[dIdx++],
        8.72, dy, dz, Math.PI / 2, 0.86, 0.98, 1,
        'First Floor North-East Classroom · Rubble Drawings & Homework Archive', 1.95
      );
    }
  }
}

function loadChildrenAndBuildInWorldMemorial() {
  if (typeof CHILDREN !== 'undefined' && Array.isArray(CHILDREN) && CHILDREN.length > 0) {
    childrenList = CHILDREN;
    teachersList = (typeof TEACHERS !== 'undefined' && Array.isArray(TEACHERS)) ? TEACHERS : [];
    drawingsList = (typeof DRAWINGS !== 'undefined' && Array.isArray(DRAWINGS)) ? DRAWINGS : [];
    populate3DSchoolPortraitsAndDrawings();
    return;
  }

  fetch('children.json')
    .then(r => r.json())
    .then(data => {
      childrenList = data.map(c => ({
        ...c,
        name: c.name || c.full_name_en,
        nameFa: c.nameFa || c.full_name_fa,
        photoPath: c.photoPath || c.photo_path || (c.photoGrid ? `images/children/child_${c.photoGrid}.jpg` : null)
      }));
      populate3DSchoolPortraitsAndDrawings();
    })
    .catch(err => console.warn('Could not load children.json for 3D frames:', err));
}

// --- 3D INTERACTIVE RAYCASTER FOR IN-ROOM PORTRAITS & RUBBLE DRAWINGS ---
function init3DPortraitRaycaster() {
  raycaster = new THREE.Raycaster();
  pointerNDC = new THREE.Vector2();
  const dom = renderer.domElement;

  dom.addEventListener('pointerdown', (e) => {
    pointerDownPos.x = e.clientX;
    pointerDownPos.y = e.clientY;
  });

  dom.addEventListener('pointermove', (e) => {
    if (clickable3DArtifacts.length === 0) return;
    const rect = dom.getBoundingClientRect();
    pointerNDC.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    pointerNDC.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(pointerNDC, camera);
    const hits = raycaster.intersectObjects(clickable3DArtifacts, false);
    dom.style.cursor = (hits.length > 0 && hits[0].object.visible) ? 'pointer' : 'grab';
  });

  dom.addEventListener('pointerup', (e) => {
    const dist = Math.hypot(e.clientX - pointerDownPos.x, e.clientY - pointerDownPos.y);
    if (dist > 6 || clickable3DArtifacts.length === 0) return;

    const rect = dom.getBoundingClientRect();
    pointerNDC.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    pointerNDC.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(pointerNDC, camera);

    const hits = raycaster.intersectObjects(clickable3DArtifacts, false);
    if (hits.length > 0) {
      const hitObj = hits[0].object;
      if (hitObj.userData && hitObj.userData.item) {
        openArtifactInspector(hitObj.userData);
      }
    }
  });
}

function openArtifactInspector(artifactData) {
  const modal = document.getElementById('artifactInspectorModal');
  if (!modal || !artifactData || !artifactData.item) return;

  const isFa = currentLang === 'fa';
  const isFi = currentLang === 'fi';
  const item = artifactData.item;
  const imgEl = document.getElementById('inspectorImg');
  const titleEl = document.getElementById('inspectorTitle');
  const subEl = document.getElementById('inspectorSubtitle');
  const badgeEl = document.getElementById('inspectorBadge');
  const metaGrid = document.getElementById('inspectorMetaGrid');
  const descEl = document.getElementById('inspectorDesc');
  const primaryLink = document.getElementById('inspectorPrimaryLink');
  const focusBtn = document.getElementById('inspectorFocus3DBtn');

  if (artifactData.artifactType === 'drawing') {
    badgeEl.textContent = item.hasBlastDamage
      ? (isFa ? '💥 سند فیزیکی سوراخ‌شده با ترکش در زیر آوار' : '💥 Shrapnel-Torn Rubble Classroom Artifact')
      : (isFa ? '🎨 نقاشی و تکلیف بیرون کشیده شده از زیر آوار' : '🎨 Classroom Drawing Pulled from the Rubble');
    imgEl.src = item.image || item.thumb;
    titleEl.textContent = (item.title && item.title[currentLang]) || (item.title && item.title.en) || item.id;
    subEl.textContent = isFa
      ? `${item.studentNameFa || 'دانش‌آموز دبستان شجره طیبه'} · ${item.dateOnPage || ''}`
      : `${item.studentNameEn || 'Elementary Student'} · ${item.dateOnPage || ''}`;

    metaGrid.innerHTML = `
      <div class="inspector-meta-pill">
        <span class="lbl">${isFa ? 'دانش‌آموز' : 'Student / Author'}</span>
        <span class="val">${isFa ? (item.studentNameFa || '—') : (item.studentNameEn || '—')}</span>
      </div>
      <div class="inspector-meta-pill">
        <span class="lbl">${isFa ? 'تاریخ روی برگه' : 'Date on Sheet'}</span>
        <span class="val">${item.dateOnPage || 'Winter 1404'}</span>
      </div>
      <div class="inspector-meta-pill" style="grid-column: span 2;">
        <span class="lbl">${isFa ? 'دست‌خط روی برگه' : 'Original Persian Inscription'}</span>
        <span class="val" dir="rtl">${item.transcriptionFa || '—'}</span>
      </div>
    `;
    descEl.textContent = (item.translation && item.translation[currentLang]) || (item.translation && item.translation.en) || '';
    if (item.studentId) {
      primaryLink.href = `child.html?id=${encodeURIComponent(item.studentId)}`;
      primaryLink.textContent = isFa ? 'مشاهده صفحه یادبود این دانش‌آموز ←' : 'Open Student\'s Memorial Profile →';
    } else {
      primaryLink.href = 'memorial.html#drawingsSection';
      primaryLink.textContent = isFa ? 'مشاهده ۲۸ نقاشی زیر آوار در صفحه یادبود ←' : 'View All 28 Rubble Drawings →';
    }
  } else {
    const isTeacher = item.category === 'teacher';
    badgeEl.textContent = isTeacher
      ? (isFa ? '👩‍🏫 آموزگار و کادر آموزشی شهیده (نسخه ۳.۰)' : '👩‍🏫 Martyred Female Educator (Dataset v3.0.0)')
      : (isFa ? '🧒 دانش‌آموز شهید دبستان شجره طیبه (نسخه ۳.۰)' : '🧒 Martyred Schoolchild (Dataset v3.0.0)');
    imgEl.src = item.photoPath || item.photo_path || 'images/children/amin-ahmadzade.jpg';
    const primaryName = isFa ? (item.nameFa || item.name) : (item.name || item.nameFa);
    const secondaryName = isFa ? (item.name || '') : (item.nameFa || '');
    titleEl.textContent = secondaryName ? `${primaryName} (${secondaryName})` : primaryName;
    subEl.textContent = artifactData.wingLabel || (isFa ? (item.roleFa || item.gradeLabelFa) : (item.role || item.gradeLabelEn));

    const dobDisplay = item.birthDateShamsi
      ? `${item.birthDateShamsi}${item.birthDateGregorian ? ' (' + item.birthDateGregorian + ')' : ''}`
      : (isTeacher ? (isFa ? 'کادر آموزشی مدرسه' : 'School Faculty') : '—');
    const gradeOrRole = isFa
      ? (item.gradeLabelFa || item.roleFa || 'دانش‌آموز')
      : (item.gradeLabelEn || item.role || 'Student');

    metaGrid.innerHTML = `
      <div class="inspector-meta-pill">
        <span class="lbl">${isFa ? 'پایه / سمت' : (isFi ? 'Luokka / Tehtävä' : 'Grade / Role')}</span>
        <span class="val">${gradeOrRole}</span>
      </div>
      <div class="inspector-meta-pill">
        <span class="lbl">${isFa ? 'سن در زمان شهادت' : (isFi ? 'Ikä' : 'Age')}</span>
        <span class="val">${item.age ? (isFa ? `${item.age} سال` : `${item.age} years old`) : (isTeacher ? (isFa ? 'فرهنگی شهیده' : 'Educator') : '—')}</span>
      </div>
      <div class="inspector-meta-pill">
        <span class="lbl">${isFa ? 'تاریخ تولد (شمسی / میلادی)' : 'Birth Date (Solar Hijri / Gregorian)'}</span>
        <span class="val">${dobDisplay}</span>
      </div>
      <div class="inspector-meta-pill">
        <span class="lbl">${isFa ? 'آرامگاه' : 'Burial Location'}</span>
        <span class="val">${item.burialLocation || 'Minab Martyrs\' Cemetery'}</span>
      </div>
    `;
    descEl.textContent = item.notes || item.biography || '';
    primaryLink.href = `child.html?id=${encodeURIComponent(item.id)}`;
    primaryLink.textContent = isFa
      ? 'مشاهده شناسنامه کامل و صفحه اختصاصی یادبود ←'
      : (isFi ? 'Avaa koko muistosivu →' : 'Open Full Memorial Profile →');
  }

  if (focusBtn) {
    if (artifactData.focusCam && artifactData.lookAt) {
      focusBtn.style.display = 'inline-flex';
      focusBtn.onclick = () => {
        closeArtifactInspector();
        closeModal();
        setTemporalCondition(0.0);
        document.getElementById('timelineSlider').value = 0.0;
        if (typeof artifactData.cutawayMode === 'number') {
          setCutawayMode(artifactData.cutawayMode);
        }
        triggerCameraAnimation(artifactData.focusCam.clone(), artifactData.lookAt.clone());
      };
    } else {
      focusBtn.style.display = 'none';
    }
  }

  modal.classList.add('visible');
}

function closeArtifactInspector() {
  const modal = document.getElementById('artifactInspectorModal');
  if (modal) modal.classList.remove('visible');
}

// --- VERIFIED TWO-FLOOR WALKABLE SCHOOL ARCHITECTURE (FA INVESTIGATION 121 & ARCHIVE FOOTAGE) ---
function buildProceduralSchoolModels() {
  groundFloorGroup = new THREE.Group();
  groundFloorGroup.name = "Ground_Floor_Boys_School";
  firstFloorGroup = new THREE.Group();
  firstFloorGroup.name = "First_Floor_Girls_School";
  roofGroup = new THREE.Group();
  roofGroup.name = "Roof_And_Parapet";

  preStrikeModelGroup.add(groundFloorGroup);
  preStrikeModelGroup.add(firstFloorGroup);
  preStrikeModelGroup.add(roofGroup);

  const floorH = 3.6;
  const murals = getSchoolMuralTextures();

  // Verified Materials from FA-121 Blueprints & On-Site Archive Photos
  const whiteWall = new THREE.MeshStandardMaterial({ color: 0xedeff2, roughness: 0.82 });
  const westGreyWall = new THREE.MeshStandardMaterial({ color: 0x9aa1aa, roughness: 0.84 });
  const floorGrey = new THREE.MeshStandardMaterial({ color: 0x9ca3af, roughness: 0.85 });
  const floorGreen = new THREE.MeshStandardMaterial({ color: 0x5c7a62, roughness: 0.80 });
  const floorBrown = new THREE.MeshStandardMaterial({ color: 0x9c7b56, roughness: 0.82 });
  const floorLilac = new THREE.MeshStandardMaterial({ color: 0xa5a1bd, roughness: 0.82 });
  const tealWall = new THREE.MeshStandardMaterial({ color: 0x4f8694, roughness: 0.76 });
  const rearTealExt = new THREE.MeshStandardMaterial({ color: 0x3b7687, roughness: 0.78 });
  const skyBlueWall = new THREE.MeshStandardMaterial({ color: 0x88b8cb, roughness: 0.76 });
  const mintGreenWall = new THREE.MeshStandardMaterial({ color: 0x9ec4a5, roughness: 0.76 });
  const yellowFacade = new THREE.MeshStandardMaterial({ color: 0xd8d278, roughness: 0.76 });
  const pinkWall = new THREE.MeshStandardMaterial({ color: 0xd4839d, roughness: 0.76 });
  const sageGreenWall = new THREE.MeshStandardMaterial({ color: 0x7fa382, roughness: 0.76 });
  const purpleDoorMat = new THREE.MeshStandardMaterial({ color: 0x8b4ca8, roughness: 0.50 });
  const pinkDoorMat = new THREE.MeshStandardMaterial({ color: 0xd16b97, roughness: 0.52 });
  const blueMetalMat = new THREE.MeshStandardMaterial({ color: 0x1d4ed8, roughness: 0.48, metalness: 0.25 });
  const terracottaStairMat = new THREE.MeshStandardMaterial({ color: 0xc98a86, roughness: 0.78 });
  const canopyGreenMat = new THREE.MeshStandardMaterial({ color: 0x7d9c78, roughness: 0.72 });
  const sunshadeMat = new THREE.MeshStandardMaterial({ color: 0xe2e6ec, roughness: 0.78 });
  const darkGlassMat = new THREE.MeshBasicMaterial({ color: 0x111827 });
  const porticoColMat = new THREE.MeshStandardMaterial({ map: murals.porticoColTex, roughness: 0.74 });
  const eastMuralMat = new THREE.MeshStandardMaterial({ map: murals.eastMuralTex, roughness: 0.76 });
  const dinoMuralMat = new THREE.MeshStandardMaterial({ map: murals.dinoWallTex, roughness: 0.78 });
  const brownDadoMat = new THREE.MeshStandardMaterial({ color: 0x78533a, roughness: 0.78 });

  // Solid structural/partition wall helper (tracked for camera collision audit)
  function addSolidWall(group, w, h, d, x, y, z, mat, extraData) {
    const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat || whiteWall);
    m.position.set(x, y, z);
    m.castShadow = true;
    m.receiveShadow = true;
    m.userData = Object.assign({ isSolidWall: true }, extraData || {});
    group.add(m);
    return m;
  }

  // Non-blocking slab, dado paint band, or trim helper
  function addSlabOrTrim(group, w, h, d, x, y, z, mat, extraData) {
    const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat || whiteWall);
    m.position.set(x, y, z);
    m.castShadow = true;
    m.receiveShadow = true;
    if (extraData) m.userData = extraData;
    group.add(m);
    return m;
  }

  // Two-tone classroom partition helper (Sage lower dado + Pink upper wall, matching FA-121 1st Floor)
  function addTwoToneWall(group, w, totalH, d, x, yBase, z, lowerMat, upperMat) {
    const dadoH = 1.45;
    const upperH = totalH - dadoH;
    addSolidWall(group, w, dadoH, d, x, yBase + dadoH / 2, z, lowerMat || sageGreenWall);
    addSolidWall(group, w, upperH, d, x, yBase + dadoH + upperH / 2, z, upperMat || pinkWall);
  }

  // Signature Purple Classroom Door + Dark Transom Window
  function addPurpleDoor(group, x, yBase, z, rotY) {
    const dGroup = new THREE.Group();
    dGroup.position.set(x, yBase, z);
    dGroup.rotation.y = rotY;
    const door = new THREE.Mesh(new THREE.BoxGeometry(1.06, 2.08, 0.28), purpleDoorMat);
    door.position.set(0, 1.04, 0);
    dGroup.add(door);
    const transom = new THREE.Mesh(new THREE.BoxGeometry(1.06, 0.50, 0.29), darkGlassMat);
    transom.position.set(0, 2.38, 0);
    dGroup.add(transom);
    group.add(dGroup);
  }

  // Recessed Dark-Glazed Exterior Window with White Mullions, Security Grille & Optional Sunshade Brow
  function addExteriorWindow(group, x, y, z, rotY, w, h, mullions, hasSunshade, depthOverride) {
    const winGroup = new THREE.Group();
    winGroup.position.set(x, y, z);
    winGroup.rotation.y = rotY;
    winGroup.userData = { feature: 'exterior_window' };

    const d = depthOverride || 0.44;
    const glass = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), darkGlassMat);
    winGroup.add(glass);

    const sill = new THREE.Mesh(new THREE.BoxGeometry(w + 0.14, 0.07, d + 0.05), sunshadeMat);
    sill.position.set(0, -h / 2 - 0.02, 0);
    winGroup.add(sill);

    const head = new THREE.Mesh(new THREE.BoxGeometry(w + 0.10, 0.06, d + 0.03), whiteWall);
    head.position.set(0, h / 2 + 0.02, 0);
    winGroup.add(head);

    const mCount = typeof mullions === 'number' ? mullions : 2;
    for (let i = 1; i <= mCount; i++) {
      const mx = -w / 2 + (w * i) / (mCount + 1);
      const bar = new THREE.Mesh(new THREE.BoxGeometry(0.055, h, d + 0.03), whiteWall);
      bar.position.set(mx, 0, 0);
      winGroup.add(bar);
    }

    if (h >= 0.9) {
      const transBar = new THREE.Mesh(new THREE.BoxGeometry(w, 0.045, d + 0.03), whiteWall);
      transBar.position.set(0, h * 0.18, 0);
      winGroup.add(transBar);
    }

    if (hasSunshade) {
      const brow = new THREE.Mesh(new THREE.BoxGeometry(w + 0.48, 0.10, 0.50), sunshadeMat);
      brow.position.set(0, h / 2 + 0.11, 0.24);
      brow.castShadow = true;
      winGroup.add(brow);
    }

    group.add(winGroup);
    return winGroup;
  }

  // =====================================================================
  // 1. GROUND FLOOR (BOYS' SCHOOL & PRE-SCHOOL — FA-121 Stepped Envelope)
  // West Wing: X [-19.0, -7.2], Z [-13.0, +2.4] (15.4m deep)
  // Central Recessed Bay: X [-7.2, +7.2], Z [-13.0, +0.5] (13.5m deep) + Portico to Z = +4.85
  // East Wing: X [+7.2, +19.0], Z [-13.0, +2.4] (15.4m deep)
  // =====================================================================
  addSlabOrTrim(groundFloorGroup, 11.8, 0.20, 15.4, -13.1, 0.10, -5.3, floorGrey);
  addSlabOrTrim(groundFloorGroup, 14.4, 0.20, 13.5, 0.0, 0.10, -6.25, floorGrey);
  addSlabOrTrim(groundFloorGroup, 14.4, 0.16, 4.35, 0.0, 0.08, 2.675, floorGrey);
  addSlabOrTrim(groundFloorGroup, 11.8, 0.20, 15.4, 13.1, 0.10, -5.3, floorGrey);

  // SW Singing Boys' Green Carpet Classroom Floor (X: -18.8..-12.7, Z: -2.4..+2.25)
  addSlabOrTrim(
    groundFloorGroup, 6.1, 0.03, 4.65, -15.75, 0.215, -0.075, floorGreen,
    { feature: 'sw_boys_green_carpet' }
  );
  // Ceremony Room Floor Accent (X: 0.1..+7.4, Z: -8.3..-3.7)
  addSlabOrTrim(groundFloorGroup, 7.2, 0.025, 4.5, 3.7, 0.212, -6.0, tealWall);

  const extT = 0.34;
  // South Facade — West Projecting Wing (Z = +2.4, X = -19.0..-7.2) + Step Return (X = -7.2, Z = +0.5..+2.4)
  addSolidWall(groundFloorGroup, 11.8, floorH, extT, -13.1, floorH / 2, 2.4, whiteWall);
  addSolidWall(groundFloorGroup, extT, floorH, 1.9, -7.2, floorH / 2, 1.45, whiteWall);
  addSlabOrTrim(groundFloorGroup, 11.84, 1.95, 0.06, -13.1, 0.98, 2.59, yellowFacade);
  addSlabOrTrim(groundFloorGroup, 0.06, 1.95, 1.92, -7.01, 0.98, 1.45, yellowFacade);

  // South Facade — Central Recessed Ground Wall (Z = +0.5, X = -7.2..+7.2, open doorway X = -2.3..+0.1)
  addSolidWall(
    groundFloorGroup, 4.9, floorH, extT, -4.75, floorH / 2, 0.5, whiteWall,
    { wallRole: 'central_front_recess' }
  );
  addSlabOrTrim(
    groundFloorGroup, 2.4, 0.75, extT, -1.1, 3.225, 0.5, whiteWall,
    { wallRole: 'central_front_recess' }
  );
  addSolidWall(
    groundFloorGroup, 7.1, floorH, extT, 3.65, floorH / 2, 0.5, whiteWall,
    { wallRole: 'central_front_recess' }
  );
  // Sky-blue & mint dado behind portico
  addSlabOrTrim(groundFloorGroup, 4.85, 2.15, 0.05, -4.75, 1.08, 0.69, skyBlueWall);
  addSlabOrTrim(groundFloorGroup, 7.05, 2.15, 0.05, 3.65, 1.08, 0.69, skyBlueWall);
  // Glazed central entrance side frames
  addSlabOrTrim(groundFloorGroup, 0.12, 2.85, 0.38, -2.24, 1.425, 0.5, purpleDoorMat);
  addSlabOrTrim(groundFloorGroup, 0.12, 2.85, 0.38, 0.04, 1.425, 0.5, purpleDoorMat);

  // South Facade — East Projecting Wing (Z = +2.4, X = +7.2..+19.0, open secondary entrance X = +10.8..+12.2)
  addSolidWall(groundFloorGroup, extT, floorH, 1.9, 7.2, floorH / 2, 1.45, whiteWall);
  addSolidWall(groundFloorGroup, 3.6, floorH, extT, 9.0, floorH / 2, 2.4, whiteWall);
  addSlabOrTrim(groundFloorGroup, 1.4, 0.62, extT, 11.5, 3.29, 2.4, whiteWall);
  addSolidWall(groundFloorGroup, 6.8, floorH, extT, 15.6, floorH / 2, 2.4, whiteWall);
  // East Wing Dados: Sky-blue left bay + Purple secondary doorway frame + Boy-Reading-on-Carpet & Tulips Mural right bay!
  addSlabOrTrim(groundFloorGroup, 0.06, 2.25, 1.92, 7.01, 1.125, 1.45, skyBlueWall);
  addSlabOrTrim(groundFloorGroup, 3.58, 2.25, 0.05, 9.0, 1.125, 2.59, skyBlueWall);
  addSlabOrTrim(groundFloorGroup, 0.12, 2.98, 0.40, 10.84, 1.49, 2.42, purpleDoorMat);
  addSlabOrTrim(groundFloorGroup, 0.12, 2.98, 0.40, 12.16, 1.49, 2.42, purpleDoorMat);
  addSlabOrTrim(groundFloorGroup, 6.78, 2.28, 0.05, 15.6, 1.14, 2.59, eastMuralMat);
  // Continuous ground-floor concrete sunshade ledge across East Wing (ref_02b_facade_real.jpg)
  addSlabOrTrim(groundFloorGroup, 8.3, 0.10, 0.52, 14.75, 3.06, 2.66, sunshadeMat);

  // 4-Column Front Portico (colX = [-6.8, -2.3, +2.3, +6.8], Z = +4.4) + Flat Canopy Slab
  for (const colX of [-6.8, -2.3, 2.3, 6.8]) {
    addSolidWall(groundFloorGroup, 0.62, floorH, 0.62, colX, floorH / 2, 4.4, porticoColMat);
  }
  addSlabOrTrim(groundFloorGroup, 16.0, 0.42, 2.45, 0.0, floorH + 0.21, 3.625, whiteWall);
  addSlabOrTrim(groundFloorGroup, 14.4, 0.42, 1.95, 0.0, floorH + 0.21, 1.475, whiteWall);

  // West (-X = -19.0, grey finish), East (+X = +19.0), and North (-Z = -13.0) Ground Floor Perimeter Walls
  addSolidWall(groundFloorGroup, extT, floorH, 15.4, -19.0, floorH / 2, -5.3, westGreyWall);
  addSolidWall(groundFloorGroup, extT, floorH, 15.4, 19.0, floorH / 2, -5.3, whiteWall);
  addSolidWall(groundFloorGroup, 38.0, floorH, extT, 0.0, floorH / 2, -13.0, whiteWall);

  // NW Rear Corner Horizontal Pink / Charcoal / Teal Stripes & Center-West Teal Exterior Finish (ref_04a_rear_fa.jpg)
  addSlabOrTrim(groundFloorGroup, 6.4, 0.68, 0.05, -15.8, 0.34, -13.19, pinkWall);
  addSlabOrTrim(groundFloorGroup, 6.4, 0.68, 0.05, -15.8, 1.02, -13.19, new THREE.MeshStandardMaterial({ color: 0x333840, roughness: 0.85 }));
  addSlabOrTrim(groundFloorGroup, 6.4, 0.72, 0.05, -15.8, 1.72, -13.19, rearTealExt);
  addSlabOrTrim(groundFloorGroup, 8.8, 2.45, 0.05, -8.2, 1.225, -13.19, rearTealExt);

  // Ground Floor Exterior Windows (All 4 Sides)
  // Front (+Z): West 3 vertical windows, Central 2 flanking windows, East triple windows + upper louvers
  addExteriorWindow(groundFloorGroup, -9.8, 1.75, 2.4, 0, 2.35, 1.35, 2, true, 0.48);
  addExteriorWindow(groundFloorGroup, -15.8, 2.55, 2.4, 0, 1.85, 0.58, 3, false, 0.48);
  addExteriorWindow(groundFloorGroup, -4.8, 1.75, 0.5, 0, 1.95, 1.45, 1, false, 0.46);
  addExteriorWindow(groundFloorGroup, 2.8, 1.75, 0.5, 0, 1.95, 1.45, 1, false, 0.46);
  addExteriorWindow(groundFloorGroup, 9.0, 1.65, 2.4, 0, 1.95, 1.20, 2, false, 0.48);
  addExteriorWindow(groundFloorGroup, 13.7, 1.42, 2.4, 0, 1.95, 1.15, 2, false, 0.48);
  addExteriorWindow(groundFloorGroup, 13.7, 2.66, 2.4, 0, 1.95, 0.50, 1, false, 0.48);
  addExteriorWindow(groundFloorGroup, 16.9, 2.42, 2.4, 0, 2.55, 0.96, 3, false, 0.48);
  // West (-X): 3 square classroom windows (ref_06_first_cutaway_fa.jpg)
  addExteriorWindow(groundFloorGroup, -19.0, 1.55, 0.0, -Math.PI / 2, 1.15, 1.15, 1, false);
  addExteriorWindow(groundFloorGroup, -19.0, 1.55, -5.2, -Math.PI / 2, 1.15, 1.15, 1, false);
  addExteriorWindow(groundFloorGroup, -19.0, 1.55, -10.5, -Math.PI / 2, 1.15, 1.15, 1, false);
  // East (+X): 3 classroom windows with sunshade brows (ref_02b_facade_real.jpg)
  addExteriorWindow(groundFloorGroup, 19.0, 1.75, -0.4, Math.PI / 2, 1.85, 1.25, 2, true);
  addExteriorWindow(groundFloorGroup, 19.0, 1.75, -5.8, Math.PI / 2, 1.85, 1.25, 2, true);
  addExteriorWindow(groundFloorGroup, 19.0, 1.75, -10.7, Math.PI / 2, 1.65, 1.15, 1, true);
  // North (-Z): Pre-school windows under green canopy + high clerestory vents above portrait line
  addExteriorWindow(groundFloorGroup, 3.2, 1.75, -13.0, Math.PI, 1.85, 1.15, 2, false);
  addExteriorWindow(groundFloorGroup, 8.2, 1.75, -13.0, Math.PI, 1.85, 1.15, 2, false);
  addExteriorWindow(groundFloorGroup, 14.5, 2.55, -13.0, Math.PI, 2.10, 0.58, 3, false);

  // =====================================================================
  // GROUND FLOOR INTERIOR PARTITIONS (FA-121 Blueprint — ref_05b_ground_ortho_fa.jpg)
  // =====================================================================
  const partT = 0.24;
  // A) West Wing Classrooms (SW Green-Carpet Room, Mid-West Desk Room, NW Room) & Corridor
  addSolidWall(groundFloorGroup, 6.25, floorH, partT, -15.725, floorH / 2, -2.5, skyBlueWall);
  addSolidWall(groundFloorGroup, 6.25, floorH, partT, -15.725, floorH / 2, -7.6, skyBlueWall);
  addSolidWall(groundFloorGroup, partT, floorH, 15.1, -12.6, floorH / 2, -5.35, skyBlueWall);
  addPurpleDoor(groundFloorGroup, -12.6, 0.2, -0.2, Math.PI / 2);
  addPurpleDoor(groundFloorGroup, -12.6, 0.2, -5.0, Math.PI / 2);
  addPurpleDoor(groundFloorGroup, -12.6, 0.2, -10.2, Math.PI / 2);

  // South-Inner Classroom (X: -10.6..-6.5, Z: -5.6..+2.25) & Two Small North Rooms (Z: -13.0..-9.0)
  addSolidWall(groundFloorGroup, partT, floorH, 7.85, -10.6, floorH / 2, -1.675, skyBlueWall);
  addSolidWall(groundFloorGroup, 4.1, floorH, partT, -8.55, floorH / 2, -5.6, skyBlueWall);
  addSolidWall(groundFloorGroup, partT, floorH, 7.85, -6.5, floorH / 2, -1.675, skyBlueWall);
  addPurpleDoor(groundFloorGroup, -10.6, 0.2, -2.2, -Math.PI / 2);

  addSolidWall(groundFloorGroup, 8.8, floorH, partT, -8.2, floorH / 2, -9.0, whiteWall);
  addSolidWall(groundFloorGroup, partT, floorH, 4.0, -8.2, floorH / 2, -11.0, skyBlueWall);
  addPurpleDoor(groundFloorGroup, -10.2, 0.2, -9.0, 0);
  addPurpleDoor(groundFloorGroup, -6.0, 0.2, -9.0, 0);

  // B) Central Assembly Hall (X: -6.5..0.0) & Front-Left Office (X: -6.5..-3.56, Z: -3.4..+0.5)
  addSolidWall(groundFloorGroup, 0.22, floorH, 3.9, -3.56, floorH / 2, -1.45, whiteWall);
  addSolidWall(groundFloorGroup, 2.94, floorH, partT, -5.03, floorH / 2, -3.4, whiteWall);
  addSolidWall(groundFloorGroup, partT, floorH, 4.8, -6.5, floorH / 2, -5.8, whiteWall);
  addSolidWall(groundFloorGroup, 0.22, floorH, 8.7, 0.02, floorH / 2, -3.85, whiteWall);
  // Purple door between Educator portrait bays at Z = -3.45 on East Central Hall wall
  addPurpleDoor(groundFloorGroup, 0.02, 0.2, -3.45, -Math.PI / 2);

  // C) Enclosed Rainbow Stairwell (X: -3.8..0.0, Z: -13.0..-8.2) + Flanking Purple Doors (M4)
  const rainbowStairGroup = new THREE.Group();
  rainbowStairGroup.name = "Enclosed_Rainbow_Stairwell";
  rainbowStairGroup.userData = { feature: 'enclosed_rainbow_stairwell' };

  addSolidWall(rainbowStairGroup, 2.7, floorH, partT, -5.15, floorH / 2, -8.2, whiteWall);
  addSolidWall(rainbowStairGroup, 2.6, floorH, partT, 1.32, floorH / 2, -8.2, whiteWall);
  addSlabOrTrim(rainbowStairGroup, 3.8, 0.65, partT, -1.9, 3.275, -8.2, whiteWall);
  addPurpleDoor(rainbowStairGroup, -5.1, 0.2, -8.2, 0);
  addPurpleDoor(rainbowStairGroup, 1.3, 0.2, -8.2, 0);

  addSolidWall(rainbowStairGroup, 0.22, floorH, 4.8, -3.8, floorH / 2, -10.6, whiteWall);
  addSolidWall(rainbowStairGroup, 0.22, floorH, 4.8, 0.02, floorH / 2, -10.6, whiteWall);

  // 12 Rainbow Treads rising North (Z: -8.35..-12.55, Y: 0.32..3.52)
  const rainbowColors = [
    0xeab308, 0x3b82f6, 0xec4899, 0x22c55e, 0xeab308, 0x3b82f6,
    0xef4444, 0x22c55e, 0xec4899, 0xeab308, 0x38bdf8, 0xf43f5e
  ];
  for (let s = 0; s < 12; s++) {
    const tread = new THREE.Mesh(
      new THREE.BoxGeometry(2.15, 0.29, 0.38),
      new THREE.MeshStandardMaterial({ color: rainbowColors[s], roughness: 0.48 })
    );
    tread.position.set(-1.35, 0.34 + s * 0.29, -8.38 - s * 0.37);
    tread.castShadow = true;
    rainbowStairGroup.add(tread);
  }
  // Brown diagonal dado & paper roses on right stairwell wall + Red metal handrail on left (ref_07a_rainbow_stairs.jpg)
  const dadoSlope = new THREE.Mesh(new THREE.BoxGeometry(0.05, 1.15, 4.4), brownDadoMat);
  dadoSlope.position.set(-0.12, 1.75, -10.5);
  dadoSlope.rotation.x = 0.64;
  rainbowStairGroup.add(dadoSlope);

  const handrail = new THREE.Mesh(
    new THREE.CylinderGeometry(0.035, 0.035, 4.8, 8),
    new THREE.MeshStandardMaterial({ color: 0xb91c1c, roughness: 0.4, metalness: 0.5 })
  );
  handrail.position.set(-2.48, 2.35, -10.45);
  handrail.rotation.x = Math.PI / 2 - 0.64;
  rainbowStairGroup.add(handrail);
  groundFloorGroup.add(rainbowStairGroup);

  // D) East Wing Classrooms, Boys' Flower Arch Ceremony Room & NE Pre-School Suite
  addSolidWall(groundFloorGroup, 7.48, floorH, partT, 3.76, floorH / 2, -3.6, tealWall);
  addSolidWall(groundFloorGroup, 7.48, floorH, partT, 3.76, floorH / 2, -8.4, tealWall);
  addSolidWall(groundFloorGroup, partT, floorH, 8.9, 7.5, floorH / 2, -3.95, tealWall);
  addPurpleDoor(groundFloorGroup, 7.5, 0.2, -6.0, -Math.PI / 2);

  // Two Decorative Red-Rose Ceremony Arches inside Boys' Ceremony Room (spot_boys_flower_arch.jpg)
  [-5.9, -7.2].forEach((az) => {
    const archTorus = new THREE.Mesh(
      new THREE.TorusGeometry(1.55, 0.11, 10, 24, Math.PI),
      new THREE.MeshStandardMaterial({ color: 0xbe123c, roughness: 0.65 })
    );
    archTorus.position.set(3.8, 1.45, az);
    groundFloorGroup.add(archTorus);
  });

  // Secondary East Entrance Corridor & SE / Mid-East Classrooms (X: +11.2..+19.0)
  addSolidWall(groundFloorGroup, partT, floorH, 10.8, 11.2, floorH / 2, -3.0, whiteWall);
  addSolidWall(groundFloorGroup, 7.8, floorH, partT, 15.1, floorH / 2, -3.2, tealWall);
  addSolidWall(groundFloorGroup, 11.5, floorH, partT, 13.25, floorH / 2, -8.4, whiteWall);
  addSolidWall(groundFloorGroup, partT, floorH, 4.6, 9.5, floorH / 2, -10.7, whiteWall);
  addPurpleDoor(groundFloorGroup, 11.2, 0.2, -0.6, Math.PI / 2);
  addPurpleDoor(groundFloorGroup, 11.2, 0.2, -5.8, Math.PI / 2);
  addPurpleDoor(groundFloorGroup, 5.2, 0.2, -8.4, 0);
  addPurpleDoor(groundFloorGroup, 13.5, 0.2, -8.4, 0);

  // =====================================================================
  // REAR EXTERIOR GIRLS' STAIRCASE, BLUE DINOSAUR GATE & SLOPED GREEN CANOPY (M2 — ref_04a_rear_fa.jpg)
  // =====================================================================
  const rearStairGroup = new THREE.Group();
  rearStairGroup.name = "Rear_Exterior_Girls_Staircase_And_Canopy";
  rearStairGroup.userData = { feature: 'rear_girls_exterior_stairs' };

  // Top concrete landing outside 1st-Floor Blue Door (X: -5.5..-3.8, Z: -15.35..-13.0, Y = 3.55)
  addSlabOrTrim(rearStairGroup, 1.75, 0.24, 2.35, -4.65, 3.50, -14.18, terracottaStairMat);
  // Support wall below landing
  addSlabOrTrim(rearStairGroup, 1.75, 3.45, 0.24, -4.65, 1.725, -15.25, pinkWall);

  // 13 Terracotta-Pink Exterior Treads rising East (X: -9.8 -> -5.5, Z: -15.2..-13.2)
  for (let rs = 0; rs < 13; rs++) {
    const stepH = (rs + 1) * (3.50 / 13);
    const tread = new THREE.Mesh(
      new THREE.BoxGeometry(0.36, stepH, 2.05),
      terracottaStairMat
    );
    tread.position.set(-9.75 + rs * 0.33, stepH / 2, -14.20);
    tread.castShadow = true;
    tread.receiveShadow = true;
    rearStairGroup.add(tread);
  }
  // White tubular stair railing along outer North edge (Z = -15.2)
  const rearRail = new THREE.Mesh(
    new THREE.CylinderGeometry(0.035, 0.035, 5.4, 8),
    new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.45, metalness: 0.45 })
  );
  rearRail.position.set(-7.6, 2.65, -15.20);
  rearRail.rotation.z = -0.68;
  rearStairGroup.add(rearRail);

  // Rear Alley Partition Wall (X = -3.8, Z = -19.5..-13.0) with Blue Metal Gate & Green Dinosaur Height-Chart Mural!
  addSlabOrTrim(rearStairGroup, 0.26, 2.45, 2.2, -3.8, 1.225, -14.1, pinkWall);
  addSlabOrTrim(rearStairGroup, 0.28, 2.45, 1.45, -3.8, 1.225, -15.65, dinoMuralMat);
  addSlabOrTrim(rearStairGroup, 3.2, 2.45, 0.06, -1.9, 1.225, -13.20, dinoMuralMat);
  const blueRearGate = new THREE.Mesh(new THREE.BoxGeometry(0.12, 2.35, 1.85), blueMetalMat);
  blueRearGate.position.set(-3.8, 1.18, -17.30);
  rearStairGroup.add(blueRearGate);
  addSlabOrTrim(rearStairGroup, 0.26, 2.45, 1.3, -3.8, 1.225, -18.85, pinkWall);

  // Pitched / Sloped Green Corrugated Pre-School Canopy (X: -3.6..+11.5, Z: -18.6..-13.0, Y: 3.55 -> 2.85)
  const slopedCanopy = new THREE.Mesh(new THREE.BoxGeometry(15.1, 0.12, 5.75), canopyGreenMat);
  slopedCanopy.position.set(3.95, 3.22, -15.82);
  slopedCanopy.rotation.x = -0.125;
  slopedCanopy.castShadow = true;
  rearStairGroup.add(slopedCanopy);

  const postSteelMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.5, metalness: 0.6 });
  [-3.2, 1.6, 6.4, 11.2].forEach((px) => {
    const post = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.055, 2.88, 8), postSteelMat);
    post.position.set(px, 1.44, -18.45);
    rearStairGroup.add(post);
  });
  groundFloorGroup.add(rearStairGroup);

  // Camera-Aligned Forensic Photos in Ground Floor Rooms (Un-mirrored, true room coordinates!)
  // 1) Boys under Red Rose Arches (Center-East Ceremony Room — X: 0..+7.5, Z: -8.4..-3.6)
  createCameraAlignedPhotoInSpace(
    groundFloorGroup,
    'images/fa_spots/spot_boys_flower_arch.jpg',
    [3.6, 1.80, -4.2],
    [3.8, 1.80, -7.85],
    0,
    4.1,
    2.35
  );

  // 2) Boys Clapping & Singing on Green Carpet (SW Classroom — X: -19.0..-12.6, Z: -2.5..+2.4)
  createCameraAlignedPhotoInSpace(
    groundFloorGroup,
    'images/fa_spots/spot_boys_classroom.jpg',
    [-13.5, 1.80, 0.3],
    [-18.25, 1.75, -0.3],
    Math.PI / 2,
    4.1,
    2.35
  );

  // 3) Teachers & Girls at the Rainbow Staircase (Central Hall looking North into Stairwell)
  createCameraAlignedPhotoInSpace(
    groundFloorGroup,
    'images/fa_spots/spot_rainbow_stairs.jpg',
    [-1.8, 1.80, -4.0],
    [-1.85, 1.85, -8.05],
    0,
    3.6,
    2.15
  );

  // =====================================================================
  // 2. FIRST FLOOR (GIRLS' PRIMARY SCHOOL — FA-121 Blueprint, ref_06_first_cutaway_fa.jpg)
  // =====================================================================
  const y1 = floorH;
  // Stepped First Floor Slabs (leaving stairwell opening at X: -3.8..0.0, Z: -13.0..-8.0)
  addSlabOrTrim(firstFloorGroup, 7.5, 0.22, 15.4, -15.25, y1, -5.3, floorGreen); // West Girls' Assembly Hall
  addSlabOrTrim(firstFloorGroup, 4.3, 0.22, 15.4, -9.35, y1, -5.3, floorGrey);
  addSlabOrTrim(firstFloorGroup, 14.4, 0.22, 8.5, 0.0, y1, -3.75, floorGrey);
  addSlabOrTrim(firstFloorGroup, 3.4, 0.22, 5.0, -5.5, y1, -10.5, floorGrey);
  addSlabOrTrim(firstFloorGroup, 8.5, 0.22, 5.0, 4.25, y1, -10.5, floorGrey);
  addSlabOrTrim(firstFloorGroup, 10.5, 0.22, 5.6, 13.75, y1, -10.2, floorBrown); // NE Rubble Archive Room (tan/brown floor)
  addSlabOrTrim(firstFloorGroup, 11.8, 0.22, 9.8, 13.1, y1, -2.5, floorGrey);
  addSlabOrTrim(firstFloorGroup, 5.8, 0.03, 5.0, 10.6, y1 + 0.12, -4.8, floorLilac);

  // Exterior First Floor Stepped Walls (Crisp White — Y = 3.6..7.2)
  addSolidWall(firstFloorGroup, 11.8, floorH, extT, -13.1, y1 + floorH / 2, 2.4, whiteWall);
  addSolidWall(firstFloorGroup, extT, floorH, 1.9, -7.2, y1 + floorH / 2, 1.45, whiteWall);
  addSolidWall(firstFloorGroup, 14.4, floorH, extT, 0.0, y1 + floorH / 2, 0.5, whiteWall);
  addSolidWall(firstFloorGroup, extT, floorH, 1.9, 7.2, y1 + floorH / 2, 1.45, whiteWall);
  addSolidWall(firstFloorGroup, 11.8, floorH, extT, 13.1, y1 + floorH / 2, 2.4, whiteWall);

  addSolidWall(firstFloorGroup, extT, floorH, 15.4, -19.0, y1 + floorH / 2, -5.3, whiteWall);
  addSolidWall(firstFloorGroup, extT, floorH, 15.4, 19.0, y1 + floorH / 2, -5.3, whiteWall);
  addSolidWall(firstFloorGroup, 38.0, floorH, extT, 0.0, y1 + floorH / 2, -13.0, whiteWall);

  // Blue First-Floor Rear Exterior Door onto Girls' Staircase Landing (X = -4.6, Z = -13.0 — ref_04a_rear_fa.jpg)
  const blueUpperDoor = new THREE.Mesh(new THREE.BoxGeometry(1.12, 2.15, 0.42), blueMetalMat);
  blueUpperDoor.position.set(-4.65, y1 + 1.15, -13.0);
  firstFloorGroup.add(blueUpperDoor);

  // First Floor Exterior Windows & Projecting Sunshade Brows (All 4 Sides — ref_02a, ref_04a, ref_06)
  // Front (+Z): West Wing slits & window, Central 3 multi-pane classroom windows above portico, East 3 slits + scorched bay + corner 4-pane
  addExteriorWindow(firstFloorGroup, -16.2, y1 + 2.25, 2.4, 0, 2.15, 0.62, 3, false);
  addExteriorWindow(firstFloorGroup, -12.8, y1 + 1.65, 2.4, 0, 1.55, 0.95, 1, false);
  addExteriorWindow(firstFloorGroup, -9.6, y1 + 2.05, 2.4, 0, 2.25, 1.45, 2, true);
  addExteriorWindow(firstFloorGroup, -4.8, y1 + 1.75, 0.5, 0, 1.95, 1.35, 1, false);
  addExteriorWindow(firstFloorGroup, -0.6, y1 + 1.75, 0.5, 0, 3.15, 1.35, 3, false);
  addExteriorWindow(firstFloorGroup, 4.1, y1 + 1.75, 0.5, 0, 1.95, 1.35, 1, false);
  addExteriorWindow(firstFloorGroup, 9.3, y1 + 2.05, 2.4, 0, 2.25, 1.45, 2, true);
  addExteriorWindow(firstFloorGroup, 12.3, y1 + 2.55, 2.4, 0, 1.05, 0.95, 1, false);
  addExteriorWindow(firstFloorGroup, 14.0, y1 + 1.75, 2.4, 0, 1.95, 1.20, 2, false);
  addExteriorWindow(firstFloorGroup, 16.9, y1 + 2.45, 2.4, 0, 2.65, 1.10, 3, false);
  addSlabOrTrim(firstFloorGroup, 7.2, 0.11, 0.52, 15.2, y1 + 3.12, 2.66, sunshadeMat);

  // West (-X): Stepped square windows positioned in portrait-free bays (Z = +1.0, -2.6, -3.4, -11.4)
  addExteriorWindow(firstFloorGroup, -19.0, y1 + 1.35, 1.0, -Math.PI / 2, 0.95, 0.95, 1, false);
  addExteriorWindow(firstFloorGroup, -19.0, y1 + 1.95, -2.55, -Math.PI / 2, 0.80, 0.80, 0, false);
  addExteriorWindow(firstFloorGroup, -19.0, y1 + 1.40, -3.40, -Math.PI / 2, 0.80, 0.80, 0, false);
  addExteriorWindow(firstFloorGroup, -19.0, y1 + 1.75, -11.4, -Math.PI / 2, 1.05, 1.05, 1, false);

  // East (+X): Upper classroom windows + sunshade brows
  addExteriorWindow(firstFloorGroup, 19.0, y1 + 1.95, -0.4, Math.PI / 2, 1.85, 1.20, 2, true);
  addExteriorWindow(firstFloorGroup, 19.0, y1 + 1.95, -5.6, Math.PI / 2, 1.85, 1.20, 2, true);
  addExteriorWindow(firstFloorGroup, 19.0, y1 + 2.35, -10.6, Math.PI / 2, 2.05, 0.70, 3, true);

  // North (-Z): High ventilation slits in NW Girls' Hall (above portrait row y1+1.15) + North classroom windows
  addExteriorWindow(firstFloorGroup, -16.2, y1 + 2.55, -13.0, Math.PI, 2.15, 0.62, 2, false);
  addExteriorWindow(firstFloorGroup, -12.9, y1 + 2.55, -13.0, Math.PI, 1.20, 0.62, 1, false);
  addExteriorWindow(firstFloorGroup, -8.8, y1 + 1.85, -13.0, Math.PI, 1.45, 1.10, 1, false);
  addExteriorWindow(firstFloorGroup, 2.2, y1 + 2.15, -13.0, Math.PI, 1.55, 1.05, 1, false);
  addExteriorWindow(firstFloorGroup, 6.4, y1 + 2.15, -13.0, Math.PI, 1.55, 1.05, 1, false);
  addExteriorWindow(firstFloorGroup, 13.8, y1 + 2.45, -13.0, Math.PI, 2.45, 0.68, 3, false);

  // =====================================================================
  // FIRST FLOOR INTERIOR PARTITIONS (Girls' Hall, Central E-W Spine Corridor, Pink/Sage Rooms & NE Archive)
  // =====================================================================
  // 1) Girls' West Assembly Hall East Partition (X = -11.5, open Pink Double Doors at Z = -5.8)
  addSolidWall(firstFloorGroup, partT, floorH, 6.2, -11.5, y1 + floorH / 2, -9.9, whiteWall);
  addSolidWall(firstFloorGroup, partT, floorH, 7.2, -11.5, y1 + floorH / 2, -1.2, whiteWall);
  addSlabOrTrim(firstFloorGroup, partT, 0.95, 2.0, -11.5, y1 + 3.125, -5.8, whiteWall);
  // Open Pink Double Doors swinging into Girls' Assembly Hall (ref_06_first_cutaway_fa.jpg)
  const pinkDoorL = new THREE.Mesh(new THREE.BoxGeometry(0.92, 2.25, 0.10), pinkDoorMat);
  pinkDoorL.position.set(-11.95, y1 + 1.20, -6.65);
  pinkDoorL.rotation.y = 0.25;
  const pinkDoorR = new THREE.Mesh(new THREE.BoxGeometry(0.92, 2.25, 0.10), pinkDoorMat);
  pinkDoorR.position.set(-11.95, y1 + 1.20, -4.95);
  pinkDoorR.rotation.y = -0.25;
  firstFloorGroup.add(pinkDoorL, pinkDoorR);

  // 2) Central E-W Spine Corridor (X: -11.5..+8.5, Z: -7.4..-4.6)
  const spineGroup = new THREE.Group();
  spineGroup.name = "First_Floor_Central_Spine_Corridor";
  spineGroup.userData = { feature: 'first_floor_spine_corridor' };

  // South Corridor Wall (Z = -4.6, X = -11.5..+7.5) + Purple Doors
  addTwoToneWall(spineGroup, 19.0, floorH, partT, -2.0, y1, -4.6, sageGreenWall, whiteWall);
  [-9.1, -4.2, 1.0, 5.5].forEach((dx) => addPurpleDoor(spineGroup, dx, y1 + 0.1, -4.6, 0));

  // North Corridor Wall (Z = -7.4, X = -11.5..-3.8 & X = 0.0..+19.0) + Purple Doors
  addTwoToneWall(spineGroup, 7.7, floorH, partT, -7.65, y1, -7.4, sageGreenWall, whiteWall);
  addSolidWall(spineGroup, 19.0, floorH, partT, 9.5, y1 + floorH / 2, -7.4, whiteWall);
  [-9.6, -5.3, 2.1, 6.2, 8.05].forEach((dx) => addPurpleDoor(spineGroup, dx, y1 + 0.1, -7.4, 0));
  firstFloorGroup.add(spineGroup);

  // 3) South Classroom Cross-Partitions (Pink & Sage Green — ref_06_first_cutaway_fa.jpg)
  addTwoToneWall(firstFloorGroup, partT, floorH, 5.1, -6.8, y1, -2.05, sageGreenWall, pinkWall);
  addTwoToneWall(firstFloorGroup, partT, floorH, 5.1, -1.6, y1, -2.05, sageGreenWall, pinkWall);
  addTwoToneWall(firstFloorGroup, partT, floorH, 5.1, 3.6, y1, -2.05, sageGreenWall, whiteWall);
  addSolidWall(firstFloorGroup, partT, floorH, 9.8, 7.5, y1 + floorH / 2, -2.5, whiteWall);

  // 4) North Classroom Cross-Partitions + Stairwell Upper Guard Walls + NE Rubble Archive West Wall (X = +8.5)
  addTwoToneWall(firstFloorGroup, partT, floorH, 5.6, -7.8, y1, -10.2, sageGreenWall, pinkWall);
  addSolidWall(firstFloorGroup, 0.22, floorH, 5.6, -3.8, y1 + floorH / 2, -10.2, whiteWall);
  addSolidWall(firstFloorGroup, 0.22, floorH, 5.6, 0.02, y1 + floorH / 2, -10.2, whiteWall);
  addTwoToneWall(firstFloorGroup, partT, floorH, 5.6, 4.2, y1, -10.2, sageGreenWall, pinkWall);
  // NE Archive West Partition (X = +8.5, Z = -13.0..-7.85, leaving vestibule entry from door at X = 8.05)
  addSolidWall(firstFloorGroup, 0.22, floorH, 5.15, 8.5, y1 + floorH / 2, -10.425, whiteWall);

  // 5) East Wing Classroom Cross-Partitions (X: +7.5..+19.0, Z: -7.4..+2.4)
  addSolidWall(firstFloorGroup, 11.5, floorH, partT, 13.25, y1 + floorH / 2, -2.2, whiteWall);
  addSolidWall(firstFloorGroup, partT, floorH, 5.2, 13.5, y1 + floorH / 2, -4.8, whiteWall);
  addPurpleDoor(firstFloorGroup, 7.5, y1 + 0.1, -5.8, -Math.PI / 2);
  addPurpleDoor(firstFloorGroup, 10.5, y1 + 0.1, -2.2, 0);

  // Camera-Aligned Photo in First Floor Girls' Assembly Hall (80+ schoolgirls seated — rec_21.jpg)
  createCameraAlignedPhotoInSpace(
    firstFloorGroup,
    'images/fa_spots/spot_girls_assembly.jpg',
    [-12.5, y1 + 1.85, -1.2],
    [-15.6, y1 + 1.80, -8.8],
    0.35,
    4.6,
    2.6
  );

  // =====================================================================
  // 3. STEPPED ROOF, PARAPET, STAIRWELL PENTHOUSE, SKYLIGHT & TELECOM MAST (M3)
  // =====================================================================
  const yRoof = floorH * 2;
  // Stepped Roof Slabs
  addSlabOrTrim(roofGroup, 12.1, 0.30, 15.7, -13.15, yRoof + 0.15, -5.3, whiteWall);
  addSlabOrTrim(roofGroup, 14.4, 0.30, 13.8, 0.0, yRoof + 0.15, -6.25, whiteWall);
  addSlabOrTrim(roofGroup, 12.1, 0.30, 15.7, 13.15, yRoof + 0.15, -5.3, whiteWall);

  // Perimeter 0.65m Parapet Walls tracing stepped footprint (Y = 7.50..8.15)
  const pH = 0.65;
  const pY = yRoof + 0.30 + pH / 2;
  addSlabOrTrim(roofGroup, 12.1, pH, 0.30, -13.15, pY, 2.42, whiteWall);
  addSlabOrTrim(roofGroup, 0.30, pH, 1.95, -7.2, pY, 1.45, whiteWall);
  addSlabOrTrim(roofGroup, 14.4, pH, 0.30, 0.0, pY, 0.52, whiteWall);
  addSlabOrTrim(roofGroup, 0.30, pH, 1.95, 7.2, pY, 1.45, whiteWall);
  addSlabOrTrim(roofGroup, 12.1, pH, 0.30, 13.15, pY, 2.42, whiteWall);
  addSlabOrTrim(roofGroup, 0.30, pH, 15.7, -19.05, pY, -5.3, whiteWall);
  addSlabOrTrim(roofGroup, 0.30, pH, 15.7, 19.05, pY, -5.3, whiteWall);
  addSlabOrTrim(roofGroup, 38.4, pH, 0.30, 0.0, pY, -13.02, whiteWall);

  // Stairwell Roof Penthouse Box (X: -4.0..+0.4, Z: -12.8..-8.0, Y: 7.50..9.35 — ref_04a_rear_fa.jpg)
  addSlabOrTrim(roofGroup, 4.4, 1.85, 4.8, -1.8, yRoof + 0.30 + 0.925, -10.4, whiteWall);
  // Central Roof Skylight / Hatch Curb (X = -1.6, Z = -5.4)
  addSlabOrTrim(roofGroup, 1.55, 0.42, 1.55, -1.6, yRoof + 0.51, -5.4, sunshadeMat);

  // White Steel Lattice Telecom Mast (X = +5.6, Z = -4.2, Y = 7.50..17.65m — ref_01_aerial_fa.jpg & ref_04a_rear_fa.jpg)
  const mastGroup = new THREE.Group();
  mastGroup.position.set(5.6, yRoof + 0.30, -4.2);
  const mastMat = new THREE.MeshStandardMaterial({ color: 0xf1f5f9, roughness: 0.45, metalness: 0.45 });
  const mastH = 9.4;
  const halfSpan = 0.26;
  [[-halfSpan, -halfSpan], [halfSpan, -halfSpan], [-halfSpan, halfSpan], [halfSpan, halfSpan]].forEach(([cx, cz]) => {
    const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.028, 0.036, mastH, 6), mastMat);
    leg.position.set(cx, mastH / 2, cz);
    mastGroup.add(leg);
  });
  for (let tier = 0; tier < 10; tier++) {
    const ty = 0.45 + tier * 0.92;
    const braceA = new THREE.Mesh(new THREE.BoxGeometry(halfSpan * 2.1, 0.03, 0.03), mastMat);
    braceA.position.set(0, ty, halfSpan);
    const braceB = braceA.clone();
    braceB.position.set(0, ty, -halfSpan);
    const braceC = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.03, halfSpan * 2.1), mastMat);
    braceC.position.set(halfSpan, ty, 0);
    const braceD = braceC.clone();
    braceD.position.set(-halfSpan, ty, 0);
    const diag = new THREE.Mesh(new THREE.BoxGeometry(halfSpan * 2.6, 0.025, 0.025), mastMat);
    diag.position.set(0, ty + 0.45, halfSpan);
    diag.rotation.z = (tier % 2 === 0 ? 1 : -1) * 0.72;
    mastGroup.add(braceA, braceB, braceC, braceD, diag);
  }
  const mastTip = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.022, 1.35, 6), mastMat);
  mastTip.position.set(0, mastH + 0.55, 0);
  mastGroup.add(mastTip);
  roofGroup.add(mastGroup);

  // =====================================================================
  // 4. POST-STRIKE MODEL: SURVIVING EAST WING, EXPOSED 2-STORY SHEAR,
  //    4 SURVIVING PORTICO COLUMNS, L-SHAPED DAMAGE VOLUME & 5M CRATER (H4, L2)
  //    Verified against ref_02b_facade_real.jpg, ref_08_damage_extent_fa.jpg & ref_09a/b
  // =====================================================================
  const ruinedConcrete = new THREE.MeshStandardMaterial({ color: 0x4b4640, roughness: 0.98 });
  const debrisMat = new THREE.MeshStandardMaterial({ color: 0x696259, roughness: 0.94 });
  const rebarMat = new THREE.MeshStandardMaterial({ color: 0x3b2f2a, roughness: 0.65, metalness: 0.55 });
  const yellowColMat = new THREE.MeshStandardMaterial({ color: 0xdccf68, roughness: 0.78 });

  // A) Surviving Detailed East Wing (X: +4.5..+19.0, Z: -13.0..+2.4)
  // Floor & Roof Slabs
  addSlabOrTrim(postStrikeModelGroup, 14.5, 0.22, 13.5, 11.75, 0.11, -6.25, floorGrey);
  addSlabOrTrim(postStrikeModelGroup, 11.8, 0.22, 1.9, 13.1, 0.11, 1.45, floorGrey);
  addSlabOrTrim(postStrikeModelGroup, 14.5, 0.24, 13.5, 11.75, y1, -6.25, floorGrey);
  addSlabOrTrim(postStrikeModelGroup, 11.8, 0.24, 1.9, 13.1, y1, 1.45, floorGrey);
  addSlabOrTrim(postStrikeModelGroup, 14.7, 0.30, 13.7, 11.75, yRoof + 0.15, -6.25, whiteWall);
  addSlabOrTrim(postStrikeModelGroup, 12.0, 0.30, 2.0, 13.1, yRoof + 0.15, 1.45, whiteWall);
  // East Wing Parapet
  addSlabOrTrim(postStrikeModelGroup, 12.0, pH, 0.30, 13.1, pY, 2.42, whiteWall);
  addSlabOrTrim(postStrikeModelGroup, 0.30, pH, 15.7, 19.02, pY, -5.3, whiteWall);
  addSlabOrTrim(postStrikeModelGroup, 14.7, pH, 0.30, 11.75, pY, -13.02, whiteWall);

  // Surviving East Wing Exterior Walls, Mural, Windows & Post-Strike Smoke Scorch Plume (ref_02b_facade_real.jpg)
  addSlabOrTrim(postStrikeModelGroup, extT, floorH * 2, 1.9, 7.2, floorH, 1.45, whiteWall);
  addSlabOrTrim(postStrikeModelGroup, 3.6, floorH * 2, extT, 9.0, floorH, 2.4, whiteWall);
  addSlabOrTrim(postStrikeModelGroup, 1.4, floorH + 0.62, extT, 11.5, y1 + 1.49, 2.4, whiteWall);
  addSlabOrTrim(postStrikeModelGroup, 6.8, floorH * 2, extT, 15.6, floorH, 2.4, whiteWall);
  addSlabOrTrim(postStrikeModelGroup, extT, floorH * 2, 15.4, 19.0, floorH, -5.3, whiteWall);
  addSlabOrTrim(postStrikeModelGroup, 14.5, floorH * 2, extT, 11.75, floorH, -13.0, whiteWall);

  addSlabOrTrim(postStrikeModelGroup, 3.58, 2.25, 0.05, 9.0, 1.125, 2.59, skyBlueWall);
  addSlabOrTrim(postStrikeModelGroup, 6.78, 2.28, 0.05, 15.6, 1.14, 2.59, eastMuralMat);
  addSlabOrTrim(postStrikeModelGroup, 8.3, 0.10, 0.52, 14.75, 3.06, 2.66, sunshadeMat);
  addSlabOrTrim(postStrikeModelGroup, 7.2, 0.11, 0.52, 15.2, y1 + 3.12, 2.66, sunshadeMat);

  addExteriorWindow(postStrikeModelGroup, 9.0, 1.65, 2.4, 0, 1.95, 1.20, 2, false, 0.48);
  addExteriorWindow(postStrikeModelGroup, 13.7, 1.42, 2.4, 0, 1.95, 1.15, 2, false, 0.48);
  addExteriorWindow(postStrikeModelGroup, 16.9, 2.42, 2.4, 0, 2.55, 0.96, 3, false, 0.48);
  addExteriorWindow(postStrikeModelGroup, 9.3, y1 + 2.05, 2.4, 0, 2.25, 1.45, 2, true);
  addExteriorWindow(postStrikeModelGroup, 14.0, y1 + 1.75, 2.4, 0, 1.95, 1.20, 2, false);
  addExteriorWindow(postStrikeModelGroup, 16.9, y1 + 2.45, 2.4, 0, 2.65, 1.10, 3, false);
  addExteriorWindow(postStrikeModelGroup, 19.0, 1.75, -0.4, Math.PI / 2, 1.85, 1.25, 2, true);
  addExteriorWindow(postStrikeModelGroup, 19.0, y1 + 1.95, -0.4, Math.PI / 2, 1.85, 1.20, 2, true);
  addExteriorWindow(postStrikeModelGroup, 19.0, 1.75, -5.8, Math.PI / 2, 1.85, 1.25, 2, true);
  addExteriorWindow(postStrikeModelGroup, 19.0, y1 + 1.95, -5.6, Math.PI / 2, 1.85, 1.20, 2, true);

  // Black Smoke Soot Scorch Plume above 1st-Floor East Window (ref_02b_facade_real.jpg)
  const scorchPlane = new THREE.Mesh(
    new THREE.PlaneGeometry(2.6, 2.1),
    new THREE.MeshBasicMaterial({ map: murals.scorchTex, transparent: true, depthWrite: false })
  );
  scorchPlane.position.set(14.0, y1 + 2.48, 2.60);
  postStrikeModelGroup.add(scorchPlane);

  // B) Exposed 2-Story Sheared Cross-Section & Surviving North Stairwell Core (ref_08, ref_09a, ref_09b)
  const shearGroup = new THREE.Group();
  shearGroup.name = "Exposed_Two_Story_Shear_Cross_Section";
  shearGroup.userData = { feature: 'exposed_shear_cross_section' };

  // Surviving North Stairwell Core (X: -3.8..+4.5, Z: -13.0..-8.2)
  addSlabOrTrim(shearGroup, 8.3, floorH * 2, extT, 0.35, floorH, -13.0, whiteWall);
  addSlabOrTrim(shearGroup, 0.28, floorH * 2, 4.8, -3.8, floorH, -10.6, whiteWall);
  addSlabOrTrim(shearGroup, 8.3, 0.24, 4.8, 0.35, y1, -10.6, floorGrey);
  // Sloped Pre-school rear canopy survived behind North wall (visible in ref_08_damage_extent_fa.jpg!)
  const postRearCanopy = new THREE.Mesh(new THREE.BoxGeometry(14.0, 0.12, 5.4), canopyGreenMat);
  postRearCanopy.position.set(4.2, 3.22, -15.7);
  postRearCanopy.rotation.x = -0.12;
  shearGroup.add(postRearCanopy);

  // Exposed North-Facing Crater Wall (Z = -8.2, X: -3.8..+4.5): Ground Teal/White + Upper Pink/Sage + Purple Doors!
  addSlabOrTrim(shearGroup, 8.3, 1.5, 0.26, 0.35, 0.75, -8.2, tealWall);
  addSlabOrTrim(shearGroup, 8.3, 2.1, 0.26, 0.35, 2.55, -8.2, whiteWall);
  addSlabOrTrim(shearGroup, 8.3, 1.45, 0.26, 0.35, y1 + 0.725, -8.2, sageGreenWall);
  addSlabOrTrim(shearGroup, 8.3, 2.15, 0.26, 0.35, y1 + 2.525, -8.2, pinkWall);
  addPurpleDoor(shearGroup, -2.1, y1 + 0.12, -8.2, 0);
  addPurpleDoor(shearGroup, 1.6, y1 + 0.12, -8.2, 0);

  // Exposed East-Facing Crater Shear Wall (X = +4.5, Z = -8.2..+0.5): Ground Teal + Upper Pink/Sage + Purple Doors + Yellow/Purple Column!
  addSlabOrTrim(shearGroup, 0.28, 1.55, 8.7, 4.5, 0.775, -3.85, tealWall);
  addSlabOrTrim(shearGroup, 0.28, 2.05, 8.7, 4.5, 2.575, -3.85, whiteWall);
  addSlabOrTrim(shearGroup, 0.28, 1.45, 8.7, 4.5, y1 + 0.725, -3.85, sageGreenWall);
  addSlabOrTrim(shearGroup, 0.28, 2.15, 8.7, 4.5, y1 + 2.525, -3.85, pinkWall);
  addPurpleDoor(shearGroup, 4.5, 0.2, -5.8, -Math.PI / 2);
  addPurpleDoor(shearGroup, 4.5, y1 + 0.12, -5.8, -Math.PI / 2);
  addPurpleDoor(shearGroup, 4.5, y1 + 0.12, -2.2, -Math.PI / 2);

  // Cylindrical Yellow & Purple Corner Column visible in ref_09a_crater_photo_fa.jpg
  const shearCylUpper = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 1.65, 16), yellowColMat);
  shearCylUpper.position.set(4.15, y1 + 1.45, -7.85);
  const shearCylBand = new THREE.Mesh(new THREE.CylinderGeometry(0.43, 0.43, 0.58, 16), purpleDoorMat);
  shearCylBand.position.set(4.15, y1 + 0.38, -7.85);
  shearGroup.add(shearCylUpper, shearCylBand);

  // Jagged Sheared Concrete Floor Slab Ledge + Hanging Rebar Rods anchored into Crater Shear Walls
  const shearedSlabMat = new THREE.MeshStandardMaterial({ color: 0x7b756d, roughness: 0.92 });
  [
    [-1.8, -8.02, 0.24, 0.08],
    [1.4, -8.02, 0.22, -0.14],
    [4.28, -6.3, 0.08, 0.30],
    [4.28, -3.2, 0.06, 0.26],
    [4.28, -0.8, 0.10, 0.22]
  ].forEach(([sx, sz, rotX, rotZ], idx) => {
    const brokenSlab = new THREE.Mesh(new THREE.BoxGeometry(1.85, 0.20, 1.05), shearedSlabMat);
    brokenSlab.position.set(sx, y1 - 0.12, sz);
    brokenSlab.rotation.set(rotX, idx * 0.18, rotZ);
    shearGroup.add(brokenSlab);

    for (let r = 0; r < 3; r++) {
      const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 1.35, 6), rebarMat);
      rod.position.set(sx - 0.3 + r * 0.3, y1 - 0.78, sz + 0.12);
      rod.rotation.z = (r - 1) * 0.20;
      shearGroup.add(rod);
    }
  });
  postStrikeModelGroup.add(shearGroup);

  // C) All 4 Surviving Tricolor Front Portico Columns + Canopy + Shattered Open-Sky Front Shell (ref_02b & ref_08)
  for (const colX of [-6.8, -2.3, 2.3, 6.8]) {
    const c = new THREE.Mesh(new THREE.BoxGeometry(0.62, floorH, 0.62), porticoColMat);
    c.position.set(colX, floorH / 2, 4.4);
    c.castShadow = true;
    c.userData = { feature: 'post_portico_col' };
    postStrikeModelGroup.add(c);
  }
  addSlabOrTrim(postStrikeModelGroup, 15.6, 0.40, 2.45, 0.2, floorH + 0.20, 3.625, whiteWall);
  addSlabOrTrim(postStrikeModelGroup, 11.8, 0.40, 1.95, 1.3, floorH + 0.20, 1.475, whiteWall);
  // Standing shattered central front facade wall shell with open sky behind broken window frame (ref_02b left side!)
  addSlabOrTrim(postStrikeModelGroup, 9.8, floorH, 0.34, 2.3, floorH / 2, 0.5, whiteWall);
  addSlabOrTrim(postStrikeModelGroup, 1.6, 2.7, 0.34, -4.2, y1 + 1.35, 0.5, whiteWall);
  addSlabOrTrim(postStrikeModelGroup, 1.6, 2.5, 0.34, -1.2, y1 + 1.25, 0.5, whiteWall);
  addSlabOrTrim(postStrikeModelGroup, 3.4, 0.65, 0.34, -2.7, y1 + 2.35, 0.5, whiteWall);
  addSlabOrTrim(postStrikeModelGroup, 5.8, floorH, 0.34, 4.3, y1 + floorH / 2, 0.5, whiteWall);
  addExteriorWindow(postStrikeModelGroup, 4.1, y1 + 1.75, 0.5, 0, 1.95, 1.35, 1, false);

  // D) Sunken Rubble-Lined 5-Meter Blast Crater Pit at (-2.5, 0, -5.5) + Forensic Scale Rings & Plaque
  const craterPitFloor = new THREE.Mesh(
    new THREE.CircleGeometry(2.52, 32),
    new THREE.MeshStandardMaterial({ color: 0x1c1a18, roughness: 1.0 })
  );
  craterPitFloor.rotation.x = -Math.PI / 2;
  craterPitFloor.position.set(-2.5, 0.04, -5.5);
  postStrikeModelGroup.add(craterPitFloor);

  for (let seg = 0; seg < 18; seg++) {
    const ang = (seg / 18) * Math.PI * 2;
    const rad = 2.52 + (seg % 3) * 0.14;
    const rimChunk = new THREE.Mesh(
      new THREE.DodecahedronGeometry(0.48 + (seg % 2) * 0.12, 0),
      seg % 2 === 0 ? ruinedConcrete : debrisMat
    );
    rimChunk.scale.set(1.35, 0.52, 1.05);
    rimChunk.position.set(
      -2.5 + Math.cos(ang) * rad,
      0.19 + (seg % 3) * 0.05,
      -5.5 + Math.sin(ang) * rad
    );
    rimChunk.rotation.set(0.25 * Math.sin(ang), -ang, 0.25 * Math.cos(ang));
    rimChunk.castShadow = true;
    rimChunk.receiveShadow = true;
    postStrikeModelGroup.add(rimChunk);
  }

  const craterCircleRing = new THREE.Mesh(
    new THREE.RingGeometry(3.05, 3.24, 40),
    new THREE.MeshBasicMaterial({ color: 0xe5e059, side: THREE.DoubleSide })
  );
  craterCircleRing.rotation.x = -Math.PI / 2;
  craterCircleRing.position.set(-2.5, 0.45, -5.5);
  postStrikeModelGroup.add(craterCircleRing);

  const exactFiveMeterRing = new THREE.Mesh(
    new THREE.RingGeometry(2.42, 2.56, 64),
    new THREE.MeshBasicMaterial({ color: 0xef4444, side: THREE.DoubleSide, transparent: true, opacity: 0.92 })
  );
  exactFiveMeterRing.rotation.x = -Math.PI / 2;
  exactFiveMeterRing.position.set(-2.5, 0.48, -5.5);
  postStrikeModelGroup.add(exactFiveMeterRing);

  const craterAxisPts = [
    new THREE.Vector3(-5.0, 0.49, -5.5),
    new THREE.Vector3(0.0, 0.49, -5.5),
    new THREE.Vector3(-2.5, 0.49, -8.0),
    new THREE.Vector3(-2.5, 0.49, -3.0)
  ];
  postStrikeModelGroup.add(new THREE.LineSegments(
    new THREE.BufferGeometry().setFromPoints(craterAxisPts),
    new THREE.LineBasicMaterial({ color: 0xfca5a5, transparent: true, opacity: 0.72 })
  ));

  const scaleCanvas = document.createElement('canvas');
  scaleCanvas.width = 512;
  scaleCanvas.height = 88;
  const sCtx = scaleCanvas.getContext('2d');
  sCtx.fillStyle = 'rgba(15, 18, 28, 0.92)';
  sCtx.fillRect(0, 0, 512, 88);
  sCtx.strokeStyle = '#ef4444';
  sCtx.lineWidth = 4;
  sCtx.strokeRect(2, 2, 508, 84);
  sCtx.textAlign = 'center';
  sCtx.fillStyle = '#fca5a5';
  sCtx.font = 'bold 22px Inter, sans-serif';
  sCtx.fillText('Ø 5.0 m IMPACT CRATER · CENTRAL HALL', 256, 36);
  sCtx.fillStyle = '#fef2f2';
  sCtx.font = 'bold 21px Tahoma, sans-serif';
  sCtx.fillText('قطر دهانه گودال انفجار: ۵ متر (مرکز سالن مدرسه)', 256, 68);
  const scaleTex = new THREE.CanvasTexture(scaleCanvas);
  const scaleBadge = new THREE.Mesh(
    new THREE.PlaneGeometry(4.2, 0.72),
    new THREE.MeshBasicMaterial({ map: scaleTex, side: THREE.DoubleSide })
  );
  scaleBadge.position.set(-2.5, 4.35, -5.5);
  postStrikeModelGroup.add(scaleBadge);

  postStrikeModelGroup.add(new THREE.Line(
    new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(-2.5, 0.5, -5.5),
      new THREE.Vector3(-2.5, 3.99, -5.5)
    ]),
    new THREE.LineBasicMaterial({ color: 0xef4444, transparent: true, opacity: 0.75 })
  ));

  // E) Deterministic Layered Concrete Rubble Slabs in Collapsed West Wing & Central Zone (Zero Math.random jitter!)
  const rubbleSpecs = [
    [-17.2, -11.2, 2.8, 0.32, 2.1, 0.22, 0.4, -0.18],
    [-14.4, -10.8, 3.2, 0.28, 2.4, -0.25, 1.1, 0.20],
    [-11.2, -11.4, 2.5, 0.35, 1.9, 0.18, 2.1, -0.28],
    [-8.4, -10.2, 2.9, 0.30, 2.2, -0.32, 0.7, 0.24],
    [-17.0, -7.2, 3.4, 0.28, 2.5, 0.28, 1.8, 0.16],
    [-13.6, -6.8, 3.0, 0.34, 2.3, -0.20, 2.5, -0.22],
    [-9.8, -6.4, 2.7, 0.30, 2.0, 0.30, 0.9, 0.19],
    [-16.8, -3.2, 3.3, 0.30, 2.4, -0.24, 1.4, -0.15],
    [-13.2, -2.8, 2.9, 0.32, 2.1, 0.21, 2.8, 0.25],
    [-9.5, -2.4, 2.6, 0.28, 1.9, -0.18, 0.5, -0.24],
    [-16.5, 0.6, 3.1, 0.28, 2.2, 0.19, 2.2, 0.14],
    [-12.8, 0.8, 2.8, 0.32, 2.0, -0.26, 1.2, -0.20],
    [-8.9, 0.5, 2.4, 0.30, 1.8, 0.22, 2.6, 0.18],
    [-5.8, -2.2, 2.6, 0.28, 2.0, -0.28, 0.8, 0.22],
    [0.8, -2.4, 2.5, 0.30, 1.9, 0.26, 1.9, -0.25],
    [2.4, -6.2, 2.2, 0.32, 1.7, -0.35, 1.1, 0.30],
    [-0.4, -7.2, 2.1, 0.28, 1.6, 0.32, 2.4, -0.18],
    [-5.6, -6.8, 2.3, 0.30, 1.8, -0.22, 0.3, 0.28]
  ];
  rubbleSpecs.forEach(([rx, rz, rw, rh, rd, rxRot, ryRot, rzRot], idx) => {
    const slab = new THREE.Mesh(
      new THREE.BoxGeometry(rw, rh, rd),
      idx % 3 === 0 ? ruinedConcrete : debrisMat
    );
    slab.position.set(rx, 0.36 + (idx % 3) * 0.22, rz);
    slab.rotation.set(rxRot, ryRot, rzRot);
    slab.castShadow = true;
    slab.receiveShadow = true;
    postStrikeModelGroup.add(slab);
  });

  // F) True L-Shaped Yellow "Extent of Damage" Volume + Clean Perimeter Wireframe (matching ref_08_damage_extent_fa.jpg!)
  // Polygon in XZ: (-19.1, +2.5) -> (-6.9, +2.5) -> (-6.9, +0.6) -> (+4.5, +0.6) -> (+4.5, -8.2) -> (-3.8, -8.2) -> (-3.8, -13.1) -> (-19.1, -13.1)
  const dmgTopY = floorH * 2 + 0.45;
  const dmgPolyXZ = [
    [-19.1, 2.5],
    [-6.9, 2.5],
    [-6.9, 0.6],
    [4.5, 0.6],
    [4.5, -8.2],
    [-3.8, -8.2],
    [-3.8, -13.1],
    [-19.1, -13.1]
  ];
  const dmgShape = new THREE.Shape();
  dmgShape.moveTo(dmgPolyXZ[0][0], -dmgPolyXZ[0][1]);
  for (let i = 1; i < dmgPolyXZ.length; i++) {
    dmgShape.lineTo(dmgPolyXZ[i][0], -dmgPolyXZ[i][1]);
  }
  dmgShape.closePath();

  const dmgExtrude = new THREE.ExtrudeGeometry(dmgShape, { depth: dmgTopY, bevelEnabled: false });
  dmgExtrude.rotateX(-Math.PI / 2);
  const dmgFill = new THREE.Mesh(
    dmgExtrude,
    new THREE.MeshBasicMaterial({ color: 0xe5e059, transparent: true, opacity: 0.13, depthWrite: false, side: THREE.DoubleSide })
  );
  postStrikeModelGroup.add(dmgFill);

  const wirePts = [];
  for (let i = 0; i < dmgPolyXZ.length; i++) {
    const [x1, z1] = dmgPolyXZ[i];
    const [x2, z2] = dmgPolyXZ[(i + 1) % dmgPolyXZ.length];
    wirePts.push(new THREE.Vector3(x1, 0.08, z1), new THREE.Vector3(x2, 0.08, z2));
    wirePts.push(new THREE.Vector3(x1, dmgTopY, z1), new THREE.Vector3(x2, dmgTopY, z2));
    wirePts.push(new THREE.Vector3(x1, 0.08, z1), new THREE.Vector3(x1, dmgTopY, z1));
  }
  postStrikeModelGroup.add(new THREE.LineSegments(
    new THREE.BufferGeometry().setFromPoints(wirePts),
    new THREE.LineBasicMaterial({ color: 0xe5e059 })
  ));

  // G) Camera-Aligned Post-Strike Crater Photogrammetry Frame (Facing West across Crater -> East Exposed Shear!)
  createCameraAlignedPhotoInSpace(
    postStrikeModelGroup,
    'images/fa_spots/spot_crater_photo.jpg',
    [-8.8, 2.35, -5.5],
    [0.8, 2.30, -5.5],
    -Math.PI / 2,
    5.1,
    2.85
  );
}

// --- CYCLE FLOORPLAN CUTAWAY (0 = Full, 1 = First Floor Cutaway, 2 = Ground Floor Cutaway) ---
function setCutawayMode(mode) {
  cutawayState = mode % 3;
  const btn = document.getElementById('btnCutaway');

  if (cutawayState === 0) {
    roofGroup.visible = true;
    firstFloorGroup.visible = true;
    groundFloorGroup.visible = true;
    if (btn) btn.textContent = currentLang === 'fa' ? '🏠 برش طبقات: نمای کامل' : (currentLang === 'fi' ? '🏠 Leikkaus: Koko rakennus' : '🏠 Floorplan Cutaway: Full Building');
  } else if (cutawayState === 1) {
    roofGroup.visible = false;
    firstFloorGroup.visible = true;
    groundFloorGroup.visible = true;
    if (btn) btn.textContent = currentLang === 'fa' ? '🏠 برش طبقات: طبقه اول (دبستان دخترانه)' : (currentLang === 'fi' ? '🏠 Leikkaus: 2. kerros (Tytöt)' : '🏠 Cutaway: 1st Floor (Girls\' School)');
  } else {
    roofGroup.visible = false;
    firstFloorGroup.visible = false;
    groundFloorGroup.visible = true;
    if (btn) btn.textContent = currentLang === 'fa' ? '🏠 برش طبقات: طبقه همکف (دبستان پسرانه)' : (currentLang === 'fi' ? '🏠 Leikkaus: 1. kerros (Pojat)' : '🏠 Cutaway: Ground Floor (Boys\' School)');
  }
}

// --- 8 CAMERA-ALIGNED HOTSPOTS (SYNCHRONIZED TO ALIGNED ROOMS & COURTYARDS) ---
const HOTSPOT_CONFIGS = [
  { id: 'courtyard_lines', icon: '1', pos: [15.5, 1.2, 8.25], presetCam: [5.5, 2.8, 12.0], target: [22.0, 1.6, 6.5], cutaway: 0 },
  { id: 'boys_flower_arch', icon: '2', pos: [3.8, 2.1, -6.0], presetCam: [2.2, 4.4, -0.5], target: [4.0, 1.8, -6.5], cutaway: 2 },
  { id: 'boys_classroom', icon: '3', pos: [-15.8, 2.1, -0.2], presetCam: [-11.8, 4.3, 3.8], target: [-16.2, 1.6, -1.0], cutaway: 2 },
  { id: 'rainbow_staircase', icon: '4', pos: [-1.8, 2.3, -8.4], presetCam: [-1.8, 2.25, -3.2], target: [-1.8, 2.0, -9.8], cutaway: 2 },
  { id: 'girls_upper_hall', icon: '5', pos: [-15.2, 5.6, -5.5], presetCam: [-9.5, 8.6, 3.5], target: [-15.2, 5.2, -5.5], cutaway: 1 },
  { id: 'crater_damage', icon: '6', pos: [-2.5, 3.2, -5.5], presetCam: [-18.0, 13.5, 12.0], target: [-1.5, 2.2, -5.5], cutaway: 0 },
  { id: 'second_wave', icon: '7', pos: [18.0, 2.5, 11.5], presetCam: [26.0, 9.5, 22.0], target: [6.0, 2.2, 1.0], cutaway: 0 },
  { id: 'vow_shrine', icon: '✍️', pos: [-1.5, 3.8, 10.5], presetCam: [-1.5, 2.4, 18.0], target: [-1.5, 2.0, 10.5], isVow: true, cutaway: 1 }
];

function initHotspots() {
  const container = document.getElementById('canvasContainer');

  HOTSPOT_CONFIGS.forEach(cfg => {
    cfg.posVec = new THREE.Vector3(cfg.pos[0], cfg.pos[1], cfg.pos[2]);
    cfg.presetCamVec = new THREE.Vector3(cfg.presetCam[0], cfg.presetCam[1], cfg.presetCam[2]);
    cfg.targetVec = new THREE.Vector3(cfg.target[0], cfg.target[1], cfg.target[2]);

    const markerMesh = new THREE.Mesh(
      new THREE.SphereGeometry(0.11, 12, 12),
      new THREE.MeshBasicMaterial({ color: cfg.isVow ? 0x10b981 : 0xd4a853, transparent: true, opacity: cfg.isVow ? 0.0 : 0.42 })
    );
    markerMesh.visible = !cfg.isVow;
    markerMesh.position.copy(cfg.posVec);
    markersGroup.add(markerMesh);
    cfg.mesh = markerMesh;

    const el = document.createElement('div');
    el.className = 'hotspot-pin' + (cfg.isVow ? ' vow-pin' : '');
    el.id = `hotspot-pin-${cfg.id}`;
    el.innerHTML = `
      <div class="pin-pulse"></div>
      <div class="pin-icon">${cfg.icon}</div>
      <div class="pin-tooltip" id="tooltip-${cfg.id}"></div>
    `;
    el.addEventListener('click', (e) => {
      e.stopPropagation();
      if (cfg.isVow) {
        triggerCameraAnimation(cfg.presetCamVec, cfg.targetVec);
        openVowModal();
      } else {
        selectHotspot(cfg.id);
      }
    });
    container.appendChild(el);
    cfg.domElement = el;
  });

  updateHotspotLabels();
}

function updateHotspotLabels() {
  const t = I18N_DATA[currentLang] || I18N_DATA.en;
  HOTSPOT_CONFIGS.forEach(cfg => {
    const tip = document.getElementById(`tooltip-${cfg.id}`);
    if (tip && t.hotspots[cfg.id]) {
      tip.textContent = t.hotspots[cfg.id].title;
    }
  });
}

function updateHotspotPositions() {
  const container = document.getElementById('canvasContainer');
  const width = container.clientWidth;
  const height = container.clientHeight;
  const tempV = new THREE.Vector3();
  const currentTourStopId = isGuidedTour && GUIDED_TOUR_STOPS[currentTourIndex]
    ? GUIDED_TOUR_STOPS[currentTourIndex].hotspotId
    : null;

  HOTSPOT_CONFIGS.forEach(cfg => {
    const isPostStrikePin = cfg.id === 'crater_damage' || cfg.id === 'second_wave';
    if (damageSliderValue < 0.35 && isPostStrikePin && currentTourStopId !== cfg.id) {
      cfg.domElement.style.display = 'none';
      return;
    }
    if (damageSliderValue >= 0.65 && !isPostStrikePin && cfg.id !== 'vow_shrine' && currentTourStopId !== cfg.id) {
      cfg.domElement.style.display = 'none';
      return;
    }
    if (cutawayState === 2 && cfg.id === 'girls_upper_hall' && currentTourStopId !== cfg.id) {
      cfg.domElement.style.display = 'none';
      return;
    }

    tempV.copy(cfg.posVec);
    tempV.project(camera);

    if (tempV.z > 1.0) {
      cfg.domElement.style.display = 'none';
      return;
    }

    cfg.domElement.style.display = 'block';
    cfg.domElement.classList.toggle('active-pin', currentTourStopId === cfg.id || activeHotspotId === cfg.id);
    const x = (tempV.x * 0.5 + 0.5) * width;
    const y = (-tempV.y * 0.5 + 0.5) * height;
    cfg.domElement.style.transform = `translate(-50%, -50%) translate(${x}px, ${y}px)`;
  });
}

function selectHotspot(id) {
  activeHotspotId = id;
  const cfg = HOTSPOT_CONFIGS.find(c => c.id === id);
  if (!cfg) return;

  if (id === 'crater_damage' || id === 'second_wave') {
    setTemporalCondition(1.0);
    document.getElementById('timelineSlider').value = 1.0;
  } else {
    setTemporalCondition(0.0);
    document.getElementById('timelineSlider').value = 0.0;
    if (typeof cfg.cutaway === 'number') {
      setCutawayMode(cfg.cutaway);
    }
  }

  triggerCameraAnimation(cfg.presetCamVec, cfg.targetVec);
  showHotspotModal(id);
}

function showHotspotModal(id) {
  activeHotspotId = id;
  const t = I18N_DATA[currentLang] || I18N_DATA.en;
  const data = t.hotspots[id];
  if (!data) return;

  document.getElementById('modalTitle').textContent = data.title;
  document.getElementById('modalCategory').textContent = data.category;
  document.getElementById('modalDesc').textContent = data.desc;
  document.getElementById('modalFinding').textContent = data.finding;
  document.getElementById('modalRef').textContent = data.evidenceRef;

  // Dedicated instant-start room video clip
  const videoPlayer = document.getElementById('modalVideoPlayer');
  if (videoPlayer && data.videoFile) {
    videoPlayer.src = data.videoFile;
    videoPlayer.loop = true;
    videoPlayer.muted = true;
    videoPlayer.currentTime = 0;
    videoPlayer.play().catch(() => {});
  }

  // Camera-Aligned Spot Frame Image
  const spotImg = document.getElementById('modalSpotImg');
  const spotCaption = document.getElementById('modalSpotCaption');
  if (spotImg && data.spotImg) {
    spotImg.src = data.spotImg;
  }
  if (spotCaption && data.spotCaption) {
    spotCaption.textContent = data.spotCaption;
  }

  // Testimony Box
  const testBox = document.getElementById('modalTestimonyBox');
  if (data.testimonyQuote) {
    document.getElementById('modalTestimonyQuote').textContent = data.testimonyQuote;
    document.getElementById('modalTestimonyAuthor').textContent = data.testimonyAuthor || '';
    testBox.classList.add('active');
  } else {
    testBox.classList.remove('active');
  }

  // Wing-Specific Children & Educators Portraits Strip (Dataset v3.0.0)
  const kidsStrip = document.getElementById('modalKidsStrip');
  const stripCountEl = document.getElementById('modalKidsStripCount');
  kidsStrip.innerHTML = '';

  const isFa = currentLang === 'fa';
  let wingVictims = [];
  let wingDrawings = [];

  if (id === 'courtyard_lines') {
    // Teacher Zohreh Shahriyari (who was in the yard) + Grade 1 & 2 pupils
    const zohreh = teachersList.find(t => t.id === 'zohreh-shahriyari');
    const g12 = childrenList.filter(c => c.photoPath && (c.grade === 1 || c.grade === 2)).slice(0, 14);
    wingVictims = zohreh ? [zohreh, ...g12] : g12;
    wingDrawings = drawingsList.filter(d => ['drawing-01', 'drawing-09', 'drawing-11', 'drawing-14'].includes(d.id));
  } else if (id === 'boys_flower_arch') {
    // Ground Floor East Ceremony Room: Boys of Grades 4, 5 & 6 + Grade 1–2 Ceremony Boys
    wingVictims = childrenList.filter(c => c.gender === 'boy' && c.photoPath && (c.grade >= 4 || c.grade === 1)).slice(0, 18);
    wingDrawings = drawingsList.filter(d => ['drawing-05', 'drawing-06', 'drawing-07', 'drawing-15', 'drawing-18'].includes(d.id));
  } else if (id === 'boys_classroom') {
    // Ground Floor West Classroom: Boys of Grades 1, 2 & 3
    wingVictims = childrenList.filter(c => c.gender === 'boy' && c.photoPath && c.grade <= 3).slice(0, 20);
    wingDrawings = drawingsList.filter(d => ['drawing-09', 'drawing-11', 'drawing-13', 'drawing-16', 'drawing-19'].includes(d.id));
  } else if (id === 'rainbow_staircase') {
    // Central Rainbow Staircase & Hall: All 26 Female Educators + Principal Fariba Jafari
    wingVictims = [...teachersList, ...childrenList.filter(c => c.photoPath).slice(0, 6)];
    wingDrawings = drawingsList.filter(d => ['drawing-04', 'drawing-10', 'drawing-23', 'drawing-24', 'drawing-26'].includes(d.id));
  } else if (id === 'girls_upper_hall') {
    // First Floor Girls' School: All 47 Martyred Schoolgirls (prioritizing Baran Ghasemi & Fatemeh Rahdar first)
    const baran = childrenList.find(c => c.id === 'baran-ghasemy');
    const fatemehR = childrenList.find(c => c.id === 'fatemeh-rahdar');
    const otherGirls = childrenList.filter(c => c.gender === 'girl' && c.photoPath && c.id !== 'baran-ghasemy' && c.id !== 'fatemeh-rahdar');
    wingVictims = [baran, fatemehR, ...otherGirls].filter(Boolean);
    wingDrawings = drawingsList.filter(d => ['drawing-02', 'drawing-27', 'drawing-03', 'drawing-12', 'drawing-20', 'drawing-23'].includes(d.id));
  } else if (id === 'crater_damage') {
    // Central Assembly Hall & Prayer Room Blast Zone
    wingVictims = [
      ...teachersList.slice(0, 6),
      ...childrenList.filter(c => c.photoPath && (c.grade === 3 || c.grade === 4)).slice(0, 14)
    ];
    wingDrawings = drawingsList.filter(d => d.hasBlastDamage || ['drawing-16', 'drawing-17', 'drawing-19', 'drawing-21', 'drawing-22'].includes(d.id));
  } else {
    // Second Wave / Vow Shrine: Cross-school representation across all 6 grades & educators
    wingVictims = [
      ...childrenList.filter(c => c.photoPath).slice(0, 12),
      ...teachersList.slice(0, 6)
    ];
    wingDrawings = drawingsList.slice(0, 8);
  }

  if (stripCountEl) {
    stripCountEl.textContent = isFa
      ? `${wingVictims.length} تصویر استودیویی — برای مشاهده شناسنامه کلیک کنید`
      : `${wingVictims.length} verified studio portraits · Click any portrait to inspect`;
  }

  wingVictims.forEach(person => {
    const card = document.createElement('a');
    card.className = 'kid-mini-card';
    card.href = `child.html?id=${encodeURIComponent(person.id)}`;
    const displayName = (isFa && person.nameFa) ? person.nameFa : person.name;
    const roleOrGrade = person.category === 'teacher'
      ? (isFa ? (person.roleFa || 'آموزگار شهیده') : (person.role || 'Educator'))
      : (isFa
          ? `پایه ${person.grade || '؟'}${person.age ? ' · ' + person.age + ' ساله' : ''}`
          : `Grade ${person.grade || '?'}${person.age ? ' · Age ' + person.age : ''}`);
    const imgSrc = person.photoPath || person.photo_path || 'images/children/amin-ahmadzade.jpg';
    card.innerHTML = `
      <img src="${imgSrc}" alt="${displayName}" loading="lazy" />
      <span class="kid-name">${displayName}</span>
      <span class="kid-meta">${roleOrGrade}</span>
    `;
    kidsStrip.appendChild(card);
  });

  // Populate Rubble Drawings Strip for this Wing
  const drwWrap = document.getElementById('modalDrawingsStripWrap');
  const drwStrip = document.getElementById('modalDrawingsStrip');
  if (drwWrap && drwStrip) {
    drwStrip.innerHTML = '';
    if (wingDrawings.length > 0) {
      drwWrap.style.display = 'block';
      wingDrawings.forEach(drw => {
        const dCard = document.createElement('div');
        dCard.className = 'drawing-mini-card';
        const dTitle = (drw.title && drw.title[currentLang]) || (drw.title && drw.title.en) || drw.id;
        const dAuthor = isFa ? (drw.studentNameFa || 'دانش‌آموز شهید') : (drw.studentNameEn || 'Elementary Student');
        dCard.innerHTML = `
          <img src="${drw.thumb || drw.image}" alt="${dTitle}" loading="lazy" />
          <span class="drw-title">${dTitle}</span>
          <span class="drw-author">${dAuthor}</span>
        `;
        dCard.addEventListener('click', () => {
          openArtifactInspector({
            artifactType: 'drawing',
            item: drw,
            wingLabel: data.title
          });
        });
        drwStrip.appendChild(dCard);
      });
    } else {
      drwWrap.style.display = 'none';
    }
  }

  document.getElementById('evidenceModal').classList.add('visible');
}

function closeModal() {
  document.getElementById('evidenceModal').classList.remove('visible');
  const videoPlayer = document.getElementById('modalVideoPlayer');
  if (videoPlayer) {
    videoPlayer.pause();
  }
  activeHotspotId = null;
}

// --- MULTI-NARRATOR HUMAN VOICEOVER + REAL ARCHIVAL SCHOOL ECHOES + ROOM ATMOSPHERE ENGINE ---
let narrationAudio = null;
let archivalAudio = null;
let narrationPhase = 'idle'; // 'idle' | 'archival' | 'delay' | 'voice'
let narrationPhaseTimer = null;
let activeNarrationHotspot = null;
let narrationRate = 1.0;
let ambientAudioCtx = null;
let ambientGainNode = null;
let ambientPadFilter = null;
let ambientOscillators = [];
let ambientBreezeGain = null;
let ambientBreezeFilter = null;
let ambientBirdTimer = null;
let guidedTourAutoAdvanceTimer = null;
let tourManualCameraOverride = false;
let tourStepStartTime = 0;
let walkthroughIdleTimer = null;
let supportsDisplayTransition;
let deterministicWalkthroughRender = false;
let activePipReelUrl = '';
const pipBlobCache = new Map();

const NARRATOR_PROFILES = {
  mostafa_fa: {
    id: 'mostafa_fa',
    lang: 'fa',
    prefix: 'fa',
    dir: 'voices/mostafa_fa',
    fallbackDir: 'voices/leila_fa',
    hudLabel: { en: 'Voice: Mostafa (FA)', fa: 'راوی: مصطفی جلالی', fi: 'Ääni: Mostafa (FA)' },
    shortLabel: { en: '🎙️ Mostafa', fa: '🎙️ مصطفی جلالی', fi: '🎙️ Mostafa' }
  },
  leila_fa: {
    id: 'leila_fa',
    lang: 'fa',
    prefix: 'fa',
    dir: 'voices/leila_fa',
    fallbackDir: 'voices/mostafa_fa',
    hudLabel: { en: 'Voice: Leila (FA)', fa: 'راوی: لیلا غضنفری', fi: 'Ääni: Leila (FA)' },
    shortLabel: { en: '🎙️ Leila', fa: '🎙️ لیلا غضنفری', fi: '🎙️ Leila' }
  },
  leila_en: {
    id: 'leila_en',
    lang: 'en',
    prefix: 'en',
    dir: 'voices/leila_en',
    fallbackDir: 'voices/leila_en',
    hudLabel: { en: 'Voice: Leila (EN)', fa: 'راوی: لیلا (EN)', fi: 'Ääni: Leila (EN)' },
    shortLabel: { en: '🎙️ Leila', fa: '🎙️ لیلا (EN)', fi: '🎙️ Leila' }
  },
  ali_en: {
    id: 'ali_en',
    lang: 'en',
    prefix: 'en',
    dir: 'voices/ali_en',
    fallbackDir: 'voices/leila_en',
    hudLabel: { en: 'Voice: Ali (EN)', fa: 'راوی: علی (EN)', fi: 'Ääni: Ali (EN)' },
    shortLabel: { en: '🎙️ Ali', fa: '🎙️ علی (EN)', fi: '🎙️ Ali' }
  }
};

let activeVoiceProfile = 'leila_en';
const preferredVoiceByLang = {
  fa: 'mostafa_fa',
  en: 'leila_en'
};

function updateNarratorButtonsUI() {
  const prof = NARRATOR_PROFILES[activeVoiceProfile] || NARRATOR_PROFILES.leila_en;
  const labelText = prof.hudLabel[currentLang] || prof.hudLabel.en;
  const hudLbl = document.getElementById('hudNarratorLabel');
  if (hudLbl) hudLbl.textContent = labelText;
  const subLbl = document.getElementById('subrowNarratorLabel');
  if (subLbl) subLbl.textContent = labelText;
  const storyBtn = document.getElementById('btnStoryNarrator');
  if (storyBtn) {
    storyBtn.textContent = prof.shortLabel[currentLang] || prof.shortLabel.en;
  }
}

function setNarratorProfile(profileId, restartAudio = true) {
  const prof = NARRATOR_PROFILES[profileId];
  if (!prof) return;
  activeVoiceProfile = profileId;
  preferredVoiceByLang[prof.lang] = profileId;
  if (prof.lang === 'fa' && currentLang !== 'fa') {
    currentLang = 'fa';
    localStorage.setItem('pfp_lang', 'fa');
    applyTranslations();
    updateHotspotLabels();
  } else if (prof.lang === 'en' && currentLang === 'fa') {
    currentLang = 'en';
    localStorage.setItem('pfp_lang', 'en');
    applyTranslations();
    updateHotspotLabels();
  }
  updateNarratorButtonsUI();
  if (restartAudio && isGuidedTour) {
    const stop = GUIDED_TOUR_STOPS[currentTourIndex];
    if (stop) playSpotNarration(stop.hotspotId);
  } else if (restartAudio && activeNarrationHotspot && isSpotAudioPlaying()) {
    playSpotNarration(activeNarrationHotspot);
  }
}
window.setNarratorProfile = setNarratorProfile;

function cycleNarratorForCurrentLanguage() {
  if (currentLang === 'fa') {
    const nextFa = activeVoiceProfile === 'mostafa_fa' ? 'leila_fa' : 'mostafa_fa';
    setNarratorProfile(nextFa, true);
  } else {
    const nextEn = activeVoiceProfile === 'leila_en' ? 'ali_en' : 'leila_en';
    setNarratorProfile(nextEn, true);
  }
}

const WALKTHROUGH_VISUAL_CONFIG = {
  courtyard_lines: {
    phase: 'pre',
    stamp: {
      en: 'FEB 28, 2026 · MORNING BEFORE THE STRIKE · MINAB SCHOOLYARD',
      fa: '۹ اسفند ۱۴۰۴ · صبح پیش از حمله · حیاط دبستان شجره طیبه میناب',
      fi: '28.2.2026 · AAMU ENNEN ISKUA · MINABIN KOULUPIHA'
    },
    pipReel: 'media/fa/real_inserts/reel_01_courtyard.mp4',
    pipBadge: { en: 'VERIFIED ARCHIVE FOOTAGE', fa: 'تصاویر مستند و آرشیوی مدرسه', fi: 'VARMENNETTU ARKISTOKUVA' },
    pipCaption: {
      en: 'Yellow morning assembly lines & pastel courtyard walls before the strike',
      fa: 'خطوط زرد صف صبحگاهی و دیوارهای رنگی حیاط مدرسه پیش از حمله',
      fi: 'Koulupihan keltaiset aamurivit ja pastellisävyinen muuri ennen iskua'
    },
    quote: {
      tone: 'pre',
      text: {
        en: '"When the first missile hit, teacher Ms. Shahriari ran toward a classroom to bring her students out — then the second hit."',
        fa: '«وقتی موشک اول اصابت کرد، خانم شهریاری به سمت کلاس دوید تا شاگردانش را بیرون بیاورد که موشک دوم فرود آمد.»',
        fi: '"Kun ensimmäinen ohjus osui, opettaja Shahriari juoksi luokkaan pelastamaan oppilaitaan — silloin toinen osui."'
      },
      author: {
        en: '— Wajiheh Zakari, Teacher at Shajareh Tayyebeh School',
        fa: '— وجیهه ذاکری، آموزگار دبستان شجره طیبه',
        fi: '— Wajiheh Zakari, koulun opettaja'
      }
    }
  },
  boys_flower_arch: {
    phase: 'pre',
    stamp: {
      en: 'GROUND FLOOR · BOYS\' CEREMONY ROOM · BEFORE THE STRIKE',
      fa: 'طبقه همکف · اتاق جشن پسران · روزهای روشن پیش از حمله',
      fi: 'ALAKERTA · POIKIEN JUHLAHUONE · ENNEN ISKUA'
    },
    pipReel: 'media/fa/real_inserts/reel_02_boys_arch.mp4',
    pipBadge: { en: 'CAMERA-MATCHED SCHOOL ARCHIVE', fa: 'آرشیو مدرسه · منطبق بر اتاق سه‌بعدی', fi: 'KOULUN ARKISTOKUVA' },
    pipCaption: {
      en: 'Boys in royal blue uniforms celebrating beneath red rose arches',
      fa: 'دانش‌آموزان پسر با لباس فرم آبی در جشن مدرسه زیر طاق گل‌های رز',
      fi: 'Sinipukuiset koulupojat juhlimassa punaisten ruusukaarten alla'
    }
  },
  boys_classroom: {
    phase: 'pre',
    stamp: {
      en: 'GROUND FLOOR WEST · BOYS\' CLASSROOM · JAN–FEB 2026',
      fa: 'طبقه همکف (بال غربی) · کلاس درس پسران · زمستان ۱۴۰۴',
      fi: 'ALAKERTA · POIKIEN LUOKKAHUONE · TALVI 2026'
    },
    pipReel: 'media/fa/real_inserts/reel_03_boys_classroom.mp4',
    pipBadge: { en: 'BEFORE & AFTER IN THE SAME ROOM', fa: 'تصویر واقعی کلاس پیش و پس از حمله', fi: 'ENNEN JA JÄLKEEN SAMASSA LUOKASSA' },
    pipCaption: {
      en: '35+ boys clapping & singing together — and the same sky-blue room after the strike',
      fa: 'هم‌خوانی و دست زدن بیش از ۳۵ دانش‌آموز پسر — و همان کلاس آبی پس از حمله',
      fi: 'Yli 35 poikaa taputtamassa ja laulamassa — ja sama sininen luokka iskun jälkeen'
    }
  },
  rainbow_staircase: {
    phase: 'pre',
    stamp: {
      en: 'CENTRAL HALL · RAINBOW STAIRCASE & PURPLE DOORS',
      fa: 'سالن مرکزی · راه‌پله رنگین‌کمان و درهای بنفش کلاس‌ها',
      fi: 'KESKUSSALI · SATEENKAARIPORTAIKKO JA VIOLETIT OVET'
    },
    pipReel: 'media/fa/real_inserts/reel_04_rainbow_stairs.mp4',
    pipBadge: { en: 'VERIFIED SCHOOL ARCHIVE', fa: 'آرشیو راستی‌آزمایی‌شده مدرسه', fi: 'VARMENNETTU KOULUARKISTO' },
    pipCaption: {
      en: 'Teachers welcoming girls at the rainbow stairs & children coloring workbooks',
      fa: 'استقبال معلمان در پای پله‌های رنگین‌کمان و رنگ‌آمیزی دفتر مشق کودکان',
      fi: 'Opettajat vastassa sateenkaariportailla ja lapset värittämässä vihkojaan'
    },
    quote: {
      tone: 'strike',
      text: {
        en: '"I stretched out my hand to pull my books toward myself — then the second strike hit and I was thrown under the rubble."',
        fa: '«دستم را دراز کردم تا کتاب‌هایم را به سمت خودم بکشم که موج بعدی اصابت کرد و زیر آوار رفتم.»',
        fi: '"Ojensin käteni vetääkseni kirjani luokseni — sitten toinen isku osui ja jäin raunioiden alle."'
      },
      author: {
        en: '— Parastesh Zaeri, 11-year-old survivor (her 8-year-old brother Ali Asghar was killed)',
        fa: '— پرستش زائری، دانش‌آموز ۱۱ ساله بازمانده (خواهر شهید ۸ ساله علی‌اصغر زائری)',
        fi: '— Parastesh Zaeri, 11-vuotias selviytyjä'
      }
    }
  },
  girls_upper_hall: {
    phase: 'pre',
    stamp: {
      en: 'FIRST FLOOR WEST · GIRLS\' PRIMARY SCHOOL ASSEMBLY HALL',
      fa: 'طبقه اول (بال غربی) · سالن بزرگ و کلاس‌های دبستان دخترانه',
      fi: 'YLÄKERTA · TYTTÖKOULUN SUURI SALI'
    },
    pipReel: 'media/fa/real_inserts/reel_05_girls_hall.mp4',
    pipBadge: { en: 'CAMERA-MATCHED UPPER FLOOR', fa: 'تصاویر واقعی طبقه اول دخترانه', fi: 'YLÄKERRAN ARKISTOKUVA' },
    pipCaption: {
      en: '80+ schoolgirls in white headscarves seated shoulder-to-shoulder on the green carpet',
      fa: 'حضور بیش از ۸۰ دانش‌آموز دختر در کنار دوستانشان روی فرش سبز طبقه اول',
      fi: 'Yli 80 koulutyttöä istumassa vierekkäin yläkerran vihreällä matolla'
    }
  },
  crater_damage: {
    phase: 'strike',
    stamp: {
      en: 'FEB 28, 2026 · 11:22 AM — DIRECT CRUISE MISSILE IMPACT (Ø 5m)',
      fa: '۹ اسفند ۱۴۰۴ · ساعت ۱۱:۲۲ صبح — اصابت مستقیم موشک کروز و گودال ۵ متری',
      fi: '28.2.2026 · KLO 11.22 — SUORA RISTEILYOHJUSOSUMA (5m KRAATTERI)'
    },
    pipReel: 'media/fa/real_inserts/reel_06_crater.mp4',
    pipBadge: { en: 'ON-SITE POST-STRIKE FOOTAGE', fa: 'تصاویر میدانی محل فروریزش و گودال ۵ متری', fi: 'KUVAMATERIAALI ISKUPAIKALTA' },
    pipCaption: {
      en: 'Sheared two-story central hall, 5-meter crater & a child\'s pink ball left in the dust',
      fa: 'برش دو طبقه فروریخته سالن مرکزی، گودال ۵ متری و توپ صورتی به‌جامانده در خاک',
      fi: 'Romahtanut kaksikerroksinen keskussali, 5 metrin kraatteri ja lapsen pallo pölyssä'
    },
    quote: {
      tone: 'strike',
      text: {
        en: '156 civilians killed — including 120+ young schoolchildren and 26 female educators inside these two floors.',
        fa: 'شهادت ۱۵۶ غیرنظامی — از جمله بیش از ۱۲۰ کودک دانش‌آموز و ۲۶ آموزگار در همین دو طبقه.',
        fi: '156 siviiliä sai surmansa — heidän joukossaan yli 120 koululaista ja 26 opettajaa.'
      },
      author: {
        en: '— Verified Casualty & Forensic Spatial Record (Investigation 121 / PFPJ ry)',
        fa: '— مستندات راستی‌آزمایی‌شده مکانی و فهرست جامع شهدا (PFPJ ry)',
        fi: '— Varmennettu uhri- ja paikkatietorekisteri (PFPJ ry)'
      }
    }
  },
  second_wave: {
    phase: 'strike',
    stamp: {
      en: 'FEB 28, 2026 · 02:30 PM — SECOND STRIKE WAVE ON FAMILIES & RESCUERS',
      fa: '۹ اسفند ۱۴۰۴ · ساعت ۱۴:۳۰ — موج دوم موشک‌های تاماهاک میان مادران و امدادگران',
      fi: '28.2.2026 · KLO 14.30 — TOINEN ISKUAALTO PERHEIDEN JA PELASTAJIEN KESKELLE'
    },
    pipReel: 'media/fa/real_inserts/reel_07_second_wave.mp4',
    pipBadge: { en: 'VERIFIED INCIDENT FOOTAGE', fa: 'ویدیوهای مستند لحظه اصابت و حیاط مدرسه', fi: 'VARMENNETTU TAPAHTUMAVIDEO' },
    pipCaption: {
      en: 'Cruise missile descending & hundreds of mothers and rescuers in the smoke-filled yard',
      fa: 'فرود موشک کروز و حضور صدها مادر و امدادگر در حیاط پر از دود و غبار مدرسه',
      fi: 'Risteilyohjus syöksymässä ja satoja äitejä sekä pelastajia savuisella koulupihalla'
    },
    quote: {
      tone: 'strike',
      text: {
        en: '"All the mothers and families were in the crowded yard... Red Crescent rescuers grabbed my hand saying we were being targeted again."',
        fa: '«همه مادرها در حیاط شلوغ مدرسه بودند... نیروهای هلال‌احمر دستم را کشیدند که منطقه دوباره هدف قرار گرفته است.»',
        fi: '"Kaikki äidit ja perheet olivat täydellä pihalla... Punaisen Puolikuun pelastajat vetivät minut turvaan."'
      },
      author: {
        en: '— Khadija Ahmedizadeh, Mother of 9-year-old Mohammad Taha Jafari',
        fa: '— خدیجه احمدی‌زاده، مادر داغدار دانش‌آموز ۹ ساله محمدطه جعفری',
        fi: '— Khadija Ahmedizadeh, 9-vuotiaan Mohammad Taha Jafarin äiti'
      }
    }
  },
  vow_shrine: {
    phase: 'memorial',
    stamp: {
      en: 'SHAJAREH TAYYEBEH MEMORIAL · GLOBAL ACCOUNTABILITY VOW',
      fa: 'یادمان دبستان شجره طیبه · میثاق جهانی دادخواهی کودکان میناب',
      fi: 'SHAJAREH TAYYEBEHIN MUISTOMERKKI · KANSAINVÄLINEN VASTUULUPAUS'
    },
    pipReel: 'media/fa/real_inserts/reel_08_memorial.mp4',
    pipBadge: { en: 'REMEMBRANCE & ACCOUNTABILITY', fa: 'یادبود و میثاق دادخواهی', fi: 'MUISTO JA OIKEUDELLINEN VASTUU' },
    pipCaption: {
      en: 'A grieving father holding his child\'s schoolbag & portrait before the ruined classrooms',
      fa: 'پدر داغدار با کیف مدرسه و تصویر فرزندش در برابر کلاس‌های فروریخته دبستان',
      fi: 'Sureva isä pitelemässä lapsensa koulureppua ja muotokuvaa raunioiden edessä'
    }
  }
};

async function initWalkthroughPipManifest() {
  try {
    const resp = await fetch('media/walkthrough_pip/manifest.json', { cache: 'no-store' });
    if (!resp.ok) return;
    const data = await resp.json();
    const stationsMap = (data && data.stations) ? data.stations : data;
    if (!stationsMap || typeof stationsMap !== 'object') return;
    Object.keys(WALKTHROUGH_VISUAL_CONFIG).forEach((hotspotId) => {
      const extCfg = stationsMap[hotspotId];
      if (!extCfg) return;
      if (typeof extCfg.video === 'string' && extCfg.video.trim()) {
        WALKTHROUGH_VISUAL_CONFIG[hotspotId].pipReel = extCfg.video.trim();
      }
      if (extCfg.caption && typeof extCfg.caption === 'object') {
        WALKTHROUGH_VISUAL_CONFIG[hotspotId].pipCaption = {
          ...WALKTHROUGH_VISUAL_CONFIG[hotspotId].pipCaption,
          ...extCfg.caption
        };
      }
    });
  } catch (_) {
    // Track 2 manifest is optional; built-in verified reels remain active.
  }
}

async function resolvePipVideoSrc(reelUrl) {
  if (!reelUrl) return '';
  if (pipBlobCache.has(reelUrl)) return pipBlobCache.get(reelUrl);
  try {
    const resp = await fetch(reelUrl);
    if (!resp.ok) return reelUrl;
    const blob = await resp.blob();
    const blobUrl = URL.createObjectURL(blob);
    pipBlobCache.set(reelUrl, blobUrl);
    return blobUrl;
  } catch (_) {
    return reelUrl;
  }
}

async function preloadAllWalkthroughPipBlobs() {
  const urls = Object.values(WALKTHROUGH_VISUAL_CONFIG).map((c) => c.pipReel).filter(Boolean);
  await Promise.all(urls.map((u) => resolvePipVideoSrc(u)));
}
window.preloadAllWalkthroughPipBlobs = preloadAllWalkthroughPipBlobs;

const SPOT_ARCHIVAL_AUDIO = {
  courtyard_lines:   { file: 'courtyard_lines.mp3',   expectedDur: 6.65 },
  boys_flower_arch:  { file: 'boys_flower_arch.mp3',  expectedDur: 11.18 },
  boys_classroom:    { file: 'boys_classroom.mp3',    expectedDur: 6.75 },
  rainbow_staircase: { file: 'rainbow_staircase.mp3', expectedDur: 7.00 },
  girls_upper_hall:  { file: 'girls_upper_hall.mp3',  expectedDur: 6.25 },
  vow_shrine:        { file: 'vow_shrine.mp3',        expectedDur: 7.40 }
};

const ROOM_ATMOSPHERE_PROFILES = {
  courtyard_lines:   { freqs: [130.81, 174.61, 196.00, 261.63], padGain: 0.011, padCutoff: 380, breezeFreq: 430, breezeQ: 0.65, breezeGain: 0.015, birdGain: 0.0042, chime: false },
  boys_flower_arch:  { freqs: [130.81, 164.81, 196.00, 246.94], padGain: 0.011, padCutoff: 320, breezeFreq: 290, breezeQ: 0.80, breezeGain: 0.007, birdGain: 0.0020, chime: false },
  boys_classroom:    { freqs: [130.81, 164.81, 196.00, 246.94], padGain: 0.011, padCutoff: 310, breezeFreq: 270, breezeQ: 0.85, breezeGain: 0.006, birdGain: 0.0016, chime: false },
  rainbow_staircase: { freqs: [130.81, 155.56, 196.00, 233.08], padGain: 0.014, padCutoff: 280, breezeFreq: 240, breezeQ: 0.90, breezeGain: 0.006, birdGain: 0.0,    chime: false },
  girls_upper_hall:  { freqs: [130.81, 155.56, 196.00, 233.08], padGain: 0.014, padCutoff: 290, breezeFreq: 250, breezeQ: 0.85, breezeGain: 0.006, birdGain: 0.0,    chime: false },
  crater_damage:     { freqs: [65.41,  130.81, 155.56, 196.00], padGain: 0.020, padCutoff: 260, breezeFreq: 205, breezeQ: 0.95, breezeGain: 0.019, birdGain: 0.0,    chime: false },
  second_wave:       { freqs: [65.41,  130.81, 155.56, 196.00], padGain: 0.020, padCutoff: 250, breezeFreq: 195, breezeQ: 1.00, breezeGain: 0.020, birdGain: 0.0,    chime: false },
  vow_shrine:        { freqs: [130.81, 164.81, 196.00, 246.94], padGain: 0.016, padCutoff: 350, breezeFreq: 330, breezeQ: 0.75, breezeGain: 0.011, birdGain: 0.0022, chime: true  }
};

function isSpotAudioPlaying() {
  if (narrationPhase === 'archival' && archivalAudio && !archivalAudio.paused) return true;
  if (narrationPhase === 'delay') return true;
  if (narrationPhase === 'voice' && narrationAudio && !narrationAudio.paused) return true;
  return false;
}

function canTransitionDisplay() {
  if (supportsDisplayTransition !== undefined) return supportsDisplayTransition;
  if (!window.CSS?.supports?.('transition-behavior', 'allow-discrete') || !document.body) {
    supportsDisplayTransition = false;
    return false;
  }
  const probe = document.createElement('div');
  probe.style.cssText = 'transition: display 1s allow-discrete !important; display: block;';
  document.body.appendChild(probe);
  getComputedStyle(probe).display;
  probe.style.display = 'none';
  supportsDisplayTransition = getComputedStyle(probe).display === 'block';
  probe.remove();
  return supportsDisplayTransition;
}

function showAnimatedOverlay(el) {
  if (!el) return;
  el.style.transition = '';
  el.style.opacity = '';
  el.style.translate = '';
  el.removeAttribute('data-closing');
  el.hidden = false;
}

async function hideAnimatedOverlay(el) {
  if (!el || el.hidden) return;
  el.style.transition = '';
  el.style.opacity = '';
  el.style.translate = '';
  if (canTransitionDisplay()) {
    el.hidden = true;
    return;
  }
  el.setAttribute('data-closing', '');
  const animations = typeof el.getAnimations === 'function' ? el.getAnimations() : [];
  if (animations.length > 0) {
    await Promise.race([
      Promise.allSettled(animations.map((a) => a.finished)),
      new Promise((r) => setTimeout(r, 450))
    ]);
  }
  if (el.hasAttribute('data-closing')) {
    el.removeAttribute('data-closing');
    el.hidden = true;
  }
}

function showStoryBanner() {
  showAnimatedOverlay(document.getElementById('storyBanner'));
}

async function hideStoryBanner() {
  await hideAnimatedOverlay(document.getElementById('storyBanner'));
}

async function ensurePipVideoLoadedForHotspot(hotspotId, autoPlayLive) {
  const vCfg = WALKTHROUGH_VISUAL_CONFIG[hotspotId];
  const pipVideo = document.getElementById('walkthroughPipVideo');
  if (!vCfg || !vCfg.pipReel || !pipVideo) return;

  if (activePipReelUrl !== vCfg.pipReel) {
    activePipReelUrl = vCfg.pipReel;
    const resolvedSrc = await resolvePipVideoSrc(vCfg.pipReel);
    if (activePipReelUrl !== vCfg.pipReel) return;
    pipVideo.src = resolvedSrc;
    pipVideo.load();
    await new Promise((resolve) => {
      if (pipVideo.readyState >= 1) {
        resolve();
        return;
      }
      const done = () => {
        pipVideo.removeEventListener('loadeddata', done);
        pipVideo.removeEventListener('loadedmetadata', done);
        pipVideo.removeEventListener('error', done);
        resolve();
      };
      pipVideo.addEventListener('loadeddata', done);
      pipVideo.addEventListener('loadedmetadata', done);
      pipVideo.addEventListener('error', done);
      setTimeout(done, 1500);
    });
  }

  if (autoPlayLive) {
    const prefersReduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!prefersReduced) {
      pipVideo.play().catch(() => {});
    } else {
      pipVideo.pause();
    }
  }
}

function applyWalkthroughStationOverlays(stopIdx) {
  const stop = GUIDED_TOUR_STOPS[stopIdx];
  if (!stop) return;
  const vCfg = WALKTHROUGH_VISUAL_CONFIG[stop.hotspotId];
  if (!vCfg) return;

  const stampEl = document.getElementById('walkthroughContextStamp');
  const stampTxt = document.getElementById('walkthroughContextText');
  if (stampEl && stampTxt) {
    stampEl.setAttribute('data-phase', vCfg.phase || 'pre');
    stampTxt.textContent = (vCfg.stamp && (vCfg.stamp[currentLang] || vCfg.stamp.en)) || '';
  }

  const pipBadge = document.getElementById('walkthroughPipBadge');
  const pipCap = document.getElementById('walkthroughPipCaption');
  if (pipBadge && vCfg.pipBadge) {
    pipBadge.textContent = vCfg.pipBadge[currentLang] || vCfg.pipBadge.en;
  }
  if (pipCap && vCfg.pipCaption) {
    pipCap.textContent = vCfg.pipCaption[currentLang] || vCfg.pipCaption.en;
  }

  const quoteEl = document.getElementById('walkthroughQuoteCallout');
  const quoteTxt = document.getElementById('walkthroughQuoteText');
  const quoteAuth = document.getElementById('walkthroughQuoteAuthor');
  if (quoteEl && quoteTxt && quoteAuth) {
    if (vCfg.quote) {
      quoteEl.setAttribute('data-tone', vCfg.quote.tone || 'pre');
      quoteTxt.textContent = vCfg.quote.text[currentLang] || vCfg.quote.text.en;
      quoteAuth.textContent = vCfg.quote.author[currentLang] || vCfg.quote.author.en;
    } else {
      quoteTxt.textContent = '';
      quoteAuth.textContent = '';
      quoteEl.hidden = true;
    }
  }
}

function updateWalkthroughVisualOverlaysLive(stopIdx, progress) {
  if (!isGuidedTour || deterministicWalkthroughRender) return;
  const stop = GUIDED_TOUR_STOPS[stopIdx];
  if (!stop) return;
  const vCfg = WALKTHROUGH_VISUAL_CONFIG[stop.hotspotId];
  if (!vCfg) return;

  const stampEl = document.getElementById('walkthroughContextStamp');
  if (stampEl && stampEl.hidden) {
    showAnimatedOverlay(stampEl);
  }

  const pipCard = document.getElementById('walkthroughPipCard');
  const pipVideo = document.getElementById('walkthroughPipVideo');
  const shouldShowPip = Boolean(vCfg.pipReel) && progress >= 0.09 && progress <= 0.88;
  if (pipCard) {
    if (shouldShowPip && (pipCard.hidden || pipCard.hasAttribute('data-closing'))) {
      showAnimatedOverlay(pipCard);
      ensurePipVideoLoadedForHotspot(stop.hotspotId, true);
    } else if (!shouldShowPip && !pipCard.hidden && !pipCard.hasAttribute('data-closing')) {
      if (pipVideo) pipVideo.pause();
      hideAnimatedOverlay(pipCard);
    }
  }

  const quoteEl = document.getElementById('walkthroughQuoteCallout');
  const shouldShowQuote = Boolean(vCfg.quote) && progress >= 0.48 && progress <= 0.86;
  if (quoteEl) {
    if (shouldShowQuote && (quoteEl.hidden || quoteEl.hasAttribute('data-closing'))) {
      showAnimatedOverlay(quoteEl);
    } else if (!shouldShowQuote && !quoteEl.hidden && !quoteEl.hasAttribute('data-closing')) {
      hideAnimatedOverlay(quoteEl);
    }
  }
}

function smoothWindowAlpha(p, inStart, inEnd, outStart, outEnd) {
  if (p <= inStart || p >= outEnd) return 0;
  if (p < inEnd) {
    const t = (p - inStart) / Math.max(0.0001, inEnd - inStart);
    return 0.5 - 0.5 * Math.cos(Math.PI * t);
  }
  if (p > outStart) {
    const t = (outEnd - p) / Math.max(0.0001, outEnd - outStart);
    return 0.5 - 0.5 * Math.cos(Math.PI * t);
  }
  return 1;
}

async function syncWalkthroughVisualsAtProgress(stopIdx, progress, totalStationSec) {
  deterministicWalkthroughRender = true;
  const stop = GUIDED_TOUR_STOPS[stopIdx];
  if (!stop) return;
  const vCfg = WALKTHROUGH_VISUAL_CONFIG[stop.hotspotId];
  applyWalkthroughStationOverlays(stopIdx);

  const stampEl = document.getElementById('walkthroughContextStamp');
  if (stampEl) {
    const sAlpha = smoothWindowAlpha(progress, 0.0, 0.04, 0.95, 1.0);
    stampEl.removeAttribute('data-closing');
    stampEl.style.transition = 'none';
    if (sAlpha <= 0.002) {
      stampEl.hidden = true;
    } else {
      stampEl.hidden = false;
      stampEl.style.opacity = sAlpha.toFixed(3);
      stampEl.style.translate = `0 ${((1 - sAlpha) * -8).toFixed(1)}px`;
    }
  }

  const pipCard = document.getElementById('walkthroughPipCard');
  const pipVideo = document.getElementById('walkthroughPipVideo');
  if (pipCard && pipVideo && vCfg && vCfg.pipReel) {
    const pAlpha = smoothWindowAlpha(progress, 0.09, 0.14, 0.83, 0.88);
    pipCard.removeAttribute('data-closing');
    pipCard.style.transition = 'none';
    if (pAlpha <= 0.002) {
      pipCard.hidden = true;
    } else {
      pipCard.hidden = false;
      pipCard.style.opacity = pAlpha.toFixed(3);
      pipCard.style.translate = '0 0';
      await ensurePipVideoLoadedForHotspot(stop.hotspotId, false);
      pipVideo.pause();
      const dur = (Number.isFinite(pipVideo.duration) && pipVideo.duration > 0.2) ? pipVideo.duration : 14.0;
      const elapsedSec = Math.max(0, (progress - 0.09) * (totalStationSec || 55.0));
      const targetTime = Math.min(dur - 0.05, elapsedSec % Math.max(0.5, dur - 0.05));
      if (Math.abs((pipVideo.currentTime || 0) - targetTime) > 0.025) {
        await new Promise((resolve) => {
          const onSeeked = () => {
            pipVideo.removeEventListener('seeked', onSeeked);
            resolve();
          };
          pipVideo.addEventListener('seeked', onSeeked);
          try {
            pipVideo.currentTime = targetTime;
          } catch (_) {
            pipVideo.removeEventListener('seeked', onSeeked);
            resolve();
          }
          setTimeout(() => {
            pipVideo.removeEventListener('seeked', onSeeked);
            resolve();
          }, 120);
        });
      }
    }
  }

  const quoteEl = document.getElementById('walkthroughQuoteCallout');
  if (quoteEl) {
    quoteEl.removeAttribute('data-closing');
    quoteEl.style.transition = 'none';
    const qAlpha = (vCfg && vCfg.quote) ? smoothWindowAlpha(progress, 0.48, 0.53, 0.82, 0.87) : 0;
    if (qAlpha <= 0.002) {
      quoteEl.hidden = true;
    } else {
      quoteEl.hidden = false;
      quoteEl.style.opacity = qAlpha.toFixed(3);
      quoteEl.style.translate = `-50% ${((1 - qAlpha) * 8).toFixed(1)}px`;
    }
  }
}
window.syncWalkthroughVisualsAtProgress = syncWalkthroughVisualsAtProgress;

function resetWalkthroughIdleTimer() {
  document.body.classList.remove('walkthrough-idle');
  if (walkthroughIdleTimer) {
    clearTimeout(walkthroughIdleTimer);
    walkthroughIdleTimer = null;
  }
  if (!isGuidedTour) return;
  walkthroughIdleTimer = setTimeout(() => {
    if (isGuidedTour && isSpotAudioPlaying()) {
      document.body.classList.add('walkthrough-idle');
    }
  }, 3500);
}

function updateStoryAudioButtonUI(isPlaying) {
  const btn = document.getElementById('btnStoryAudio');
  if (!btn) return;
  if (isPlaying) {
    btn.textContent = '⏸';
    btn.setAttribute('aria-label', 'Pause voiceover');
    btn.setAttribute('title', 'Pause voiceover');
  } else {
    btn.textContent = '▶';
    btn.setAttribute('aria-label', 'Play voiceover');
    btn.setAttribute('title', 'Play voiceover');
  }
}

function setWalkthroughProgress(progress) {
  const fill = document.getElementById('storyProgressFill');
  if (!fill) return;
  const clamped = Math.max(0, Math.min(1, progress || 0));
  fill.style.transform = `scaleX(${clamped.toFixed(4)})`;
}

function sampleGuidedTourCamera(stopIndex, rawProgress) {
  const stop = GUIDED_TOUR_STOPS[stopIndex];
  if (!stop) return null;
  const pts = Array.isArray(stop.waypoints) && stop.waypoints.length >= 2
    ? stop.waypoints
    : [{ camPos: stop.camPos, lookAt: stop.lookAt }, { camPos: stop.camPos, lookAt: stop.lookAt }];

  const p = Math.max(0, Math.min(1, rawProgress || 0));
  // Cosine ease-in-out for calm museum motion
  const eased = 0.5 - 0.5 * Math.cos(Math.PI * p);
  const scaled = eased * (pts.length - 1);
  const segIdx = Math.min(pts.length - 2, Math.floor(scaled));
  const localT = scaled - segIdx;
  const segEase = 0.5 - 0.5 * Math.cos(Math.PI * localT);

  const a = pts[segIdx];
  const b = pts[segIdx + 1];
  const pos = new THREE.Vector3(
    THREE.MathUtils.lerp(a.camPos[0], b.camPos[0], segEase),
    THREE.MathUtils.lerp(a.camPos[1], b.camPos[1], segEase),
    THREE.MathUtils.lerp(a.camPos[2], b.camPos[2], segEase)
  );
  const lookAt = new THREE.Vector3(
    THREE.MathUtils.lerp(a.lookAt[0], b.lookAt[0], segEase),
    THREE.MathUtils.lerp(a.lookAt[1], b.lookAt[1], segEase),
    THREE.MathUtils.lerp(a.lookAt[2], b.lookAt[2], segEase)
  );
  return { pos, lookAt };
}
window.sampleGuidedTourCamera = sampleGuidedTourCamera;
window.setWalkthroughProgress = setWalkthroughProgress;

function scheduleMorningBirdsong(birdGainTarget) {
  if (ambientBirdTimer) {
    clearTimeout(ambientBirdTimer);
    ambientBirdTimer = null;
  }
  if (!birdGainTarget || birdGainTarget <= 0 || !ambientAudioCtx) return;

  const triggerChirp = () => {
    if (!ambientAudioCtx || ambientAudioCtx.state !== 'running' || !isSpotAudioPlaying()) return;
    try {
      const now = ambientAudioCtx.currentTime;
      const notes = [2480 + Math.random() * 260, 2860 + Math.random() * 280];
      notes.forEach((baseFreq, i) => {
        const t0 = now + i * 0.16;
        const osc = ambientAudioCtx.createOscillator();
        const g = ambientAudioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(baseFreq, t0);
        osc.frequency.exponentialRampToValueAtTime(baseFreq * 1.14, t0 + 0.07);
        osc.frequency.exponentialRampToValueAtTime(baseFreq * 0.96, t0 + 0.14);
        g.gain.setValueAtTime(0.0001, t0);
        g.gain.linearRampToValueAtTime(birdGainTarget, t0 + 0.03);
        g.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.15);
        osc.connect(g);
        g.connect(ambientAudioCtx.destination);
        osc.start(t0);
        osc.stop(t0 + 0.17);
      });
    } catch (_) {}
    ambientBirdTimer = setTimeout(triggerChirp, 4800 + Math.random() * 3400);
  };

  ambientBirdTimer = setTimeout(triggerChirp, 1600 + Math.random() * 1800);
}

function triggerMemorialBellHarmonic() {
  if (!ambientAudioCtx) return;
  try {
    const now = ambientAudioCtx.currentTime;
    [523.25, 783.99].forEach((freq, idx) => {
      const osc = ambientAudioCtx.createOscillator();
      const g = ambientAudioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, now);
      const peak = idx === 0 ? 0.011 : 0.0045;
      g.gain.setValueAtTime(0.0001, now);
      g.gain.linearRampToValueAtTime(peak, now + 0.08);
      g.gain.exponentialRampToValueAtTime(0.0001, now + 4.2);
      osc.connect(g);
      g.connect(ambientAudioCtx.destination);
      osc.start(now);
      osc.stop(now + 4.4);
    });
  } catch (_) {}
}

function startMemorialAmbientPad(hotspotId) {
  try {
    const profile = ROOM_ATMOSPHERE_PROFILES[hotspotId] || ROOM_ATMOSPHERE_PROFILES.rainbow_staircase;
    if (!ambientAudioCtx) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (!AudioContextClass) return;
      ambientAudioCtx = new AudioContextClass();

      ambientGainNode = ambientAudioCtx.createGain();
      ambientGainNode.gain.setValueAtTime(0.0001, ambientAudioCtx.currentTime);

      ambientPadFilter = ambientAudioCtx.createBiquadFilter();
      ambientPadFilter.type = 'lowpass';
      ambientPadFilter.frequency.setValueAtTime(profile.padCutoff, ambientAudioCtx.currentTime);

      ambientOscillators = profile.freqs.map((f, idx) => {
        const osc = ambientAudioCtx.createOscillator();
        osc.type = idx % 2 === 0 ? 'sine' : 'triangle';
        osc.frequency.setValueAtTime(f, ambientAudioCtx.currentTime);
        const oscGain = ambientAudioCtx.createGain();
        oscGain.gain.setValueAtTime(idx === 0 ? 0.34 : 0.17, ambientAudioCtx.currentTime);
        osc.connect(oscGain);
        oscGain.connect(ambientPadFilter);
        osc.start();
        return osc;
      });

      ambientPadFilter.connect(ambientGainNode);
      ambientGainNode.connect(ambientAudioCtx.destination);

      // Gentle filtered courtyard breeze / room air buffer (4s pink-filtered loop)
      const sampleRate = ambientAudioCtx.sampleRate || 44100;
      const bufLen = sampleRate * 4;
      const noiseBuf = ambientAudioCtx.createBuffer(1, bufLen, sampleRate);
      const out = noiseBuf.getChannelData(0);
      let b0 = 0, b1 = 0, b2 = 0;
      for (let i = 0; i < bufLen; i++) {
        const white = Math.random() * 2 - 1;
        b0 = 0.99765 * b0 + white * 0.0990460;
        b1 = 0.96300 * b1 + white * 0.2965164;
        b2 = 0.57000 * b2 + white * 1.0526913;
        out[i] = (b0 + b1 + b2 + white * 0.1848) * 0.12;
      }
      // Crossfade loop seam smoothly
      const fadeSamples = Math.floor(sampleRate * 0.15);
      for (let i = 0; i < fadeSamples; i++) {
        const t = i / fadeSamples;
        out[i] = out[i] * t + out[bufLen - fadeSamples + i] * (1 - t);
      }

      const noiseSrc = ambientAudioCtx.createBufferSource();
      noiseSrc.buffer = noiseBuf;
      noiseSrc.loop = true;

      ambientBreezeFilter = ambientAudioCtx.createBiquadFilter();
      ambientBreezeFilter.type = 'bandpass';
      ambientBreezeFilter.frequency.setValueAtTime(profile.breezeFreq, ambientAudioCtx.currentTime);
      ambientBreezeFilter.Q.setValueAtTime(profile.breezeQ, ambientAudioCtx.currentTime);

      ambientBreezeGain = ambientAudioCtx.createGain();
      ambientBreezeGain.gain.setValueAtTime(0.0001, ambientAudioCtx.currentTime);

      noiseSrc.connect(ambientBreezeFilter);
      ambientBreezeFilter.connect(ambientBreezeGain);
      ambientBreezeGain.connect(ambientAudioCtx.destination);
      noiseSrc.start();
    }

    if (ambientAudioCtx.state === 'suspended') {
      ambientAudioCtx.resume();
    }

    const now = ambientAudioCtx.currentTime;
    ambientOscillators.forEach((osc, idx) => {
      const targetFreq = profile.freqs[idx] || profile.freqs[0];
      osc.frequency.cancelScheduledValues(now);
      osc.frequency.exponentialRampToValueAtTime(Math.max(40, targetFreq), now + 1.2);
    });
    if (ambientPadFilter) {
      ambientPadFilter.frequency.cancelScheduledValues(now);
      ambientPadFilter.frequency.linearRampToValueAtTime(profile.padCutoff, now + 1.2);
    }
    if (ambientGainNode) {
      ambientGainNode.gain.cancelScheduledValues(now);
      ambientGainNode.gain.linearRampToValueAtTime(profile.padGain, now + 1.6);
    }
    if (ambientBreezeFilter && ambientBreezeGain) {
      ambientBreezeFilter.frequency.cancelScheduledValues(now);
      ambientBreezeFilter.frequency.linearRampToValueAtTime(profile.breezeFreq, now + 1.2);
      ambientBreezeFilter.Q.setValueAtTime(profile.breezeQ, now);
      ambientBreezeGain.gain.cancelScheduledValues(now);
      ambientBreezeGain.gain.linearRampToValueAtTime(profile.breezeGain, now + 1.6);
    }

    scheduleMorningBirdsong(profile.birdGain);
    if (profile.chime) {
      triggerMemorialBellHarmonic();
    }
  } catch (_) {
    // Ignore WebAudio restrictions if any
  }
}

function stopMemorialAmbientPad() {
  try {
    if (ambientBirdTimer) {
      clearTimeout(ambientBirdTimer);
      ambientBirdTimer = null;
    }
    if (ambientAudioCtx) {
      const now = ambientAudioCtx.currentTime;
      if (ambientGainNode) {
        ambientGainNode.gain.cancelScheduledValues(now);
        ambientGainNode.gain.linearRampToValueAtTime(0.0001, now + 1.0);
      }
      if (ambientBreezeGain) {
        ambientBreezeGain.gain.cancelScheduledValues(now);
        ambientBreezeGain.gain.linearRampToValueAtTime(0.0001, now + 1.0);
      }
    }
  } catch (_) {}
}

function pauseSpotNarration() {
  if (narrationPhaseTimer) {
    clearTimeout(narrationPhaseTimer);
    narrationPhaseTimer = null;
    narrationPhase = 'voice';
  }
  if (archivalAudio && !archivalAudio.paused) {
    archivalAudio.pause();
  }
  if (narrationAudio && !narrationAudio.paused) {
    narrationAudio.pause();
  }
  stopMemorialAmbientPad();
  updateStoryAudioButtonUI(false);
  const listenBtn = document.getElementById('modalListenBtn');
  if (listenBtn) {
    listenBtn.textContent = '🎧 Listen to Room Voiceover';
  }
}

function resumeSpotNarration(fallbackHotspotId) {
  const hotspotId = activeNarrationHotspot || fallbackHotspotId;
  if (!hotspotId) return;
  voiceNarrationEnabled = true;

  if (narrationPhase === 'archival' && archivalAudio && archivalAudio.src && !archivalAudio.ended) {
    startMemorialAmbientPad(hotspotId);
    archivalAudio.play().catch(() => {});
    updateStoryAudioButtonUI(true);
    return;
  }
  if (narrationPhase === 'voice' && narrationAudio && narrationAudio.src && !narrationAudio.ended) {
    startMemorialAmbientPad(hotspotId);
    narrationAudio.play().catch(() => {});
    updateStoryAudioButtonUI(true);
    return;
  }
  playSpotNarration(hotspotId);
}

function getGuidedTourAudioProgress() {
  const stop = GUIDED_TOUR_STOPS[currentTourIndex];
  const hotspotId = activeNarrationHotspot || (stop && stop.hotspotId) || '';
  const archCfg = SPOT_ARCHIVAL_AUDIO[hotspotId];
  const archDur = archCfg
    ? (archivalAudio && Number.isFinite(archivalAudio.duration) && archivalAudio.duration > 0 ? archivalAudio.duration : archCfg.expectedDur)
    : ((hotspotId === 'crater_damage' || hotspotId === 'second_wave') ? 1.1 : 0);
  const voiceDur = (narrationAudio && Number.isFinite(narrationAudio.duration) && narrationAudio.duration > 0)
    ? narrationAudio.duration
    : 55;
  const totalDur = Math.max(1, archDur + voiceDur);

  if (narrationPhase === 'archival' && archivalAudio) {
    return Math.min(1, (archivalAudio.currentTime || 0) / totalDur);
  }
  if (narrationPhase === 'delay') {
    return Math.min(1, archDur / totalDur);
  }
  if (narrationPhase === 'voice' && narrationAudio) {
    return Math.min(1, (archDur + (narrationAudio.currentTime || 0)) / totalDur);
  }
  if (tourStepStartTime > 0) {
    return Math.min(1, (performance.now() - tourStepStartTime) / 60000);
  }
  return 0;
}

function stopSpotNarration() {
  if (guidedTourAutoAdvanceTimer) {
    clearTimeout(guidedTourAutoAdvanceTimer);
    guidedTourAutoAdvanceTimer = null;
  }
  if (narrationPhaseTimer) {
    clearTimeout(narrationPhaseTimer);
    narrationPhaseTimer = null;
  }
  narrationPhase = 'idle';
  activeNarrationHotspot = null;
  if (archivalAudio) {
    archivalAudio.onended = null;
    archivalAudio.onerror = null;
    archivalAudio.pause();
    archivalAudio.currentTime = 0;
  }
  if (narrationAudio) {
    narrationAudio.onended = null;
    narrationAudio.onerror = null;
    narrationAudio.pause();
    narrationAudio.currentTime = 0;
  }
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
  stopMemorialAmbientPad();
  updateStoryAudioButtonUI(false);
  const listenBtn = document.getElementById('modalListenBtn');
  if (listenBtn) {
    listenBtn.textContent = '🎧 Listen to Room Voiceover';
  }
}

function playSpotNarration(hotspotId) {
  stopSpotNarration();
  if (!voiceNarrationEnabled) return;

  activeNarrationHotspot = hotspotId;
  const prof = NARRATOR_PROFILES[activeVoiceProfile] || (currentLang === 'fa' ? NARRATOR_PROFILES.mostafa_fa : NARRATOR_PROFILES.leila_en);
  const narrationVersion = '20261112a';
  const primarySrc = `media/narration/${prof.dir}/${prof.prefix}_${hotspotId}.mp3?v=${narrationVersion}`;
  const fallbackSrc = `media/narration/${prof.fallbackDir || 'voices/leila_en'}/${prof.prefix}_${hotspotId}.mp3?v=${narrationVersion}`;

  if (!narrationAudio) {
    narrationAudio = new Audio();
  }
  if (!archivalAudio) {
    archivalAudio = new Audio();
  }

  const speedSelect = document.getElementById('narrationSpeedSelect');
  if (speedSelect) {
    narrationRate = parseFloat(speedSelect.value) || 1.0;
  }

  narrationAudio.preload = 'auto';
  narrationAudio.src = primarySrc;
  narrationAudio.playbackRate = narrationRate;
  if ('preservesPitch' in narrationAudio) narrationAudio.preservesPitch = true;
  if ('webkitPreservesPitch' in narrationAudio) narrationAudio.webkitPreservesPitch = true;
  narrationAudio.load();

  startMemorialAmbientPad(hotspotId);
  updateStoryAudioButtonUI(true);
  resetWalkthroughIdleTimer();

  const listenBtn = document.getElementById('modalListenBtn');
  if (listenBtn) {
    listenBtn.textContent = '⏸ Pause Room Voiceover';
  }

  narrationAudio.onended = () => {
    narrationPhase = 'idle';
    stopMemorialAmbientPad();
    updateStoryAudioButtonUI(false);
    setWalkthroughProgress(1);
    document.body.classList.remove('walkthrough-idle');
    if (listenBtn) {
      listenBtn.textContent = '🎧 Listen to Room Voiceover';
    }
    if (isGuidedTour && !document.getElementById('evidenceModal')?.classList.contains('visible')) {
      guidedTourAutoAdvanceTimer = setTimeout(() => {
        if (!isGuidedTour) return;
        if (currentTourIndex < GUIDED_TOUR_STOPS.length - 1) {
          currentTourIndex += 1;
          renderGuidedTourStep(currentTourIndex, true);
        } else {
          stopGuidedTour();
          openVowModal();
        }
      }, 1400);
    }
  };

  narrationAudio.onerror = () => {
    if (narrationAudio.src.indexOf(fallbackSrc) === -1) {
      narrationAudio.src = fallbackSrc;
      narrationAudio.playbackRate = narrationRate;
      if (narrationPhase === 'voice') {
        narrationAudio.play().catch(() => {});
      }
    }
  };

  const launchVoiceover = () => {
    if (activeNarrationHotspot !== hotspotId) return;
    narrationPhase = 'voice';
    narrationAudio.playbackRate = narrationRate;
    narrationAudio.play().catch(() => {
      narrationPhase = 'idle';
      stopMemorialAmbientPad();
      updateStoryAudioButtonUI(false);
    });
  };

  const archivalCfg = SPOT_ARCHIVAL_AUDIO[hotspotId];
  if (archivalCfg) {
    narrationPhase = 'archival';
    archivalAudio.src = `media/narration/archival/${archivalCfg.file}?v=${narrationVersion}`;
    archivalAudio.volume = 0.88;
    archivalAudio.playbackRate = 1.0;
    archivalAudio.onended = () => {
      if (activeNarrationHotspot !== hotspotId) return;
      narrationPhase = 'delay';
      narrationPhaseTimer = setTimeout(launchVoiceover, 380);
    };
    archivalAudio.onerror = () => {
      if (activeNarrationHotspot !== hotspotId) return;
      launchVoiceover();
    };
    archivalAudio.play().catch(() => {
      launchVoiceover();
    });
  } else {
    // Solemn aftermath silence with soft courtyard wind before narration begins
    narrationPhase = 'delay';
    narrationPhaseTimer = setTimeout(launchVoiceover, 1100);
  }
}

// --- GUIDED 8-STOP INTERIOR & COURTYARD TOUR ---
function startGuidedTour() {
  isGuidedTour = true;
  deterministicWalkthroughRender = false;
  currentTourIndex = 0;
  tourManualCameraOverride = false;
  closeModal();
  closeVowModal();
  closeArtifactInspector();
  document.body.classList.add('walkthrough-mode');
  if (markersGroup) markersGroup.visible = false;
  document.getElementById('btnGuidedTour').classList.add('active');
  showStoryBanner();
  resetWalkthroughIdleTimer();
  renderGuidedTourStep(0, true);
}

function stopGuidedTour() {
  isGuidedTour = false;
  deterministicWalkthroughRender = false;
  tourManualCameraOverride = false;
  if (walkthroughIdleTimer) {
    clearTimeout(walkthroughIdleTimer);
    walkthroughIdleTimer = null;
  }
  document.body.classList.remove('walkthrough-mode', 'walkthrough-idle');
  if (markersGroup) markersGroup.visible = true;
  document.getElementById('btnGuidedTour').classList.remove('active');
  const pipVideo = document.getElementById('walkthroughPipVideo');
  if (pipVideo) pipVideo.pause();
  hideAnimatedOverlay(document.getElementById('walkthroughContextStamp'));
  hideAnimatedOverlay(document.getElementById('walkthroughPipCard'));
  hideAnimatedOverlay(document.getElementById('walkthroughQuoteCallout'));
  hideStoryBanner();
  setWalkthroughProgress(0);
  stopSpotNarration();
}

function renderGuidedTourStep(idx, speakNow) {
  const stop = GUIDED_TOUR_STOPS[idx];
  if (!stop) return;
  const t = I18N_DATA[currentLang] || I18N_DATA.en;
  const hData = t.hotspots[stop.hotspotId];

  tourManualCameraOverride = false;
  tourStepStartTime = performance.now();
  setWalkthroughProgress(0);
  applyWalkthroughStationOverlays(idx);

  if (!deterministicWalkthroughRender) {
    const pipCard = document.getElementById('walkthroughPipCard');
    const quoteEl = document.getElementById('walkthroughQuoteCallout');
    if (pipCard) pipCard.hidden = true;
    if (quoteEl) quoteEl.hidden = true;
    showAnimatedOverlay(document.getElementById('walkthroughContextStamp'));
    ensurePipVideoLoadedForHotspot(stop.hotspotId, false);
  }

  setTemporalCondition(stop.temporal);
  document.getElementById('timelineSlider').value = stop.temporal;
  if (stop.temporal < 0.5 && typeof stop.cutawayMode === 'number') {
    setCutawayMode(stop.cutawayMode);
  }

  triggerCameraAnimation(
    new THREE.Vector3(stop.camPos[0], stop.camPos[1], stop.camPos[2]),
    new THREE.Vector3(stop.lookAt[0], stop.lookAt[1], stop.lookAt[2])
  );

  const badgeEl = document.getElementById('storyStepBadge');
  if (badgeEl) {
    const shortBadge = stop.shortBadge && (stop.shortBadge[currentLang] || stop.shortBadge.en);
    badgeEl.textContent = shortBadge || (stop.badge[currentLang] || stop.badge.en);
  }
  const titleEl = document.getElementById('storyTitle');
  if (titleEl && hData) {
    titleEl.textContent = hData.title.replace(/^[0-9۰-۹]+\.\s*/, '');
  }

  if (speakNow && voiceNarrationEnabled) {
    playSpotNarration(stop.hotspotId);
  } else {
    updateStoryAudioButtonUI(false);
  }
}

// --- WALK INSIDE MODE & KEYBOARD NAVIGATION ---
function toggleWalkMode() {
  isWalkMode = !isWalkMode;
  const btn = document.getElementById('btnWalkMode');
  btn.classList.toggle('active', isWalkMode);
  if (isWalkMode) {
    setTemporalCondition(0.0);
    document.getElementById('timelineSlider').value = 0.0;
    setCutawayMode(2); // Open ground floor rooms for immediate walking inside!
    triggerCameraAnimation(new THREE.Vector3(-1.2, 1.85, 6.2), new THREE.Vector3(-1.2, 1.85, -8.5));
  } else {
    setCutawayMode(0);
    triggerCameraAnimation(new THREE.Vector3(28, 22, 34), new THREE.Vector3(0, 3.0, -3));
  }
}

function initKeyboardWalkControls() {
  window.addEventListener('keydown', (e) => {
    if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) return;
    if (e.code === 'KeyW' || e.code === 'ArrowUp') moveKeys.forward = true;
    if (e.code === 'KeyS' || e.code === 'ArrowDown') moveKeys.backward = true;
    if (e.code === 'KeyA' || e.code === 'ArrowLeft') moveKeys.left = true;
    if (e.code === 'KeyD' || e.code === 'ArrowRight') moveKeys.right = true;
  });

  window.addEventListener('keyup', (e) => {
    if (e.code === 'KeyW' || e.code === 'ArrowUp') moveKeys.forward = false;
    if (e.code === 'KeyS' || e.code === 'ArrowDown') moveKeys.backward = false;
    if (e.code === 'KeyA' || e.code === 'ArrowLeft') moveKeys.left = false;
    if (e.code === 'KeyD' || e.code === 'ArrowRight') moveKeys.right = false;
  });
}

function applyKeyboardMovement(delta) {
  if (!moveKeys.forward && !moveKeys.backward && !moveKeys.left && !moveKeys.right) return;
  isAnimatingCamera = false;
  const speed = 10.0 * delta;
  const forward = new THREE.Vector3();
  camera.getWorldDirection(forward);
  forward.y = 0;
  forward.normalize();

  const right = new THREE.Vector3().crossVectors(forward, camera.up).normalize();
  const moveVec = new THREE.Vector3();

  if (moveKeys.forward) moveVec.add(forward);
  if (moveKeys.backward) moveVec.sub(forward);
  if (moveKeys.right) moveVec.add(right);
  if (moveKeys.left) moveVec.sub(right);

  if (moveVec.lengthSq() > 0) {
    moveVec.normalize().multiplyScalar(speed);
    camera.position.add(moveVec);
    controls.target.add(moveVec);
    if (isWalkMode) {
      camera.position.y = 1.85;
      controls.target.y = 1.85;
    }
  }
}

// --- SPATIAL.IO .GLB 3D ENVIRONMENT EXPORTER ---
function exportSceneToGLB() {
  if (typeof THREE.GLTFExporter === 'undefined') {
    alert('GLTFExporter is still loading. Please try again in a moment.');
    return;
  }
  const exporter = new THREE.GLTFExporter();
  const exportGroup = new THREE.Group();
  exportGroup.name = "Minab_Shajareh_Tayyebeh_School_SpatialIO";
  exportGroup.add(terrainGroup.clone());
  exportGroup.add(preStrikeModelGroup.clone());

  exporter.parse(
    exportGroup,
    (result) => {
      const blob = new Blob([result], { type: 'model/gltf-binary' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'minab_shajareh_tayyebeh_spatial.glb';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    { binary: true }
  );
}

// --- ACCOUNTABILITY VOW & PETITION MODAL LOGIC ---
function syncReconstructionVowRolesUI() {
  document.querySelectorAll('#vowContributionGroup .vow-role-option').forEach(lbl => {
    const cb = lbl.querySelector('input[type="checkbox"]');
    lbl.classList.toggle('is-checked', Boolean(cb && cb.checked));
  });
}

function getReconstructionSelectedVowRoles() {
  const groupEl = document.getElementById('vowContributionGroup');
  if (groupEl) {
    return Array.from(groupEl.querySelectorAll('input[name="vowContribution"]:checked'))
      .map(cb => cb.value)
      .filter(Boolean);
  }
  const legacySelect = document.getElementById('vowContribution');
  return legacySelect && legacySelect.value ? [legacySelect.value] : [];
}

function formatReconstructionVowSummary(rolesList) {
  if (!rolesList || rolesList.length === 0) {
    return 'Accountability Vow — Public Petitioner & Campaigner';
  }
  if (rolesList.length === 1) return rolesList[0];
  const shortLabels = rolesList.map(r => String(r).replace(/^Accountability Vow\s*[—-]\s*/, '').trim());
  return ('Accountability Vow — ' + shortLabels.join(' | ')).slice(0, 500);
}

function openVowModal() {
  const statusEl = document.getElementById('vowStatusMsg');
  if (statusEl) statusEl.style.display = 'none';
  const groupEl = document.getElementById('vowContributionGroup');
  if (groupEl) {
    groupEl.removeAttribute('aria-invalid');
    if (!groupEl.__reconChangeBound) {
      groupEl.__reconChangeBound = true;
      groupEl.addEventListener('change', () => {
        syncReconstructionVowRolesUI();
        if (getReconstructionSelectedVowRoles().length > 0 && groupEl.getAttribute('aria-invalid') === 'true') {
          groupEl.removeAttribute('aria-invalid');
          if (statusEl) statusEl.style.display = 'none';
        }
      });
    }
  }
  syncReconstructionVowRolesUI();
  document.getElementById('vowModal').classList.add('visible');
  if (typeof window.__pfpTrackEvent === 'function') {
    window.__pfpTrackEvent('vow_open');
  }
}

function closeVowModal() {
  document.getElementById('vowModal').classList.remove('visible');
}

async function submitVowForm(e) {
  e.preventDefault();
  const t = I18N_DATA[currentLang] || I18N_DATA.en;
  const name = document.getElementById('vowName').value.trim();
  const email = document.getElementById('vowEmail').value.trim();
  const telegram_username = (document.getElementById('vowTelegram')?.value || '').trim();
  const phone_number = (document.getElementById('vowPhone')?.value || '').trim();
  const city = document.getElementById('vowCity').value.trim();
  const selectedRoles = getReconstructionSelectedVowRoles();
  const personalMsg = document.getElementById('vowMessage').value.trim();
  const statusEl = document.getElementById('vowStatusMsg');
  const submitBtn = document.getElementById('vowSubmitBtn');
  const groupEl = document.getElementById('vowContributionGroup');

  if (selectedRoles.length === 0) {
    if (groupEl) groupEl.setAttribute('aria-invalid', 'true');
    statusEl.style.display = 'block';
    statusEl.style.background = 'rgba(239, 68, 68, 0.16)';
    statusEl.style.color = '#fca5a5';
    statusEl.textContent = t.vowSelectError || 'Please select at least one way to take action.';
    const firstCb = groupEl ? groupEl.querySelector('input[type="checkbox"]') : null;
    if (firstCb) firstCb.focus();
    return;
  }
  if (groupEl) groupEl.removeAttribute('aria-invalid');

  const roleSummary = formatReconstructionVowSummary(selectedRoles);

  statusEl.style.display = 'block';
  statusEl.style.background = 'rgba(255,255,255,0.06)';
  statusEl.style.color = '#f0ebe3';
  statusEl.textContent = 'Recording your Accountability Vow...';
  submitBtn.disabled = true;

  const contact_handle = [telegram_username, phone_number].filter(Boolean).join(' | ');
  const rolesBulletText = selectedRoles.map(item => `  - ${item}`).join('\n');
  const fullMessage = [
    '[MINAB ACCOUNTABILITY VOW — NOV 20 HYBRID EVENT]',
    `City/Country: ${city}`,
    telegram_username ? `Telegram: ${telegram_username}` : null,
    phone_number ? `Phone/Signal: ${phone_number}` : null,
    selectedRoles.length > 1
      ? `Action Roles (${selectedRoles.length}):\n${rolesBulletText}`
      : `Action Role: ${roleSummary}`,
    'Pledge: Affirmed solemn vow to participate in holding every person in the chain of command accountable.',
    `Note: ${personalMsg || 'Signed from 3D Spatial School Reconstruction.'}`
  ].filter(Boolean).join('\n');

  let apiUrl = '/api/telegram/submit-contact/';
  if (window.location.protocol === 'file:' || window.location.port === '8090') {
    apiUrl = 'http://localhost:8000/api/telegram/submit-contact/';
  }

  try {
    const resp = await fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name,
        email,
        telegram_username,
        phone_number,
        city_country: city,
        contact_handle,
        role: roleSummary,
        roles: selectedRoles,
        message: fullMessage
      })
    });
    let data = {};
    try {
      data = await resp.json();
    } catch (_) {}

    if (!resp.ok) {
      throw new Error(data.error || data.message || `HTTP ${resp.status}`);
    }

    if (typeof data.vow_count === 'number') {
      vowSignatoryCount = data.vow_count;
      window.vowSignatoryCount = data.vow_count;
    } else {
      vowSignatoryCount += 1;
      window.vowSignatoryCount = vowSignatoryCount;
    }
  } catch (_) {
    submitBtn.disabled = false;
    statusEl.style.display = 'block';
    statusEl.style.background = 'rgba(239, 68, 68, 0.16)';
    statusEl.style.color = '#fca5a5';
    statusEl.textContent = t.vowSubmitError || 'Could not save your Accountability Vow right now. Please try again.';
    return;
  }

  updateVowBadge();
  if (typeof window.__pfpTrackEvent === 'function') {
    window.__pfpTrackEvent('vow_signed');
  }

  statusEl.style.background = 'rgba(16, 185, 129, 0.18)';
  statusEl.style.color = '#6ee7b7';
  const countSuffix = vowSignatoryCount >= VOW_BADGE_THRESHOLD ? ` (#${vowSignatoryCount.toLocaleString()})` : '';
  statusEl.textContent = (t.vowSuccessMsg || '✓ Thank you, {name}. Your Accountability Vow{count} has been recorded.')
    .replace('{name}', name)
    .replace('{count}', countSuffix);
  document.getElementById('vowForm').reset();
  const defaultCb = document.getElementById('vowCheckPetitioner');
  if (defaultCb) defaultCb.checked = true;
  const consentCb = document.getElementById('vowCheckbox');
  if (consentCb) consentCb.checked = true;
  syncReconstructionVowRolesUI();
  submitBtn.disabled = false;

  setTimeout(() => {
    closeVowModal();
    statusEl.style.display = 'none';
  }, 2600);
}

// --- UI CONTROLS & CAMERA PRESETS ---
function initUIControls() {
  const slider = document.getElementById('timelineSlider');
  slider.addEventListener('input', (e) => {
    setTemporalCondition(parseFloat(e.target.value));
  });

  document.getElementById('btnGuidedTour').addEventListener('click', () => {
    if (isGuidedTour) stopGuidedTour();
    else startGuidedTour();
  });

  const btnHudNarrator = document.getElementById('btnHudNarrator');
  if (btnHudNarrator) {
    btnHudNarrator.addEventListener('click', cycleNarratorForCurrentLanguage);
  }
  const btnSubrowNarrator = document.getElementById('btnSubrowNarrator');
  if (btnSubrowNarrator) {
    btnSubrowNarrator.addEventListener('click', cycleNarratorForCurrentLanguage);
  }
  const btnStoryNarrator = document.getElementById('btnStoryNarrator');
  if (btnStoryNarrator) {
    btnStoryNarrator.addEventListener('click', () => {
      resetWalkthroughIdleTimer();
      cycleNarratorForCurrentLanguage();
    });
  }

  document.getElementById('btnCutaway').addEventListener('click', () => {
    setTemporalCondition(0.0);
    document.getElementById('timelineSlider').value = 0.0;
    setCutawayMode(cutawayState + 1);
    if (cutawayState !== 0) {
      triggerCameraAnimation(new THREE.Vector3(-18, 22, 18), new THREE.Vector3(0, 2.5, -5));
    }
  });

  document.getElementById('btnStoryPrev').addEventListener('click', () => {
    currentTourIndex = (currentTourIndex - 1 + GUIDED_TOUR_STOPS.length) % GUIDED_TOUR_STOPS.length;
    renderGuidedTourStep(currentTourIndex, true);
  });

  document.getElementById('btnStoryNext').addEventListener('click', () => {
    if (currentTourIndex === GUIDED_TOUR_STOPS.length - 1) {
      stopGuidedTour();
      openVowModal();
    } else {
      currentTourIndex += 1;
      renderGuidedTourStep(currentTourIndex, true);
    }
  });

  document.getElementById('btnStoryAudio').addEventListener('click', () => {
    resetWalkthroughIdleTimer();
    const stop = GUIDED_TOUR_STOPS[currentTourIndex];
    if (isSpotAudioPlaying()) {
      pauseSpotNarration();
    } else if (stop) {
      resumeSpotNarration(stop.hotspotId);
    }
  });

  ['pointermove', 'pointerdown', 'keydown'].forEach((evtName) => {
    window.addEventListener(evtName, () => {
      if (isGuidedTour) resetWalkthroughIdleTimer();
    }, { passive: true });
  });

  window.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    const inspector = document.getElementById('artifactInspectorModal');
    if (inspector && inspector.classList.contains('visible')) {
      closeArtifactInspector();
      return;
    }
    const evModal = document.getElementById('evidenceModal');
    if (evModal && evModal.classList.contains('visible')) {
      closeModal();
      return;
    }
    const vModal = document.getElementById('vowModal');
    if (vModal && vModal.classList.contains('visible')) {
      closeVowModal();
      return;
    }
    if (isGuidedTour) {
      stopGuidedTour();
    }
  });

  const speedSelect = document.getElementById('narrationSpeedSelect');
  if (speedSelect) {
    speedSelect.addEventListener('change', (e) => {
      narrationRate = parseFloat(e.target.value) || 1.0;
      if (narrationAudio) {
        narrationAudio.playbackRate = narrationRate;
      }
    });
  }

  const modalListenBtn = document.getElementById('modalListenBtn');
  if (modalListenBtn) {
    modalListenBtn.addEventListener('click', () => {
      if (!activeHotspotId) return;
      if (isSpotAudioPlaying()) {
        stopSpotNarration();
      } else {
        voiceNarrationEnabled = true;
        playSpotNarration(activeHotspotId);
      }
    });
  }

  document.getElementById('btnStoryVideo').addEventListener('click', () => {
    const stop = GUIDED_TOUR_STOPS[currentTourIndex];
    if (stop) {
      if (stop.hotspotId === 'vow_shrine') openVowModal();
      else showHotspotModal(stop.hotspotId);
    }
  });

  document.getElementById('btnStoryClose').addEventListener('click', stopGuidedTour);

  document.getElementById('btnWalkMode').addEventListener('click', toggleWalkMode);

  document.getElementById('presetBoysArch').addEventListener('click', () => {
    selectHotspot('boys_flower_arch');
  });

  document.getElementById('presetStairs').addEventListener('click', () => {
    selectHotspot('rainbow_staircase');
  });

  document.getElementById('presetGirlsHall').addEventListener('click', () => {
    selectHotspot('girls_upper_hall');
  });

  const presetClassGalleryBtn = document.getElementById('presetClassGallery');
  if (presetClassGalleryBtn) {
    let galleryViewStep = 0;
    presetClassGalleryBtn.addEventListener('click', () => {
      closeModal();
      setTemporalCondition(0.0);
      document.getElementById('timelineSlider').value = 0.0;
      galleryViewStep = (galleryViewStep + 1) % 4;
      if (galleryViewStep === 1) {
        // View 1: Ground Floor Boys' Classrooms (Grades 1–3) & Desks with Rubble Drawings
        setCutawayMode(2);
        triggerCameraAnimation(new THREE.Vector3(-13.2, 2.45, -3.0), new THREE.Vector3(-18.2, 1.65, -5.4));
      } else if (galleryViewStep === 2) {
        // View 2: First Floor Girls' Assembly Hall (47 Schoolgirls)
        setCutawayMode(1);
        triggerCameraAnimation(new THREE.Vector3(-12.4, 5.85, -1.8), new THREE.Vector3(-18.2, 5.25, -7.5));
      } else if (galleryViewStep === 3) {
        // View 3: First Floor North-East Classroom (28 Rubble Drawings & Homework Archive)
        setCutawayMode(1);
        triggerCameraAnimation(new THREE.Vector3(17.2, 5.7, -11.8), new THREE.Vector3(10.5, 5.2, -8.2));
      } else {
        // View 4: Central Rainbow Staircase Hall (26 Martyred Female Educators)
        setCutawayMode(2);
        triggerCameraAnimation(new THREE.Vector3(-1.4, 2.35, -3.8), new THREE.Vector3(-6.0, 1.9, -6.2));
      }
    });
  }

  document.getElementById('presetCrater').addEventListener('click', () => {
    selectHotspot('crater_damage');
  });

  const inspectorCloseBtn = document.getElementById('inspectorCloseBtn');
  if (inspectorCloseBtn) {
    inspectorCloseBtn.addEventListener('click', closeArtifactInspector);
  }
  const inspectorModal = document.getElementById('artifactInspectorModal');
  if (inspectorModal) {
    inspectorModal.addEventListener('click', (e) => {
      if (e.target.id === 'artifactInspectorModal') closeArtifactInspector();
    });
  }

  document.getElementById('btnExportGlb').addEventListener('click', exportSceneToGLB);

  document.querySelectorAll('#openVowBtn').forEach(btn => {
    if (!btn.__pfpReconVowBound) {
      btn.__pfpReconVowBound = true;
      btn.addEventListener('click', () => openVowModal());
    }
  });
  const vowCloseEl = document.getElementById('vowCloseBtn');
  if (vowCloseEl && !vowCloseEl.__pfpBound) {
    vowCloseEl.__pfpBound = true;
    vowCloseEl.addEventListener('click', closeVowModal);
  }
  const vowModalEl = document.getElementById('vowModal');
  if (vowModalEl && !vowModalEl.__pfpBackdropBound) {
    vowModalEl.__pfpBackdropBound = true;
    vowModalEl.addEventListener('click', (e) => {
      if (e.target.id === 'vowModal') closeVowModal();
    });
  }
  const vowFormEl = document.getElementById('vowForm');
  if (vowFormEl && !vowFormEl.__pfpBound) {
    vowFormEl.__pfpBound = true;
    vowFormEl.addEventListener('submit', submitVowForm);
  }

  const vrBtn = document.getElementById('enterVrBtn');
  if ('xr' in navigator) {
    navigator.xr.isSessionSupported('immersive-vr').then(supported => {
      if (supported) {
        vrBtn.style.display = 'inline-flex';
        vrBtn.addEventListener('click', startWebXRSession);
      }
    });
  }

  document.getElementById('modalCloseBtn').addEventListener('click', closeModal);
  document.getElementById('evidenceModal').addEventListener('click', (e) => {
    if (e.target.id === 'evidenceModal') closeModal();
  });
}

function setTemporalCondition(val) {
  damageSliderValue = THREE.MathUtils.clamp(val, 0.0, 1.0);

  if (damageSliderValue < 0.05) {
    preStrikeModelGroup.visible = true;
    postStrikeModelGroup.visible = false;
  } else if (damageSliderValue > 0.95) {
    preStrikeModelGroup.visible = false;
    postStrikeModelGroup.visible = true;
  } else {
    preStrikeModelGroup.visible = true;
    postStrikeModelGroup.visible = true;
  }

  const isPost = damageSliderValue >= 0.5;
  document.getElementById('btnStatePre').classList.toggle('active', !isPost);
  document.getElementById('btnStatePost').classList.toggle('active', isPost);
}

function triggerCameraAnimation(newPos, newLookAt) {
  isAnimatingCamera = true;
  animationTarget.pos = newPos;
  animationTarget.lookAt = newLookAt;
}

function startWebXRSession() {
  if (!navigator.xr) return;
  navigator.xr.requestSession('immersive-vr').then(session => {
    renderer.xr.setSession(session);
  }).catch(err => {
    alert("WebXR session could not be started: " + err.message);
  });
}

// --- ANIMATION LOOP ---
function animate() {
  requestAnimationFrame(animate);

  const delta = clock.getDelta();
  applyKeyboardMovement(delta);

  if (isGuidedTour && !deterministicWalkthroughRender) {
    const tourProgress = getGuidedTourAudioProgress();
    setWalkthroughProgress(tourProgress);
    updateWalkthroughVisualOverlaysLive(currentTourIndex, tourProgress);

    if (isAnimatingCamera && animationTarget.pos) {
      camera.position.lerp(animationTarget.pos, 0.06);
      controls.target.lerp(animationTarget.lookAt, 0.06);
      if (camera.position.distanceTo(animationTarget.pos) < 0.25) {
        isAnimatingCamera = false;
      }
    } else if (!tourManualCameraOverride) {
      const sampled = sampleGuidedTourCamera(currentTourIndex, tourProgress);
      if (sampled) {
        camera.position.lerp(sampled.pos, 0.045);
        controls.target.lerp(sampled.lookAt, 0.055);
      }
    }
  } else if (isAnimatingCamera && animationTarget.pos) {
    camera.position.lerp(animationTarget.pos, 0.06);
    controls.target.lerp(animationTarget.lookAt, 0.06);

    if (camera.position.distanceTo(animationTarget.pos) < 0.25) {
      isAnimatingCamera = false;
    }
  }

  controls.update();
  updateHotspotPositions();
  renderer.render(scene, camera);
}
