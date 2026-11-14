// Records the full 8-station Director's Cut guided walkthrough (Prologue + 8 Stations + 6 Cinema Interludes + Epilogue) via Playwright.
// Usage: node record_tour.mjs <lang:en|fa> <outputName> [maxStations] [voiceProfile]
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '../../../..');

const LANG = process.argv[2] || 'en';
const OUT_NAME = process.argv[3] || `pfp_walkthrough_${LANG}`;
const MAX_STATIONS = parseInt(process.argv[4] || '-1', 10);
const VOICE_PROFILE = process.argv[5] || '';
const PORT = process.env.PFP_PORT || '8123';
const OUT_DIR = process.env.PFP_OUT_DIR || path.join(REPO_ROOT, 'scratch/walkthrough_recordings');
fs.mkdirSync(OUT_DIR, { recursive: true });

const voiceParam = VOICE_PROFILE ? `&voice=${encodeURIComponent(VOICE_PROFILE)}` : '';
const BASE = `http://localhost:${PORT}/reconstruction.html?lang=${LANG}${voiceParam}&recording=1`;

const preExistingWebms = new Set(fs.readdirSync(OUT_DIR).filter((f) => f.endsWith('.webm')));

const browser = await chromium.launch({
  headless: true,
  args: [
    '--enable-webgl',
    '--ignore-gpu-blocklist',
    '--use-angle=metal',
    '--autoplay-policy=no-user-gesture-required',
  ],
});

const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  recordVideo: { dir: OUT_DIR, size: { width: 1920, height: 1080 } },
});

await context.addInitScript(() => {
  window.__tourEvents = [];
  document.addEventListener('DOMContentLoaded', () => {
    document.body.classList.add('walkthrough-mode', 'recording-mode');
  });
});

const page = await context.newPage();
const pageLog = [];
page.on('console', (m) => {
  if (m.type() === 'error') pageLog.push('console.error: ' + m.text().slice(0, 200));
});
page.on('pageerror', (e) => pageLog.push('pageerror: ' + String(e).slice(0, 200)));

const ctxStart = Date.now();
await page.goto(BASE, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(2600);

await page.evaluate(async () => {
  if (window.preloadAllWalkthroughPipBlobs) {
    try { await window.preloadAllWalkthroughPipBlobs(); } catch (_) {}
  }
});

const delta = await page.evaluate((ctxStartMs) => {
  const pn = performance.now();
  const wall = Date.now();
  return (wall - ctxStartMs) - pn;
}, ctxStart);

const tourStart = Date.now();
await page.evaluate(() => {
  if (typeof startGuidedTour === 'function') startGuidedTour();
});
console.log(`Director's Cut tour started (lang=${LANG}, voice=${VOICE_PROFILE || 'default'}, maxStations=${MAX_STATIONS}, delta=${delta.toFixed(1)}ms)`);

const deadline = Date.now() + (MAX_STATIONS < 0 ? 18 * 60 * 1000 : MAX_STATIONS * 120 * 1000);
let lastStateKey = '';
while (Date.now() < deadline) {
  const state = await page.evaluate(() => {
    const badge = document.getElementById('storyStepBadge')?.textContent || '';
    const interludeVis = !document.getElementById('cinemaInterludeOverlay')?.hidden;
    const interludeKicker = interludeVis ? (document.getElementById('interludeKicker')?.textContent || 'INTERLUDE') : '';
    const epilogueVis = !document.getElementById('walkthroughEpilogueOverlay')?.hidden;
    const vowVisible = Boolean(document.getElementById('vowModal')?.classList.contains('visible'));
    return { badge, interludeVis, interludeKicker, epilogueVis, vowVisible };
  }).catch(() => ({ badge: '', interludeVis: false, interludeKicker: '', epilogueVis: false, vowVisible: false }));

  const key = `${state.badge}|${state.interludeVis ? state.interludeKicker : ''}|${state.epilogueVis ? 'EPI' : ''}`;
  if (key !== lastStateKey) {
    if (state.epilogueVis) console.log('  [epilogue] Dedication card visible');
    else if (state.interludeVis) console.log(`  [interlude] ${state.interludeKicker}`);
    else if (state.badge) console.log(`  [station]   ${state.badge}`);
    lastStateKey = key;
  }

  if (state.vowVisible) {
    console.log('Vow modal appeared — holding 3.5s for graceful fadeout.');
    await page.waitForTimeout(3500);
    break;
  }

  if (MAX_STATIONS > 0 && !state.interludeVis) {
    const m = state.badge.match(/([0-9۰-۹]+)/);
    if (m) {
      const normalized = m[1].replace(/[۰-۹]/g, (d) => '۰۱۲۳۴۵۶۷۸۹'.indexOf(d));
      if (parseInt(normalized, 10) > MAX_STATIONS) {
        console.log('Reached maxStations + its interlude, stopping.');
        await page.waitForTimeout(1500);
        break;
      }
    }
  }

  await page.waitForTimeout(750);
}

const videoEndWall = Date.now();
const events = await page.evaluate(() => window.__tourEvents || []);
const logPath = path.join(OUT_DIR, `${OUT_NAME}.timeline.json`);
fs.writeFileSync(
  logPath,
  JSON.stringify({ lang: LANG, voice: VOICE_PROFILE || null, ctxStart, tourStart, videoEndWall, approxVideoSec: (videoEndWall - ctxStart) / 1000, delta, events, pageLog }, null, 2)
);
console.log('timeline saved:', logPath, `(${events.length} events)`);

const videoObj = page.video();
await context.close();
await browser.close();

let recordedPath = videoObj ? await videoObj.path().catch(() => null) : null;
if (!recordedPath || !fs.existsSync(recordedPath)) {
  const candidates = fs.readdirSync(OUT_DIR)
    .filter((f) => f.endsWith('.webm') && !preExistingWebms.has(f))
    .map((f) => ({ f, mtime: fs.statSync(path.join(OUT_DIR, f)).mtimeMs }))
    .sort((a, b) => b.mtime - a.mtime);
  if (candidates.length) recordedPath = path.join(OUT_DIR, candidates[0].f);
}

if (recordedPath && fs.existsSync(recordedPath)) {
  const dst = path.join(OUT_DIR, `${OUT_NAME}.webm`);
  if (recordedPath !== dst) {
    if (fs.existsSync(dst)) fs.unlinkSync(dst);
    fs.renameSync(recordedPath, dst);
  }
  console.log('video:', dst);
} else {
  console.error('ERROR: recorded .webm not found!');
  process.exit(1);
}
