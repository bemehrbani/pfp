/**
 * ES Module entry point for the Shajareh Tayyebeh Primary School 3D Spatial Reconstruction.
 * Wires cross-module callbacks, registers backwards-compatible `window` shims for
 * `site-nav.js`, `contact-modal.js`, and Playwright Director's Cut exporters (`record_tour.mjs`),
 * and starts the Three.js render loop.
 */
import * as THREE from 'three';

import { appState } from './state.js';
import { GUIDED_TOUR_STOPS } from './data/tour-config.js';
import {
  initI18n,
  setLanguage,
  selectNarratorByActor,
  setNarratorProfile,
} from './data/i18n.js';
import {
  initAmbientOcclusion,
  initThreeEngine,
  renderFrame,
  setTemporalCondition,
  useFrontFaceShadowCasters,
} from './engine/core.js';
import {
  sampleGuidedTourCamera,
  sampleGuidedTourCameraCoords,
  initKeyboardWalkControls,
  initLookControls,
  syncOrbitPolarLimit,
  clampCameraAboveGround,
  applyKeyboardMovement,
  stepCameraFrame,
} from './engine/camera-rig.js';
import {
  buildEnvironmentAndTerrain,
  buildProceduralSchoolModels,
  setCutawayMode,
} from './scene/school-world.js';
import {
  loadChildrenAndBuildInWorldMemorial,
  init3DPortraitRaycaster,
} from './scene/memorial-gallery.js';
import {
  refreshInWorldScreensLanguage,
  updateInWorldScreensLive,
} from './scene/in-world-screens.js';
import {
  initWalkthroughPipManifest,
  resolvePipVideoSrc,
  preloadAllWalkthroughPipBlobs,
  isSpotAudioPlaying,
  getGuidedTourAudioProgress,
  applyBookendTexts,
  playSpotNarration,
  resetWalkthroughIdleTimer,
  setWalkthroughProgress,
  updateWalkthroughVisualOverlaysLive,
  syncWalkthroughVisualsAtProgress,
  startGuidedTour,
  stopGuidedTour,
  renderGuidedTourStep,
} from './tour/tour-director.js';
import {
  openArtifactInspector,
  closeArtifactInspector,
  initHotspots,
  updateHotspotLabels,
  updateHotspotPositions,
  showHotspotModal,
  closeModal,
  updateVowBadge,
  fetchRealVowCount,
  openVowModal,
  closeVowModal,
  initUIControls,
} from './ui/hud-modals-vow.js';

appState.callbacks = {
  setCutawayMode,
  applyBookendTexts,
  updateHotspotLabels,
  updateHotspotPositions,
  refreshInWorldScreensLanguage,
  showHotspotModal,
  closeModal,
  openVowModal,
  closeVowModal,
  openArtifactInspector,
  closeArtifactInspector,
  renderGuidedTourStep,
  resetWalkthroughIdleTimer,
  playSpotNarration,
  isSpotAudioPlaying,
  resolvePipVideoSrc,
};

let resolveReconReady = null;
const reconReadyPromise = new Promise((resolve) => {
  resolveReconReady = resolve;
});

export function animate() {
  requestAnimationFrame(animate);
  if (!appState.clock || !appState.renderer || !appState.scene || !appState.camera) return;

  const rawDelta = appState.clock.getDelta();
  const delta = Math.min(Math.max(rawDelta, 0), 0.1);
  applyKeyboardMovement(delta);

  let tourProgress = 0;
  if (appState.isGuidedTour && !appState.deterministicWalkthroughRender) {
    tourProgress = getGuidedTourAudioProgress();
    setWalkthroughProgress(tourProgress);
    updateWalkthroughVisualOverlaysLive(appState.currentTourIndex, tourProgress);
    const activeStop = GUIDED_TOUR_STOPS[appState.currentTourIndex];
    updateInWorldScreensLive(activeStop ? activeStop.hotspotId : null, tourProgress);
  } else if (!appState.deterministicWalkthroughRender) {
    if (isSpotAudioPlaying() && appState.activeNarrationHotspot) {
      updateInWorldScreensLive(appState.activeNarrationHotspot, 0.35);
    }
  }

  stepCameraFrame(delta, tourProgress);

  if (appState.controls) {
    // The right-drag look pivots the orbit target around the camera, so the polar
    // clamp has to allow an upward aim and the camera must stay above the ground.
    syncOrbitPolarLimit();
    appState.controls.update();
    clampCameraAboveGround();
  }
  updateHotspotPositions();
  if (appState.shadowWarmupFrames > 0 && appState.sunLight) {
    appState.shadowWarmupFrames -= 1;
    appState.sunLight.shadow.needsUpdate = true;
  }
  renderFrame();
}

export async function startReconstructionApp() {
  if (typeof window === 'undefined' || typeof document === 'undefined') return;

  const bootParams = new URLSearchParams(window.location.search);
  appState.recordingMode = bootParams.get('recording') === '1';

  try {
    localStorage.removeItem('pfp_vow_count');
  } catch (_) {}

  appState.clock = new THREE.Clock();
  updateVowBadge();
  fetchRealVowCount();
  initI18n();
  initWalkthroughPipManifest();
  try {
    await initThreeEngine();
  } catch (err) {
    console.error('3D renderer could not start:', err);
    return;
  }
  buildEnvironmentAndTerrain();
  buildProceduralSchoolModels();
  useFrontFaceShadowCasters(appState.scene);
  await initAmbientOcclusion();
  loadChildrenAndBuildInWorldMemorial();
  init3DPortraitRaycaster();
  initHotspots();
  initUIControls();
  initKeyboardWalkControls();
  initLookControls();
  animate();

  if (appState.recordingMode) {
    document.body.classList.add('recording-mode');
  }
  // Clean-capture: hides every tour overlay that is not part of the film
  // (bottom pill, top-left stamp, skip button) for screen recording.
  // ?recording=1 or ?clean=1 starts with it on; press H to toggle at any time.
  // The 3D vow shrine is scene geometry (not DOM), so it needs a visibility sync.
  const setCleanCapture = (on) => {
    document.body.classList.toggle('clean-capture', on);
    const shrine = appState.scene.getObjectByName('Vow_Shrine_3D');
    if (shrine) shrine.visible = !on;
  };
  setCleanCapture(appState.recordingMode || bootParams.get('clean') === '1');
  window.addEventListener('keydown', (e) => {
    if ((e.key !== 'h' && e.key !== 'H') || e.ctrlKey || e.metaKey || e.altKey || e.repeat) return;
    const t = e.target;
    if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
    setCleanCapture(!document.body.classList.contains('clean-capture'));
  });
  if (bootParams.get('autostart') === '1') {
    document.body.classList.add('walkthrough-mode');
    setTimeout(() => {
      if (!appState.isGuidedTour) startGuidedTour();
    }, 1200);
  }

  if (resolveReconReady) resolveReconReady(appState);
}

if (typeof window !== 'undefined' && typeof document !== 'undefined') {
  // Backwards-compatible globals for site-nav.js, contact-modal.js, and Playwright render tools
  window.setLanguage = setLanguage;
  window.selectNarratorByActor = selectNarratorByActor;
  window.setNarratorProfile = setNarratorProfile;
  window.setTemporalCondition = setTemporalCondition;
  window.closeModal = closeModal;
  window.openVowModal = openVowModal;
  window.closeVowModal = closeVowModal;
  window.startGuidedTour = startGuidedTour;
  window.stopGuidedTour = stopGuidedTour;
  window.preloadAllWalkthroughPipBlobs = preloadAllWalkthroughPipBlobs;
  window.sampleGuidedTourCamera = sampleGuidedTourCamera;
  window.setWalkthroughProgress = setWalkthroughProgress;
  window.syncWalkthroughVisualsAtProgress = syncWalkthroughVisualsAtProgress;

  window.__reconReady = reconReadyPromise;
  window.PFPRecon = {
    state: appState,
    setLanguage,
    selectNarratorByActor,
    setNarratorProfile,
    setTemporalCondition,
    setCutawayMode,
    startGuidedTour,
    stopGuidedTour,
    sampleGuidedTourCamera,
    sampleGuidedTourCameraCoords,
    syncWalkthroughVisualsAtProgress,
    preloadAllWalkthroughPipBlobs,
    openVowModal,
    closeVowModal,
    showHotspotModal,
    closeModal,
    openArtifactInspector,
    closeArtifactInspector,
  };

  if (document.readyState === 'loading') {
    window.addEventListener('DOMContentLoaded', startReconstructionApp);
  } else {
    startReconstructionApp();
  }
}
