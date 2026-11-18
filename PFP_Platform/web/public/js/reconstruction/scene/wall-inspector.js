/**
 * Wall inspector, enabled with `?walls=1` on reconstruction.html.
 *
 * Floats each data-driven wall's ID above it and, on click, outlines the wall and shows its
 * end points, length and openings, so a wall can be named precisely ("move G-14 0.5 m north").
 * It only reads `appState.wallRegistry`; nothing here changes the scene for regular visitors.
 */
import * as THREE from 'three';

import { appState } from '../state.js';

const LABEL_LIFT_M = 0.7;

function makeLabelSprite(text) {
  const canvas = document.createElement('canvas');
  canvas.width = 256;
  canvas.height = 96;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
  ctx.beginPath();
  ctx.roundRect(4, 4, 248, 88, 18);
  ctx.fill();
  ctx.strokeStyle = '#facc15';
  ctx.lineWidth = 5;
  ctx.stroke();
  ctx.fillStyle = '#facc15';
  ctx.font = 'bold 54px system-ui, sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(text, 128, 50);
  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  const mat = new THREE.SpriteMaterial({ map: tex, depthTest: false, depthWrite: false });
  const sprite = new THREE.Sprite(mat);
  sprite.scale.set(1.6, 0.6, 1);
  sprite.renderOrder = 999;
  return sprite;
}

const fmt = (n) => (Math.round(n * 100) / 100).toString();

function describe(entry) {
  const { def, length } = entry;
  const lines = [
    `<strong>${def.id}</strong>${def.note ? ` — ${def.note}` : ''}`,
    `from [${def.from.map(fmt).join(', ')}] → to [${def.to.map(fmt).join(', ')}]`,
    `length ${fmt(length)} m · thickness ${fmt(def.t ?? 0.24)} m`,
  ];
  (def.openings || []).forEach((op, i) => {
    const size = op.w ? ` ${fmt(op.w)}×${fmt(op.h)} m` : '';
    const sill = op.sill ? ` sill ${fmt(op.sill)}` : '';
    lines.push(`#${i + 1} ${op.type} at ${fmt(op.at)} m${size}${sill}`);
  });
  return lines.join('<br>');
}

export function initWallInspector() {
  if (typeof window === 'undefined') return;
  if (new URLSearchParams(window.location.search).get('walls') !== '1') return;
  const registry = appState.wallRegistry || [];
  if (!registry.length || !appState.renderer) return;

  for (const entry of registry) {
    const label = makeLabelSprite(entry.def.id);
    // The wall group sits at the wall's midpoint, so a local offset lands over its centre.
    label.position.set(0, (entry.def.h ?? 3.6) + LABEL_LIFT_M, 0);
    entry.group.add(label);
  }

  const panel = document.createElement('div');
  panel.style.cssText = [
    'position:fixed', 'left:12px', 'bottom:12px', 'z-index:9999', 'max-width:min(420px, calc(100vw - 24px))',
    'padding:10px 12px', 'border-radius:10px', 'background:rgba(15,23,42,0.92)', 'color:#f8fafc',
    'font:13px/1.45 system-ui, sans-serif', 'border:1px solid #facc15', 'pointer-events:none',
  ].join(';');
  panel.innerHTML = 'Wall inspector: click a wall.';
  document.body.appendChild(panel);

  const meshes = [];
  for (const entry of registry) {
    entry.group.traverse((o) => {
      if (o.isMesh && o.userData && o.userData.wallId) meshes.push(o);
    });
  }

  let outline = null;
  const raycaster = new THREE.Raycaster();
  const ndc = new THREE.Vector2();
  const dom = appState.renderer.domElement;
  let downX = 0;
  let downY = 0;
  dom.addEventListener('pointerdown', (e) => {
    downX = e.clientX;
    downY = e.clientY;
  });
  dom.addEventListener('pointerup', (e) => {
    if (Math.hypot(e.clientX - downX, e.clientY - downY) > 6) return;
    const rect = dom.getBoundingClientRect();
    ndc.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    ndc.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(ndc, appState.camera);
    const hit = raycaster.intersectObjects(meshes, false).find((h) => h.object.visible);
    if (!hit) return;
    const entry = registry.find((r) => r.def.id === hit.object.userData.wallId);
    if (!entry) return;
    if (outline) {
      outline.parent?.remove(outline);
      outline.dispose();
    }
    // Bound the wall's meshes only, so the floating label does not stretch the outline.
    const box = new THREE.Box3();
    entry.group.traverse((o) => {
      if (o.isMesh) box.expandByObject(o);
    });
    outline = new THREE.Box3Helper(box, 0xfacc15);
    outline.renderOrder = 998;
    outline.material.depthTest = false;
    appState.scene.add(outline);
    panel.innerHTML = describe(entry);
    console.info(`[walls] ${entry.def.id}`, entry.def);
  });
}
