/**
 * Guided Tour waypoint camera spline sampler, camera target transitions,
 * right-drag look-around, and first-person WASD / Arrow flight with Q/E height
 * (free-fly only; walk mode stays pinned to eye level).
 */
import * as THREE from 'three';

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
 * Pure waypoint interpolation helper: returns plain coordinate arrays, so it needs no
 * renderer and stays usable from Node-side tooling.
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

// Right-button look-around. The camera turns in place by orbiting its OrbitControls
// target around the camera position, which keeps the pivot, the orbit radius, wheel
// zoom, panning and the next left-button orbit drag anchored to whatever the user is
// looking at instead of the stale scene centre.

/** Maximum pitch (radians) the look may add above or below level. */
export const LOOK_ELEVATION_LIMIT = Math.PI / 2 - 0.02;

// Radians per viewport-height of drag, matching the OrbitControls.rotateSpeed = 1.0 feel.
const LOOK_RADIANS_PER_VIEWPORT_HEIGHT = Math.PI * 2;
const LOOK_RADIUS_EPSILON = 1e-4;

// Keep in sync with engine/core.js: a plain orbit may not swing the camera below
// the target's height, but an upward look has to be allowed past that.
const ORBIT_MAX_POLAR_DEFAULT = Math.PI / 2 - 0.01;
const ORBIT_MAX_POLAR_LOOK_UP = Math.PI - 0.01;

// Floor guard for orbiting around an upward-aimed target.
const CAMERA_GROUND_FLOOR_Y = 0.35;

function clampLookValue(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

/**
 * Rotates the orbit target around the camera by one pointer delta. The camera
 * position and the orbit radius are preserved, so the camera turns in place while
 * its pivot follows the gaze.
 * Pure math on `{x, y, z}` objects (safe to run in Node tests without THREE).
 * Signs follow OrbitControls: dragging right turns the view right, dragging down
 * turns it down.
 * @param {{x: number, y: number, z: number}} cameraPos
 * @param {{x: number, y: number, z: number}} target
 * @param {number} dx
 * @param {number} dy
 * @param {number} viewportHeight
 * @param {number} [speed]
 * @returns {{x: number, y: number, z: number}} the rotated target position
 */
export function rotateTargetAroundCamera(cameraPos, target, dx, dy, viewportHeight, speed = 1) {
  const height = Math.max(1, Number(viewportHeight) || 1);
  const radiansPerPixel = (LOOK_RADIANS_PER_VIEWPORT_HEIGHT * (Number(speed) || 1)) / height;

  const ox = target.x - cameraPos.x;
  const oy = target.y - cameraPos.y;
  const oz = target.z - cameraPos.z;
  const radius = Math.sqrt(ox * ox + oy * oy + oz * oz);
  if (radius < LOOK_RADIUS_EPSILON) {
    return { x: target.x, y: target.y, z: target.z };
  }

  const yaw = Math.atan2(ox, oz) - dx * radiansPerPixel;
  const elevation = clampLookValue(
    Math.asin(clampLookValue(oy / radius, -1, 1)) - dy * radiansPerPixel,
    -LOOK_ELEVATION_LIMIT,
    LOOK_ELEVATION_LIMIT
  );
  const horizontal = Math.cos(elevation) * radius;

  return {
    x: cameraPos.x + Math.sin(yaw) * horizontal,
    y: cameraPos.y + Math.sin(elevation) * radius,
    z: cameraPos.z + Math.cos(yaw) * horizontal,
  };
}

/**
 * Widens OrbitControls' polar clamp only while the look has aimed the camera
 * upward (target above the camera). In every other state the default clamp keeps
 * a plain drag from swinging the camera under the courtyard.
 */
export function syncOrbitPolarLimit() {
  const { camera, controls } = appState;
  if (!camera || !controls) return;
  const lookingUp = controls.target.y > camera.position.y + 1e-3;
  controls.maxPolarAngle = lookingUp ? ORBIT_MAX_POLAR_LOOK_UP : ORBIT_MAX_POLAR_DEFAULT;
}

/**
 * Keeps the camera above the courtyard when an upward-aimed pivot is orbited.
 * Scripted camera moves are left untouched.
 */
export function clampCameraAboveGround() {
  const { camera, controls } = appState;
  if (!camera || !controls) return;
  if (appState.isAnimatingCamera || appState.deterministicWalkthroughRender) return;
  if (camera.position.y >= CAMERA_GROUND_FLOOR_Y) return;
  camera.position.y = CAMERA_GROUND_FLOOR_Y;
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
    if (e.code === 'KeyE') moveKeys.up = true;
    if (e.code === 'KeyQ') moveKeys.down = true;
  });

  window.addEventListener('keyup', (e) => {
    if (e.code === 'KeyW' || e.code === 'ArrowUp') moveKeys.forward = false;
    if (e.code === 'KeyS' || e.code === 'ArrowDown') moveKeys.backward = false;
    if (e.code === 'KeyA' || e.code === 'ArrowLeft') moveKeys.left = false;
    if (e.code === 'KeyD' || e.code === 'ArrowRight') moveKeys.right = false;
    if (e.code === 'KeyE') moveKeys.up = false;
    if (e.code === 'KeyQ') moveKeys.down = false;
  });
}

/**
 * Installs the right-button look gesture. The pointer-down is intercepted in the
 * capture phase on `window` so OrbitControls never enters its own pan / rotate state
 * for this gesture; the drag then pivots the orbit target around the camera, which
 * turns the camera in place. Right-drag is the gesture because it needs no modifier:
 * Ctrl/Cmd + drag is undiscoverable, turns into a right-click on macOS, and does not
 * exist on touch screens.
 */
export function initLookControls() {
  if (typeof window === 'undefined' || !appState.renderer) return;
  const dom = appState.renderer.domElement;
  if (!dom) return;

  const wantsLook = (e) => e.button === 2;

  const endLookGesture = (pointerId) => {
    const activeId = appState.lookDragPointerId;
    if (activeId === null || activeId === undefined) return;
    if (pointerId !== undefined && pointerId !== activeId) return;
    appState.lookDragPointerId = null;
    dom.style.cursor = 'grab';
    try {
      dom.releasePointerCapture(activeId);
    } catch (_) {}
  };

  const onPointerDown = (e) => {
    if (e.target !== dom) return;
    if (appState.lookDragPointerId !== null) {
      // A look gesture already drives the camera; keep every extra pointer away from
      // OrbitControls so two fingers cannot orbit and look at the same time.
      e.preventDefault();
      e.stopPropagation();
      return;
    }
    if (!wantsLook(e)) return;
    e.preventDefault();
    e.stopPropagation();
    appState.lookDragPointerId = e.pointerId;
    appState.lookDragLastX = e.clientX;
    appState.lookDragLastY = e.clientY;
    dom.style.cursor = 'grabbing';
    if (appState.isGuidedTour) {
      appState.tourManualCameraOverride = true;
      appState.isAnimatingCamera = false;
    }
    try {
      dom.setPointerCapture(e.pointerId);
    } catch (_) {}
  };

  const onPointerMove = (e) => {
    if (appState.lookDragPointerId === null) return;
    e.preventDefault();
    e.stopPropagation();
    if (e.pointerId !== appState.lookDragPointerId) return;
    const { camera, controls } = appState;
    if (!camera || !controls) return;
    const height = dom.clientHeight || (typeof window !== 'undefined' ? window.innerHeight : 1);
    const rotated = rotateTargetAroundCamera(
      camera.position,
      controls.target,
      e.clientX - appState.lookDragLastX,
      e.clientY - appState.lookDragLastY,
      height
    );
    controls.target.set(rotated.x, rotated.y, rotated.z);
    appState.lookDragLastX = e.clientX;
    appState.lookDragLastY = e.clientY;
  };

  const onPointerUp = (e) => {
    if (appState.lookDragPointerId === null) return;
    e.stopPropagation();
    if (e.pointerId !== appState.lookDragPointerId) return;
    endLookGesture(e.pointerId);
  };

  window.addEventListener('pointerdown', onPointerDown, true);
  window.addEventListener('pointermove', onPointerMove, true);
  window.addEventListener('pointerup', onPointerUp, true);
  window.addEventListener('pointercancel', onPointerUp, true);
  window.addEventListener('blur', () => endLookGesture(), false);
}

export function applyKeyboardMovement(delta) {
  const { moveKeys, camera, controls } = appState;
  if (!camera || !controls) return;

  // Walk mode is grounded at eye level, so vertical flight belongs to free-fly navigation.
  const verticalInput = appState.isWalkMode ? 0 : (moveKeys.up ? 1 : 0) - (moveKeys.down ? 1 : 0);
  const hasPlanarInput = moveKeys.forward || moveKeys.backward || moveKeys.left || moveKeys.right;
  if (!hasPlanarInput && verticalInput === 0) return;

  appState.isAnimatingCamera = false;
  const speed = 10.0 * delta;

  const moveVec = new THREE.Vector3();
  if (hasPlanarInput) {
    const forward = new THREE.Vector3();
    camera.getWorldDirection(forward);
    forward.y = 0;
    forward.normalize();

    const right = new THREE.Vector3().crossVectors(forward, camera.up).normalize();
    if (moveKeys.forward) moveVec.add(forward);
    if (moveKeys.backward) moveVec.sub(forward);
    if (moveKeys.right) moveVec.add(right);
    if (moveKeys.left) moveVec.sub(right);

    if (moveVec.lengthSq() > 0) {
      moveVec.normalize().multiplyScalar(speed);
      camera.position.add(moveVec);
      controls.target.add(moveVec);
      if (appState.isWalkMode) {
        // Unchanged walk-mode rule: every step returns to eye level with a level view.
        camera.position.y = 1.85;
        controls.target.y = 1.85;
      }
    }
  }

  if (verticalInput !== 0) {
    const lift = verticalInput * speed;
    camera.position.y += lift;
    controls.target.y += lift;
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
