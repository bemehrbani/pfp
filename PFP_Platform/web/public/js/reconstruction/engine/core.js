/**
 * Three.js (r128) WebGL renderer, lighting, top-level scene groups,
 * pre/post-strike temporal visibility, WebXR entry, and frustum photo helper.
 */
import { appState } from '../state.js';

/**
 * Initializes the Three.js scene, camera, ACES Filmic renderer, OrbitControls,
 * lighting rig, and structural floor/memorial groups.
 */
export function initThreeEngine() {
  const container = document.getElementById('canvasContainer');
  if (!container) return;
  const width = container.clientWidth || window.innerWidth;
  const height = container.clientHeight || window.innerHeight;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0e17);
  scene.fog = new THREE.FogExp2(0x0a0e17, 0.0055);

  const camera = new THREE.PerspectiveCamera(48, width / height, 0.25, 1000);
  camera.position.set(28, 22, 34);

  const renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: false,
    powerPreference: 'high-performance',
  });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.22;
  if (renderer.xr) {
    renderer.xr.enabled = true;
  }
  container.appendChild(renderer.domElement);

  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.06;
  controls.maxPolarAngle = Math.PI / 2 - 0.01;
  controls.minDistance = 0.8;
  controls.maxDistance = 140;
  controls.target.set(0, 3.0, -3);
  controls.addEventListener('start', () => {
    if (appState.isGuidedTour) {
      appState.tourManualCameraOverride = true;
      appState.isAnimatingCamera = false;
    }
  });

  const hemiLight = new THREE.HemisphereLight(0xfff9f0, 0x263042, 0.88);
  hemiLight.position.set(0, 55, 0);
  scene.add(hemiLight);

  const sunLight = new THREE.DirectionalLight(0xfff3db, 1.35);
  sunLight.position.set(28, 58, 24);
  sunLight.castShadow = true;
  sunLight.shadow.mapSize.width = 2048;
  sunLight.shadow.mapSize.height = 2048;
  sunLight.shadow.camera.near = 10;
  sunLight.shadow.camera.far = 150;
  sunLight.shadow.camera.left = -45;
  sunLight.shadow.camera.right = 45;
  sunLight.shadow.camera.top = 45;
  sunLight.shadow.camera.bottom = -45;
  sunLight.shadow.bias = -0.0005;
  scene.add(sunLight);

  const terrainGroup = new THREE.Group();
  terrainGroup.name = 'Minab_Courtyard_And_Boundary';
  const preStrikeModelGroup = new THREE.Group();
  preStrikeModelGroup.name = 'Shajareh_Tayyebeh_School_PreStrike';
  const postStrikeModelGroup = new THREE.Group();
  postStrikeModelGroup.name = 'Shajareh_Tayyebeh_School_PostStrike';
  const memorialBoardsGroup = new THREE.Group();
  memorialBoardsGroup.name = 'InWorld_Children_Portraits_And_Vow_Shrine';
  const markersGroup = new THREE.Group();

  scene.add(terrainGroup);
  scene.add(preStrikeModelGroup);
  scene.add(postStrikeModelGroup);
  scene.add(memorialBoardsGroup);
  scene.add(markersGroup);

  postStrikeModelGroup.visible = false;

  appState.scene = scene;
  appState.camera = camera;
  appState.renderer = renderer;
  appState.controls = controls;
  appState.terrainGroup = terrainGroup;
  appState.preStrikeModelGroup = preStrikeModelGroup;
  appState.postStrikeModelGroup = postStrikeModelGroup;
  appState.memorialBoardsGroup = memorialBoardsGroup;
  appState.markersGroup = markersGroup;

  window.addEventListener('resize', onWindowResize, false);
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden && appState.clock) {
      appState.clock.getDelta();
    }
  });
}

export function onWindowResize() {
  if (typeof document === 'undefined' || !appState.camera || !appState.renderer) return;
  const container = document.getElementById('canvasContainer');
  const width = (container && container.clientWidth) || window.innerWidth;
  const height = (container && container.clientHeight) || window.innerHeight;
  appState.camera.aspect = width / height;
  appState.camera.updateProjectionMatrix();
  appState.renderer.setSize(width, height);
}

/**
 * Switches between pre-strike (0.0) and post-strike (1.0) school models.
 * @param {number} val
 */
export function setTemporalCondition(val) {
  const clamped = Math.max(0.0, Math.min(1.0, Number(val) || 0.0));
  appState.damageSliderValue = clamped;

  const { preStrikeModelGroup, postStrikeModelGroup } = appState;
  if (preStrikeModelGroup && postStrikeModelGroup) {
    if (clamped < 0.05) {
      preStrikeModelGroup.visible = true;
      postStrikeModelGroup.visible = false;
    } else if (clamped > 0.95) {
      preStrikeModelGroup.visible = false;
      postStrikeModelGroup.visible = true;
    } else {
      preStrikeModelGroup.visible = true;
      postStrikeModelGroup.visible = true;
    }
  }

  if (typeof document !== 'undefined') {
    const isPost = clamped >= 0.5;
    const preBtn = document.getElementById('btnStatePre');
    const postBtn = document.getElementById('btnStatePost');
    if (preBtn) preBtn.classList.toggle('active', !isPost);
    if (postBtn) postBtn.classList.toggle('active', isPost);
  }
}

export function startWebXRSession() {
  if (typeof navigator === 'undefined' || !navigator.xr || !appState.renderer) return;
  navigator.xr
    .requestSession('immersive-vr')
    .then((session) => {
      appState.renderer.xr.setSession(session);
    })
    .catch((err) => {
      alert('WebXR session could not be started: ' + err.message);
    });
}

export function createCameraAlignedPhotoInSpace(parentGroup, photoUrl, camPos, photoPos, rotY, width, height) {
  const group = new THREE.Group();
  const loader = new THREE.TextureLoader();

  const yellowLineMat = new THREE.LineBasicMaterial({ color: 0xe5e059 });
  const hw = width / 2;
  const hh = height / 2;

  const corners = [
    new THREE.Vector3(-hw, -hh, 0),
    new THREE.Vector3(hw, -hh, 0),
    new THREE.Vector3(hw, hh, 0),
    new THREE.Vector3(-hw, hh, 0),
  ];

  const frameGroup = new THREE.Group();
  frameGroup.position.set(photoPos[0], photoPos[1], photoPos[2]);
  frameGroup.rotation.y = rotY;
  frameGroup.userData = { photoUrl, feature: 'camera_aligned_photo' };

  const borderPts = [...corners, corners[0]];
  const borderGeo = new THREE.BufferGeometry().setFromPoints(borderPts);
  frameGroup.add(new THREE.Line(borderGeo, yellowLineMat));

  const worldDelta = new THREE.Vector3(
    camPos[0] - photoPos[0],
    camPos[1] - photoPos[1],
    camPos[2] - photoPos[2]
  );
  const localCam = worldDelta.applyAxisAngle(new THREE.Vector3(0, 1, 0), -rotY);
  if (localCam.lengthSq() < 0.25) {
    localCam.set(0, 0, 2.2);
  }

  const rayPts = [];
  corners.forEach((c) => {
    rayPts.push(localCam, c);
  });
  const rayGeo = new THREE.BufferGeometry().setFromPoints(rayPts);
  frameGroup.add(new THREE.LineSegments(rayGeo, yellowLineMat));

  loader.load(photoUrl, (tex) => {
    const mat = new THREE.MeshBasicMaterial({
      map: tex,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.92,
    });
    const mesh = new THREE.Mesh(new THREE.PlaneGeometry(width, height), mat);
    frameGroup.add(mesh);
  });

  group.add(frameGroup);
  parentGroup.add(group);
  return frameGroup;
}
