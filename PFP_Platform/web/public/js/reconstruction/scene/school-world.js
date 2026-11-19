/**
 * Procedural Minab courtyard murals, terrain, Vow Shrine obelisk,
 * and two-floor Shajareh Tayyebeh school pre/post-strike 3D architecture.
 */
import * as THREE from 'three';

import { appState } from '../state.js';
import { GROUND_FLOOR_WALLS } from './ground-floor-walls.js';
import { FIRST_FLOOR_WALLS } from './first-floor-walls.js';
import { buildAllInWorldWalkthroughScreens } from './in-world-screens.js';
import { buildWalls } from './wall-builder.js';
import { cornerExtensions } from './wall-joints.js';
import {
  createPaintedPlasterMaterial,
  plasterBoxGeometry,
  wallBoxGeometry,
} from './painted-plaster-material.js';

/** Persian and English faces for painted signs; both are loaded by reconstruction.html. */
const FA_CANVAS_FONT = '"Vazirmatn", Tahoma, sans-serif';
const EN_CANVAS_FONT = '"Source Sans 3", "Segoe UI", system-ui, sans-serif';

/**
 * Canvas text does not trigger a webfont download, so a sign painted at boot can keep the
 * fallback face. Re-run its text pass once the requested faces are available.
 */
function repaintCanvasWhenFontsReady(fonts, repaint) {
  if (typeof document === 'undefined' || !document.fonts || !document.fonts.load) return;
  try {
    Promise.all(fonts.map((f) => document.fonts.load(f.font, f.text || ' ')))
      .then(() => repaint())
      .catch(() => {});
  } catch (_) {}
}

/** Canvas murals and painted signs are colour maps, so each one is decoded as sRGB. */
function canvasColorTexture(canvas) {
  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

let cachedMuralTextures = null;
export function getSchoolMuralTextures() {
  if (cachedMuralTextures) return cachedMuralTextures;

  // 3. Main Gate Mint Wall with Colored Pencils & Persian Letters (pip01b_01)
  const gateCanvas = document.createElement('canvas');
  gateCanvas.width = 512;
  gateCanvas.height = 512;
  const gc = gateCanvas.getContext('2d');
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
  // Repaints the whole canvas (background, quoins, pencils, letters) so a font-ready repaint
  // replaces the fallback-face glyphs instead of overlapping them.
  const drawGateLetters = () => {
    gc.fillStyle = '#bfe3d0';
    gc.fillRect(0, 0, 512, 512);
    // Left brick quoins
    for (let by = 16; by < 496; by += 76) {
      gc.fillStyle = '#c84b31';
      gc.fillRect(10, by, 34, 52);
    }
    drawPencil(165, 315, 0.52, '#60a5fa');
    drawPencil(305, 165, -0.68, '#f472b6');
    drawPencil(410, 330, -0.25, '#facc15');
    gc.fillStyle = '#eab308';
    gc.strokeStyle = '#1e293b';
    gc.lineWidth = 4;
    gc.font = `bold 92px ${FA_CANVAS_FONT}`;
    gc.fillText('آ ب', 235, 390);
    gc.strokeText('آ ب', 235, 390);
  };
  drawGateLetters();
  const pencilGateTex = canvasColorTexture(gateCanvas);
  repaintCanvasWhenFontsReady([{ font: `bold 92px ${FA_CANVAS_FONT}`, text: 'آ ب' }], () => {
    drawGateLetters();
    pencilGateTex.needsUpdate = true;
  });

  // 4. Portico Column Texture: the tricolor flag wrapped round the shaft.
  // Only the yard-facing face of a column is painted (see porticoColMats below), so the
  // canvas is one 0.62 m face wide and the full column tall.
  const COL_FACE_M = 0.62;
  const COL_H_M = 3.6; // portico column height, matching floorH
  const colCanvas = document.createElement('canvas');
  colCanvas.width = 512;
  colCanvas.height = 2048;
  const cc = colCanvas.getContext('2d');
  const colPxY = (m) => colCanvas.height - (m * colCanvas.height) / COL_H_M;

  // Three equal bands, green over white over red, tilted so a turn of the shaft climbs
  // 0.4 m. Green runs out to the canopy and red to the ground rather than stopping short.
  const COL_BAND_M = COL_H_M / 3;
  const COL_RISE_M = 0.4;
  const flagEdge = (band, s) => COL_BAND_M * band + (COL_RISE_M * s) / COL_FACE_M;
  const fillBand = (bottomM, topM, fill) => {
    cc.fillStyle = fill;
    cc.beginPath();
    cc.moveTo(0, colPxY(bottomM(0)));
    cc.lineTo(colCanvas.width, colPxY(bottomM(COL_FACE_M)));
    cc.lineTo(colCanvas.width, colPxY(topM(COL_FACE_M)));
    cc.lineTo(0, colPxY(topM(0)));
    cc.closePath();
    cc.fill();
  };
  fillBand(() => 0, (s) => flagEdge(1, s), '#c8393c');
  fillBand((s) => flagEdge(1, s), (s) => flagEdge(2, s), '#fbfcfd');
  fillBand((s) => flagEdge(2, s), () => COL_H_M, '#2f8a52');

  // Hairline along each band edge: the white band needs it to read against pale whitewash.
  cc.strokeStyle = 'rgba(22, 30, 38, 0.24)';
  cc.lineWidth = 3;
  for (const band of [1, 2]) {
    cc.beginPath();
    cc.moveTo(0, colPxY(flagEdge(band, 0)));
    cc.lineTo(colCanvas.width, colPxY(flagEdge(band, COL_FACE_M)));
    cc.stroke();
  }

  const porticoColTex = canvasColorTexture(colCanvas);
  if (appState.renderer) {
    porticoColTex.anisotropy = Math.max(1, Math.min(appState.renderer.getMaxAnisotropy(), 8));
  }

  cachedMuralTextures = {
    pencilGateTex,
    porticoColTex
  };
  return cachedMuralTextures;
}

// --- TERRAIN, 3 WALLED COURTYARDS, 90°-ALIGNED ASSEMBLY LINES, STRIPED SHED & VOW SHRINE ---
export function buildEnvironmentAndTerrain() {
  const { terrainGroup, memorialBoardsGroup } = appState;
  const murals = getSchoolMuralTextures();

  // Outer surroundings plane
  const groundGeo = new THREE.PlaneGeometry(190, 165, 16, 16);
  const groundMat = new THREE.MeshStandardMaterial({ color: 0x20242b, roughness: 0.92, metalness: 0.06 });
  const ground = new THREE.Mesh(groundGeo, groundMat);
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  terrainGroup.add(ground);

  // 1) SE Main Boys' Courtyard Asphalt (X: -17.0..+42.5, Z: +2.4..+30.0)
  const boysYard = new THREE.Mesh(
    new THREE.PlaneGeometry(59.5, 27.6),
    new THREE.MeshStandardMaterial({ color: 0x3b4049, roughness: 0.84 })
  );
  boysYard.rotation.x = -Math.PI / 2;
  boysYard.position.set(12.75, 0.02, 16.2);
  boysYard.receiveShadow = true;
  terrainGroup.add(boysYard);

  // 2) SW Girls' School Yard Surface (X: -34.0..-17.0, Z: -19.5..+30.0)
  const girlsYard = new THREE.Mesh(
    new THREE.PlaneGeometry(17.0, 49.5),
    new THREE.MeshStandardMaterial({ color: 0x464a42, roughness: 0.86 })
  );
  girlsYard.rotation.x = -Math.PI / 2;
  girlsYard.position.set(-25.5, 0.02, 5.25);
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

  // 4) Rear Staircase & Shade Alley (X: -17.0..+19.0, Z: -19.5..-12.8; west of -17.0 is the girls' yard)
  const rearAlley = new THREE.Mesh(
    new THREE.PlaneGeometry(36.0, 6.8),
    new THREE.MeshStandardMaterial({ color: 0x353a42, roughness: 0.86 })
  );
  rearAlley.rotation.x = -Math.PI / 2;
  // Starts at X = -17.0 so it does not overlap the girls' yard plane at the same height.
  rearAlley.position.set(1.0, 0.02, -16.1);
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
  // The north/south bars run the full outer width and the west/east bars fit between them,
  // so the four corners meet cleanly with no overlapping coplanar quads.
  const bT = 0.22;
  const bNorth = new THREE.Mesh(new THREE.PlaneGeometry(boxW + bT, bT), greenBorderMat);
  bNorth.rotation.x = -Math.PI / 2; bNorth.position.set(0, 0, -boxD / 2);
  assemblyGroup.add(bNorth);
  const bSouth = new THREE.Mesh(new THREE.PlaneGeometry(boxW + bT, bT), greenBorderMat);
  bSouth.rotation.x = -Math.PI / 2; bSouth.position.set(0, 0, boxD / 2);
  assemblyGroup.add(bSouth);
  const bWest = new THREE.Mesh(new THREE.PlaneGeometry(bT, boxD - bT), greenBorderMat);
  bWest.rotation.x = -Math.PI / 2; bWest.position.set(-boxW / 2, 0, 0);
  assemblyGroup.add(bWest);
  const bEast = new THREE.Mesh(new THREE.PlaneGeometry(bT, boxD - bT), greenBorderMat);
  bEast.rotation.x = -Math.PI / 2; bEast.position.set(boxW / 2, 0, 0);
  assemblyGroup.add(bEast);

  for (let i = 0; i < 6; i++) {
    const lz = -3.5 + i * 1.40;
    const yLine = new THREE.Mesh(new THREE.PlaneGeometry(13.7, 0.19), yellowMarkMat);
    yLine.rotation.x = -Math.PI / 2;
    yLine.position.set(0.2, 0.005, lz);
    yLine.userData = { feature: 'assembly_yellow_line' };
    assemblyGroup.add(yLine);

    // Standing circle at the -X (portico-facing) head of each line
    const yDot = new THREE.Mesh(new THREE.CircleGeometry(0.30, 24), yellowMarkMat);
    yDot.rotation.x = -Math.PI / 2;
    yDot.position.set(-6.65, 0.006, lz);
    assemblyGroup.add(yDot);
  }

  terrainGroup.add(assemblyGroup);

  const whiteLineMat = new THREE.MeshBasicMaterial({ color: 0xcbd5e1, side: THREE.DoubleSide });

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

  terrainGroup.add(planterGroup);

  // ========================================================
  // COURTYARD DIVIDING & PERIMETER WALLS
  // ========================================================
  const wallMat = createPaintedPlasterMaterial(0xe2e6ec);
  const wallH = 2.65;
  const wallT = 0.36;

  // Every courtyard wall is recorded as a centre-line segment so corners can be closed below.
  const courtyardWalls = [];
  function addCourtyardWall(w, h, d, x, y, z, mat, featureTag, isSolid = true) {
    const alongX = w > d;
    courtyardWalls.push({
      id: `courtyard-${courtyardWalls.length}`,
      from: alongX ? [x - w / 2, z] : [x, z - d / 2],
      to: alongX ? [x + w / 2, z] : [x, z + d / 2],
      t: alongX ? d : w,
      h,
      y,
      mat: mat || wallMat,
    });
    const m = new THREE.Mesh(wallBoxGeometry(w, h, d, mat || wallMat), mat || wallMat);
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

  // 5. SW Girls' Yard Dividing Wall (X = -17.0, Z = +2.4..+30.0), just inside the school's west end
  addCourtyardWall(wallT, wallH, 27.6, -17.0, wallH / 2, 16.2, wallMat, 'sw_girls_dividing_wall', true);

  // 6. South Perimeter Wall (Z = +30.0) & Main Gate with Colored-Pencil Mural (X = -4.2..+1.0 open entrance)
  addCourtyardWall(29.8, wallH, wallT, -19.1, wallH / 2, 30.0, wallMat, null, true);
  addCourtyardWall(41.5, wallH, wallT, 21.75, wallH / 2, 30.0, wallMat, null, true);

  // const pencilGatePanel = new THREE.Mesh(
  //   new THREE.BoxGeometry(3.6, 2.65, 0.44),
  //   new THREE.MeshStandardMaterial({ map: murals.pencilGateTex, roughness: 0.72 })
  // );
  // pencilGatePanel.position.set(2.8, 1.35, 30.0);
  // pencilGatePanel.userData = { feature: 'pencil_main_gate', isSolidWall: true };
  // terrainGroup.add(pencilGatePanel);

  // Y-shaped security light post atop main gate pier (pip01b_01)
  const poleMat = new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.5 });
  const gPole = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.95, 8), poleMat);
  gPole.position.set(1.25, 3.15, 30.0);
  terrainGroup.add(gPole);

  // 7. Outer West Wall (X = -34.0) & North-West Rear Alley Wall (Z = -19.5, X = -34.0..+19.0)
  addCourtyardWall(wallT, wallH, 49.5, -34.0, wallH / 2, 5.25, wallMat, null, true);
  addCourtyardWall(53.0, wallH, wallT, -7.5, wallH / 2, -19.5, wallMat, null, true);

  // Close the notch at each outer corner where two courtyard walls meet end to end.
  for (const [id, ext] of cornerExtensions(courtyardWalls, wallT)) {
    const wall = courtyardWalls.find((c) => c.id === id);
    const [x1, z1] = wall.from;
    const [x2, z2] = wall.to;
    const len = Math.hypot(x2 - x1, z2 - z1);
    const ux = (x2 - x1) / len;
    const uz = (z2 - z1) / len;
    [['start', -1, x1, z1], ['end', 1, x2, z2]].forEach(([which, sign, ex, ez]) => {
      if (!(ext[which] > 0)) return;
      const along = wall.t < len && ux !== 0; // wall runs along X
      const cx = ex + sign * ux * ext[which] / 2;
      const cz = ez + sign * uz * ext[which] / 2;
      addCourtyardWall(along ? ext[which] : wall.t, wall.h, along ? wall.t : ext[which], cx, wall.y, cz, wall.mat, null, true);
      courtyardWalls.pop(); // caps are not walls to join
    });
  }

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

  // Makan Nasiri's Small Red-Soled Sneaker Resting on Red Roses at Base of Vow Shrine (Station 8 Tribute)
  const roseCaseGroup = new THREE.Group();
  roseCaseGroup.position.set(shrineX, 0.42, shrineZ + 1.55);
  const plinthBox = new THREE.Mesh(
    new THREE.BoxGeometry(0.76, 0.28, 0.54),
    new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.45, metalness: 0.35 })
  );
  plinthBox.position.y = -0.14;
  roseCaseGroup.add(plinthBox);
  const roseMat = new THREE.MeshStandardMaterial({ color: 0xbe123c, roughness: 0.65 });
  for (let rx = -0.24; rx <= 0.25; rx += 0.12) {
    for (let rz = -0.14; rz <= 0.15; rz += 0.14) {
      const rose = new THREE.Mesh(new THREE.DodecahedronGeometry(0.055, 0), roseMat);
      rose.position.set(rx, 0.04, rz);
      roseCaseGroup.add(rose);
    }
  }
  const sneakerSole = new THREE.Mesh(
    new THREE.BoxGeometry(0.22, 0.035, 0.095),
    new THREE.MeshStandardMaterial({ color: 0xdc2626, roughness: 0.6 })
  );
  sneakerSole.position.set(0, 0.09, 0);
  sneakerSole.rotation.y = 0.25;
  const sneakerUpper = new THREE.Mesh(
    new THREE.BoxGeometry(0.19, 0.075, 0.088),
    new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.72 })
  );
  sneakerUpper.position.set(-0.01, 0.135, 0);
  sneakerUpper.rotation.y = 0.25;
  const glassVitrine = new THREE.Mesh(
    new THREE.BoxGeometry(0.68, 0.26, 0.46),
    new THREE.MeshStandardMaterial({ color: 0xe0f2fe, transparent: true, opacity: 0.22, roughness: 0.15 })
  );
  glassVitrine.position.y = 0.13;
  roseCaseGroup.add(sneakerSole, sneakerUpper, glassVitrine);
  memorialBoardsGroup.add(roseCaseGroup);
}

export function buildProceduralSchoolModels() {
  const { preStrikeModelGroup, postStrikeModelGroup } = appState;
  const groundFloorGroup = new THREE.Group();
  groundFloorGroup.name = "Ground_Floor_Boys_School";
  const firstFloorGroup = new THREE.Group();
  firstFloorGroup.name = "First_Floor_Girls_School";
  const roofGroup = new THREE.Group();
  roofGroup.name = "Roof_And_Parapet";
  appState.groundFloorGroup = groundFloorGroup;
  appState.firstFloorGroup = firstFloorGroup;
  appState.roofGroup = roofGroup;

  preStrikeModelGroup.add(groundFloorGroup);
  preStrikeModelGroup.add(firstFloorGroup);
  preStrikeModelGroup.add(roofGroup);

  const floorH = 3.6;
  const murals = getSchoolMuralTextures();

  // Verified Materials from FA-121 Blueprints & On-Site Archive Photos
  const whiteWall = createPaintedPlasterMaterial(0xedeff2);
  const westGreyWall = createPaintedPlasterMaterial(0x9aa1aa);
  const floorGrey = new THREE.MeshStandardMaterial({ color: 0x9ca3af, roughness: 0.85 });
  const floorGreen = new THREE.MeshStandardMaterial({ color: 0x5c7a62, roughness: 0.80 });
  const floorBrown = new THREE.MeshStandardMaterial({ color: 0x9c7b56, roughness: 0.82 });
  const tealWall = createPaintedPlasterMaterial(0x4f8694);
  const rearTealExt = createPaintedPlasterMaterial(0x3b7687);
  const skyBlueWall = createPaintedPlasterMaterial(0x88b8cb);
  const mintGreenWall = createPaintedPlasterMaterial(0x9ec4a5);
  const yellowFacade = createPaintedPlasterMaterial(0xd8d278);
  const pinkWall = createPaintedPlasterMaterial(0xd4839d);
  // Sills, window mullions and trims are too narrow for a 2 m texture tile, so
  // they keep the flat whitewash colour.
  const trimWhiteMat = new THREE.MeshStandardMaterial({ color: 0xedeff2, roughness: 0.82 });
  const purpleDoorMat = new THREE.MeshStandardMaterial({ color: 0xd16b97, roughness: 0.52 }); // classroom doors are pink; the name is historical
  const pinkDoorMat = new THREE.MeshStandardMaterial({ color: 0xd16b97, roughness: 0.52 });
  const blueMetalMat = new THREE.MeshStandardMaterial({ color: 0x1d4ed8, roughness: 0.48, metalness: 0.25 });
  const terracottaStairMat = new THREE.MeshStandardMaterial({ color: 0xc98a86, roughness: 0.78 });
  const canopyGreenMat = new THREE.MeshStandardMaterial({ color: 0x7d9c78, roughness: 0.72 });
  const sunshadeMat = new THREE.MeshStandardMaterial({ color: 0xe2e6ec, roughness: 0.78 });
  const darkGlassMat = new THREE.MeshBasicMaterial({ color: 0x111827 });
  const brownDadoMat = createPaintedPlasterMaterial(0x78533a);
  // The flag goes on the yard-facing face only; every other face and the caps stay plain
  // whitewash. BoxGeometry material order is +X, -X, +Y, -Y, +Z, -Z.
  const porticoColMat = new THREE.MeshStandardMaterial({ map: murals.porticoColTex, roughness: 0.74 });
  const porticoColPlainMat = new THREE.MeshStandardMaterial({ color: 0xe7eaed, roughness: 0.74 });
  const porticoColMats = [
    porticoColPlainMat,
    porticoColPlainMat,
    porticoColPlainMat,
    porticoColPlainMat,
    porticoColMat,
    porticoColPlainMat,
  ];

  // All eight standing and surviving columns are identical, so one geometry serves them all.
  const porticoColGeo = new THREE.BoxGeometry(0.62, floorH, 0.62);

  function addPorticoColumn(group, x, y, z, extraData) {
    const col = new THREE.Mesh(porticoColGeo, porticoColMats);
    col.position.set(x, y, z);
    col.castShadow = true;
    col.receiveShadow = true;
    col.userData = Object.assign({ isSolidWall: true }, extraData || {});
    group.add(col);
    return col;
  }

  // Solid structural/partition wall helper (tracked for camera collision audit)
  function addSolidWall(group, w, h, d, x, y, z, mat, extraData) {
    const m = new THREE.Mesh(wallBoxGeometry(w, h, d, mat || whiteWall), mat || whiteWall);
    m.position.set(x, y, z);
    m.castShadow = true;
    m.receiveShadow = true;
    m.userData = Object.assign({ isSolidWall: true }, extraData || {});
    group.add(m);
    return m;
  }

  // One plaster finish for every ceiling: the underside of the first-floor slabs (ground-floor
  // ceiling) and of the roof slabs (first-floor ceiling), and the soffits under the stairs.
  // Undersides face away from the sun and the shadow-casting lights, so plain plaster would
  // render near black there; the emissive term (modulated by the plaster grain) keeps it a
  // clean light off-white without flattening the texture.
  const ceilingPlaster = createPaintedPlasterMaterial(0xe6e2dc);
  // Warm grey, matching the lit wall plaster; a cool emissive made ceilings look blue next to the walls.
  ceilingPlaster.emissive = new THREE.Color(0x938d85);
  ceilingPlaster.emissiveMap = ceilingPlaster.map;

  // Slab whose underside is the shared ceiling plaster; `topMat` finishes the top and the edges.
  // BoxGeometry material order is +X, -X, +Y, -Y, +Z, -Z, so the ceiling is index 3.
  function addCeilingSlab(group, w, h, d, x, y, z, topMat, extraData) {
    const mats = [topMat, topMat, topMat, ceilingPlaster, topMat, topMat];
    const m = new THREE.Mesh(plasterBoxGeometry(w, h, d), mats);
    m.position.set(x, y, z);
    m.castShadow = true;
    m.receiveShadow = true;
    if (extraData) m.userData = extraData;
    group.add(m);
    return m;
  }

  // Non-blocking slab, dado paint band, or trim helper
  function addSlabOrTrim(group, w, h, d, x, y, z, mat, extraData) {
    const m = new THREE.Mesh(wallBoxGeometry(w, h, d, mat || whiteWall), mat || whiteWall);
    m.position.set(x, y, z);
    m.castShadow = true;
    m.receiveShadow = true;
    if (extraData) m.userData = extraData;
    group.add(m);
    return m;
  }

  // Two-tone classroom partition helper (Sage lower dado + Pink upper wall, matching FA-121 1st Floor)
  // Signature pink classroom door + Dark Transom Window
  function addPurpleDoor(group, x, yBase, z, rotY, depth = 0.28, openTransom = false, width = 1.06) {
    const dGroup = new THREE.Group();
    dGroup.position.set(x, yBase, z);
    dGroup.rotation.y = rotY;
    // The leaf is 2 cm wider than the hole cut for it, so its edges sit inside the jambs.
    const door = new THREE.Mesh(new THREE.BoxGeometry(width + 0.04, 2.08, depth), purpleDoorMat);
    door.position.set(0, 1.04, 0);
    dGroup.add(door);
    // Doors in cut walls (see buildWalls) leave the transom as an open hole; doors set into
    // solid walls keep the dark pane.
    if (!openTransom) {
      const transom = new THREE.Mesh(new THREE.BoxGeometry(width, 0.50, depth + 0.01), darkGlassMat);
      transom.position.set(0, 2.38, 0);
      dGroup.add(transom);
    }
    group.add(dGroup);
  }

  // Recessed Dark-Glazed Exterior Window with White Mullions, Security Grille & Optional Sunshade Brow
  function addExteriorWindow(group, x, y, z, rotY, w, h, mullions, hasSunshade, depthOverride, openGlass = false) {
    const winGroup = new THREE.Group();
    winGroup.position.set(x, y, z);
    winGroup.rotation.y = rotY;
    winGroup.userData = { feature: 'exterior_window' };

    const d = depthOverride || 0.44;
    // `openGlass` is for windows whose hole is cut through the wall (see buildWalls): no pane is
    // drawn, so you see straight into the room. Windows set into solid walls keep the dark pane.
    if (!openGlass) {
      const glass = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), darkGlassMat);
      winGroup.add(glass);
    }

    // Slim frame set back inside the wall opening: every member is a shallow bar centred in
    // the wall's thickness, so nothing reaches either face of the wall.
    const barD = Math.min(d, 0.1);
    const sill = new THREE.Mesh(new THREE.BoxGeometry(w + 0.06, 0.05, barD), sunshadeMat);
    sill.position.set(0, -h / 2 - 0.01, 0);
    winGroup.add(sill);

    const head = new THREE.Mesh(new THREE.BoxGeometry(w + 0.04, 0.04, barD), trimWhiteMat);
    head.position.set(0, h / 2 + 0.01, 0);
    winGroup.add(head);

    // Vertical jambs at the left and right ends of the opening
    [-1, 1].forEach((side) => {
      const jamb = new THREE.Mesh(new THREE.BoxGeometry(0.04, h, barD), trimWhiteMat);
      jamb.position.set(side * (w / 2 - 0.02), 0, 0);
      winGroup.add(jamb);
    });

    const mCount = typeof mullions === 'number' ? mullions : 2;
    for (let i = 1; i <= mCount; i++) {
      const mx = -w / 2 + (w * i) / (mCount + 1);
      const bar = new THREE.Mesh(new THREE.BoxGeometry(0.03, h, barD), trimWhiteMat);
      bar.position.set(mx, 0, 0);
      winGroup.add(bar);
    }

    if (h >= 0.9) {
      const transBar = new THREE.Mesh(new THREE.BoxGeometry(w, 0.025, barD), trimWhiteMat);
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

  // SW Singing Boys' Green Carpet Classroom Floor. The room runs from the west wall (G-06) to the
  // corridor wall G-12 (x = -10.6) and from G-09 (z = -2.5) to the south facade (G-01, z = 2.4), so
  // the carpet covers all of it; its edges tuck into those walls.
  addSlabOrTrim(
    groundFloorGroup, 8.3, 0.03, 4.8, -14.75, 0.215, -0.1, floorGreen,
    { feature: 'sw_boys_green_carpet' }
  );
  // Exterior / partition thicknesses, still used by the first floor and the post-strike ruins.
  const extT = 0.34;
  const partT = 0.24;

  // 4-Column Front Portico (colX = [-6.8, -2.3, +2.3, +6.8], Z = +4.4) + Flat Canopy Slab
  for (const colX of [-6.8, -2.3, 2.3, 6.8]) {
    addPorticoColumn(groundFloorGroup, colX, floorH / 2, 4.4);
  }
  addCeilingSlab(groundFloorGroup, 16.0, 0.42, 2.45, 0.0, floorH + 0.21, 3.625, whiteWall);
  addCeilingSlab(groundFloorGroup, 14.4, 0.42, 1.95, 0.0, floorH + 0.21, 1.475, whiteWall);

  // =====================================================================
  // GROUND FLOOR WALLS — exterior envelope, facade finishes, windows, doors and interior
  // partitions all come from GROUND_FLOOR_WALLS (ground-floor-walls.js). Open the page with
  // ?walls=1 to see each wall's ID in the scene.
  // =====================================================================
  // Grille bars use the classroom-door pink (same material), so the window and the doors match.
  const pinkGrilleMat = purpleDoorMat;
  // Pink security-grilled inner window (Station 2 script: "calm teal-blue walls and pink window grilles")
  function addPinkGrilledRoomWindow(group, x, y, z, rotY, w, h) {
    const wg = new THREE.Group();
    wg.position.set(x, y, z);
    wg.rotation.y = rotY;
    // Door-pink frame and black glass (was white trim and sky-blue glass)
    const frame = new THREE.Mesh(new THREE.BoxGeometry(w + 0.12, h + 0.12, 0.06), purpleDoorMat);
    const pane = new THREE.Mesh(
      new THREE.PlaneGeometry(w, h),
      new THREE.MeshBasicMaterial({ color: 0x050507 })
    );
    pane.position.z = 0.035;
    wg.add(frame, pane);
    for (let gx = -w * 0.36; gx <= w * 0.37; gx += w * 0.24) {
      const vBar = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, h, 8), pinkGrilleMat);
      vBar.position.set(gx, 0, 0.055);
      wg.add(vBar);
    }
    [-h * 0.26, 0, h * 0.26].forEach((gy) => {
      const hBar = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, w, 8), pinkGrilleMat);
      hBar.rotation.z = Math.PI / 2;
      hBar.position.set(0, gy, 0.055);
      wg.add(hBar);
    });
    group.add(wg);
  }

  const groundWallCtx = {
    parents: { default: groundFloorGroup },
    height: floorH,
    thickness: 0.24,
    mats: {
      white: whiteWall,
      westGrey: westGreyWall,
      teal: tealWall,
      skyBlue: skyBlueWall,
      pink: pinkWall,
      rearTeal: rearTealExt,
      charcoal: new THREE.MeshStandardMaterial({ color: 0x333840, roughness: 0.85 }),
      cream: new THREE.MeshStandardMaterial({ color: 0xfef3c7, roughness: 0.80 }),
      yellowFacade,
      sunshade: sunshadeMat,
      purpleDoor: purpleDoorMat,
    },
    addWindow: (g, x, y, z, rotY, w, h, mullions, sunshade, depth) =>
      addExteriorWindow(g, x, y, z, rotY, w, h, mullions, sunshade, depth, true),
    addDoor: (g, x, yBase, z, rotY, depth, width) => addPurpleDoor(g, x, yBase, z, rotY, depth, true, width),
    addGrille: addPinkGrilledRoomWindow,
  };
  appState.wallRegistry = buildWalls(GROUND_FLOOR_WALLS, groundWallCtx);

  // C) Rainbow Stairwell props (X: -3.8..0.0, Z: -13.0..-8.2), open to the hall; its walls are G-22 / G-23.
  const rainbowStairGroup = new THREE.Group();
  rainbowStairGroup.name = "Enclosed_Rainbow_Stairwell";
  rainbowStairGroup.userData = { feature: 'enclosed_rainbow_stairwell' };

  // Split-level (switchback) stairwell. Two flights of 9 steps, side by side, meet at a half-landing
  // against the north wall; the rear exterior staircase enters that landing through a door in G-08.
  //   Flight A (east, x -0.41..1.09): hall, z = -8.6 -> -11.3, rises north to the half-landing.
  //   Half-landing (full width, z -11.3..-12.83) at STAIR_LANDING_Y, exactly half way up.
  //   Flight B (west, x -2.13..-0.63): rises south from the landing to the first-floor slab.
  //   A 0.22 m wall (x = -0.52) divides the flights.
  // Slab tops: ground 0.20 (slab centre 0.10, h 0.20), first floor 3.71 (slab centre 3.60, h 0.22).
  const STAIR_GROUND_Y = 0.2;
  const STAIR_FIRST_Y = floorH + 0.11;
  const STAIR_LANDING_Y = (STAIR_GROUND_Y + STAIR_FIRST_Y) / 2; // 1.955
  const STAIR_STEPS = 9;
  const STAIR_RISE = (STAIR_LANDING_Y - STAIR_GROUND_Y) / STAIR_STEPS; // 0.195 m
  const STAIR_RUN = 0.30;
  // Stairwell interior is x -2.13..1.09: two 1.5 m flights with a 0.22 m wall between them.
  // West wall G-22 / F-20 sits at x = -2.24, east wall G-23 / F-21 at x = 1.2.
  const STAIR_FLIGHT_W = 1.5;
  const STAIR_MID_X = -0.52; // centre of the dividing wall and of the landing
  const STAIR_LANDING_Z = -8.6 - STAIR_STEPS * STAIR_RUN; // -11.3: where flight A ends and flight B starts
  const STAIR_A_X = 0.34; // east flight, x -0.41..1.09
  const STAIR_B_X = -1.38; // west flight, x -2.13..-0.63

  // Rainbow treads — bottom 5 match narration: yellow, blue, pink, green, red
  const rainbowColors = [0xeab308, 0x3b82f6, 0xec4899, 0x22c55e, 0xef4444, 0x3b82f6, 0xef4444, 0x22c55e, 0xec4899];
  // Everything you see from underneath the stairs (soffits, landing blocks) uses the shared ceiling plaster.
  const stairUndersideMat = ceilingPlaster;

  // One flight: STAIR_STEPS rainbow step blocks (each exactly one riser tall) plus a flat white soffit panel
  // under the whole flight, so from below you see one white sloped surface instead of the steps.
  // The flight is 4 cm wider than the gap it fills, so its sides tuck 2 cm into the walls on both sides
  // instead of sharing a plane with them (that shared plane z-fought on the top step).
  function addStairFlight(x, startZ, dirZ, baseY, group = rainbowStairGroup, rise = STAIR_RISE) {
    const w = STAIR_FLIGHT_W + 0.04;
    for (let s = 0; s < STAIR_STEPS; s++) {
      const topY = baseY + (s + 1) * rise;
      const tread = new THREE.Mesh(
        new THREE.BoxGeometry(w, rise, STAIR_RUN),
        new THREE.MeshStandardMaterial({ color: rainbowColors[s], roughness: 0.48 })
      );
      tread.position.set(x, topY - rise / 2, startZ + dirZ * (s + 0.5) * STAIR_RUN);
      tread.castShadow = true;
      tread.receiveShadow = true;
      group.add(tread);
    }
    // Soffit: its visible underside is the plane through the lowest (back-bottom) corners of the
    // step blocks, so it touches every step instead of hanging below them. The slab is a box
    // sheared along the flight, which keeps both ends vertical: the low end meets the floor or
    // the half-landing block flush and the high end meets the next floor slab flush. (A tilted
    // box has slanted ends, which left slivers of tread and a white lip at the ceiling.)
    const planLen = STAIR_STEPS * STAIR_RUN;
    const slope = rise / STAIR_RUN;
    const thickness = rise * 0.9; // stays inside the step blocks at the back, so no coplanar faces
    const soffitGeo = wallBoxGeometry(w, thickness, planLen, stairUndersideMat);
    const lift = dirZ < 0 ? -slope : slope; // y rises toward the high end of the flight
    soffitGeo.applyMatrix4(new THREE.Matrix4().set(
      1, 0, 0, 0,
      0, 1, lift, 0,
      0, 0, 1, 0,
      0, 0, 0, 1
    ));
    soffitGeo.computeVertexNormals();
    const soffit = new THREE.Mesh(soffitGeo, stairUndersideMat);
    // Underside height at mid-flight is baseY - rise + 4.5 rise; the box centre sits half its thickness above it.
    soffit.position.set(x, baseY + (STAIR_STEPS / 2 - 1) * rise + thickness / 2, startZ + (dirZ * planLen) / 2);
    soffit.receiveShadow = true;
    group.add(soffit);
  }
  addStairFlight(STAIR_A_X, -8.6, -1, STAIR_GROUND_Y);
  addStairFlight(STAIR_B_X, STAIR_LANDING_Z, +1, STAIR_LANDING_Y);

  // Half-landing: a solid block from the ground slab up to STAIR_LANDING_Y across the full stairwell width.
  addSlabOrTrim(
    rainbowStairGroup, 3.22, STAIR_LANDING_Y - STAIR_GROUND_Y, 12.83 + STAIR_LANDING_Z,
    STAIR_MID_X, (STAIR_LANDING_Y + STAIR_GROUND_Y) / 2, (STAIR_LANDING_Z - 12.83) / 2, stairUndersideMat,
    { feature: 'stair_half_landing' }
  );

  // Dividing wall between the two flights, from the landing edge to the foot of flight A (ground to the first-floor slab).
  // The part above the first floor is a guard wall, added with the first-floor slabs below.
  const midWallLen = -8.6 - STAIR_LANDING_Z; // 2.7
  addSolidWall(
    rainbowStairGroup, 0.22, STAIR_FIRST_Y - STAIR_GROUND_Y, midWallLen,
    STAIR_MID_X, (STAIR_FIRST_Y + STAIR_GROUND_Y) / 2, STAIR_LANDING_Z + midWallLen / 2, whiteWall,
    { feature: 'stair_dividing_wall' }
  );

  groundFloorGroup.add(rainbowStairGroup);

  // =====================================================================
  // REAR EXTERIOR GIRLS' STAIRCASE, BLUE GATE & SLOPED GREEN CANOPY (M2 — ref_04a_rear_fa.jpg)
  // =====================================================================
  const rearStairGroup = new THREE.Group();
  rearStairGroup.name = "Rear_Exterior_Girls_Staircase_And_Canopy";
  rearStairGroup.userData = { feature: 'rear_girls_exterior_stairs' };

  // The staircase now ends at the half-landing door in the north wall (G-08 / F-08, x = -1.3), at
  // STAIR_LANDING_Y. From that door you see flight A going down to the hall and flight B going up.
  const REAR_DOOR_X = STAIR_MID_X;
  const REAR_ALLEY_Y = 0.02; // rear alley plane height
  const REAR_STEPS = 9;
  const REAR_RISE = (STAIR_LANDING_Y - REAR_ALLEY_Y) / REAR_STEPS; // ~0.215 m
  const REAR_RUN = 0.30;
  const REAR_W = 1.83;
  const REAR_LANDING_X0 = REAR_DOOR_X - 1.1; // landing spans x -2.4..-0.2
  const REAR_LANDING_Z = -13.17 - REAR_W / 2; // outer face of the 0.34 m wall -> 1.83 m deep

  // Outside landing in front of the door: solid pink block topped by a terracotta slab
  addSlabOrTrim(rearStairGroup, 2.2, STAIR_LANDING_Y - REAR_ALLEY_Y - 0.08, REAR_W, REAR_DOOR_X, (STAIR_LANDING_Y - 0.08 + REAR_ALLEY_Y) / 2, REAR_LANDING_Z, pinkWall);
  addSlabOrTrim(rearStairGroup, 2.2, 0.08, REAR_W, REAR_DOOR_X, STAIR_LANDING_Y - 0.04, REAR_LANDING_Z, terracottaStairMat);

  // 9 Terracotta-Pink Exterior Treads rising East toward the landing (X: -5.1 -> -2.4); the 9th is flush with it
  for (let rs = 0; rs < REAR_STEPS; rs++) {
    const topY = REAR_ALLEY_Y + (rs + 1) * REAR_RISE;
    const h = topY - REAR_ALLEY_Y;
    const tread = new THREE.Mesh(
      new THREE.BoxGeometry(REAR_RUN, h, REAR_W),
      terracottaStairMat
    );
    tread.position.set(REAR_LANDING_X0 - (REAR_STEPS - rs - 0.5) * REAR_RUN, REAR_ALLEY_Y + h / 2, REAR_LANDING_Z);
    tread.castShadow = true;
    tread.receiveShadow = true;
    rearStairGroup.add(tread);
  }

  // Open blue metal door in the half-landing doorway, hinged on the west jamb, swung out onto the landing
  const rearDoorPivot = new THREE.Group();
  rearDoorPivot.position.set(REAR_DOOR_X - 0.5, STAIR_LANDING_Y + 1.05, -13.2);
  rearDoorPivot.rotation.y = 1.9;
  const rearDoorLeaf = new THREE.Mesh(new THREE.BoxGeometry(1.0, 2.1, 0.06), blueMetalMat);
  rearDoorLeaf.position.set(0.5, 0, 0);
  rearDoorLeaf.castShadow = true;
  rearDoorPivot.add(rearDoorLeaf);
  rearStairGroup.add(rearDoorPivot);

  // Rear Alley Partition Wall (X = -3.8, Z = -19.5..-15.2) with Blue Metal Gate. The stairs now
  // run through its southern end (z -13..-15.2), so that stretch is gone.
  addSlabOrTrim(rearStairGroup, 0.26, 2.45, 1.175, -3.8, 1.225, -15.7875, pinkWall);
  const blueRearGate = new THREE.Mesh(new THREE.BoxGeometry(0.12, 2.35, 1.85), blueMetalMat);
  blueRearGate.position.set(-3.8, 1.18, -17.30);
  rearStairGroup.add(blueRearGate);
  addSlabOrTrim(rearStairGroup, 0.26, 2.45, 1.275, -3.8, 1.225, -18.8625, pinkWall);

  // Pitched / Sloped Green Corrugated Pre-School Canopy (X: +0.9..+11.5, Z: -18.6..-13.0, Y: 3.55 -> 2.85).
  // It starts east of the stair landing (x -1.62..0.58) so it does not cut across the new doorway.
  const slopedCanopy = new THREE.Mesh(new THREE.BoxGeometry(10.6, 0.12, 5.75), canopyGreenMat);
  slopedCanopy.position.set(6.2, 3.22, -15.82);
  slopedCanopy.rotation.x = -0.125;
  slopedCanopy.castShadow = true;
  rearStairGroup.add(slopedCanopy);

  const postSteelMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.5, metalness: 0.6 });
  [1.6, 6.4, 11.2].forEach((px) => {
    const post = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.055, 2.88, 8), postSteelMat);
    post.position.set(px, 1.44, -18.45);
    rearStairGroup.add(post);
  });
  groundFloorGroup.add(rearStairGroup);

  // =====================================================================
  // 2. FIRST FLOOR (GIRLS' PRIMARY SCHOOL — FA-121 Blueprint, ref_06_first_cutaway_fa.jpg)
  // =====================================================================
  const y1 = floorH;
  // Stepped First Floor Slabs (leaving stairwell opening at X: -3.8..0.0, Z: -13.0..-8.0)
  addCeilingSlab(firstFloorGroup, 7.5, 0.22, 15.4, -15.25, y1, -5.3, floorGreen); // West Girls' Assembly Hall
  addCeilingSlab(firstFloorGroup, 4.3, 0.22, 15.4, -9.35, y1, -5.3, floorGrey);
  addCeilingSlab(firstFloorGroup, 14.4, 0.22, 8.5, 0.0, y1, -3.75, floorGrey);
  addCeilingSlab(firstFloorGroup, 4.96, 0.22, 5.0, -4.72, y1, -10.5, floorGrey); // ends at X = -2.24, the stairwell west wall (G-22 / F-20)
  addCeilingSlab(firstFloorGroup, 7.3, 0.22, 5.0, 4.85, y1, -10.5, floorGrey); // starts at X = 1.2, the stairwell east wall (G-23 / F-21)
  // Stair arrival: flight B's top step ends at z = -8.6 (landing z -11.3 + 9 steps x 0.3 m) and the slab starts
  // exactly there; any overlap would z-fight with the step's top face.
  addCeilingSlab(firstFloorGroup, 3.44, 0.22, 0.6, -0.52, y1, -8.3, floorGrey);
  // Fills the gap between the central slab (ends z = -8.0 at x = 7.2) and the east-wing slab (starts z = -7.4)
  addCeilingSlab(firstFloorGroup, 1.3, 0.22, 0.6, 7.85, y1, -7.7, floorGrey);

  // Upper switchback to the roof, stacked over the lower one (same footprint, 9 + 9 steps):
  //   Flight C (east): from the first floor at z = -8.6, rises north to the upper half-landing.
  //   Flight D (west): from the landing, rises south to the roof slab at z = -8.6.
  // The stair-to-roof opening in the roof slab and the head-house over it are built with the roof below.
  const ROOF_TOP_Y = floorH * 2 + 0.3;
  const UP_LANDING_Y = (STAIR_FIRST_Y + ROOF_TOP_Y) / 2;
  const UP_RISE = (UP_LANDING_Y - STAIR_FIRST_Y) / STAIR_STEPS;
  const UP_LANDING_Z = -8.6 - STAIR_STEPS * STAIR_RUN; // -11.3
  addStairFlight(STAIR_A_X, -8.6, -1, STAIR_FIRST_Y, firstFloorGroup, UP_RISE);
  addStairFlight(STAIR_B_X, UP_LANDING_Z, +1, UP_LANDING_Y, firstFloorGroup, UP_RISE);
  // Upper half-landing: a slab only, so the rear door below keeps its full height
  addSlabOrTrim(firstFloorGroup, 3.22, 0.25, UP_LANDING_Z + 12.83, STAIR_MID_X, UP_LANDING_Y - 0.125, (UP_LANDING_Z - 12.83) / 2, stairUndersideMat, { feature: 'stair_upper_landing' });
  // Dividing wall between the upper flights, up to the roof
  // Ends 2 cm north of z = -8.6: flight C's first step is tucked 2 cm into this wall and its front face
  // at z = -8.6 would otherwise be coplanar with the wall's end face (z-fighting sliver).
  addSolidWall(
    firstFloorGroup, 0.22, ROOF_TOP_Y - STAIR_FIRST_Y, -8.62 - UP_LANDING_Z,
    STAIR_MID_X, (ROOF_TOP_Y + STAIR_FIRST_Y) / 2, (UP_LANDING_Z - 8.62) / 2, whiteWall,
    { feature: 'stair_upper_dividing_wall' }
  );
  addCeilingSlab(firstFloorGroup, 10.5, 0.22, 5.6, 13.75, y1, -10.2, floorBrown); // NE Rubble Archive Room (tan/brown floor)
  addCeilingSlab(firstFloorGroup, 11.8, 0.22, 9.8, 13.1, y1, -2.5, floorGrey);

  // First-floor walls, windows and doors all come from FIRST_FLOOR_WALLS (first-floor-walls.js),
  // built the same way as the ground floor so openings cut real holes through the walls.
  const firstFloorWallCtx = {
    ...groundWallCtx,
    parents: { default: firstFloorGroup },
  };
  appState.wallRegistry.push(...buildWalls(FIRST_FLOOR_WALLS, firstFloorWallCtx));

  // Sunshade slab above the east-wing windows
  addSlabOrTrim(firstFloorGroup, 7.2, 0.11, 0.52, 15.2, y1 + 3.12, 2.66, sunshadeMat);

  // Open Pink Double Doors swinging into Girls' Assembly Hall, in the F-09 gap (ref_06_first_cutaway_fa.jpg)
  const pinkDoorL = new THREE.Mesh(new THREE.BoxGeometry(0.92, 2.25, 0.10), pinkDoorMat);
  pinkDoorL.position.set(-11.95, y1 + 1.20, -6.35);
  pinkDoorL.rotation.y = 0.25;
  const pinkDoorR = new THREE.Mesh(new THREE.BoxGeometry(0.92, 2.25, 0.10), pinkDoorMat);
  pinkDoorR.position.set(-11.95, y1 + 1.20, -4.65);
  pinkDoorR.rotation.y = -0.25;
  firstFloorGroup.add(pinkDoorL, pinkDoorR);

  // =====================================================================
  // 3. STEPPED ROOF, PARAPET, STAIRWELL PENTHOUSE, SKYLIGHT & TELECOM MAST (M3)
  // =====================================================================
  const yRoof = floorH * 2;
  // Stepped Roof Slabs
  addCeilingSlab(roofGroup, 12.1, 0.30, 15.7, -13.15, yRoof + 0.15, -5.3, whiteWall);
  // Centre roof slab, with an opening over the stairwell (x -2.24..1.2, z -13.15..-8.6) where the roof stairs come out
  addCeilingSlab(roofGroup, 4.96, 0.30, 13.8, -4.72, yRoof + 0.15, -6.25, whiteWall);
  addCeilingSlab(roofGroup, 6.0, 0.30, 13.8, 4.2, yRoof + 0.15, -6.25, whiteWall);
  addCeilingSlab(roofGroup, 3.44, 0.30, 9.25, -0.52, yRoof + 0.15, -3.975, whiteWall);
  addCeilingSlab(roofGroup, 12.1, 0.30, 15.7, 13.15, yRoof + 0.15, -5.3, whiteWall);

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

  // Stairwell head-house over the roof opening: side walls and a flat cap, open to the south where the
  // stairs come out. Walls stand on the stairwell walls below (x = -2.24 and x = 1.2).
  const headH = 2.3;
  addSlabOrTrim(roofGroup, 0.22, headH, 4.4, -2.24, ROOF_TOP_Y + headH / 2, -10.8, whiteWall);
  addSlabOrTrim(roofGroup, 0.22, headH, 4.4, 1.2, ROOF_TOP_Y + headH / 2, -10.8, whiteWall);
  addSlabOrTrim(roofGroup, 3.66, 0.25, 4.4, -0.52, ROOF_TOP_Y + headH + 0.125, -10.8, whiteWall);
  // Closed north end of the head-house. Without it, looking up the stairwell from the first-floor hall showed
  // sky through the open north face above the parapet (8.15..9.8 m). It starts at the roof slab's underside
  // (7.2 m, not 7.5) so there is no 0.3 m slot under it where the F-08 wall top (7.2) ends. It sits between the side walls (3.26 m,
  // tucked 2 cm into each) and 2 cm in from their north faces, so no faces are coplanar. South stays open.
  addSlabOrTrim(roofGroup, 3.26, headH + 0.3, 0.20, -0.52, ROOF_TOP_Y - 0.3 + (headH + 0.3) / 2, -12.88, whiteWall);
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

  // Surviving East Wing exteriors. These must match the pre-strike east wing exactly, so the
  // ground floor is built from the same wall data (G-04, G-05, G-07 and the east end of G-08)
  // and the first floor repeats the pre-strike first-floor walls and windows.
  const northDef = GROUND_FLOOR_WALLS.find((d) => d.id === 'G-08');
  const NORTH_CLIP_X = 4.5; // the ruined centre bay starts west of this
  const eastNorthDef = {
    ...northDef,
    id: 'G-08E',
    from: [NORTH_CLIP_X, -13.0],
    liners: [],
    openings: northDef.openings
      .map((op) => ({ ...op, at: op.at - (NORTH_CLIP_X - northDef.from[0]) }))
      .filter((op) => op.at > 0),
  };
  buildWalls(
    [...GROUND_FLOOR_WALLS.filter((d) => ['G-04', 'G-05', 'G-07'].includes(d.id)), eastNorthDef],
    { ...groundWallCtx, parents: { default: postStrikeModelGroup } }
  );

  // First floor of the surviving east wing: same wall data as the intact building.
  const firstNorth = FIRST_FLOOR_WALLS.find((d) => d.id === 'F-08');
  const firstNorthEast = {
    ...firstNorth,
    id: 'F-08E',
    from: [NORTH_CLIP_X, -13.0],
    openings: firstNorth.openings
      .map((op) => ({ ...op, at: op.at - (NORTH_CLIP_X - firstNorth.from[0]) }))
      .filter((op) => op.at > op.w / 2),
  };
  buildWalls(
    [...FIRST_FLOOR_WALLS.filter((d) => ['F-04', 'F-05', 'F-07'].includes(d.id)), firstNorthEast],
    { ...firstFloorWallCtx, parents: { default: postStrikeModelGroup } }
  );
  addSlabOrTrim(postStrikeModelGroup, 7.2, 0.11, 0.52, 15.2, y1 + 3.12, 2.66, sunshadeMat);

  // East-wing interior walls and doors survive; anything at or west of X = 4.5 is the impact zone
  // and stays destroyed. Walls that run across X = 4.5 are cut off there.
  const EAST_WING_X = 4.5;
  const clipFromX = (def) => {
    const cut = EAST_WING_X - def.from[0];
    if (cut <= 0) return def;
    return {
      ...def,
      from: [EAST_WING_X, def.from[1]],
      openings: (def.openings || [])
        .map((op) => ({ ...op, at: op.at - cut }))
        .filter((op) => op.at - (op.w ?? 1.06) / 2 > 0),
    };
  };
  buildWalls(
    ['G-24', 'G-25', 'G-26', 'G-27', 'G-28', 'G-29', 'G-30']
      .map((id) => clipFromX(GROUND_FLOOR_WALLS.find((d) => d.id === id))),
    { ...groundWallCtx, parents: { default: postStrikeModelGroup } }
  );
  buildWalls(
    ['F-10', 'F-16', 'F-17', 'F-23', 'F-26', 'F-27']
      .map((id) => clipFromX(FIRST_FLOOR_WALLS.find((d) => d.id === id))),
    { ...firstFloorWallCtx, parents: { default: postStrikeModelGroup } }
  );

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
    addPorticoColumn(postStrikeModelGroup, colX, floorH / 2, 4.4, { feature: 'post_portico_col' });
  }
  addSlabOrTrim(postStrikeModelGroup, 15.6, 0.40, 2.45, 0.2, floorH + 0.20, 3.625, whiteWall);
  addSlabOrTrim(postStrikeModelGroup, 11.8, 0.40, 1.95, 1.3, floorH + 0.20, 1.475, whiteWall);
  // Standing shattered central front facade wall shell with open sky behind broken window frame (ref_02b left side!)
  // Ground-floor stretch of the central front wall (X = -2.6..7.2) keeps its entrance doorway
  const groundFront = GROUND_FLOOR_WALLS.find((d) => d.id === 'G-03');
  const frontCut = -2.6 - groundFront.from[0];
  buildWalls(
    [{
      ...groundFront,
      id: 'G-03E',
      from: [-2.6, 0.5],
      liners: groundFront.liners.map((l) => ({ ...l, from: Math.max(0, l.from - frontCut), to: l.to - frontCut })),
      openings: groundFront.openings
        .map((op) => ({ ...op, at: op.at - frontCut }))
        .filter((op) => op.at - (op.w ?? 1.06) / 2 > 0),
    }],
    { ...groundWallCtx, parents: { default: postStrikeModelGroup } }
  );
  addSlabOrTrim(postStrikeModelGroup, 1.6, 2.7, 0.34, -4.2, y1 + 1.35, 0.5, whiteWall);
  addSlabOrTrim(postStrikeModelGroup, 1.6, 2.5, 0.34, -1.2, y1 + 1.25, 0.5, whiteWall);
  addSlabOrTrim(postStrikeModelGroup, 3.4, 0.65, 0.34, -2.7, y1 + 2.35, 0.5, whiteWall);
  // Surviving first-floor stretch of the central front wall (X = 1.4..7.2), with F-03's window cut through it
  const frontWall = FIRST_FLOOR_WALLS.find((d) => d.id === 'F-03');
  buildWalls(
    [{
      ...frontWall,
      id: 'F-03E',
      from: [1.4, 0.5],
      openings: frontWall.openings
        .map((op) => ({ ...op, at: op.at - (1.4 - frontWall.from[0]) }))
        .filter((op) => op.at - op.w / 2 > 0),
    }],
    { ...firstFloorWallCtx, parents: { default: postStrikeModelGroup } }
  );

  // D) Sunken Rubble-Lined 5-Meter Blast Crater Pit at (-2.5, 0, -5.5) + Forensic Scale Rings & Plaque
  const craterPitFloor = new THREE.Mesh(
    new THREE.CircleGeometry(2.52, 32),
    new THREE.MeshStandardMaterial({ color: 0x1c1a18, roughness: 1.0 })
  );
  craterPitFloor.rotation.x = -Math.PI / 2;
  craterPitFloor.position.set(-2.5, 0.06, -5.5);
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
  const CRATER_EN_TEXT = 'Ø 5.0 m IMPACT CRATER · CENTRAL HALL';
  const CRATER_FA_TEXT = 'قطر دهانه گودال انفجار: ۵ متر (مرکز سالن مدرسه)';
  const drawCraterLabels = () => {
    // Clear and repaint the background first so a font-ready repaint does not overlap glyphs.
    sCtx.clearRect(0, 0, 512, 88);
    sCtx.fillStyle = 'rgba(15, 18, 28, 0.92)';
    sCtx.fillRect(0, 0, 512, 88);
    sCtx.strokeStyle = '#ef4444';
    sCtx.lineWidth = 4;
    sCtx.strokeRect(2, 2, 508, 84);
    sCtx.textAlign = 'center';
    sCtx.direction = 'ltr';
    sCtx.fillStyle = '#fca5a5';
    sCtx.font = `700 22px ${EN_CANVAS_FONT}`;
    sCtx.fillText(CRATER_EN_TEXT, 256, 36);

    sCtx.direction = 'rtl';
    sCtx.fillStyle = '#fef2f2';
    let faPx = 21;
    sCtx.font = `700 ${faPx}px ${FA_CANVAS_FONT}`;
    // Vazirmatn runs wider than the fallback face on this single unwrapped line.
    while (faPx > 15 && sCtx.measureText(CRATER_FA_TEXT).width > 472) {
      faPx -= 1;
      sCtx.font = `700 ${faPx}px ${FA_CANVAS_FONT}`;
    }
    sCtx.fillText(CRATER_FA_TEXT, 256, 68);
  };
  drawCraterLabels();
  const scaleTex = canvasColorTexture(scaleCanvas);
  repaintCanvasWhenFontsReady(
    [
      { font: `700 22px ${EN_CANVAS_FONT}`, text: 'IMPACT' },
      { font: `700 21px ${FA_CANVAS_FONT}`, text: 'قطر' },
    ],
    () => {
      drawCraterLabels();
      scaleTex.needsUpdate = true;
    }
  );
  const scaleBadge = new THREE.Mesh(
    new THREE.PlaneGeometry(3.6, 3.6 * (88 / 512)),
    new THREE.MeshBasicMaterial({ map: scaleTex, side: THREE.DoubleSide })
  );
  // Station 6: the crater banner sits on top of tour frame 06_A (x = 2.95, centre y = 2.53, h = 2.02,
  // top edge near y = 3.6), same width as the frame, facing west. It used to float over the crater
  // on a leader line; the line is gone because the banner no longer sits above the crater.
  scaleBadge.position.set(2.93, 4.0, -4.45);
  scaleBadge.rotation.y = -Math.PI / 2;
  postStrikeModelGroup.add(scaleBadge);

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
    [2.4, -6.2, 2.2, 0.32, 1.7, -0.35, 1.1, 0.30]
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
    // polygonOffset pushes the tint behind coplanar opaque surfaces (slab tops/undersides, parapet and
    // wall faces) so it cannot z-fight with them; it draws after all opaque geometry.
    new THREE.MeshBasicMaterial({
      color: 0xe5e059, transparent: true, opacity: 0.08, depthWrite: false, side: THREE.DoubleSide,
      polygonOffset: true, polygonOffsetFactor: 2, polygonOffsetUnits: 4
    })
  );
  dmgFill.renderOrder = 10;
  // Lifted off the ground plane so its bottom face does not z-fight with it.
  dmgFill.position.y = 0.05;
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

  // G) Dust-Covered Pastel Schoolbags & Shrapnel-Pierced Homework Sheets in Rubble around 5m Crater (Station 6 script)
  const dustyBagPalette = [0xc08497, 0x7ea8be, 0xcab87a, 0x8fb399, 0xb88ca8];
  [
    [-4.6, 0.44, -4.8, 0.5],
    [-3.4, 0.42, -3.1, -0.4],
    [-1.3, 0.44, -3.2, 0.8],
    [0.3, 0.46, -4.5, -0.7],
    [-1.8, 0.40, -7.1, 0.3]
  ].forEach(([bx, by, bz, brot], idx) => {
    const dBag = new THREE.Mesh(
      new THREE.BoxGeometry(0.32, 0.22, 0.25),
      new THREE.MeshStandardMaterial({ color: dustyBagPalette[idx], roughness: 0.92 })
    );
    dBag.position.set(bx, by, bz);
    dBag.rotation.set(0.25, brot, -0.18);
    dBag.castShadow = true;
    postStrikeModelGroup.add(dBag);
  });
  [
    [-3.9, 0.36, -3.8, 0.4], [-2.6, 0.35, -2.9, -0.5], [-0.8, 0.36, -3.6, 0.9],
    [0.5, 0.38, -5.2, -0.3], [-1.1, 0.35, -6.5, 0.2], [-3.1, 0.34, -6.8, 1.1]
  ].forEach(([px, py, pz, prot]) => {
    const tornPage = new THREE.Mesh(
      new THREE.PlaneGeometry(0.30, 0.22),
      new THREE.MeshBasicMaterial({ color: 0xe7e5e4, side: THREE.DoubleSide })
    );
    tornPage.rotation.x = -Math.PI / 2 + 0.08;
    tornPage.rotation.z = prot;
    tornPage.position.set(px, py, pz);
    postStrikeModelGroup.add(tornPage);
  });

  // I) Mount All 16 Verified 1080p Pre-Strike & Incident Videos/Photos Directly Inside the 3D School Architecture
  buildAllInWorldWalkthroughScreens();
}

export function setCutawayMode(mode) {
  appState.cutawayState = ((mode % 3) + 3) % 3;
  const { cutawayState, roofGroup, firstFloorGroup, groundFloorGroup, currentLang } = appState;
  const btn = typeof document !== 'undefined' ? document.getElementById('btnCutaway') : null;
  // Roof/floor visibility changes what casts shadow; the sun shadow map is static otherwise.
  if (appState.sunLight) appState.sunLight.shadow.needsUpdate = true;

  if (cutawayState === 0) {
    if (roofGroup) roofGroup.visible = true;
    if (firstFloorGroup) firstFloorGroup.visible = true;
    if (groundFloorGroup) groundFloorGroup.visible = true;
    if (btn) {
      btn.textContent =
        currentLang === 'fa'
          ? '🏠 برش طبقات: نمای کامل'
          : currentLang === 'fi'
            ? '🏠 Leikkaus: Koko rakennus'
            : '🏠 Floorplan Cutaway: Full Building';
    }
  } else if (cutawayState === 1) {
    if (roofGroup) roofGroup.visible = false;
    if (firstFloorGroup) firstFloorGroup.visible = true;
    if (groundFloorGroup) groundFloorGroup.visible = true;
    if (btn) {
      btn.textContent =
        currentLang === 'fa'
          ? '🏠 برش طبقات: طبقه اول (دبستان دخترانه)'
          : currentLang === 'fi'
            ? '🏠 Leikkaus: 2. kerros (Tytöt)'
            : '🏠 Cutaway: 1st Floor (Girls\' School)';
    }
  } else {
    if (roofGroup) roofGroup.visible = false;
    if (firstFloorGroup) firstFloorGroup.visible = false;
    if (groundFloorGroup) groundFloorGroup.visible = true;
    if (btn) {
      btn.textContent =
        currentLang === 'fa'
          ? '🏠 برش طبقات: طبقه همکف (دبستان پسرانه)'
          : currentLang === 'fi'
            ? '🏠 Leikkaus: 1. kerros (Pojat)'
            : '🏠 Cutaway: Ground Floor (Boys\' School)';
    }
  }
}
