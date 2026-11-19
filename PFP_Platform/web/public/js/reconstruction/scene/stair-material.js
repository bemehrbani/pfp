/**
 * Plastered-concrete surface for the stairs (rainbow stairwell treads, rear exterior staircase).
 *
 * Maps come from the plastered_wall_04_1k asset set. The diffuse JPG is served as-is; the EXR
 * normal and roughness maps are converted to 8-bit PNG by scripts/convert_exr_to_png.py and
 * served from textures/stairs.
 *
 * The diffuse is a neutral mid-grey, so each stair keeps its own colour (the rainbow treads follow
 * the narration order, the rear treads are terracotta) as the material tint, and only the grain,
 * bumps and roughness variation come from the textures. A tint can only darken a mid-grey map, so
 * a brightness gain lifts the result back to the intended colour.
 *
 * Like the painted plaster, the material carries `userData.plaster` so the slab helpers rescale
 * each face's UVs to its real size.
 */

import * as THREE from 'three';

/**
 * One texture tile spans this many metres. Treads are about 0.2 x 0.3 m, so the tile is smaller
 * than the 2 m used for walls; otherwise only a smudge of the texture would land on each step.
 */
export const STAIR_TILE_METRES = 0.8;

/** Lifts the mid-grey diffuse so the tint reads as the intended colour, not a darkened one. */
const DEFAULT_BRIGHTNESS = 1.8;

const STAIR_TEXTURE_DIR = 'textures/stairs/';
const STAIR_MAPS = {
  map: { file: 'plastered_wall_04_diff_1k.jpg', color: true },
  normalMap: { file: 'plastered_wall_04_nor_gl_1k.png', color: false },
  roughnessMap: { file: 'plastered_wall_04_rough_1k.png', color: false },
};

let cachedStairMaps = null;
/** Materials by tint and brightness: the rainbow reuses colours, so each is built once. */
const materialCache = new Map();

/** Loads the maps once; colour is decoded as sRGB, normal and roughness stay linear. */
function loadStairMaps() {
  if (cachedStairMaps) return cachedStairMaps;
  const loader = new THREE.TextureLoader();
  cachedStairMaps = {};
  Object.entries(STAIR_MAPS).forEach(([slot, spec]) => {
    const tex = loader.load(STAIR_TEXTURE_DIR + spec.file);
    if (spec.color) tex.colorSpace = THREE.SRGBColorSpace;
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.anisotropy = 8;
    cachedStairMaps[slot] = tex;
  });
  return cachedStairMaps;
}

export function createStairMaterial(tint, options = {}) {
  const brightness = options.brightness ?? DEFAULT_BRIGHTNESS;
  const key = `${tint}:${brightness}`;
  const cached = materialCache.get(key);
  if (cached) return cached;

  const maps = loadStairMaps();
  const mat = new THREE.MeshStandardMaterial({
    color: tint,
    map: maps.map,
    normalMap: maps.normalMap,
    roughnessMap: maps.roughnessMap,
    normalScale: new THREE.Vector2(0.8, 0.8),
    roughness: 1,
    metalness: 0,
  });
  mat.color.multiplyScalar(brightness);
  mat.userData.plaster = true; // metre-tiled UVs, see the header comment
  materialCache.set(key, mat);
  return mat;
}
