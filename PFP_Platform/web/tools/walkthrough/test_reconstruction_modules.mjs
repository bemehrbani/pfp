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
  assert.deepEqual(s0.pos, [4.5, 2.75, 13.8]);
  assert.deepEqual(s0.lookAt, [10.5, 1.3, 7.5]);

  const s1 = sampleGuidedTourCameraCoords(0, 0.14);
  assert.deepEqual(s1.pos, [5.8, 2.35, 11.4]);
  assert.deepEqual(s1.lookAt, [12.5, 0.75, 8.0]);

  const spec = { cueStartP: 0.1, cueEndP: 0.5, cueStartPFa: 0.2, cueEndPFa: 0.7 };
  appState.currentLang = 'en';
  assert.deepEqual(resolveInWorldCueWindow(spec), { start: 0.1, end: 0.5 });
  appState.currentLang = 'fa';
  assert.deepEqual(resolveInWorldCueWindow(spec), { start: 0.2, end: 0.7 });
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
