/**
 * Rough-concrete surface for everything that appears after the strike: the crater rim chunks, the
 * collapsed-wing rubble slabs, the sheared slab ledge and the crater pit floor.
 *
 * Maps come from the rough_concrete_1k asset set. The diffuse JPG is served as-is; the EXR normal
 * and roughness maps are converted to 8-bit PNG by scripts/convert_exr_to_png.py and served from
 * textures/rubble.
 *
 * The diffuse is a pale grey-beige, while the post-strike surfaces were deliberately dark and
 * dusty. Each keeps its own colour as the material tint, and a brightness gain makes up for the
 * lighter map so the tint still reads as that colour.
 */

import * as THREE from 'three';

/** One texture tile spans this many metres. Rubble chunks are 0.5 - 3 m across. */
export const RUBBLE_TILE_METRES = 1.0;

/** Lifts the pale diffuse so a dark tint reads as the intended dark colour, not near-black. */
const DEFAULT_BRIGHTNESS = 1.8;

const RUBBLE_TEXTURE_DIR = 'textures/rubble/';
const RUBBLE_MAPS = {
  map: { file: 'rough_concrete_diff_1k.jpg', color: true },
  normalMap: { file: 'rough_concrete_nor_gl_1k.png', color: false },
  roughnessMap: { file: 'rough_concrete_rough_1k.png', color: false },
};

let cachedRubbleMaps = null;

/** Loads the maps once; colour is decoded as sRGB, normal and roughness stay linear. */
function loadRubbleMaps() {
  if (cachedRubbleMaps) return cachedRubbleMaps;
  const loader = new THREE.TextureLoader();
  cachedRubbleMaps = {};
  Object.entries(RUBBLE_MAPS).forEach(([slot, spec]) => {
    const tex = loader.load(RUBBLE_TEXTURE_DIR + spec.file);
    if (spec.color) tex.colorSpace = THREE.SRGBColorSpace;
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.anisotropy = 8;
    cachedRubbleMaps[slot] = tex;
  });
  return cachedRubbleMaps;
}

export function createRubbleMaterial(tint, options = {}) {
  const maps = loadRubbleMaps();
  const brightness = options.brightness ?? DEFAULT_BRIGHTNESS;
  const mat = new THREE.MeshStandardMaterial({
    color: tint,
    map: maps.map,
    normalMap: maps.normalMap,
    roughnessMap: maps.roughnessMap,
    normalScale: new THREE.Vector2(1, 1),
    roughness: 1,
    metalness: 0,
  });
  mat.color.multiplyScalar(brightness);
  return mat;
}

/**
 * Overwrites a geometry's UVs with a box projection in object space: each vertex is projected
 * onto the plane its face normal points along most. The chunks here are flat-shaded polyhedra and
 * boxes, so every face gets clean, undistorted texture, where the polyhedron's own spherical UVs
 * would smear it and pinch at the seam. Works for indexed and non-indexed geometry as long as the
 * vertices carry per-face normals, which Box, Dodecahedron and Circle geometry do.
 */
export function boxProjectUVs(geometry, tile = RUBBLE_TILE_METRES) {
  const pos = geometry.attributes.position;
  const nor = geometry.attributes.normal;
  if (!nor) geometry.computeVertexNormals();
  const normals = geometry.attributes.normal;
  const uvs = new Float32Array(pos.count * 2);
  for (let i = 0; i < pos.count; i++) {
    const ax = Math.abs(normals.getX(i));
    const ay = Math.abs(normals.getY(i));
    const az = Math.abs(normals.getZ(i));
    let u;
    let v;
    if (ax >= ay && ax >= az) {
      u = pos.getZ(i);
      v = pos.getY(i);
    } else if (ay >= az) {
      u = pos.getX(i);
      v = pos.getZ(i);
    } else {
      u = pos.getX(i);
      v = pos.getY(i);
    }
    uvs[i * 2] = u / tile;
    uvs[i * 2 + 1] = v / tile;
  }
  geometry.setAttribute('uv', new THREE.BufferAttribute(uvs, 2));
  return geometry;
}
