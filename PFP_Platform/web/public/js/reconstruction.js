/**
 * Minab School 3D Spatial Reconstruction & Forensic WebXR Engine
 * Developed for People for Peace & Justice ry (PFPJ ry) — Helsinki, Finland
 * Standalone, self-hosted Three.js spatial platform documenting the Shajareh Tayyebeh School airstrike.
 */

// --- TRILINGUAL LOCALIZATION DICTIONARY ---
const I18N_DATA = {
  en: {
    pageTitle: "3D Spatial Reconstruction — Minab Primary School",
    navHome: "Home",
    navEvidence: "← Back to Evidence",
    navMemorial: "Memorial",
    navAbout: "About Us",
    badgeLabel: "Spatial Forensics & OSINT",
    heroTitle: "Shajareh Tayyebeh Primary School",
    heroCoords: "27°08'43\"N 57°05'02\"E · Minab, Hormozgan · Strike: Feb 28, 2026",
    sliderLabel: "Temporal Condition:",
    preStrikeBtn: "Pre-Strike (Intact)",
    postStrikeBtn: "Post-Strike (Damage)",
    presetsLabel: "Camera Presets:",
    presetOrbit: "Drone Orbit",
    presetCrater: "Impact Crater",
    presetEntrances: "Dual Entrances",
    presetWall: "2016 Boundary Wall",
    presetTopDown: "Satellite Ortho",
    enterVrBtn: "🥽 Enter WebXR VR",
    hotspotsCount: "5 Verified Evidence Coordinates Active",
    closeModal: "Close",
    evidenceBadge: "Forensic Evidence Dossier",
    viewInEvidencePortal: "View in Evidence Registry →",
    controlsHelp: "Drag to rotate · Scroll / Pinch to zoom · Right-click / Two fingers to pan · Click pulsing markers for evidence",
    hotspots: {
      crater: {
        title: "Primary 5-Meter Impact Crater",
        category: "Blast Dynamics & Munitions",
        desc: "Forensic 3D spatial reconstruction identifies a 5-meter wide impact crater located in the center of the school's central assembly hall. The kinetic penetration collapsed the reinforced concrete roof and the intermediate floor slab, directly impacting children assembled in the central atrium.",
        finding: "Consistent with heavy penetrator warhead (WDU-36/B / unitary blast-fragmentation) detonating at interior ceiling level.",
        evidenceRef: "EVD-CRATER-001 / Forensic Architecture Investigation 121",
        image: "images/og-evidence.png"
      },
      entrance_separation: {
        title: "Dual Gendered School Entrances",
        category: "Civilian Facility Architecture",
        desc: "The two-story complex had two distinct, independent portals: the ground floor housed the boys' primary school and nursery, while the upper floor housed the girls' elementary school. Separate staircases and entryways were painted in bright blue and pink accents.",
        finding: "Disproves operational co-location claims; establishes dedicated, continuous educational use since 2015.",
        evidenceRef: "EVD-ARCH-002 / School Registry Records",
        image: "images/og-memorial.png"
      },
      boundary_wall: {
        title: "2016 Concrete Separation Wall",
        category: "Geospatial Satellite Verification",
        desc: "High-resolution satellite chronological analysis (Planet Labs / Maxar 2013–2026) verifies that in early 2016, a continuous reinforced concrete boundary wall was constructed, physically partitioning the school campus from any adjacent historical zones.",
        finding: "Proves strict physical partition and zero military utility at time of target designation under Geneva Protocol I, Art. 57.",
        evidenceRef: "EVD-SAT-001 / Planet Labs Archive",
        image: "images/og-evidence.png"
      },
      munitions_debris: {
        title: "BGM-109 Tomahawk Missile Actuator Debris",
        category: "Physical Munitions Forensics",
        desc: "Debris recovered from the schoolyard perimeter includes control fin actuator housings and booster separation fragments bearing NATO CAGE codes and serial markings consistent with US Navy BGM-109 Tomahawk Block IV/V cruise missiles.",
        finding: "Corroborated by independent OSINT researchers and on-site recovery teams; confirms maritime standoff launch vector.",
        evidenceRef: "EVD-MUN-002 / Weapons Debris Dossier",
        image: "images/og-evidence.png"
      },
      classrooms: {
        title: "Classroom Wings & Student Assembly Hall",
        category: "Casualty Context & Spatial Layout",
        desc: "Surrounding the central assembly hall were 12 active classrooms decorated with student artwork and pedagogical displays. At 11:22 AM local time, classes were in full session with over 150 pupils and educators present inside the main perimeter.",
        finding: "120 children and 26 educators lost their lives within these specific ground and first-floor corridors.",
        evidenceRef: "EVD-CASUALTY-001 / Master Casualty Registry",
        image: "images/og-memorial.png"
      }
    }
  },
  fi: {
    pageTitle: "3D-tilan rekonstruktio — Minabin peruskoulu",
    navHome: "Etusivu",
    navEvidence: "← Takaisin todisteisiin",
    navMemorial: "Muistosivu",
    navAbout: "Tietoa meistä",
    badgeLabel: "Paikkatietotutkinta & OSINT",
    heroTitle: "Shajareh Tayyebehin peruskoulu",
    heroCoords: "27°08'43\"N 57°05'02\"E · Minab, Hormozgan · Isku: 28.2.2026",
    sliderLabel: "Aikajana & tilanne:",
    preStrikeBtn: "Ennen iskua (Eheä)",
    postStrikeBtn: "Iskun jälkeen (Tuhot)",
    presetsLabel: "Kuvakulmat:",
    presetOrbit: "Drone-kierto",
    presetCrater: "Iskukraatteri",
    presetEntrances: "Sisäänkäynnit",
    presetWall: "Vuoden 2016 muuri",
    presetTopDown: "Satelliittinäkymä",
    enterVrBtn: "🥽 Avaa WebXR VR",
    hotspotsCount: "5 todennettua todistekoordinaattia aktiivisena",
    closeModal: "Sulje",
    evidenceBadge: "Oikeuslääketieteellinen todisteaineisto",
    viewInEvidencePortal: "Avaa todisterekisterissä →",
    controlsHelp: "Pyöritä vetämällä · Zoomaa rullalla / nipistämällä · Siirrä hiiren kakkospainikkeella · Klikkaa merkkejä",
    hotspots: {
      crater: {
        title: "Pääiskun 5-metrinen kraatteri",
        category: "Räjähdysdynamiikka & Aseistus",
        desc: "3D-mallinnus osoittaa 5 metrin läpimittaisen iskukraatterin keskellä koulun pääjuhlasalia. Isku murskasi teräsbetonisen kattorakenteen ja välikaton suoraan saliin kokoontuneiden lasten päälle.",
        finding: "Vastaa raskasta läpäisevää taistelukärkeä (WDU-36/B / Tomahawk), joka laukesi sisätilassa.",
        evidenceRef: "EVD-CRATER-001 / Forensic Architecture -tutkinta 121",
        image: "images/og-evidence.png"
      },
      entrance_separation: {
        title: "Koulun erilliset sisäänkäynnit",
        category: "Siviilirakennuksen arkkitehtuuri",
        desc: "Kaksikerroksisessa rakennuksessa oli kaksi erillistä sisäänkäyntiä: alakerrassa sijaitsi poikien peruskoulu ja esikoulu, yläkerrassa tyttökoulu. Porraskäytävät ja seinät oli maalattu vaaleansinisellä ja vaaleanpunaisella.",
        finding: "Kumoaa väitteet sotilaskäytöstä; todistaa jatkuvan ja kiistattoman opetuskäytön vuodesta 2015 alkaen.",
        evidenceRef: "EVD-ARCH-002 / Kouluasiakirjat",
        image: "images/og-memorial.png"
      },
      boundary_wall: {
        title: "Vuoden 2016 betoninen suojamuuri",
        category: "Satelliittikuvien kronologia",
        desc: "Satelliittikuvien (Planet Labs / Maxar 2013–2026) tarkastelu vahvistaa, että alkuvuodesta 2016 rakennettiin yhtenäinen betonimuuri erottamaan koulu selkeästi ympäröivistä alueista.",
        finding: "Osoittaa Geneven sopimuksen 1. lisäpöytäkirjan (57 art.) mukaisen varotoimenpiteiden laiminlyönnin iskun suorittajalta.",
        evidenceRef: "EVD-SAT-001 / Planet Labs -arkisto",
        image: "images/og-evidence.png"
      },
      munitions_debris: {
        title: "BGM-109 Tomahawk -ohjuksen sirpaleet",
        category: "Fyysinen aselajitutkinta",
        desc: "Koulun pihalta ja raunioista kerätyt ohjussirpaleet sisältävät ohjaussiivekkeiden hydraulisia osia ja NATO CAGE -tunnisteisia runko-osia.",
        finding: "Täsmää Yhdysvaltain laivaston BGM-109 Tomahawk Block IV/V -risteilyohjuksen osiin.",
        evidenceRef: "EVD-MUN-002 / Asetutkintaraportti",
        image: "images/og-evidence.png"
      },
      classrooms: {
        title: "Luokkahuoneet ja kokoontumissali",
        category: "Uhritiedot & tilallinen sijoittuminen",
        desc: "Keskussalia ympäröi 12 aktiivista luokkahuonetta. Kello 11.22 oppitunnit olivat käynnissä ja koulussa oli yli 150 oppilasta ja opettajaa.",
        finding: "120 lasta ja 26 opettajaa sai surmansa näissä käytävissä ja luokissa.",
        evidenceRef: "EVD-CASUALTY-001 / Pääuhrirekisteri",
        image: "images/og-memorial.png"
      }
    }
  },
  fa: {
    pageTitle: "بازسازی سه‌بعدی فضایی فاجعه دبستان میناب",
    navHome: "صفحه اصلی",
    navEvidence: "← بازگشت به پرونده اسناد",
    navMemorial: "یادبود شهیدان",
    navAbout: "درباره ما",
    badgeLabel: "کالبدشکافی فضایی و داده‌های متن‌باز OSINT",
    heroTitle: "دبستان دخترانه و پسرانه شجره طیبه میناب",
    heroCoords: "۲۷°۰۸'۴۳\" شمالی ۵۷°۰۵'۰۲\" شرقی · هرمزگان، میناب · زمان اصابت: ۹ اسفند ۱۴۰۴",
    sliderLabel: "خط زمانی و وضعیت سازه:",
    preStrikeBtn: "پیش از حمله (مدرسه دایر)",
    postStrikeBtn: "پس از حمله (آثار اصابت)",
    presetsLabel: "زوایای دوربین:",
    presetOrbit: "چرخش پهپادی",
    presetCrater: "محل گودال انفجار",
    presetEntrances: "ورودی‌های مجزا",
    presetWall: "دیوار حائل بتنی ۲۰۱۶",
    presetTopDown: "تصویر قائم ماهواره‌ای",
    enterVrBtn: "🥽 ورود به حالت واقعیت مجازی VR",
    hotspotsCount: "۵ مختصات اثبات‌شده حقوقی و فنی فعال است",
    closeModal: "بستن",
    evidenceBadge: "مستندات پرونده کیفری بین‌المللی",
    viewInEvidencePortal: "مشاهده در پایگاه اسناد حقوقی →",
    controlsHelp: "چرخش با درگ کردن · بزرگ‌نمایی با اسکرول / پینچ · حرکت با راست‌کلیک · کلیک روی نشانگرها برای دیدن اسناد",
    hotspots: {
      crater: {
        title: "گودال ۵ متری اصابت موشک اول",
        category: "دینامیک انفجار و کلاهک موشک",
        desc: "بازسازی سه‌بعدی فضایی نشان می‌دهد گودالی به قطر ۵ متر درست در سالن اجتماعات مرکزی ایجاد شده است. موج انفجار سقف بتن‌آرمه و کف طبقه اول را به‌طور کامل در هم کوبیده است.",
        finding: "منطبق بر اصابت کلاهک سنگین نفوذگر موشک کروز تاماهاک با فیوز تأخیری انفجار در فضای بسته.",
        evidenceRef: "EVD-CRATER-001 / گزارش ۱۲۱ فورنزیک آرکیتکچر",
        image: "images/og-evidence.png"
      },
      entrance_separation: {
        title: "ورودی‌های مجزای پیش‌دبستانی و دبستان",
        category: "معماری و کاربری قطعی آموزشی",
        desc: "ساختمان دو طبقه دارای ورودی‌های کاملاً مجزا بود: طبقه همکف به پیش‌دبستانی و دبستان پسرانه اختصاص داشت و طبقه اول دبستان دخترانه بود. راه‌پله‌ها با رنگ‌های شاد آبی و صورتی نقاشی شده بودند.",
        finding: "رد قاطع ادعای استفاده نظامی مشترک؛ اثبات کاربری مستمر، علنی و ۱۰ ساله آموزشی از سال ۲۰۱۵.",
        evidenceRef: "EVD-ARCH-002 / اسناد ثبتی نوسازی مدارس",
        image: "images/og-memorial.png"
      },
      boundary_wall: {
        title: "دیوار حائل بتنی مصوب سال ۲۰۱۶",
        category: "تحلیل تغییرات زمانی ماهواره‌ای",
        desc: "بررسی تصاویر ماهواره‌ای پلانِت و مکسار (۲۰۱۳ تا ۲۰۲۶) اثبات می‌کند در اوایل سال ۲۰۱۶ دیوار بتنی بلندی کشیده شده و حریم آموزشی دبستان را از محیط‌های مجاور کاملاً تفکیک کرده است.",
        finding: "اثبات نقض فاحش اصل احتیاط در حمله (ماده ۵۷ پروتکل اول کنوانسیون‌های ژنو).",
        evidenceRef: "EVD-SAT-001 / آرشیو ماهواره‌ای Planet Labs",
        image: "images/og-evidence.png"
      },
      munitions_debris: {
        title: "ترکش‌ها و بالک هدایت موشک تاماهاک BGM-109",
        category: "شواهد جرم‌شناسی مهمات",
        desc: "ترکش‌های کشف شده در حیاط و ویرانه‌های مدرسه شامل قطعات عملگر بالک‌های هدایت هیدرولیک با کدهای نظامی ناتو (CAGE Code) منطبق بر موشک‌های کروز تاماهاک بلوک IV/V است.",
        finding: "تطبیق داده شده توسط محققان مستقل تسلیحات و اثبات پرتاب از ناوگان دریایی در دریای عمان.",
        evidenceRef: "EVD-MUN-002 / پرونده شواهد تسلیحاتی",
        image: "images/og-evidence.png"
      },
      classrooms: {
        title: "کلاس‌های درس و سالن مرکزی اجتماعات",
        category: "تلفات غیرنظامی و چینش فضایی",
        desc: "۱۲ کلاس درس فعال سالن مرکزی را در بر گرفته بودند. در ساعت ۱۱:۲۲ صبح و در اوج ساعت درسی، بیش از ۱۵۰ دانش‌آموز خردسال و آموزگار در این فضا حضور داشتند.",
        finding: "شهادت ۱۲۰ کودک ۶ تا ۱۲ ساله و ۲۶ معلم و کادر آموزشی در این راهروها به ثبت رسیده است.",
        evidenceRef: "EVD-CASUALTY-001 / ثبت رسمی اسامی شهدا",
        image: "images/og-memorial.png"
      }
    }
  }
};

// --- APPLICATION STATE ---
let currentLang = 'en';
let scene, camera, renderer, controls;
let preStrikeModelGroup, postStrikeModelGroup, terrainGroup, markersGroup;
let damageSliderValue = 0.0; // 0.0 = Pre-Strike, 1.0 = Post-Strike
let activeHotspotId = null;
let isAnimatingCamera = false;
let animationTarget = { pos: null, lookAt: null };
let clock;

// --- INITIALIZATION ---
function startReconstructionApp() {
  if (typeof THREE === 'undefined') {
    console.error('Three.js failed to load. Retrying in 100ms...');
    setTimeout(startReconstructionApp, 100);
    return;
  }
  clock = new THREE.Clock();
  initI18n();
  initThreeEngine();
  buildEnvironmentAndTerrain();
  buildProceduralSchoolModels();
  initHotspots();
  initUIControls();
  animate();
}

if (document.readyState === 'loading') {
  window.addEventListener('DOMContentLoaded', startReconstructionApp);
} else {
  startReconstructionApp();
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
}

function applyTranslations() {
  const t = I18N_DATA[currentLang] || I18N_DATA.en;
  document.documentElement.lang = currentLang;
  document.documentElement.dir = (currentLang === 'fa') ? 'rtl' : 'ltr';

  // Text replacements by data-i18n attribute
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (t[key]) el.textContent = t[key];
  });

  // Active button styling
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-lang') === currentLang);
  });
}

// --- THREE.JS ENGINE CORE ---
function initThreeEngine() {
  const container = document.getElementById('canvasContainer');
  const width = container.clientWidth || window.innerWidth;
  const height = container.clientHeight || window.innerHeight;

  // 1. Scene
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0e17);
  scene.fog = new THREE.FogExp2(0x0a0e17, 0.007);

  // 2. Camera
  camera = new THREE.PerspectiveCamera(45, width / height, 0.5, 1000);
  camera.position.set(45, 30, 48); // Natural drone angle

  // 3. Renderer
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: "high-performance" });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.15;
  if (renderer.xr) {
    renderer.xr.enabled = true;
  }
  container.appendChild(renderer.domElement);

  // 4. Controls
  controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.maxPolarAngle = Math.PI / 2 - 0.04; // Don't clip below ground
  controls.minDistance = 8;
  controls.maxDistance = 140;
  controls.target.set(0, 3, 0);

  // 5. Lighting (matching Minab solar angle at 11:22 AM)
  const hemiLight = new THREE.HemisphereLight(0xfff8ee, 0x1a2130, 0.7);
  hemiLight.position.set(0, 50, 0);
  scene.add(hemiLight);

  const sunLight = new THREE.DirectionalLight(0xfff3db, 1.4);
  sunLight.position.set(30, 60, 20);
  sunLight.castShadow = true;
  sunLight.shadow.mapSize.width = 2048;
  sunLight.shadow.mapSize.height = 2048;
  sunLight.shadow.camera.near = 10;
  sunLight.shadow.camera.far = 150;
  sunLight.shadow.camera.left = -40;
  sunLight.shadow.camera.right = 40;
  sunLight.shadow.camera.top = 40;
  sunLight.shadow.camera.bottom = -40;
  sunLight.shadow.bias = -0.0005;
  scene.add(sunLight);

  // Groups
  terrainGroup = new THREE.Group();
  preStrikeModelGroup = new THREE.Group();
  postStrikeModelGroup = new THREE.Group();
  markersGroup = new THREE.Group();

  scene.add(terrainGroup);
  scene.add(preStrikeModelGroup);
  scene.add(postStrikeModelGroup);
  scene.add(markersGroup);

  // Post-strike hidden by default
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

// --- TERRAIN & ENVIRONMENT GENERATION ---
function buildEnvironmentAndTerrain() {
  // Ground plane (Hormozgan coastal clay / desert soil color)
  const groundGeo = new THREE.PlaneGeometry(160, 140, 32, 32);
  const groundMat = new THREE.MeshStandardMaterial({
    color: 0x22252a,
    roughness: 0.9,
    metalness: 0.1
  });
  const ground = new THREE.Mesh(groundGeo, groundMat);
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  terrainGroup.add(ground);

  // School Courtyard Asphalt / Paved Playground
  const yardGeo = new THREE.PlaneGeometry(62, 44);
  const yardMat = new THREE.MeshStandardMaterial({
    color: 0x2d323c,
    roughness: 0.8
  });
  const yard = new THREE.Mesh(yardGeo, yardMat);
  yard.rotation.x = -Math.PI / 2;
  yard.position.set(0, 0.02, 3);
  yard.receiveShadow = true;
  terrainGroup.add(yard);

  // 2016 Concrete Boundary Wall
  const wallMat = new THREE.MeshStandardMaterial({ color: 0x7c818b, roughness: 0.9 });
  const wallThickness = 0.5;
  const wallHeight = 2.8;

  // North wall
  const nWall = new THREE.Mesh(new THREE.BoxGeometry(64, wallHeight, wallThickness), wallMat);
  nWall.position.set(0, wallHeight / 2, -19);
  nWall.castShadow = true; nWall.receiveShadow = true;
  terrainGroup.add(nWall);

  // South wall
  const sWall = new THREE.Mesh(new THREE.BoxGeometry(64, wallHeight, wallThickness), wallMat);
  sWall.position.set(0, wallHeight / 2, 25);
  sWall.castShadow = true; sWall.receiveShadow = true;
  terrainGroup.add(sWall);

  // East wall (The key 2016 partition wall)
  const eWall = new THREE.Mesh(new THREE.BoxGeometry(wallThickness, wallHeight, 44), wallMat);
  eWall.position.set(32, wallHeight / 2, 3);
  eWall.castShadow = true; eWall.receiveShadow = true;
  terrainGroup.add(eWall);

  // West wall (with gate gap)
  const wWall1 = new THREE.Mesh(new THREE.BoxGeometry(wallThickness, wallHeight, 18), wallMat);
  wWall1.position.set(-32, wallHeight / 2, -10);
  wWall1.castShadow = true; wWall1.receiveShadow = true;
  terrainGroup.add(wWall1);

  const wWall2 = new THREE.Mesh(new THREE.BoxGeometry(wallThickness, wallHeight, 18), wallMat);
  wWall2.position.set(-32, wallHeight / 2, 16);
  wWall2.castShadow = true; wWall2.receiveShadow = true;
  terrainGroup.add(wWall2);

  // School Flagpole in Yard
  const pole = new THREE.Mesh(
    new THREE.CylinderGeometry(0.08, 0.1, 9, 12),
    new THREE.MeshStandardMaterial({ color: 0xd4d8e0, metalness: 0.8, roughness: 0.3 })
  );
  pole.position.set(-10, 4.5, 12);
  pole.castShadow = true;
  terrainGroup.add(pole);

  // Playground lines / Sports Court Markings
  const lineMat = new THREE.MeshBasicMaterial({ color: 0x64748b });
  const courtLine = new THREE.Mesh(new THREE.RingGeometry(3.5, 3.7, 32), lineMat);
  courtLine.rotation.x = -Math.PI / 2;
  courtLine.position.set(8, 0.03, 10);
  terrainGroup.add(courtLine);
}

// --- PROCEDURAL 3D SCHOOL ARCHITECTURE (PRE & POST STRIKE) ---
function buildProceduralSchoolModels() {
  const schoolLength = 44;
  const schoolWidth = 18;
  const wallHeight = 3.6; // per floor
  const twoFloorHeight = wallHeight * 2;

  // Materials
  const stuccoMat = new THREE.MeshStandardMaterial({ color: 0xd6cbb8, roughness: 0.85 }); // Warm Iranian plaster
  const baseConcrete = new THREE.MeshStandardMaterial({ color: 0x8a8479, roughness: 0.9 });
  const roofMat = new THREE.MeshStandardMaterial({ color: 0x5a6068, roughness: 0.7 });
  const blueWallMat = new THREE.MeshStandardMaterial({ color: 0x4a90d9, roughness: 0.7 }); // Elementary blue
  const pinkWallMat = new THREE.MeshStandardMaterial({ color: 0xdf7a8c, roughness: 0.7 }); // Elementary pink
  const glassMat = new THREE.MeshStandardMaterial({ color: 0x1f3448, metalness: 0.9, roughness: 0.1, transparent: true, opacity: 0.7 });
  const ruinedConcrete = new THREE.MeshStandardMaterial({ color: 0x3d3935, roughness: 1.0 });
  const debrisMat = new THREE.MeshStandardMaterial({ color: 0x4d4740, roughness: 0.95 });

  // ==========================================
  // 1. PRE-STRIKE (INTACT) GEOMETRY
  // ==========================================
  
  // West Wing (Classrooms)
  const westWing = new THREE.Mesh(new THREE.BoxGeometry(16, twoFloorHeight, schoolWidth), stuccoMat);
  westWing.position.set(-14, twoFloorHeight / 2, -6);
  westWing.castShadow = true; westWing.receiveShadow = true;
  preStrikeModelGroup.add(westWing);

  // East Wing (Classrooms)
  const eastWing = new THREE.Mesh(new THREE.BoxGeometry(16, twoFloorHeight, schoolWidth), stuccoMat);
  eastWing.position.set(14, twoFloorHeight / 2, -6);
  eastWing.castShadow = true; eastWing.receiveShadow = true;
  preStrikeModelGroup.add(eastWing);

  // Central Assembly Hall (Connecting atrium with raised skylight)
  const hallLength = 12;
  const hall = new THREE.Mesh(new THREE.BoxGeometry(hallLength, twoFloorHeight + 1.2, schoolWidth - 2), stuccoMat);
  hall.position.set(0, (twoFloorHeight + 1.2) / 2, -6);
  hall.castShadow = true; hall.receiveShadow = true;
  preStrikeModelGroup.add(hall);

  // Skylight Glass Roof
  const skylight = new THREE.Mesh(new THREE.BoxGeometry(8, 0.4, 8), glassMat);
  skylight.position.set(0, twoFloorHeight + 1.4, -6);
  preStrikeModelGroup.add(skylight);

  // Floor partition decorative band (Blue & Pink stripe)
  const stripeBlue = new THREE.Mesh(new THREE.BoxGeometry(44.2, 0.3, schoolWidth + 0.2), blueWallMat);
  stripeBlue.position.set(0, wallHeight, -6);
  preStrikeModelGroup.add(stripeBlue);

  const stripePink = new THREE.Mesh(new THREE.BoxGeometry(44.2, 0.3, schoolWidth + 0.2), pinkWallMat);
  stripePink.position.set(0, wallHeight + 0.3, -6);
  preStrikeModelGroup.add(stripePink);

  // Windows grid (South facade facing courtyard)
  for (let wingX of [-18, -14, -10, 10, 14, 18]) {
    // Ground floor window
    const winG = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.8, 0.2), glassMat);
    winG.position.set(wingX, 2.0, 3.05);
    preStrikeModelGroup.add(winG);

    // 1st floor window
    const win1 = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.8, 0.2), glassMat);
    win1.position.set(wingX, 5.6, 3.05);
    preStrikeModelGroup.add(win1);
  }

  // Pre-school & Boys' Entrance Canopy (West side)
  const canopy1 = new THREE.Mesh(new THREE.BoxGeometry(4, 0.3, 3), baseConcrete);
  canopy1.position.set(-14, 3.6, 3.8);
  canopy1.castShadow = true;
  preStrikeModelGroup.add(canopy1);

  // Girls' School Portal Entrance (Central corridor)
  const portal = new THREE.Mesh(new THREE.BoxGeometry(4.5, 5.5, 0.6), baseConcrete);
  portal.position.set(0, 2.75, 3.2);
  portal.castShadow = true;
  preStrikeModelGroup.add(portal);

  // ==========================================
  // 2. POST-STRIKE (AIRSTRIKE DAMAGE) GEOMETRY
  // ==========================================

  // Remaining West Wing (partial collapse on inner boundary)
  const westWingDamaged = new THREE.Mesh(new THREE.BoxGeometry(14, twoFloorHeight, schoolWidth), ruinedConcrete);
  westWingDamaged.position.set(-15, twoFloorHeight / 2, -6);
  westWingDamaged.castShadow = true; westWingDamaged.receiveShadow = true;
  postStrikeModelGroup.add(westWingDamaged);

  // Remaining East Wing (partially fractured)
  const eastWingDamaged = new THREE.Mesh(new THREE.BoxGeometry(14, twoFloorHeight, schoolWidth), ruinedConcrete);
  eastWingDamaged.position.set(15, twoFloorHeight / 2, -6);
  eastWingDamaged.castShadow = true; eastWingDamaged.receiveShadow = true;
  postStrikeModelGroup.add(eastWingDamaged);

  // Center Assembly Hall: Completely Collapsed with 5m Crater Cavity
  const craterRim = new THREE.Mesh(
    new THREE.TorusGeometry(3.0, 0.8, 12, 24),
    ruinedConcrete
  );
  craterRim.rotation.x = -Math.PI / 2;
  craterRim.position.set(0, 0.3, -6);
  craterRim.receiveShadow = true;
  postStrikeModelGroup.add(craterRim);

  // Crater Depth Pit
  const craterHole = new THREE.Mesh(
    new THREE.CylinderGeometry(2.4, 0.4, 2.2, 16),
    new THREE.MeshBasicMaterial({ color: 0x0f0e0c })
  );
  craterHole.position.set(0, -0.9, -6);
  postStrikeModelGroup.add(craterHole);

  // Slabs of collapsed ceiling fallen into the hole at acute angles
  const slab1 = new THREE.Mesh(new THREE.BoxGeometry(5.0, 0.4, 4.0), ruinedConcrete);
  slab1.position.set(1.2, 1.2, -5.5);
  slab1.rotation.set(0.4, 0.2, -0.6);
  slab1.castShadow = true;
  postStrikeModelGroup.add(slab1);

  const slab2 = new THREE.Mesh(new THREE.BoxGeometry(4.5, 0.4, 3.5), ruinedConcrete);
  slab2.position.set(-1.4, 0.8, -6.8);
  slab2.rotation.set(-0.5, -0.3, 0.4);
  slab2.castShadow = true;
  postStrikeModelGroup.add(slab2);

  // Scattered Rubble Debris Field (Procedural chunks)
  for (let i = 0; i < 28; i++) {
    const rx = (Math.random() - 0.5) * 18;
    const rz = (Math.random() - 0.5) * 16 - 6;
    const size = 0.4 + Math.random() * 0.9;
    const chunk = new THREE.Mesh(new THREE.BoxGeometry(size, size * 0.7, size), debrisMat);
    chunk.position.set(rx, size / 2, rz);
    chunk.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, 0);
    chunk.castShadow = true; chunk.receiveShadow = true;
    postStrikeModelGroup.add(chunk);
  }

  // Tomahawk Booster Debris Marker Flag in yard
  const debrisMarker = new THREE.Mesh(
    new THREE.ConeGeometry(0.3, 1.2, 8),
    new THREE.MeshStandardMaterial({ color: 0xc4564a, roughness: 0.3, metalness: 0.8 })
  );
  debrisMarker.position.set(3.5, 0.6, 2.1);
  debrisMarker.castShadow = true;
  postStrikeModelGroup.add(debrisMarker);
}

// --- FORENSIC HOTSPOTS & 3D PINS ---
const HOTSPOT_CONFIGS = [
  { id: 'crater', pos: [0, 2.0, -6.0], presetCam: [8, 12, 4], target: [0, 1, -6] },
  { id: 'entrance_separation', pos: [-14, 2.5, 3.8], presetCam: [-22, 7, 14], target: [-14, 2, 3] },
  { id: 'boundary_wall', pos: [32, 2.0, 3.0], presetCam: [38, 14, 24], target: [32, 2, 3] },
  { id: 'munitions_debris', pos: [3.5, 1.2, 2.1], presetCam: [8, 6, 9], target: [3.5, 0.8, 2.1] },
  { id: 'classrooms', pos: [-14, 5.0, -6.0], presetCam: [-26, 12, 6], target: [-14, 4, -6] }
];

function initHotspots() {
  const container = document.getElementById('canvasContainer');

  HOTSPOT_CONFIGS.forEach(cfg => {
    // 1. Create Vector3 objects
    cfg.posVec = new THREE.Vector3(cfg.pos[0], cfg.pos[1], cfg.pos[2]);
    cfg.presetCamVec = new THREE.Vector3(cfg.presetCam[0], cfg.presetCam[1], cfg.presetCam[2]);
    cfg.targetVec = new THREE.Vector3(cfg.target[0], cfg.target[1], cfg.target[2]);

    // 2. Create 3D anchor mesh
    const markerMesh = new THREE.Mesh(
      new THREE.SphereGeometry(0.4, 16, 16),
      new THREE.MeshBasicMaterial({ color: 0xd4a853, transparent: true, opacity: 0.85 })
    );
    markerMesh.position.copy(cfg.posVec);
    markersGroup.add(markerMesh);
    cfg.mesh = markerMesh;

    // 2. Create 2D Overlay HTML Element
    const el = document.createElement('div');
    el.className = 'hotspot-pin';
    el.id = `hotspot-pin-${cfg.id}`;
    el.innerHTML = `
      <div class="pin-pulse"></div>
      <div class="pin-icon">✦</div>
      <div class="pin-tooltip" id="tooltip-${cfg.id}"></div>
    `;
    el.addEventListener('click', (e) => {
      e.stopPropagation();
      selectHotspot(cfg.id);
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

  HOTSPOT_CONFIGS.forEach(cfg => {
    tempV.copy(cfg.posVec);
    // Project 3D coordinate to normalized device coordinates
    tempV.project(camera);

    // Behind camera check
    if (tempV.z > 1.0) {
      cfg.domElement.style.display = 'none';
      return;
    }

    cfg.domElement.style.display = 'block';
    const x = (tempV.x * 0.5 + 0.5) * width;
    const y = (-tempV.y * 0.5 + 0.5) * height;
    cfg.domElement.style.transform = `translate(-50%, -50%) translate(${x}px, ${y}px)`;
  });
}

function selectHotspot(id) {
  activeHotspotId = id;
  const cfg = HOTSPOT_CONFIGS.find(c => c.id === id);
  if (!cfg) return;

  // Move camera smoothly
  triggerCameraAnimation(cfg.presetCamVec, cfg.targetVec);

  // Show detailed modal
  showHotspotModal(id);
}

function showHotspotModal(id) {
  const t = I18N_DATA[currentLang] || I18N_DATA.en;
  const data = t.hotspots[id];
  if (!data) return;

  const modal = document.getElementById('evidenceModal');
  const title = document.getElementById('modalTitle');
  const cat = document.getElementById('modalCategory');
  const desc = document.getElementById('modalDesc');
  const finding = document.getElementById('modalFinding');
  const ref = document.getElementById('modalRef');

  title.textContent = data.title;
  cat.textContent = data.category;
  desc.textContent = data.desc;
  finding.textContent = data.finding;
  ref.textContent = data.evidenceRef;

  modal.classList.add('visible');
}

function closeModal() {
  document.getElementById('evidenceModal').classList.remove('visible');
  activeHotspotId = null;
}

// --- UI CONTROLS & CAMERA PRESETS ---
function initUIControls() {
  // 1. Before/After Scrubber Slider
  const slider = document.getElementById('timelineSlider');
  slider.addEventListener('input', (e) => {
    setTemporalCondition(parseFloat(e.target.value));
  });

  // 2. Preset Buttons
  document.getElementById('presetOrbit').addEventListener('click', () => {
    triggerCameraAnimation(new THREE.Vector3(45, 30, 48), new THREE.Vector3(0, 3, 0));
  });

  document.getElementById('presetCrater').addEventListener('click', () => {
    setTemporalCondition(1.0);
    document.getElementById('timelineSlider').value = 1.0;
    selectHotspot('crater');
  });

  document.getElementById('presetEntrances').addEventListener('click', () => {
    setTemporalCondition(0.0);
    document.getElementById('timelineSlider').value = 0.0;
    selectHotspot('entrance_separation');
  });

  document.getElementById('presetWall').addEventListener('click', () => {
    selectHotspot('boundary_wall');
  });

  document.getElementById('presetTopDown').addEventListener('click', () => {
    triggerCameraAnimation(new THREE.Vector3(0, 75, 0.1), new THREE.Vector3(0, 0, 0));
  });

  // 3. WebXR Button
  const vrBtn = document.getElementById('enterVrBtn');
  if ('xr' in navigator) {
    navigator.xr.isSessionSupported('immersive-vr').then(supported => {
      if (supported) {
        vrBtn.style.display = 'inline-flex';
        vrBtn.addEventListener('click', startWebXRSession);
      }
    });
  }

  // 4. Modal Close
  document.getElementById('modalCloseBtn').addEventListener('click', closeModal);
  document.getElementById('evidenceModal').addEventListener('click', (e) => {
    if (e.target.id === 'evidenceModal') closeModal();
  });
}

function setTemporalCondition(val) {
  damageSliderValue = THREE.MathUtils.clamp(val, 0.0, 1.0);

  // Cross-fade visibility and material opacities
  if (damageSliderValue < 0.05) {
    preStrikeModelGroup.visible = true;
    postStrikeModelGroup.visible = false;
  } else if (damageSliderValue > 0.95) {
    preStrikeModelGroup.visible = false;
    postStrikeModelGroup.visible = true;
  } else {
    preStrikeModelGroup.visible = true;
    postStrikeModelGroup.visible = true;
    // Semi-transparent transition
    preStrikeModelGroup.traverse(child => {
      if (child.isMesh && child.material) {
        child.material.transparent = true;
        child.material.opacity = 1.0 - damageSliderValue;
      }
    });
    postStrikeModelGroup.traverse(child => {
      if (child.isMesh && child.material) {
        child.material.transparent = true;
        child.material.opacity = damageSliderValue;
      }
    });
  }

  // Active state styling on buttons
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
    console.warn("WebXR Session error:", err);
    alert("WebXR session could not be started: " + err.message);
  });
}

// --- ANIMATION LOOP ---
function animate() {
  requestAnimationFrame(animate);

  const delta = clock.getDelta();

  // Smooth camera tweening when jumping to presets
  if (isAnimatingCamera && animationTarget.pos) {
    camera.position.lerp(animationTarget.pos, 0.06);
    controls.target.lerp(animationTarget.lookAt, 0.06);

    if (camera.position.distanceTo(animationTarget.pos) < 0.2) {
      isAnimatingCamera = false;
    }
  }

  controls.update();
  updateHotspotPositions();
  renderer.render(scene, camera);
}
