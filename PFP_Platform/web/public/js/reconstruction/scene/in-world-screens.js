/**
 * In-world 3D museum video screens & bilingual caption plaques mounted inside
 * the Shajareh Tayyebeh school rooms and courtyard.
 *
 * Memory & decoder optimization:
 * - At initial boot, all 16 screens load lightweight `.jpg` posters via `THREE.TextureLoader`
 *   (zero idle `1280×720` `<canvas>` backing stores and zero `<video>` decoders at startup).
 * - When a station becomes active (live tour, room voiceover, or deterministic seek),
 *   only that station's screens lazily allocate a `1280×720` `<canvas>` + `<video>` decoder.
 * - Inactive rooms release excess offscreen `<video>` elements (`<= 4` active decoders)
 *   while preserving their frozen end-frame or poster on the 3D wall.
 */
import * as THREE from 'three';

import { appState } from '../state.js';
import { IN_WORLD_SCREEN_SPECS, MEDIA_ASSET_VERSION } from '../data/tour-config.js';
import { FRAME_DECAL_GAP, makeDecalMaterial } from './frame-stack.js';

const MAX_POOLED_VIDEO_DECODERS = 4;

/**
 * Plaque faces. Vazirmatn and Source Sans 3 are the page's RTL and body fonts and
 * reconstruction.html already loads them; canvas text does not fetch them on its own,
 * so the plaque captions are repainted once the faces resolve.
 */
const PLAQUE_FA_FONT = '"Vazirmatn", Tahoma, sans-serif';
const PLAQUE_EN_FONT = '"Source Sans 3", "Segoe UI", system-ui, sans-serif';

const PLAQUE_FA_BADGE_SPEC = `700 20px ${PLAQUE_FA_FONT}`;
const PLAQUE_FA_CAPTION_SPEC = `500 22px ${PLAQUE_FA_FONT}`;
const PLAQUE_EN_BADGE_SPEC = `700 18px ${PLAQUE_EN_FONT}`;
const PLAQUE_EN_CAPTION_SPEC = `500 21px ${PLAQUE_EN_FONT}`;

export function wrapCanvasCaptionLines(ctx, text, maxWidth, maxLines) {
  const words = String(text || '')
    .trim()
    .split(/\s+/)
    .filter(Boolean);
  if (words.length === 0) return [];
  const lines = [];
  let current = words[0];
  for (let i = 1; i < words.length; i++) {
    const candidate = current + ' ' + words[i];
    if (ctx.measureText(candidate).width <= maxWidth) {
      current = candidate;
    } else {
      lines.push(current);
      current = words[i];
      if (lines.length >= maxLines - 1) {
        for (let j = i + 1; j < words.length; j++) {
          const nextTry = current + ' ' + words[j];
          if (ctx.measureText(nextTry).width <= maxWidth - 18) {
            current = nextTry;
          } else {
            current += '…';
            break;
          }
        }
        break;
      }
    }
  }
  if (lines.length < maxLines && current) {
    lines.push(current);
  }
  return lines;
}

export function renderInWorldPlaqueCanvas(screen) {
  if (!screen || !screen.plaqueCanvas) return;
  const canvas = screen.plaqueCanvas;
  const ctx = canvas.getContext('2d');
  const currentLang = appState.currentLang;
  const isFa = currentLang === 'fa';
  const langKey = ['en', 'fi', 'fa'].includes(currentLang) ? currentLang : 'en';

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = 'rgba(11, 16, 28, 0.96)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = screen.isFocal ? '#facc15' : '#94a3b8';
  ctx.lineWidth = screen.isFocal ? 4 : 2.5;
  ctx.strokeRect(3, 3, canvas.width - 6, canvas.height - 6);

  ctx.direction = isFa ? 'rtl' : 'ltr';
  ctx.textAlign = 'center';

  const badgeStr = (screen.spec.badge && (screen.spec.badge[langKey] || screen.spec.badge.en)) || '';
  const capStr = (screen.spec.caption && (screen.spec.caption[langKey] || screen.spec.caption.en)) || '';

  ctx.fillStyle = screen.isFocal ? '#fde047' : '#e2c074';
  ctx.font = isFa ? PLAQUE_FA_BADGE_SPEC : PLAQUE_EN_BADGE_SPEC;
  ctx.fillText(badgeStr, canvas.width / 2, 34);

  ctx.fillStyle = '#f8fafc';
  ctx.font = isFa ? PLAQUE_FA_CAPTION_SPEC : PLAQUE_EN_CAPTION_SPEC;
  const wrapped = wrapCanvasCaptionLines(ctx, capStr, canvas.width - 56, 2);
  if (wrapped.length === 1) {
    ctx.fillText(wrapped[0], canvas.width / 2, 86);
  } else if (wrapped.length >= 2) {
    ctx.fillText(wrapped[0], canvas.width / 2, 74);
    ctx.fillText(wrapped[1], canvas.width / 2, 108);
  }

  if (screen.plaqueTex) {
    screen.plaqueTex.needsUpdate = true;
  }
}

const SCREEN_CANVAS_W = 1280;

/**
 * Backing-canvas height for a screen. Stele screens use their own aspect so the texture maps
 * 1:1 onto the plane; every other screen keeps the 16:9 canvas.
 */
function screenCanvasHeight(screen) {
  const { w, h, style } = screen.spec;
  return style === 'stele' ? Math.round((SCREEN_CANVAS_W * h) / w) : 720;
}

/**
 * Letterbox (contain) fit: draws `src` as large as fits inside the canvas without changing
 * its aspect ratio, on a dark backdrop, so nothing is stretched or cropped.
 */
function drawContained(ctx, src, srcW, srcH, cw, ch) {
  ctx.fillStyle = '#0b0f1a';
  ctx.fillRect(0, 0, cw, ch);
  if (!srcW || !srcH) return;
  const scale = Math.min(cw / srcW, ch / srcH);
  const dw = srcW * scale;
  const dh = srcH * scale;
  ctx.drawImage(src, (cw - dw) / 2, (ch - dh) / 2, dw, dh);
}

function ensureInWorldScreenCanvas(screen) {
  if (!screen) return null;
  if (!screen.screenCanvas) {
    const screenCanvas = document.createElement('canvas');
    screenCanvas.width = SCREEN_CANVAS_W;
    screenCanvas.height = screenCanvasHeight(screen);
    const screenCtx = screenCanvas.getContext('2d');
    screenCtx.fillStyle = '#0f172a';
    screenCtx.fillRect(0, 0, screenCanvas.width, screenCanvas.height);
    if (screen.posterTex && screen.posterTex.image) {
      try {
        screenCtx.drawImage(screen.posterTex.image, 0, 0, screenCanvas.width, screenCanvas.height);
      } catch (_) {}
    }
    screen.screenCanvas = screenCanvas;
    screen.screenCtx = screenCtx;
    screen.canvasTex = new THREE.CanvasTexture(screenCanvas);
    screen.canvasTex.colorSpace = THREE.SRGBColorSpace;
  }
  return screen.screenCtx;
}

export function drawPosterToInWorldScreen(screen) {
  if (!screen || !screen.screenMat) return;
  if (screen.posterLoaded && screen.posterTex) {
    if (screen.screenCtx && screen.posterTex.image) {
      try {
        screen.screenCtx.drawImage(
          screen.posterTex.image, 0, 0, screen.screenCanvas.width, screen.screenCanvas.height
        );
        if (screen.canvasTex) screen.canvasTex.needsUpdate = true;
      } catch (_) {}
    }
    if (screen.screenMat.map !== screen.posterTex) {
      screen.screenMat.color.setHex(0xffffff);
      screen.screenMat.map = screen.posterTex;
      screen.screenMat.needsUpdate = true;
    }
    screen.usingCanvasTex = false;
    return;
  }
  screen.screenMat.color.setHex(0x0f172a);
  screen.screenMat.map = null;
  screen.screenMat.needsUpdate = true;
}

export function drawVideoToInWorldScreen(screen) {
  if (!screen || !screen.videoEl || !screen.screenMat) return false;
  if (screen.videoEl.readyState >= 2 && screen.videoEl.videoWidth > 0) {
    const ctx = ensureInWorldScreenCanvas(screen);
    if (!ctx) return false;
    try {
      drawContained(
        ctx, screen.videoEl, screen.videoEl.videoWidth, screen.videoEl.videoHeight,
        screen.screenCanvas.width, screen.screenCanvas.height
      );
      screen.canvasTex.needsUpdate = true;
      if (screen.screenMat.map !== screen.canvasTex) {
        screen.screenMat.color.setHex(0xffffff);
        screen.screenMat.map = screen.canvasTex;
        screen.screenMat.needsUpdate = true;
      }
      screen.usingCanvasTex = true;
      return true;
    } catch (_) {}
  }
  return false;
}

/**
 * Photo-slideshow screens (spec.images) have no <video>: the slides are painted onto the
 * same 1280x720 canvas texture a video would use, each held for spec.slideSec seconds.
 */
function ensureSlideshowImages(screen) {
  if (!screen.slideImages) {
    screen.slideImages = screen.spec.images.map((url) => {
      const img = new Image();
      img.decoding = 'async';
      img.src = `${url}?v=${MEDIA_ASSET_VERSION}`;
      return img;
    });
  }
  return screen.slideImages;
}

export function drawSlideshowToInWorldScreen(screen, elapsedSec) {
  if (!screen || !screen.screenMat || !screen.spec.images) return false;
  const imgs = ensureSlideshowImages(screen);
  const ctx = ensureInWorldScreenCanvas(screen);
  if (!ctx || imgs.length === 0) return false;
  const slideSec = screen.spec.slideSec || 3.5;
  const idx = Math.floor(Math.max(0, elapsedSec) / slideSec) % imgs.length;
  const img = imgs[idx];
  if (!img.complete || !img.naturalWidth) return false;
  try {
    drawContained(
      ctx, img, img.naturalWidth, img.naturalHeight,
      screen.screenCanvas.width, screen.screenCanvas.height
    );
  } catch (_) {
    return false;
  }
  screen.canvasTex.needsUpdate = true;
  if (screen.screenMat.map !== screen.canvasTex) {
    screen.screenMat.color.setHex(0xffffff);
    screen.screenMat.map = screen.canvasTex;
    screen.screenMat.needsUpdate = true;
  }
  screen.usingCanvasTex = true;
  return true;
}

export function setInWorldScreenFocalState(screen, isFocal) {
  if (!screen || screen.isFocal === isFocal) return;
  screen.isFocal = isFocal;
  if (screen.accentBarMat) {
    screen.accentBarMat.color.setHex(isFocal ? 0xfacc15 : 0x94a3b8);
  }
  if (screen.innerTrimMat) {
    screen.innerTrimMat.color.setHex(isFocal ? 0xeab308 : 0x64748b);
  }
  renderInWorldPlaqueCanvas(screen);
}

export function buildAllInWorldWalkthroughScreens() {
  appState.inWorldScreens.length = 0;
  const groupLookup = {
    preStrike: appState.preStrikeModelGroup,
    groundFloor: appState.groundFloorGroup,
    firstFloor: appState.firstFloorGroup,
    postStrike: appState.postStrikeModelGroup,
    memorial: appState.memorialBoardsGroup,
  };
  const bezelMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.55, metalness: 0.35 });
  const legMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.5, metalness: 0.55 });
  const posterLoader = new THREE.TextureLoader();

  // Screen and plaque decals ride FRAME_DECAL_GAP in front of their backing.
  const INNER_TRIM_DEPTH = 0.05;
  const SCREEN_PLANE_Z = INNER_TRIM_DEPTH / 2 + FRAME_DECAL_GAP;
  const PLAQUE_BACKING_DEPTH = 0.032;
  const PLAQUE_BACKING_Z = 0.004;
  const PLAQUE_PLANE_Z = PLAQUE_BACKING_Z + PLAQUE_BACKING_DEPTH / 2 + FRAME_DECAL_GAP;

  IN_WORLD_SCREEN_SPECS.forEach((spec) => {
    const parentGroup = groupLookup[spec.groupKey] || appState.preStrikeModelGroup;
    if (!parentGroup) return;

    const root = new THREE.Group();
    root.name = `InWorldScreen_${spec.id}`;
    root.position.set(spec.pos[0], spec.pos[1], spec.pos[2]);
    root.rotation.y = spec.rotY || 0;
    root.userData = { feature: 'in_world_video_screen', screenId: spec.id, hotspotId: spec.hotspotId };

    const isStele = spec.style === 'stele';
    let innerTrimMat = null;
    let accentBarMat = null;
    let screenPlaneZ = SCREEN_PLANE_Z;

    if (isStele) {
      // Same look as the Courtyard Memorial Avenue steles: dark slate slab with a gold rim,
      // standing on the ground (slab bottom at y = 0.14, so spec.pos[1] = 0.14 + slabH / 2).
      const STELE_SLAB_DEPTH = 0.1;
      const slab = new THREE.Mesh(
        new THREE.BoxGeometry(spec.w + 0.12, spec.h + 0.2, STELE_SLAB_DEPTH),
        new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.5 })
      );
      slab.castShadow = true;
      root.add(slab);
      const rim = new THREE.Mesh(
        new THREE.BoxGeometry(spec.w + 0.18, spec.h + 0.26, 0.07),
        new THREE.MeshBasicMaterial({ color: 0xd4a853 })
      );
      root.add(rim);
      screenPlaneZ = STELE_SLAB_DEPTH / 2 + FRAME_DECAL_GAP;
    } else {
      const outerFrame = new THREE.Mesh(
        new THREE.BoxGeometry(spec.w + 0.11, spec.h + 0.11, 0.045),
        bezelMat
      );
      outerFrame.castShadow = true;
      root.add(outerFrame);

      innerTrimMat = makeDecalMaterial({ color: 0x64748b, side: THREE.FrontSide });
      const innerTrim = new THREE.Mesh(
        new THREE.BoxGeometry(spec.w + 0.028, spec.h + 0.028, INNER_TRIM_DEPTH),
        innerTrimMat
      );
      root.add(innerTrim);

      accentBarMat = new THREE.MeshBasicMaterial({ color: 0x94a3b8 });
      const accentBar = new THREE.Mesh(
        new THREE.BoxGeometry(spec.w * 0.94, 0.028, 0.058),
        accentBarMat
      );
      accentBar.position.set(0, spec.h / 2 + 0.04, 0.006);
      root.add(accentBar);
    }

    const screenMat = makeDecalMaterial({
      color: 0x0f172a,
      side: THREE.FrontSide,
      toneMapped: false,
    });
    const screenPlane = new THREE.Mesh(new THREE.PlaneGeometry(spec.w, spec.h), screenMat);
    screenPlane.position.set(0, 0, screenPlaneZ);
    root.add(screenPlane);

    // spec.noPlaque: bare frame, no caption plaque underneath (plaqueCanvas stays null,
    // which renderInWorldPlaqueCanvas treats as "nothing to paint").
    let plaqueCanvas = null;
    let plaqueTex = null;
    if (!spec.noPlaque) {
      plaqueCanvas = document.createElement('canvas');
      plaqueCanvas.width = 1024;
      plaqueCanvas.height = 136;
      plaqueTex = new THREE.CanvasTexture(plaqueCanvas);
      plaqueTex.colorSpace = THREE.SRGBColorSpace;
      const plaqueW = Math.min(spec.w * 0.94, 3.1);
      const plaqueH = plaqueW * (136 / 1024);
      const plaqueBacking = new THREE.Mesh(
        new THREE.BoxGeometry(plaqueW + 0.04, plaqueH + 0.03, PLAQUE_BACKING_DEPTH),
        bezelMat
      );
      const plaqueY = -spec.h / 2 - 0.055 - plaqueH / 2 - 0.035;
      plaqueBacking.position.set(0, plaqueY, PLAQUE_BACKING_Z);
      root.add(plaqueBacking);

      const plaqueMesh = new THREE.Mesh(
        new THREE.PlaneGeometry(plaqueW, plaqueH),
        makeDecalMaterial({ map: plaqueTex, side: THREE.FrontSide, toneMapped: false })
      );
      plaqueMesh.position.set(0, plaqueY, PLAQUE_PLANE_Z);
      root.add(plaqueMesh);
    }

    if (spec.hasLegs) {
      const floorLocalY = (typeof spec.legFloorY === 'number' ? spec.legFloorY : 0.02) - spec.pos[1];
      const frameBottomY = -spec.h / 2 - 0.055;
      const legLen = Math.max(0.15, frameBottomY - floorLocalY);
      const legOffsetX = Math.max(0.55, spec.w * 0.34);
      [-legOffsetX, legOffsetX].forEach((lx) => {
        const post = new THREE.Mesh(new THREE.CylinderGeometry(0.028, 0.032, legLen, 10), legMat);
        post.position.set(lx, floorLocalY + legLen / 2, -0.01);
        post.castShadow = true;
        const base = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.025, 0.32), legMat);
        base.position.set(lx, floorLocalY + 0.0125, -0.01);
        root.add(post, base);
      });
    }

    parentGroup.add(root);

    const screenRecord = {
      id: spec.id,
      hotspotId: spec.hotspotId,
      slot: spec.slot,
      spec,
      root,
      screenMat,
      screenCanvas: null,
      screenCtx: null,
      canvasTex: null,
      usingCanvasTex: false,
      plaqueCanvas,
      plaqueTex,
      accentBarMat,
      innerTrimMat,
      posterUrl: spec.noPoster ? null : `media/walkthrough_pip/posters/${spec.file}.jpg?v=${MEDIA_ASSET_VERSION}`,
      videoUrl: spec.images ? null : `media/walkthrough_pip/${spec.file}.mp4?v=${MEDIA_ASSET_VERSION}`,
      slideImages: null,
      slideElapsed: 0,
      slideLastMs: 0,
      posterTex: null,
      posterLoaded: false,
      videoEl: null,
      videoReadyPromise: null,
      lastUsedAt: 0,
      cueStartedInLiveRun: false,
      isFocal: false,
    };

    renderInWorldPlaqueCanvas(screenRecord);

    if (screenRecord.posterUrl) {
      posterLoader.load(screenRecord.posterUrl, (tex) => {
        tex.colorSpace = THREE.SRGBColorSpace;
        screenRecord.posterTex = tex;
        screenRecord.posterLoaded = true;
        if (!screenRecord.usingCanvasTex) {
          drawPosterToInWorldScreen(screenRecord);
        }
      });
    }

    appState.inWorldScreens.push(screenRecord);
  });

  repaintPlaquesWhenFontsReady();
}

/**
 * Canvas text does not trigger a webfont download, so plaques painted at boot keep the
 * fallback face. Repaint them once the plaque faces resolve.
 */
function repaintPlaquesWhenFontsReady() {
  if (typeof document === 'undefined' || !document.fonts || !document.fonts.load) return;
  const specs = [
    { font: PLAQUE_FA_BADGE_SPEC, text: 'س' },
    { font: PLAQUE_FA_CAPTION_SPEC, text: 'س' },
    { font: PLAQUE_EN_BADGE_SPEC, text: 'A' },
    { font: PLAQUE_EN_CAPTION_SPEC, text: 'A' },
  ];
  try {
    Promise.all(specs.map((s) => document.fonts.load(s.font, s.text)))
      .then(() => refreshInWorldScreensLanguage())
      .catch(() => {});
  } catch (_) {}
}

export function refreshInWorldScreensLanguage() {
  appState.inWorldScreens.forEach((screen) => {
    renderInWorldPlaqueCanvas(screen);
  });
}

function detachScreenVideoDecoder(screen) {
  if (!screen || !screen.videoEl) return;
  const vid = screen.videoEl;
  try {
    vid.pause();
    vid.removeAttribute('src');
    vid.load();
    vid.remove();
  } catch (_) {}
  screen.videoEl = null;
  screen.videoReadyPromise = null;
}

function releaseInactiveInWorldDecoders(keepHotspotId) {
  const activeWithVideo = appState.inWorldScreens.filter((s) => Boolean(s.videoEl));
  if (activeWithVideo.length <= MAX_POOLED_VIDEO_DECODERS) return;

  const candidates = activeWithVideo
    .filter((s) => s.hotspotId !== keepHotspotId)
    .sort((a, b) => (a.lastUsedAt || 0) - (b.lastUsedAt || 0));

  let excess = activeWithVideo.length - MAX_POOLED_VIDEO_DECODERS;
  for (const sc of candidates) {
    if (excess <= 0) break;
    detachScreenVideoDecoder(sc);
    excess -= 1;
  }
}

export function ensureInWorldScreenVideoElement(screen) {
  if (!screen || typeof document === 'undefined' || !screen.videoUrl) return Promise.resolve(null);
  screen.lastUsedAt = typeof performance !== 'undefined' ? performance.now() : Date.now();
  if (screen.videoReadyPromise) {
    return screen.videoReadyPromise;
  }

  releaseInactiveInWorldDecoders(screen.hotspotId);

  let pool = document.getElementById('inWorldVideoPool');
  if (!pool && document.body) {
    pool = document.createElement('div');
    pool.id = 'inWorldVideoPool';
    pool.setAttribute('aria-hidden', 'true');
    pool.style.cssText =
      'position:fixed;left:0;bottom:0;width:2px;height:2px;opacity:0.001;pointer-events:none;overflow:hidden;z-index:-1;';
    document.body.appendChild(pool);
  }
  const vid = document.createElement('video');
  vid.muted = true;
  vid.defaultMuted = true;
  vid.playsInline = true;
  vid.setAttribute('playsinline', '');
  vid.setAttribute('webkit-playsinline', '');
  vid.loop = Boolean(screen.spec.loop) || !appState.isGuidedTour;
  vid.preload = 'auto';
  vid.width = 320;
  vid.height = 180;
  if (pool) pool.appendChild(vid);
  screen.videoEl = vid;

  const resolveSrc = appState.callbacks.resolvePipVideoSrc || ((url) => Promise.resolve(url));
  screen.videoReadyPromise = resolveSrc(screen.videoUrl).then(
    (resolvedSrc) =>
      new Promise((resolve) => {
        if (screen.videoEl !== vid) {
          resolve(null);
          return;
        }
        vid.src = resolvedSrc || screen.videoUrl;
        if (vid.readyState >= 2) {
          resolve(vid);
          return;
        }
        const finish = () => {
          vid.removeEventListener('loadeddata', finish);
          vid.removeEventListener('canplay', finish);
          vid.removeEventListener('error', finish);
          resolve(vid);
        };
        vid.addEventListener('loadeddata', finish);
        vid.addEventListener('canplay', finish);
        vid.addEventListener('error', finish);
        try {
          vid.load();
        } catch (_) {}
        setTimeout(finish, 2200);
      })
  );
  return screen.videoReadyPromise;
}

export function pauseAllInWorldVideos(restorePoster = false) {
  appState.inWorldScreens.forEach((screen) => {
    screen.cueStartedInLiveRun = false;
    setInWorldScreenFocalState(screen, false);
    if (screen.videoEl && !screen.videoEl.paused) {
      screen.videoEl.pause();
    }
    if (restorePoster) {
      drawPosterToInWorldScreen(screen);
      detachScreenVideoDecoder(screen);
    }
  });
}

export function resolveInWorldCueWindow(spec) {
  if (!spec) return { start: 0, end: 1 };
  const lang = appState.currentLang;
  let start = spec.cueStartP;
  let end = spec.cueEndP;
  if (lang === 'fa') {
    if (typeof spec.cueStartPFa === 'number') start = spec.cueStartPFa;
    if (typeof spec.cueEndPFa === 'number') end = spec.cueEndPFa;
  } else if (lang === 'fi') {
    if (typeof spec.cueStartPFi === 'number') start = spec.cueStartPFi;
    if (typeof spec.cueEndPFi === 'number') end = spec.cueEndPFi;
  }
  return {
    start: typeof start === 'number' && Number.isFinite(start) ? start : 0,
    end: typeof end === 'number' && Number.isFinite(end) ? end : 1,
  };
}

export function updateInWorldScreensLive(activeHotspotIdForScreens, progress) {
  if (appState.deterministicWalkthroughRender || typeof window === 'undefined') return;
  const prefersReduced =
    window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isGuidedTour = appState.isGuidedTour;
  const runKey = `${isGuidedTour ? 'tour' : 'spot'}:${activeHotspotIdForScreens || 'none'}`;

  if (runKey !== appState.activeInWorldRunKey) {
    appState.activeInWorldRunKey = runKey;
    appState.inWorldScreens.forEach((sc) => {
      sc.cueStartedInLiveRun = false;
      if (sc.hotspotId !== activeHotspotIdForScreens) {
        setInWorldScreenFocalState(sc, false);
        if (sc.videoEl && !sc.videoEl.paused) {
          sc.videoEl.pause();
        }
      } else {
        ensureInWorldScreenVideoElement(sc);
      }
    });
    releaseInactiveInWorldDecoders(activeHotspotIdForScreens);
  }

  if (!activeHotspotIdForScreens) return;

  const audioPlaying = Boolean(appState.callbacks.isSpotAudioPlaying?.());
  appState.inWorldScreens.forEach((sc) => {
    if (sc.hotspotId !== activeHotspotIdForScreens) return;
    sc.lastUsedAt = performance.now();
    const p = isGuidedTour ? progress : 0.35;
    const cue = resolveInWorldCueWindow(sc.spec);
    const isCueWindow = isGuidedTour ? p >= cue.start && p <= cue.end : true;
    setInWorldScreenFocalState(sc, isCueWindow);

    if (sc.spec.images) {
      // Slideshow clock: starts when the cue opens and only advances while narration plays,
      // mirroring how the muted videos pause with the audio.
      const nowMs = performance.now();
      const shouldRun = !isGuidedTour || p >= cue.start;
      if (!prefersReduced && shouldRun) {
        if (!sc.cueStartedInLiveRun) {
          sc.cueStartedInLiveRun = true;
          sc.slideElapsed = 0;
          sc.slideLastMs = nowMs;
        }
        if (audioPlaying) sc.slideElapsed += (nowMs - sc.slideLastMs) / 1000;
        sc.slideLastMs = nowMs;
      }
      drawSlideshowToInWorldScreen(sc, prefersReduced || !shouldRun ? 0 : sc.slideElapsed);
      return;
    }

    if (prefersReduced) {
      if (sc.videoEl && !sc.videoEl.paused) sc.videoEl.pause();
      drawPosterToInWorldScreen(sc);
      return;
    }

    ensureInWorldScreenVideoElement(sc);
    const vid = sc.videoEl;
    if (!vid) return;
    vid.loop = Boolean(sc.spec.loop) || !isGuidedTour;

    const shouldPlayNow = !isGuidedTour || p >= cue.start;
    if (shouldPlayNow) {
      if (!sc.cueStartedInLiveRun && vid.readyState >= 1) {
        sc.cueStartedInLiveRun = true;
        try {
          vid.currentTime = 0.04;
        } catch (_) {}
      }
      if (audioPlaying && vid.paused && !vid.ended) {
        vid.play().catch(() => {});
      } else if (!audioPlaying && !vid.paused) {
        vid.pause();
      }
      drawVideoToInWorldScreen(sc);
    } else {
      if (!vid.paused) vid.pause();
      if (vid.readyState >= 2) {
        if (Math.abs((vid.currentTime || 0) - 0.04) > 0.08) {
          try {
            vid.currentTime = 0.04;
          } catch (_) {}
        }
        drawVideoToInWorldScreen(sc);
      } else {
        drawPosterToInWorldScreen(sc);
      }
    }
  });
}

export async function seekInWorldScreensDeterministic(hotspotId, progress, totalStationSec) {
  const stationScreens = appState.inWorldScreens.filter((s) => s.hotspotId === hotspotId);
  appState.inWorldScreens.forEach((s) => {
    if (s.hotspotId !== hotspotId) {
      setInWorldScreenFocalState(s, false);
      if (s.videoEl && !s.videoEl.paused) s.videoEl.pause();
    }
  });
  releaseInactiveInWorldDecoders(hotspotId);

  await Promise.all(
    stationScreens.map(async (sc) => {
      const cue = resolveInWorldCueWindow(sc.spec);
      const isFocal = progress >= cue.start && progress <= cue.end;
      setInWorldScreenFocalState(sc, isFocal);

      if (sc.spec.images) {
        const elapsed = progress >= cue.start ? (progress - cue.start) * (totalStationSec || 60.0) : 0;
        const imgs = ensureSlideshowImages(sc);
        await Promise.all(imgs.map((img) => (img.decode ? img.decode().catch(() => {}) : null)));
        drawSlideshowToInWorldScreen(sc, elapsed);
        return;
      }

      const vid = await ensureInWorldScreenVideoElement(sc);
      if (!vid) {
        drawPosterToInWorldScreen(sc);
        return;
      }
      vid.loop = false;
      if (!vid.paused) vid.pause();

      const dur =
        Number.isFinite(vid.duration) && vid.duration > 0.4
          ? vid.duration
          : sc.spec.durationSec || 11.0;
      const safeDur = Math.max(0.8, dur - 0.08);
      let targetTime = 0.45;
      if (progress >= cue.start) {
        const elapsedOnCue = Math.max(0, (progress - cue.start) * (totalStationSec || 60.0));
        // spec.loop screens wrap around like they do live; the rest hold their last frame.
        targetTime = sc.spec.loop ? (0.4 + elapsedOnCue) % safeDur : Math.min(safeDur, 0.4 + elapsedOnCue);
      }

      if (Math.abs((vid.currentTime || 0) - targetTime) > 0.022) {
        await new Promise((resolve) => {
          const onSeeked = () => {
            vid.removeEventListener('seeked', onSeeked);
            resolve();
          };
          vid.addEventListener('seeked', onSeeked);
          try {
            vid.currentTime = targetTime;
          } catch (_) {
            vid.removeEventListener('seeked', onSeeked);
            resolve();
          }
          setTimeout(() => {
            vid.removeEventListener('seeked', onSeeked);
            resolve();
          }, 160);
        });
      }

      if (!drawVideoToInWorldScreen(sc)) {
        drawPosterToInWorldScreen(sc);
      }
    })
  );
}
