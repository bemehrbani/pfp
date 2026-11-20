/**
 * Corner joints for data-driven walls (pure maths, no THREE, so it can be tested in Node).
 *
 * Walls are drawn on their centre lines, so where two perpendicular walls meet end to end
 * (an L corner) each one stops on the centre line and leaves a square notch, half of the other
 * wall's thickness deep, on the outside of the corner. `cornerExtensions` finds those corners
 * and says how far each wall end must grow to fill the notch.
 *
 * Ends that land inside the middle of another wall (T junctions, crossings) are not touched.
 */

/** Distance within which two wall end points count as the same corner, in metres. */
const CORNER_TOLERANCE = 0.2;

/** Stops the extension 2 mm short of the other wall's far face so their faces never coincide. */
const FACE_GAP = 0.002;

const DEFAULT_ANGLE_EPS = 0.05;

function unit(def) {
  const dx = def.to[0] - def.from[0];
  const dz = def.to[1] - def.from[1];
  const len = Math.hypot(dx, dz) || 1;
  return [dx / len, dz / len];
}

/**
 * @param {Array} defs  wall definitions ({ id, from, to, t? })
 * @param {number} defaultThickness  thickness used when a wall has no `t`
 * @returns {Map<string, { start: number, end: number }>}  metres to add at each end
 */
export function cornerExtensions(defs, defaultThickness) {
  const thick = (d) => d.t ?? defaultThickness;
  const result = new Map();

  for (const a of defs) {
    const ua = unit(a);
    const ext = { start: 0, end: 0 };

    for (const which of ['start', 'end']) {
      const point = which === 'start' ? a.from : a.to;
      // Direction pointing out of the wall at this end.
      const out = which === 'start' ? [-ua[0], -ua[1]] : ua;

      for (const b of defs) {
        if (b === a) continue;
        const ub = unit(b);
        // Only perpendicular walls form a corner.
        if (Math.abs(ua[0] * ub[0] + ua[1] * ub[1]) > DEFAULT_ANGLE_EPS) continue;

        for (const end of [b.from, b.to]) {
          const dx = end[0] - point[0];
          const dz = end[1] - point[1];
          if (Math.hypot(dx, dz) > CORNER_TOLERANCE) continue;
          // Far face of wall b, measured along the outward direction of wall a.
          const far = dx * out[0] + dz * out[1] + thick(b) / 2 - FACE_GAP;
          if (far > 0.02) ext[which] = Math.max(ext[which], far);
        }
      }
    }
    result.set(a.id, ext);
  }
  return result;
}
