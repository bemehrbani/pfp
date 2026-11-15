/**
 * Guided 8-Station Director's Cut Tour, Cinema Witness Interludes,
 * cancel-safe run gate (`AbortController` + timer tracking), WebAudio room atmosphere,
 * background score ducking, and live HTTP 206 vs. bounded recording-mode PiP loading.
 */
import * as THREE from 'three';

import { appState } from '../state.js';
import {
  MEDIA_ASSET_VERSION,
  GUIDED_TOUR_STOPS,
  IN_WORLD_SCREEN_SPECS,
  WALKTHROUGH_VISUAL_CONFIG,
  SPOT_ARCHIVAL_AUDIO,
  WALKTHROUGH_BOOKENDS,
  WALKTHROUGH_INTERLUDES,
  ROOM_ATMOSPHERE_PROFILES,
} from '../data/tour-config.js';
import { I18N_DATA, NARRATOR_PROFILES } from '../data/i18n.js';
import { setTemporalCondition } from '../engine/core.js';
import { sampleGuidedTourCamera, triggerCameraAnimation } from '../engine/camera-rig.js';
import { setCutawayMode } from '../scene/school-world.js';
import {
  ensureInWorldScreenVideoElement,
  pauseAllInWorldVideos,
  seekInWorldScreensDeterministic,
} from '../scene/in-world-screens.js';

let tourRunSeq = 0;
let supportsDisplayTransition;

/**
 * Aborts the active Guided Tour run and clears every pending outer or nested timer.
 */
export function cancelActiveTourRun() {
  const run = appState.activeTourRun;
  if (!run) return;
  run.cancelled = true;
  try {
    run.controller.abort();
  } catch (_) {}
  for (const timerId of run.timers) {
    clearTimeout(timerId);
  }
  run.timers.clear();
  appState.activeTourRun = null;
}

/**
 * Starts a fresh cancel-safe Guided Tour run, cancelling any prior run first.
 */
export function beginNewTourRun() {
  cancelActiveTourRun();
  const controller = new AbortController();
  const run = {
    id: ++tourRunSeq,
    controller,
    signal: controller.signal,
    cancelled: false,
    timers: new Set(),
  };
  appState.activeTourRun = run;
  return run;
}

export function isTourRunActive(run) {
  return Boolean(run && !run.cancelled && !run.signal.aborted && appState.activeTourRun === run);
}

/**
 * Schedules a timeout bound to `run`; automatically cleared if `cancelActiveTourRun()` fires.
 */
export function scheduleTourTimer(run, delayMs, callback) {
  if (!isTourRunActive(run)) return null;
  const timerId = setTimeout(() => {
    run.timers.delete(timerId);
    if (!isTourRunActive(run)) return;
    callback();
  }, delayMs);
  run.timers.add(timerId);
  run.signal.addEventListener(
    'abort',
    () => {
      clearTimeout(timerId);
      run.timers.delete(timerId);
    },
    { once: true }
  );
  return timerId;
}

/**
 * Applies `media/walkthrough_pip/manifest.json` data onto `WALKTHROUGH_VISUAL_CONFIG`.
 * Supports both array-per-station entries (`[{ file, captions }]`) and `stations` object maps.
 */
export function applyPipManifestData(data, targetConfig = WALKTHROUGH_VISUAL_CONFIG) {
  if (!data || typeof data !== 'object' || !targetConfig) return;
  const stationsMap = data.stations && typeof data.stations === 'object' ? data.stations : null;

  Object.keys(targetConfig).forEach((hotspotId) => {
    const topEntry = data[hotspotId];
    const stationEntry = stationsMap ? stationsMap[hotspotId] : null;

    if (Array.isArray(topEntry) && topEntry.length > 0) {
      const first = topEntry[0];
      const reel = first && (first.file || first.video);
      if (typeof reel === 'string' && reel.trim()) {
        targetConfig[hotspotId].pipReel = reel.trim();
      }
      const cap = first && (first.captions || first.caption);
      if (cap && typeof cap === 'object') {
        targetConfig[hotspotId].pipCaption = {
          ...targetConfig[hotspotId].pipCaption,
          ...cap,
        };
      }
      targetConfig[hotspotId].pipReels = topEntry;
      return;
    }

    const objEntry =
      topEntry && typeof topEntry === 'object' && !Array.isArray(topEntry) ? topEntry : stationEntry;
    if (!objEntry || typeof objEntry !== 'object') return;

    const reel = objEntry.video || objEntry.file;
    if (typeof reel === 'string' && reel.trim()) {
      targetConfig[hotspotId].pipReel = reel.trim();
    }
    const cap = objEntry.caption || objEntry.captions;
    if (cap && typeof cap === 'object') {
      targetConfig[hotspotId].pipCaption = {
        ...targetConfig[hotspotId].pipCaption,
        ...cap,
      };
    }
  });
}

export async function initWalkthroughPipManifest() {
  if (typeof fetch === 'undefined') return;
  try {
    const resp = await fetch('media/walkthrough_pip/manifest.json', { cache: 'no-store' });
    if (!resp.ok) return;
    const data = await resp.json();
    applyPipManifestData(data, WALKTHROUGH_VISUAL_CONFIG);
  } catch (_) {
    // Manifest is optional; built-in verified reels remain active.
  }
}

/**
 * Returns direct HTTP 206 streamable URLs in live browser sessions (`!appState.recordingMode`),
 * and deduplicated Blob object URLs in headless Playwright recording mode (`?recording=1`).
 */
export async function resolvePipVideoSrc(reelUrl) {
  if (!reelUrl) return '';
  if (appState.pipBlobCache.has(reelUrl)) {
    return appState.pipBlobCache.get(reelUrl);
  }
  if (!appState.recordingMode) {
    return reelUrl;
  }
  if (appState.pipInflightCache.has(reelUrl)) {
    return appState.pipInflightCache.get(reelUrl);
  }

  const task = (async () => {
    try {
      const resp = await fetch(reelUrl);
      if (!resp.ok) return reelUrl;
      const blob = await resp.blob();
      const blobUrl = URL.createObjectURL(blob);
      appState.pipBlobCache.set(reelUrl, blobUrl);
      return blobUrl;
    } catch (_) {
      return reelUrl;
    } finally {
      appState.pipInflightCache.delete(reelUrl);
    }
  })();

  appState.pipInflightCache.set(reelUrl, task);
  return task;
}

/**
 * Executes `worker(url, index)` over `urls` with bounded concurrency (`<= 4` by default).
 */
export async function preloadUrlsBounded(urls, worker, concurrency = 4) {
  const queue = Array.from(urls || []);
  if (queue.length === 0) return;
  const limit = Math.max(1, Math.min(concurrency || 4, queue.length));
  let cursor = 0;
  const runners = Array.from({ length: limit }, async () => {
    while (cursor < queue.length) {
      const idx = cursor++;
      await worker(queue[idx], idx);
    }
  });
  await Promise.all(runners);
}

function withMediaVersion(url) {
  if (!url) return '';
  return url.includes('?') ? url : `${url}?v=${MEDIA_ASSET_VERSION}`;
}

export async function preloadAllWalkthroughPipBlobs() {
  const pipUrls = Object.values(WALKTHROUGH_VISUAL_CONFIG)
    .map((c) => withMediaVersion(c.pipReel))
    .filter(Boolean);
  const screenUrls = IN_WORLD_SCREEN_SPECS.map((s) => `media/walkthrough_pip/${s.file}.mp4?v=${MEDIA_ASSET_VERSION}`);
  const interludeUrls = Object.values(WALKTHROUGH_INTERLUDES).map((c) => withMediaVersion(c.src));
  const all = Array.from(new Set([...pipUrls, ...screenUrls, ...interludeUrls]));
  const prevMode = appState.recordingMode;
  appState.recordingMode = true;
  try {
    await preloadUrlsBounded(all, (u) => resolvePipVideoSrc(u), 4);
  } finally {
    appState.recordingMode = prevMode;
  }
}

export function rampBackgroundScoreVolume(targetVol) {
  appState.backgroundScoreTargetVol = Math.max(0, Math.min(1, targetVol));
  if (!appState.backgroundScoreAudio) return;
  if (appState.backgroundScoreFadeTimer) {
    clearInterval(appState.backgroundScoreFadeTimer);
    appState.backgroundScoreFadeTimer = null;
  }
  appState.backgroundScoreFadeTimer = setInterval(() => {
    const audio = appState.backgroundScoreAudio;
    if (!audio) {
      clearInterval(appState.backgroundScoreFadeTimer);
      appState.backgroundScoreFadeTimer = null;
      return;
    }
    const cur = audio.volume;
    const diff = appState.backgroundScoreTargetVol - cur;
    if (Math.abs(diff) <= 0.02) {
      audio.volume = appState.backgroundScoreTargetVol;
      if (appState.backgroundScoreTargetVol <= 0.001 && !audio.paused) {
        audio.pause();
      }
      clearInterval(appState.backgroundScoreFadeTimer);
      appState.backgroundScoreFadeTimer = null;
    } else {
      audio.volume = Math.max(0, Math.min(1, cur + Math.sign(diff) * 0.036));
    }
  }, 24);
}

export function ensureBackgroundScorePlaying(phase = 'voice') {
  if (!appState.voiceNarrationEnabled || typeof Audio === 'undefined') return;
  if (!appState.backgroundScoreAudio) {
    const score = new Audio('media/audio/memorial_ambient_loop.mp3?v=20261112c');
    score.loop = true;
    score.preload = 'auto';
    score.volume = 0.04;
    appState.backgroundScoreAudio = score;
  }
  const volByPhase = {
    archival: 0.21,
    delay: 0.34,
    transition: 0.35,
    voice: 0.27,
  };
  const desired = volByPhase[phase] !== undefined ? volByPhase[phase] : 0.27;
  if (appState.backgroundScoreAudio.paused) {
    appState.backgroundScoreAudio.play().catch(() => {});
  }
  rampBackgroundScoreVolume(desired);
}

export function pauseBackgroundScore(resetToStart = false) {
  const audio = appState.backgroundScoreAudio;
  if (!audio) return;
  if (resetToStart) {
    if (appState.backgroundScoreFadeTimer) {
      clearInterval(appState.backgroundScoreFadeTimer);
      appState.backgroundScoreFadeTimer = null;
    }
    audio.pause();
    try {
      audio.currentTime = 0;
    } catch (_) {}
    audio.volume = 0.04;
    return;
  }
  rampBackgroundScoreVolume(0.0);
}

export function isSpotAudioPlaying() {
  if (appState.narrationPhase === 'archival' && appState.archivalAudio && !appState.archivalAudio.paused) {
    return true;
  }
  if (appState.narrationPhase === 'delay') return true;
  if (appState.narrationPhase === 'voice' && appState.narrationAudio && !appState.narrationAudio.paused) {
    return true;
  }
  return false;
}

function canTransitionDisplay() {
  if (supportsDisplayTransition !== undefined) return supportsDisplayTransition;
  if (
    typeof window === 'undefined' ||
    !window.CSS?.supports?.('transition-behavior', 'allow-discrete') ||
    !document.body
  ) {
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

export function showAnimatedOverlay(el) {
  if (!el) return;
  el.style.transition = '';
  el.style.opacity = '';
  el.style.translate = '';
  el.removeAttribute('data-closing');
  el.hidden = false;
}

export async function hideAnimatedOverlay(el) {
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
      new Promise((r) => setTimeout(r, 450)),
    ]);
  }
  if (el.hasAttribute('data-closing')) {
    el.removeAttribute('data-closing');
    el.hidden = true;
  }
}

export function showStoryBanner() {
  if (typeof document === 'undefined') return;
  showAnimatedOverlay(document.getElementById('storyBanner'));
}

export async function hideStoryBanner() {
  if (typeof document === 'undefined') return;
  await hideAnimatedOverlay(document.getElementById('storyBanner'));
}

function applyWalkthroughStationOverlays(stopIdx) {
  if (typeof document === 'undefined') return;
  const stop = GUIDED_TOUR_STOPS[stopIdx];
  if (!stop) return;
  const vCfg = WALKTHROUGH_VISUAL_CONFIG[stop.hotspotId];
  if (!vCfg) return;
  const currentLang = appState.currentLang;

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

function getQuoteWindow(vCfg) {
  if (!vCfg || !vCfg.quote) return null;
  if (Array.isArray(vCfg.quote.window) && vCfg.quote.window.length === 2) {
    return { start: vCfg.quote.window[0], end: vCfg.quote.window[1] };
  }
  return { start: 0.54, end: 0.68 };
}

export function updateWalkthroughVisualOverlaysLive(stopIdx, progress) {
  if (!appState.isGuidedTour || appState.deterministicWalkthroughRender || typeof document === 'undefined') {
    return;
  }
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
  if (pipCard && !pipCard.hidden) {
    if (pipVideo && !pipVideo.paused) pipVideo.pause();
    pipCard.hidden = true;
  }

  const quoteEl = document.getElementById('walkthroughQuoteCallout');
  const qw = getQuoteWindow(vCfg);
  const shouldShowQuote = Boolean(qw) && progress >= qw.start && progress <= qw.end;
  if (quoteEl) {
    if (shouldShowQuote && (quoteEl.hidden || quoteEl.hasAttribute('data-closing'))) {
      showAnimatedOverlay(quoteEl);
    } else if (!shouldShowQuote && !quoteEl.hidden && !quoteEl.hasAttribute('data-closing')) {
      hideAnimatedOverlay(quoteEl);
    }
  }
}

export function smoothWindowAlpha(p, inStart, inEnd, outStart, outEnd) {
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

export function setWalkthroughProgress(progress) {
  if (typeof document === 'undefined') return;
  const fill = document.getElementById('storyProgressFill');
  if (!fill) return;
  const clamped = Math.max(0, Math.min(1, progress || 0));
  fill.style.transform = `scaleX(${clamped.toFixed(4)})`;
}

export async function syncWalkthroughVisualsAtProgress(stopIdx, progress, totalStationSec) {
  appState.deterministicWalkthroughRender = true;
  appState.isGuidedTour = true;
  appState.isAnimatingCamera = false;
  appState.tourManualCameraOverride = false;
  appState.currentTourIndex = stopIdx;

  const stop = GUIDED_TOUR_STOPS[stopIdx];
  if (!stop) return;
  const currentLang = appState.currentLang;
  const t = I18N_DATA[currentLang] || I18N_DATA.en;
  const hData = t.hotspots && t.hotspots[stop.hotspotId];
  const vCfg = WALKTHROUGH_VISUAL_CONFIG[stop.hotspotId];

  document.body.classList.add('walkthrough-mode');
  if (appState.markersGroup) appState.markersGroup.visible = false;
  showStoryBanner();

  setTemporalCondition(stop.temporal);
  const sliderEl = document.getElementById('timelineSlider');
  if (sliderEl) sliderEl.value = stop.temporal;
  if (stop.temporal < 0.5 && typeof stop.cutawayMode === 'number') {
    setCutawayMode(stop.cutawayMode);
  }

  const badgeEl = document.getElementById('storyStepBadge');
  if (badgeEl) {
    const shortBadge = stop.shortBadge && (stop.shortBadge[currentLang] || stop.shortBadge.en);
    badgeEl.textContent = shortBadge || stop.badge[currentLang] || stop.badge.en;
  }
  const titleEl = document.getElementById('storyTitle');
  if (titleEl && hData) {
    titleEl.textContent = hData.title.replace(/^[0-9۰-۹]+\.\s*/, '');
  }

  setWalkthroughProgress(progress);
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
  if (pipCard) {
    pipCard.hidden = true;
  }

  const quoteEl = document.getElementById('walkthroughQuoteCallout');
  if (quoteEl) {
    quoteEl.removeAttribute('data-closing');
    quoteEl.style.transition = 'none';
    const qw = getQuoteWindow(vCfg);
    const qAlpha = qw
      ? smoothWindowAlpha(
          progress,
          qw.start,
          Math.min(qw.end, qw.start + 0.06),
          Math.max(qw.start, qw.end - 0.06),
          qw.end
        )
      : 0;
    if (qAlpha <= 0.002) {
      quoteEl.hidden = true;
    } else {
      quoteEl.hidden = false;
      quoteEl.style.opacity = qAlpha.toFixed(3);
      quoteEl.style.translate = `-50% ${((1 - qAlpha) * 8).toFixed(1)}px`;
    }
  }

  const sampled = sampleGuidedTourCamera(stopIdx, progress);
  if (sampled && appState.camera && appState.controls) {
    appState.camera.position.copy(sampled.pos);
    appState.controls.target.copy(sampled.lookAt);
    appState.controls.update();
  }

  await seekInWorldScreensDeterministic(stop.hotspotId, progress, totalStationSec || 60.0);
  appState.callbacks.updateHotspotPositions?.();
  if (appState.renderer && appState.scene && appState.camera) {
    appState.renderer.render(appState.scene, appState.camera);
  }
}

export function resetWalkthroughIdleTimer() {
  if (typeof document === 'undefined') return;
  document.body.classList.remove('walkthrough-idle');
  if (appState.walkthroughIdleTimer) {
    clearTimeout(appState.walkthroughIdleTimer);
    appState.walkthroughIdleTimer = null;
  }
  if (!appState.isGuidedTour) return;
  appState.walkthroughIdleTimer = setTimeout(() => {
    if (appState.isGuidedTour && isSpotAudioPlaying()) {
      document.body.classList.add('walkthrough-idle');
    }
  }, 3500);
}

export function updateStoryAudioButtonUI(isPlaying) {
  if (typeof document === 'undefined') return;
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

function scheduleMorningBirdsong(birdGainTarget) {
  if (appState.ambientBirdTimer) {
    clearTimeout(appState.ambientBirdTimer);
    appState.ambientBirdTimer = null;
  }
  if (!birdGainTarget || birdGainTarget <= 0 || !appState.ambientAudioCtx) return;

  const triggerChirp = () => {
    const ctx = appState.ambientAudioCtx;
    if (!ctx || ctx.state !== 'running' || !isSpotAudioPlaying()) return;
    try {
      const now = ctx.currentTime;
      const notes = [2480 + Math.random() * 260, 2860 + Math.random() * 280];
      notes.forEach((baseFreq, i) => {
        const t0 = now + i * 0.16;
        const osc = ctx.createOscillator();
        const g = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(baseFreq, t0);
        osc.frequency.exponentialRampToValueAtTime(baseFreq * 1.14, t0 + 0.07);
        osc.frequency.exponentialRampToValueAtTime(baseFreq * 0.96, t0 + 0.14);
        g.gain.setValueAtTime(0.0001, t0);
        g.gain.linearRampToValueAtTime(birdGainTarget, t0 + 0.03);
        g.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.15);
        osc.connect(g);
        g.connect(ctx.destination);
        osc.start(t0);
        osc.stop(t0 + 0.17);
      });
    } catch (_) {}
    appState.ambientBirdTimer = setTimeout(triggerChirp, 4800 + Math.random() * 3400);
  };

  appState.ambientBirdTimer = setTimeout(triggerChirp, 1600 + Math.random() * 1800);
}

function triggerMemorialBellHarmonic() {
  const ctx = appState.ambientAudioCtx;
  if (!ctx) return;
  try {
    const now = ctx.currentTime;
    [523.25, 783.99].forEach((freq, idx) => {
      const osc = ctx.createOscillator();
      const g = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, now);
      const peak = idx === 0 ? 0.011 : 0.0045;
      g.gain.setValueAtTime(0.0001, now);
      g.gain.linearRampToValueAtTime(peak, now + 0.08);
      g.gain.exponentialRampToValueAtTime(0.0001, now + 4.2);
      osc.connect(g);
      g.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 4.4);
    });
  } catch (_) {}
}

export function startMemorialAmbientPad(hotspotId) {
  if (typeof window === 'undefined') return;
  try {
    const profile = ROOM_ATMOSPHERE_PROFILES[hotspotId] || ROOM_ATMOSPHERE_PROFILES.rainbow_staircase;
    if (!appState.ambientAudioCtx) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (!AudioContextClass) return;
      const ctx = new AudioContextClass();
      appState.ambientAudioCtx = ctx;

      const gainNode = ctx.createGain();
      gainNode.gain.setValueAtTime(0.0001, ctx.currentTime);
      appState.ambientGainNode = gainNode;

      const padFilter = ctx.createBiquadFilter();
      padFilter.type = 'lowpass';
      padFilter.frequency.setValueAtTime(profile.padCutoff, ctx.currentTime);
      appState.ambientPadFilter = padFilter;

      appState.ambientOscillators = profile.freqs.map((f, idx) => {
        const osc = ctx.createOscillator();
        osc.type = idx % 2 === 0 ? 'sine' : 'triangle';
        osc.frequency.setValueAtTime(f, ctx.currentTime);
        const oscGain = ctx.createGain();
        oscGain.gain.setValueAtTime(idx === 0 ? 0.34 : 0.17, ctx.currentTime);
        osc.connect(oscGain);
        oscGain.connect(padFilter);
        osc.start();
        return osc;
      });

      padFilter.connect(gainNode);
      gainNode.connect(ctx.destination);

      const sampleRate = ctx.sampleRate || 44100;
      const bufLen = sampleRate * 4;
      const noiseBuf = ctx.createBuffer(1, bufLen, sampleRate);
      const out = noiseBuf.getChannelData(0);
      let b0 = 0;
      let b1 = 0;
      let b2 = 0;
      for (let i = 0; i < bufLen; i++) {
        const white = Math.random() * 2 - 1;
        b0 = 0.99765 * b0 + white * 0.099046;
        b1 = 0.963 * b1 + white * 0.2965164;
        b2 = 0.57 * b2 + white * 1.0526913;
        out[i] = (b0 + b1 + b2 + white * 0.1848) * 0.12;
      }
      const fadeSamples = Math.floor(sampleRate * 0.15);
      for (let i = 0; i < fadeSamples; i++) {
        const t = i / fadeSamples;
        out[i] = out[i] * t + out[bufLen - fadeSamples + i] * (1 - t);
      }

      const noiseSrc = ctx.createBufferSource();
      noiseSrc.buffer = noiseBuf;
      noiseSrc.loop = true;

      const breezeFilter = ctx.createBiquadFilter();
      breezeFilter.type = 'bandpass';
      breezeFilter.frequency.setValueAtTime(profile.breezeFreq, ctx.currentTime);
      breezeFilter.Q.setValueAtTime(profile.breezeQ, ctx.currentTime);
      appState.ambientBreezeFilter = breezeFilter;

      const breezeGain = ctx.createGain();
      breezeGain.gain.setValueAtTime(0.0001, ctx.currentTime);
      appState.ambientBreezeGain = breezeGain;

      noiseSrc.connect(breezeFilter);
      breezeFilter.connect(breezeGain);
      breezeGain.connect(ctx.destination);
      noiseSrc.start();
    }

    const ctx = appState.ambientAudioCtx;
    if (ctx.state === 'suspended') {
      ctx.resume();
    }

    const now = ctx.currentTime;
    appState.ambientOscillators.forEach((osc, idx) => {
      const targetFreq = profile.freqs[idx] || profile.freqs[0];
      osc.frequency.cancelScheduledValues(now);
      osc.frequency.exponentialRampToValueAtTime(Math.max(40, targetFreq), now + 1.2);
    });
    if (appState.ambientPadFilter) {
      appState.ambientPadFilter.frequency.cancelScheduledValues(now);
      appState.ambientPadFilter.frequency.linearRampToValueAtTime(profile.padCutoff, now + 1.2);
    }
    if (appState.ambientGainNode) {
      appState.ambientGainNode.gain.cancelScheduledValues(now);
      appState.ambientGainNode.gain.linearRampToValueAtTime(profile.padGain, now + 1.6);
    }
    if (appState.ambientBreezeFilter && appState.ambientBreezeGain) {
      appState.ambientBreezeFilter.frequency.cancelScheduledValues(now);
      appState.ambientBreezeFilter.frequency.linearRampToValueAtTime(profile.breezeFreq, now + 1.2);
      appState.ambientBreezeFilter.Q.setValueAtTime(profile.breezeQ, now);
      appState.ambientBreezeGain.gain.cancelScheduledValues(now);
      appState.ambientBreezeGain.gain.linearRampToValueAtTime(profile.breezeGain, now + 1.6);
    }

    scheduleMorningBirdsong(profile.birdGain);
    if (profile.chime) {
      triggerMemorialBellHarmonic();
    }
  } catch (_) {}
}

export function stopMemorialAmbientPad() {
  try {
    if (appState.ambientBirdTimer) {
      clearTimeout(appState.ambientBirdTimer);
      appState.ambientBirdTimer = null;
    }
    const ctx = appState.ambientAudioCtx;
    if (ctx) {
      const now = ctx.currentTime;
      if (appState.ambientGainNode) {
        appState.ambientGainNode.gain.cancelScheduledValues(now);
        appState.ambientGainNode.gain.linearRampToValueAtTime(0.0001, now + 1.0);
      }
      if (appState.ambientBreezeGain) {
        appState.ambientBreezeGain.gain.cancelScheduledValues(now);
        appState.ambientBreezeGain.gain.linearRampToValueAtTime(0.0001, now + 1.0);
      }
    }
  } catch (_) {}
}

export function pauseSpotNarration() {
  if (appState.narrationPhaseTimer) {
    clearTimeout(appState.narrationPhaseTimer);
    appState.narrationPhaseTimer = null;
    appState.narrationPhase = 'voice';
  }
  if (appState.archivalAudio && !appState.archivalAudio.paused) {
    appState.archivalAudio.pause();
  }
  if (appState.narrationAudio && !appState.narrationAudio.paused) {
    appState.narrationAudio.pause();
  }
  pauseBackgroundScore(false);
  pauseAllInWorldVideos(false);
  stopMemorialAmbientPad();
  updateStoryAudioButtonUI(false);
  if (typeof document !== 'undefined') {
    const listenBtn = document.getElementById('modalListenBtn');
    if (listenBtn) {
      listenBtn.textContent = '🎧 Listen to Room Voiceover';
    }
  }
}

export function resumeSpotNarration(fallbackHotspotId) {
  const hotspotId = appState.activeNarrationHotspot || fallbackHotspotId;
  if (!hotspotId) return;
  appState.voiceNarrationEnabled = true;

  if (
    appState.narrationPhase === 'archival' &&
    appState.archivalAudio &&
    appState.archivalAudio.src &&
    !appState.archivalAudio.ended
  ) {
    ensureBackgroundScorePlaying('archival');
    startMemorialAmbientPad(hotspotId);
    appState.archivalAudio.play().catch(() => {});
    updateStoryAudioButtonUI(true);
    return;
  }
  if (
    appState.narrationPhase === 'voice' &&
    appState.narrationAudio &&
    appState.narrationAudio.src &&
    !appState.narrationAudio.ended
  ) {
    ensureBackgroundScorePlaying('voice');
    startMemorialAmbientPad(hotspotId);
    appState.narrationAudio.play().catch(() => {});
    updateStoryAudioButtonUI(true);
    return;
  }
  playSpotNarration(hotspotId);
}

export function getGuidedTourAudioProgress() {
  const stop = GUIDED_TOUR_STOPS[appState.currentTourIndex];
  const hotspotId = appState.activeNarrationHotspot || (stop && stop.hotspotId) || '';
  const archCfg = SPOT_ARCHIVAL_AUDIO[hotspotId];
  const archDur = archCfg
    ? appState.archivalAudio &&
      Number.isFinite(appState.archivalAudio.duration) &&
      appState.archivalAudio.duration > 0
      ? appState.archivalAudio.duration
      : archCfg.expectedDur
    : 0.85;
  const voiceDur =
    appState.narrationAudio &&
    Number.isFinite(appState.narrationAudio.duration) &&
    appState.narrationAudio.duration > 0
      ? appState.narrationAudio.duration
      : 55;
  const totalDur = Math.max(1, archDur + voiceDur);

  if (appState.narrationPhase === 'archival' && appState.archivalAudio) {
    return Math.min(1, (appState.archivalAudio.currentTime || 0) / totalDur);
  }
  if (appState.narrationPhase === 'delay') {
    return Math.min(1, archDur / totalDur);
  }
  if (appState.narrationPhase === 'voice' && appState.narrationAudio) {
    return Math.min(1, (archDur + (appState.narrationAudio.currentTime || 0)) / totalDur);
  }
  if (appState.tourStepStartTime > 0 && typeof performance !== 'undefined') {
    return Math.min(1, (performance.now() - appState.tourStepStartTime) / 60000);
  }
  return 0;
}

export function stopSpotNarration(opts = {}) {
  const keepBackground = Boolean(opts && opts.keepBackground);
  if (appState.guidedTourAutoAdvanceTimer) {
    clearTimeout(appState.guidedTourAutoAdvanceTimer);
    appState.guidedTourAutoAdvanceTimer = null;
  }
  if (appState.narrationPhaseTimer) {
    clearTimeout(appState.narrationPhaseTimer);
    appState.narrationPhaseTimer = null;
  }
  appState.narrationPhase = 'idle';
  appState.activeNarrationHotspot = null;

  if (appState.archivalAudio) {
    appState.archivalAudio.onended = null;
    appState.archivalAudio.onerror = null;
    appState.archivalAudio.pause();
    try {
      appState.archivalAudio.currentTime = 0;
    } catch (_) {}
  }
  if (appState.narrationAudio) {
    appState.narrationAudio.onended = null;
    appState.narrationAudio.onerror = null;
    appState.narrationAudio.pause();
    try {
      appState.narrationAudio.currentTime = 0;
    } catch (_) {}
  }
  if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
  if (!keepBackground) {
    pauseBackgroundScore(true);
    pauseAllInWorldVideos(true);
    stopMemorialAmbientPad();
  }
  updateStoryAudioButtonUI(false);
  if (typeof document !== 'undefined') {
    const listenBtn = document.getElementById('modalListenBtn');
    if (listenBtn) {
      listenBtn.textContent = '🎧 Listen to Room Voiceover';
    }
  }
}

export function emitTourTimelineEvent(type, extra = {}) {
  if (typeof window === 'undefined') return;
  if (!window.__tourEvents) window.__tourEvents = [];
  window.__tourEvents.push(Object.assign({ type, name: type, t: performance.now() }, extra));
}

export function applyBookendTexts() {
  if (typeof document === 'undefined') return;
  const lang = appState.currentLang || 'en';
  const p = WALKTHROUGH_BOOKENDS.prologue;
  const e = WALKTHROUGH_BOOKENDS.epilogue;
  const setTxt = (id, dict) => {
    const el = document.getElementById(id);
    if (el && dict) el.textContent = dict[lang] || dict.en;
  };
  setTxt('prologueKicker', p.kicker);
  setTxt('prologueTitle', p.title);
  setTxt('prologueCoords', p.coords);
  setTxt('prologueNote', p.note);
  setTxt('epilogueKicker', e.kicker);
  setTxt('epilogueTitle', e.title);
  setTxt('epilogueCoords', e.coords);
  setTxt('epilogueNote', e.note);
  setTxt('btnSkipInterlude', WALKTHROUGH_BOOKENDS.skipBtn);
}

export function hideAllBookendsAndInterludes() {
  if (appState.bookendTimer) {
    clearTimeout(appState.bookendTimer);
    appState.bookendTimer = null;
  }
  if (typeof document === 'undefined') {
    appState.activeInterludeState = null;
    return;
  }
  const pro = document.getElementById('walkthroughPrologueOverlay');
  const epi = document.getElementById('walkthroughEpilogueOverlay');
  if (pro) {
    pro.classList.remove('is-fading');
    pro.hidden = true;
  }
  if (epi) {
    epi.classList.remove('is-fading');
    epi.hidden = true;
  }

  const ov = document.getElementById('cinemaInterludeOverlay');
  const vid = document.getElementById('cinemaInterludeVideo');
  const rup = document.getElementById('interludeRuptureCard');
  if (vid) {
    vid.onended = null;
    vid.onerror = null;
    vid.ontimeupdate = null;
    try {
      vid.pause();
    } catch (_) {}
  }
  if (rup) rup.hidden = true;
  if (ov) {
    ov.classList.remove('is-fading');
    ov.hidden = true;
  }
  if (appState.activeInterludeState && appState.activeInterludeState.timer) {
    clearTimeout(appState.activeInterludeState.timer);
  }
  appState.activeInterludeState = null;
}

export function finishActiveInterlude() {
  if (!appState.activeInterludeState) return;
  const { onDone, timer, run } = appState.activeInterludeState;
  if (timer) clearTimeout(timer);
  appState.activeInterludeState = null;

  const ov = typeof document !== 'undefined' ? document.getElementById('cinemaInterludeOverlay') : null;
  const vid = typeof document !== 'undefined' ? document.getElementById('cinemaInterludeVideo') : null;
  if (vid) {
    vid.onended = null;
    vid.onerror = null;
    vid.ontimeupdate = null;
    try {
      vid.pause();
    } catch (_) {}
  }
  const schedule = (ms, fn) => (run ? scheduleTourTimer(run, ms, fn) : setTimeout(fn, ms));

  if (ov) {
    ov.classList.add('is-fading');
    schedule(440, () => {
      if (!appState.activeInterludeState && ov) {
        ov.hidden = true;
        ov.classList.remove('is-fading');
      }
    });
  }
  if (typeof onDone === 'function') {
    schedule(360, () => {
      if (appState.isGuidedTour) onDone();
    });
  }
}

export async function playCinemaInterlude(afterHotspotId, onDone) {
  const cfg = WALKTHROUGH_INTERLUDES[afterHotspotId];
  const run = appState.activeTourRun;
  if (!cfg || !appState.isGuidedTour || (run && !isTourRunActive(run))) {
    if (typeof onDone === 'function' && appState.isGuidedTour) onDone();
    return;
  }

  hideAllBookendsAndInterludes();
  applyBookendTexts();

  const lang = appState.currentLang || 'en';
  const ov = document.getElementById('cinemaInterludeOverlay');
  const vid = document.getElementById('cinemaInterludeVideo');
  const kickerEl = document.getElementById('interludeKicker');
  const subEl = document.getElementById('interludeSubtitleText');
  const ctxEl = document.getElementById('interludeContextLine');
  const progEl = document.getElementById('interludeProgressFill');
  const rupEl = document.getElementById('interludeRuptureCard');
  const rupTimeEl = document.getElementById('interludeRuptureTime');
  const rupTitleEl = document.getElementById('interludeRuptureTitle');

  if (!ov || !vid) {
    if (typeof onDone === 'function') onDone();
    return;
  }

  hideAnimatedOverlay(document.getElementById('walkthroughContextStamp'));
  hideAnimatedOverlay(document.getElementById('walkthroughQuoteCallout'));
  pauseAllInWorldVideos(false);
  stopMemorialAmbientPad();
  rampBackgroundScoreVolume(0.015);

  ov.setAttribute('data-aspect', cfg.aspect || 'portrait');
  ov.setAttribute('data-tone', cfg.tone || 'pre');
  if (kickerEl) kickerEl.textContent = (cfg.kicker && (cfg.kicker[lang] || cfg.kicker.en)) || '';
  if (ctxEl) ctxEl.textContent = (cfg.context && (cfg.context[lang] || cfg.context.en)) || '';
  if (subEl) subEl.textContent = '';
  if (progEl) progEl.style.width = '0%';
  if (rupEl) rupEl.hidden = true;

  const versionedSrc = withMediaVersion(cfg.src);
  const resolvedUrl = await resolvePipVideoSrc(versionedSrc);
  if (!appState.isGuidedTour || (run && !isTourRunActive(run))) return;

  vid.src = resolvedUrl || versionedSrc;
  vid.muted = false;
  vid.volume = appState.voiceNarrationEnabled ? 1.0 : 0.0;
  vid.currentTime = 0;

  appState.activeInterludeState = { cfg, onDone, timer: null, run };
  ov.classList.remove('is-fading');
  ov.hidden = false;

  vid.ontimeupdate = () => {
    const cur = vid.currentTime || 0;
    const dur = Number.isFinite(vid.duration) && vid.duration > 0 ? vid.duration : 15;
    if (progEl) {
      progEl.style.width = `${Math.min(100, (cur / dur) * 100).toFixed(1)}%`;
    }
    if (cfg.ruptureWindow && rupEl) {
      const inRup = cur >= cfg.ruptureWindow.s && cur <= cfg.ruptureWindow.e;
      rupEl.hidden = !inRup;
      if (inRup) {
        if (rupTimeEl) rupTimeEl.textContent = cfg.ruptureWindow.time[lang] || cfg.ruptureWindow.time.en;
        if (rupTitleEl) rupTitleEl.textContent = cfg.ruptureWindow.title[lang] || cfg.ruptureWindow.title.en;
        if (appState.damageSliderValue < 0.5) {
          setTemporalCondition(1.0);
          const sl = document.getElementById('timelineSlider');
          if (sl) sl.value = 1.0;
        }
      }
    }
    if (subEl && Array.isArray(cfg.cues)) {
      const cue = cfg.cues.find((c) => cur >= c.s && cur <= c.e);
      subEl.textContent = cue ? cue[lang] || cue.en || '' : '';
    }
  };

  vid.onended = () => finishActiveInterlude();
  vid.onerror = () => finishActiveInterlude();

  appState.activeInterludeState.timer = run
    ? scheduleTourTimer(run, 48000, () => finishActiveInterlude())
    : setTimeout(() => finishActiveInterlude(), 48000);

  vid
    .play()
    .then(() => {
      emitTourTimelineEvent('interlude_start', { interludeId: cfg.id, afterHotspotId, src: cfg.src });
    })
    .catch(() => {
      vid.muted = true;
      vid
        .play()
        .then(() => {
          emitTourTimelineEvent('interlude_start', {
            interludeId: cfg.id,
            afterHotspotId,
            src: cfg.src,
            mutedFallback: true,
          });
        })
        .catch(() => finishActiveInterlude());
    });
}

export function playSpotNarration(hotspotId) {
  stopSpotNarration({ keepBackground: true });
  if (!appState.voiceNarrationEnabled || typeof Audio === 'undefined') return;

  const run = appState.isGuidedTour ? appState.activeTourRun : null;
  const scheduleScoped = (ms, fn) => (run ? scheduleTourTimer(run, ms, fn) : setTimeout(fn, ms));

  appState.activeNarrationHotspot = hotspotId;
  const prof =
    NARRATOR_PROFILES[appState.activeVoiceProfile] ||
    (appState.currentLang === 'fa'
      ? NARRATOR_PROFILES.mostafa_fa
      : appState.currentLang === 'fi'
        ? NARRATOR_PROFILES.mostafa_fi
        : NARRATOR_PROFILES.mostafa_en);
  const narrationVersion = '20261115a';
  const primarySrc = `media/narration/${prof.dir}/${prof.prefix}_${hotspotId}.mp3?v=${narrationVersion}`;
  const fallbackBase =
    prof.fallbackDir === '.'
      ? 'media/narration'
      : `media/narration/${prof.fallbackDir || 'voices/leila_en'}`;
  const fallbackSrc = `${fallbackBase}/${prof.prefix}_${hotspotId}.mp3?v=${narrationVersion}`;

  if (!appState.narrationAudio) {
    appState.narrationAudio = new Audio();
  }
  if (!appState.archivalAudio) {
    appState.archivalAudio = new Audio();
  }
  const narrationAudio = appState.narrationAudio;
  const archivalAudio = appState.archivalAudio;

  const speedSelect = typeof document !== 'undefined' ? document.getElementById('narrationSpeedSelect') : null;
  if (speedSelect) {
    appState.narrationRate = parseFloat(speedSelect.value) || 1.0;
  }

  narrationAudio.preload = 'auto';
  narrationAudio.src = primarySrc;
  narrationAudio.playbackRate = appState.narrationRate;
  if ('preservesPitch' in narrationAudio) narrationAudio.preservesPitch = true;
  if ('webkitPreservesPitch' in narrationAudio) narrationAudio.webkitPreservesPitch = true;
  narrationAudio.load();

  startMemorialAmbientPad(hotspotId);
  updateStoryAudioButtonUI(true);
  resetWalkthroughIdleTimer();

  const listenBtn = typeof document !== 'undefined' ? document.getElementById('modalListenBtn') : null;
  if (listenBtn) {
    listenBtn.textContent = '⏸ Pause Room Voiceover';
  }

  narrationAudio.onended = () => {
    appState.narrationPhase = 'idle';
    updateStoryAudioButtonUI(false);
    setWalkthroughProgress(1);
    if (typeof document !== 'undefined') {
      document.body.classList.remove('walkthrough-idle');
    }
    if (listenBtn) {
      listenBtn.textContent = '🎧 Listen to Room Voiceover';
    }
    const evidenceModalOpen =
      typeof document !== 'undefined' &&
      Boolean(document.getElementById('evidenceModal')?.classList.contains('visible'));

    if (appState.isGuidedTour && (!run || isTourRunActive(run)) && !evidenceModalOpen) {
      const hasInterlude = Boolean(WALKTHROUGH_INTERLUDES[hotspotId]);
      if (appState.currentTourIndex < GUIDED_TOUR_STOPS.length - 1) {
        if (!hasInterlude) {
          ensureBackgroundScorePlaying('transition');
        }
        appState.guidedTourAutoAdvanceTimer = scheduleScoped(900, () => {
          if (!appState.isGuidedTour) return;
          const advanceNext = () => {
            if (!appState.isGuidedTour) return;
            appState.currentTourIndex += 1;
            renderGuidedTourStep(appState.currentTourIndex, true);
          };
          if (hasInterlude) {
            playCinemaInterlude(hotspotId, advanceNext);
          } else {
            advanceNext();
          }
        });
      } else {
        ensureBackgroundScorePlaying('transition');
        rampBackgroundScoreVolume(0.38);
        appState.guidedTourAutoAdvanceTimer = scheduleScoped(900, () => {
          if (!appState.isGuidedTour) return;
          applyBookendTexts();
          const epi = document.getElementById('walkthroughEpilogueOverlay');
          hideStoryBanner();
          hideAnimatedOverlay(document.getElementById('walkthroughContextStamp'));
          if (epi) {
            epi.classList.remove('is-fading');
            epi.hidden = false;
          }
          emitTourTimelineEvent('epilogue_start', {
            durationMs: WALKTHROUGH_BOOKENDS.epilogue.durationMs,
          });
          appState.bookendTimer = scheduleScoped(WALKTHROUGH_BOOKENDS.epilogue.durationMs, () => {
            if (epi) epi.classList.add('is-fading');
            scheduleScoped(650, () => {
              emitTourTimelineEvent('tour_complete', {});
              stopGuidedTour();
              appState.callbacks.openVowModal?.();
            });
          });
        });
      }
    } else {
      pauseBackgroundScore(true);
      pauseAllInWorldVideos(true);
      stopMemorialAmbientPad();
    }
  };

  narrationAudio.onerror = () => {
    if (narrationAudio.src.indexOf(fallbackSrc) === -1) {
      narrationAudio.src = fallbackSrc;
      narrationAudio.playbackRate = appState.narrationRate;
      if (appState.narrationPhase === 'voice') {
        narrationAudio.play().catch(() => {});
      }
    }
  };

  const launchVoiceover = () => {
    if (appState.activeNarrationHotspot !== hotspotId) return;
    if (run && !isTourRunActive(run)) return;
    appState.narrationPhase = 'voice';
    ensureBackgroundScorePlaying('voice');
    narrationAudio.playbackRate = appState.narrationRate;
    narrationAudio
      .play()
      .then(() => {
        emitTourTimelineEvent('station_voice_start', {
          hotspotId,
          profile: appState.activeVoiceProfile,
        });
      })
      .catch(() => {
        appState.narrationPhase = 'idle';
        pauseBackgroundScore(false);
        stopMemorialAmbientPad();
        updateStoryAudioButtonUI(false);
      });
  };

  const archivalCfg = SPOT_ARCHIVAL_AUDIO[hotspotId];
  if (archivalCfg) {
    appState.narrationPhase = 'archival';
    ensureBackgroundScorePlaying('archival');
    archivalAudio.src = `media/narration/archival/${archivalCfg.file}?v=${narrationVersion}`;
    archivalAudio.volume = 0.88;
    archivalAudio.playbackRate = 1.0;
    archivalAudio.onended = () => {
      if (appState.activeNarrationHotspot !== hotspotId) return;
      appState.narrationPhase = 'delay';
      ensureBackgroundScorePlaying('delay');
      appState.narrationPhaseTimer = scheduleScoped(380, launchVoiceover);
    };
    archivalAudio.onerror = () => {
      if (appState.activeNarrationHotspot !== hotspotId) return;
      launchVoiceover();
    };
    archivalAudio.play().catch(() => {
      launchVoiceover();
    });
  } else {
    appState.narrationPhase = 'delay';
    ensureBackgroundScorePlaying('delay');
    appState.narrationPhaseTimer = scheduleScoped(850, launchVoiceover);
  }
}

export function startGuidedTour() {
  const run = beginNewTourRun();
  appState.isGuidedTour = true;
  appState.deterministicWalkthroughRender = false;
  appState.currentTourIndex = 0;
  appState.tourManualCameraOverride = false;
  hideAllBookendsAndInterludes();
  appState.callbacks.closeModal?.();
  appState.callbacks.closeVowModal?.();
  appState.callbacks.closeArtifactInspector?.();

  document.body.classList.add('walkthrough-mode');
  if (appState.markersGroup) appState.markersGroup.visible = false;
  const tourBtn = document.getElementById('btnGuidedTour');
  if (tourBtn) tourBtn.classList.add('active');
  resetWalkthroughIdleTimer();

  setTemporalCondition(0.0);
  const sl = document.getElementById('timelineSlider');
  if (sl) sl.value = 0.0;
  setCutawayMode(0);
  if (appState.camera && appState.controls) {
    appState.camera.position.set(7.5, 9.2, 22.5);
    appState.controls.target.set(2.5, 2.0, 2.5);
    appState.controls.update();
  }
  triggerCameraAnimation(new THREE.Vector3(4.5, 2.75, 13.8), new THREE.Vector3(3.2, 2.05, 4.0));

  applyBookendTexts();
  const pro = document.getElementById('walkthroughPrologueOverlay');
  if (pro) {
    pro.classList.remove('is-fading');
    pro.hidden = false;
  }
  ensureBackgroundScorePlaying('delay');
  startMemorialAmbientPad('courtyard_lines');
  emitTourTimelineEvent('prologue_start', { durationMs: WALKTHROUGH_BOOKENDS.prologue.durationMs });

  appState.bookendTimer = scheduleTourTimer(run, WALKTHROUGH_BOOKENDS.prologue.durationMs, () => {
    if (!appState.isGuidedTour) return;
    if (pro) pro.classList.add('is-fading');
    scheduleTourTimer(run, 620, () => {
      if (pro) {
        pro.hidden = true;
        pro.classList.remove('is-fading');
      }
      if (!appState.isGuidedTour) return;
      showStoryBanner();
      renderGuidedTourStep(0, true);
    });
  });
}

export function stopGuidedTour() {
  cancelActiveTourRun();
  appState.isGuidedTour = false;
  appState.deterministicWalkthroughRender = false;
  appState.tourManualCameraOverride = false;
  appState.activeInWorldRunKey = '';
  hideAllBookendsAndInterludes();

  if (appState.walkthroughIdleTimer) {
    clearTimeout(appState.walkthroughIdleTimer);
    appState.walkthroughIdleTimer = null;
  }
  if (typeof document !== 'undefined') {
    document.body.classList.remove('walkthrough-mode', 'walkthrough-idle');
    if (appState.markersGroup) appState.markersGroup.visible = true;
    const tourBtn = document.getElementById('btnGuidedTour');
    if (tourBtn) tourBtn.classList.remove('active');
    const pipVideo = document.getElementById('walkthroughPipVideo');
    if (pipVideo) pipVideo.pause();
    hideAnimatedOverlay(document.getElementById('walkthroughContextStamp'));
    hideAnimatedOverlay(document.getElementById('walkthroughPipCard'));
    hideAnimatedOverlay(document.getElementById('walkthroughQuoteCallout'));
    hideStoryBanner();
  }
  setWalkthroughProgress(0);
  stopSpotNarration({ keepBackground: false });
}

export function jumpGuidedTourStep(nextIdx) {
  beginNewTourRun();
  appState.isGuidedTour = true;
  hideAllBookendsAndInterludes();
  showStoryBanner();
  appState.currentTourIndex = nextIdx;
  renderGuidedTourStep(nextIdx, true);
}

export function renderGuidedTourStep(idx, speakNow) {
  const stop = GUIDED_TOUR_STOPS[idx];
  if (!stop) return;
  const currentLang = appState.currentLang;
  const t = I18N_DATA[currentLang] || I18N_DATA.en;
  const hData = t.hotspots[stop.hotspotId];

  appState.tourManualCameraOverride = false;
  appState.tourStepStartTime = typeof performance !== 'undefined' ? performance.now() : Date.now();
  setWalkthroughProgress(0);
  applyWalkthroughStationOverlays(idx);

  if (!appState.deterministicWalkthroughRender && typeof document !== 'undefined') {
    const pipCard = document.getElementById('walkthroughPipCard');
    const quoteEl = document.getElementById('walkthroughQuoteCallout');
    if (pipCard) pipCard.hidden = true;
    if (quoteEl) quoteEl.hidden = true;
    showAnimatedOverlay(document.getElementById('walkthroughContextStamp'));
    appState.inWorldScreens.forEach((sc) => {
      if (sc.hotspotId === stop.hotspotId) {
        sc.cueStartedInLiveRun = false;
        ensureInWorldScreenVideoElement(sc);
      }
    });
  }

  setTemporalCondition(stop.temporal);
  const sliderEl = typeof document !== 'undefined' ? document.getElementById('timelineSlider') : null;
  if (sliderEl) sliderEl.value = stop.temporal;
  if (stop.temporal < 0.5 && typeof stop.cutawayMode === 'number') {
    setCutawayMode(stop.cutawayMode);
  }

  triggerCameraAnimation(
    new THREE.Vector3(stop.camPos[0], stop.camPos[1], stop.camPos[2]),
    new THREE.Vector3(stop.lookAt[0], stop.lookAt[1], stop.lookAt[2])
  );

  if (typeof document !== 'undefined') {
    const badgeEl = document.getElementById('storyStepBadge');
    if (badgeEl) {
      const shortBadge = stop.shortBadge && (stop.shortBadge[currentLang] || stop.shortBadge.en);
      badgeEl.textContent = shortBadge || stop.badge[currentLang] || stop.badge.en;
    }
    const titleEl = document.getElementById('storyTitle');
    if (titleEl && hData) {
      titleEl.textContent = hData.title.replace(/^[0-9۰-۹]+\.\s*/, '');
    }
  }

  if (speakNow && appState.voiceNarrationEnabled) {
    playSpotNarration(stop.hotspotId);
  } else {
    updateStoryAudioButtonUI(false);
  }
}
