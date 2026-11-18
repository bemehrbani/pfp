/**
 * First-floor walls as data, built by `buildWalls` in wall-builder.js (same format as
 * ground-floor-walls.js; read the notes there). Every wall stands on the first-floor slab,
 * so each carries `y0: FLOOR_Y`. IDs are F-01 onward: F-01..F-08 are the exterior envelope,
 * the rest are interior partitions.
 *
 * Windows and doors cut real holes through these walls, so they are see-through.
 */

const EXT = 0.34;
const FLOOR_Y = 3.6;

/** Doors here sit 0.1 m above the first-floor slab. */
const DOOR_BASE = 0.1;
const door = (at) => ({ type: 'door', at, base: DOOR_BASE });

/** Sage-green dado on both faces of a wall; `axis` is the direction the wall runs along. */
const dado = (axis) => {
  const sides = axis === 'x' ? ['N', 'S'] : ['E', 'W'];
  return sides.map((side) => ({ side, mat: 'sage', y0: 0, y1: 1.45, t: 0.03 }));
};

export const FIRST_FLOOR_WALLS = [
  // ---------------------------------------------------------------- Exterior envelope
  {
    id: 'F-01', note: 'South facade, west wing',
    from: [-19.0, 2.4], to: [-7.2, 2.4], t: EXT, y0: FLOOR_Y, outside: 'S',
    openings: [
      { type: 'window', at: 2.8, w: 2.15, h: 0.62, sill: 1.94, mullions: 3 },
      { type: 'window', at: 6.2, w: 1.55, h: 0.95, sill: 1.175, mullions: 1 },
      { type: 'window', at: 9.4, w: 2.25, h: 1.45, sill: 1.325, mullions: 2, sunshade: true },
    ],
  },
  { id: 'F-02', note: 'West step return at the central recess', from: [-7.2, 0.5], to: [-7.2, 2.4], t: EXT, y0: FLOOR_Y, outside: 'W' },
  {
    id: 'F-03', note: 'Central recessed front wall above the portico',
    from: [-7.2, 0.5], to: [7.2, 0.5], t: EXT, y0: FLOOR_Y, outside: 'S',
    openings: [
      { type: 'window', at: 2.4, w: 1.95, h: 1.35, sill: 1.075, mullions: 1 },
      { type: 'window', at: 6.6, w: 3.15, h: 1.35, sill: 1.075, mullions: 3 },
      { type: 'window', at: 11.3, w: 1.95, h: 1.35, sill: 1.075, mullions: 1 },
    ],
  },
  { id: 'F-04', note: 'East step return at the central recess', from: [7.2, 0.5], to: [7.2, 2.4], t: EXT, y0: FLOOR_Y, outside: 'W' },
  {
    id: 'F-05', note: 'South facade, east wing',
    from: [7.2, 2.4], to: [19.0, 2.4], t: EXT, y0: FLOOR_Y, outside: 'S',
    openings: [
      { type: 'window', at: 2.1, w: 2.25, h: 1.45, sill: 1.325, mullions: 2, sunshade: true },
      { type: 'window', at: 5.1, w: 1.05, h: 0.95, sill: 2.075, mullions: 1 },
      { type: 'window', at: 6.8, w: 1.95, h: 1.2, sill: 1.15, mullions: 2 },
      { type: 'window', at: 9.7, w: 2.65, h: 1.1, sill: 1.9, mullions: 3 },
    ],
  },
  {
    id: 'F-06', note: 'West facade',
    from: [-19.0, -13.0], to: [-19.0, 2.4], t: EXT, y0: FLOOR_Y, outside: 'W',
    openings: [
      { type: 'window', at: 1.6, w: 1.05, h: 1.05, sill: 1.225, mullions: 1 },
      { type: 'window', at: 9.6, w: 0.8, h: 0.8, sill: 1.0, mullions: 0 },
      { type: 'window', at: 10.45, w: 0.8, h: 0.8, sill: 1.55, mullions: 0 },
      { type: 'window', at: 14.0, w: 0.95, h: 0.95, sill: 0.875, mullions: 1 },
    ],
  },
  {
    id: 'F-07', note: 'East facade',
    from: [19.0, -13.0], to: [19.0, 2.4], t: EXT, y0: FLOOR_Y, outside: 'E',
    openings: [
      { type: 'window', at: 2.4, w: 2.05, h: 0.7, sill: 2.0, mullions: 3, sunshade: true },
      { type: 'window', at: 7.4, w: 1.85, h: 1.2, sill: 1.35, mullions: 2, sunshade: true },
      { type: 'window', at: 12.6, w: 1.85, h: 1.2, sill: 1.35, mullions: 2, sunshade: true },
    ],
  },
  {
    id: 'F-08', note: 'North (rear) facade',
    from: [-19.0, -13.0], to: [19.0, -13.0], t: EXT, y0: FLOOR_Y, outside: 'N',
    openings: [
      { type: 'window', at: 2.8, w: 2.15, h: 0.62, sill: 2.24, mullions: 2 },
      { type: 'window', at: 6.1, w: 1.2, h: 0.62, sill: 2.24, mullions: 1 },
      { type: 'window', at: 10.2, w: 1.45, h: 1.1, sill: 1.3, mullions: 1 },
      { type: 'window', at: 21.2, w: 1.55, h: 1.05, sill: 1.625, mullions: 1 },
      { type: 'window', at: 25.4, w: 1.55, h: 1.05, sill: 1.625, mullions: 1 },
      { type: 'window', at: 32.8, w: 2.45, h: 0.68, sill: 2.11, mullions: 3 },
    ],
  },

  // ---------------------------------------------------------------- Girls' hall and west wing
  {
    id: 'F-09', note: "Girls' west assembly hall, east partition (open double-door gap at Z = -5.8)",
    from: [-11.5, -13.0], to: [-11.5, 2.4], y0: FLOOR_Y,
    openings: [{ type: 'doorway', at: 7.2, w: 2.0, h: 2.65 }],
  },
  {
    id: 'F-10', note: 'Spine corridor, south wall',
    from: [-11.5, -4.6], to: [7.5, -4.6], y0: FLOOR_Y, liners: dado('x'),
    openings: [door(2.4), door(7.3), door(12.5), door(17.0)],
  },
  {
    id: 'F-11', note: 'Spine corridor, north wall, west of the stairwell',
    from: [-11.5, -7.4], to: [-3.8, -7.4], y0: FLOOR_Y, liners: dado('x'),
    openings: [door(1.9), door(6.2)],
  },
  {
    id: 'F-12', note: 'Spine corridor, north wall, east of the stairwell',
    from: [0.0, -7.4], to: [19.0, -7.4], y0: FLOOR_Y,
    openings: [door(2.1), door(6.2), door(8.05)],
  },

  // ---------------------------------------------------------------- South classrooms
  { id: 'F-13', note: 'South classroom partition, west', from: [-6.8, -4.6], to: [-6.8, 0.5], y0: FLOOR_Y, mat: 'pink', liners: dado('z') },
  { id: 'F-14', note: 'South classroom partition, middle', from: [-1.6, -4.6], to: [-1.6, 0.5], y0: FLOOR_Y, mat: 'pink', liners: dado('z') },
  { id: 'F-15', note: 'South classroom partition, east', from: [3.6, -4.6], to: [3.6, 0.5], y0: FLOOR_Y, liners: dado('z') },
  {
    id: 'F-16', note: 'East wing classroom west wall',
    from: [7.5, -7.4], to: [7.5, 2.4], y0: FLOOR_Y,
    openings: [door(1.6)],
  },
  {
    id: 'F-17', note: 'East wing classroom cross wall',
    from: [7.5, -2.2], to: [19.0, -2.2], y0: FLOOR_Y,
    openings: [door(3.0)],
  },
  { id: 'F-18', note: 'East wing classroom partition', from: [13.5, -7.4], to: [13.5, -2.2], y0: FLOOR_Y },

  // ---------------------------------------------------------------- North classrooms and stairwell
  { id: 'F-19', note: 'North classroom partition, west', from: [-7.8, -13.0], to: [-7.8, -7.4], y0: FLOOR_Y, mat: 'pink', liners: dado('z') },
  { id: 'F-20', note: 'Stairwell upper guard wall, west', from: [-3.8, -13.0], to: [-3.8, -7.4], t: 0.22, y0: FLOOR_Y },
  { id: 'F-21', note: 'Stairwell upper guard wall, east', from: [0.02, -13.0], to: [0.02, -7.4], t: 0.22, y0: FLOOR_Y },
  { id: 'F-22', note: 'North classroom partition, east', from: [4.2, -13.0], to: [4.2, -7.4], y0: FLOOR_Y, mat: 'pink', liners: dado('z') },
  { id: 'F-23', note: 'NE rubble archive, west partition', from: [8.5, -13.0], to: [8.5, -7.85], t: 0.22, y0: FLOOR_Y },
];
