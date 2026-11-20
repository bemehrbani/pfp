/**
 * Oak-veneer surface for the door leaves (classroom doors and the first-floor double doors).
 *
 * Maps come from the oak_veneer_03_1k asset set. The diffuse JPG is served as-is; the EXR normal
 * and roughness maps are converted to 8-bit PNG by scripts/convert_exr_to_png.py and served from
 * textures/doors.
 *
 * The veneer is pale, so a tint over it reads as stained wood with the grain still visible. Pass a
 * tint of 0xffffff for natural oak.
 */

import * as THREE from 'three';

/** One texture tile spans this many metres; a door leaf is about 1.1 x 2.1 m. */
export const DOOR_TILE_METRES = 1.0;

const DOOR_TEXTURE_DIR = 'textures/doors/';
const DOOR_MAPS = {
  map: { file: 'oak_veneer_03_diff_1k.jpg', color: true },
  normalMap: { file: 'oak_veneer_03_nor_gl_1k.png', color: false },
  roughnessMap: { file: 'oak_veneer_03_rough_1k.png', color: false },
};

let cachedDoorMaps = null;

/** Loads the maps once; colour is decoded as sRGB, normal and roughness stay linear. */
function loadDoorMaps() {
  if (cachedDoorMaps) return cachedDoorMaps;
  const loader = new THREE.TextureLoader();
  cachedDoorMaps = {};
  Object.entries(DOOR_MAPS).forEach(([slot, spec]) => {
    const tex = loader.load(DOOR_TEXTURE_DIR + spec.file);
    if (spec.color) tex.colorSpace = THREE.SRGBColorSpace;
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.anisotropy = 8;
    cachedDoorMaps[slot] = tex;
  });
  return cachedDoorMaps;
}

export function createDoorMaterial(tint = 0xffffff) {
  const maps = loadDoorMaps();
  return new THREE.MeshStandardMaterial({
    color: tint,
    map: maps.map,
    normalMap: maps.normalMap,
    roughnessMap: maps.roughnessMap,
    normalScale: new THREE.Vector2(0.6, 0.6),
    roughness: 1,
    metalness: 0,
  });
}

/**
 * Door-leaf box with UVs in metres. The veneer's grain runs along U, but a door's grain runs
 * vertically, so on the two big faces (+Z and -Z) U follows the height and V the width.
 * BoxGeometry face order is +X, -X, +Y, -Y, +Z, -Z.
 */
export function doorBoxGeometry(width, height, depth, tile = DOOR_TILE_METRES) {
  const geo = new THREE.BoxGeometry(width, height, depth);
  const uv = geo.attributes.uv;
  if (uv.count !== 24) return geo;
  // [u span, v span] per face, before any swap.
  const faceSpans = [
    [depth, height],
    [depth, height],
    [width, depth],
    [width, depth],
    [width, height],
    [width, height],
  ];
  for (let face = 0; face < 6; face++) {
    const [uSpan, vSpan] = faceSpans[face];
    const swap = face === 4 || face === 5; // vertical grain on the leaf faces
    for (let corner = 0; corner < 4; corner++) {
      const i = face * 4 + corner;
      const u = uv.getX(i);
      const v = uv.getY(i);
      if (swap) uv.setXY(i, (v * vSpan) / tile, (u * uSpan) / tile);
      else uv.setXY(i, (u * uSpan) / tile, (v * vSpan) / tile);
    }
  }
  uv.needsUpdate = true;
  return geo;
}
