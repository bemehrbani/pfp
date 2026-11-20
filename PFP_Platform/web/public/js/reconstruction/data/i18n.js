/**
 * Trilingual (EN / FI / FA) localization dictionary & human narrator profiles.
 */
import { appState } from '../state.js';
import { GUIDED_TOUR_STOPS } from './tour-config.js';

export const I18N_DATA = {
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
    preStrikeBtn: "Before Strike",
    postStrikeBtn: "After Strike",
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
    preStrikeBtn: "Ennen iskua",
    postStrikeBtn: "Iskun jälkeen",
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
    preStrikeBtn: "پیش از حمله",
    postStrikeBtn: "پس از حمله",
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

export const NARRATOR_PROFILES = {
  mostafa_fi: {
    id: 'mostafa_fi',
    actor: 'mostafa',
    lang: 'fi',
    prefix: 'fi',
    dir: 'voices/mostafa_fi',
    fallbackDir: '.',
    hudLabel: { en: 'Voice: Mostafa (FI)', fa: 'راوی: مصطفی جلالی (FI)', fi: 'Ääni: Mostafa (FI)' },
    shortLabel: { en: '🎙️ Mostafa', fa: '🎙️ مصطفی (FI)', fi: '🎙️ Mostafa' }
  },
  mostafa_fa: {
    id: 'mostafa_fa',
    actor: 'mostafa',
    lang: 'fa',
    prefix: 'fa',
    dir: 'voices/mostafa_fa',
    fallbackDir: 'voices/leila_fa',
    hudLabel: { en: 'Voice: Mostafa (FA)', fa: 'راوی: مصطفی جلالی', fi: 'Ääni: Mostafa (FA)' },
    shortLabel: { en: '🎙️ Mostafa', fa: '🎙️ مصطفی جلالی', fi: '🎙️ Mostafa' }
  },
  mostafa_en: {
    id: 'mostafa_en',
    actor: 'mostafa',
    lang: 'en',
    prefix: 'en',
    dir: 'voices/mostafa_en',
    fallbackDir: 'voices/leila_en',
    hudLabel: { en: 'Voice: Mostafa (EN)', fa: 'راوی: مصطفی جلالی (EN)', fi: 'Ääni: Mostafa (EN)' },
    shortLabel: { en: '🎙️ Mostafa', fa: '🎙️ مصطفی (EN)', fi: '🎙️ Mostafa' }
  },
  leila_fa: {
    id: 'leila_fa',
    actor: 'leila',
    lang: 'fa',
    prefix: 'fa',
    dir: 'voices/leila_fa',
    fallbackDir: 'voices/mostafa_fa',
    hudLabel: { en: 'Voice: Leila (FA)', fa: 'راوی: لیلا غضنفری', fi: 'Ääni: Leila (FA)' },
    shortLabel: { en: '🎙️ Leila', fa: '🎙️ لیلا غضنفری', fi: '🎙️ Leila' }
  },
  leila_en: {
    id: 'leila_en',
    actor: 'leila',
    lang: 'en',
    prefix: 'en',
    dir: 'voices/leila_en',
    fallbackDir: 'voices/leila_en',
    hudLabel: { en: 'Voice: Leila (EN)', fa: 'راوی: لیلا (EN)', fi: 'Ääni: Leila (EN)' },
    shortLabel: { en: '🎙️ Leila', fa: '🎙️ لیلا (EN)', fi: '🎙️ Leila' }
  },
  ali_en: {
    id: 'ali_en',
    actor: 'ali',
    lang: 'en',
    prefix: 'en',
    dir: 'voices/ali_en',
    fallbackDir: 'voices/leila_en',
    hudLabel: { en: 'Voice: Ali (EN)', fa: 'راوی: علی (EN)', fi: 'Ääni: Ali (EN)' },
    shortLabel: { en: '🎙️ Ali', fa: '🎙️ علی (EN)', fi: '🎙️ Ali' }
  }
};

export function initI18n() {
  if (typeof window === 'undefined') return;
  const params = new URLSearchParams(window.location.search);
  const urlVoice = params.get('voice');
  const urlLang = params.get('lang');
  let saved = null;
  try {
    saved = window.localStorage ? window.localStorage.getItem('pfp_lang') : null;
  } catch (_) {}

  if (urlVoice && NARRATOR_PROFILES[urlVoice]) {
    appState.activeVoiceProfile = urlVoice;
    appState.preferredVoiceByLang[NARRATOR_PROFILES[urlVoice].lang] = urlVoice;
    appState.currentLang = NARRATOR_PROFILES[urlVoice].lang;
  } else if (urlLang && ['en', 'fi', 'fa'].includes(urlLang)) {
    appState.currentLang = urlLang;
    appState.activeVoiceProfile =
      appState.preferredVoiceByLang[appState.currentLang] || appState.preferredVoiceByLang.en;
  } else if (saved && ['en', 'fi', 'fa'].includes(saved)) {
    appState.currentLang = saved;
    appState.activeVoiceProfile =
      appState.preferredVoiceByLang[appState.currentLang] || appState.preferredVoiceByLang.en;
  }
  applyTranslations();
  updateNarratorButtonsUI();
}

export function applyTranslations() {
  if (typeof document === 'undefined') return;
  const lang = appState.currentLang;
  const t = I18N_DATA[lang] || I18N_DATA.en;
  document.documentElement.lang = lang;
  document.documentElement.dir = lang === 'fa' ? 'rtl' : 'ltr';
  if (document.body) {
    document.body.dir = lang === 'fa' ? 'rtl' : 'ltr';
  }

  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const key = el.getAttribute('data-i18n');
    if (key && t[key]) el.textContent = t[key];
  });

  document.querySelectorAll('.lang-btn').forEach((btn) => {
    const btnLang = btn.getAttribute('data-lang') || btn.getAttribute('data-pfp-lang');
    btn.classList.toggle('active', btnLang === lang);
  });
}

export function updateNarratorButtonsUI() {
  if (typeof document === 'undefined') return;
  const lang = appState.currentLang;
  const prof = NARRATOR_PROFILES[appState.activeVoiceProfile] || NARRATOR_PROFILES.mostafa_en;
  const labelText = prof.hudLabel[lang] || prof.hudLabel.en;
  const hudLbl = document.getElementById('hudNarratorLabel');
  if (hudLbl) hudLbl.textContent = labelText;
  const subLbl = document.getElementById('subrowNarratorLabel');
  if (subLbl) subLbl.textContent = labelText;
  const storyBtn = document.getElementById('btnStoryNarrator');
  if (storyBtn) {
    storyBtn.textContent = prof.shortLabel[lang] || prof.shortLabel.en;
  }

  const slotLabels = {
    mostafa: lang === 'fa' ? 'مصطفی' : 'Mostafa',
    leila: lang === 'fa' ? 'لیلا' : 'Leila',
    ali: lang === 'fa' ? 'علی (EN)' : 'Ali',
  };
  document.querySelectorAll('[data-voice-slot]').forEach((btn) => {
    const slot = btn.getAttribute('data-voice-slot');
    if (slot && slotLabels[slot]) btn.textContent = slotLabels[slot];
    if (slot === 'leila') {
      btn.style.display = lang === 'fi' ? 'none' : '';
    } else if (slot === 'ali') {
      btn.style.display = lang === 'fa' || lang === 'fi' ? 'none' : '';
    }
    btn.classList.toggle('active', prof.actor === slot);
  });
}

export function setLanguage(lang) {
  if (!['en', 'fi', 'fa'].includes(lang)) return;
  appState.currentLang = lang;
  try {
    if (typeof localStorage !== 'undefined') localStorage.setItem('pfp_lang', lang);
  } catch (_) {}

  const targetLangBucket = ['fa', 'fi', 'en'].includes(lang) ? lang : 'en';
  const curProf = NARRATOR_PROFILES[appState.activeVoiceProfile];
  if (!curProf || curProf.lang !== targetLangBucket) {
    appState.activeVoiceProfile =
      appState.preferredVoiceByLang[targetLangBucket] || appState.preferredVoiceByLang.en;
  }

  applyTranslations();
  appState.callbacks.applyBookendTexts?.();
  updateNarratorButtonsUI();
  appState.callbacks.updateHotspotLabels?.();
  appState.callbacks.refreshInWorldScreensLanguage?.();
  if (appState.activeHotspotId) {
    appState.callbacks.showHotspotModal?.(appState.activeHotspotId);
  }
  if (appState.isGuidedTour) {
    appState.callbacks.renderGuidedTourStep?.(appState.currentTourIndex, true);
  }
}

export function setNarratorProfile(profileId, restartAudio = true) {
  const prof = NARRATOR_PROFILES[profileId];
  if (!prof) return;
  appState.activeVoiceProfile = profileId;
  appState.preferredVoiceByLang[prof.lang] = profileId;

  if (prof.lang && prof.lang !== appState.currentLang) {
    appState.currentLang = prof.lang;
    try {
      if (typeof localStorage !== 'undefined') localStorage.setItem('pfp_lang', prof.lang);
    } catch (_) {}
    applyTranslations();
    appState.callbacks.updateHotspotLabels?.();
    appState.callbacks.refreshInWorldScreensLanguage?.();
  }
  updateNarratorButtonsUI();

  if (restartAudio && appState.isGuidedTour) {
    const stop = GUIDED_TOUR_STOPS[appState.currentTourIndex];
    if (stop) appState.callbacks.playSpotNarration?.(stop.hotspotId);
  } else if (restartAudio && appState.activeNarrationHotspot && appState.callbacks.isSpotAudioPlaying?.()) {
    appState.callbacks.playSpotNarration?.(appState.activeNarrationHotspot);
  }
}

export function selectNarratorByActor(actor) {
  appState.callbacks.resetWalkthroughIdleTimer?.();
  if (appState.currentLang === 'fa') {
    if (actor === 'mostafa') setNarratorProfile('mostafa_fa', true);
    else if (actor === 'leila') setNarratorProfile('leila_fa', true);
    else if (actor === 'ali') setNarratorProfile('ali_en', true);
  } else if (appState.currentLang === 'fi') {
    if (actor === 'mostafa') setNarratorProfile('mostafa_fi', true);
    else if (actor === 'leila') setNarratorProfile('leila_en', true);
    else if (actor === 'ali') setNarratorProfile('ali_en', true);
  } else {
    if (actor === 'mostafa') setNarratorProfile('mostafa_en', true);
    else if (actor === 'leila') setNarratorProfile('leila_en', true);
    else if (actor === 'ali') setNarratorProfile('ali_en', true);
  }
}

export function cycleNarratorForCurrentLanguage() {
  if (appState.currentLang === 'fa') {
    const nextFa = appState.activeVoiceProfile === 'mostafa_fa' ? 'leila_fa' : 'mostafa_fa';
    setNarratorProfile(nextFa, true);
  } else if (appState.currentLang === 'fi') {
    setNarratorProfile('mostafa_fi', true);
  } else {
    const order = ['mostafa_en', 'leila_en', 'ali_en'];
    const curIdx = order.indexOf(appState.activeVoiceProfile);
    const nextEn = order[(curIdx + 1) % order.length];
    setNarratorProfile(nextEn, true);
  }
}
