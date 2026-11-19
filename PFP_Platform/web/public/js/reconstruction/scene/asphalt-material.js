/**
 * Asphalt surfaces for the school courtyards and rear alley.
 *
 * Maps come from the Asphalt026C 1K JPG set (colour, OpenGL-convention normal, roughness),
 * served from textures/asphalt. The texture carries the asphalt colour, so the material tint is
 * kept near white and only nudges each yard slightly.
 */

import * as THREE from 'three';
import {
  color,
  float,
  mix,
  normalMap,
  positionWorld,
  rotateUV,
  sin,
  smoothstep,
  texture,
  vec2,
} from 'three/tsl';

/** One texture tile spans this many metres. */
export const ASPHALT_TILE_METRES = 3.0;

const ASPHALT_TEXTURE_DIR = 'textures/asphalt/';
const ASPHALT_MAPS = {
  map: { file: 'Asphalt026C_1K-JPG_Color.jpg', color: true },
  normalMap: { file: 'Asphalt026C_1K-JPG_NormalGL.jpg', color: false },
  roughnessMap: { file: 'Asphalt026C_1K-JPG_Roughness.jpg', color: false },
};

let cachedAsphaltMaps = null;

/** Loads the maps once; colour is decoded as sRGB, normal and roughness stay linear. */
function loadAsphaltMaps() {
  if (cachedAsphaltMaps) return cachedAsphaltMaps;
  const loader = new THREE.TextureLoader();
  cachedAsphaltMaps = {};
  Object.entries(ASPHALT_MAPS).forEach(([slot, spec]) => {
    const tex = loader.load(ASPHALT_TEXTURE_DIR + spec.file);
    if (spec.color) tex.colorSpace = THREE.SRGBColorSpace;
    tex.wrapS = THREE.RepeatWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.anisotropy = 8; // ground is seen at grazing angles
    cachedAsphaltMaps[slot] = tex;
  });
  return cachedAsphaltMaps;
}

/**
 * Asphalt with the tiling hidden. A single repeating texture shows its grid at once, so every
 * map is sampled twice: at the base tile and at a rotated, larger, offset tile. A slow
 * low-frequency mask (world space, so it never lines up with the tile edges) blends the two,
 * and a second slow field varies brightness the way weathered patches do. The two samples have
 * different periods, so the combined pattern only repeats over a far larger distance.
 */
export function createAsphaltMaterial(tint = 0xffffff) {
  const maps = loadAsphaltMaps();
  const mat = new THREE.MeshStandardNodeMaterial({ color: tint, metalness: 0 });

  // World-space coordinates keep the surface continuous across the separate yard planes.
  // The ground planes are rotated -90 degrees about X, so their local +V runs along world -Z.
  // `normalMap` builds its tangent frame from the geometry UVs, so the sampling coordinates must
  // use the same handedness (u = +X, v = -Z) or the bumps shade inverted and the surface looks
  // wrong under the sun and sky light.
  const world = vec2(positionWorld.x, positionWorld.z.negate());
  const uvA = world.div(ASPHALT_TILE_METRES);
  const uvB = rotateUV(world.div(ASPHALT_TILE_METRES * 2.37), float(0.83), vec2(0.5, 0.5)).add(vec2(0.37, 0.61));

  // Smooth 0..1 field from three plane waves heading in different, non-axis-aligned directions.
  // A product of two axis-aligned sines tiles into a checkerboard of saturated cells, which is
  // exactly what showed from above; summing oblique waves gives irregular blobs instead.
  const waves = (a, b, c) => {
    const w = (dx, dz, phase) => sin(world.x.mul(dx).add(world.y.mul(dz)).add(phase));
    return w(a[0], a[1], 1.3).add(w(b[0], b[1], 0.4)).add(w(c[0], c[1], 2.1)).div(6).add(0.5);
  };
  const blendField = waves([0.113, 0.071], [-0.067, 0.131], [0.159, -0.043]);
  const patch = waves([0.047, 0.061], [-0.053, 0.029], [0.019, -0.071]);

  // The blend weight stays within 0.3..0.7, so both samples contribute everywhere. At weight 0
  // or 1 one sample would show alone, and the small-scale one visibly repeats every tile.
  const blend = mix(0.3, 0.7, smoothstep(0.25, 0.75, blendField));
  // Averaging two samples flattens contrast. Rescale the deviation from the map's mean (its
  // lowest mip) by the inverse of that loss, so blended areas keep the same grain strength.
  const keepContrast = float(1).div(blend.mul(blend).add(float(1).sub(blend).mul(float(1).sub(blend))).sqrt());
  const sample = (map) => {
    const mean = texture(map, vec2(0.5, 0.5)).level(float(9));
    const mixed = mix(texture(map, uvA), texture(map, uvB), blend);
    return mean.add(mixed.sub(mean).mul(keepContrast));
  };

  // A custom colorNode replaces the built-in `color` multiply, so the yard tint is applied here.
  // The colour map is photographed asphalt at full exposure, much lighter than the flat
  // 0x3b4049-style yards it replaced and than real worn asphalt (albedo ~0.1-0.2), so it is
  // scaled down; the patch field then varies it around that darker mean.
  mat.colorNode = sample(maps.map).mul(color(tint)).mul(mix(0.4, 0.58, patch));
  // Softened normals: full strength catches the sun and sky as glitter on a wide flat plane.
  mat.normalNode = normalMap(sample(maps.normalMap), vec2(0.6, 0.6));
  // Dry asphalt is matte. The map's own values are fairly low, and the sky environment light
  // then mirrors the sky at grazing angles, so keep the map's variation but floor it high.
  mat.roughnessNode = sample(maps.roughnessMap).g.mul(0.2).add(0.8);
  return mat;
}

/**
 * Flat ground rectangle (width along X, depth along Z once rotated) with UVs scaled so the
 * texture density is the same on every yard regardless of its size. The textures are shared,
 * so tiling lives in the geometry instead of `texture.repeat`.
 */
export function asphaltPlaneGeometry(width, depth, tile = ASPHALT_TILE_METRES) {
  const geo = new THREE.PlaneGeometry(width, depth);
  const uv = geo.attributes.uv;
  for (let i = 0; i < uv.count; i++) {
    uv.setXY(i, uv.getX(i) * (width / tile), uv.getY(i) * (depth / tile));
  }
  uv.needsUpdate = true;
  return geo;
}
