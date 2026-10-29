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
    vowPledgeText: "\"Having walked through the reconstructed halls of Shajareh Tayyebeh Primary School and witnessed the lives of the 120+ schoolchildren and 26 educators taken on February 28, 2026, I solemnly vow to stand ready and participate in every lawful civic, investigative, and judicial endeavor to hold every person in the chain of command responsible for this atrocity.\"",
    vowNameLabel: "Full Name *",
    vowEmailLabel: "Email Address *",
    vowCityLabel: "City & Country *",
    vowHowLabel: "How I Will Contribute to Accountability",
    vowMessageLabel: "Personal Message of Remembrance or Commitment (Optional)",
    vowConsentText: "I affirm this vow and consent to be contacted by People for Peace & Justice ry when collective legal, parliamentary, or civic actions are mobilized.",
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
    vowPledgeText: "\"Kuljettuani Shajareh Tayyebehin peruskoulun rekonstruoiduissa tiloissa ja nähtyäni 28.2.2026 surmattujen yli 120 koululaisen ja 26 opettajan kohtalon, lupaan olla valmis osallistumaan kaikkiin laillisiin kansalais-, tutkinta- ja oikeustoimiin, jotta jokainen tähän julmuuteen syyllistynyt saatetaan vastuuseen.\"",
    vowNameLabel: "Koko nimi *",
    vowEmailLabel: "Sähköpostiosoite *",
    vowCityLabel: "Kaupunki & Maa *",
    vowHowLabel: "Miten voin osallistua vastuuseen saattamiseen",
    vowMessageLabel: "Henkilökohtainen muistoviesti (Valinnainen)",
    vowConsentText: "Vahvistan tämän lupauksen ja suostun siihen, että People for Peace & Justice ry ottaa minuun yhteyttä yhteisten toimien käynnistyessä.",
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
    vowSubtitle: "۲۰ نوامبر (روز جهانی کودک) · انجمن صلح و عدالت (PFPJ ry)",
    vowPledgeText: "«پس از گام برداشتن در کلاس‌ها و راهروهای بازسازی‌شده دبستان شجره طیبه میناب و مشاهده تصاویر و زندگی بیش از ۱۲۰ کودک دانش‌آموز و ۲۶ آموزگار که در ۹ اسفند ۱۴۰۴ جان باختند، صمیمانه پیمان می‌بندم که در هر تلاش قانونی، مدنی، تحقیقاتی و قضایی برای پاسخگو کردن تمامی آمران و عاملان این جنایت مشارکت و همراهی کنم.»",
    vowNameLabel: "نام و نام خانوادگی *",
    vowEmailLabel: "آدرس ایمیل *",
    vowCityLabel: "شهر و کشور محل سکونت *",
    vowHowLabel: "نحوه همراهی و مشارکت من در دادخواهی",
    vowMessageLabel: "پیام یادبود یا تعهد شخصی (اختیاری)",
    vowConsentText: "این میثاق را تأیید می‌کنم و موافقم در زمان آغاز اقدامات جمعی حقوقی، پارلمانی و مدنی با من تماس گرفته شود.",
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
    cutawayMode: 0, // Full building
    camPos: [16, 2.4, 15],
    lookAt: [4, 2.0, 0],
    badge: { en: "STOP 1 OF 8 · COURTYARD YELLOW ASSEMBLY LINES", fi: "PISTE 1/8 · KOULUPIHAN AAMURIVIT", fa: "ایستگاه ۱ از ۸ · خطوط زرد صف صبحگاهی در حیاط" }
  },
  {
    hotspotId: 'boys_flower_arch',
    temporal: 0.0,
    cutawayMode: 2, // Ground floor cutaway so room is open & bright
    camPos: [8, 2.2, -1.5],
    lookAt: [12, 1.8, -5.8],
    badge: { en: "STOP 2 OF 8 · GROUND FLOOR: BOYS' CEREMONY ROOM (ROSE ARCHES)", fi: "PISTE 2/8 · ALAKERTA: POIKIEN JUHLAHUONE", fa: "ایستگاه ۲ از ۸ · طبقه همکف: اتاق جشن پسران (طاق گل رز)" }
  },
  {
    hotspotId: 'boys_classroom',
    temporal: 0.0,
    cutawayMode: 2, // Ground floor cutaway
    camPos: [-8, 2.2, -1.5],
    lookAt: [-13, 1.8, -5.8],
    badge: { en: "STOP 3 OF 8 · GROUND FLOOR: BOYS' CLASSROOM (CLAPPING & SINGING)", fi: "PISTE 3/8 · ALAKERTA: POIKIEN LUOKKAHUONE", fa: "ایستگاه ۳ از ۸ · طبقه همکف: کلاس درس پسران" }
  },
  {
    hotspotId: 'rainbow_staircase',
    temporal: 0.0,
    cutawayMode: 2, // Ground floor cutaway showing staircase
    camPos: [-1, 2.2, -2.2],
    lookAt: [-1, 2.3, -9.5],
    badge: { en: "STOP 4 OF 8 · THE RAINBOW STAIRCASE & PURPLE DOORS", fi: "PISTE 4/8 · SATEENKAARIPORTAIKKO", fa: "ایستگاه ۴ از ۸ · راه‌پله رنگین‌کمان و درهای بنفش" }
  },
  {
    hotspotId: 'girls_upper_hall',
    temporal: 0.0,
    cutawayMode: 1, // First floor cutaway showing upper rooms
    camPos: [-9, 6.0, -1.0],
    lookAt: [-14, 5.2, -6.5],
    badge: { en: "STOP 5 OF 8 · FIRST FLOOR: GIRLS' ASSEMBLY HALL & PINK/GREEN ROOMS", fi: "PISTE 5/8 · YLÄKERTA: TYTTÖJEN SALI", fa: "ایستگاه ۵ از ۸ · طبقه اول: سالن بزرگ دختران و کلاس‌های صورتی/سبز" }
  },
  {
    hotspotId: 'crater_damage',
    temporal: 1.0,
    cutawayMode: 0,
    camPos: [-18, 14.0, 14.0],
    lookAt: [-4, 2.0, -6.0],
    badge: { en: "STOP 6 OF 8 · 11:22 AM STRIKE: 5M CRATER & EXTENT OF COLLAPSE", fi: "PISTE 6/8 · KLO 11.22 ISKU: 5M KRAATTERI", fa: "ایستگاه ۶ از ۸ · ساعت ۱۱:۲۲: گودال ۵ متری و محدوده تخریب" }
  },
  {
    hotspotId: 'second_wave',
    temporal: 1.0,
    cutawayMode: 0,
    camPos: [20, 8.0, 16.0],
    lookAt: [3.5, 1.5, 2.1],
    badge: { en: "STOP 7 OF 8 · 2:30 PM SECOND WAVE & TOMAHAWK EVIDENCE", fi: "PISTE 7/8 · KLO 14.30 TOINEN ISKUAALTO", fa: "ایستگاه ۷ از ۸ · ساعت ۱۴:۳۰: موج دوم حملات و شواهد تاماهاک" }
  },
  {
    hotspotId: 'vow_shrine',
    temporal: 0.0,
    cutawayMode: 1,
    camPos: [0, 2.2, 16.5],
    lookAt: [0, 2.2, 9.0],
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
let vowSignatoryCount = parseInt(localStorage.getItem('pfp_vow_count') || '1428', 10);

// --- INITIALIZATION ---
function startReconstructionApp() {
  if (typeof THREE === 'undefined') {
    setTimeout(startReconstructionApp, 100);
    return;
  }
  clock = new THREE.Clock();
  updateVowBadge();
  initI18n();
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
  const badge = document.getElementById('vowCountBadge');
  if (badge) badge.textContent = vowSignatoryCount.toLocaleString();
}

// --- LOCALIZATION HANDLER ---
function initI18n() {
  const saved = localStorage.getItem('pfp_lang');
  if (saved && ['en', 'fi', 'fa'].includes(saved)) {
    currentLang = saved;
  }
  applyTranslations();
}

function setLanguage(lang) {
  currentLang = lang;
  localStorage.setItem('pfp_lang', lang);
  applyTranslations();
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

  // 1. Yellow Wireframe Frustum Pyramid (matching Forensic Architecture's yellow camera cones)
  const yellowLineMat = new THREE.LineBasicMaterial({ color: 0xe5e059 });
  const hw = width / 2;
  const hh = height / 2;

  // Frame rectangle corners in local space of photoPos
  const corners = [
    new THREE.Vector3(-hw, -hh, 0),
    new THREE.Vector3(hw, -hh, 0),
    new THREE.Vector3(hw, hh, 0),
    new THREE.Vector3(-hw, hh, 0)
  ];

  const frameGroup = new THREE.Group();
  frameGroup.position.set(photoPos[0], photoPos[1], photoPos[2]);
  frameGroup.rotation.y = rotY;

  // Outer yellow border
  const borderPts = [...corners, corners[0]];
  const borderGeo = new THREE.BufferGeometry().setFromPoints(borderPts);
  frameGroup.add(new THREE.Line(borderGeo, yellowLineMat));

  // Pyramid rays from camera apex to photo corners
  const localCam = new THREE.Vector3(0, 0, 2.2);
  const rayPts = [];
  corners.forEach(c => {
    rayPts.push(localCam, c);
  });
  const rayGeo = new THREE.BufferGeometry().setFromPoints(rayPts);
  frameGroup.add(new THREE.LineSegments(rayGeo, yellowLineMat));

  // Load actual school archive image onto the plane
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
}

// --- TERRAIN, COURTYARD YELLOW ASSEMBLY LINES, PASTEL WALLS & VOW SHRINE ---
function buildEnvironmentAndTerrain() {
  const groundGeo = new THREE.PlaneGeometry(160, 140, 16, 16);
  const groundMat = new THREE.MeshStandardMaterial({ color: 0x22252a, roughness: 0.9, metalness: 0.1 });
  const ground = new THREE.Mesh(groundGeo, groundMat);
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  terrainGroup.add(ground);

  // Main Courtyard Asphalt
  const yardGeo = new THREE.PlaneGeometry(68, 48);
  const yardMat = new THREE.MeshStandardMaterial({ color: 0x363b44, roughness: 0.82 });
  const yard = new THREE.Mesh(yardGeo, yardMat);
  yard.rotation.x = -Math.PI / 2;
  yard.position.set(0, 0.02, 4);
  yard.receiveShadow = true;
  terrainGroup.add(yard);

  // ========================================================
  // VERIFIED COURTYARD MARKINGS (FA 01_reconstruction 00:35)
  // 1. Six Parallel Yellow Assembly Lines + Yellow Standing Circles inside Green Border
  // ========================================================
  const assemblyGroup = new THREE.Group();
  assemblyGroup.position.set(13, 0.04, 8.5);

  const greenBorderMat = new THREE.MeshBasicMaterial({ color: 0x3b6e4c, side: THREE.DoubleSide });
  const yellowMarkMat = new THREE.MeshBasicMaterial({ color: 0xd9cf52, side: THREE.DoubleSide });

  // Outer green rectangle border (10m x 12m)
  const gTop = new THREE.Mesh(new THREE.PlaneGeometry(10.4, 0.25), greenBorderMat);
  gTop.rotation.x = -Math.PI / 2; gTop.position.set(0, 0, -6);
  assemblyGroup.add(gTop);
  const gBot = new THREE.Mesh(new THREE.PlaneGeometry(10.4, 0.25), greenBorderMat);
  gBot.rotation.x = -Math.PI / 2; gBot.position.set(0, 0, 6);
  assemblyGroup.add(gBot);

  for (let i = 0; i < 6; i++) {
    const lx = -4.2 + i * 1.68;
    // Yellow line
    const yLine = new THREE.Mesh(new THREE.PlaneGeometry(0.22, 11.6), yellowMarkMat);
    yLine.rotation.x = -Math.PI / 2;
    yLine.position.set(lx, 0.005, 0);
    assemblyGroup.add(yLine);

    // Yellow standing circle at the head of each line (facing school)
    const yDot = new THREE.Mesh(new THREE.CircleGeometry(0.32, 20), yellowMarkMat);
    yDot.rotation.x = -Math.PI / 2;
    yDot.position.set(lx - 0.45, 0.006, -5.2);
    assemblyGroup.add(yDot);
  }
  terrainGroup.add(assemblyGroup);

  // 2. White Circular Play Marking with Star (FA 02_progression)
  const whiteLineMat = new THREE.MeshBasicMaterial({ color: 0xcbd5e1, side: THREE.DoubleSide });
  const playRing = new THREE.Mesh(new THREE.RingGeometry(2.8, 2.95, 32), whiteLineMat);
  playRing.rotation.x = -Math.PI / 2;
  playRing.position.set(-14, 0.04, 11);
  terrainGroup.add(playRing);

  // 3. Courtyard Perimeter Wall with Pastel Yellow, Mint Green, White & Sky Blue Panels (rec_04.jpg)
  const wallMat = new THREE.MeshStandardMaterial({ color: 0xdbe0e6, roughness: 0.85 });
  const wallHeight = 2.6;
  const wallThickness = 0.45;

  // North (Rear) Wall
  const nWall = new THREE.Mesh(new THREE.BoxGeometry(68, wallHeight, wallThickness), wallMat);
  nWall.position.set(0, wallHeight / 2, -19.5);
  terrainGroup.add(nWall);

  // South Wall
  const sWall = new THREE.Mesh(new THREE.BoxGeometry(68, wallHeight, wallThickness), wallMat);
  sWall.position.set(0, wallHeight / 2, 27.5);
  terrainGroup.add(sWall);

  // East Wall with alternating Pastel Yellow, Mint Green & White panels (visible in rec_04.jpg)
  const eWall = new THREE.Mesh(new THREE.BoxGeometry(wallThickness, wallHeight, 47), wallMat);
  eWall.position.set(34, wallHeight / 2, 4);
  terrainGroup.add(eWall);

  const pastelPalette = [0xd8d896, 0x9ec4a5, 0xf1f5f9, 0x9ec4a5, 0xd8d896, 0x8ab8c9];
  for (let i = 0; i < 6; i++) {
    const pPanel = new THREE.Mesh(
      new THREE.BoxGeometry(0.08, 2.3, 5.5),
      new THREE.MeshStandardMaterial({ color: pastelPalette[i], roughness: 0.7 })
    );
    pPanel.position.set(33.72, 1.25, -12 + i * 6.0);
    terrainGroup.add(pPanel);
  }

  // Red & White Striped Corner Shed / Gatehouse (visible in rec_04.jpg)
  const shed = new THREE.Mesh(
    new THREE.BoxGeometry(5.5, 3.0, 4.0),
    new THREE.MeshStandardMaterial({ color: 0xc84b31, roughness: 0.7 })
  );
  shed.position.set(30.5, 1.5, 24.5);
  terrainGroup.add(shed);

  // West Wall
  const wWall = new THREE.Mesh(new THREE.BoxGeometry(wallThickness, wallHeight, 47), wallMat);
  wWall.position.set(-34, wallHeight / 2, 4);
  terrainGroup.add(wWall);

  // ==========================================
  // CENTRAL ACCOUNTABILITY VOW SHRINE / OBELISK
  // ==========================================
  const shrinePedestal = new THREE.Mesh(
    new THREE.CylinderGeometry(2.0, 2.4, 0.42, 24),
    new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.4, metalness: 0.5 })
  );
  shrinePedestal.position.set(0, 0.21, 10.5);
  memorialBoardsGroup.add(shrinePedestal);

  const goldRing = new THREE.Mesh(
    new THREE.RingGeometry(2.1, 2.35, 32),
    new THREE.MeshBasicMaterial({ color: 0xd4a853, side: THREE.DoubleSide })
  );
  goldRing.rotation.x = -Math.PI / 2;
  goldRing.position.set(0, 0.05, 10.5);
  memorialBoardsGroup.add(goldRing);

  const obelisk = new THREE.Mesh(
    new THREE.CylinderGeometry(0.32, 0.6, 3.4, 8),
    new THREE.MeshStandardMaterial({
      color: 0xd4a853,
      emissive: 0xd4a853,
      emissiveIntensity: 0.28,
      metalness: 0.75,
      roughness: 0.25
    })
  );
  obelisk.position.set(0, 2.1, 10.5);
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

function create3DFramedPortraitOnWall(parentGroup, loader, item, x, y, z, rotY, frameW, frameH, borderHex, cutawayMode, wingLabel) {
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

  // Compute camera focus point 2.2m in front of the portrait normal
  const normal = new THREE.Vector3(0, 0, 1).applyAxisAngle(new THREE.Vector3(0, 1, 0), rotY);
  const focusCam = new THREE.Vector3(x, y + 0.1, z).add(normal.clone().multiplyScalar(2.35));
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

function create3DRubbleDrawingOnWall(parentGroup, loader, drw, x, y, z, rotY, frameW, frameH, cutawayMode, wingLabel) {
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

  const normal = new THREE.Vector3(0, 0, 1).applyAxisAngle(new THREE.Vector3(0, 1, 0), rotY);
  const focusCam = new THREE.Vector3(x, y + 0.1, z).add(normal.clone().multiplyScalar(2.35));
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

  const woodMat = new THREE.MeshStandardMaterial({ color: 0x8b5a2b, roughness: 0.75 });
  const top = new THREE.Mesh(new THREE.BoxGeometry(1.15, 0.06, 0.68), woodMat);
  top.position.set(0, 0.68, 0);
  top.castShadow = true;
  deskGroup.add(top);

  const bench = new THREE.Mesh(new THREE.BoxGeometry(1.15, 0.42, 0.34), woodMat);
  bench.position.set(0, 0.21, 0.52);
  deskGroup.add(bench);

  if (drw) {
    const sheet = new THREE.Mesh(
      new THREE.PlaneGeometry(0.48, 0.36),
      new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide })
    );
    sheet.rotation.x = -Math.PI / 2;
    sheet.position.set(0, 0.715, 0);
    deskGroup.add(sheet);

    loader.load(drw.thumb || drw.image, (tex) => {
      sheet.material = new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide });
      sheet.material.needsUpdate = true;
    });

    const artifactData = {
      artifactType: 'drawing',
      item: drw,
      wingLabel: 'Ground Floor Classroom Desk (Recovered from Rubble)',
      focusCam: new THREE.Vector3(x, yBase + 1.9, z + 1.4),
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

  // 1. COURTYARD MEMORIAL STELE WALK (24 Double-Sided Steles around the Vow Shrine)
  const portraitSample = childrenList.filter(c => c.photoPath).slice(0, 24);
  const cols = 12;
  const startX = -16.5;
  const spacingX = 3.0;

  portraitSample.forEach((child, idx) => {
    const row = Math.floor(idx / cols);
    const col = idx % cols;
    const x = startX + col * spacingX;
    const z = 19.5 + row * 3.0;
    const imgUrl = child.photoPath;

    const post = new THREE.Mesh(
      new THREE.BoxGeometry(1.38, 2.02, 0.12),
      new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.5 })
    );
    post.position.set(x, 1.18, z);
    post.rotation.y = Math.PI;
    post.castShadow = true;
    memorialBoardsGroup.add(post);

    const border = new THREE.Mesh(
      new THREE.BoxGeometry(1.44, 2.08, 0.08),
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
      new THREE.PlaneGeometry(1.24, 0.34),
      new THREE.MeshBasicMaterial({ map: labelTex, side: THREE.DoubleSide })
    );
    frontLabel.position.set(0, -0.74, 0.075);
    post.add(frontLabel);

    const backLabel = frontLabel.clone();
    backLabel.position.set(0, -0.74, -0.075);
    backLabel.rotation.y = Math.PI;
    post.add(backLabel);

    const steleArtifact = {
      artifactType: 'victim',
      item: child,
      wingLabel: 'Courtyard 100 Faces Memorial Walk',
      focusCam: new THREE.Vector3(x, 1.5, z - 2.6),
      lookAt: new THREE.Vector3(x, 1.2, z),
      cutawayMode: 0
    };
    post.userData = steleArtifact;
    clickable3DArtifacts.push(post);

    if (imgUrl) {
      loader.load(imgUrl, (tex) => {
        const portraitMesh = new THREE.Mesh(
          new THREE.PlaneGeometry(1.24, 1.48),
          new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide })
        );
        portraitMesh.position.set(0, 0.18, 0.075);
        portraitMesh.userData = steleArtifact;
        post.add(portraitMesh);
        clickable3DArtifacts.push(portraitMesh);

        const backMesh = portraitMesh.clone();
        backMesh.position.set(0, 0.18, -0.075);
        backMesh.rotation.y = Math.PI;
        backMesh.userData = steleArtifact;
        post.add(backMesh);
        clickable3DArtifacts.push(backMesh);
      });
    }
  });

  if (!groundFloorGroup || !firstFloorGroup) return;

  // =========================================================================
  // 2. GROUND FLOOR WEST WING: BOYS OF GRADES 1, 2 & 3 (55 BOYS WITH PORTRAITS)
  // =========================================================================
  const boysGrades1to3 = childrenList.filter(c => c.gender === 'boy' && (c.grade || 1) <= 3 && c.photoPath);
  createWingBannerIn3D(
    groundFloorGroup,
    `GROUND FLOOR WEST CLASSROOMS · BOYS GRADES 1–3 (${boysGrades1to3.length} STUDENTS)`,
    `کلاس‌های طبقه همکف (بال غربی) · ۵۵ دانش‌آموز پسر پایه‌های اول تا سوم`,
    -12.75, 3.22, -12.70, 0, 7.6, '#0d1b2a', '#38bdf8'
  );

  // Place along West Wall (x = -18.74, facing East +X, rotY = Math.PI / 2): 2 rows x 12 cols = 24 portraits
  let bIdx = 0;
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 12; col++) {
      if (bIdx >= boysGrades1to3.length) break;
      const z = -12.1 + col * 1.08;
      const y = 1.25 + row * 1.18;
      create3DFramedPortraitOnWall(
        groundFloorGroup, loader, boysGrades1to3[bIdx++],
        -18.72, y, z, Math.PI / 2, 0.88, 1.06, 0x38bdf8, 2,
        'Ground Floor West Wing · Boys Classrooms (Grades 1–3)'
      );
    }
  }
  // Place along North-West Wall (z = -12.72, facing South +Z, rotY = 0): 2 rows x 9 cols = 18 portraits
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 9; col++) {
      if (bIdx >= boysGrades1to3.length) break;
      const x = -17.6 + col * 1.22;
      const y = 1.25 + row * 1.18;
      create3DFramedPortraitOnWall(
        groundFloorGroup, loader, boysGrades1to3[bIdx++],
        x, y, -12.72, 0, 0.88, 1.06, 0x38bdf8, 2,
        'Ground Floor North-West Classroom · Boys Grades 1–3'
      );
    }
  }
  // Place remaining Grade 1–3 boys along South-West Wall (z = 0.72, facing North -Z, rotY = Math.PI) & Cross Partition (z = -5.78, rotY = 0)
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 9; col++) {
      if (bIdx >= boysGrades1to3.length) break;
      const x = -17.6 + col * 1.22;
      const y = 1.25 + row * 1.18;
      create3DFramedPortraitOnWall(
        groundFloorGroup, loader, boysGrades1to3[bIdx++],
        x, y, 0.72, Math.PI, 0.88, 1.06, 0x38bdf8, 2,
        'Ground Floor South-West Classroom · Boys Grades 1–2'
      );
    }
  }

  // Add 6 Classroom Desks with 1st-Grade Rubble Drawings in the Ground Floor West Classroom
  const groundDeskDrawings = drawingsList.slice(0, 6);
  for (let d = 0; d < 6; d++) {
    const dx = -15.5 + (d % 3) * 2.8;
    const dz = -4.2 + Math.floor(d / 3) * 2.2;
    createClassroomDeskWithDrawing(groundFloorGroup, loader, groundDeskDrawings[d], dx, 0.2, dz, 2);
  }

  // =========================================================================
  // 3. GROUND FLOOR EAST WING: BOYS OF GRADES 4, 5 & 6 (17 BOYS WITH PORTRAITS)
  // =========================================================================
  const boysGrades4to6 = childrenList.filter(c => c.gender === 'boy' && (c.grade || 1) >= 4 && c.photoPath);
  createWingBannerIn3D(
    groundFloorGroup,
    `GROUND FLOOR EAST WING · BOYS GRADES 4–6 & CEREMONY ROOM (${boysGrades4to6.length} STUDENTS)`,
    `طبقه همکف (بال شرقی) · دانش‌آموزان پسر پایه‌های چهارم تا ششم و اتاق جشن`,
    12.75, 3.22, -12.70, 0, 7.6, '#0d1b2a', '#d4a853'
  );

  let b4Idx = 0;
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 10; col++) {
      if (b4Idx >= boysGrades4to6.length) break;
      const z = -12.0 + col * 1.18;
      const y = 1.25 + row * 1.18;
      create3DFramedPortraitOnWall(
        groundFloorGroup, loader, boysGrades4to6[b4Idx++],
        18.72, y, z, -Math.PI / 2, 0.92, 1.08, 0xd4a853, 2,
        'Ground Floor East Wing · Boys Grades 4–6 & Ceremony Room'
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
    0, 3.32, -12.70, 0, 7.2, '#1f122b', '#f472b6'
  );

  // Mount 13 teachers on Left Hall Wall (x = -6.32, facing East +X) and 13 on Right Hall Wall (x = +6.32, facing West -X)
  teachersList.forEach((teacher, idx) => {
    const isLeft = idx < 13;
    const localIdx = isLeft ? idx : idx - 13;
    const row = Math.floor(localIdx / 7);
    const col = localIdx % 7;
    // Space along Z avoiding purple doors at z = -3.0 and z = -9.0
    const zSlots = [-0.6, -1.7, -4.3, -5.4, -6.5, -7.6, -10.4];
    const z = zSlots[col] || (-1.0 - col * 1.4);
    const y = 1.25 + row * 1.18;
    const x = isLeft ? -6.32 : 6.32;
    const rotY = isLeft ? Math.PI / 2 : -Math.PI / 2;

    create3DFramedPortraitOnWall(
      groundFloorGroup, loader, teacher,
      x, y, z, rotY, 0.88, 1.06, 0xf472b6, 2,
      'Central Assembly Hall & Rainbow Staircase · 26 Martyred Female Educators'
    );
  });

  // =========================================================================
  // 5. FIRST FLOOR WEST HALL: ALL 47 MARTYRED SCHOOLGIRLS (GRADES 1–6)
  // =========================================================================
  const y1 = 3.6;
  const girlsAll = childrenList.filter(c => c.gender === 'girl' && c.photoPath);
  createWingBannerIn3D(
    firstFloorGroup,
    `FIRST FLOOR GIRLS' ASSEMBLY HALL · ALL ${girlsAll.length} MARTYRED SCHOOLGIRLS (GRADES 1–6)`,
    `طبقه اول (سالن بزرگ دختران) · ۴۷ دانش‌آموز دختر شهیده در پایه‌های اول تا ششم`,
    -13.2, y1 + 3.22, -12.70, 0, 7.8, '#2b1222', '#f472b6'
  );

  let gIdx = 0;
  // West Wall of Girls' Hall (x = -18.72, facing East +X): 2 rows x 12 cols = 24 portraits
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 12; col++) {
      if (gIdx >= girlsAll.length) break;
      const z = -12.1 + col * 1.08;
      const y = y1 + 1.25 + row * 1.18;
      create3DFramedPortraitOnWall(
        firstFloorGroup, loader, girlsAll[gIdx++],
        -18.72, y, z, Math.PI / 2, 0.88, 1.06, 0xf472b6, 1,
        'First Floor West Wing · Girls\' Assembly Hall (Grades 1–6)'
      );
    }
  }
  // North Wall of Girls' Hall (z = -12.72, facing South +Z): 2 rows x 7 cols = 14 portraits
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 7; col++) {
      if (gIdx >= girlsAll.length) break;
      const x = -17.6 + col * 1.32;
      const y = y1 + 1.25 + row * 1.18;
      create3DFramedPortraitOnWall(
        firstFloorGroup, loader, girlsAll[gIdx++],
        x, y, -12.72, 0, 0.88, 1.06, 0xf472b6, 1,
        'First Floor Girls\' Hall · North Wall Gallery'
      );
    }
  }
  // South Wall of Girls' Hall (z = 0.72, facing North -Z): remaining 9 portraits
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 7; col++) {
      if (gIdx >= girlsAll.length) break;
      const x = -17.6 + col * 1.32;
      const y = y1 + 1.25 + row * 1.18;
      create3DFramedPortraitOnWall(
        firstFloorGroup, loader, girlsAll[gIdx++],
        x, y, 0.72, Math.PI, 0.88, 1.06, 0xf472b6, 1,
        'First Floor Girls\' Hall · South Wall Gallery'
      );
    }
  }

  // =========================================================================
  // 6. FIRST FLOOR EAST CLASSROOMS: ALL 28 DRAWINGS & HOMEWORK PULLED FROM RUBBLE
  // =========================================================================
  createWingBannerIn3D(
    firstFloorGroup,
    `FIRST FLOOR CLASSROOMS · 28 DRAWINGS & HOMEWORK PULLED FROM THE RUBBLE`,
    `کلاس‌های طبقه اول · ۲۸ برگ نقاشی و مشق بیرون کشیده شده از زیر آوار مدرسه`,
    12.75, y1 + 3.22, -12.70, 0, 7.8, '#1e1b18', '#fcd34d'
  );

  let dIdx = 0;
  // East Wall (x = 18.72, facing West -X): 2 rows x 10 cols = 20 drawings
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 10; col++) {
      if (dIdx >= drawingsList.length) break;
      const z = -12.0 + col * 1.22;
      const y = y1 + 1.25 + row * 1.18;
      create3DRubbleDrawingOnWall(
        firstFloorGroup, loader, drawingsList[dIdx++],
        18.72, y, z, -Math.PI / 2, 1.02, 1.06, 1,
        'First Floor East Classroom · Rubble Drawings & Homework Archive'
      );
    }
  }
  // North-East Wall (z = -12.72, facing South +Z): remaining 8 drawings
  for (let col = 0; col < 8; col++) {
    if (dIdx >= drawingsList.length) break;
    const x = 7.8 + col * 1.32;
    const y = y1 + 1.85;
    create3DRubbleDrawingOnWall(
      firstFloorGroup, loader, drawingsList[dIdx++],
      x, y, -12.72, 0, 1.08, 1.12, 1,
      'First Floor East Classroom · Rubble Drawings & Homework Archive'
    );
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

// --- VERIFIED TWO-FLOOR WALKABLE SCHOOL ARCHITECTURE (FA INVESTIGATION 121) ---
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

  // Verified Materials from FA Video Frames (rec_03, rec_05, rec_08, rec_12, rec_17, rec_18, rec_21, rec_25, rec_26)
  const whiteWall = new THREE.MeshStandardMaterial({ color: 0xedeff2, roughness: 0.82 });
  const floorGrey = new THREE.MeshStandardMaterial({ color: 0x9ca3af, roughness: 0.85 });
  const floorGreen = new THREE.MeshStandardMaterial({ color: 0x5c7a62, roughness: 0.8 }); // Girls assembly & boys carpet floor
  const tealWall = new THREE.MeshStandardMaterial({ color: 0x5d8c96, roughness: 0.75 }); // Boys flower arch room
  const skyBlueWall = new THREE.MeshStandardMaterial({ color: 0x8ab8c9, roughness: 0.75 }); // Boys classroom & right facade
  const mintGreenWall = new THREE.MeshStandardMaterial({ color: 0x9ec4a5, roughness: 0.75 }); // Facade lower band
  const yellowFacade = new THREE.MeshStandardMaterial({ color: 0xd8d278, roughness: 0.75 }); // Left facade lower band
  const pinkWall = new THREE.MeshStandardMaterial({ color: 0xc86d8a, roughness: 0.75 }); // Girls upper classrooms
  const sageGreenWall = new THREE.MeshStandardMaterial({ color: 0x668768, roughness: 0.75 }); // Girls lower dado
  const purpleDoorMat = new THREE.MeshStandardMaterial({ color: 0x7c3f9c, roughness: 0.5 }); // Signature purple doors!
  const canopyGreenMat = new THREE.MeshStandardMaterial({ color: 0x9ab596, roughness: 0.7 }); // Rear shade roof

  // Helper to add a wall segment
  function addWall(group, w, h, d, x, y, z, mat) {
    const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat || whiteWall);
    m.position.set(x, y, z);
    m.castShadow = true;
    m.receiveShadow = true;
    group.add(m);
    return m;
  }

  // Helper to add a signature Purple Door with dark transom window above (rec_05.jpg, rec_17.jpg, rec_22.jpg)
  function addPurpleDoor(group, x, yBase, z, rotY) {
    const dGroup = new THREE.Group();
    dGroup.position.set(x, yBase, z);
    dGroup.rotation.y = rotY;
    const door = new THREE.Mesh(new THREE.BoxGeometry(1.15, 2.1, 0.18), purpleDoorMat);
    door.position.set(0, 1.05, 0);
    dGroup.add(door);
    const transom = new THREE.Mesh(
      new THREE.BoxGeometry(1.15, 0.55, 0.19),
      new THREE.MeshBasicMaterial({ color: 0x111827 })
    );
    transom.position.set(0, 2.4, 0);
    dGroup.add(transom);
    group.add(dGroup);
  }

  // =========================================================
  // 1. GROUND FLOOR (BOYS' SCHOOL & PRE-SCHOOL — rec_26.jpg)
  // Footprint: X from -19 to +19 (38m), Z from -13 to +1 (14m)
  // =========================================================
  // Ground floor slab
  addWall(groundFloorGroup, 38, 0.2, 14, 0, 0.1, -6, floorGrey);
  // Green carpet zones in west classroom & east ceremony room
  addWall(groundFloorGroup, 11, 0.22, 6.2, -13, 0.11, -9.5, floorGreen);
  addWall(groundFloorGroup, 11, 0.22, 6.2, 13, 0.11, -3.0, tealWall);

  // Exterior Perimeter Walls (Ground Floor)
  // South Facade (Left wing, Central recessed entry, Right wing)
  addWall(groundFloorGroup, 13, floorH, 0.35, -12.5, floorH / 2, 1.0, whiteWall);
  // Left wing Yellow exterior dado band (rec_03.jpg)
  addWall(groundFloorGroup, 13.1, 1.6, 0.38, -12.5, 0.8, 1.02, yellowFacade);

  addWall(groundFloorGroup, 13, floorH, 0.35, 12.5, floorH / 2, 1.0, whiteWall);
  // Right wing Sky-Blue & Mint-Green exterior dado bands (rec_03.jpg, rec_04.jpg)
  addWall(groundFloorGroup, 6.5, 2.2, 0.38, 9.2, 1.1, 1.02, skyBlueWall);
  addWall(groundFloorGroup, 6.5, 1.2, 0.39, 15.7, 0.6, 1.02, mintGreenWall);
  addWall(groundFloorGroup, 6.5, 1.0, 0.38, 15.7, 1.7, 1.02, skyBlueWall);

  // 4-Column Front Porch Portico (rec_03.jpg)
  for (const colX of [-5.2, -1.8, 1.8, 5.2]) {
    addWall(groundFloorGroup, 0.65, floorH, 0.65, colX, floorH / 2, 3.6, whiteWall);
  }
  // Portico flat canopy slab
  addWall(groundFloorGroup, 13.2, 0.45, 3.4, 0, floorH + 0.1, 2.3, whiteWall);

  // West, East, and North (Rear) Ground Floor Walls
  addWall(groundFloorGroup, 0.35, floorH, 14, -19, floorH / 2, -6, whiteWall);
  addWall(groundFloorGroup, 0.35, floorH, 14, 19, floorH / 2, -6, whiteWall);
  addWall(groundFloorGroup, 38, floorH, 0.35, 0, floorH / 2, -13, skyBlueWall);

  // Interior Ground Floor Partition Walls (forming Central Assembly Hall + 6 Classrooms — rec_26.jpg)
  addWall(groundFloorGroup, 0.25, floorH, 14, -6.5, floorH / 2, -6, skyBlueWall);
  addWall(groundFloorGroup, 0.25, floorH, 14, 6.5, floorH / 2, -6, tealWall);
  // Cross partitions in West & East wings
  addWall(groundFloorGroup, 12.5, floorH, 0.25, -12.75, floorH / 2, -6, skyBlueWall);
  addWall(groundFloorGroup, 12.5, floorH, 0.25, 12.75, floorH / 2, -6, tealWall);

  // Purple Classroom Doors along Ground Floor Central Assembly Hall (rec_05.jpg, rec_17.jpg)
  addPurpleDoor(groundFloorGroup, -6.35, 0.2, -3.0, Math.PI / 2);
  addPurpleDoor(groundFloorGroup, -6.35, 0.2, -9.0, Math.PI / 2);
  addPurpleDoor(groundFloorGroup, 6.35, 0.2, -3.0, -Math.PI / 2);
  addPurpleDoor(groundFloorGroup, 6.35, 0.2, -9.0, -Math.PI / 2);
  addPurpleDoor(groundFloorGroup, -3.2, 0.2, -11.5, 0);
  addPurpleDoor(groundFloorGroup, 3.2, 0.2, -11.5, 0);

  // =========================================================
  // THE RAINBOW STAIRCASE (Connecting Ground & First Floor — rec_17.jpg)
  // =========================================================
  const rainbowColors = [0xeab308, 0x3b82f6, 0xec4899, 0x22c55e, 0xeab308, 0x3b82f6, 0xef4444, 0x22c55e, 0xec4899, 0xeab308];
  for (let s = 0; s < 10; s++) {
    const stepMesh = new THREE.Mesh(
      new THREE.BoxGeometry(2.4, 0.34, 0.45),
      new THREE.MeshStandardMaterial({ color: rainbowColors[s], roughness: 0.5 })
    );
    stepMesh.position.set(0, 0.35 + s * 0.34, -8.5 - s * 0.42);
    groundFloorGroup.add(stepMesh);
  }

  // Rear Green Shade Canopy & Exterior Staircase (rec_15.jpg)
  const rearCanopy = new THREE.Mesh(new THREE.BoxGeometry(15, 0.18, 5.5), canopyGreenMat);
  rearCanopy.position.set(9.5, 3.5, -15.8);
  groundFloorGroup.add(rearCanopy);

  // Camera-Aligned Photos in Ground Floor Rooms (with Yellow Wireframe Camera Frustums!)
  // 1) Boys under Red Rose Arches (East Ground Room — rec_08.jpg)
  createCameraAlignedPhotoInSpace(
    groundFloorGroup,
    'images/fa_spots/spot_boys_flower_arch.jpg',
    [11, 1.8, -1.5],
    [12.5, 1.85, -5.6],
    0,
    4.2,
    2.4
  );

  // 2) Boys Clapping & Singing in Classroom (West Ground Room — rec_12.jpg)
  createCameraAlignedPhotoInSpace(
    groundFloorGroup,
    'images/fa_spots/spot_boys_classroom.jpg',
    [-11, 1.8, -6.5],
    [-12.8, 1.85, -12.4],
    0,
    4.4,
    2.5
  );

  // 3) Teachers & Girls at the Rainbow Staircase (Central Hall — rec_17.jpg)
  createCameraAlignedPhotoInSpace(
    groundFloorGroup,
    'images/fa_spots/spot_rainbow_stairs.jpg',
    [0, 1.8, -4.5],
    [0, 1.85, -7.8],
    0,
    3.8,
    2.2
  );

  // =========================================================
  // 2. FIRST FLOOR (GIRLS' PRIMARY SCHOOL — rec_25.jpg)
  // =========================================================
  const y1 = floorH;
  // First floor slab (with stairwell opening)
  addWall(firstFloorGroup, 16, 0.22, 14, -11, y1, -6, floorGreen); // Girls' West Hall has green floor (rec_21, rec_25)
  addWall(firstFloorGroup, 16, 0.22, 14, 11, y1, -6, floorGrey);
  addWall(firstFloorGroup, 6, 0.22, 7.5, 0, y1, -2.25, floorGrey);

  // Exterior First Floor Walls (Crisp White — rec_03.jpg, rec_25.jpg)
  addWall(firstFloorGroup, 38, floorH, 0.35, 0, y1 + floorH / 2, 1.0, whiteWall);
  addWall(firstFloorGroup, 38, floorH, 0.35, 0, y1 + floorH / 2, -13.0, whiteWall);
  addWall(firstFloorGroup, 0.35, floorH, 14, -19, y1 + floorH / 2, -6, whiteWall);
  addWall(firstFloorGroup, 0.35, floorH, 14, 19, y1 + floorH / 2, -6, whiteWall);

  // Interior First Floor Partitions: Pink & Sage Green Classrooms + Girls' Large West Assembly Hall (rec_18.jpg, rec_21.jpg, rec_25.jpg)
  addWall(firstFloorGroup, 0.25, floorH, 14, -7.5, y1 + floorH / 2, -6, pinkWall);
  addWall(firstFloorGroup, 0.25, floorH, 14, 6.5, y1 + floorH / 2, -6, whiteWall);

  // Pink upper + Sage Green lower classroom walls (rec_18.jpg, rec_25.jpg)
  addWall(firstFloorGroup, 7.0, 1.6, 0.25, -4.0, y1 + 0.8, -1.5, sageGreenWall);
  addWall(firstFloorGroup, 7.0, 2.0, 0.25, -4.0, y1 + 2.6, -1.5, pinkWall);
  addWall(firstFloorGroup, 12.5, floorH, 0.25, 12.75, y1 + floorH / 2, -6, pinkWall);

  // Purple Classroom Doors on First Floor (rec_22.jpg, rec_25.jpg)
  addPurpleDoor(firstFloorGroup, -7.35, y1 + 0.1, -4.0, Math.PI / 2);
  addPurpleDoor(firstFloorGroup, 6.35, y1 + 0.1, -3.5, -Math.PI / 2);
  addPurpleDoor(firstFloorGroup, 6.35, y1 + 0.1, -9.0, -Math.PI / 2);

  // Camera-Aligned Photo in First Floor Girls' Assembly Hall (80+ schoolgirls seated — rec_21.jpg)
  createCameraAlignedPhotoInSpace(
    firstFloorGroup,
    'images/fa_spots/spot_girls_assembly.jpg',
    [-11, y1 + 1.8, -2.0],
    [-13.2, y1 + 1.85, -8.5],
    0,
    4.8,
    2.7
  );

  // =========================================================
  // 3. ROOF & PARAPET GROUP (Toggled by Cutaway Button)
  // =========================================================
  const yRoof = floorH * 2;
  addWall(roofGroup, 38.4, 0.35, 14.4, 0, yRoof + 0.15, -6, whiteWall);
  // Stairwell roof penthouse box (visible in rec_01.jpg, rec_15.jpg)
  addWall(roofGroup, 5.5, 1.8, 4.2, -1.5, yRoof + 0.9, -10.2, whiteWall);

  // =========================================================
  // 4. POST-STRIKE GEOMETRY + FA YELLOW "EXTENT OF DAMAGE" BOX (rec_29.jpg & 07_impact_crater.mp4)
  // =========================================================
  const ruinedConcrete = new THREE.MeshStandardMaterial({ color: 0x47423d, roughness: 1.0 });
  const debrisMat = new THREE.MeshStandardMaterial({ color: 0x575049, roughness: 0.95 });

  // Standing Right (East) Wing (partially intact as shown in rec_29.jpg & sheet_07_crater.jpg)
  const eastStanding = new THREE.Mesh(new THREE.BoxGeometry(17, floorH * 2, 14), whiteWall);
  eastStanding.position.set(10.5, floorH, -6);
  eastStanding.castShadow = true; eastStanding.receiveShadow = true;
  postStrikeModelGroup.add(eastStanding);

  // Standing Front Portico Columns (survived at front edge — rec_29.jpg)
  for (const colX of [-1.8, 1.8, 5.2]) {
    const c = new THREE.Mesh(new THREE.BoxGeometry(0.65, floorH, 0.65), whiteWall);
    c.position.set(colX, floorH / 2, 3.6);
    postStrikeModelGroup.add(c);
  }

  // 5-Meter Impact Crater in the Central Assembly Hall (sheet_07_crater.jpg)
  const craterRim = new THREE.Mesh(new THREE.TorusGeometry(2.8, 0.65, 12, 28), ruinedConcrete);
  craterRim.rotation.x = -Math.PI / 2;
  craterRim.position.set(-2.5, 0.3, -6);
  postStrikeModelGroup.add(craterRim);

  // Yellow Circle around the 5m Impact Crater (matching FA's yellow crater circle in sheet_07_crater.jpg)
  const craterCircleRing = new THREE.Mesh(
    new THREE.RingGeometry(3.1, 3.28, 36),
    new THREE.MeshBasicMaterial({ color: 0xe5e059, side: THREE.DoubleSide })
  );
  craterCircleRing.rotation.x = -Math.PI / 2;
  craterCircleRing.position.set(-2.5, 0.45, -6);
  postStrikeModelGroup.add(craterCircleRing);

  // Collapsed West Wing & Central Assembly Rubble Slabs
  for (let i = 0; i < 36; i++) {
    const rx = -18 + Math.random() * 19;
    const rz = -12.5 + Math.random() * 13;
    const size = 0.6 + Math.random() * 1.4;
    const chunk = new THREE.Mesh(new THREE.BoxGeometry(size * 1.4, size * 0.45, size), debrisMat);
    chunk.position.set(rx, size * 0.35, rz);
    chunk.rotation.set((Math.random() - 0.5) * 0.6, Math.random() * Math.PI, (Math.random() - 0.5) * 0.6);
    chunk.castShadow = true;
    postStrikeModelGroup.add(chunk);
  }

  // Yellow Wireframe "Extent of Damage" Bounding Volume (matching rec_29.jpg!)
  const dmgBoxGeo = new THREE.BoxGeometry(21.5, floorH * 2 + 0.4, 14.6);
  const dmgEdges = new THREE.EdgesGeometry(dmgBoxGeo);
  const dmgWire = new THREE.LineSegments(dmgEdges, new THREE.LineBasicMaterial({ color: 0xe5e059 }));
  dmgWire.position.set(-8.5, floorH, -6);
  postStrikeModelGroup.add(dmgWire);

  const dmgFill = new THREE.Mesh(
    dmgBoxGeo,
    new THREE.MeshBasicMaterial({ color: 0xe5e059, transparent: true, opacity: 0.12, depthWrite: false })
  );
  dmgFill.position.copy(dmgWire.position);
  postStrikeModelGroup.add(dmgFill);

  // Camera-Aligned Post-Strike Crater Photogrammetry Frame inside the Crater
  createCameraAlignedPhotoInSpace(
    postStrikeModelGroup,
    'images/fa_spots/spot_crater_photo.jpg',
    [-2.5, 2.5, 1.0],
    [-2.5, 2.2, -5.5],
    0,
    5.0,
    2.8
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

// --- 8 CAMERA-ALIGNED HOTSPOTS ---
const HOTSPOT_CONFIGS = [
  { id: 'courtyard_lines', icon: '1', pos: [13, 1.2, 8.5], presetCam: [18, 4.5, 18], target: [8, 1.5, 2], cutaway: 0 },
  { id: 'boys_flower_arch', icon: '2', pos: [12.5, 2.2, -4.5], presetCam: [9, 4.2, 2], target: [12.5, 1.8, -5.6], cutaway: 2 },
  { id: 'boys_classroom', icon: '3', pos: [-12.8, 2.2, -10.5], presetCam: [-9, 4.2, -3], target: [-12.8, 1.8, -11.5], cutaway: 2 },
  { id: 'rainbow_staircase', icon: '4', pos: [0, 2.4, -7.8], presetCam: [0, 3.8, -1.5], target: [0, 2.0, -8.5], cutaway: 2 },
  { id: 'girls_upper_hall', icon: '5', pos: [-13.2, 5.8, -7.5], presetCam: [-8, 8.5, 2], target: [-13.2, 5.2, -7.5], cutaway: 1 },
  { id: 'crater_damage', icon: '6', pos: [-2.5, 3.2, -6.0], presetCam: [-16, 13, 12], target: [-4, 2.0, -6], cutaway: 0 },
  { id: 'second_wave', icon: '7', pos: [18, 2.5, 14.0], presetCam: [26, 8, 22], target: [8, 1.5, 4], cutaway: 0 },
  { id: 'vow_shrine', icon: '✍️', pos: [0, 3.8, 10.5], presetCam: [0, 2.4, 17.5], target: [0, 2.0, 10.5], isVow: true, cutaway: 1 }
];

function initHotspots() {
  const container = document.getElementById('canvasContainer');

  HOTSPOT_CONFIGS.forEach(cfg => {
    cfg.posVec = new THREE.Vector3(cfg.pos[0], cfg.pos[1], cfg.pos[2]);
    cfg.presetCamVec = new THREE.Vector3(cfg.presetCam[0], cfg.presetCam[1], cfg.presetCam[2]);
    cfg.targetVec = new THREE.Vector3(cfg.target[0], cfg.target[1], cfg.target[2]);

    const markerMesh = new THREE.Mesh(
      new THREE.SphereGeometry(0.35, 16, 16),
      new THREE.MeshBasicMaterial({ color: cfg.isVow ? 0x10b981 : 0xd4a853, transparent: true, opacity: 0.9 })
    );
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

// --- CALM, KIND & SORROWFUL FEMALE VOICEOVER ENGINE + GENTLE AMBIENT PAD ---
let narrationAudio = null;
let narrationRate = 0.94;
let ambientAudioCtx = null;
let ambientGainNode = null;

function startMemorialAmbientPad() {
  try {
    if (!ambientAudioCtx) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (!AudioContextClass) return;
      ambientAudioCtx = new AudioContextClass();

      ambientGainNode = ambientAudioCtx.createGain();
      ambientGainNode.gain.setValueAtTime(0.001, ambientAudioCtx.currentTime);

      const filter = ambientAudioCtx.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(340, ambientAudioCtx.currentTime);

      // Warm, sorrowful C-minor cello/pad chord (C3, Eb3, G3, Bb3)
      const freqs = [130.81, 155.56, 196.00, 233.08];
      freqs.forEach((f, idx) => {
        const osc = ambientAudioCtx.createOscillator();
        osc.type = idx % 2 === 0 ? 'sine' : 'triangle';
        osc.frequency.setValueAtTime(f, ambientAudioCtx.currentTime);
        const oscGain = ambientAudioCtx.createGain();
        oscGain.gain.setValueAtTime(idx === 0 ? 0.35 : 0.18, ambientAudioCtx.currentTime);
        osc.connect(oscGain);
        oscGain.connect(filter);
        osc.start();
      });

      filter.connect(ambientGainNode);
      ambientGainNode.connect(ambientAudioCtx.destination);
    }
    if (ambientAudioCtx.state === 'suspended') {
      ambientAudioCtx.resume();
    }
    ambientGainNode.gain.cancelScheduledValues(ambientAudioCtx.currentTime);
    ambientGainNode.gain.linearRampToValueAtTime(0.022, ambientAudioCtx.currentTime + 1.8);
  } catch (_) {
    // Ignore WebAudio restrictions if any
  }
}

function stopMemorialAmbientPad() {
  try {
    if (ambientAudioCtx && ambientGainNode) {
      ambientGainNode.gain.cancelScheduledValues(ambientAudioCtx.currentTime);
      ambientGainNode.gain.linearRampToValueAtTime(0.0001, ambientAudioCtx.currentTime + 1.2);
    }
  } catch (_) {}
}

function stopSpotNarration() {
  if (narrationAudio) {
    narrationAudio.pause();
    narrationAudio.currentTime = 0;
  }
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
  stopMemorialAmbientPad();
  const listenBtn = document.getElementById('modalListenBtn');
  if (listenBtn) {
    listenBtn.textContent = '🎧 Listen to Room Voiceover';
  }
}

function playSpotNarration(hotspotId) {
  stopSpotNarration();
  if (!voiceNarrationEnabled) return;

  const langPrefix = ['en', 'fa', 'fi'].includes(currentLang) ? currentLang : 'en';
  const primarySrc = `media/narration/${langPrefix}_${hotspotId}.mp3`;
  const fallbackSrc = `media/narration/en_${hotspotId}.mp3`;

  if (!narrationAudio) {
    narrationAudio = new Audio();
  }

  const speedSelect = document.getElementById('narrationSpeedSelect');
  if (speedSelect) {
    narrationRate = parseFloat(speedSelect.value) || 0.94;
  }

  narrationAudio.src = primarySrc;
  narrationAudio.playbackRate = narrationRate;
  if ('preservesPitch' in narrationAudio) narrationAudio.preservesPitch = true;
  if ('webkitPreservesPitch' in narrationAudio) narrationAudio.webkitPreservesPitch = true;

  startMemorialAmbientPad();

  const listenBtn = document.getElementById('modalListenBtn');
  if (listenBtn) {
    listenBtn.textContent = '⏸ Pause Room Voiceover';
  }

  narrationAudio.onended = () => {
    stopMemorialAmbientPad();
    if (listenBtn) {
      listenBtn.textContent = '🎧 Listen to Room Voiceover';
    }
  };

  narrationAudio.onerror = () => {
    if (narrationAudio.src.indexOf(fallbackSrc) === -1) {
      narrationAudio.src = fallbackSrc;
      narrationAudio.playbackRate = narrationRate;
      narrationAudio.play().catch(() => {});
    }
  };

  narrationAudio.play().catch(() => {
    stopMemorialAmbientPad();
  });
}

// --- GUIDED 8-STOP INTERIOR & COURTYARD TOUR ---
function startGuidedTour() {
  isGuidedTour = true;
  currentTourIndex = 0;
  document.getElementById('btnGuidedTour').classList.add('active');
  document.getElementById('storyBanner').classList.add('visible');
  renderGuidedTourStep(0, true);
}

function stopGuidedTour() {
  isGuidedTour = false;
  document.getElementById('btnGuidedTour').classList.remove('active');
  document.getElementById('storyBanner').classList.remove('visible');
  stopSpotNarration();
}

function renderGuidedTourStep(idx, speakNow) {
  const stop = GUIDED_TOUR_STOPS[idx];
  if (!stop) return;
  const t = I18N_DATA[currentLang] || I18N_DATA.en;
  const hData = t.hotspots[stop.hotspotId];

  setTemporalCondition(stop.temporal);
  document.getElementById('timelineSlider').value = stop.temporal;
  if (stop.temporal < 0.5 && typeof stop.cutawayMode === 'number') {
    setCutawayMode(stop.cutawayMode);
  }

  triggerCameraAnimation(
    new THREE.Vector3(stop.camPos[0], stop.camPos[1], stop.camPos[2]),
    new THREE.Vector3(stop.lookAt[0], stop.lookAt[1], stop.lookAt[2])
  );

  document.getElementById('storyStepBadge').textContent = stop.badge[currentLang] || stop.badge.en;
  document.getElementById('storyTitle').textContent = hData.title;
  document.getElementById('storyText').textContent = `${hData.desc}`;
  const thumb = document.getElementById('storyThumbImg');
  if (thumb && hData.spotImg) {
    thumb.src = hData.spotImg;
    thumb.onclick = () => showHotspotModal(stop.hotspotId);
  }

  if (speakNow && voiceNarrationEnabled) {
    playSpotNarration(stop.hotspotId);
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
    triggerCameraAnimation(new THREE.Vector3(0, 1.85, 4.5), new THREE.Vector3(0, 1.85, -8.5));
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
function openVowModal() {
  document.getElementById('vowModal').classList.add('visible');
}

function closeVowModal() {
  document.getElementById('vowModal').classList.remove('visible');
}

async function submitVowForm(e) {
  e.preventDefault();
  const name = document.getElementById('vowName').value.trim();
  const email = document.getElementById('vowEmail').value.trim();
  const city = document.getElementById('vowCity').value.trim();
  const role = document.getElementById('vowContribution').value;
  const personalMsg = document.getElementById('vowMessage').value.trim();
  const statusEl = document.getElementById('vowStatusMsg');
  const submitBtn = document.getElementById('vowSubmitBtn');

  statusEl.style.display = 'block';
  statusEl.style.background = 'rgba(255,255,255,0.06)';
  statusEl.style.color = '#f0ebe3';
  statusEl.textContent = 'Recording your Accountability Vow...';
  submitBtn.disabled = true;

  const fullMessage = `[MINAB ACCOUNTABILITY VOW — NOV 20 HYBRID EVENT]\nCity/Country: ${city}\nPledge: Affirmed solemn vow to participate in holding every person in the chain of command accountable.\nNote: ${personalMsg || 'Signed from 3D Spatial School Reconstruction.'}`;

  let apiUrl = '/api/telegram/submit-contact/';
  if (window.location.protocol === 'file:' || window.location.port === '8090') {
    apiUrl = 'http://localhost:8000/api/telegram/submit-contact/';
  }

  try {
    const resp = await fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, role, message: fullMessage })
    });
    if (!resp.ok) throw new Error('API fallback');
  } catch (_) {
    const localVows = JSON.parse(localStorage.getItem('pfp_local_vows') || '[]');
    localVows.push({ name, email, city, role, personalMsg, ts: new Date().toISOString() });
    localStorage.setItem('pfp_local_vows', JSON.stringify(localVows));
  }

  vowSignatoryCount += 1;
  localStorage.setItem('pfp_vow_count', String(vowSignatoryCount));
  updateVowBadge();

  statusEl.style.background = 'rgba(16, 185, 129, 0.18)';
  statusEl.style.color = '#6ee7b7';
  statusEl.textContent = `✓ Thank you, ${name}. Your Accountability Vow (#${vowSignatoryCount.toLocaleString()}) has been recorded.`;
  document.getElementById('vowForm').reset();
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
      openVowModal();
    } else {
      currentTourIndex += 1;
      renderGuidedTourStep(currentTourIndex, true);
    }
  });

  document.getElementById('btnStoryAudio').addEventListener('click', (e) => {
    voiceNarrationEnabled = !voiceNarrationEnabled;
    e.target.textContent = voiceNarrationEnabled ? '🔊 Female Voice On' : '🔇 Voice Muted';
    if (!voiceNarrationEnabled) {
      stopSpotNarration();
    } else {
      renderGuidedTourStep(currentTourIndex, true);
    }
  });

  const speedSelect = document.getElementById('narrationSpeedSelect');
  if (speedSelect) {
    speedSelect.addEventListener('change', (e) => {
      narrationRate = parseFloat(e.target.value) || 0.94;
      if (narrationAudio) {
        narrationAudio.playbackRate = narrationRate;
      }
    });
  }

  const modalListenBtn = document.getElementById('modalListenBtn');
  if (modalListenBtn) {
    modalListenBtn.addEventListener('click', () => {
      if (!activeHotspotId) return;
      if (narrationAudio && !narrationAudio.paused) {
        stopSpotNarration();
      } else {
        voiceNarrationEnabled = true;
        const audioToggle = document.getElementById('btnStoryAudio');
        if (audioToggle) audioToggle.textContent = '🔊 Female Voice On';
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
        triggerCameraAnimation(new THREE.Vector3(-11.5, 2.3, -2.2), new THREE.Vector3(-18.5, 1.8, -4.5));
      } else if (galleryViewStep === 2) {
        // View 2: First Floor Girls' Assembly Hall (47 Schoolgirls)
        setCutawayMode(1);
        triggerCameraAnimation(new THREE.Vector3(-10.5, 5.9, -2.5), new THREE.Vector3(-18.5, 5.3, -7.0));
      } else if (galleryViewStep === 3) {
        // View 3: First Floor North-East Classroom (28 Rubble Drawings & Homework Archive)
        setCutawayMode(1);
        triggerCameraAnimation(new THREE.Vector3(11.2, 5.6, -7.4), new THREE.Vector3(18.5, 5.2, -10.2));
      } else {
        // View 4: Central Rainbow Staircase Hall (26 Martyred Female Educators)
        setCutawayMode(2);
        triggerCameraAnimation(new THREE.Vector3(1.5, 2.35, -1.2), new THREE.Vector3(-6.2, 1.9, -5.5));
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

  document.getElementById('openVowBtn').addEventListener('click', openVowModal);
  document.getElementById('vowCloseBtn').addEventListener('click', closeVowModal);
  document.getElementById('vowModal').addEventListener('click', (e) => {
    if (e.target.id === 'vowModal') closeVowModal();
  });
  document.getElementById('vowForm').addEventListener('submit', submitVowForm);

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

  if (isAnimatingCamera && animationTarget.pos) {
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
