/**
 * In-world 3D classroom portraits (119 schoolchildren + 26 female educators),
 * 28 recovered rubble drawings, classroom desks, and interactive raycasting.
 *
 * Reuses shared BoxGeometry / PlaneGeometry caches by exact dimensions to eliminate
 * hundreds of duplicate WebGL geometry buffers while preserving identical vertex layout.
 */
import * as THREE from 'three';

import { appState } from '../state.js';
import {
  FRAME_BACKING_DEPTH,
  FRAME_DECAL_GAP,
  FRAME_IMAGE_Z,
  FRAME_LABEL_Z,
  FRAME_STACK_STEP,
  FRAME_IMAGE_CENTER_Y,
  FRAME_IMAGE_HEIGHT,
  FRAME_LABEL_HEIGHT,
  FRAME_LABEL_CENTER_Y,
  makeDecalMaterial,
} from './frame-stack.js';

const boxGeoCache = new Map();
const planeGeoCache = new Map();

function getSharedBoxGeo(w, h, d) {
  const key = `${w.toFixed(4)}_${h.toFixed(4)}_${d.toFixed(4)}`;
  let geo = boxGeoCache.get(key);
  if (!geo) {
    geo = new THREE.BoxGeometry(w, h, d);
    boxGeoCache.set(key, geo);
  }
  return geo;
}

function getSharedPlaneGeo(w, h) {
  const key = `${w.toFixed(4)}_${h.toFixed(4)}`;
  let geo = planeGeoCache.get(key);
  if (!geo) {
    geo = new THREE.PlaneGeometry(w, h);
    planeGeoCache.set(key, geo);
  }
  return geo;
}

// --- Shared in-world text ----------------------------------------------------

/**
 * Font stacks for canvas-painted plaques and banners. Vazirmatn and Source Sans 3 are
 * the page's RTL and body faces and reconstruction.html already loads them, so reusing
 * them costs no extra request. Canvas text never triggers a webfont download by itself,
 * which is why every painter repaints once its faces have resolved.
 */
const FA_FONT_STACK = '"Vazirmatn", Tahoma, sans-serif';
const EN_FONT_STACK = '"Source Sans 3", "Segoe UI", system-ui, sans-serif';

/**
 * Anisotropic filtering keeps wall text and photos legible at the grazing angles the
 * camera usually views them from. Past 8x the extra taps cost fill rate without adding
 * detail at glyph scale.
 */
function textureAnisotropy() {
  if (!appState.renderer) return 1;
  return Math.max(1, Math.min(appState.renderer.getMaxAnisotropy(), 8));
}

/**
 * Prepares a canvas- or photo-authored decal: sRGB decoding, then the shared filtering and
 * anisotropy. Every decal here is painted colour, never a data map.
 */
function prepareDecalTexture(tex) {
  if (!tex) return tex;
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = textureAnisotropy();
  tex.generateMipmaps = true;
  tex.minFilter = THREE.LinearMipmapLinearFilter;
  tex.magFilter = THREE.LinearFilter;
  tex.needsUpdate = true;
  return tex;
}

/**
 * Fills a decal with a photo, cropping the overflow instead of stretching it. Portrait
 * photos are anchored to the top: the head sits in the upper centre of these shots, so the
 * cropped band comes off the shoulders, not the face. Side overflow is always split evenly.
 *
 * @param {number} planeAspect decal width / height
 * @param {number} anchorY 0 keeps the top of the photo, 0.5 centres it, 1 keeps the bottom
 */
function coverDecalTexture(tex, planeAspect, anchorY) {
  const image = tex && tex.image;
  if (!image || !image.width || !image.height || !(planeAspect > 0)) return;
  const imageAspect = image.width / image.height;
  if (Math.abs(imageAspect - planeAspect) < 0.005) return;

  if (imageAspect > planeAspect) {
    // Photo is wider than the opening: trim left and right, keeping the subject centred.
    const keep = planeAspect / imageAspect;
    tex.repeat.set(keep, 1);
    tex.offset.set((1 - keep) / 2, 0);
    return;
  }

  // Photo is taller than the opening: trim the overflow. flipY puts the photo's top at
  // v = 1, so a top anchor starts the window one cropped band below that edge.
  const keep = imageAspect / planeAspect;
  const anchor = Math.min(1, Math.max(0, typeof anchorY === 'number' ? anchorY : 0.5));
  const drop = anchor * (1 - keep);
  tex.repeat.set(1, keep);
  tex.offset.set(0, tex.flipY ? 1 - keep - drop : drop);
}

/**
 * Fits a scanned drawing or desk sheet inside its decal instead of stretching it, narrowing
 * the decal to the image aspect. Nothing is cropped: the sheet edges and the child's
 * handwriting are part of the artifact, so the mount behind fills the leftover area.
 */
function containDecalTexture(tex, mesh, boxW, boxH) {
  const image = tex && tex.image;
  if (!image || !image.width || !image.height || !(boxW > 0) || !(boxH > 0)) return;
  const imageAspect = image.width / image.height;
  const boxAspect = boxW / boxH;
  if (Math.abs(imageAspect - boxAspect) < 0.005) return;

  mesh.geometry =
    imageAspect > boxAspect
      ? getSharedPlaneGeo(boxW, boxW / imageAspect)
      : getSharedPlaneGeo(boxH * imageAspect, boxH);
}

/** Dark mount behind contained drawings; shared by every frame so the extra quads stay cheap. */
let imageMatMaterial = null;
function getImageMatMaterial() {
  if (!imageMatMaterial) {
    imageMatMaterial = new THREE.MeshBasicMaterial({ color: 0x1e293b, side: THREE.DoubleSide, toneMapped: false });
  }
  return imageMatMaterial;
}

/** Repaints a canvas once the fonts its text is set in have loaded. */
function repaintWhenFontsReady(specs, texts, repaint) {
  if (typeof document === 'undefined' || !document.fonts || !document.fonts.load) return;
  try {
    const pending = specs.map((spec, i) => document.fonts.load(spec, texts[i] || ' '));
    Promise.all(pending)
      .then(() => repaint())
      .catch(() => {});
  } catch (_) {
    // The fallback-painted canvas is already valid; a font that cannot be loaded is cosmetic.
  }
}

/** Centred line drawn at the largest size that fits, ellipsised only if it still overflows. */
function drawFittedLine(ctx, text, fontStack, weight, basePx, minPx, maxWidth, centerX, baselineY) {
  const value = text == null ? '' : String(text);
  const floorPx = Math.max(6, Math.round(minPx));
  let size = Math.max(floorPx, Math.round(basePx));
  for (;;) {
    ctx.font = `${weight} ${size}px ${fontStack}`;
    if (ctx.measureText(value).width <= maxWidth || size <= floorPx) break;
    size -= 1;
  }

  let shown = value;
  if (ctx.measureText(shown).width > maxWidth) {
    const ellipsis = '…';
    let end = shown.length;
    while (end > 0 && ctx.measureText(shown.slice(0, end) + ellipsis).width > maxWidth) end -= 1;
    shown = shown.slice(0, end).trimEnd() + ellipsis;
  }
  ctx.fillText(shown, centerX, Math.round(baselineY));
}

// --- Nameplates --------------------------------------------------------------

/**
 * Nameplate texel density. A plate is about 0.2 m tall on the wall and is read from the
 * inspector at roughly 1.8 m; below about 550 px/m the glyph edges turn to mush at that
 * distance. Lower it to trade sharpness for texture memory, since the gallery builds one
 * RGBA texture per plate.
 */
const NAMEPLATE_TEXELS_PER_METRE = 600;
const NAMEPLATE_DESIGN_HEIGHT = 76;
const NAMEPLATE_DEFAULT_WIDTH = 0.72;
const NAMEPLATE_DEFAULT_HEIGHT = 0.196;

/**
 * Paints a nameplate. Every metric is defined for the 76 px design plate and scaled by
 * the painted height, so a plate reads the same whatever the frame size around it.
 */
function paintNameplate(canvas, line1Fa, line2En, line3Meta, accentHex) {
  const ctx = canvas.getContext('2d');
  const s = canvas.height / NAMEPLATE_DESIGN_HEIGHT;

  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = '#0d1322';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  const border = Math.max(2, Math.round(3 * s));
  ctx.strokeStyle = accentHex || '#d4a853';
  ctx.lineWidth = border;
  // Half-width inset keeps the full stroke inside the texture.
  ctx.strokeRect(border / 2, border / 2, canvas.width - border, canvas.height - border);

  ctx.textAlign = 'center';
  ctx.textBaseline = 'alphabetic';
  const maxTextWidth = canvas.width * 0.9;

  ctx.direction = 'rtl';
  ctx.fillStyle = '#fef3c7';
  drawFittedLine(ctx, line1Fa || line2En || '', FA_FONT_STACK, 700, 17 * s, 10 * s, maxTextWidth, canvas.width / 2, 25 * s);

  ctx.direction = 'ltr';
  ctx.fillStyle = '#e2e8f0';
  drawFittedLine(ctx, line2En || '', EN_FONT_STACK, 600, 13 * s, 9 * s, maxTextWidth, canvas.width / 2, 46 * s);

  ctx.fillStyle = accentHex || '#d4a853';
  drawFittedLine(ctx, line3Meta || '', EN_FONT_STACK, 700, 12 * s, 9 * s, maxTextWidth, canvas.width / 2, 65 * s);
}

/**
 * Builds a nameplate texture sized to the plate it will be mapped onto, so the glyphs are
 * never stretched to fit a mismatched canvas aspect.
 */
export function createNameplateTexture(line1Fa, line2En, line3Meta, accentHex, plateWidth, plateHeight) {
  const width = plateWidth > 0 ? plateWidth : NAMEPLATE_DEFAULT_WIDTH;
  const height = plateHeight > 0 ? plateHeight : NAMEPLATE_DEFAULT_HEIGHT;

  const canvas = document.createElement('canvas');
  canvas.width = Math.max(256, Math.round((width * NAMEPLATE_TEXELS_PER_METRE) / 2) * 2);
  canvas.height = Math.max(64, Math.round(canvas.width * (height / width)));
  paintNameplate(canvas, line1Fa, line2En, line3Meta, accentHex);

  const tex = new THREE.CanvasTexture(canvas);
  prepareDecalTexture(tex);

  const s = canvas.height / NAMEPLATE_DESIGN_HEIGHT;
  repaintWhenFontsReady(
    [
      `700 ${Math.round(17 * s)}px ${FA_FONT_STACK}`,
      `600 ${Math.round(13 * s)}px ${EN_FONT_STACK}`,
      `700 ${Math.round(12 * s)}px ${EN_FONT_STACK}`,
    ],
    [line1Fa, line2En, line3Meta],
    () => {
      paintNameplate(canvas, line1Fa, line2En, line3Meta, accentHex);
      tex.needsUpdate = true;
    }
  );

  return tex;
}

// --- Wing banners ------------------------------------------------------------

/**
 * A banner plane spans 5–7 m of wall, so its legibility is limited by texel density,
 * not by antialiasing. The canvas is painted at a fixed texel density and every layout
 * number below is expressed in a 768x110 design space that gets scaled up to the canvas.
 */
const BANNER_DESIGN_WIDTH = 768;
const BANNER_DESIGN_HEIGHT = 110;
const BANNER_TEXELS_PER_METRE = 320;
const BANNER_TEXTURE_WIDTH_MIN = 1024;
const BANNER_TEXTURE_WIDTH_MAX = 2560;
const BANNER_TEXT_MARGIN = 32;

/**
 * Persian and English faces for banner titles live in the shared stacks above; these
 * sizes, weights and baselines describe the 768x110 banner design space.
 */
const BANNER_FA_WEIGHT = 700;
const BANNER_EN_WEIGHT = 700;
const BANNER_FA_SIZE = 26;
const BANNER_EN_SIZE = 20;
const BANNER_FA_MIN_SIZE = 15;
const BANNER_EN_MIN_SIZE = 12;
const BANNER_FA_BASELINE_Y = 44;
const BANNER_EN_BASELINE_Y = 82;

/** Texture width for a banner plane of the given world width, rounded for GPU alignment. */
function bannerTextureWidth(planeWidth) {
  const wanted = planeWidth * BANNER_TEXELS_PER_METRE;
  const clamped = Math.min(BANNER_TEXTURE_WIDTH_MAX, Math.max(BANNER_TEXTURE_WIDTH_MIN, wanted));
  return Math.round(clamped / 8) * 8;
}

/**
 * Sets ctx.font to the largest size at or below basePx at which the string fits inside
 * the banner's border. Without the fit, long Persian titles are clipped by the canvas edge.
 */
function fitBannerFont(ctx, text, fontStack, weight, basePx, minPx, scale) {
  const maxWidth = (BANNER_DESIGN_WIDTH - BANNER_TEXT_MARGIN * 2) * scale;
  let size = basePx;
  for (;;) {
    const deviceSize = Math.max(10, Math.round(size * scale));
    ctx.font = `${weight} ${deviceSize}px ${fontStack}`;
    if (ctx.measureText(text).width <= maxWidth || size <= minPx) return deviceSize;
    size -= 1;
  }
}

/**
 * Paints a banner onto its canvas. Runs twice: once with whatever font is already
 * resolved, then again once the webfonts arrive, because canvas text does not trigger
 * a webfont download by itself.
 */
function paintWingBanner(canvas, titleEn, titleFa, bgHex, borderHex) {
  const ctx = canvas.getContext('2d');
  const scale = canvas.width / BANNER_DESIGN_WIDTH;

  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = bgHex || 'rgba(13, 19, 34, 0.94)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  const border = Math.max(2, Math.round(5 * scale));
  ctx.strokeStyle = borderHex || '#d4a853';
  ctx.lineWidth = border;
  // Half-width inset keeps the full stroke inside the texture.
  ctx.strokeRect(border / 2, border / 2, canvas.width - border, canvas.height - border);

  ctx.textAlign = 'center';
  ctx.textBaseline = 'alphabetic';

  ctx.direction = 'rtl';
  ctx.fillStyle = '#fde68a';
  fitBannerFont(ctx, titleFa, FA_FONT_STACK, BANNER_FA_WEIGHT, BANNER_FA_SIZE, BANNER_FA_MIN_SIZE, scale);
  ctx.fillText(titleFa, canvas.width / 2, Math.round(BANNER_FA_BASELINE_Y * scale));

  ctx.direction = 'ltr';
  ctx.fillStyle = '#f8fafc';
  fitBannerFont(ctx, titleEn, EN_FONT_STACK, BANNER_EN_WEIGHT, BANNER_EN_SIZE, BANNER_EN_MIN_SIZE, scale);
  ctx.fillText(titleEn, canvas.width / 2, Math.round(BANNER_EN_BASELINE_Y * scale));
}

export function createWingBannerIn3D(parentGroup, titleEn, titleFa, x, y, z, rotY, width, bgHex, borderHex) {
  const canvas = document.createElement('canvas');
  canvas.width = bannerTextureWidth(width);
  canvas.height = Math.round(canvas.width * (BANNER_DESIGN_HEIGHT / BANNER_DESIGN_WIDTH));
  paintWingBanner(canvas, titleEn, titleFa, bgHex, borderHex);

  const tex = new THREE.CanvasTexture(canvas);
  prepareDecalTexture(tex);

  // Banner text is a sign, not lit geometry: keep the painted colours exactly as authored
  // instead of letting the scene's ACES tone mapping wash the glyphs toward grey.
  const mat = new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide, toneMapped: false });
  const mesh = new THREE.Mesh(
    getSharedPlaneGeo(width, width * (BANNER_DESIGN_HEIGHT / BANNER_DESIGN_WIDTH)),
    mat
  );
  mesh.position.set(x, y, z);
  mesh.rotation.y = rotY;
  parentGroup.add(mesh);

  const scale = canvas.width / BANNER_DESIGN_WIDTH;
  repaintWhenFontsReady(
    [
      `${BANNER_FA_WEIGHT} ${Math.round(BANNER_FA_SIZE * scale)}px ${FA_FONT_STACK}`,
      `${BANNER_EN_WEIGHT} ${Math.round(BANNER_EN_SIZE * scale)}px ${EN_FONT_STACK}`,
    ],
    [titleFa, titleEn],
    () => {
      paintWingBanner(canvas, titleEn, titleFa, bgHex, borderHex);
      tex.needsUpdate = true;
    }
  );
}

/**
 * Builds a wall-mounted frame: backing box, photo / drawing decal, nameplate decal.
 * Shared by the portrait and drawing builders; layering comes from frame-stack.js.
 */
function buildFramedWallItem(parentGroup, loader, opts) {
  const {
    item,
    x,
    y,
    z,
    rotY,
    frameW,
    frameH,
    borderHex,
    imageWidthFactor,
    imageUrl,
    nameplateTexture,
    artifactType,
    wingLabel,
    cutawayMode,
    focusDist,
  } = opts;

  const holder = new THREE.Group();
  holder.position.set(x, y, z);
  holder.rotation.y = rotY;

  const backing = new THREE.Mesh(
    getSharedBoxGeo(frameW, frameH, FRAME_BACKING_DEPTH),
    new THREE.MeshBasicMaterial({ color: borderHex })
  );
  holder.add(backing);

  const imageW = frameW * imageWidthFactor;
  const imageH = frameH * FRAME_IMAGE_HEIGHT;

  // Scanned drawings are contained, so they need a dark mount inside the opening. Portraits
  // fill the opening, so their placeholder is all that sits behind the photo.
  const containsWholeImage = artifactType === 'drawing';
  if (containsWholeImage) {
    const mountPlane = new THREE.Mesh(getSharedPlaneGeo(imageW, imageH), getImageMatMaterial());
    mountPlane.position.set(0, frameH * FRAME_IMAGE_CENTER_Y, FRAME_IMAGE_Z);
    holder.add(mountPlane);
  }

  const imagePlane = new THREE.Mesh(
    getSharedPlaneGeo(imageW, imageH),
    makeDecalMaterial({ color: 0x1e293b })
  );
  imagePlane.position.set(
    0,
    frameH * FRAME_IMAGE_CENTER_Y,
    containsWholeImage ? FRAME_LABEL_Z : FRAME_IMAGE_Z
  );
  holder.add(imagePlane);

  if (imageUrl) {
    loader.load(imageUrl, (tex) => {
      prepareDecalTexture(tex);
      if (containsWholeImage) {
        containDecalTexture(tex, imagePlane, imageW, imageH);
      } else {
        // Portraits: fill the opening and take the crop off the bottom of the photo.
        coverDecalTexture(tex, imageW / imageH, 0);
      }
      imagePlane.material = makeDecalMaterial({ map: tex });
      imagePlane.material.needsUpdate = true;
    });
  }

  const labelPlane = new THREE.Mesh(
    getSharedPlaneGeo(imageW, frameH * FRAME_LABEL_HEIGHT),
    makeDecalMaterial({ map: nameplateTexture, toneMapped: false })
  );
  labelPlane.position.set(0, frameH * FRAME_LABEL_CENTER_Y, FRAME_LABEL_Z);
  holder.add(labelPlane);

  const normal = new THREE.Vector3(0, 0, 1).applyAxisAngle(new THREE.Vector3(0, 1, 0), rotY);
  const focusCam = new THREE.Vector3(x, y + 0.08, z).add(normal.clone().multiplyScalar(focusDist));
  const lookAt = new THREE.Vector3(x, y, z);

  const artifactData = {
    artifactType,
    item,
    wingLabel,
    focusCam,
    lookAt,
    cutawayMode,
  };
  imagePlane.userData = artifactData;
  backing.userData = artifactData;
  labelPlane.userData = artifactData;
  appState.clickable3DArtifacts.push(imagePlane, backing, labelPlane);

  parentGroup.add(holder);
}

export function create3DFramedPortraitOnWall(
  parentGroup,
  loader,
  item,
  x,
  y,
  z,
  rotY,
  frameW,
  frameH,
  borderHex,
  cutawayMode,
  wingLabel,
  focusDist
) {
  const imageUrl =
    item.photoPath || item.photo_path || (item.photoGrid ? `images/children/child_${item.photoGrid}.jpg` : null);
  const metaText =
    item.category === 'teacher'
      ? item.role || 'Educator'
      : `Grade ${item.grade || '?'} · Age ${item.age || '?'}`;
  // Painted at the exact size of the label plane buildFramedWallItem creates, so the
  // glyphs are never stretched to fit a mismatched canvas aspect.
  const imageWidthFactor = 0.9;
  const nameplateTexture = createNameplateTexture(
    item.nameFa || item.full_name_fa,
    item.name || item.full_name_en,
    metaText,
    borderHex === 0xf472b6 ? '#f472b6' : '#d4a853',
    frameW * imageWidthFactor,
    frameH * FRAME_LABEL_HEIGHT
  );

  buildFramedWallItem(parentGroup, loader, {
    item,
    x,
    y,
    z,
    rotY,
    frameW,
    frameH,
    borderHex: borderHex || 0xd4a853,
    imageWidthFactor,
    imageUrl,
    nameplateTexture,
    artifactType: 'victim',
    wingLabel: wingLabel || 'Reconstructed School Interior',
    cutawayMode: typeof cutawayMode === 'number' ? cutawayMode : 2,
    focusDist: typeof focusDist === 'number' ? focusDist : 1.85,
  });
}

export function create3DRubbleDrawingOnWall(
  parentGroup,
  loader,
  drw,
  x,
  y,
  z,
  rotY,
  frameW,
  frameH,
  cutawayMode,
  wingLabel,
  focusDist
) {
  const imageWidthFactor = 0.91;
  const nameplateTexture = createNameplateTexture(
    drw.studentNameFa || 'نقاشی زیر آوار',
    drw.title && drw.title.en ? drw.title.en : drw.id,
    drw.dateOnPage || 'Rubble Artifact',
    drw.hasBlastDamage ? '#f87171' : '#fcd34d',
    frameW * imageWidthFactor,
    frameH * FRAME_LABEL_HEIGHT
  );

  buildFramedWallItem(parentGroup, loader, {
    item: drw,
    x,
    y,
    z,
    rotY,
    frameW,
    frameH,
    borderHex: drw.hasBlastDamage ? 0xef4444 : 0xd4a853,
    imageWidthFactor,
    imageUrl: drw.thumb || drw.image,
    nameplateTexture,
    artifactType: 'drawing',
    wingLabel: wingLabel || 'Classroom Rubble Artifact',
    cutawayMode: typeof cutawayMode === 'number' ? cutawayMode : 1,
    focusDist: typeof focusDist === 'number' ? focusDist : 1.95,
  });
}

export function createClassroomDeskWithDrawing(parentGroup, loader, drw, x, yBase, z, cutawayMode) {
  const deskGroup = new THREE.Group();
  deskGroup.position.set(x, yBase, z);
  deskGroup.userData = { feature: 'classroom_desk' };

  const woodMat = new THREE.MeshStandardMaterial({ color: 0x8b5a2b, roughness: 0.75 });
  const frameMetalMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.55, metalness: 0.4 });

  const top = new THREE.Mesh(getSharedBoxGeo(1.12, 0.05, 0.58), woodMat);
  top.position.set(0, 0.68, 0);
  top.castShadow = true;
  deskGroup.add(top);

  [
    [-0.5, -0.23],
    [0.5, -0.23],
    [-0.5, 0.23],
    [0.5, 0.23],
  ].forEach(([lx, lz]) => {
    const leg = new THREE.Mesh(getSharedBoxGeo(0.045, 0.66, 0.045), frameMetalMat);
    leg.position.set(lx, 0.33, lz);
    leg.castShadow = true;
    deskGroup.add(leg);
  });

  const bench = new THREE.Mesh(getSharedBoxGeo(1.12, 0.045, 0.32), woodMat);
  bench.position.set(0, 0.4, 0.5);
  bench.castShadow = true;
  deskGroup.add(bench);

  [-0.48, 0.48].forEach((bx) => {
    const bLeg = new THREE.Mesh(getSharedBoxGeo(0.045, 0.39, 0.28), frameMetalMat);
    bLeg.position.set(bx, 0.195, 0.5);
    deskGroup.add(bLeg);
  });

  if (drw) {
    // Desk surface sits at y = 0.705; float the sheet clear of it.
    const sheet = new THREE.Mesh(
      getSharedPlaneGeo(0.46, 0.34),
      makeDecalMaterial({ color: 0xffffff })
    );
    sheet.rotation.x = -Math.PI / 2;
    sheet.position.set(0, 0.705 + FRAME_DECAL_GAP, 0);
    deskGroup.add(sheet);

    loader.load(drw.thumb || drw.image, (tex) => {
      prepareDecalTexture(tex);
      containDecalTexture(tex, sheet, 0.46, 0.34);
      sheet.material = makeDecalMaterial({ map: tex });
      sheet.material.needsUpdate = true;
    });

    const artifactData = {
      artifactType: 'drawing',
      item: drw,
      wingLabel: 'Ground Floor Classroom Desk (Recovered from Rubble)',
      focusCam: new THREE.Vector3(x, yBase + 1.75, z + 1.25),
      lookAt: new THREE.Vector3(x, yBase + 0.7, z),
      cutawayMode: cutawayMode || 2,
    };
    sheet.userData = artifactData;
    appState.clickable3DArtifacts.push(sheet);
  }

  parentGroup.add(deskGroup);
}

/**
 * Courtyard stele: dark slate slab with a gold rim, a portrait and a nameplate on both faces.
 * Used by the Memorial Avenue and by the schoolyard row beside the assembly lines.
 * Decals ride FRAME_DECAL_GAP off the slab's +/-0.05 faces, one stack step apart.
 */
function createCourtyardStele(parentGroup, loader, child, { x, z, rotY, wingLabel, focusCam, lookAt }) {
  const isTeacher = child.category === 'teacher';
  const STELE_FACE_Z = 0.05;
  const STELE_LABEL_Z = STELE_FACE_Z + FRAME_DECAL_GAP;
  const STELE_PORTRAIT_Z = STELE_LABEL_Z + FRAME_STACK_STEP;
  const imgUrl =
    child.photoPath || child.photo_path || (child.photoGrid ? `images/children/child_${child.photoGrid}.jpg` : null);

  const post = new THREE.Mesh(
    getSharedBoxGeo(0.96, 1.88, 0.1),
    new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.5 })
  );
  post.position.set(x, 1.08, z);
  post.rotation.y = rotY;
  post.castShadow = true;
  parentGroup.add(post);

  const border = new THREE.Mesh(
    getSharedBoxGeo(1.02, 1.94, 0.07),
    new THREE.MeshBasicMaterial({ color: 0xd4a853 })
  );
  post.add(border);

  const labelTex = createNameplateTexture(
    child.nameFa || child.full_name_fa,
    child.name || child.full_name_en,
    isTeacher ? child.role || 'Educator' : `Grade ${child.grade || '?'} · Age ${child.age || '?'}`,
    '#d4a853',
    0.88,
    0.3
  );
  const frontLabel = new THREE.Mesh(
    getSharedPlaneGeo(0.88, 0.3),
    makeDecalMaterial({ map: labelTex, toneMapped: false })
  );
  frontLabel.position.set(0, -0.68, STELE_LABEL_Z);
  post.add(frontLabel);

  const backLabel = frontLabel.clone();
  backLabel.position.set(0, -0.68, -STELE_LABEL_Z);
  backLabel.rotation.y = Math.PI;
  post.add(backLabel);

  const steleArtifact = {
    artifactType: 'victim',
    item: child,
    wingLabel,
    focusCam,
    lookAt,
    cutawayMode: 0,
  };
  post.userData = steleArtifact;
  appState.clickable3DArtifacts.push(post);

  if (imgUrl) {
    loader.load(imgUrl, (tex) => {
      prepareDecalTexture(tex);
      const portraitMesh = new THREE.Mesh(
        getSharedPlaneGeo(0.88, 1.32),
        makeDecalMaterial({ map: tex })
      );
      coverDecalTexture(tex, 0.88 / 1.32, 0);
      portraitMesh.position.set(0, 0.18, STELE_PORTRAIT_Z);
      portraitMesh.userData = steleArtifact;
      post.add(portraitMesh);
      appState.clickable3DArtifacts.push(portraitMesh);

      const backMesh = portraitMesh.clone();
      backMesh.position.set(0, 0.18, -STELE_PORTRAIT_Z);
      backMesh.rotation.y = Math.PI;
      backMesh.userData = steleArtifact;
      post.add(backMesh);
      appState.clickable3DArtifacts.push(backMesh);
    });
  }
}

export function populate3DSchoolPortraitsAndDrawings() {
  const loader = new THREE.TextureLoader();
  appState.clickable3DArtifacts = [];
  const {
    childrenList,
    teachersList,
    drawingsList,
    memorialBoardsGroup,
    preStrikeModelGroup,
    groundFloorGroup,
    firstFloorGroup,
  } = appState;

  // 1. COURTYARD MEMORIAL AVENUE (24 Double-Sided Steles flanking the Central Vow Shrine Walk at X = -5.2 & X = +2.2)
  const portraitSample = childrenList.filter((c) => c.photoPath).slice(0, 24);
  portraitSample.forEach((child, idx) => {
    const isLeft = idx < 12;
    const slot = isLeft ? idx : idx - 12;
    const x = isLeft ? -5.2 : 2.2;
    const z = 13.0 + slot * 1.2;
    createCourtyardStele(memorialBoardsGroup, loader, child, {
      x,
      z,
      rotY: isLeft ? Math.PI / 2 : -Math.PI / 2,
      wingLabel: 'Courtyard 100 Faces Memorial Walk',
      focusCam: new THREE.Vector3(-1.5, 1.45, z),
      lookAt: new THREE.Vector3(x, 1.15, z),
    });
  });

  // Devoted 2nd-Grade Teacher Ms. Zohreh Shahriyari Courtyard Stand (Station 1)
  const zohrehTeacher = teachersList.find((t) => t.id === 'zohreh-shahriyari');
  if (zohrehTeacher) {
    // Same stele as the Memorial Avenue, standing in line with the 01_B screen stele
    // (x = 8.0, z = 9.5, tour-config.js) and facing east over the assembly lines.
    const tx = 8.0;
    const tz = 7.9;
    const tRot = Math.PI / 2;
    createCourtyardStele(preStrikeModelGroup, loader, zohrehTeacher, {
      x: tx,
      z: tz,
      rotY: tRot,
      wingLabel: 'Morning Schoolyard · Martyred 2nd-Grade Teacher Zohreh Shahriyari & Unborn Son',
      focusCam: new THREE.Vector3(tx + 2.25, 1.45, tz),
      lookAt: new THREE.Vector3(tx, 1.15, tz),
    });
  }

  if (!groundFloorGroup || !firstFloorGroup) return;

  // 2. GROUND FLOOR WEST WING: BOYS OF GRADES 1, 2 & 3
  const boysGrades1to3 = childrenList.filter((c) => c.gender === 'boy' && (c.grade || 1) <= 3 && c.photoPath);
  createWingBannerIn3D(
    groundFloorGroup,
    `GROUND FLOOR WEST CLASSROOMS: BOYS GRADES 1–3 (${boysGrades1to3.length} STUDENTS)`,
    `کلاس‌های طبقه همکف (بال غربی): ۴۸ دانش‌آموز پسر پایه‌های اول تا سوم`,
    -15.8,
    3.25,
    -2.3,
    0,
    5.8,
    '#0d1b2a',
    '#38bdf8'
  );

  let bIdx = 0;
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 6; col++) {
      if (bIdx >= boysGrades1to3.length) break;
      const px = -18.1 + col * 0.94;
      const py = 1.22 + row * 1.12;
      create3DFramedPortraitOnWall(
        groundFloorGroup,
        loader,
        boysGrades1to3[bIdx++],
        px,
        py,
        -7.38,
        0,
        0.8,
        0.98,
        0x38bdf8,
        2,
        'Ground Floor West Wing · Boys Classrooms (Grades 1–3)',
        1.75
      );
    }
  }
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 6; col++) {
      if (bIdx >= boysGrades1to3.length) break;
      const px = -18.1 + col * 0.94;
      const py = 1.22 + row * 1.12;
      create3DFramedPortraitOnWall(
        groundFloorGroup,
        loader,
        boysGrades1to3[bIdx++],
        px,
        py,
        -2.72,
        Math.PI,
        0.8,
        0.98,
        0x38bdf8,
        2,
        'Ground Floor West Wing · Boys Classrooms (Grades 1–3)',
        1.75
      );
    }
  }
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 6; col++) {
      if (bIdx >= boysGrades1to3.length) break;
      const px = -18.1 + col * 0.94;
      const py = 1.22 + row * 1.12;
      create3DFramedPortraitOnWall(
        groundFloorGroup,
        loader,
        boysGrades1to3[bIdx++],
        px,
        py,
        -2.28,
        0,
        0.8,
        0.98,
        0x38bdf8,
        2,
        'Ground Floor South-West Classroom · Boys Grades 1–2',
        1.75
      );
    }
  }
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 6; col++) {
      if (bIdx >= boysGrades1to3.length) break;
      const px = -18.1 + col * 0.94;
      const py = 1.22 + row * 1.12;
      create3DFramedPortraitOnWall(
        groundFloorGroup,
        loader,
        boysGrades1to3[bIdx++],
        px,
        py,
        -12.72,
        0,
        0.8,
        0.98,
        0x38bdf8,
        2,
        'Ground Floor North-West Classroom · Boys Grades 1–3',
        1.75
      );
    }
  }
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 6; col++) {
      if (bIdx >= boysGrades1to3.length) break;
      const pz = -5.0 + col * 1.12;
      const py = 1.22 + row * 1.12;
      create3DFramedPortraitOnWall(
        groundFloorGroup,
        loader,
        boysGrades1to3[bIdx++],
        -7.42,
        py,
        pz,
        -Math.PI / 2,
        0.8,
        0.98,
        0x38bdf8,
        2,
        'Ground Floor South-Inner Classroom · Boys Grades 2–3',
        1.65
      );
    }
  }

  const groundDeskDrawings = drawingsList.slice(0, 6);
  for (let d = 0; d < 6; d++) {
    const dx = -17.3 + (d % 3) * 1.65;
    const dz = -5.9 + Math.floor(d / 3) * 1.85;
    createClassroomDeskWithDrawing(groundFloorGroup, loader, groundDeskDrawings[d], dx, 0.2, dz, 2);
  }

  // 3. GROUND FLOOR EAST WING: BOYS OF GRADES 4, 5 & 6
  const boysGrades4to6 = childrenList.filter((c) => c.gender === 'boy' && (c.grade || 1) >= 4 && c.photoPath);
  // Banner hidden for now. Station 2 lives in the ground-floor central hall (where the rainbow stairs
  // start); it ran along the hall face of G-20 (x = 1.09), above the frames, facing west.
  // createWingBannerIn3D(
  //   groundFloorGroup,
  //   `GROUND FLOOR EAST WING: BOYS GRADES 4–6 & CEREMONY ROOM (${boysGrades4to6.length} STUDENTS)`,
  //   `طبقه همکف (بال شرقی): دانش‌آموزان پسر پایه‌های چهارم تا ششم و اتاق جشن`,
  //   1.07,
  //   3.25,
  //   -4.9,
  //   -Math.PI / 2,
  //   6.4,
  //   '#0d1b2a',
  //   '#d4a853'
  // );

  // Two columns of frames facing each other across the hall: G-20's west face (x = 1.09, facing west)
  // and G-17's east face (x = -3.45, facing east).
  let b4Idx = 0;
  const boysHallWalls = [
    // G-20: between the 02_B frame (z -6.42..-4.18) and the door near the entrance (z -0.83..0.23)
    { x: 1.06, rotY: -Math.PI / 2, zs: [-3.5, -2.5, -1.5] },
    { x: -3.42, rotY: Math.PI / 2, zs: [-2.3, -1.3, -0.3] },
  ];
  for (const wall of boysHallWalls) {
    for (let col = 0; col < 3; col++) {
      for (let row = 0; row < 2; row++) {
        if (b4Idx >= boysGrades4to6.length) break;
        create3DFramedPortraitOnWall(
          groundFloorGroup,
          loader,
          boysGrades4to6[b4Idx++],
          wall.x,
          1.22 + row * 1.12,
          wall.zs[col],
          wall.rotY,
          0.84,
          1.02,
          0xd4a853,
          2,
          'Ground Floor Central Hall · Boys Grades 4–6',
          1.75
        );
      }
    }
  }
  // Remaining grade 4-6 boys stand in the schoolyard as steles, in one row just south of the
  // morning assembly lines (the lines' green border ends at Z = 12.55), facing north.
  const yardFrames = boysGrades4to6.slice(b4Idx, b4Idx + 10);
  yardFrames.forEach((child, i) => {
    const fx = 16.5 + (i - (yardFrames.length - 1) / 2) * 1.3;
    const fz = 13.8;
    createCourtyardStele(preStrikeModelGroup, loader, child, {
      x: fx,
      z: fz,
      rotY: Math.PI,
      wingLabel: 'Schoolyard · Boys Grades 4–6',
      focusCam: new THREE.Vector3(fx, 1.45, fz - 2.25),
      lookAt: new THREE.Vector3(fx, 1.15, fz),
    });
  });

  // 4. CENTRAL HALL & RAINBOW STAIRCASE: ALL 26 MARTYRED FEMALE EDUCATORS
  // The staircase station lives in the FIRST-FLOOR central hall (x -7.8..7.5, z -8.6..-3.3), at the
  // top of the rainbow stairs. Slab top is y = 3.71, so the frame heights below are measured from
  // the first-floor group origin exactly like the Girls' Hall frames further down (y1 = 3.6).
  const yStairHall = 3.6;
  // Banner hidden for Station 4 (it hung above the stele row at the top of the rainbow stairs).
  // createWingBannerIn3D(
  //   firstFloorGroup,
  //   `CENTRAL HALL & RAINBOW STAIRCASE: THE 26 MARTYRED FEMALE EDUCATORS`,
  //   `سالن مرکزی و راه‌پله رنگین‌کمان: ۲۶ معلم و مدیر شهیده دبستان شجره طیبه`,
  //   -5.02,
  //   yStairHall + 3.3,
  //   -8.43,
  //   0,
  //   5.2,
  //   '#1f122b',
  //   '#f472b6'
  // );

  // Wall columns for the educators, each a stack of two frames (rows at +1.22 m and +2.34 m).
  // Only wall stretches clear of doors are used (doors are 1.06 m wide: F-10 at x = -4.75 / 0.15 / 5.05,
  // F-11 at x = -5.5, F-12 at x = 2.1). The south-wall gap x -4.22..-0.38 is left free for the
  // wall-mounted video 04_B. Filled in this order, so the educators nearest the stairs come first.
  //   north wall (F-12, east of stairwell) faces south: z = -8.6 + 0.12 wall half + 0.03
  //   south wall (F-10) faces north:                    z = -3.3 - 0.12 - 0.03
  const NORTH_Z = -8.45;
  const SOUTH_Z = -3.45;
  const teacherCols = [
    ...[3.2, 4.3, 5.4, 6.5, 7.6].map((x) => ({ x, z: NORTH_Z, rotY: 0 })), // F-12, east of the stairs
    ...[1.5, 2.6, 3.7].map((x) => ({ x, z: SOUTH_Z, rotY: Math.PI })), // F-10, between the middle and east doors
    { x: 6.54, z: SOUTH_Z, rotY: Math.PI }, // F-10, east of the east door
    { x: -6.24, z: SOUTH_Z, rotY: Math.PI }, // F-10, west of the west door
    { x: -3.43, z: NORTH_Z, rotY: 0 }, // F-11, between the NW-room door and the stairwell
    { x: -7.19, z: NORTH_Z, rotY: 0 }, // F-11, west of the NW-room door
    { x: -4.45, z: NORTH_Z, rotY: 0 }, // F-11, right beside the -3.43 column (door edge is x = -4.97)
  ];

  teachersList.forEach((teacher, idx) => {
    const slot = teacherCols[Math.floor(idx / 2)] || teacherCols[teacherCols.length - 1];
    const row = idx % 2;
    create3DFramedPortraitOnWall(
      firstFloorGroup,
      loader,
      teacher,
      slot.x,
      yStairHall + 1.22 + row * 1.12,
      slot.z,
      slot.rotY,
      0.82,
      0.98,
      0xf472b6,
      1,
      'Central Assembly Hall & Rainbow Staircase · 26 Martyred Female Educators',
      1.75
    );
  });

  // 5. FIRST FLOOR WEST GIRLS' ASSEMBLY HALL: ALL 47 MARTYRED SCHOOLGIRLS
  const y1 = 3.6;
  const girlsAll = childrenList.filter((c) => c.gender === 'girl' && c.photoPath);
  // Banner hidden for Station 5 (it hung on the north wall at z = -12.7, above the prayer-room steles).
  // createWingBannerIn3D(
  //   firstFloorGroup,
  //   `FIRST FLOOR GIRLS' ASSEMBLY HALL: ALL 47 MARTYRED SCHOOLGIRLS (GRADES 1–6)`,
  //   `طبقه اول (سالن بزرگ دختران): ۴۷ دانش‌آموز دختر شهیده در پایه‌های اول تا ششم`,
  //   -15.25,
  //   y1 + 3.48,
  //   -12.7,
  //   0,
  //   6.8,
  //   '#2b1222',
  //   '#f472b6'
  // );

  let gIdx = 0;
  const girlsEastZ = [-12.0, -10.9, -9.8, -8.7, -7.6, -3.9, -2.8, -1.7, -0.6, 0.6, 1.6];
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < girlsEastZ.length; col++) {
      if (gIdx >= girlsAll.length) break;
      create3DFramedPortraitOnWall(
        firstFloorGroup,
        loader,
        girlsAll[gIdx++],
        -11.72,
        y1 + 1.22 + row * 1.12,
        girlsEastZ[col],
        -Math.PI / 2,
        0.82,
        0.98,
        0xf472b6,
        1,
        "First Floor West Wing · Girls' Assembly Hall (Grades 1–6)",
        2.1
      );
    }
  }
  const girlsWestZ = [-9.6, -8.6, -6.9, -5.9, -4.9, -1.6, -0.6];
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < girlsWestZ.length; col++) {
      if (gIdx >= girlsAll.length) break;
      create3DFramedPortraitOnWall(
        firstFloorGroup,
        loader,
        girlsAll[gIdx++],
        -18.72,
        y1 + 1.22 + row * 1.12,
        girlsWestZ[col],
        Math.PI / 2,
        0.82,
        0.98,
        0xf472b6,
        1,
        "First Floor West Wing · Girls' Assembly Hall (Grades 1–6)",
        2.1
      );
    }
  }
  for (let col = 0; col < 6; col++) {
    if (gIdx >= girlsAll.length) break;
    create3DFramedPortraitOnWall(
      firstFloorGroup,
      loader,
      girlsAll[gIdx++],
      -17.8 + col * 1.05,
      y1 + 1.15,
      -12.72,
      0,
      0.82,
      0.96,
      0xf472b6,
      1,
      "First Floor Girls' Hall · North Wall Gallery",
      2.1
    );
  }
  for (let col = 0; col < 6; col++) {
    if (gIdx >= girlsAll.length) break;
    create3DFramedPortraitOnWall(
      firstFloorGroup,
      loader,
      girlsAll[gIdx++],
      -17.8 + col * 1.05,
      y1 + 1.15,
      2.12,
      Math.PI,
      0.82,
      0.96,
      0xf472b6,
      1,
      "First Floor Girls' Hall · South Wall Gallery",
      2.1
    );
  }

  // 6. FIRST FLOOR NE CLASSROOM: ALL 28 DRAWINGS & HOMEWORK PULLED FROM RUBBLE
  createWingBannerIn3D(
    firstFloorGroup,
    `FIRST FLOOR CLASSROOMS · 28 DRAWINGS & HOMEWORK PULLED FROM THE RUBBLE`,
    `کلاس‌های طبقه اول · ۲۸ برگ نقاشی و مشق بیرون کشیده شده از زیر آوار مدرسه`,
    13.75,
    y1 + 3.22,
    -7.64,
    Math.PI,
    7.4,
    '#1e1b18',
    '#fcd34d'
  );

  let dIdx = 0;
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 9; col++) {
      if (dIdx >= drawingsList.length) break;
      const dx = 9.35 + col * 1.06;
      const dy = y1 + 1.18 + row * 1.08;
      create3DRubbleDrawingOnWall(
        firstFloorGroup,
        loader,
        drawingsList[dIdx++],
        dx,
        dy,
        -7.64,
        Math.PI,
        0.92,
        0.98,
        1,
        'First Floor North-East Classroom · Rubble Drawings & Homework Archive',
        1.95
      );
    }
  }
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 5; col++) {
      if (dIdx >= drawingsList.length) break;
      const dz = -8.25 - col * 0.96;
      const dy = y1 + 1.18 + row * 1.08;
      create3DRubbleDrawingOnWall(
        firstFloorGroup,
        loader,
        drawingsList[dIdx++],
        8.72,
        dy,
        dz,
        Math.PI / 2,
        0.86,
        0.98,
        1,
        'First Floor North-East Classroom · Rubble Drawings & Homework Archive',
        1.95
      );
    }
  }
}

export function loadChildrenAndBuildInWorldMemorial() {
  if (typeof CHILDREN !== 'undefined' && Array.isArray(CHILDREN) && CHILDREN.length > 0) {
    appState.childrenList = CHILDREN;
    appState.teachersList = typeof TEACHERS !== 'undefined' && Array.isArray(TEACHERS) ? TEACHERS : [];
    appState.drawingsList = typeof DRAWINGS !== 'undefined' && Array.isArray(DRAWINGS) ? DRAWINGS : [];
    populate3DSchoolPortraitsAndDrawings();
    return;
  }

  if (typeof fetch === 'undefined') return;
  fetch('children.json')
    .then((r) => r.json())
    .then((data) => {
      appState.childrenList = data.map((c) => ({
        ...c,
        name: c.name || c.full_name_en,
        nameFa: c.nameFa || c.full_name_fa,
        photoPath: c.photoPath || c.photo_path || (c.photoGrid ? `images/children/child_${c.photoGrid}.jpg` : null),
      }));
      populate3DSchoolPortraitsAndDrawings();
    })
    .catch((err) => console.warn('Could not load children.json for 3D frames:', err));
}

export function init3DPortraitRaycaster() {
  if (!appState.renderer) return;
  const raycaster = new THREE.Raycaster();
  const pointerNDC = new THREE.Vector2();
  appState.raycaster = raycaster;
  appState.pointerNDC = pointerNDC;
  const dom = appState.renderer.domElement;

  dom.addEventListener('pointerdown', (e) => {
    appState.pointerDownPos.x = e.clientX;
    appState.pointerDownPos.y = e.clientY;
  });

  dom.addEventListener('pointermove', (e) => {
    if (appState.clickable3DArtifacts.length === 0) return;
    const rect = dom.getBoundingClientRect();
    pointerNDC.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    pointerNDC.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(pointerNDC, appState.camera);
    const hits = raycaster.intersectObjects(appState.clickable3DArtifacts, false);
    dom.style.cursor = hits.length > 0 && hits[0].object.visible ? 'pointer' : 'grab';
  });

  dom.addEventListener('pointerup', (e) => {
    const dist = Math.hypot(
      e.clientX - appState.pointerDownPos.x,
      e.clientY - appState.pointerDownPos.y
    );
    if (dist > 6 || appState.clickable3DArtifacts.length === 0) return;

    const rect = dom.getBoundingClientRect();
    pointerNDC.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    pointerNDC.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(pointerNDC, appState.camera);

    const hits = raycaster.intersectObjects(appState.clickable3DArtifacts, false);
    if (hits.length > 0) {
      const hitObj = hits[0].object;
      if (hitObj.userData && hitObj.userData.item) {
        appState.callbacks.openArtifactInspector?.(hitObj.userData);
      }
    }
  });
}
