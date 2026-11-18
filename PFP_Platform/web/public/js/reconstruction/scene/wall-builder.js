/**
 * Data-driven wall builder.
 *
 * A wall is a straight run on the floor plan from `from` to `to` (world [x, z] in metres,
 * +X east, +Z south). Each wall becomes one THREE.Group placed at its midpoint and turned
 * so that local +X runs from `from` to `to`; every piece below is built in that local frame,
 * which is what lets a wall carry its openings and paint panels when it moves.
 *
 * Openings (`at` is the distance in metres from `from` to the centre of the opening):
 *   { type: 'window',   at, w, h, sill, mullions?, sunshade?, depth? }  cut + glazed window
 *   { type: 'doorway',  at, w, h, frame? }                              walk-through gap
 *   { type: 'hole',     at, w, h, sill? }                               plain rectangular cut
 *   { type: 'door',     at, base?, w? }                                      pink door (w defaults to 1.06); open hole above it, liners cut to its full height
 *   { type: 'grille',   at, w, h, y, side }                             pink-grilled inner window, no cut
 *
 * Liners are thin paint/mural panels on one face:
 *   { side: 'N'|'S'|'E'|'W', mat, y0, y1, from?, to?, t?, offset? }  (`from`/`to` along the wall)
 * Cutting openings also cut the liners, so a hole goes through both.
 *
 * Cuts are made by splitting the wall into boxes column by column, not by CSG, so every
 * piece stays a plain box that keeps the tiled plaster UVs and the `isSolidWall` tag.
 */
import * as THREE from 'three';

import { wallBoxGeometry } from './painted-plaster-material.js';
import { cornerExtensions } from './wall-joints.js';

const EPS = 1e-4;
const CUTTING_TYPES = new Set(['window', 'doorway', 'hole']);
const SIDE_VECTORS = { N: [0, -1], S: [0, 1], E: [1, 0], W: [-1, 0] };

/** Wall length, centre and Y rotation from its two floor-plan end points. */
export function wallFrame(def) {
  const [x1, z1] = def.from;
  const [x2, z2] = def.to;
  const dx = x2 - x1;
  const dz = z2 - z1;
  return {
    length: Math.hypot(dx, dz),
    cx: (x1 + x2) / 2,
    cz: (z1 + z2) / 2,
    rotY: -Math.atan2(dz, dx),
  };
}

/** +1 when a compass side lies on the wall's local +Z face, -1 when it lies on local -Z. */
function sideSign(rotY, side) {
  const v = SIDE_VECTORS[side];
  if (!v) return 1;
  // Local +Z in world space is (sin rotY, cos rotY) on the (x, z) plane.
  return Math.sin(rotY) * v[0] + Math.cos(rotY) * v[1] >= 0 ? 1 : -1;
}

// Pink door + transom footprint (see addPurpleDoor in school-world.js): 1.06 m wide,
// from the floor to the top of the transom.
const DOOR_W = 1.06;
const DOOR_THICKNESS = 0.05; // the leaf is a thin panel centred in the hole, not as thick as the wall
const DOOR_BASE = 0.2; // default height of a door above the wall's base
const DOOR_LEAF_H = 2.08;
const TRANSOM_H = 0.5; // the open gap above the door leaf

/**
 * The rectangle a closed door clears from the wall's paint liners. The wall itself stays
 * solid behind the door; only the liners are cut so the door face is not buried under them.
 */
function doorLinerCut(op) {
  if (op.type !== 'door') return null;
  const base = op.base ?? DOOR_BASE;
  const w = op.w ?? DOOR_W;
  return { a0: op.at - w / 2, a1: op.at + w / 2, y0: 0, y1: base + DOOR_LEAF_H + TRANSOM_H + 0.05 };
}

/** The [along0, along1] x [y0, y1] rectangle an opening removes, or null for a non-cutting one. */
function cutRect(op, wallH) {
  // A door removes the wall from its threshold to above the transom: the leaf fills the lower part
  // and the transom stays open, so there is no wall geometry hidden inside the door.
  if (op.type === 'door') {
    const base = op.base ?? DOOR_BASE;
    const w = op.w ?? DOOR_W;
    return {
      a0: op.at - w / 2,
      a1: op.at + w / 2,
      y0: base,
      y1: Math.min(base + DOOR_LEAF_H + TRANSOM_H + 0.05, wallH),
    };
  }
  if (!CUTTING_TYPES.has(op.type)) return null;
  const sill = op.type === 'doorway' ? 0 : op.sill || 0;
  return {
    a0: op.at - op.w / 2,
    a1: op.at + op.w / 2,
    y0: sill,
    y1: Math.min(sill + op.h, wallH),
  };
}

/**
 * Splits [a0, a1] x [y0, y1] into solid boxes around the cut rectangles. Columns between
 * consecutive cut edges get their vertical solid spans; neighbouring columns with the same
 * spans are merged so an uncut wall stays a single box.
 */
export function solidBoxes(a0, a1, y0, y1, cuts) {
  const edges = [a0, a1];
  for (const c of cuts) {
    if (c.a0 > a0 + EPS && c.a0 < a1 - EPS) edges.push(c.a0);
    if (c.a1 > a0 + EPS && c.a1 < a1 - EPS) edges.push(c.a1);
  }
  edges.sort((p, q) => p - q);
  const cols = [];
  for (let i = 0; i < edges.length - 1; i++) {
    const p = edges[i];
    const q = edges[i + 1];
    if (q - p < EPS) continue;
    const mid = (p + q) / 2;
    const holes = cuts
      .filter((c) => c.a0 < mid && c.a1 > mid)
      .map((c) => [Math.max(c.y0, y0), Math.min(c.y1, y1)])
      .filter(([h0, h1]) => h1 - h0 > EPS)
      .sort((m, n) => m[0] - n[0]);
    const spans = [];
    let cursor = y0;
    for (const [h0, h1] of holes) {
      if (h0 - cursor > EPS) spans.push([cursor, h0]);
      cursor = Math.max(cursor, h1);
    }
    if (y1 - cursor > EPS) spans.push([cursor, y1]);
    const key = spans.map((s) => s.map((n) => n.toFixed(4)).join(':')).join('|');
    const last = cols[cols.length - 1];
    if (last && last.key === key && Math.abs(last.a1 - p) < EPS) last.a1 = q;
    else cols.push({ a0: p, a1: q, spans, key });
  }
  const boxes = [];
  for (const col of cols) {
    for (const [s0, s1] of col.spans) boxes.push({ a0: col.a0, a1: col.a1, y0: s0, y1: s1 });
  }
  return boxes;
}

function addBox(group, mat, len, h, depth, x, y, z, userData, solid) {
  const mesh = new THREE.Mesh(wallBoxGeometry(len, h, depth, mat), mat);
  mesh.position.set(x, y, z);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  mesh.userData = Object.assign(solid ? { isSolidWall: true } : {}, userData);
  group.add(mesh);
  return mesh;
}

/**
 * Builds every wall in `defs`.
 *
 * ctx = {
 *   parents:  { default: THREE.Object3D, [name]: THREE.Object3D }   // def.group picks one
 *   mats:     { [key]: THREE.Material }                              // def.mat / liner.mat keys
 *   height, thickness,                                               // defaults
 *   addWindow(group, x, y, z, rotY, w, h, mullions, sunshade, depth),
 *   addDoor(group, x, yBase, z, rotY, depth),
 *   addGrille(group, x, y, z, rotY, w, h),
 * }
 * Returns [{ def, group, length }] for the wall inspector.
 */
export function buildWalls(defs, ctx) {
  const built = [];
  // Where two walls meet at a corner, each end grows to fill the notch left by the centre lines.
  const corners = cornerExtensions(defs, ctx.thickness);
  for (const def of defs) {
    const mat = ctx.mats[def.mat || 'white'];
    if (!mat) throw new Error(`Wall ${def.id}: unknown material "${def.mat}"`);
    const H = def.h ?? ctx.height;
    const T = def.t ?? ctx.thickness;
    const { length: L, cx, cz, rotY } = wallFrame(def);
    const openings = def.openings || [];
    const cuts = openings.map((op) => cutRect(op, H)).filter(Boolean);
    const linerCuts = cuts.concat(openings.map(doorLinerCut).filter(Boolean));

    const group = new THREE.Group();
    group.name = `Wall_${def.id}`;
    group.position.set(cx, def.y0 || 0, cz);
    group.rotation.y = rotY;
    group.userData = { wallId: def.id };
    const tag = Object.assign({ wallId: def.id }, def.userData || {});

    for (const b of solidBoxes(0, L, 0, H, cuts)) {
      addBox(group, mat, b.a1 - b.a0, b.y1 - b.y0, T, (b.a0 + b.a1) / 2 - L / 2, (b.y0 + b.y1) / 2, 0, tag, true);
    }

    // Corner caps: plain solid boxes continuing the wall past its end point.
    const cap = corners.get(def.id);
    if (cap && cap.start > 0) {
      addBox(group, mat, cap.start, H, T, -L / 2 - cap.start / 2, H / 2, 0, tag, true);
    }
    if (cap && cap.end > 0) {
      addBox(group, mat, cap.end, H, T, L / 2 + cap.end / 2, H / 2, 0, tag, true);
    }

    for (const liner of def.liners || []) {
      const lmat = ctx.mats[liner.mat];
      if (!lmat) throw new Error(`Wall ${def.id}: unknown liner material "${liner.mat}"`);
      const t = liner.t ?? 0.05;
      const offset = liner.offset ?? T / 2 + t / 2 - 0.01;
      const z = sideSign(rotY, liner.side) * offset;
      const a0 = liner.from ?? 0;
      const a1 = liner.to ?? L;
      for (const b of solidBoxes(a0, a1, liner.y0, liner.y1, linerCuts)) {
        addBox(group, lmat, b.a1 - b.a0, b.y1 - b.y0, t, (b.a0 + b.a1) / 2 - L / 2, (b.y0 + b.y1) / 2, z, { wallId: def.id, liner: true }, false);
      }
    }

    // Windows face the wall's `outside` side so sunshade brows land outdoors.
    const outRot = sideSign(rotY, def.outside) > 0 ? 0 : Math.PI;
    for (const op of openings) {
      const x = op.at - L / 2;
      if (op.type === 'window') {
        ctx.addWindow(group, x, (op.sill || 0) + op.h / 2, 0, outRot, op.w, op.h, op.mullions ?? 2, !!op.sunshade, op.depth ?? T + 0.01);
      } else if (op.type === 'door') {
        // A thin panel centred in the wall, 2 cm wider than the hole so its edges are tucked into the jambs.
        ctx.addDoor(group, x, op.base ?? DOOR_BASE, 0, 0, DOOR_THICKNESS, op.w ?? DOOR_W);
      } else if (op.type === 'grille') {
        const s = sideSign(rotY, op.side);
        ctx.addGrille(group, x, op.y, s * (T / 2 + 0.04), s > 0 ? 0 : Math.PI, op.w, op.h);
      } else if (op.type === 'doorway' && op.frame) {
        const fmat = ctx.mats[op.frame];
        for (const jx of [op.at - op.w / 2 + 0.035, op.at + op.w / 2 - 0.035]) {
          addBox(group, fmat, 0.07, op.h, T + 0.01, jx - L / 2, op.h / 2, 0, { wallId: def.id }, false);
        }
      }
    }

    (ctx.parents[def.group] || ctx.parents.default).add(group);
    built.push({ def, group, length: L });
  }
  return built;
}
