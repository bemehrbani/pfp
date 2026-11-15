/**
 * Guided Tour waypoint camera spline sampler, camera target transitions,
 * and first-person WASD / Arrow keyboard walk navigation.
 */
import { appState } from '../state.js';
import { GUIDED_TOUR_STOPS } from '../data/tour-config.js';
import { setTemporalCondition } from './core.js';

function clampUnit(value) {
  return Math.max(0, Math.min(1, value || 0));
}

function lerpScalar(a, b, t) {
  if (t <= 0) return a;
  if (t >= 1) return b;
  return a + (b - a) * t;
}

/**
 * Pure waypoint interpolation helper (safe to run in Node tests without `THREE`).
 * @param {number} stopIndex
 * @param {number} rawProgress
 * @returns {{ pos: [number, number, number], lookAt: [number, number, number] } | null}
 */
export function sampleGuidedTourCameraCoords(stopIndex, rawProgress) {
  const stop = GUIDED_TOUR_STOPS[stopIndex];
  if (!stop) return null;
  const pts =
    Array.isArray(stop.waypoints) && stop.waypoints.length >= 2
      ? stop.waypoints
      : [
          { t: 0.0, camPos: stop.camPos, lookAt: stop.lookAt },
          { t: 1.0, camPos: stop.camPos, lookAt: stop.lookAt },
        ];

  const p = clampUnit(rawProgress);
  let a = pts[0];
  let b = pts[pts.length - 1];
  let localT = 0;

  if (typeof pts[0].t === 'number') {
    let segIdx = pts.length - 2;
    for (let i = 0; i < pts.length - 1; i++) {
      const tNext = typeof pts[i + 1].t === 'number' ? pts[i + 1].t : (i + 1) / (pts.length - 1);
      if (p <= tNext || i === pts.length - 2) {
        segIdx = i;
        break;
      }
    }
    a = pts[segIdx];
    b = pts[segIdx + 1];
    const t0 = typeof a.t === 'number' ? a.t : 0;
    const t1 = typeof b.t === 'number' ? b.t : 1;
    localT = clampUnit((p - t0) / Math.max(0.0001, t1 - t0));
  } else {
    const eased = 0.5 - 0.5 * Math.cos(Math.PI * p);
    const scaled = eased * (pts.length - 1);
    const segIdx = Math.min(pts.length - 2, Math.floor(scaled));
    a = pts[segIdx];
    b = pts[segIdx + 1];
    localT = scaled - segIdx;
  }

  const segEase = 0.5 - 0.5 * Math.cos(Math.PI * localT);
  return {
    pos: [
      lerpScalar(a.camPos[0], b.camPos[0], segEase),
      lerpScalar(a.camPos[1], b.camPos[1], segEase),
      lerpScalar(a.camPos[2], b.camPos[2], segEase),
    ],
    lookAt: [
      lerpScalar(a.lookAt[0], b.lookAt[0], segEase),
      lerpScalar(a.lookAt[1], b.lookAt[1], segEase),
      lerpScalar(a.lookAt[2], b.lookAt[2], segEase),
    ],
  };
}

/**
 * Samples the Guided Tour camera position and target as `THREE.Vector3` pairs.
 * @param {number} stopIndex
 * @param {number} rawProgress
 */
export function sampleGuidedTourCamera(stopIndex, rawProgress) {
  const coords = sampleGuidedTourCameraCoords(stopIndex, rawProgress);
  if (!coords) return null;
  if (typeof THREE === 'undefined') return coords;
  return {
    pos: new THREE.Vector3(coords.pos[0], coords.pos[1], coords.pos[2]),
    lookAt: new THREE.Vector3(coords.lookAt[0], coords.lookAt[1], coords.lookAt[2]),
  };
}

export function triggerCameraAnimation(newPos, newLookAt) {
  appState.isAnimatingCamera = true;
  appState.animationTarget.pos = newPos;
  appState.animationTarget.lookAt = newLookAt;
}

export function toggleWalkMode() {
  appState.isWalkMode = !appState.isWalkMode;
  const btn = typeof document !== 'undefined' ? document.getElementById('btnWalkMode') : null;
  if (btn) btn.classList.toggle('active', appState.isWalkMode);

  if (appState.isWalkMode) {
    setTemporalCondition(0.0);
    const slider = typeof document !== 'undefined' ? document.getElementById('timelineSlider') : null;
    if (slider) slider.value = 0.0;
    appState.callbacks.setCutawayMode?.(2);
    triggerCameraAnimation(new THREE.Vector3(-1.2, 1.85, 6.2), new THREE.Vector3(-1.2, 1.85, -8.5));
  } else {
    appState.callbacks.setCutawayMode?.(0);
    triggerCameraAnimation(new THREE.Vector3(28, 22, 34), new THREE.Vector3(0, 3.0, -3));
  }
}

export function initKeyboardWalkControls() {
  if (typeof window === 'undefined') return;
  const { moveKeys } = appState;

  window.addEventListener('keydown', (e) => {
    const activeTag = typeof document !== 'undefined' ? document.activeElement?.tagName : '';
    if (['INPUT', 'TEXTAREA', 'SELECT'].includes(activeTag)) return;
    if (e.code === 'KeyW' || e.code === 'ArrowUp') moveKeys.forward = true;
    if (e.code === 'KeyS' || e.code === 'ArrowDown') moveKeys.backward = true;
    if (e.code === 'KeyA' || e.code === 'ArrowLeft') moveKeys.left = true;
    if (e.code === 'KeyD' || e.code === 'ArrowRight') moveKeys.right = true;
  });

  window.addEventListener('keyup', (e) => {
    if (e.code === 'KeyW' || e.code === 'ArrowUp') moveKeys.forward = false;
    if (e.code === 'KeyS' || e.code === 'ArrowDown') moveKeys.backward = false;
    if (e.code === 'KeyA' || e.code === 'ArrowLeft') moveKeys.left = false;
    if (e.code === 'KeyD' || e.code === 'ArrowRight') moveKeys.right = false;
  });
}

export function applyKeyboardMovement(delta) {
  const { moveKeys, camera, controls } = appState;
  if (!camera || !controls) return;
  if (!moveKeys.forward && !moveKeys.backward && !moveKeys.left && !moveKeys.right) return;

  appState.isAnimatingCamera = false;
  const speed = 10.0 * delta;
  const forward = new THREE.Vector3();
  camera.getWorldDirection(forward);
  forward.y = 0;
  forward.normalize();

  const right = new THREE.Vector3().crossVectors(forward, camera.up).normalize();
  const moveVec = new THREE.Vector3();

  if (moveKeys.forward) moveVec.add(forward);
  if (moveKeys.backward) moveVec.sub(forward);
  if (moveKeys.right) moveVec.add(right);
  if (moveKeys.left) moveVec.sub(right);

  if (moveVec.lengthSq() > 0) {
    moveVec.normalize().multiplyScalar(speed);
    camera.position.add(moveVec);
    controls.target.add(moveVec);
    if (appState.isWalkMode) {
      camera.position.y = 1.85;
      controls.target.y = 1.85;
    }
  }
}

export function stepCameraFrame(delta, tourProgress) {
  const { camera, controls, animationTarget } = appState;
  if (!camera || !controls) return;

  if (appState.isGuidedTour && !appState.deterministicWalkthroughRender) {
    if (appState.isAnimatingCamera && animationTarget.pos) {
      camera.position.lerp(animationTarget.pos, 0.08);
      controls.target.lerp(animationTarget.lookAt, 0.08);
      if (camera.position.distanceTo(animationTarget.pos) < 0.35) {
        appState.isAnimatingCamera = false;
      }
    } else if (!appState.tourManualCameraOverride) {
      const sampled = sampleGuidedTourCamera(appState.currentTourIndex, tourProgress);
      if (sampled) {
        const smoothAlpha = 1 - Math.exp(-5.2 * Math.min(Math.max(delta, 0.008), 0.05));
        camera.position.lerp(sampled.pos, smoothAlpha);
        controls.target.lerp(sampled.lookAt, smoothAlpha);
      }
    }
  } else if (!appState.deterministicWalkthroughRender) {
    if (appState.isAnimatingCamera && animationTarget.pos) {
      camera.position.lerp(animationTarget.pos, 0.06);
      controls.target.lerp(animationTarget.lookAt, 0.06);
      if (camera.position.distanceTo(animationTarget.pos) < 0.25) {
        appState.isAnimatingCamera = false;
      }
    }
  }
}
