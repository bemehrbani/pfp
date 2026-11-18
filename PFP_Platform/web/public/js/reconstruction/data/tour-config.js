/**
 * Declarative 8-station Guided Tour spline, hotspots, in-world 3D screens,
 * Cinema Witness Interludes, bookends, and room atmosphere profiles.
 */

export const MEDIA_ASSET_VERSION = '20261115a';

export const GUIDED_TOUR_STOPS = [
  {
    hotspotId: 'courtyard_lines',
    smoothSpline: true,
    temporal: 0.0,
    cutawayMode: 0,
    camPos: [9.0, 1.90, 8.25],
    lookAt: [25.0, 1.90, 8.25],
    waypoints: [
      // Level camera: eye height and gaze height are fixed at 1.9 m for the whole stop (no
      // pitch, no bobbing). The stop starts at (9, 8.25), 16 m back from the east steles; the
      // tour-start fly-in targets camPos/lookAt above, which equal this first waypoint, so
      // there is no jump. A slow straight walk in to (16, 8.25), a hold with all four east
      // steles in view, then one turn east -> south -> west.
      { t: 0.00, camPos: [9.0, 1.90, 8.25], lookAt: [25.0, 1.90, 8.25] },
      { t: 0.34, camPos: [16.0, 1.90, 8.25], lookAt: [25.0, 1.90, 8.25] },
      { t: 0.56, camPos: [16.0, 1.90, 8.25], lookAt: [25.0, 1.90, 8.25] },
      { t: 0.6125, camPos: [16.0, 1.90, 8.50], lookAt: [24.0, 1.90, 14.50] },
      { t: 0.665, camPos: [16.0, 1.90, 8.90], lookAt: [17.5, 1.90, 19.50] },
      { t: 0.7175, camPos: [15.8, 1.90, 9.30], lookAt: [9.0, 1.90, 15.00] },
      { t: 0.77, camPos: [15.5, 1.90, 9.00], lookAt: [8.0, 1.90, 8.90] },
      { t: 1.00, camPos: [12.5, 1.90, 9.00], lookAt: [8.0, 1.90, 8.90] }
    ],
    shortBadge: { en: "01 / 08", fi: "01 / 08", fa: "۰۱ / ۰۸" },
    badge: { en: "STOP 1 OF 8 · COURTYARD YELLOW ASSEMBLY LINES", fi: "PISTE 1/8 · KOULUPIHAN AAMURIVIT", fa: "ایستگاه ۱ از ۸ · خطوط زرد صف صبحگاهی در حیاط" }
  },
  {
    hotspotId: 'boys_flower_arch',
    temporal: 0.0,
    cutawayMode: 2,
    camPos: [3.62, 1.72, -4.35],
    lookAt: [3.62, 1.54, -8.04],
    waypoints: [
      { t: 0.00, camPos: [3.62, 1.66, -4.04], lookAt: [3.62, 1.54, -8.04] },
      { t: 0.16, camPos: [3.62, 1.62, -4.55], lookAt: [3.62, 1.54, -8.04] },
      { t: 0.28, camPos: [5.55, 1.66, -4.30], lookAt: [0.17, 1.80, -4.62] },
      { t: 0.42, camPos: [5.55, 1.66, -6.40], lookAt: [0.22, 1.60, -6.40] },
      { t: 0.68, camPos: [4.55, 1.64, -6.40], lookAt: [0.22, 1.60, -6.40] },
      { t: 1.00, camPos: [4.55, 1.64, -6.40], lookAt: [0.22, 1.60, -6.40] }
    ],
    shortBadge: { en: "02 / 08", fi: "02 / 08", fa: "۰۲ / ۰۸" },
    badge: { en: "STOP 2 OF 8 · GROUND FLOOR: BOYS' CEREMONY ROOM (ROSE ARCHES)", fi: "PISTE 2/8 · ALAKERTA: POIKIEN JUHLAHUONE", fa: "ایستگاه ۲ از ۸ · طبقه همکف: اتاق جشن پسران (طاق گل رز)" }
  },
  {
    hotspotId: 'boys_classroom',
    temporal: 0.0,
    cutawayMode: 2,
    camPos: [-13.35, 2.02, -0.95],
    lookAt: [-17.3, 1.52, 1.15],
    waypoints: [
      { t: 0.00, camPos: [-14.73, 1.66, 0.00], lookAt: [-18.73, 1.55, 0.00] },
      { t: 0.16, camPos: [-13.95, 1.70, -1.65], lookAt: [-18.00, 1.60, 0.85] },
      { t: 0.34, camPos: [-13.95, 1.70, -1.65], lookAt: [-18.00, 1.60, 0.85] },
      { t: 0.44, camPos: [-14.73, 1.66, 0.00], lookAt: [-18.73, 1.58, 0.00] },
      { t: 0.64, camPos: [-14.73, 1.66, 0.00], lookAt: [-18.73, 1.58, 0.00] },
      { t: 0.75, camPos: [-14.70, 1.60, -0.35], lookAt: [-15.40, 1.45, -2.50] },
      { t: 0.84, camPos: [-14.45, 1.60, -1.75], lookAt: [-14.45, 1.48, 2.15] },
      { t: 1.00, camPos: [-14.45, 1.60, -1.75], lookAt: [-14.45, 1.48, 2.15] }
    ],
    shortBadge: { en: "03 / 08", fi: "03 / 08", fa: "۰۳ / ۰۸" },
    badge: { en: "STOP 3 OF 8 · GROUND FLOOR: BOYS' CLASSROOM (CLAPPING & SINGING)", fi: "PISTE 3/8 · ALAKERTA: POIKIEN LUOKKAHUONE", fa: "ایستگاه ۳ از ۸ · طبقه همکف: کلاس درس پسران" }
  },
  {
    hotspotId: 'rainbow_staircase',
    temporal: 0.0,
    cutawayMode: 2,
    camPos: [-1.65, 2.05, -2.35],
    lookAt: [-1.55, 1.72, -9.80],
    waypoints: [
      { t: 0.00, camPos: [-3.30, 1.66, -4.05], lookAt: [-4.45, 1.58, -7.35] },
      { t: 0.14, camPos: [-3.30, 1.66, -4.05], lookAt: [-4.45, 1.58, -7.35] },
      { t: 0.22, camPos: [-1.55, 1.92, -6.20], lookAt: [-1.50, 1.35, -10.00] },
      { t: 0.38, camPos: [-1.55, 1.92, -6.20], lookAt: [-1.50, 1.35, -10.00] },
      { t: 0.45, camPos: [-2.60, 1.48, -5.40], lookAt: [-2.78, 0.96, -8.02] },
      { t: 0.53, camPos: [-2.60, 1.48, -5.40], lookAt: [-2.78, 0.96, -8.02] },
      { t: 0.60, camPos: [-5.03, 1.64, -6.65], lookAt: [-5.03, 1.58, -3.58] },
      { t: 1.00, camPos: [-5.03, 1.64, -6.65], lookAt: [-5.03, 1.58, -3.58] }
    ],
    shortBadge: { en: "04 / 08", fi: "04 / 08", fa: "۰۴ / ۰۸" },
    badge: { en: "STOP 4 OF 8 · THE RAINBOW STAIRCASE & PURPLE DOORS", fi: "PISTE 4/8 · SATEENKAARIPORTAIKKO", fa: "ایستگاه ۴ از ۸ · راه‌پله رنگین‌کمان و درهای بنفش" }
  },
  {
    hotspotId: 'girls_upper_hall',
    temporal: 0.0,
    cutawayMode: 1,
    camPos: [-12.45, 5.55, -1.60],
    lookAt: [-15.55, 5.15, -9.20],
    waypoints: [
      { t: 0.00, camPos: [-15.25, 5.16, -6.35], lookAt: [-15.25, 4.88, -10.35] },
      { t: 0.18, camPos: [-15.00, 5.30, -1.60], lookAt: [-15.00, 5.20, -8.60] },
      { t: 0.32, camPos: [-15.00, 5.30, -1.60], lookAt: [-15.00, 5.20, -8.60] },
      { t: 0.40, camPos: [-15.25, 5.16, -6.35], lookAt: [-15.25, 4.88, -10.35] },
      { t: 0.55, camPos: [-15.25, 5.16, -6.35], lookAt: [-15.25, 4.88, -10.35] },
      { t: 0.62, camPos: [-15.25, 5.16, -4.15], lookAt: [-15.25, 5.12, -0.15] },
      { t: 1.00, camPos: [-15.25, 5.16, -4.15], lookAt: [-15.25, 5.12, -0.15] }
    ],
    shortBadge: { en: "05 / 08", fi: "05 / 08", fa: "۰۵ / ۰۸" },
    badge: { en: "STOP 5 OF 8 · FIRST FLOOR: GIRLS' ASSEMBLY HALL & PINK/GREEN ROOMS", fi: "PISTE 5/8 · YLÄKERTA: TYTTÖJEN SALI", fa: "ایستگاه ۵ از ۸ · طبقه اول: سالن بزرگ دختران و کلاس‌های صورتی/سبز" }
  },
  {
    hotspotId: 'crater_damage',
    temporal: 1.0,
    cutawayMode: 0,
    camPos: [-16.5, 11.8, 9.5],
    lookAt: [-1.8, 2.0, -5.2],
    waypoints: [
      { t: 0.00, camPos: [-16.5, 11.8, 9.5], lookAt: [-1.8, 2.0, -5.2] },
      { t: 0.14, camPos: [-5.85, 3.05, -4.85], lookAt: [-0.20, 1.25, -4.75] },
      { t: 0.32, camPos: [-5.85, 3.05, -4.85], lookAt: [-0.20, 1.25, -4.75] },
      { t: 0.40, camPos: [-1.80, 2.25, -4.45], lookAt: [2.95, 1.95, -4.45] },
      { t: 0.50, camPos: [-1.80, 2.25, -4.45], lookAt: [2.95, 1.95, -4.45] },
      { t: 0.58, camPos: [-0.85, 2.15, -1.65], lookAt: [-0.85, 1.65, -6.75] },
      { t: 1.00, camPos: [-0.85, 2.15, -1.65], lookAt: [-0.85, 1.65, -6.75] }
    ],
    shortBadge: { en: "06 / 08", fi: "06 / 08", fa: "۰۶ / ۰۸" },
    badge: { en: "STOP 6 OF 8 · 11:22 AM STRIKE: 5M CRATER & EXTENT OF COLLAPSE", fi: "PISTE 6/8 · KLO 11.22 ISKU: 5M KRAATTERI", fa: "ایستگاه ۶ از ۸ · ساعت ۱۱:۲۲: گودال ۵ متری و محدوده تخریب" }
  },
  {
    hotspotId: 'second_wave',
    temporal: 1.0,
    cutawayMode: 0,
    camPos: [25.5, 5.1, 13.8],
    lookAt: [13.5, 2.5, 2.6],
    waypoints: [
      { t: 0.00, camPos: [25.5, 5.1, 13.8], lookAt: [13.5, 2.5, 2.6] },
      { t: 0.12, camPos: [21.5, 2.12, 8.75], lookAt: [22.75, 1.98, 3.10] },
      { t: 0.30, camPos: [21.2, 2.06, 8.30], lookAt: [22.75, 1.98, 3.10] },
      { t: 0.42, camPos: [13.65, 1.84, 10.75], lookAt: [13.50, 1.72, 5.55] },
      { t: 0.64, camPos: [13.55, 1.78, 10.20], lookAt: [13.50, 1.74, 5.55] },
      { t: 1.00, camPos: [13.55, 1.78, 10.20], lookAt: [13.50, 1.74, 5.55] }
    ],
    shortBadge: { en: "07 / 08", fi: "07 / 08", fa: "۰۷ / ۰۸" },
    badge: { en: "STOP 7 OF 8 · 2:30 PM SECOND WAVE & TOMAHAWK EVIDENCE", fi: "PISTE 7/8 · KLO 14.30 TOINEN ISKUAALTO", fa: "ایستگاه ۷ از ۸ · ساعت ۱۴:۳۰: موج دوم حملات و شواهد تاماهاک" }
  },
  {
    hotspotId: 'vow_shrine',
    temporal: 0.0,
    cutawayMode: 0,
    camPos: [-1.5, 2.35, 23.2],
    lookAt: [-1.5, 2.05, 9.5],
    waypoints: [
      { t: 0.00, camPos: [-1.5, 2.35, 23.2], lookAt: [-1.5, 1.85, 11.0] },
      { t: 0.18, camPos: [-2.40, 1.85, 16.0], lookAt: [-5.20, 1.40, 15.0] },
      { t: 0.32, camPos: [-0.60, 1.85, 16.0], lookAt: [2.20, 1.40, 15.0] },
      { t: 0.44, camPos: [-2.95, 1.90, 13.65], lookAt: [-4.45, 1.88, 9.65] },
      { t: 0.60, camPos: [-2.95, 1.90, 13.65], lookAt: [-4.45, 1.88, 9.65] },
      { t: 0.68, camPos: [-0.05, 1.90, 13.65], lookAt: [1.45, 1.88, 9.65] },
      { t: 0.82, camPos: [-0.05, 1.90, 13.65], lookAt: [1.45, 1.88, 9.65] },
      { t: 0.90, camPos: [-1.5, 2.48, 18.8], lookAt: [-1.5, 1.88, 9.5] },
      { t: 1.00, camPos: [-1.5, 2.48, 18.8], lookAt: [-1.5, 1.88, 9.5] }
    ],
    shortBadge: { en: "08 / 08", fi: "08 / 08", fa: "۰۸ / ۰۸" },
    badge: { en: "STOP 8 OF 8 · THE ACCOUNTABILITY VOW SHRINE", fi: "PISTE 8/8 · VASTUULUPAUKSEN MUISTOMERKKI", fa: "ایستگاه ۸ از ۸ · یادمان میثاق دادخواهی — ثبت پیمان جهانی" }
  }
];

export const HOTSPOT_CONFIGS = [
  { id: 'courtyard_lines', icon: '1', pos: [15.5, 1.2, 8.25], presetCam: [5.5, 2.8, 12.0], target: [22.0, 1.6, 6.5], cutaway: 0 },
  { id: 'boys_flower_arch', icon: '2', pos: [3.8, 2.1, -6.0], presetCam: [2.2, 4.4, -0.5], target: [4.0, 1.8, -6.5], cutaway: 2 },
  { id: 'boys_classroom', icon: '3', pos: [-15.8, 2.1, -0.2], presetCam: [-11.8, 4.3, 3.8], target: [-16.2, 1.6, -1.0], cutaway: 2 },
  { id: 'rainbow_staircase', icon: '4', pos: [-1.8, 2.3, -8.4], presetCam: [-1.8, 2.25, -3.2], target: [-1.8, 2.0, -9.8], cutaway: 2 },
  { id: 'girls_upper_hall', icon: '5', pos: [-15.2, 5.6, -5.5], presetCam: [-9.5, 8.6, 3.5], target: [-15.2, 5.2, -5.5], cutaway: 1 },
  { id: 'crater_damage', icon: '6', pos: [-2.5, 3.2, -5.5], presetCam: [-18.0, 13.5, 12.0], target: [-1.5, 2.2, -5.5], cutaway: 0 },
  { id: 'second_wave', icon: '7', pos: [18.0, 2.5, 11.5], presetCam: [26.0, 9.5, 22.0], target: [6.0, 2.2, 1.0], cutaway: 0 },
  { id: 'vow_shrine', icon: '✍️', pos: [-1.5, 3.8, 10.5], presetCam: [-1.5, 2.4, 18.0], target: [-1.5, 2.0, 10.5], isVow: true, cutaway: 1 }
];

export const IN_WORLD_SCREEN_SPECS = [
  // Station 1: Courtyard Morning Lines (mounted in preStrikeModelGroup so post-strike yard stays clean)
  // Yard steles, all facing the yard. They copy the Courtyard Memorial Avenue steles (dark
  // slab, gold rim, on the ground): style 'stele', no plaque, no poster. The media area is
  // letterboxed inside the slab, never stretched. Media lives in media/walkthrough_pip/yard/.
  // EAST: three steles in a row at x = 25.0 facing west over the lines (A, C, D), with the
  // 16:9 video stele (E) stacked on top of the middle one. The row starts south of the pastel
  // dividing wall (Z = 2.4) and stays clear of the yard portrait steles (Z = 13.8, X <= 22.8).
  // WEST: the schoolyard still-photo stele (01_B) with Ms. Shahriyari's stele beside it,
  // in one line at x = 8.0 facing east (the teacher's is built in memorial-gallery.js).
  {
    id: '01_A', hotspotId: 'courtyard_lines', slot: 'A', groupKey: 'preStrike',
    file: 'yard/yard_video_01', style: 'stele', noPoster: true, noPlaque: true,
    durationSec: 30, cueStartP: 0.0, cueEndP: 0.539, cueStartPFa: 0.0, cueEndPFa: 0.587, cueStartPFi: 0.0, cueEndPFi: 0.513,
    pos: [25.00, 1.54, 4.45], rotY: -Math.PI / 2, w: 3.00, h: 2.60, hasLegs: false,
    badge: { en: '', fi: '', fa: '' }, caption: { en: '', fi: '', fa: '' }
  },
  {
    id: '01_C', hotspotId: 'courtyard_lines', slot: 'C', groupKey: 'preStrike',
    file: 'yard/yard_video_02', style: 'stele', noPoster: true, noPlaque: true,
    durationSec: 30, cueStartP: 0.0, cueEndP: 0.539, cueStartPFa: 0.0, cueEndPFa: 0.587, cueStartPFi: 0.0, cueEndPFi: 0.513,
    pos: [25.00, 1.54, 8.25], rotY: -Math.PI / 2, w: 3.00, h: 2.60, hasLegs: false,
    badge: { en: '', fi: '', fa: '' }, caption: { en: '', fi: '', fa: '' }
  },
  {
    id: '01_D', hotspotId: 'courtyard_lines', slot: 'D', groupKey: 'preStrike',
    images: [1, 2, 3, 4, 5, 6, 7, 8].map((n) => `media/walkthrough_pip/yard/yard_photo_0${n}.jpg`),
    slideSec: 3.5, style: 'stele', noPoster: true, noPlaque: true,
    durationSec: 28, cueStartP: 0.0, cueEndP: 0.539, cueStartPFa: 0.0, cueEndPFa: 0.587, cueStartPFi: 0.0, cueEndPFi: 0.513,
    pos: [25.00, 1.54, 12.05], rotY: -Math.PI / 2, w: 3.00, h: 2.60, hasLegs: false,
    badge: { en: '', fi: '', fa: '' }, caption: { en: '', fi: '', fa: '' }
  },
  {
    id: '01_E', hotspotId: 'courtyard_lines', slot: 'E', groupKey: 'preStrike',
    file: 'yard/yard_video_03', style: 'stele', noPoster: true, noPlaque: true,
    durationSec: 30, cueStartP: 0.0, cueEndP: 0.539, cueStartPFa: 0.0, cueEndPFa: 0.587, cueStartPFi: 0.0, cueEndPFi: 0.513,
    pos: [25.00, 3.93, 8.25], rotY: -Math.PI / 2, w: 3.00, h: 1.69, hasLegs: false,
    badge: { en: '', fi: '', fa: '' }, caption: { en: '', fi: '', fa: '' }
  },
  {
    id: '01_B', hotspotId: 'courtyard_lines', slot: 'B', groupKey: 'preStrike',
    file: 'yard/yard_video_04', loop: true, style: 'stele', noPoster: true, noPlaque: true, durationSec: 30.0, cueStartP: 0.539, cueEndP: 0.991, cueStartPFa: 0.587, cueEndPFa: 0.975, cueStartPFi: 0.513, cueEndPFi: 0.987,
    pos: [8.00, 1.49, 9.50], rotY: Math.PI / 2, w: 1.40, h: 2.50, hasLegs: false,
    badge: { en: '', fi: '', fa: '' }, caption: { en: '', fi: '', fa: '' }
  },
  // Station 2: Ground-Floor Boys' Ceremony Room & Colorful Playroom
  {
    id: '02_A', hotspotId: 'boys_flower_arch', slot: 'A', groupKey: 'groundFloor',
    file: '02_sync_playroom_memories', durationSec: 24.0, cueStartP: 0.0, cueEndP: 0.403, cueStartPFa: 0.0, cueEndPFa: 0.407, cueStartPFi: 0.0, cueEndPFi: 0.430,
    pos: [3.62, 1.54, -8.04], rotY: 0, w: 1.90, h: 1.07, hasLegs: false,
    badge: {
      en: 'GROUND FLOOR · PLAYROOM & CHILDHOOD MEMORIES',
      fi: 'ALAKERTA · LEIKKIHUONE JA LAPSUUDEN MUISTOT',
      fa: 'طبقه همکف · خانه بازی و خاطرات کودکی'
    },
    caption: {
      en: 'Pre-school children laughing inside the mural-painted playroom and ball-pit, and the room\'s Mother\'s Day and book fair memories.',
      fi: 'Esikoululaiset nauramassa kuvitetussa leikkihuoneessa ja pallomeressä sekä huoneen äitienpäivä- ja kirjamessumuistot.',
      fa: 'خنده نوآموزان در «خانه بازی» رنگارنگ و خاطرات جشن روز مادر و نمایشگاه کتاب همین اتاق.'
    }
  },
  {
    id: '02_B', hotspotId: 'boys_flower_arch', slot: 'B', groupKey: 'groundFloor',
    file: '02_sync_rose_arch_photo', durationSec: 32.0, cueStartP: 0.403, cueEndP: 0.989, cueStartPFa: 0.407, cueEndPFa: 0.972, cueStartPFi: 0.430, cueEndPFi: 0.980,
    pos: [0.22, 1.60, -6.40], rotY: Math.PI / 2, w: 2.24, h: 1.26, hasLegs: false,
    badge: {
      en: 'ROSE ARCH PHOTO · TWELVE BOYS IN ROYAL-BLUE UNIFORMS',
      fi: 'RUUSUKAARIVALOKUVA · KAKSITOISTA POIKAA SINISISSÄ KOULUPUVUISSA',
      fa: 'عکس طاق گل رز · دوازده پسر با لباس فرم آبی'
    },
    caption: {
      en: 'The teacher\'s photograph of twelve little boys in royal-blue uniforms standing proudly beneath two arches of red roses.',
      fi: 'Opettajan valokuva kahdestatoista pienestä pojasta sinisissä koulupuvuissaan seisomassa kahden punaisen ruusukaaren alla.',
      fa: 'عکس معلم از دوازده پسر کوچک با لباس فرم آبی که با غرور زیر دو طاق گل سرخ ایستاده‌اند.'
    }
  },
  // Station 3: Ground-Floor West Boys' Classroom (Sky-Blue Walls & Green Carpet)
  {
    id: '03_A', hotspotId: 'boys_classroom', slot: 'A', groupKey: 'groundFloor',
    file: '03_sync_boys_carpet_clapping', durationSec: 27.6, cueStartP: 0.0, cueEndP: 0.754, cueStartPFa: 0.0, cueEndPFa: 0.721, cueStartPFi: 0.0, cueEndPFi: 0.738,
    pos: [-18.73, 1.58, 0.00], rotY: Math.PI / 2, w: 2.68, h: 1.51, hasLegs: false,
    badge: {
      en: 'SKY-BLUE CLASSROOM · 35+ BOYS CLAPPING ON CARPETS',
      fi: 'TAIVAANSININEN LUOKKA · YLI 35 POIKAA TAPUTTAMASSA',
      fa: 'کلاس آبی‌آسمانی · دست‌زدن بیش از ۳۵ پسر بر موکت سبز'
    },
    caption: {
      en: 'More than thirty-five boys sitting side by side on the green carpets, clapping their hands joyfully and singing together.',
      fi: 'Yli kolmekymmentäviisi poikaa istumassa vierekkäin vihreillä matoilla, taputtaen ja laulaen yhdessä.',
      fa: 'بیش از سی‌وپنج دانش‌آموز پسر کنار هم بر موکت سبز نشسته و با شادی دست می‌زنند و هم‌خوانی می‌کنند.'
    }
  },
  {
    id: '03_B', hotspotId: 'boys_classroom', slot: 'B', groupKey: 'groundFloor',
    file: '03_sync_faces_and_drawings', durationSec: 23.8, cueStartP: 0.754, cueEndP: 0.991, cueStartPFa: 0.721, cueEndPFa: 0.968, cueStartPFi: 0.738, cueEndPFi: 0.985,
    pos: [-14.45, 1.48, 2.15], rotY: Math.PI, w: 2.48, h: 1.40, hasLegs: false,
    badge: {
      en: 'THEIR FACES & THE DRAWINGS THEY LEFT BEHIND',
      fi: 'HEIDÄN KASVONSA JA SEINILLE JÄÄNEET PIIRUSTUKSET',
      fa: 'چهره‌هایشان و نقاشی‌های به‌جامانده بر دیوار'
    },
    caption: {
      en: 'A quiet moment to look at the boys\' faces and the drawings they left behind on these classroom walls.',
      fi: 'Hiljainen hetki katsoa poikien kasvoja ja piirustuksia, jotka jäivät näiden luokkahuoneiden seinille.',
      fa: 'لحظه‌ای آرام برای نگاه به چهره پسران و نقاشی‌های به‌جامانده بر دیوار همین کلاس.'
    }
  },
  // Station 4: Central Hall & Enclosed Rainbow Staircase
  {
    id: '04_A', hotspotId: 'rainbow_staircase', slot: 'A', groupKey: 'groundFloor',
    file: '04_sync_stairs_welcome', durationSec: 26.4, cueStartP: 0.0, cueEndP: 0.572, cueStartPFa: 0.0, cueEndPFa: 0.576, cueStartPFi: 0.0, cueEndPFi: 0.613,
    pos: [-4.45, 1.58, -7.35], rotY: 0.35, w: 2.46, h: 1.38, hasLegs: true, legFloorY: 0.20,
    badge: {
      en: 'RAINBOW STAIRS · TEACHERS WELCOME WITH TRAYS OF SWEETS',
      fi: 'SATEENKAARIPORTAAT · OPETTAJAT VASTAASSA MAKEISIN',
      fa: 'پله‌های رنگین‌کمان · استقبال معلمان با سینی شیرینی'
    },
    caption: {
      en: 'Teachers standing at the foot of the rainbow stairs with trays of sweets, beside the purple classroom doors and paper flowers.',
      fi: 'Opettajat seisomassa sateenkaariportaiden juurella makeistarjottimineen purppuraovien ja paperikukkien vieressä.',
      fa: 'معلمان در پای پله‌های رنگین‌کمان با سینی‌های شیرینی، کنار درهای بنفش کلاس‌ها و گل‌های کاغذی.'
    }
  },
  {
    id: '04_B', hotspotId: 'rainbow_staircase', slot: 'B', groupKey: 'groundFloor',
    file: '04_sync_stairwell_collapse', durationSec: 27.4, cueStartP: 0.572, cueEndP: 0.968, cueStartPFa: 0.576, cueEndPFa: 0.968, cueStartPFi: 0.613, cueEndPFi: 0.989,
    pos: [-5.03, 1.60, -3.58], rotY: Math.PI, w: 2.50, h: 1.41, hasLegs: false,
    badge: {
      en: 'THE COLLAPSE · PRINCIPAL SANGARZADEH FELL DOWN THESE STAIRS',
      fi: 'ROMAHDUS · REHTORI SANGARZADEH PUTOSI PORTAISSA',
      fa: 'لحظه فروریختن · خانم سنگرزاده از همین پله‌ها افتاد'
    },
    caption: {
      en: 'The stairwell where the blast threw principal Ms. Sangarzadeh down the stairs, and the roof collapsed above the children.',
      fi: 'Portaikko, jossa räjähdys paiskasi rehtori Sangarzadehin alas portaita ja katto romahti lasten päälle.',
      fa: 'راه‌پله‌ای که موج انفجار خانم سنگرزاده را از آن پایین انداخت و سقف بر سر کودکان فروریخت.'
    }
  },
  // Station 5: First-Floor Girls' Primary School Assembly Hall
  {
    id: '05_A', hotspotId: 'girls_upper_hall', slot: 'A', groupKey: 'firstFloor',
    file: '05_sync_80_girls_hall', durationSec: 30.0, cueStartP: 0.0, cueEndP: 0.588, cueStartPFa: 0.0, cueEndPFa: 0.635, cueStartPFi: 0.0, cueEndPFi: 0.594,
    pos: [-15.25, 5.06, -10.35], rotY: 0, w: 3.35, h: 1.88, hasLegs: true, legFloorY: 3.71,
    badge: {
      en: '80+ SCHOOLGIRLS IN THE UPPER ASSEMBLY HALL',
      fi: 'YLI 80 KOULUTYTTÖÄ YLÄKERRAN SALISSA',
      fa: 'بیش از ۸۰ دانش‌آموز دختر در سالن بزرگ طبقه بالا'
    },
    caption: {
      en: 'A teacher\'s photograph of more than eighty schoolgirls in white headscarves sitting shoulder to shoulder on the green carpet.',
      fi: 'Opettajan valokuva yli kahdeksastakymmenestä valkohuivisesta koulutytöstä istumassa vierekkäin vihreällä matolla.',
      fa: 'عکس معلم از بیش از هشتاد دانش‌آموز دختر با مقنعه سفید که شانه‌به‌شانه بر فرش سبز نشسته‌اند.'
    }
  },
  {
    id: '05_B', hotspotId: 'girls_upper_hall', slot: 'B', groupKey: 'firstFloor',
    file: '05_sync_desks_and_notebooks', durationSec: 26.1, cueStartP: 0.588, cueEndP: 0.975, cueStartPFa: 0.635, cueEndPFa: 0.973, cueStartPFi: 0.594, cueEndPFi: 0.985,
    pos: [-15.25, 5.12, -0.15], rotY: Math.PI, w: 3.35, h: 1.88, hasLegs: true, legFloorY: 3.71,
    badge: {
      en: 'HOMEWORK NOTEBOOKS & COLORED PENCILS',
      fi: 'KOTITEHTÄVÄVIHKOT JA VÄRIKYNÄT',
      fa: 'دفترهای مشق باز و مدادهای رنگی'
    },
    caption: {
      en: 'Seven-, eight- and nine-year-old girls sitting beside their closest friends with open homework notebooks and colored pencils.',
      fi: 'Seitsemän-, kahdeksan- ja yhdeksänvuotiaat tytöt istumassa ystäviensä vieressä vihkot auki ja värikynät kädessään.',
      fa: 'دختران هفت، هشت و نه ساله کنار نزدیک‌ترین دوستانشان با دفترهای مشق باز و مدادهای رنگی.'
    }
  },
  // Station 6: 11:22 AM Direct Cruise Missile Impact & 5m Crater
  {
    id: '06_A', hotspotId: 'crater_damage', slot: 'A', groupKey: 'postStrike',
    file: '06_sync_crater_comparison', durationSec: 28.2, cueStartP: 0.0, cueEndP: 0.514, cueStartPFa: 0.0, cueEndPFa: 0.532, cueStartPFi: 0.0, cueEndPFi: 0.475,
    pos: [2.95, 1.98, -4.45], rotY: -Math.PI / 2, w: 3.60, h: 2.02, hasLegs: true, legFloorY: 0.15,
    badge: {
      en: '5-METER CRATER · BEFORE & AFTER COMPARISON',
      fi: '5 METRIN KRAATTERI · ENNEN JA JÄLKEEN -VERTAILU',
      fa: 'گودال ۵ متری · مقایسه پیش و پس از حمله'
    },
    caption: {
      en: 'Direct cruise missile strikes through the central hall roof and the five-meter crater left where the children had been sitting.',
      fi: 'Risteilyohjusten suorat osumat keskussalin katon läpi sekä viiden metrin kraatteri, joka jäi lasten istumapaikalle.',
      fa: 'اصابت مستقیم موشک‌های کروز به سقف سالن مرکزی و گودال پنج متری برجای‌مانده در جای نشستن کودکان.'
    }
  },
  {
    id: '06_B', hotspotId: 'crater_damage', slot: 'B', groupKey: 'postStrike',
    file: '06_sync_mothers_bags_and_drawings', durationSec: 32.2, cueStartP: 0.514, cueEndP: 0.977, cueStartPFa: 0.532, cueEndPFa: 0.957, cueStartPFi: 0.475, cueEndPFi: 0.984,
    pos: [-0.85, 1.96, -6.75], rotY: 0, w: 3.55, h: 2.00, hasLegs: true, legFloorY: 0.15,
    badge: {
      en: 'MOTHERS, SCHOOLBAGS & 28 SHRAPNEL-PIERCED DRAWINGS',
      fi: 'ÄIDIT, KOULUREPUT JA 28 SIRPALEIDEN LÄVISTÄMÄÄ PIIRUSTUSTA',
      fa: 'مادران، کیف‌های مدرسه و ۲۸ نقاشی سوراخ‌شده از ترکش'
    },
    caption: {
      en: 'Bereaved mothers amid the rubble, and the dust-covered schoolbags and twenty-eight shrapnel-pierced drawings that remained.',
      fi: 'Surevia äitejä raunioiden keskellä sekä pölyn peittämät koulureput ja kaksikymmentäkahdeksan sirpaleiden lävistämää piirustusta.',
      fa: 'مادران داغدار در میان آوار و کیف‌های خاک‌گرفته مدرسه و بیست‌وهشت نقاشی و مشق سوراخ‌شده از ترکش.'
    }
  },
  // Station 7: 2:30 PM Second Wave & Recovered US Tomahawk Munitions Evidence
  {
    id: '07_A', hotspotId: 'second_wave', slot: 'A', groupKey: 'postStrike',
    file: '07_sync_barehands_rescue', durationSec: 24.5, cueStartP: 0.0, cueEndP: 0.400, cueStartPFa: 0.0, cueEndPFa: 0.401, cueStartPFi: 0.0, cueEndPFi: 0.411,
    pos: [22.75, 2.04, 3.10], rotY: -0.18, w: 4.15, h: 2.33, hasLegs: true, legFloorY: 0.02,
    badge: {
      en: 'MOTHERS & RESCUERS DIGGING WITH BARE HANDS',
      fi: 'ÄIDIT JA PELASTAJAT KAIVAMASSA PALJAIN KÄSIN',
      fa: 'مادران و امدادگران در حال آواربرداری با دست خالی'
    },
    caption: {
      en: 'More than a thousand mothers, fathers, and Red Crescent rescuers digging through the rubble with their bare hands.',
      fi: 'Yli tuhat äitiä, isää ja Punaisen Puolikuun pelastajaa kaivamassa raunioita paljain käsin.',
      fa: 'بیش از هزار مادر، پدر و امدادگر هلال‌احمر که با دست خالی آوار را کنار می‌زدند.'
    }
  },
  {
    id: '07_B', hotspotId: 'second_wave', slot: 'B', groupKey: 'postStrike',
    file: '07_sync_tomahawk_then_smoke', durationSec: 35.6, cueStartP: 0.400, cueEndP: 0.984, cueStartPFa: 0.401, cueEndPFa: 0.969, cueStartPFi: 0.411, cueEndPFi: 0.984,
    pos: [13.50, 2.16, 5.55], rotY: 0, w: 3.75, h: 2.05, hasLegs: true, legFloorY: 0.02,
    badge: {
      en: '2:30 PM SECOND WAVE · TOMAHAWK & BLACK SMOKE',
      fi: 'KLO 14.30 TOINEN AALTO · TOMAHAWK JA MUSTA SAVU',
      fa: 'ساعت ۱۴:۳۰ موج دوم · تاماهاک و دود سیاه'
    },
    caption: {
      en: 'The second wave of cruise missiles striking beside the school as the sky turns black with smoke and dust again.',
      fi: 'Toinen risteilyohjusten aalto iskee koulun viereen taivaan pimentyessä jälleen savusta ja pölystä.',
      fa: 'موج دوم موشک‌های کروز در کنار مدرسه فرود می‌آید و آسمان بار دیگر از دود و غبار سیاه می‌شود.'
    }
  },
  // Station 8: Accountability Vow Shrine & Tribute Boards
  {
    id: '08_A', hotspotId: 'vow_shrine', slot: 'A', groupKey: 'memorial',
    file: '08_sync_echo_of_rooms', durationSec: 34.4, cueStartP: 0.435, cueEndP: 0.665, cueStartPFa: 0.465, cueEndPFa: 0.724, cueStartPFi: 0.427, cueEndPFi: 0.715,
    pos: [-4.45, 1.92, 9.65], rotY: 0.30, w: 3.35, h: 1.88, hasLegs: true, legFloorY: 0.02,
    badge: {
      en: 'WALK THROUGH THEIR CLASSROOMS · HEAR THEIR VOICES',
      fi: 'KULJE HEIDÄN LUOKKIENSA LÄPI · KUULE HEIDÄN ÄÄNENSÄ',
      fa: 'قدم‌زدن در کلاس‌هایشان · شنیدن صدایشان'
    },
    caption: {
      en: 'Walking through the rebuilt classrooms, seeing their rainbow stairs, touching their drawings, and hearing their voices.',
      fi: 'Kävely uudelleen rakennettujen luokkien läpi, sateenkaariportaiden näkeminen, piirustusten koskettaminen ja äänten kuuleminen.',
      fa: 'قدم‌زدن در کلاس‌های بازسازی‌شده، دیدن پله‌های رنگین‌کمانشان، لمس نقاشی‌هایشان و شنیدن صدایشان.'
    }
  },
  {
    id: '08_B', hotspotId: 'vow_shrine', slot: 'B', groupKey: 'memorial',
    file: '08_sync_justice_vow', durationSec: 26.3, cueStartP: 0.665, cueEndP: 0.988, cueStartPFa: 0.724, cueEndPFa: 0.992, cueStartPFi: 0.715, cueEndPFi: 0.991,
    pos: [1.45, 1.92, 9.65], rotY: -0.30, w: 3.35, h: 1.88, hasLegs: true, legFloorY: 0.02,
    badge: {
      en: 'SIGN THE MINAB ACCOUNTABILITY VOW',
      fi: 'ALLEKIRJOITA MINABIN VASTUULUPAUS',
      fa: 'امضای میثاق دادخواهی میناب'
    },
    caption: {
      en: 'Signing the vow that until every person who ordered and carried out this crime answers before justice, we will stand beside the truth.',
      fi: 'Allekirjoita lupaus, että seisomme totuuden rinnalla, kunnes jokainen tähän rikokseen syyllistynyt vastaa oikeuden edessä.',
      fa: 'امضای میثاقی که تا پاسخ‌گویی تک‌تک عاملان این جنایت در برابر عدالت، در کنار حقیقت خواهیم ایستاد.'
    }
  }
];

export const WALKTHROUGH_VISUAL_CONFIG = {
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
      window: [0.54, 0.74],
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
      window: [0.76, 0.88],
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
      window: [0.53, 0.78],
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
      window: [0.64, 0.94],
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

export const SPOT_ARCHIVAL_AUDIO = {};

export const WALKTHROUGH_BOOKENDS = {
  prologue: {
    durationMs: 5200,
    kicker: {
      en: 'FORENSIC SPATIAL RECONSTRUCTION & LIVING ARCHIVE',
      fa: 'بازسازی فضایی مستند و آرشیو زنده مدرسه میناب',
      fi: 'FORENSINEN TILAREKONSTRUKTIO JA ELÄVÄ ARKISTO'
    },
    title: {
      en: 'Shajareh Tayyebeh Primary School',
      fa: 'دبستان شجره طیبه میناب',
      fi: 'Shajareh Tayyebehin alakoulu'
    },
    coords: {
      en: '27°08′43″N 57°05′02″E · Minab, Hormozgan · February 28, 2026',
      fa: 'میناب، استان هرمزگان · شنبه ۹ اسفند ۱۴۰۴ (۲۸ فوریه ۲۰۲۶)',
      fi: '27°08′43″N 57°05′02″E · Minab · 28. helmikuuta 2026'
    },
    note: {
      en: 'Every photograph, child\'s voice, and eyewitness video inside these rooms was recorded in this school before and on the day of the strike.',
      fa: 'تمامی عکس‌ها، صدای کودکان و ویدیوهای درون این اتاق‌ها، پیش از حمله و در روز حادثه در همین دبستان ثبت شده‌اند.',
      fi: 'Jokainen valokuva, lapsen ääni ja silminnäkijävideo näissä huoneissa on tallennettu tässä koulussa ennen iskua ja iskun päivänä.'
    }
  },
  epilogue: {
    durationMs: 7000,
    kicker: {
      en: 'IN REMEMBRANCE & PURSUIT OF JUSTICE',
      fa: 'به یاد کودکان میناب و در مسیر دادخواهی',
      fi: 'MUISTOKSI JA OIKEUDENMUKAISUUDEN PUOLESTA'
    },
    title: {
      en: '120 Schoolchildren & 26 Educators',
      fa: '۱۲۰ دانش‌آموز خردسال و ۲۶ آموزگار',
      fi: '120 koululaista ja 26 opettajaa'
    },
    coords: {
      en: 'Shajareh Tayyebeh Primary School · Minab · February 28, 2026',
      fa: 'دبستان شجره طیبه میناب · ۹ اسفند ۱۴۰۴',
      fi: 'Shajareh Tayyebehin alakoulu · Minab · 28.2.2026'
    },
    note: {
      en: 'Stand beside their families and sign the Global Accountability Vow — peopleforpeace.live',
      fa: 'در کنار خانواده‌هایشان بایستید و «میثاق جهانی دادخواهی میناب» را امضا کنید — peopleforpeace.live',
      fi: 'Seiso perheiden rinnalla ja allekirjoita vastuulupaus — peopleforpeace.live'
    }
  },
  skipBtn: {
    en: 'Skip Interlude ›',
    fa: 'عبور از ویدیو ›',
    fi: 'Ohita välivideo ›'
  }
};

export const WALKTHROUGH_INTERLUDES = {
  boys_flower_arch: {
    id: 'interlude_02',
    src: 'media/walkthrough_interludes/interlude_02_rose_arch_and_mahan.mp4',
    aspect: 'classic',
    tone: 'pre',
    kicker: {
      en: 'GROUND FLOOR · ROSE ARCH SINGING & MAHAN\'S MOTHER\'S DAY VOICE',
      fa: 'طبقه همکف · هم‌خوانی زیر طاق گل رز و پیام روز مادر ماهان',
      fi: 'ALAKERTA · RUUSUKAARILAULU JA PIKKU MAHANIN ÄITIENPÄIVÄVIESTI'
    },
    context: { en: '', fa: '', fi: '' },
    // Subtitles intentionally removed: the previous cues did not match the footage.
    cues: []
  },
  boys_classroom: {
    id: 'interlude_03',
    src: 'media/walkthrough_interludes/interlude_03_boys_classroom_laughter.mp4',
    aspect: 'classic',
    tone: 'pre',
    kicker: {
      en: 'UNEDITED CLASSROOM AUDIO · CHILDHOOD LAUGHTER AT GREEN DESKS',
      fa: 'صدای کاملاً طبیعی و بدون ویرایش · خنده‌های کودکانه پشت نیمکت‌های سبز',
      fi: 'ALKUPERÄINEN LUOKKAÄÄNI · POIKIEN NAURU VIHREILLÄ PULPETEILLA'
    },
    context: {
      en: 'Raw classroom recording inside Shajareh Tayyebeh Boys\' School — unedited laughter during a playful science activity',
      fa: 'فیلم خام کلاسی از شوخی و خنده‌های بی‌وقفه دانش‌آموزان پسر با آموزگارشان در دبستان شجره طیبه',
      fi: 'Muokkaamaton luokkahuonetallenne poikien ilosta ja naurusta opettajansa kanssa'
    },
    cues: [
      {
        s: 0.4, e: 15.1,
        en: '[Unedited classroom audio: young boys laughing and cheering together at their green desks]',
        fa: '[صدای واقعی کلاس: خنده‌ها و شادی کودکانه دانش‌آموزان پسر پشت نیمکت‌های سبز]',
        fi: '[Alkuperäinen luokkaääni: pienten koulupoikien iloinen nauru luokkahuoneessa]'
      }
    ]
  },
  girls_upper_hall: {
    id: 'interlude_04',
    src: 'media/walkthrough_interludes/interlude_04_the_hinge_1045am.mp4',
    aspect: 'portrait',
    tone: 'strike',
    ruptureWindow: {
      s: 8.2, e: 10.7,
      time: {
        en: 'SATURDAY · FEBRUARY 28, 2026 · FIRST STRIKE',
        fa: 'شنبه ۹ اسفند ۱۴۰۴ · لحظه اصابت نخستین موشک',
        fi: 'LAUANTAI · 28. HELMIKUUTA 2026 · ENSIMMÄINEN ISKU'
      },
      title: {
        en: 'Direct Cruise Missile Impact on Shajareh Tayyebeh Primary School',
        fa: 'اصابت مستقیم موشک کروز به دبستان شجره طیبه میناب',
        fi: 'Risteilyohjuksen suora osuma Shajareh Tayyebehin alakouluun'
      }
    },
    kicker: {
      en: 'FINAL MINUTES IN 1ST GRADE → FIRST MINUTES IN THE COURTYARD',
      fa: 'آخرین عکس کلاس اول پیش از انفجار ← دقایق نخست در حیاط پر از دود',
      fi: 'EKALUOKAN VIIMEISET HETKET → ENSIMMÄISET MINUUTIT KOULUPIHALLA'
    },
    context: {
      en: 'Photos sent by the 1st-grade teacher to the mothers\' group minutes before impact, followed by raw citizen courtyard video',
      fa: 'تصاویر ارسالی معلم شهید کلاس اول در گروه مادران دقایقی پیش از حمله، و فیلم خام حیاط مدرسه بلافاصله پس از اصابت',
      fi: 'Ekaluokan opettajan äideille lähettämät viimeiset kuvat juuri ennen iskua sekä silminnäkijävideo pihalta iskun jälkeen'
    },
    cues: [
      {
        s: 0.2, e: 8.0,
        en: 'Final photographs sent by the first-grade teacher to the mothers\' chat group — minutes before the strike',
        fa: 'آخرین عکس‌های دانش‌آموزان کلاس اول که معلم شهید دقایقی پیش از اصابت موشک در گروه مادران فرستاد',
        fi: 'Ekaluokan opettajan äitien ryhmään lähettämät viimeiset valokuvat — minuutteja ennen ohjusiskua'
      },
      {
        s: 11.0, e: 16.5,
        en: '[Raw courtyard audio — torn homework sheets cover the dust as families rush toward the smoking classrooms]',
        fa: '[صدای خام صحنه — برگه‌های پراکنده دفتر مشق روی خاک حیاط و دویدن خانواده‌ها به سوی دود سیاه کلاس‌ها]',
        fi: '[Alkuperäinen pihaääni — repeytyneitä koulutehtäviä maassa perheiden ryntäillessä savuaville luokille]'
      },
      {
        s: 16.5, e: 22.8,
        en: 'Voice crying out in the courtyard: "Mohaddeseh!..."',
        fa: 'فریاد مضطرب در حیاط مدرسه: «محدثه!...»',
        fi: 'Hätääntynyt huuto koulupihalla: "Mohaddeseh!..."'
      }
    ]
  },
  crater_damage: {
    id: 'interlude_05',
    src: 'media/walkthrough_interludes/interlude_05_staircase_witness_and_shoes.mp4',
    aspect: 'tall',
    tone: 'strike',
    kicker: {
      en: 'ON-SITE SPATIAL TESTIMONY · SHEARED STAIRCASE & RECOVERED SHOES',
      fa: 'شهادت میدانی در برابر راه‌پله منهدم‌شده و ردیف کفش‌های کوچک کودکان',
      fi: 'PAIKAN PÄÄLLÄ KUVATTU TODISTUS · SORTUNUT PORTAIKKO JA LASTEN KENGÄT'
    },
    context: {
      en: 'Unedited field narration before the sheared central stairwell, followed by recovered children\'s shoes laid out on carpets',
      fa: 'گزارش میدانی بدون ویرایش از مقابل راه‌پله فروریخته مرکزی، و ردیف کفش‌ها و کیف‌های به‌جامانده دانش‌آموزان',
      fi: 'Muokkaamaton kenttätodistus sortuneen keskusportaikon edessä sekä matolle järjestetyt lasten kengät ja reput'
    },
    cues: [
      {
        s: 0.3, e: 6.8,
        en: '"This staircase you see right here — the first missile struck squarely in the center of the building."',
        fa: '«این راه‌پله‌ای که اینجا می‌بینید، موشک اول قشنگ خورده وسط ساختمان، این سمت.»',
        fi: '"Tämä portaikko, jonka näet tässä — ensimmäinen ohjus osui suoraan rakennuksen keskelle."'
      },
      {
        s: 6.8, e: 15.2,
        en: '"The upper floor was the girls\' school, and the ground floor was the boys\' school, with two separate courtyards."',
        fa: '«طبقه بالا مدرسه دخترانه بوده، طبقه پایین مدرسه پسرانه بوده با دو تا حیاط مجزا به این شکل.»',
        fi: '"Yläkerrassa oli tyttöjen koulu ja alakerrassa poikien koulu, joilla oli kaksi erillistä pihaa."'
      },
      {
        s: 15.2, e: 27.9,
        en: '"After the first missile hit the staircase, the second missile struck where the children and mothers had gathered — families who came to save their children were killed."',
        fa: '«بعد از اصابت موشک اول به راه‌پله، موشک دوم زد توی تجمع بچه‌ها؛ مادرهایی که آمده بودند بچه‌ها را ببرند شهید شدند...»',
        fi: '"Ensimmäisen ohjuksen jälkeen toinen ohjus iski sinne, minne lapset ja heitä hakemaan tulleet äidit olivat kokoontuneet."'
      },
      {
        s: 28.4, e: 35.8,
        en: 'Dozens of recovered small shoes, pastel schoolbags, and homework notebooks laid out in rows for parents to identify',
        fa: 'ده‌ها جفت کفش کوچک خاکی، کیف و دفتر مشق دانش‌آموزان که برای شناسایی توسط مادران و پدران بر روی فرش چیده شده است',
        fi: 'Kymmeniä raunioista löydettyjä pieniä kenkiä, koulureppuja ja vihkoja järjestettynä vanhempien tunnistettavaksi'
      }
    ]
  },
  second_wave: {
    id: 'interlude_06',
    src: 'media/walkthrough_interludes/interlude_06_survivors_and_150_graves.mp4',
    aspect: 'portrait',
    tone: 'strike',
    kicker: {
      en: 'HUMAN TOLL · CHILD SURVIVORS, RECOVERED SNEAKER & 150+ GRAVES',
      fa: 'ابعاد انسانی فاجعه · کودکان بازمانده، کفش زیر آوار و ردیف مزارهای کوچک',
      fi: 'INHIMILLINEN HINTA · SELVIYTYNEET LAPSET, PIENI KENKÄ JA YLI 150 HAUTAA'
    },
    context: {
      en: 'Surviving sisters Reyhaneh & Mastaneh, a child\'s sneaker lifted from concrete, and aerial view of the cemetery in Minab',
      fa: 'نگاه بهت‌زده ریحانه و مستانه، کفش کوچک بیرون‌آمده از زیر بتن، و نمای هوایی مزارهای کودکان میناب',
      fi: 'Selviytyneet sisarukset Reyhaneh ja Mastaneh, raunioista nostettu lapsen kenkä sekä ilmakuva Minabin hautausmaalta'
    },
    cues: [
      {
        s: 0.2, e: 5.4,
        en: 'Young surviving sisters Reyhaneh and Mastaneh, covered in blast dust, looking back toward their burning school',
        fa: '«ریحانه» و «مستانه»، دو دانش‌آموز خردسال بازمانده، در میان گردوغبار به ویرانه مدرسه‌شان نگاه می‌کنند',
        fi: 'Pienet selviytyneet sisarukset Reyhaneh ja Mastaneh katsovat pölyn peittäminä palavaa kouluaan'
      },
      {
        s: 5.5, e: 11.9,
        en: 'A rescuer\'s gloved hand gently lifts a child\'s dust-covered sneaker from the shattered classroom concrete',
        fa: 'دستان امدادگر، کفش کوچک خاک‌گرفته یکی از کودکان را از میان سنگ و بتن کلاس بیرون می‌آورد',
        fi: 'Pelastajan käsi nostaa varovasti lapsen pölyisen kengän murskaantuneen luokkahuoneen betonin keskeltä'
      },
      {
        s: 12.0, e: 21.3,
        en: 'Over one hundred small graves excavated side by side in Minab as thousands gather to lay the children to rest',
        fa: 'بیش از صد مزار کوچک حفرشده در کنار یکدیگر در میناب و حضور هزاران سوگوار برای بدرقه کودکان شجره طیبه',
        fi: 'Yli sata vierekkäin kaivettua pientä hautaa Minabissa tuhansien saattajien kokoontuessa hyvästelemään lapset'
      }
    ]
  }
};

export const ROOM_ATMOSPHERE_PROFILES = {
  courtyard_lines:   { freqs: [130.81, 174.61, 196.00, 261.63], padGain: 0.011, padCutoff: 380, breezeFreq: 430, breezeQ: 0.65, breezeGain: 0.015, birdGain: 0.0042, chime: false },
  boys_flower_arch:  { freqs: [130.81, 164.81, 196.00, 246.94], padGain: 0.011, padCutoff: 320, breezeFreq: 290, breezeQ: 0.80, breezeGain: 0.007, birdGain: 0.0020, chime: false },
  boys_classroom:    { freqs: [130.81, 164.81, 196.00, 246.94], padGain: 0.011, padCutoff: 310, breezeFreq: 270, breezeQ: 0.85, breezeGain: 0.006, birdGain: 0.0016, chime: false },
  rainbow_staircase: { freqs: [130.81, 155.56, 196.00, 233.08], padGain: 0.014, padCutoff: 280, breezeFreq: 240, breezeQ: 0.90, breezeGain: 0.006, birdGain: 0.0,    chime: false },
  girls_upper_hall:  { freqs: [130.81, 155.56, 196.00, 233.08], padGain: 0.014, padCutoff: 290, breezeFreq: 250, breezeQ: 0.85, breezeGain: 0.006, birdGain: 0.0,    chime: false },
  crater_damage:     { freqs: [65.41,  130.81, 155.56, 196.00], padGain: 0.020, padCutoff: 260, breezeFreq: 205, breezeQ: 0.95, breezeGain: 0.019, birdGain: 0.0,    chime: false },
  second_wave:       { freqs: [65.41,  130.81, 155.56, 196.00], padGain: 0.020, padCutoff: 250, breezeFreq: 195, breezeQ: 1.00, breezeGain: 0.020, birdGain: 0.0,    chime: false },
  vow_shrine:        { freqs: [130.81, 164.81, 196.00, 246.94], padGain: 0.016, padCutoff: 350, breezeFreq: 330, breezeQ: 0.75, breezeGain: 0.011, birdGain: 0.0022, chime: true  }
};
