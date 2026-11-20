import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '../../../..');
const WEB_DIR = path.join(REPO_ROOT, 'PFP_Platform/web');
const PUB_DIR = path.join(WEB_DIR, 'public');
const RECON_DIR = path.join(PUB_DIR, 'js/reconstruction');

const EXPECTED_MODULES = [
  'state.js',
  'data/i18n.js',
  'data/tour-config.js',
  'engine/core.js',
  'engine/camera-rig.js',
  'scene/school-world.js',
  'scene/memorial-gallery.js',
  'scene/in-world-screens.js',
  'tour/tour-director.js',
  'ui/hud-modals-vow.js',
  'main.js',
];

async function importReconModule(relPath) {
  const fullPath = path.join(RECON_DIR, relPath);
  return import(pathToFileURL(fullPath).href);
}

test('1. Modular file layout & extracted CSS exist and wire cleanly in reconstruction.html', () => {
  const cssPath = path.join(PUB_DIR, 'css/reconstruction.css');
  assert.ok(fs.existsSync(cssPath), 'css/reconstruction.css should exist');
  assert.ok(fs.statSync(cssPath).size > 15000, 'css/reconstruction.css should contain extracted styles');

  for (const mod of EXPECTED_MODULES) {
    const full = path.join(RECON_DIR, mod);
    assert.ok(fs.existsSync(full), `Expected module missing: js/reconstruction/${mod}`);
  }

  const html = fs.readFileSync(path.join(PUB_DIR, 'reconstruction.html'), 'utf8');
  assert.match(html, /href="css\/reconstruction\.css\?v=/, 'reconstruction.html must link css/reconstruction.css');
  assert.match(
    html,
    /<script\s+type="module"\s+src="js\/reconstruction\/main\.js\?v=/,
    'reconstruction.html must load js/reconstruction/main.js as an ES module'
  );
  assert.doesNotMatch(html, /<style>[\s\S]{1000,}<\/style>/, 'Inline <style> monolith should be extracted');
});

test('2. applyPipManifestData handles real array-per-station manifest.json schema', async () => {
  const { WALKTHROUGH_VISUAL_CONFIG } = await importReconModule('data/tour-config.js');
  const { applyPipManifestData } = await importReconModule('tour/tour-director.js');

  const rawManifest = JSON.parse(
    fs.readFileSync(path.join(PUB_DIR, 'media/walkthrough_pip/manifest.json'), 'utf8')
  );
  assert.ok(Array.isArray(rawManifest.courtyard_lines), 'Real manifest uses array per station');

  const targetClone = structuredClone(WALKTHROUGH_VISUAL_CONFIG);
  targetClone.courtyard_lines.pipReel = 'placeholder.mp4';
  applyPipManifestData(rawManifest, targetClone);

  assert.equal(
    targetClone.courtyard_lines.pipReel,
    rawManifest.courtyard_lines[0].file,
    'Array station manifest entry should update pipReel'
  );
  assert.equal(
    targetClone.courtyard_lines.pipCaption.en,
    rawManifest.courtyard_lines[0].captions.en,
    'Array station manifest entry should update localized pipCaption'
  );
});

test('3. resolvePipVideoSrc uses direct HTTP 206 URLs in live mode and deduplicated bounded blobs in recording mode', async () => {
  const { appState } = await importReconModule('state.js');
  const { resolvePipVideoSrc, preloadUrlsBounded } = await importReconModule('tour/tour-director.js');

  let fetchCount = 0;
  const origFetch = globalThis.fetch;
  const origCreateObj = URL.createObjectURL;

  try {
    globalThis.fetch = async () => {
      fetchCount += 1;
      await new Promise((r) => setTimeout(r, 15));
      return {
        ok: true,
        blob: async () => new Blob(['video-bytes'], { type: 'video/mp4' }),
      };
    };
    URL.createObjectURL = () => `blob:mock-${fetchCount}`;

    appState.recordingMode = false;
    appState.pipBlobCache.clear();
    appState.pipInflightCache.clear();

    const liveUrl = await resolvePipVideoSrc('media/walkthrough_pip/01_sync_morning_queue.mp4');
    assert.equal(liveUrl, 'media/walkthrough_pip/01_sync_morning_queue.mp4');
    assert.equal(fetchCount, 0, 'Live mode must not fetch whole MP4 into Blob RAM');

    appState.recordingMode = true;
    const [u1, u2, u3] = await Promise.all([
      resolvePipVideoSrc('media/walkthrough_pip/test_clip.mp4'),
      resolvePipVideoSrc('media/walkthrough_pip/test_clip.mp4'),
      resolvePipVideoSrc('media/walkthrough_pip/test_clip.mp4'),
    ]);
    assert.equal(u1, u2);
    assert.equal(u2, u3);
    assert.equal(fetchCount, 1, 'Concurrent recording-mode calls for same URL must deduplicate');

    let active = 0;
    let maxActive = 0;
    const urls = Array.from({ length: 10 }, (_, i) => `clip_${i}.mp4`);
    await preloadUrlsBounded(
      urls,
      async () => {
        active += 1;
        maxActive = Math.max(maxActive, active);
        await new Promise((r) => setTimeout(r, 10));
        active -= 1;
      },
      4
    );
    assert.ok(maxActive <= 4, `Expected max concurrency <= 4, saw ${maxActive}`);
  } finally {
    globalThis.fetch = origFetch;
    URL.createObjectURL = origCreateObj;
    appState.recordingMode = false;
    appState.pipBlobCache.clear();
    appState.pipInflightCache.clear();
  }
});

test('4. Tour runId / AbortController gate cancels pending and nested timers cleanly', async () => {
  const { beginNewTourRun, cancelActiveTourRun, scheduleTourTimer } = await importReconModule('tour/tour-director.js');

  const events = [];
  const run = beginNewTourRun();
  scheduleTourTimer(run, 20, () => {
    events.push('outer');
    scheduleTourTimer(run, 20, () => {
      events.push('nested');
    });
  });

  cancelActiveTourRun();
  await new Promise((r) => setTimeout(r, 60));
  assert.deepEqual(events, [], 'Cancelled tour run must never fire pending or nested callbacks');
});

test('5. Zero dynamic .innerHTML assignments across all reconstruction modules', () => {
  const walkJs = (dir) => {
    const out = [];
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) out.push(...walkJs(full));
      else if (entry.name.endsWith('.js')) out.push(full);
    }
    return out;
  };

  const files = walkJs(RECON_DIR);
  assert.ok(files.length >= EXPECTED_MODULES.length);
  for (const file of files) {
    const src = fs.readFileSync(file, 'utf8');
    assert.doesNotMatch(
      src,
      /\.innerHTML\s*=/,
      `Forbidden .innerHTML sink found in ${path.relative(PUB_DIR, file)}`
    );
  }
});

test('6. Camera spline, cue window, smoothWindowAlpha, and Vow summary helpers preserve exact math', async () => {
  const { appState } = await importReconModule('state.js');
  const { sampleGuidedTourCameraCoords } = await importReconModule('engine/camera-rig.js');
  const { resolveInWorldCueWindow } = await importReconModule('scene/in-world-screens.js');
  const { smoothWindowAlpha } = await importReconModule('tour/tour-director.js');
  const { formatReconstructionVowSummary } = await importReconModule('ui/hud-modals-vow.js');

  const s0 = sampleGuidedTourCameraCoords(0, 0);
  assert.deepEqual(s0.pos, [9.0, 1.9, 8.25]);
  assert.deepEqual(s0.lookAt, [25.0, 1.9, 8.25]);

  // Stop 1 uses the smooth (Hermite) spline, so a waypoint is hit to within float rounding.
  const s1 = sampleGuidedTourCameraCoords(0, 0.34);
  [16.0, 1.9, 8.25].forEach((v, i) => assert.ok(Math.abs(s1.pos[i] - v) < 1e-9));
  [25.0, 1.9, 8.25].forEach((v, i) => assert.ok(Math.abs(s1.lookAt[i] - v) < 1e-9));

  const spec = { cueStartP: 0.1, cueEndP: 0.5, cueStartPFa: 0.2, cueEndPFa: 0.7, cueStartPFi: 0.15, cueEndPFi: 0.6 };
  appState.currentLang = 'en';
  assert.deepEqual(resolveInWorldCueWindow(spec), { start: 0.1, end: 0.5 });
  appState.currentLang = 'fa';
  assert.deepEqual(resolveInWorldCueWindow(spec), { start: 0.2, end: 0.7 });
  appState.currentLang = 'fi';
  assert.deepEqual(resolveInWorldCueWindow(spec), { start: 0.15, end: 0.6 });
  appState.currentLang = 'en';

  assert.equal(smoothWindowAlpha(0.5, 0.1, 0.2, 0.8, 0.9), 1);
  assert.equal(smoothWindowAlpha(0.05, 0.1, 0.2, 0.8, 0.9), 0);

  assert.equal(
    formatReconstructionVowSummary([
      'Accountability Vow — Legal & Judicial Counsel',
      'Accountability Vow — Forensic & OSINT Research',
    ]),
    'Accountability Vow — Legal & Judicial Counsel | Forensic & OSINT Research'
  );
});

test('7. Nginx configs disable stale caching on /js/reconstruction/ and /css/reconstruction.css, and files have zero BOM/mojibake', () => {
  for (const cfgName of ['nginx.conf', 'nginx.production.conf']) {
    const cfg = fs.readFileSync(path.join(WEB_DIR, cfgName), 'utf8');
    assert.match(cfg, /location\s+\^~\s+\/js\/reconstruction\//, `${cfgName} must guard /js/reconstruction/ with ^~`);
    assert.match(cfg, /location\s+=\s+\/css\/reconstruction\.css/, `${cfgName} must guard /css/reconstruction.css`);
  }

  const mojibakeRe = /â€”|â€“|Â¶|Â§|â€™|ChorzÃ³w|KoriÅ¡a|â†‘/;
  const checkFiles = [
    path.join(PUB_DIR, 'reconstruction.html'),
    path.join(PUB_DIR, 'css/reconstruction.css'),
    path.join(WEB_DIR, 'tools/walkthrough/README_ONBOARDING.md'),
    ...EXPECTED_MODULES.map((m) => path.join(RECON_DIR, m)),
  ];
  for (const f of checkFiles) {
    const buf = fs.readFileSync(f);
    assert.notEqual(
      buf.slice(0, 3).toString('hex'),
      'efbbbf',
      `UTF-8 BOM forbidden in ${path.relative(REPO_ROOT, f)}`
    );
    const txt = buf.toString('utf8');
    assert.doesNotMatch(txt, mojibakeRe, `Mojibake sequence detected in ${path.relative(REPO_ROOT, f)}`);
  }
});

test('8. Finnish (mostafa_fi) narrator profile, manifest, and all 8 audio files are present and wired', async () => {
  const { appState } = await importReconModule('state.js');
  const { NARRATOR_PROFILES, setLanguage } = await importReconModule('data/i18n.js');
  const { GUIDED_TOUR_STOPS } = await importReconModule('data/tour-config.js');

  assert.ok(NARRATOR_PROFILES.mostafa_fi, 'mostafa_fi profile must exist');
  assert.equal(NARRATOR_PROFILES.mostafa_fi.lang, 'fi');
  assert.equal(NARRATOR_PROFILES.mostafa_fi.dir, 'voices/mostafa_fi');

  const voicesManifest = JSON.parse(
    fs.readFileSync(path.join(PUB_DIR, 'media/narration/voices/manifest.json'), 'utf8')
  );
  assert.equal(voicesManifest.defaultByLang.fi, 'mostafa_fi');
  assert.equal(voicesManifest.profiles.mostafa_fi.stationsCount, 8);

  for (const stop of GUIDED_TOUR_STOPS) {
    const mp3 = path.join(PUB_DIR, `media/narration/voices/mostafa_fi/fi_${stop.hotspotId}.mp3`);
    assert.ok(fs.existsSync(mp3), `Missing Finnish voiceover: ${mp3}`);
    assert.ok(fs.statSync(mp3).size > 500000, `Unexpectedly small Finnish MP3: ${mp3}`);
  }

  setLanguage('fi');
  assert.equal(appState.currentLang, 'fi');
  assert.equal(appState.activeVoiceProfile, 'mostafa_fi');
  setLanguage('en');
  assert.equal(appState.activeVoiceProfile, 'mostafa_en');
});

test('9. Ctrl + drag look pivots the orbit target around the camera, keeping radius and clamping pitch', async () => {
  const { rotateTargetAroundCamera, LOOK_ELEVATION_LIMIT } = await importReconModule('engine/camera-rig.js');

  const camera = { x: 0, y: 0, z: 10 };
  const target = { x: 0, y: 0, z: 0 };
  const height = 1000;
  const step = (Math.PI * 2 * 10) / 1000; // 10 px of drag at a 1000 px viewport
  const radiusOf = (p) => Math.hypot(p.x - camera.x, p.y - camera.y, p.z - camera.z);

  // Drag right turns the view right: the pivot swings toward +X on the same radius.
  const right = rotateTargetAroundCamera(camera, target, 10, 0, height);
  assert.ok(Math.abs(right.x - 10 * Math.sin(step)) < 1e-9);
  assert.ok(Math.abs(right.z - (10 - 10 * Math.cos(step))) < 1e-9);
  assert.ok(Math.abs(radiusOf(right) - 10) < 1e-9);

  // Drag down turns the view down: the pivot drops below the camera.
  const down = rotateTargetAroundCamera(camera, target, 0, 10, height);
  assert.ok(down.y < 0);
  assert.ok(Math.abs(down.y - -10 * Math.sin(step)) < 1e-9);

  // Drag up aims the camera at the sky: the pivot rises above the camera.
  const up = rotateTargetAroundCamera(camera, target, 0, -10, height);
  assert.ok(up.y > 0);

  // Pitch clamps at the elevation limit instead of flipping over the camera.
  const flipped = rotateTargetAroundCamera(camera, target, 0, 5000, height);
  assert.ok(Math.abs(flipped.y - -10 * Math.sin(LOOK_ELEVATION_LIMIT)) < 1e-9);
  assert.ok(Math.abs(radiusOf(flipped) - 10) < 1e-9);

  // A collapsed radius (camera on target) must not produce NaN.
  const collapsed = rotateTargetAroundCamera(camera, { x: 0, y: 0, z: 9.99999 }, 200, 200, height);
  assert.deepEqual(collapsed, { x: 0, y: 0, z: 9.99999 });
});

