/**
 * Three.js WebGPU renderer (WebGL 2 fallback), lighting, top-level scene groups,
 * pre/post-strike temporal visibility, WebXR entry, and frustum photo helper.
 */
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

import { appState } from '../state.js';

// Bounding box of everything that casts or receives sun shadow: the three walled yards
// (X -34..42.5, Z -19.5..30) plus a margin, and the building height (roof and parapets
// stay under ~14 units). Update this if the site layout in school-world.js grows.
const SITE_SHADOW_BOUNDS = new THREE.Box3(
  new THREE.Vector3(-36, -0.5, -22),
  new THREE.Vector3(44.5, 14, 32)
);
const SUN_DIRECTION = new THREE.Vector3(28, 58, 24).normalize();

/**
 * Aims the sun at the site centre and sizes its orthographic shadow frustum to the site's
 * eight bounding-box corners as seen from the light, so no shadow-map texels are wasted on
 * empty ground around the school.
 */
function fitSunShadowToSite(sunLight, scene) {
  const center = SITE_SHADOW_BOUNDS.getCenter(new THREE.Vector3());
  sunLight.target.position.copy(center);
  scene.add(sunLight.target);
  sunLight.position.copy(center).addScaledVector(SUN_DIRECTION, 80);

  const lightView = new THREE.OrthographicCamera();
  lightView.position.copy(sunLight.position);
  lightView.lookAt(center);
  lightView.updateMatrixWorld(true);

  const { min, max } = SITE_SHADOW_BOUNDS;
  const view = new THREE.Box3();
  const corner = new THREE.Vector3();
  for (const x of [min.x, max.x]) {
    for (const y of [min.y, max.y]) {
      for (const z of [min.z, max.z]) {
        view.expandByPoint(corner.set(x, y, z).applyMatrix4(lightView.matrixWorldInverse));
      }
    }
  }

  const cam = sunLight.shadow.camera;
  const pad = 1;
  cam.left = view.min.x - pad;
  cam.right = view.max.x + pad;
  cam.bottom = view.min.y - pad;
  cam.top = view.max.y + pad;
  // View space looks down -Z, so nearer points have larger z.
  cam.near = Math.max(0.5, -view.max.z - pad);
  cam.far = -view.min.z + pad;
  cam.updateProjectionMatrix();
}

/**
 * Makes every shadow-casting mesh write its FRONT faces into the shadow map.
 *
 * three's default is to render back faces. For a slab that stores the depth of its underside,
 * which is exactly the plane the wall tops and ceiling joints touch, so those contact points
 * compare equal to the stored depth and let sun leak in as a bright line along the ceiling
 * edges. Front faces store the slab's top surface instead, leaving the full slab thickness
 * between the stored depth and the contact plane. Call once after the geometry is built.
 */
export function useFrontFaceShadowCasters(root) {
  root.traverse((obj) => {
    if (!obj.isMesh || !obj.castShadow) return;
    const mats = Array.isArray(obj.material) ? obj.material : [obj.material];
    for (const mat of mats) {
      if (mat && mat.side === THREE.FrontSide) mat.shadowSide = THREE.FrontSide;
    }
  });
  requestSunShadowRefresh();
}

/**
 * Sets up GTAO ambient occlusion through a post-processing RenderPipeline, with temporal
 * reprojection anti-aliasing (TRAA).
 *
 * GTAO's sampling noise is fixed to the screen, so on its own it shimmers over moving
 * geometry. Temporal filtering makes the noise pattern change every frame, and TRAA then
 * averages those frames along each pixel's motion, which converges to smooth occlusion.
 * TRAA also anti-aliases the whole image (it replaces MSAA inside this pipeline).
 *
 * `?ao=0` turns it off, `?ao=debug` shows the raw AO buffer, `?traa=0` keeps AO but skips the
 * temporal pass (noisy, for comparison), `?aoStrength=n` sets the contrast. The AO darkens
 * the final image (direct sun and emissive surfaces included). On any setup failure the plain
 * renderer path stays in use.
 */
export async function initAmbientOcclusion() {
  const params = new URLSearchParams(window.location.search);
  const mode = params.get('ao');
  if (mode === '0' || !appState.renderer) return;
  try {
    const [tsl, aoModule, traaModule] = await Promise.all([
      import('three/tsl'),
      import('three/addons/tsl/display/GTAONode.js'),
      import('three/addons/tsl/display/TRAANode.js'),
    ]);
    const { pass, mrt, output, normalView, velocity, screenUV } = tsl;
    const { scene, camera, renderer } = appState;
    const useTraa = params.get('traa') !== '0' && mode !== 'debug';

    // One geometry pass writes colour, view-space normals and motion vectors. MSAA must be off
    // for TRAA, so the pass gets 0 samples instead of inheriting the renderer's 4.
    const scenePass = pass(scene, camera, { samples: 0 });
    scenePass.setMRT(mrt({ output, normal: normalView, velocity }));
    const sceneColor = scenePass.getTextureNode('output');
    const sceneNormal = scenePass.getTextureNode('normal');
    const sceneVelocity = scenePass.getTextureNode('velocity');
    const sceneDepth = scenePass.getTextureNode('depth');

    const aoPass = aoModule.ao(sceneDepth, sceneNormal, camera);
    aoPass.useTemporalFiltering = useTraa; // rotate the sample pattern each frame for TRAA to average
    aoPass.radius.value = 0.7; // world units: room corners and wall/ceiling joints
    aoPass.samples.value = 16;
    aoPass.thickness.value = 1;

    // Tune the contrast of the occlusion; >1 deepens creases, <1 softens them.
    const strength = Number(params.get('aoStrength')) || 1.4;
    const aoValue = aoPass.getTextureNode().sample(screenUV).r.pow(strength);

    // The AO is multiplied into the finished scene colour as a post-process. (Feeding it to the
    // materials through `builtinAOContext` makes the AO pass render while the scene pass is
    // still writing its target, which WebGPU rejects as a usage conflict.)
    const lit = sceneColor.mul(aoValue);

    const pipeline = new THREE.RenderPipeline(renderer);
    if (mode === 'debug') pipeline.outputNode = aoValue; // white = open, dark = occluded
    else pipeline.outputNode = useTraa ? traaModule.traa(lit, sceneDepth, sceneVelocity, camera) : lit;
    appState.renderPipeline = pipeline;
    console.info('[AO] GTAO pipeline active', { mode: mode || 'default', traa: useTraa, strength });
  } catch (err) {
    console.warn('Ambient occlusion unavailable, rendering without it', err);
    appState.renderPipeline = null;
  }
}

/** Renders one frame, through the AO pipeline when it is active. */
export function renderFrame() {
  const { renderPipeline, renderer, scene, camera } = appState;
  // WebXR presents through its own stereo camera rig, which the post pipeline does not drive.
  if (renderPipeline && !renderer.xr?.isPresenting) renderPipeline.render();
  else renderer.render(scene, camera);
}

/** Re-renders the (otherwise static) sun shadow map on the next frame. */
export function requestSunShadowRefresh() {
  if (appState.sunLight) appState.sunLight.shadow.needsUpdate = true;
}

/**
 * Initializes the Three.js scene, camera, ACES Filmic renderer, OrbitControls,
 * lighting rig, and structural floor/memorial groups.
 */
export async function initThreeEngine() {
  const container = document.getElementById('canvasContainer');
  if (!container) return;
  const width = container.clientWidth || window.innerWidth;
  const height = container.clientHeight || window.innerHeight;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0e17); // fallback until the skybox loads
  // Skybox: six cube faces (+X, -X, +Y, -Y, +Z, -Z) from images/sky/sky_122_2k/.
  new THREE.CubeTextureLoader()
    .setPath('images/sky/sky_122_2k/')
    .load(['px.png', 'nx.png', 'py.png', 'ny.png', 'pz.png', 'nz.png'], (cube) => {
      cube.colorSpace = THREE.SRGBColorSpace;
      scene.background = cube;
      // Image-based lighting from the same sky: the renderer prefilters the cube map itself.
      // It supplies the soft indirect fill that shaded interior walls otherwise lack (the sun
      // is blocked there and the hemisphere light alone is flat). Kept low so the courtyard
      // exposure the tour framing was built around does not shift much.
      scene.environment = cube;
      scene.environmentIntensity = 0.5;
    }, undefined, (err) => console.warn('Skybox failed to load', err));
  scene.fog = new THREE.FogExp2(0x0a0e17, 0.0055);

  const camera = new THREE.PerspectiveCamera(48, width / height, 0.25, 1000);
  camera.position.set(28, 22, 34);

  const renderer = new THREE.WebGPURenderer({
    antialias: true,
    alpha: false,
    powerPreference: 'high-performance',
  });
  // Acquires the GPU device (or the WebGL 2 fallback backend) before any resource is built.
  await renderer.init();
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.shadowMap.enabled = true;
  // The node renderer implements PCF and VSM only; PCFSoft is mapped to PCF with a warning.
  renderer.shadowMap.type = THREE.PCFShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.22;
  if (renderer.xr) {
    renderer.xr.enabled = true;
  }
  container.appendChild(renderer.domElement);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.06;
  controls.maxPolarAngle = Math.PI / 2 - 0.01;
  controls.minDistance = 0.8;
  controls.maxDistance = 140;
  // Left drag orbits, middle drag pans, right drag looks around in place (camera-rig.js
  // intercepts the right button before OrbitControls sees it).
  controls.mouseButtons = {
    LEFT: THREE.MOUSE.ROTATE,
    MIDDLE: THREE.MOUSE.PAN,
    RIGHT: THREE.MOUSE.PAN,
  };
  controls.target.set(0, 3.0, -3);
  controls.addEventListener('start', () => {
    if (appState.isGuidedTour) {
      appState.tourManualCameraOverride = true;
      appState.isAnimatingCamera = false;
    }
  });

  // Light units are physical (three r155+); the π factor maps this rig's 0..1 brightness
  // scale onto them, keeping the courtyard exposure that the tour framing was built around.
  // The ground colour is the light that walls receive from below, i.e. sun bounced off floors
  // and courtyard. A warm plaster/dust tone reads as bounce light; the old cold dark blue
  // (0x263042) left shaded interior walls near black. Sky intensity is trimmed slightly because
  // the environment map (see skybox load above) now adds fill on top.
  const hemiLight = new THREE.HemisphereLight(0xfff9f0, 0x8a7a68, 0.75 * Math.PI);
  hemiLight.position.set(0, 55, 0);
  scene.add(hemiLight);

  const sunLight = new THREE.DirectionalLight(0xfff3db, 1.35 * Math.PI);
  sunLight.castShadow = true;
  sunLight.shadow.mapSize.width = 4096;
  sunLight.shadow.mapSize.height = 4096;
  // A small depth bias plus a normal-offset bias: the normal offset stops self-shadow acne
  // without the large negative depth bias that detached shadows from the thin walls (light
  // leaking at wall bases and corners).
  sunLight.shadow.bias = -0.0002;
  sunLight.shadow.normalBias = 0.04;
  fitSunShadowToSite(sunLight, scene);
  // The sun and all shadow casters are static, so the map is only re-rendered on demand
  // (see requestSunShadowRefresh) rather than every frame. That is what pays for the 4096 map.
  sunLight.shadow.autoUpdate = false;
  sunLight.shadow.needsUpdate = true;
  appState.sunLight = sunLight;
  // Scene content is built after this point, so keep refreshing for the first few seconds.
  appState.shadowWarmupFrames = 240;
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
 * Toggles between the pre-strike (0) and post-strike (1) school models. Any value of 0.5 or
 * more counts as post-strike; the two models are never shown together.
 * @param {number} val
 */
export function setTemporalCondition(val) {
  const isPost = (Number(val) || 0) >= 0.5;
  appState.damageSliderValue = isPost ? 1.0 : 0.0;

  const { preStrikeModelGroup, postStrikeModelGroup } = appState;
  if (preStrikeModelGroup && postStrikeModelGroup) {
    preStrikeModelGroup.visible = !isPost;
    postStrikeModelGroup.visible = isPost;
    requestSunShadowRefresh();
  }

  if (typeof document !== 'undefined') {
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
    // Archive stills are authored in sRGB; tone mapping needs the linear values.
    tex.colorSpace = THREE.SRGBColorSpace;
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
