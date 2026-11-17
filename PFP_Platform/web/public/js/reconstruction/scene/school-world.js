/**
 * Procedural Minab courtyard murals, terrain, Vow Shrine obelisk,
 * and two-floor Shajareh Tayyebeh school pre/post-strike 3D architecture.
 */
import * as THREE from 'three';

import { appState } from '../state.js';
import { buildAllInWorldWalkthroughScreens } from './in-world-screens.js';
import {
  createPaintedPlasterMaterial,
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
  const eastMuralTex = canvasColorTexture(eastCanvas);

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
  const yellowTulipTex = canvasColorTexture(tulipCanvas);

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
  const drawGateLetters = () => {
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
  const dinoWallTex = canvasColorTexture(dinoCanvas);

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
  const eastTreeMuralTex = canvasColorTexture(treeMuralCanvas);

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
  const scorchTex = canvasColorTexture(scorchCanvas);

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

  // Children's Morning Schoolbags resting beside the yellow standing circles (matching Station 1 script)
  const bagColors = [0xf472b6, 0x38bdf8, 0xfacc15, 0x34d399];
  [-3.5, -2.1, -0.7, 0.7].forEach((lz, bIdx) => {
    const bagGrp = new THREE.Group();
    bagGrp.position.set(-7.18, 0.0, lz + 0.22);
    bagGrp.rotation.y = 0.35 + (bIdx % 2) * 0.28;
    const bagMat = new THREE.MeshStandardMaterial({ color: bagColors[bIdx], roughness: 0.65 });
    const pocketMat = new THREE.MeshStandardMaterial({ color: 0xfef3c7, roughness: 0.72 });
    const body = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.36, 0.17), bagMat);
    body.position.y = 0.18;
    body.castShadow = true;
    const pocket = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.16, 0.05), pocketMat);
    pocket.position.set(0, 0.12, 0.10);
    bagGrp.add(body, pocket);
    assemblyGroup.add(bagGrp);
  });
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
  const wallMat = createPaintedPlasterMaterial(0xe2e6ec);
  const wallH = 2.65;
  const wallT = 0.36;

  function addCourtyardWall(w, h, d, x, y, z, mat, featureTag, isSolid = true) {
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
  const floorLilac = new THREE.MeshStandardMaterial({ color: 0xa5a1bd, roughness: 0.82 });
  const tealWall = createPaintedPlasterMaterial(0x4f8694);
  const rearTealExt = createPaintedPlasterMaterial(0x3b7687);
  const skyBlueWall = createPaintedPlasterMaterial(0x88b8cb);
  const mintGreenWall = createPaintedPlasterMaterial(0x9ec4a5);
  const yellowFacade = createPaintedPlasterMaterial(0xd8d278);
  const pinkWall = createPaintedPlasterMaterial(0xd4839d);
  const sageGreenWall = createPaintedPlasterMaterial(0x7fa382);
  // Sills, window mullions and trims are too narrow for a 2 m texture tile, so
  // they keep the flat whitewash colour.
  const trimWhiteMat = new THREE.MeshStandardMaterial({ color: 0xedeff2, roughness: 0.82 });
  const purpleDoorMat = new THREE.MeshStandardMaterial({ color: 0x8b4ca8, roughness: 0.50 });
  const pinkDoorMat = new THREE.MeshStandardMaterial({ color: 0xd16b97, roughness: 0.52 });
  const blueMetalMat = new THREE.MeshStandardMaterial({ color: 0x1d4ed8, roughness: 0.48, metalness: 0.25 });
  const terracottaStairMat = new THREE.MeshStandardMaterial({ color: 0xc98a86, roughness: 0.78 });
  const canopyGreenMat = new THREE.MeshStandardMaterial({ color: 0x7d9c78, roughness: 0.72 });
  const sunshadeMat = new THREE.MeshStandardMaterial({ color: 0xe2e6ec, roughness: 0.78 });
  const darkGlassMat = new THREE.MeshBasicMaterial({ color: 0x111827 });
  const eastMuralMat = new THREE.MeshStandardMaterial({ map: murals.eastMuralTex, roughness: 0.76 });
  const dinoMuralMat = new THREE.MeshStandardMaterial({ map: murals.dinoWallTex, roughness: 0.78 });
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

    const head = new THREE.Mesh(new THREE.BoxGeometry(w + 0.10, 0.06, d + 0.03), trimWhiteMat);
    head.position.set(0, h / 2 + 0.02, 0);
    winGroup.add(head);

    const mCount = typeof mullions === 'number' ? mullions : 2;
    for (let i = 1; i <= mCount; i++) {
      const mx = -w / 2 + (w * i) / (mCount + 1);
      const bar = new THREE.Mesh(new THREE.BoxGeometry(0.055, h, d + 0.03), trimWhiteMat);
      bar.position.set(mx, 0, 0);
      winGroup.add(bar);
    }

    if (h >= 0.9) {
      const transBar = new THREE.Mesh(new THREE.BoxGeometry(w, 0.045, d + 0.03), trimWhiteMat);
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
    addPorticoColumn(groundFloorGroup, colX, floorH / 2, 4.4);
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

  // 12 Rainbow Treads rising North (Z: -8.35..-12.55, Y: 0.32..3.52) — bottom 5 match narration: yellow, blue, pink, green, red
  const rainbowColors = [
    0xeab308, 0x3b82f6, 0xec4899, 0x22c55e, 0xef4444, 0x3b82f6,
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
  const dadoSlope = new THREE.Mesh(wallBoxGeometry(0.05, 1.15, 4.4, brownDadoMat), brownDadoMat);
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

  // Colorful 3D Paper Flowers rising along both stairwell walls (Station 4 script)
  const flowerPalette = [0xf472b6, 0xfacc15, 0x38bdf8, 0xfb7185, 0x4ade80, 0xc084fc];
  for (let f = 0; f < 8; f++) {
    const fz = -8.55 - f * 0.48;
    const fy = 1.15 + f * 0.28;
    const fMat = new THREE.MeshBasicMaterial({ color: flowerPalette[f % flowerPalette.length] });
    const centerMat = new THREE.MeshBasicMaterial({ color: 0xfef08a });
    [-3.66, -0.10].forEach((fx, sideIdx) => {
      const fGrp = new THREE.Group();
      fGrp.position.set(fx, fy, fz);
      fGrp.rotation.y = sideIdx === 0 ? Math.PI / 2 : -Math.PI / 2;
      for (let p = 0; p < 5; p++) {
        const ang = (p / 5) * Math.PI * 2;
        const petal = new THREE.Mesh(new THREE.CircleGeometry(0.075, 12), fMat);
        petal.position.set(Math.cos(ang) * 0.085, Math.sin(ang) * 0.085, 0.005);
        fGrp.add(petal);
      }
      const core = new THREE.Mesh(new THREE.CircleGeometry(0.045, 12), centerMat);
      core.position.z = 0.01;
      fGrp.add(core);
      rainbowStairGroup.add(fGrp);
    });
  }

  // Welcoming Tray of Sweets on Small Stand + Parastesh's Fallen Schoolbooks at Foot of Rainbow Stairs (Station 4 script)
  const sweetStand = new THREE.Mesh(
    new THREE.CylinderGeometry(0.24, 0.20, 0.72, 14),
    new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.6 })
  );
  sweetStand.position.set(-2.78, 0.56, -8.02);
  const sweetTray = new THREE.Mesh(
    new THREE.CylinderGeometry(0.28, 0.24, 0.04, 18),
    new THREE.MeshStandardMaterial({ color: 0xd4a853, metalness: 0.65, roughness: 0.3 })
  );
  sweetTray.position.set(-2.78, 0.94, -8.02);
  rainbowStairGroup.add(sweetStand, sweetTray);
  for (let sw = 0; sw < 7; sw++) {
    const swAng = (sw / 7) * Math.PI * 2;
    const candy = new THREE.Mesh(
      new THREE.SphereGeometry(0.036, 8, 8),
      new THREE.MeshStandardMaterial({ color: flowerPalette[sw % flowerPalette.length], roughness: 0.4 })
    );
    candy.position.set(-2.78 + Math.cos(swAng) * 0.12, 0.975, -8.02 + Math.sin(swAng) * 0.12);
    rainbowStairGroup.add(candy);
  }

  // Parastesh's Schoolbooks & Colored Pencils at Foot of Rainbow Stairs
  [
    [-1.48, 0.225, -7.88, 0.24, 0x38bdf8],
    [-1.18, 0.225, -7.76, -0.38, 0xf472b6],
    [-1.32, 0.252, -7.92, 0.62, 0xfacc15]
  ].forEach(([bx, by, bz, brot, bcol]) => {
    const bk = new THREE.Mesh(
      new THREE.BoxGeometry(0.26, 0.028, 0.19),
      new THREE.MeshStandardMaterial({ color: bcol, roughness: 0.65 })
    );
    bk.position.set(bx, by, bz);
    bk.rotation.y = brot;
    rainbowStairGroup.add(bk);
  });
  groundFloorGroup.add(rainbowStairGroup);

  // D) East Wing Classrooms, Boys' Flower Arch Ceremony Room & NE Pre-School Suite
  addSolidWall(groundFloorGroup, 7.48, floorH, partT, 3.76, floorH / 2, -3.6, tealWall);
  addSolidWall(groundFloorGroup, 7.48, floorH, partT, 3.76, floorH / 2, -8.4, tealWall);
  addSolidWall(groundFloorGroup, partT, floorH, 8.9, 7.5, floorH / 2, -3.95, tealWall);
  // Calm teal inner wall finish on West wall of Ceremony Room (X = 0.14)
  addSlabOrTrim(groundFloorGroup, 0.03, floorH - 0.15, 4.54, 0.145, floorH / 2, -6.0, tealWall);
  addPurpleDoor(groundFloorGroup, 7.5, 0.2, -6.0, -Math.PI / 2);

  // Pink Window Security Grilles inside Boys' Ceremony Room (matching Station 2 script: "calm teal-blue walls and pink window grilles")
  const pinkGrilleMat = new THREE.MeshStandardMaterial({ color: 0xf472b6, roughness: 0.45, metalness: 0.35 });
  function addPinkGrilledRoomWindow(x, y, z, rotY, w, h) {
    const wg = new THREE.Group();
    wg.position.set(x, y, z);
    wg.rotation.y = rotY;
    const frame = new THREE.Mesh(new THREE.BoxGeometry(w + 0.12, h + 0.12, 0.06), trimWhiteMat);
    const pane = new THREE.Mesh(
      new THREE.PlaneGeometry(w, h),
      new THREE.MeshBasicMaterial({ color: 0xbae6fd })
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
    groundFloorGroup.add(wg);
  }
  addPinkGrilledRoomWindow(7.35, 1.86, -7.35, -Math.PI / 2, 1.25, 1.05);
  addPinkGrilledRoomWindow(0.17, 1.86, -4.62, Math.PI / 2, 1.18, 1.02);

  // Two Decorative Red-Rose Ceremony Arches inside Boys' Ceremony Room (centered on X = 3.62 clear of stairwell wall at X = 2.62 & door at X = 5.2)
  [-5.65, -7.15].forEach((az) => {
    const archTorus = new THREE.Mesh(
      new THREE.TorusGeometry(1.34, 0.095, 12, 28, Math.PI),
      new THREE.MeshStandardMaterial({ color: 0xbe123c, roughness: 0.62 })
    );
    archTorus.position.set(3.62, 1.44, az);
    groundFloorGroup.add(archTorus);
    // Individual red roses & green leaves along the arch
    for (let ra = 0.12; ra <= Math.PI - 0.12; ra += 0.28) {
      const blossom = new THREE.Mesh(
        new THREE.DodecahedronGeometry(0.082, 0),
        new THREE.MeshStandardMaterial({ color: 0xe11d48, roughness: 0.55 })
      );
      blossom.position.set(3.62 + Math.cos(ra) * 1.34, 1.44 + Math.sin(ra) * 1.34, az + 0.06);
      groundFloorGroup.add(blossom);
    }
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

  // Sky-Blue Inner South Wall + Paper Hot-Air Balloons & Colorful Paper Crayons inside SW Boys' Classroom (Station 3 script)
  const creamDadoMat = new THREE.MeshStandardMaterial({ color: 0xfef3c7, roughness: 0.80 });
  addSlabOrTrim(groundFloorGroup, 6.08, 1.02, 0.03, -15.76, 0.72, 2.21, creamDadoMat);
  addSlabOrTrim(groundFloorGroup, 6.08, 2.28, 0.03, -15.76, 2.37, 2.21, skyBlueWall);

  // Handmade Paper Hot-Air Balloons & Colorful Crayons placed on sky-blue classroom walls
  function addPaperBalloonAndCrayons(group, x, y, z, rotY) {
    const decoGrp = new THREE.Group();
    decoGrp.position.set(x, y, z);
    decoGrp.rotation.y = rotY;
    [
      [-0.65, 0.22, 0xf43f5e, 0xfacc15],
      [0.0, 0.34, 0x38bdf8, 0xf472b6],
      [0.62, 0.18, 0x4ade80, 0xfb923c]
    ].forEach(([bx, by, c1, c2]) => {
      const balloon = new THREE.Mesh(new THREE.CircleGeometry(0.22, 20), new THREE.MeshBasicMaterial({ color: c1 }));
      balloon.position.set(bx, by, 0.01);
      const stripe = new THREE.Mesh(new THREE.PlaneGeometry(0.14, 0.38), new THREE.MeshBasicMaterial({ color: c2 }));
      stripe.position.set(bx, by, 0.015);
      const basket = new THREE.Mesh(new THREE.PlaneGeometry(0.11, 0.09), new THREE.MeshBasicMaterial({ color: 0xb45309 }));
      basket.position.set(bx, by - 0.31, 0.012);
      decoGrp.add(balloon, stripe, basket);
    });
    const crayonCols = [0xef4444, 0xf97316, 0xeab308, 0x22c55e, 0x3b82f6, 0xa855f7];
    crayonCols.forEach((cc, idx) => {
      const cx = -0.72 + idx * 0.28;
      const cy = -0.34;
      const cBody = new THREE.Mesh(new THREE.PlaneGeometry(0.11, 0.36), new THREE.MeshBasicMaterial({ color: cc }));
      cBody.position.set(cx, cy, 0.012);
      const cTip = new THREE.Mesh(new THREE.ConeGeometry(0.056, 0.11, 3), new THREE.MeshBasicMaterial({ color: cc }));
      cTip.position.set(cx, cy + 0.235, 0.012);
      cTip.rotation.y = Math.PI / 6;
      decoGrp.add(cBody, cTip);
    });
    group.add(decoGrp);
  }
  addPaperBalloonAndCrayons(groundFloorGroup, -17.15, 1.62, 2.18, Math.PI);
  addPaperBalloonAndCrayons(groundFloorGroup, -12.76, 1.66, -1.48, -Math.PI / 2);

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

  // Soft-Pink & Light-Green Wall Trim + Open Homework Notebooks & Colored Pencils on Girls' Upper Hall Carpet (Station 5 script)
  addSlabOrTrim(firstFloorGroup, 0.04, 0.38, 14.8, -18.80, y1 + 2.85, -5.3, pinkWall);
  addSlabOrTrim(firstFloorGroup, 0.04, 0.38, 14.8, -11.65, y1 + 2.85, -5.3, sageGreenWall);
  const notebookSpecs = [
    [-16.1, -8.4, 0.22, 0xf472b6], [-15.3, -8.6, -0.18, 0x38bdf8],
    [-14.4, -8.3, 0.35, 0x4ade80], [-16.0, -7.4, -0.28, 0xfacc15],
    [-15.1, -7.5, 0.14, 0xc084fc], [-14.3, -7.2, -0.32, 0xfb7185],
    [-15.7, -6.5, 0.40, 0x38bdf8], [-14.8, -6.4, -0.15, 0xf472b6]
  ];
  notebookSpecs.forEach(([nx, nz, nrot, coverCol]) => {
    const nbGrp = new THREE.Group();
    nbGrp.position.set(nx, y1 + 0.125, nz);
    nbGrp.rotation.y = nrot;
    const cover = new THREE.Mesh(
      new THREE.BoxGeometry(0.36, 0.016, 0.25),
      new THREE.MeshStandardMaterial({ color: coverCol, roughness: 0.7 })
    );
    const pages = new THREE.Mesh(
      new THREE.PlaneGeometry(0.33, 0.22),
      new THREE.MeshBasicMaterial({ color: 0xfefce8 })
    );
    pages.rotation.x = -Math.PI / 2;
    pages.position.y = 0.011;
    const pencilA = new THREE.Mesh(
      new THREE.CylinderGeometry(0.008, 0.008, 0.19, 6),
      new THREE.MeshBasicMaterial({ color: 0xef4444 })
    );
    pencilA.rotation.z = Math.PI / 2;
    pencilA.rotation.y = 0.35;
    pencilA.position.set(0.22, 0.012, 0.04);
    const pencilB = new THREE.Mesh(
      new THREE.CylinderGeometry(0.008, 0.008, 0.19, 6),
      new THREE.MeshBasicMaterial({ color: 0x22c55e })
    );
    pencilB.rotation.z = Math.PI / 2;
    pencilB.rotation.y = -0.22;
    pencilB.position.set(0.24, 0.012, -0.04);
    nbGrp.add(cover, pages, pencilA, pencilB);
    firstFloorGroup.add(nbGrp);
  });

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
    addPorticoColumn(postStrikeModelGroup, colX, floorH / 2, 4.4, { feature: 'post_portico_col' });
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
  const CRATER_EN_TEXT = 'Ø 5.0 m IMPACT CRATER · CENTRAL HALL';
  const CRATER_FA_TEXT = 'قطر دهانه گودال انفجار: ۵ متر (مرکز سالن مدرسه)';
  const drawCraterLabels = () => {
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
    new THREE.PlaneGeometry(4.2, 0.72),
    new THREE.MeshBasicMaterial({ map: scaleTex, side: THREE.DoubleSide })
  );
  scaleBadge.position.set(-2.5, 5.35, -5.5);
  postStrikeModelGroup.add(scaleBadge);

  postStrikeModelGroup.add(new THREE.Line(
    new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(-2.5, 0.5, -5.5),
      new THREE.Vector3(-2.5, 4.99, -5.5)
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

  // H) 3D Green School Desk Displaying Recovered US Tomahawk Guidance Subassemblies in Courtyard (Station 7 script & clip 07_B)
  const forensicDeskGroup = new THREE.Group();
  forensicDeskGroup.position.set(13.50, 0.02, 7.35);
  forensicDeskGroup.rotation.y = 0.08;
  const greenDeskMat = new THREE.MeshStandardMaterial({ color: 0x2f6f4e, roughness: 0.62 });
  const deskSteelMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.5, metalness: 0.45 });
  const alloyMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.38, metalness: 0.72 });
  const charredAlloyMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.55, metalness: 0.58 });
  const pcbMat = new THREE.MeshStandardMaterial({ color: 0x166534, roughness: 0.5, metalness: 0.3 });

  const fTop = new THREE.Mesh(new THREE.BoxGeometry(1.55, 0.06, 0.72), greenDeskMat);
  fTop.position.set(0, 0.76, 0);
  fTop.castShadow = true;
  forensicDeskGroup.add(fTop);
  [[-0.70, -0.29], [0.70, -0.29], [-0.70, 0.29], [0.70, 0.29]].forEach(([lx, lz]) => {
    const leg = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.74, 0.05), deskSteelMat);
    leg.position.set(lx, 0.37, lz);
    forensicDeskGroup.add(leg);
  });
  // Recovered Tomahawk guidance ring, actuator housing & Ball Aerospace / MADE IN USA electronics subassembly
  const guidanceRing = new THREE.Mesh(new THREE.CylinderGeometry(0.21, 0.23, 0.18, 20), alloyMat);
  guidanceRing.position.set(-0.38, 0.88, -0.02);
  guidanceRing.rotation.z = 0.22;
  const pcbUnit = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.09, 0.20), pcbMat);
  pcbUnit.position.set(0.06, 0.835, 0.04);
  const finBlade = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.03, 0.19), charredAlloyMat);
  finBlade.position.set(0.46, 0.815, -0.04);
  finBlade.rotation.y = -0.35;
  finBlade.rotation.z = 0.14;
  const tagMat = new THREE.MeshBasicMaterial({ color: 0xfacc15 });
  [-0.56, -0.08, 0.34].forEach((tx) => {
    const evTag = new THREE.Mesh(new THREE.ConeGeometry(0.045, 0.09, 4), tagMat);
    evTag.position.set(tx, 0.835, 0.22);
    forensicDeskGroup.add(evTag);
  });
  forensicDeskGroup.add(guidanceRing, pcbUnit, finBlade);
  postStrikeModelGroup.add(forensicDeskGroup);

  // I) Mount All 16 Verified 1080p Pre-Strike & Incident Videos/Photos Directly Inside the 3D School Architecture
  buildAllInWorldWalkthroughScreens();
}

export function setCutawayMode(mode) {
  appState.cutawayState = ((mode % 3) + 3) % 3;
  const { cutawayState, roofGroup, firstFloorGroup, groundFloorGroup, currentLang } = appState;
  const btn = typeof document !== 'undefined' ? document.getElementById('btnCutaway') : null;

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
