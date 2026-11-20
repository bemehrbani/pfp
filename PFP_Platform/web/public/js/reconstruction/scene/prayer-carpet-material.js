/**
 * Prayer-rug floor covering for the two green-floored rooms: the boys' ground-floor classroom
 * (station 3) and the girls' first-floor assembly hall (station 5).
 *
 * The image is one whole rug (689 x 1024, 2:3 portrait) and is repeated across the floor in both
 * directions. Each repeat is sized as a real rug, so the 2:3 proportion is kept instead of being
 * stretched to a square tile.
 */

import * as THREE from 'three';

/** Size of one rug in metres. Keep the 2:3 ratio of the image (689 x 1024). */
export const PRAYER_RUG_WIDTH_METRES = 0.8;
export const PRAYER_RUG_LENGTH_METRES = 1.2;

/**
 * Direction the niche (pointed arch) of every rug faces, in degrees clockwise from north:
 * 315 is north-west. (For reference, the qibla seen from Minab is about 254, west-southwest.)
 */
export const RUG_FACING_BEARING_DEG = 315;

// Scene axes: -X is west and +Z is south (the yard and front facade are at +Z). A bearing
// measured clockwise from north therefore gives east = sin(b) = +X and south = -cos(b) = +Z.
const bearingRad = (RUG_FACING_BEARING_DEG * Math.PI) / 180;
/** Unit vector (x, z) along the rug's length, pointing from the base toward the niche. */
const RUG_FACING = { x: Math.sin(bearingRad), z: -Math.cos(bearingRad) };
/** Unit vector along the rug's width: the facing direction turned 90 degrees clockwise seen from above. */
const RUG_RIGHT = { x: -RUG_FACING.z, z: RUG_FACING.x };

const PRAYER_CARPET_URL = 'textures/carpet/prayer_carpet.jpg';

let cachedCarpetMap = null;

function loadCarpetMap() {
  if (cachedCarpetMap) return cachedCarpetMap;
  const tex = new THREE.TextureLoader().load(PRAYER_CARPET_URL);
  tex.colorSpace = THREE.SRGBColorSpace;
  // The UVs are scaled past 0..1 by the geometry, so the map has to repeat on both axes.
  tex.wrapS = THREE.RepeatWrapping;
  tex.wrapT = THREE.RepeatWrapping;
  tex.anisotropy = 8; // floors are seen at grazing angles
  cachedCarpetMap = tex;
  return tex;
}

export function createPrayerCarpetMaterial() {
  const mat = new THREE.MeshStandardMaterial({
    color: 0xffffff, // the image carries the colour
    map: loadCarpetMap(),
    roughness: 1, // wool pile: no sheen
    metalness: 0,
  });
  // Lets the slab helpers pick the carpet's own UV scaling.
  mat.userData.prayerCarpet = true;
  return mat;
}

export function isPrayerCarpetMaterial(mat) {
  return Boolean(mat && mat.userData && mat.userData.prayerCarpet);
}

/**
 * Box whose top (and bottom) UVs are scaled so one rug spans 0.8 m along X and 1.2 m along Z.
 * BoxGeometry face order is +X, -X, +Y, -Y, +Z, -Z, so the top is the third group of four
 * vertices. Side faces are thin slab edges; they get the same rug scale per metre.
 */
export function prayerCarpetBoxGeometry(width, height, depth) {
  const geo = new THREE.BoxGeometry(width, height, depth);
  const uv = geo.attributes.uv;
  if (uv.count !== 24) return geo;
  const u = PRAYER_RUG_WIDTH_METRES;
  const v = PRAYER_RUG_LENGTH_METRES;
  const faceSpans = [
    [depth / u, height / v],
    [depth / u, height / v],
    [width / u, depth / v],
    [width / u, depth / v],
    [width / u, height / v],
    [width / u, height / v],
  ];
  for (let face = 0; face < 6; face++) {
    const [uRepeat, vRepeat] = faceSpans[face];
    for (let corner = 0; corner < 4; corner++) {
      const i = face * 4 + corner;
      uv.setXY(i, uv.getX(i) * uRepeat, uv.getY(i) * vRepeat);
    }
  }
  // Top (+Y, face 2) and bottom (-Y, face 3): project each vertex onto the rug's own axes so the
  // rug is rotated to face RUG_FACING. u runs along the rug's width and v along its length (the
  // niche end is +v, the top of the image).
  for (const face of [2, 3]) {
    for (let corner = 0; corner < 4; corner++) {
      const i = face * 4 + corner;
      const x = geo.attributes.position.getX(i);
      const z = geo.attributes.position.getZ(i);
      uv.setXY(i, (x * RUG_RIGHT.x + z * RUG_RIGHT.z) / u, (x * RUG_FACING.x + z * RUG_FACING.z) / v);
    }
  }
  uv.needsUpdate = true;
  return geo;
}
