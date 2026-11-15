/**
 * Shared application state container for the Shajareh Tayyebeh 3D Spatial Reconstruction.
 * Keeps all mutable engine, scene, media, and tour references in one inspectable place
 * without referencing browser globals (`window`, `document`, `THREE`) at module import time.
 */

export const VOW_BADGE_THRESHOLD = 100;

export const appState = {
  currentLang: 'en',
  activeVoiceProfile: 'mostafa_en',
  preferredVoiceByLang: {
    fa: 'mostafa_fa',
    en: 'mostafa_en',
    fi: 'mostafa_fi',
  },

  // Three.js core objects
  scene: null,
  camera: null,
  renderer: null,
  controls: null,
  clock: null,

  // Top-level 3D scene groups
  terrainGroup: null,
  preStrikeModelGroup: null,
  postStrikeModelGroup: null,
  memorialBoardsGroup: null,
  markersGroup: null,

  // Cutaway floor groups inside preStrikeModelGroup
  groundFloorGroup: null,
  firstFloorGroup: null,
  roofGroup: null,
  cutawayState: 0,
  damageSliderValue: 0.0,

  // Camera & navigation state
  activeHotspotId: null,
  isAnimatingCamera: false,
  animationTarget: { pos: null, lookAt: null },
  isWalkMode: false,
  moveKeys: { forward: false, backward: false, left: false, right: false },

  // Casualties, educators & rubble artifacts registry
  childrenList: [],
  teachersList: [],
  drawingsList: [],
  clickable3DArtifacts: [],
  raycaster: null,
  pointerNDC: null,
  pointerDownPos: { x: 0, y: 0 },

  // Vow signatory badge state
  vowSignatoryCount: 0,

  // Guided Tour & media state
  isGuidedTour: false,
  currentTourIndex: 0,
  voiceNarrationEnabled: true,
  tourManualCameraOverride: false,
  tourStepStartTime: 0,
  deterministicWalkthroughRender: false,
  recordingMode: false,
  activeTourRun: null,

  // Video & Blob caches
  activePipReelUrl: '',
  pipBlobCache: new Map(),
  pipInflightCache: new Map(),
  inWorldScreens: [],
  activeInWorldRunKey: '',

  // Audio & interlude runtime handles
  narrationAudio: null,
  archivalAudio: null,
  backgroundScoreAudio: null,
  backgroundScoreFadeTimer: null,
  backgroundScoreTargetVol: 0.0,
  narrationPhase: 'idle',
  narrationPhaseTimer: null,
  activeNarrationHotspot: null,
  narrationRate: 1.0,
  ambientAudioCtx: null,
  ambientGainNode: null,
  ambientPadFilter: null,
  ambientOscillators: [],
  ambientBreezeGain: null,
  ambientBreezeFilter: null,
  ambientBirdTimer: null,
  guidedTourAutoAdvanceTimer: null,
  walkthroughIdleTimer: null,
  activeInterludeState: null,
  bookendTimer: null,

  // Cross-module hooks wired by main.js to keep imports strictly acyclic
  callbacks: {},
};
