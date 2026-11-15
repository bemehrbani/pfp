/**
 * Shared depth layering for the wall-mounted photo, drawing and screen frames.
 *
 * Each frame is a solid backing panel with thin decal planes (photo, nameplate,
 * plaque) floating in front of it. Those planes need real Z separation: coplanar or
 * millimetre-close decals lose the depth test and shimmer. All decal offsets live
 * here so every frame shares one stack.
 */

/** Thickness of the solid backing box every frame is hung on. */
export const FRAME_BACKING_DEPTH = 0.04;

/** Front face of that backing, in frame-local Z. */
export const FRAME_BACKING_FRONT = FRAME_BACKING_DEPTH / 2;

/** Gap between a decal plane and the surface behind it. */
export const FRAME_DECAL_GAP = 0.014;

/** Extra Z separation between two decals stacked on the same backing. */
export const FRAME_STACK_STEP = 0.008;

// --- Normalised layout shared by portraits and drawings (fractions of frameH) ---

/** Vertical centre of the photo / drawing. */
export const FRAME_IMAGE_CENTER_Y = 0.09;

/** Height of the photo / drawing. */
export const FRAME_IMAGE_HEIGHT = 0.76;

/** Height of the nameplate. */
export const FRAME_LABEL_HEIGHT = 0.2;

/** Vertical centre of the nameplate, clear of the photo's bottom edge (-0.29). */
export const FRAME_LABEL_CENTER_Y = -0.395;

/**
 * Decal material: a basic material with polygon offset, so a decal reliably wins the
 * depth test against the surface behind it even on a 16-bit depth buffer.
 */
export function makeDecalMaterial(params) {
  return new THREE.MeshBasicMaterial(
    Object.assign(
      {
        side: THREE.DoubleSide,
        polygonOffset: true,
        polygonOffsetFactor: -1,
        polygonOffsetUnits: -1,
      },
      params || {}
    )
  );
}

/** Local Z for the photo / drawing decal on a standard backing. */
export const FRAME_IMAGE_Z = FRAME_BACKING_FRONT + FRAME_DECAL_GAP;

/** Local Z for the nameplate, one stack step above the photo. */
export const FRAME_LABEL_Z = FRAME_IMAGE_Z + FRAME_STACK_STEP;
