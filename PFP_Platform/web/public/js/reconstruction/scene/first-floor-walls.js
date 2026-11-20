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
  // The middle of the floor is one big hall (x -7.8..7.5, z -8.6..-3.3), bounded north by the shallow
  // north rooms, which end at z = -8.6, level with the top of the stairs. At each end a narrow hallway:
  //   west  x -11.5..-7.8, z -6.5..-4.5, between the two pink rooms, to the big west room through F-09;
  //   east  x 7.5..11.33, z -7.4..-5.2, to the door into the NE archive room.
  {
    id: 'F-09', note: "Girls' west assembly hall, east partition (open double-door gap centred in the west hallway, Z = -5.5)",
    from: [-11.5, -13.0], to: [-11.5, 2.4], y0: FLOOR_Y,
    openings: [{ type: 'doorway', at: 7.5, w: 1.8, h: 2.65 }],
  },
  {
    id: 'F-10', note: 'Hall, south wall (pink room and three classrooms)',
    from: [-7.2, -3.3], to: [7.5, -3.3], y0: FLOOR_Y,
    openings: [door(2.45), door(7.35), door(12.25)],
  },
  {
    id: 'F-28', note: 'West hallway, south wall (north wall of the SW pink room, which reaches further north than the classrooms)',
    from: [-11.5, -4.5], to: [-7.2, -4.5], y0: FLOOR_Y,
    openings: [door(3.3)],
  },
  {
    id: 'F-11', note: 'Hall, north wall, west of the stairwell (shallow room, z -13..-8.6, level with the top of the stairs)',
    from: [-7.8, -8.6], to: [-2.24, -8.6], y0: FLOOR_Y,
    openings: [door(2.3)],
  },
  {
    id: 'F-12', note: 'Hall, north wall, east of the stairwell (one shallow room, z -13..-8.6, running east to the NE archive room wall F-23)',
    from: [1.2, -8.6], to: [8.5, -8.6], y0: FLOOR_Y,
    openings: [door(0.9)],
  },
  {
    id: 'F-27', note: 'East hallway and east classrooms, north wall (south wall of the NE archive room)',
    from: [8.5, -7.4], to: [19.0, -7.4], y0: FLOOR_Y,
    openings: [door(1.0)],
  },
  {
    id: 'F-25', note: 'West hallway, north wall (south wall of the NW pink room)',
    from: [-11.5, -6.5], to: [-7.8, -6.5], y0: FLOOR_Y,
  },

  // ---------------------------------------------------------------- South classrooms
  { id: 'F-13', note: 'South classroom partition, west (continues as the west step return)', from: [-7.2, -4.5], to: [-7.2, 0.5], y0: FLOOR_Y },
  { id: 'F-14', note: 'South classroom partition, middle', from: [-2.3, -3.3], to: [-2.3, 0.5], y0: FLOOR_Y },
  { id: 'F-15', note: 'South classroom partition, east', from: [2.6, -3.3], to: [2.6, 0.5], y0: FLOOR_Y },
  {
    id: 'F-16', note: 'East wing classroom 1, west wall (door onto the hall)',
    from: [7.5, -5.2], to: [7.5, 2.4], y0: FLOOR_Y,
    openings: [door(1.0)],
  },
  // The east wing is classroom 1 (x 7.5..11.33, starting at the east hallway, z = -5.2) and one big
  // classroom (x 11.33..19) running from the north wall F-27.
  {
    id: 'F-26', note: 'East wing classroom 1, north wall (south side of the east hallway)',
    from: [7.5, -5.2], to: [11.33, -5.2], y0: FLOOR_Y,
  },
  {
    id: 'F-17', note: 'East wing, partition between classroom 1 and the big classroom',
    from: [11.33, -7.4], to: [11.33, 2.4], y0: FLOOR_Y,
    // End of the east hallway (z = -6.3) into classroom 2, and classroom 1 <-> 2 (z = -3.9)
    openings: [door(1.1), door(3.5)],
  },

  // ---------------------------------------------------------------- North classrooms and stairwell
  {
    id: 'F-19', note: 'NW pink room, east wall',
    from: [-7.8, -13.0], to: [-7.8, -6.5], y0: FLOOR_Y,
    openings: [door(5.4)], // faces east, onto the hall
  },
  { id: 'F-20', note: 'Stairwell upper guard wall, west', from: [-2.24, -13.0], to: [-2.24, -8.6], t: 0.22, y0: FLOOR_Y },
  { id: 'F-21', note: 'Stairwell upper guard wall, east (stacks on G-23)', from: [1.2, -13.0], to: [1.2, -8.6], t: 0.22, y0: FLOOR_Y },
  {
    id: 'F-23', note: 'NE rubble archive, west wall (door from the hall at z = -8.0)',
    from: [8.5, -13.0], to: [8.5, -7.4], t: 0.22, y0: FLOOR_Y,
    openings: [door(5.0)],
  },
];
