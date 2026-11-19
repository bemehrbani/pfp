/**
 * Granite floor tiles for the school interior.
 *
 * Maps come from the granite_tile_03_1k asset set. The diffuse JPG is served as-is; the EXR
 * normal and roughness maps are converted to 8-bit PNG by scripts/convert_exr_to_png.py and
 * served from textures/granite. The roughness map is nearly flat (about 0.9), so the floor
 * stays matte and does not mirror the sky environment light.
 *
 * The material carries the same `userData.plaster` marker as the painted-plaster walls. That
 * flag is what makes `wallBoxGeometry` and `plasterBoxGeometry` rescale each slab face's UVs to
 * its real size, so a tile keeps the same physical size on every floor slab. It means "uses
 * metre-tiled UVs" here, not that the surface is plaster.
 */

import * as THREE from 'three';
import { PLASTER_TILE_METRES } from './painted-plaster-material.js';

/** Tile span in metres. Shared with the plaster helpers that build the slab UVs. */
export const GRANITE_TILE_METRES = PLASTER_TILE_METRES;

const GRANITE_TEXTURE_DIR = 'textures/granite/';
const GRANITE_MAPS = {
  map: { file: 'granite_tile_03_diff_1k.jpg', color: true },
  normalMap: { file: 'granite_tile_03_nor_gl_1k.png', color: false },
  roughnessMap: { file: 'granite_tile_03_rough_1k.png', color: false },
};

let cachedGraniteMaps = null;

/** Loads the maps once; colour is decoded as sRGB, normal and roughness stay linear. */
function loadGraniteMaps() {
  if (cachedGraniteMaps) return cachedGraniteMaps;
  const loader = new THREE.TextureLoader();
  cachedGraniteMaps = {};
  Object.entries(GRANITE_MAPS).forEach(([slot, spec]) => {
    const tex = loader.load(GRANITE_TEXTURE_DIR + spec.file);
    if (spec.color) tex.colorSpace = THREE.SRGBColorSpace;
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.anisotropy = 8; // floors are seen at grazing angles
    cachedGraniteMaps[slot] = tex;
  });
  return cachedGraniteMaps;
}

/** `tint` multiplies the diffuse, so each room keeps its blueprint floor colour. */
export function createGraniteFloorMaterial(tint = 0xffffff, options = {}) {
  const maps = loadGraniteMaps();
  const normalStrength = options.normalScale ?? 0.8;
  // The diffuse map is mid-grey granite, so a tint can only darken it. A gain above 1 lifts the
  // floor toward a pale tile; linear colour values are not clamped to 1.
  const brightness = options.brightness ?? 1.5;
  const mat = new THREE.MeshStandardMaterial({
    color: tint,
    map: maps.map,
    normalMap: maps.normalMap,
    roughnessMap: maps.roughnessMap,
    normalScale: new THREE.Vector2(normalStrength, normalStrength),
    roughness: 1,
    metalness: 0,
  });
  mat.color.multiplyScalar(brightness);
  mat.userData.plaster = true; // metre-tiled slab UVs, see the header comment
  return mat;
}
