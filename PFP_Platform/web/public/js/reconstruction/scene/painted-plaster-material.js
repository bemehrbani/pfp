/**
 * Painted-plaster wall surfaces for the school model.
 *
 * Maps come from the painted_plaster_wall_1k asset set. The EXR maps are
 * converted to 8-bit PNG by scripts/convert_exr_to_png.py and served from
 * textures/plaster. The diffuse map is a neutral off-white, so walls keep their
 * FA-121 palette colour as the material tint and only the surface grain, bumps,
 * and roughness variation come from the textures.
 */

/** One texture tile spans this many metres, so grain density stays plausible. */
export const PLASTER_TILE_METRES = 2.0;

const PLASTER_TEXTURE_DIR = 'textures/plaster/';
const PLASTER_MAP_FILES = {
  map: 'painted_plaster_wall_diff_1k.jpg',
  normalMap: 'painted_plaster_wall_nor_gl_1k.png',
  roughnessMap: 'painted_plaster_wall_rough_1k.png',
};

let cachedPlasterMaps = null;

/**
 * The renderer writes linear output and never decodes sRGB colour maps, so the
 * diffuse map is left undecoded to match the flat palette it replaces. Decoding
 * this map without also switching the renderer's output colourspace would
 * darken every wall against the rest of the scene.
 */
function loadPlasterMaps() {
  if (cachedPlasterMaps) return cachedPlasterMaps;
  const loader = new THREE.TextureLoader();
  cachedPlasterMaps = {};
  Object.keys(PLASTER_MAP_FILES).forEach((slot) => {
    const tex = loader.load(PLASTER_TEXTURE_DIR + PLASTER_MAP_FILES[slot]);
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.anisotropy = 4;
    cachedPlasterMaps[slot] = tex;
  });
  return cachedPlasterMaps;
}

export function createPaintedPlasterMaterial(tint, options = {}) {
  const maps = loadPlasterMaps();
  const normalStrength = options.normalScale ?? 1;
  const mat = new THREE.MeshStandardMaterial({
    color: tint,
    map: maps.map,
    normalMap: maps.normalMap,
    roughnessMap: maps.roughnessMap,
    normalScale: new THREE.Vector2(normalStrength, normalStrength),
    roughness: options.roughness ?? 1,
    metalness: 0,
  });
  // Lets the wall helpers pick tiled UVs without tracking every tint by hand.
  mat.userData.plaster = true;
  return mat;
}

export function isPaintedPlasterMaterial(mat) {
  return Boolean(mat && mat.userData && mat.userData.plaster);
}

/**
 * BoxGeometry gives every face UVs of 0..1, which would stretch one tile across
 * a 23 m courtyard wall and squeeze the same tile onto a 0.36 m jamb. Rescaling
 * each face to its own span lets every plaster wall share one material.
 *
 * Only single-segment boxes (all the walls) carry the 24 vertices this walks;
 * segmented boxes are returned untouched.
 */
export function plasterBoxGeometry(width, height, depth, tile = PLASTER_TILE_METRES) {
  const geo = new THREE.BoxGeometry(width, height, depth);
  const uv = geo.attributes.uv;
  if (uv.count !== 24) return geo;
  // BoxGeometry face order is +X, -X, +Y, -Y, +Z, -Z.
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
    for (let corner = 0; corner < 4; corner++) {
      const i = face * 4 + corner;
      uv.setXY(i, (uv.getX(i) * uSpan) / tile, (uv.getY(i) * vSpan) / tile);
    }
  }
  uv.needsUpdate = true;
  return geo;
}

/** Wall-sized geometry for a plaster material, plain geometry for anything else. */
export function wallBoxGeometry(width, height, depth, mat) {
  return isPaintedPlasterMaterial(mat)
    ? plasterBoxGeometry(width, height, depth)
    : new THREE.BoxGeometry(width, height, depth);
}
