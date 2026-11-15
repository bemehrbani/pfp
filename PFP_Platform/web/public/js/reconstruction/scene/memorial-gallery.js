/**
 * In-world 3D classroom portraits (119 schoolchildren + 26 female educators),
 * 28 recovered rubble drawings, classroom desks, and interactive raycasting.
 *
 * Reuses shared BoxGeometry / PlaneGeometry caches by exact dimensions to eliminate
 * hundreds of duplicate WebGL geometry buffers while preserving identical vertex layout.
 */
import { appState } from '../state.js';

const boxGeoCache = new Map();
const planeGeoCache = new Map();

function getSharedBoxGeo(w, h, d) {
  const key = `${w.toFixed(4)}_${h.toFixed(4)}_${d.toFixed(4)}`;
  let geo = boxGeoCache.get(key);
  if (!geo) {
    geo = new THREE.BoxGeometry(w, h, d);
    boxGeoCache.set(key, geo);
  }
  return geo;
}

function getSharedPlaneGeo(w, h) {
  const key = `${w.toFixed(4)}_${h.toFixed(4)}`;
  let geo = planeGeoCache.get(key);
  if (!geo) {
    geo = new THREE.PlaneGeometry(w, h);
    planeGeoCache.set(key, geo);
  }
  return geo;
}

export function createNameplateTexture(line1Fa, line2En, line3Meta, accentHex) {
  const canvas = document.createElement('canvas');
  canvas.width = 256;
  canvas.height = 76;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#0d1322';
  ctx.fillRect(0, 0, 256, 76);
  ctx.strokeStyle = accentHex || '#d4a853';
  ctx.lineWidth = 3;
  ctx.strokeRect(2, 2, 252, 72);

  ctx.textAlign = 'center';
  ctx.fillStyle = '#fef3c7';
  ctx.font = 'bold 17px Tahoma, sans-serif';
  ctx.fillText((line1Fa || line2En || '').slice(0, 26), 128, 25);

  ctx.fillStyle = '#e2e8f0';
  ctx.font = '600 13px Inter, sans-serif';
  ctx.fillText((line2En || '').slice(0, 28), 128, 46);

  ctx.fillStyle = accentHex || '#d4a853';
  ctx.font = 'bold 12px Inter, sans-serif';
  ctx.fillText((line3Meta || '').slice(0, 32), 128, 65);

  const tex = new THREE.CanvasTexture(canvas);
  tex.needsUpdate = true;
  return tex;
}

export function createWingBannerIn3D(parentGroup, titleEn, titleFa, x, y, z, rotY, width, bgHex, borderHex) {
  const canvas = document.createElement('canvas');
  canvas.width = 768;
  canvas.height = 110;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = bgHex || 'rgba(13, 19, 34, 0.94)';
  ctx.fillRect(0, 0, 768, 110);
  ctx.strokeStyle = borderHex || '#d4a853';
  ctx.lineWidth = 5;
  ctx.strokeRect(3, 3, 762, 104);

  ctx.textAlign = 'center';
  ctx.fillStyle = '#fde68a';
  ctx.font = 'bold 26px Tahoma, sans-serif';
  ctx.fillText(titleFa, 384, 44);

  ctx.fillStyle = '#f8fafc';
  ctx.font = 'bold 20px Inter, sans-serif';
  ctx.fillText(titleEn, 384, 82);

  const tex = new THREE.CanvasTexture(canvas);
  const mat = new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide });
  const mesh = new THREE.Mesh(getSharedPlaneGeo(width, width * (110 / 768)), mat);
  mesh.position.set(x, y, z);
  mesh.rotation.y = rotY;
  parentGroup.add(mesh);
}

export function create3DFramedPortraitOnWall(
  parentGroup,
  loader,
  item,
  x,
  y,
  z,
  rotY,
  frameW,
  frameH,
  borderHex,
  cutawayMode,
  wingLabel,
  focusDist
) {
  const holder = new THREE.Group();
  holder.position.set(x, y, z);
  holder.rotation.y = rotY;

  const backing = new THREE.Mesh(
    getSharedBoxGeo(frameW, frameH, 0.04),
    new THREE.MeshBasicMaterial({ color: borderHex || 0xd4a853 })
  );
  holder.add(backing);

  const innerMat = new THREE.MeshBasicMaterial({ color: 0x1e293b, side: THREE.DoubleSide });
  const portraitH = frameH * 0.76;
  const portraitW = frameW * 0.9;
  const portraitPlane = new THREE.Mesh(getSharedPlaneGeo(portraitW, portraitH), innerMat);
  portraitPlane.position.set(0, frameH * 0.09, 0.026);
  holder.add(portraitPlane);

  const imgUrl =
    item.photoPath || item.photo_path || (item.photoGrid ? `images/children/child_${item.photoGrid}.jpg` : null);
  if (imgUrl) {
    loader.load(imgUrl, (tex) => {
      portraitPlane.material = new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide });
      portraitPlane.material.needsUpdate = true;
    });
  }

  const metaText =
    item.category === 'teacher'
      ? item.role || 'Educator'
      : `Grade ${item.grade || '?'} · Age ${item.age || '?'}`;
  const labelTex = createNameplateTexture(
    item.nameFa || item.full_name_fa,
    item.name || item.full_name_en,
    metaText,
    borderHex === 0xf472b6 ? '#f472b6' : '#d4a853'
  );
  const labelPlane = new THREE.Mesh(
    getSharedPlaneGeo(portraitW, frameH * 0.2),
    new THREE.MeshBasicMaterial({ map: labelTex, side: THREE.DoubleSide })
  );
  labelPlane.position.set(0, -frameH * 0.38, 0.026);
  holder.add(labelPlane);

  const dist = typeof focusDist === 'number' ? focusDist : 1.85;
  const normal = new THREE.Vector3(0, 0, 1).applyAxisAngle(new THREE.Vector3(0, 1, 0), rotY);
  const focusCam = new THREE.Vector3(x, y + 0.08, z).add(normal.clone().multiplyScalar(dist));
  const lookAt = new THREE.Vector3(x, y, z);

  const artifactData = {
    artifactType: 'victim',
    item,
    wingLabel: wingLabel || 'Reconstructed School Interior',
    focusCam,
    lookAt,
    cutawayMode: typeof cutawayMode === 'number' ? cutawayMode : 2,
  };
  portraitPlane.userData = artifactData;
  backing.userData = artifactData;
  labelPlane.userData = artifactData;
  appState.clickable3DArtifacts.push(portraitPlane, backing, labelPlane);

  parentGroup.add(holder);
}

export function create3DRubbleDrawingOnWall(
  parentGroup,
  loader,
  drw,
  x,
  y,
  z,
  rotY,
  frameW,
  frameH,
  cutawayMode,
  wingLabel,
  focusDist
) {
  const holder = new THREE.Group();
  holder.position.set(x, y, z);
  holder.rotation.y = rotY;

  const borderColor = drw.hasBlastDamage ? 0xef4444 : 0xd4a853;
  const backing = new THREE.Mesh(
    getSharedBoxGeo(frameW, frameH, 0.04),
    new THREE.MeshBasicMaterial({ color: borderColor })
  );
  holder.add(backing);

  const imgH = frameH * 0.76;
  const imgW = frameW * 0.91;
  const artPlane = new THREE.Mesh(
    getSharedPlaneGeo(imgW, imgH),
    new THREE.MeshBasicMaterial({ color: 0x1e293b, side: THREE.DoubleSide })
  );
  artPlane.position.set(0, frameH * 0.09, 0.026);
  holder.add(artPlane);

  loader.load(drw.thumb || drw.image, (tex) => {
    artPlane.material = new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide });
    artPlane.material.needsUpdate = true;
  });

  const labelTex = createNameplateTexture(
    drw.studentNameFa || 'نقاشی زیر آوار',
    drw.title && drw.title.en ? drw.title.en : drw.id,
    drw.dateOnPage || 'Rubble Artifact',
    drw.hasBlastDamage ? '#f87171' : '#fcd34d'
  );
  const labelPlane = new THREE.Mesh(
    getSharedPlaneGeo(imgW, frameH * 0.2),
    new THREE.MeshBasicMaterial({ map: labelTex, side: THREE.DoubleSide })
  );
  labelPlane.position.set(0, -frameH * 0.38, 0.026);
  holder.add(labelPlane);

  const dist = typeof focusDist === 'number' ? focusDist : 1.95;
  const normal = new THREE.Vector3(0, 0, 1).applyAxisAngle(new THREE.Vector3(0, 1, 0), rotY);
  const focusCam = new THREE.Vector3(x, y + 0.08, z).add(normal.clone().multiplyScalar(dist));
  const lookAt = new THREE.Vector3(x, y, z);

  const artifactData = {
    artifactType: 'drawing',
    item: drw,
    wingLabel: wingLabel || 'Classroom Rubble Artifact',
    focusCam,
    lookAt,
    cutawayMode: typeof cutawayMode === 'number' ? cutawayMode : 1,
  };
  artPlane.userData = artifactData;
  backing.userData = artifactData;
  labelPlane.userData = artifactData;
  appState.clickable3DArtifacts.push(artPlane, backing, labelPlane);

  parentGroup.add(holder);
}

export function createClassroomDeskWithDrawing(parentGroup, loader, drw, x, yBase, z, cutawayMode) {
  const deskGroup = new THREE.Group();
  deskGroup.position.set(x, yBase, z);
  deskGroup.userData = { feature: 'classroom_desk' };

  const woodMat = new THREE.MeshStandardMaterial({ color: 0x8b5a2b, roughness: 0.75 });
  const frameMetalMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.55, metalness: 0.4 });

  const top = new THREE.Mesh(getSharedBoxGeo(1.12, 0.05, 0.58), woodMat);
  top.position.set(0, 0.68, 0);
  top.castShadow = true;
  deskGroup.add(top);

  [
    [-0.5, -0.23],
    [0.5, -0.23],
    [-0.5, 0.23],
    [0.5, 0.23],
  ].forEach(([lx, lz]) => {
    const leg = new THREE.Mesh(getSharedBoxGeo(0.045, 0.66, 0.045), frameMetalMat);
    leg.position.set(lx, 0.33, lz);
    leg.castShadow = true;
    deskGroup.add(leg);
  });

  const bench = new THREE.Mesh(getSharedBoxGeo(1.12, 0.045, 0.32), woodMat);
  bench.position.set(0, 0.4, 0.5);
  bench.castShadow = true;
  deskGroup.add(bench);

  [-0.48, 0.48].forEach((bx) => {
    const bLeg = new THREE.Mesh(getSharedBoxGeo(0.045, 0.39, 0.28), frameMetalMat);
    bLeg.position.set(bx, 0.195, 0.5);
    deskGroup.add(bLeg);
  });

  if (drw) {
    const sheet = new THREE.Mesh(
      getSharedPlaneGeo(0.46, 0.34),
      new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide })
    );
    sheet.rotation.x = -Math.PI / 2;
    sheet.position.set(0, 0.712, 0);
    deskGroup.add(sheet);

    loader.load(drw.thumb || drw.image, (tex) => {
      sheet.material = new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide });
      sheet.material.needsUpdate = true;
    });

    const artifactData = {
      artifactType: 'drawing',
      item: drw,
      wingLabel: 'Ground Floor Classroom Desk (Recovered from Rubble)',
      focusCam: new THREE.Vector3(x, yBase + 1.75, z + 1.25),
      lookAt: new THREE.Vector3(x, yBase + 0.7, z),
      cutawayMode: cutawayMode || 2,
    };
    sheet.userData = artifactData;
    appState.clickable3DArtifacts.push(sheet);
  }

  parentGroup.add(deskGroup);
}

export function populate3DSchoolPortraitsAndDrawings() {
  const loader = new THREE.TextureLoader();
  appState.clickable3DArtifacts = [];
  const {
    childrenList,
    teachersList,
    drawingsList,
    memorialBoardsGroup,
    preStrikeModelGroup,
    groundFloorGroup,
    firstFloorGroup,
  } = appState;

  // 1. COURTYARD MEMORIAL AVENUE (24 Double-Sided Steles flanking the Central Vow Shrine Walk at X = -5.2 & X = +2.2)
  const portraitSample = childrenList.filter((c) => c.photoPath).slice(0, 24);
  portraitSample.forEach((child, idx) => {
    const isLeft = idx < 12;
    const slot = isLeft ? idx : idx - 12;
    const x = isLeft ? -5.2 : 2.2;
    const z = 13.0 + slot * 1.2;
    const rotY = isLeft ? Math.PI / 2 : -Math.PI / 2;
    const imgUrl = child.photoPath;

    const post = new THREE.Mesh(
      getSharedBoxGeo(0.96, 1.88, 0.1),
      new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.5 })
    );
    post.position.set(x, 1.08, z);
    post.rotation.y = rotY;
    post.castShadow = true;
    memorialBoardsGroup.add(post);

    const border = new THREE.Mesh(
      getSharedBoxGeo(1.02, 1.94, 0.07),
      new THREE.MeshBasicMaterial({ color: 0xd4a853 })
    );
    post.add(border);

    const labelTex = createNameplateTexture(
      child.nameFa,
      child.name,
      `Grade ${child.grade || '?'} · Age ${child.age || '?'}`,
      '#d4a853'
    );
    const frontLabel = new THREE.Mesh(
      getSharedPlaneGeo(0.88, 0.3),
      new THREE.MeshBasicMaterial({ map: labelTex, side: THREE.DoubleSide })
    );
    frontLabel.position.set(0, -0.68, 0.065);
    post.add(frontLabel);

    const backLabel = frontLabel.clone();
    backLabel.position.set(0, -0.68, -0.065);
    backLabel.rotation.y = Math.PI;
    post.add(backLabel);

    const steleArtifact = {
      artifactType: 'victim',
      item: child,
      wingLabel: 'Courtyard 100 Faces Memorial Walk',
      focusCam: new THREE.Vector3(-1.5, 1.45, z),
      lookAt: new THREE.Vector3(x, 1.15, z),
      cutawayMode: 0,
    };
    post.userData = steleArtifact;
    appState.clickable3DArtifacts.push(post);

    if (imgUrl) {
      loader.load(imgUrl, (tex) => {
        const portraitMesh = new THREE.Mesh(
          getSharedPlaneGeo(0.88, 1.32),
          new THREE.MeshBasicMaterial({ map: tex, side: THREE.DoubleSide })
        );
        portraitMesh.position.set(0, 0.18, 0.065);
        portraitMesh.userData = steleArtifact;
        post.add(portraitMesh);
        appState.clickable3DArtifacts.push(portraitMesh);

        const backMesh = portraitMesh.clone();
        backMesh.position.set(0, 0.18, -0.065);
        backMesh.rotation.y = Math.PI;
        backMesh.userData = steleArtifact;
        post.add(backMesh);
        appState.clickable3DArtifacts.push(backMesh);
      });
    }
  });

  // Devoted 2nd-Grade Teacher Ms. Zohreh Shahriyari Courtyard Stand (Station 1)
  const zohrehTeacher = teachersList.find((t) => t.id === 'zohreh-shahriyari');
  if (zohrehTeacher) {
    const standLegsMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.48, metalness: 0.42 });
    [-0.36, 0.36].forEach((lx) => {
      const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.026, 0.032, 1.25, 10), standLegsMat);
      leg.position.set(8.25 + lx * Math.cos(0.35), 0.625, 4.15 - lx * Math.sin(0.35));
      leg.castShadow = true;
      preStrikeModelGroup.add(leg);
    });
    create3DFramedPortraitOnWall(
      preStrikeModelGroup,
      loader,
      zohrehTeacher,
      8.25,
      1.38,
      4.15,
      0.35,
      1.02,
      1.24,
      0xd4a853,
      0,
      'Morning Schoolyard · Martyred 2nd-Grade Teacher Zohreh Shahriyari & Unborn Son',
      2.25
    );
  }

  if (!groundFloorGroup || !firstFloorGroup) return;

  // 2. GROUND FLOOR WEST WING: BOYS OF GRADES 1, 2 & 3
  const boysGrades1to3 = childrenList.filter((c) => c.gender === 'boy' && (c.grade || 1) <= 3 && c.photoPath);
  createWingBannerIn3D(
    groundFloorGroup,
    `GROUND FLOOR WEST CLASSROOMS · BOYS GRADES 1–3 (${boysGrades1to3.length} STUDENTS)`,
    `کلاس‌های طبقه همکف (بال غربی) · ۵۵ دانش‌آموز پسر پایه‌های اول تا سوم`,
    -15.8,
    3.25,
    -2.3,
    0,
    5.8,
    '#0d1b2a',
    '#38bdf8'
  );

  let bIdx = 0;
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 6; col++) {
      if (bIdx >= boysGrades1to3.length) break;
      const px = -18.1 + col * 0.94;
      const py = 1.22 + row * 1.12;
      create3DFramedPortraitOnWall(
        groundFloorGroup,
        loader,
        boysGrades1to3[bIdx++],
        px,
        py,
        -7.38,
        0,
        0.8,
        0.98,
        0x38bdf8,
        2,
        'Ground Floor West Wing · Boys Classrooms (Grades 1–3)',
        1.75
      );
    }
  }
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 6; col++) {
      if (bIdx >= boysGrades1to3.length) break;
      const px = -18.1 + col * 0.94;
      const py = 1.22 + row * 1.12;
      create3DFramedPortraitOnWall(
        groundFloorGroup,
        loader,
        boysGrades1to3[bIdx++],
        px,
        py,
        -2.72,
        Math.PI,
        0.8,
        0.98,
        0x38bdf8,
        2,
        'Ground Floor West Wing · Boys Classrooms (Grades 1–3)',
        1.75
      );
    }
  }
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 6; col++) {
      if (bIdx >= boysGrades1to3.length) break;
      const px = -18.1 + col * 0.94;
      const py = 1.22 + row * 1.12;
      create3DFramedPortraitOnWall(
        groundFloorGroup,
        loader,
        boysGrades1to3[bIdx++],
        px,
        py,
        -2.28,
        0,
        0.8,
        0.98,
        0x38bdf8,
        2,
        'Ground Floor South-West Classroom · Boys Grades 1–2',
        1.75
      );
    }
  }
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 6; col++) {
      if (bIdx >= boysGrades1to3.length) break;
      const px = -18.1 + col * 0.94;
      const py = 1.22 + row * 1.12;
      create3DFramedPortraitOnWall(
        groundFloorGroup,
        loader,
        boysGrades1to3[bIdx++],
        px,
        py,
        -12.72,
        0,
        0.8,
        0.98,
        0x38bdf8,
        2,
        'Ground Floor North-West Classroom · Boys Grades 1–3',
        1.75
      );
    }
  }
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 6; col++) {
      if (bIdx >= boysGrades1to3.length) break;
      const pz = -5.0 + col * 1.12;
      const py = 1.22 + row * 1.12;
      create3DFramedPortraitOnWall(
        groundFloorGroup,
        loader,
        boysGrades1to3[bIdx++],
        -6.72,
        py,
        pz,
        -Math.PI / 2,
        0.8,
        0.98,
        0x38bdf8,
        2,
        'Ground Floor South-Inner Classroom · Boys Grades 2–3',
        1.65
      );
    }
  }

  const groundDeskDrawings = drawingsList.slice(0, 6);
  for (let d = 0; d < 6; d++) {
    const dx = -17.3 + (d % 3) * 1.65;
    const dz = -5.9 + Math.floor(d / 3) * 1.85;
    createClassroomDeskWithDrawing(groundFloorGroup, loader, groundDeskDrawings[d], dx, 0.2, dz, 2);
  }

  // 3. GROUND FLOOR EAST WING: BOYS OF GRADES 4, 5 & 6
  const boysGrades4to6 = childrenList.filter((c) => c.gender === 'boy' && (c.grade || 1) >= 4 && c.photoPath);
  createWingBannerIn3D(
    groundFloorGroup,
    `GROUND FLOOR EAST WING · BOYS GRADES 4–6 & CEREMONY ROOM (${boysGrades4to6.length} STUDENTS)`,
    `طبقه همکف (بال شرقی) · دانش‌آموزان پسر پایه‌های چهارم تا ششم و اتاق جشن`,
    3.75,
    3.25,
    -8.18,
    0,
    6.4,
    '#0d1b2a',
    '#d4a853'
  );

  let b4Idx = 0;
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 6; col++) {
      if (b4Idx >= boysGrades4to6.length) break;
      const px = 0.95 + col * 1.05;
      const py = 1.22 + row * 1.12;
      create3DFramedPortraitOnWall(
        groundFloorGroup,
        loader,
        boysGrades4to6[b4Idx++],
        px,
        py,
        -3.82,
        Math.PI,
        0.84,
        1.02,
        0xd4a853,
        2,
        'Ground Floor East Wing · Boys Grades 4–6 & Ceremony Room',
        1.75
      );
    }
  }
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 5; col++) {
      if (b4Idx >= boysGrades4to6.length) break;
      const px = 12.2 + col * 1.25;
      const py = 1.22 + row * 1.12;
      create3DFramedPortraitOnWall(
        groundFloorGroup,
        loader,
        boysGrades4to6[b4Idx++],
        px,
        py,
        -2.98,
        0,
        0.84,
        1.02,
        0xd4a853,
        2,
        'Ground Floor East Wing · Boys Grades 4–6 Classroom',
        1.75
      );
    }
  }

  // 4. CENTRAL HALL & RAINBOW STAIRCASE: ALL 26 MARTYRED FEMALE EDUCATORS
  createWingBannerIn3D(
    groundFloorGroup,
    `CENTRAL HALL & RAINBOW STAIRCASE · THE 26 MARTYRED FEMALE EDUCATORS`,
    `سالن مرکزی و راه‌پله رنگین‌کمان · ۲۶ معلم و مدیر شهیده دبستان شجره طیبه`,
    -1.9,
    3.3,
    -8.02,
    0,
    5.6,
    '#1f122b',
    '#f472b6'
  );

  const leftHallSlots = [
    [-3.38, -0.5],
    [-3.38, -1.5],
    [-3.38, -2.5],
    [-6.28, -4.1],
    [-6.28, -5.1],
    [-6.28, -6.1],
    [-6.28, -7.2],
  ];
  const rightHallZ = [-0.4, -1.45, -2.5, -4.4, -5.45, -6.5, -7.45];

  teachersList.forEach((teacher, idx) => {
    const isLeft = idx < 13;
    const localIdx = isLeft ? idx : idx - 13;
    const row = Math.floor(localIdx / 7);
    const col = localIdx % 7;
    const py = 1.22 + row * 1.12;
    if (isLeft) {
      const [lx, lz] = leftHallSlots[col] || [-6.28, -4.5];
      create3DFramedPortraitOnWall(
        groundFloorGroup,
        loader,
        teacher,
        lx,
        py,
        lz,
        Math.PI / 2,
        0.82,
        0.98,
        0xf472b6,
        2,
        'Central Assembly Hall & Rainbow Staircase · 26 Martyred Female Educators',
        1.55
      );
    } else {
      const rz = rightHallZ[col] || -4.5;
      create3DFramedPortraitOnWall(
        groundFloorGroup,
        loader,
        teacher,
        -0.18,
        py,
        rz,
        -Math.PI / 2,
        0.82,
        0.98,
        0xf472b6,
        2,
        'Central Assembly Hall & Rainbow Staircase · 26 Martyred Female Educators',
        1.55
      );
    }
  });

  // 5. FIRST FLOOR WEST GIRLS' ASSEMBLY HALL: ALL 47 MARTYRED SCHOOLGIRLS
  const y1 = 3.6;
  const girlsAll = childrenList.filter((c) => c.gender === 'girl' && c.photoPath);
  createWingBannerIn3D(
    firstFloorGroup,
    `FIRST FLOOR GIRLS' ASSEMBLY HALL · ALL ${girlsAll.length} MARTYRED SCHOOLGIRLS (GRADES 1–6)`,
    `طبقه اول (سالن بزرگ دختران) · ۴۷ دانش‌آموز دختر شهیده در پایه‌های اول تا ششم`,
    -15.25,
    y1 + 3.48,
    -12.7,
    0,
    6.8,
    '#2b1222',
    '#f472b6'
  );

  let gIdx = 0;
  const girlsEastZ = [-12.0, -10.9, -9.8, -8.7, -7.6, -3.9, -2.8, -1.7, -0.6, 0.6, 1.6];
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < girlsEastZ.length; col++) {
      if (gIdx >= girlsAll.length) break;
      create3DFramedPortraitOnWall(
        firstFloorGroup,
        loader,
        girlsAll[gIdx++],
        -11.72,
        y1 + 1.22 + row * 1.12,
        girlsEastZ[col],
        -Math.PI / 2,
        0.82,
        0.98,
        0xf472b6,
        1,
        "First Floor West Wing · Girls' Assembly Hall (Grades 1–6)",
        2.1
      );
    }
  }
  const girlsWestZ = [-9.6, -8.6, -6.9, -5.9, -4.9, -1.6, -0.6];
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < girlsWestZ.length; col++) {
      if (gIdx >= girlsAll.length) break;
      create3DFramedPortraitOnWall(
        firstFloorGroup,
        loader,
        girlsAll[gIdx++],
        -18.72,
        y1 + 1.22 + row * 1.12,
        girlsWestZ[col],
        Math.PI / 2,
        0.82,
        0.98,
        0xf472b6,
        1,
        "First Floor West Wing · Girls' Assembly Hall (Grades 1–6)",
        2.1
      );
    }
  }
  for (let col = 0; col < 6; col++) {
    if (gIdx >= girlsAll.length) break;
    create3DFramedPortraitOnWall(
      firstFloorGroup,
      loader,
      girlsAll[gIdx++],
      -17.8 + col * 1.05,
      y1 + 1.15,
      -12.72,
      0,
      0.82,
      0.96,
      0xf472b6,
      1,
      "First Floor Girls' Hall · North Wall Gallery",
      2.1
    );
  }
  for (let col = 0; col < 6; col++) {
    if (gIdx >= girlsAll.length) break;
    create3DFramedPortraitOnWall(
      firstFloorGroup,
      loader,
      girlsAll[gIdx++],
      -17.8 + col * 1.05,
      y1 + 1.15,
      2.12,
      Math.PI,
      0.82,
      0.96,
      0xf472b6,
      1,
      "First Floor Girls' Hall · South Wall Gallery",
      2.1
    );
  }

  // 6. FIRST FLOOR NE CLASSROOM: ALL 28 DRAWINGS & HOMEWORK PULLED FROM RUBBLE
  createWingBannerIn3D(
    firstFloorGroup,
    `FIRST FLOOR CLASSROOMS · 28 DRAWINGS & HOMEWORK PULLED FROM THE RUBBLE`,
    `کلاس‌های طبقه اول · ۲۸ برگ نقاشی و مشق بیرون کشیده شده از زیر آوار مدرسه`,
    13.75,
    y1 + 3.22,
    -7.64,
    Math.PI,
    7.4,
    '#1e1b18',
    '#fcd34d'
  );

  let dIdx = 0;
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 9; col++) {
      if (dIdx >= drawingsList.length) break;
      const dx = 9.35 + col * 1.06;
      const dy = y1 + 1.18 + row * 1.08;
      create3DRubbleDrawingOnWall(
        firstFloorGroup,
        loader,
        drawingsList[dIdx++],
        dx,
        dy,
        -7.64,
        Math.PI,
        0.92,
        0.98,
        1,
        'First Floor North-East Classroom · Rubble Drawings & Homework Archive',
        1.95
      );
    }
  }
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 5; col++) {
      if (dIdx >= drawingsList.length) break;
      const dz = -8.25 - col * 0.96;
      const dy = y1 + 1.18 + row * 1.08;
      create3DRubbleDrawingOnWall(
        firstFloorGroup,
        loader,
        drawingsList[dIdx++],
        8.72,
        dy,
        dz,
        Math.PI / 2,
        0.86,
        0.98,
        1,
        'First Floor North-East Classroom · Rubble Drawings & Homework Archive',
        1.95
      );
    }
  }
}

export function loadChildrenAndBuildInWorldMemorial() {
  if (typeof CHILDREN !== 'undefined' && Array.isArray(CHILDREN) && CHILDREN.length > 0) {
    appState.childrenList = CHILDREN;
    appState.teachersList = typeof TEACHERS !== 'undefined' && Array.isArray(TEACHERS) ? TEACHERS : [];
    appState.drawingsList = typeof DRAWINGS !== 'undefined' && Array.isArray(DRAWINGS) ? DRAWINGS : [];
    populate3DSchoolPortraitsAndDrawings();
    return;
  }

  if (typeof fetch === 'undefined') return;
  fetch('children.json')
    .then((r) => r.json())
    .then((data) => {
      appState.childrenList = data.map((c) => ({
        ...c,
        name: c.name || c.full_name_en,
        nameFa: c.nameFa || c.full_name_fa,
        photoPath: c.photoPath || c.photo_path || (c.photoGrid ? `images/children/child_${c.photoGrid}.jpg` : null),
      }));
      populate3DSchoolPortraitsAndDrawings();
    })
    .catch((err) => console.warn('Could not load children.json for 3D frames:', err));
}

export function init3DPortraitRaycaster() {
  if (!appState.renderer) return;
  const raycaster = new THREE.Raycaster();
  const pointerNDC = new THREE.Vector2();
  appState.raycaster = raycaster;
  appState.pointerNDC = pointerNDC;
  const dom = appState.renderer.domElement;

  dom.addEventListener('pointerdown', (e) => {
    appState.pointerDownPos.x = e.clientX;
    appState.pointerDownPos.y = e.clientY;
  });

  dom.addEventListener('pointermove', (e) => {
    if (appState.clickable3DArtifacts.length === 0) return;
    const rect = dom.getBoundingClientRect();
    pointerNDC.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    pointerNDC.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(pointerNDC, appState.camera);
    const hits = raycaster.intersectObjects(appState.clickable3DArtifacts, false);
    dom.style.cursor = hits.length > 0 && hits[0].object.visible ? 'pointer' : 'grab';
  });

  dom.addEventListener('pointerup', (e) => {
    const dist = Math.hypot(
      e.clientX - appState.pointerDownPos.x,
      e.clientY - appState.pointerDownPos.y
    );
    if (dist > 6 || appState.clickable3DArtifacts.length === 0) return;

    const rect = dom.getBoundingClientRect();
    pointerNDC.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    pointerNDC.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    raycaster.setFromCamera(pointerNDC, appState.camera);

    const hits = raycaster.intersectObjects(appState.clickable3DArtifacts, false);
    if (hits.length > 0) {
      const hitObj = hits[0].object;
      if (hitObj.userData && hitObj.userData.item) {
        appState.callbacks.openArtifactInspector?.(hitObj.userData);
      }
    }
  });
}
