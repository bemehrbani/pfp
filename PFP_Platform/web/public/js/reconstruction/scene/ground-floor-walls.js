/**
 * Ground-floor walls as data, built by `buildWalls` in wall-builder.js.
 *
 * Coordinates are world metres on the floor plan: +X east, +Z south (the schoolyard side).
 * `from` / `to` are the wall's centre-line end points; `at` on an opening is the distance
 * from `from` to the opening's centre. Open the page with `?walls=1` to see every ID in the
 * scene and click a wall for its numbers.
 *
 * G-01..G-08 are the exterior envelope; G-09 onward are interior partitions, west to east.
 * This is the original FA-121 layout, converted one-to-one from the hand-placed boxes.
 */

const EXT = 0.34;

export const GROUND_FLOOR_WALLS = [
  // ---------------------------------------------------------------- Exterior envelope
  {
    id: 'G-01', note: 'South facade, west wing',
    from: [-19.0, 2.4], to: [-7.2, 2.4], t: EXT, outside: 'S',
    liners: [
      { side: 'S', mat: 'yellowFacade', from: -0.02, to: 11.82, y0: 0.005, y1: 1.955, t: 0.06 },
    ],
    openings: [
      { type: 'window', at: 3.2, w: 1.85, h: 0.58, sill: 2.26, mullions: 3 },
      { type: 'window', at: 9.2, w: 2.35, h: 1.35, sill: 1.075, mullions: 2, sunshade: true },
    ],
  },
  {
    id: 'G-02', note: 'West step return at the central recess, continuing north as the south-inner classroom east wall',
    from: [-7.2, -5.0], to: [-7.2, 2.4], outside: 'E',
    liners: [
      // Yellow dado on the outside of the step (Z = 0.5..2.4 is 5.5..7.4 along the wall)
      { side: 'E', mat: 'yellowFacade', from: 5.49, to: 7.41, y0: 0.005, y1: 1.955, t: 0.06 },
    ],
    openings: [{ type: 'door', at: 0.8 }],
  },
  {
    id: 'G-03', note: 'Central recessed front wall with the main entrance',
    from: [-7.2, 0.5], to: [7.2, 0.5], t: EXT, outside: 'S',
    userData: { wallRole: 'central_front_recess' },
    // Sky-blue dado behind the portico (the entrance doorway cuts it in two)
    liners: [{ side: 'S', mat: 'skyBlue', from: 0.025, to: 14.375, y0: 0, y1: 2.15 }],
    openings: [
      { type: 'window', at: 2.4, w: 1.95, h: 1.45, sill: 1.025, mullions: 1 },
      { type: 'doorway', at: 6.6, w: 3.4, h: 2.85, frame: 'purpleDoor' },
      { type: 'window', at: 10.0, w: 1.95, h: 1.45, sill: 1.025, mullions: 1 },
    ],
  },
  {
    id: 'G-04', note: 'East step return at the central recess',
    from: [7.2, 0.5], to: [7.2, 2.4], t: EXT, outside: 'W',
    liners: [{ side: 'W', mat: 'skyBlue', from: -0.01, to: 1.91, y0: 0, y1: 2.25, t: 0.06 }],
  },
  {
    id: 'G-05', note: 'South facade, east wing, with the secondary entrance',
    from: [7.2, 2.4], to: [19.0, 2.4], t: EXT, outside: 'S',
    liners: [
      { side: 'S', mat: 'skyBlue', from: 0.01, to: 3.59, y0: 0, y1: 2.25 },
      // Concrete sunshade ledge across the east wing
      { side: 'S', mat: 'sunshade', from: 3.4, to: 11.7, y0: 3.01, y1: 3.11, t: 0.52, offset: 0.26 },
    ],
    openings: [
      { type: 'doorway', at: 1.8, w: 1.4, h: 2.98, frame: 'purpleDoor' },
      { type: 'window', at: 6.5, w: 1.95, h: 1.15, sill: 0.845, mullions: 2 },
      { type: 'window', at: 6.5, w: 1.95, h: 0.5, sill: 2.41, mullions: 1 },
      { type: 'window', at: 9.7, w: 2.55, h: 0.96, sill: 1.94, mullions: 3 },
    ],
  },
  {
    id: 'G-06', note: 'West facade (grey finish)',
    from: [-19.0, -13.0], to: [-19.0, 2.4], t: EXT, outside: 'W', mat: 'westGrey',
    openings: [
      { type: 'window', at: 2.5, w: 1.15, h: 1.15, sill: 0.975, mullions: 1 },
      { type: 'window', at: 7.8, w: 1.15, h: 1.15, sill: 0.975, mullions: 1 },
      { type: 'window', at: 13.0, w: 1.15, h: 1.15, sill: 0.975, mullions: 1 },
    ],
  },
  {
    id: 'G-07', note: 'East facade',
    from: [19.0, -13.0], to: [19.0, 2.4], t: EXT, outside: 'E',
    openings: [
      { type: 'window', at: 2.3, w: 1.65, h: 1.15, sill: 1.175, mullions: 1, sunshade: true },
      { type: 'window', at: 7.2, w: 1.85, h: 1.25, sill: 1.125, mullions: 2, sunshade: true },
      { type: 'window', at: 12.6, w: 1.85, h: 1.25, sill: 1.125, mullions: 2, sunshade: true },
    ],
  },
  {
    id: 'G-08', note: 'North (rear) facade',
    from: [-19.0, -13.0], to: [19.0, -13.0], t: EXT, outside: 'N',
    liners: [
      // NW corner pink / charcoal / teal stripes, centre-west teal finish
      { side: 'N', mat: 'pink', from: 0, to: 6.4, y0: 0, y1: 0.68 },
      { side: 'N', mat: 'charcoal', from: 0, to: 6.4, y0: 0.68, y1: 1.36 },
      { side: 'N', mat: 'rearTeal', from: 0, to: 6.4, y0: 1.36, y1: 2.08 },
      { side: 'N', mat: 'rearTeal', from: 6.4, to: 15.2, y0: 0, y1: 2.45 },
    ],
    openings: [
      { type: 'window', at: 22.2, w: 1.85, h: 1.15, sill: 1.175, mullions: 2 },
      { type: 'window', at: 27.2, w: 1.85, h: 1.15, sill: 1.175, mullions: 2 },
      { type: 'window', at: 33.5, w: 2.1, h: 0.58, sill: 2.26, mullions: 3 },
      // Rear staircase door at the stairwell half-landing (X = -0.52, floor at Y = 1.955); its top
      // continues through F-08 above. Keep in sync with STAIR_LANDING_Y in school-world.js.
      { type: 'hole', at: 18.48, w: 1.1, h: 1.7, sill: 1.955 },
    ],
  },

  // ---------------------------------------------------------------- West wing
  {
    id: 'G-09', note: 'SW green-carpet room / mid-west room, continues across the corridor to G-12',
    from: [-18.85, -2.5], to: [-10.6, -2.5],
    // Door in the corridor stretch between G-11 (X = -12.6) and G-12 (X = -10.6)
    openings: [{ type: 'door', at: 7.25 }],
  },
  { id: 'G-10', note: 'Mid-west room / NW room', from: [-18.85, -6.1], to: [-12.6, -6.1] },
  {
    id: 'G-11', note: 'West classrooms / corridor (stops at G-09; the SW room opens onto the corridor)',
    from: [-12.6, -12.9], to: [-12.6, -2.5],
    // NW room door (just north of G-10) and mid-west room door
    openings: [{ type: 'door', at: 6.0 }, { type: 'door', at: 7.9 }],
  },
  {
    id: 'G-12', note: 'Corridor east wall, rear wall to the front (south-inner classroom west wall)',
    from: [-10.6, -13.0], to: [-10.6, 2.25],
    openings: [{ type: 'door', at: 7.2 }],
  },
  { id: 'G-13', note: 'South-inner classroom, north wall', from: [-10.6, -5.0], to: [-7.2, -5.0] },
  {
    id: 'G-15', note: 'Narrow north room, south wall (between G-11 and G-12)',
    from: [-12.6, -9.0], to: [-10.6, -9.0],
    openings: [{ type: 'door', at: 1.0 }],
  },
  {
    id: 'G-33', note: 'North room beside the stairs, south wall (between G-16 and G-22)',
    from: [-8.2, -9.0], to: [-2.24, -9.0],
    openings: [{ type: 'door', at: 2.2 }],
  },
  { id: 'G-16', note: 'Between the two small north rooms', from: [-8.2, -13.0], to: [-8.2, -9.0] },
  { id: 'G-31', note: 'Small room under G-15, south wall', from: [-10.6, -6.6], to: [-8.2, -6.6] },
  {
    id: 'G-32', note: 'Small room under G-15, east wall',
    from: [-8.2, -9.0], to: [-8.2, -6.6],
    openings: [{ type: 'door', at: 1.2 }],
  },

  // ---------------------------------------------------------------- Central hall & stairs
  { id: 'G-17', note: 'Front-left office, east wall', from: [-3.56, -3.4], to: [-3.56, 0.5], t: 0.22 },
  {
    id: 'G-18', note: 'Front-left office, north wall',
    from: [-7.2, -3.4], to: [-3.56, -3.4],
    openings: [{ type: 'door', at: 2.7 }],
  },
  {
    id: 'G-20', note: 'Central hall east wall / ceremony room west wall',
    from: [1.2, -8.2], to: [1.2, 0.5], t: 0.22,
    openings: [
      { type: 'grille', at: 3.58, side: 'E', y: 1.86, w: 1.18, h: 1.02 },
      { type: 'door', at: 4.75 },
    ],
  },
  { id: 'G-22', note: 'Rainbow stairwell, west wall (stops at G-33)', from: [-2.24, -13.0], to: [-2.24, -9.0], t: 0.22 },
  { id: 'G-23', note: 'Rainbow stairwell, east wall', from: [1.2, -13.0], to: [1.2, -8.2], t: 0.22 },

  // ---------------------------------------------------------------- East wing
  { id: 'G-24', note: 'Ceremony room, south wall', from: [1.2, -3.6], to: [7.5, -3.6] },
  {
    id: 'G-25', note: 'Ceremony room, north wall',
    from: [1.2, -8.4], to: [7.5, -8.4],
    openings: [{ type: 'door', at: 4.0 }],
  },
  {
    id: 'G-26', note: 'Ceremony room east wall, continues to the front wall',
    from: [7.5, -8.4], to: [7.5, 0.5],
    openings: [
      { type: 'grille', at: 1.05, side: 'W', y: 1.86, w: 1.25, h: 1.05 },
      { type: 'door', at: 2.4 },
    ],
  },
  {
    id: 'G-27', note: 'Secondary east entrance corridor, east wall',
    from: [11.2, -8.4], to: [11.2, 2.4],
    openings: [{ type: 'door', at: 2.6 }, { type: 'door', at: 7.8 }],
  },
  { id: 'G-28', note: 'Mid-east / SE classrooms', from: [11.2, -3.2], to: [19.0, -3.2] },
  {
    id: 'G-29', note: 'East wing, north partition',
    from: [7.5, -8.4], to: [19.0, -8.4],
    openings: [{ type: 'door', at: 6.0 }],
  },
  { id: 'G-30', note: 'NE pre-school rooms', from: [9.5, -13.0], to: [9.5, -8.4] },
];
