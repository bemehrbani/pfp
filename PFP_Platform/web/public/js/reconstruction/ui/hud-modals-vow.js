/**
 * HUD controls, 3D hotspot pins, Evidence Modal, Artifact Inspector Modal,
 * Accountability Vow petition modal, and Spatial.io `.glb` scene exporter.
 *
 * Uses programmatic DOM construction (`createElement` + `textContent` + `replaceChildren`)
 * everywhere — zero raw HTML string sinks.
 */
import { appState, VOW_BADGE_THRESHOLD } from '../state.js';
import { GUIDED_TOUR_STOPS, HOTSPOT_CONFIGS } from '../data/tour-config.js';
import {
  I18N_DATA,
  setLanguage,
  selectNarratorByActor,
  cycleNarratorForCurrentLanguage,
} from '../data/i18n.js';
import { setTemporalCondition, startWebXRSession } from '../engine/core.js';
import { triggerCameraAnimation, toggleWalkMode } from '../engine/camera-rig.js';
import { setCutawayMode } from '../scene/school-world.js';
import {
  isSpotAudioPlaying,
  pauseSpotNarration,
  resumeSpotNarration,
  stopSpotNarration,
  playSpotNarration,
  resetWalkthroughIdleTimer,
  finishActiveInterlude,
  startGuidedTour,
  stopGuidedTour,
  jumpGuidedTourStep,
} from '../tour/tour-director.js';

function createInspectorMetaPill(label, value, opts = {}) {
  const pill = document.createElement('div');
  pill.className = 'inspector-meta-pill';
  if (opts.spanTwo) pill.style.gridColumn = 'span 2';

  const lbl = document.createElement('span');
  lbl.className = 'lbl';
  lbl.textContent = label;

  const val = document.createElement('span');
  val.className = 'val';
  if (opts.dir) val.dir = opts.dir;
  val.textContent = value;

  pill.append(lbl, val);
  return pill;
}

export function openArtifactInspector(artifactData) {
  const modal = document.getElementById('artifactInspectorModal');
  if (!modal || !artifactData || !artifactData.item) return;

  const currentLang = appState.currentLang;
  const isFa = currentLang === 'fa';
  const isFi = currentLang === 'fi';
  const item = artifactData.item;
  const imgEl = document.getElementById('inspectorImg');
  const titleEl = document.getElementById('inspectorTitle');
  const subEl = document.getElementById('inspectorSubtitle');
  const badgeEl = document.getElementById('inspectorBadge');
  const metaGrid = document.getElementById('inspectorMetaGrid');
  const descEl = document.getElementById('inspectorDesc');
  const primaryLink = document.getElementById('inspectorPrimaryLink');
  const focusBtn = document.getElementById('inspectorFocus3DBtn');

  if (artifactData.artifactType === 'drawing') {
    if (badgeEl) {
      badgeEl.textContent = item.hasBlastDamage
        ? isFa
          ? '💥 سند فیزیکی سوراخ‌شده با ترکش در زیر آوار'
          : '💥 Shrapnel-Torn Rubble Classroom Artifact'
        : isFa
          ? '🎨 نقاشی و تکلیف بیرون کشیده شده از زیر آوار'
          : '🎨 Classroom Drawing Pulled from the Rubble';
    }
    if (imgEl) imgEl.src = item.image || item.thumb || '';
    if (titleEl) {
      titleEl.textContent =
        (item.title && item.title[currentLang]) || (item.title && item.title.en) || item.id;
    }
    if (subEl) {
      subEl.textContent = isFa
        ? `${item.studentNameFa || 'دانش‌آموز دبستان شجره طیبه'} · ${item.dateOnPage || ''}`
        : `${item.studentNameEn || 'Elementary Student'} · ${item.dateOnPage || ''}`;
    }

    if (metaGrid) {
      metaGrid.replaceChildren(
        createInspectorMetaPill(
          isFa ? 'دانش‌آموز' : 'Student / Author',
          isFa ? item.studentNameFa || '—' : item.studentNameEn || '—'
        ),
        createInspectorMetaPill(
          isFa ? 'تاریخ روی برگه' : 'Date on Sheet',
          item.dateOnPage || 'Winter 1404'
        ),
        createInspectorMetaPill(
          isFa ? 'دست‌خط روی برگه' : 'Original Persian Inscription',
          item.transcriptionFa || '—',
          { spanTwo: true, dir: 'rtl' }
        )
      );
    }

    if (descEl) {
      descEl.textContent =
        (item.translation && item.translation[currentLang]) ||
        (item.translation && item.translation.en) ||
        '';
    }
    if (primaryLink) {
      if (item.studentId) {
        primaryLink.href = `child.html?id=${encodeURIComponent(item.studentId)}`;
        primaryLink.textContent = isFa
          ? 'مشاهده صفحه یادبود این دانش‌آموز ←'
          : "Open Student's Memorial Profile →";
      } else {
        primaryLink.href = 'memorial.html#drawingsSection';
        primaryLink.textContent = isFa
          ? 'مشاهده ۲۸ نقاشی زیر آوار در صفحه یادبود ←'
          : 'View All 28 Rubble Drawings →';
      }
    }
  } else {
    const isTeacher = item.category === 'teacher';
    if (badgeEl) {
      badgeEl.textContent = isTeacher
        ? isFa
          ? '👩‍🏫 آموزگار و کادر آموزشی شهیده (نسخه ۳.۰)'
          : '👩‍🏫 Martyred Female Educator (Dataset v3.0.0)'
        : isFa
          ? '🧒 دانش‌آموز شهید دبستان شجره طیبه (نسخه ۳.۰)'
          : '🧒 Martyred Schoolchild (Dataset v3.0.0)';
    }
    if (imgEl) imgEl.src = item.photoPath || item.photo_path || 'images/children/amin-ahmadzade.jpg';
    const primaryName = isFa ? item.nameFa || item.name : item.name || item.nameFa;
    const secondaryName = isFa ? item.name || '' : item.nameFa || '';
    if (titleEl) {
      titleEl.textContent = secondaryName ? `${primaryName} (${secondaryName})` : primaryName || '';
    }
    if (subEl) {
      subEl.textContent =
        artifactData.wingLabel ||
        (isFa ? item.roleFa || item.gradeLabelFa : item.role || item.gradeLabelEn) ||
        '';
    }

    const dobDisplay = item.birthDateShamsi
      ? `${item.birthDateShamsi}${item.birthDateGregorian ? ' (' + item.birthDateGregorian + ')' : ''}`
      : isTeacher
        ? isFa
          ? 'کادر آموزشی مدرسه'
          : 'School Faculty'
        : '—';
    const gradeOrRole = isFa
      ? item.gradeLabelFa || item.roleFa || 'دانش‌آموز'
      : item.gradeLabelEn || item.role || 'Student';
    const ageDisplay = item.age
      ? isFa
        ? `${item.age} سال`
        : `${item.age} years old`
      : isTeacher
        ? isFa
          ? 'فرهنگی شهیده'
          : 'Educator'
        : '—';

    if (metaGrid) {
      metaGrid.replaceChildren(
        createInspectorMetaPill(
          isFa ? 'پایه / سمت' : isFi ? 'Luokka / Tehtävä' : 'Grade / Role',
          gradeOrRole
        ),
        createInspectorMetaPill(isFa ? 'سن در زمان شهادت' : isFi ? 'Ikä' : 'Age', ageDisplay),
        createInspectorMetaPill(
          isFa ? 'تاریخ تولد (شمسی / میلادی)' : 'Birth Date (Solar Hijri / Gregorian)',
          dobDisplay
        ),
        createInspectorMetaPill(
          isFa ? 'آرامگاه' : 'Burial Location',
          item.burialLocation || "Minab Martyrs' Cemetery"
        )
      );
    }

    if (descEl) descEl.textContent = item.notes || item.biography || '';
    if (primaryLink) {
      primaryLink.href = `child.html?id=${encodeURIComponent(item.id)}`;
      primaryLink.textContent = isFa
        ? 'مشاهده شناسنامه کامل و صفحه اختصاصی یادبود ←'
        : isFi
          ? 'Avaa koko muistosivu →'
          : 'Open Full Memorial Profile →';
    }
  }

  if (focusBtn) {
    if (artifactData.focusCam && artifactData.lookAt) {
      focusBtn.style.display = 'inline-flex';
      focusBtn.onclick = () => {
        closeArtifactInspector();
        closeModal();
        setTemporalCondition(0.0);
        const slider = document.getElementById('timelineSlider');
        if (slider) slider.value = 0.0;
        if (typeof artifactData.cutawayMode === 'number') {
          setCutawayMode(artifactData.cutawayMode);
        }
        triggerCameraAnimation(artifactData.focusCam.clone(), artifactData.lookAt.clone());
      };
    } else {
      focusBtn.style.display = 'none';
    }
  }

  modal.classList.add('visible');
}

export function closeArtifactInspector() {
  const modal = document.getElementById('artifactInspectorModal');
  if (modal) modal.classList.remove('visible');
}

export function initHotspots() {
  const container = document.getElementById('canvasContainer');
  if (!container) return;

  HOTSPOT_CONFIGS.forEach((cfg) => {
    cfg.posVec = new THREE.Vector3(cfg.pos[0], cfg.pos[1], cfg.pos[2]);
    cfg.presetCamVec = new THREE.Vector3(cfg.presetCam[0], cfg.presetCam[1], cfg.presetCam[2]);
    cfg.targetVec = new THREE.Vector3(cfg.target[0], cfg.target[1], cfg.target[2]);

    const markerMesh = new THREE.Mesh(
      new THREE.SphereGeometry(0.11, 12, 12),
      new THREE.MeshBasicMaterial({
        color: cfg.isVow ? 0x10b981 : 0xd4a853,
        transparent: true,
        opacity: cfg.isVow ? 0.0 : 0.42,
      })
    );
    markerMesh.visible = !cfg.isVow;
    markerMesh.position.copy(cfg.posVec);
    if (appState.markersGroup) appState.markersGroup.add(markerMesh);
    cfg.mesh = markerMesh;

    const el = document.createElement('div');
    el.className = 'hotspot-pin' + (cfg.isVow ? ' vow-pin' : '');
    el.id = `hotspot-pin-${cfg.id}`;

    const pulseEl = document.createElement('div');
    pulseEl.className = 'pin-pulse';
    const iconEl = document.createElement('div');
    iconEl.className = 'pin-icon';
    iconEl.textContent = cfg.icon;
    const tooltipEl = document.createElement('div');
    tooltipEl.className = 'pin-tooltip';
    tooltipEl.id = `tooltip-${cfg.id}`;
    el.append(pulseEl, iconEl, tooltipEl);

    el.addEventListener('click', (e) => {
      e.stopPropagation();
      if (cfg.isVow) {
        triggerCameraAnimation(cfg.presetCamVec, cfg.targetVec);
        openVowModal();
      } else {
        selectHotspot(cfg.id);
      }
    });
    container.appendChild(el);
    cfg.domElement = el;
  });

  updateHotspotLabels();
}

export function updateHotspotLabels() {
  if (typeof document === 'undefined') return;
  const t = I18N_DATA[appState.currentLang] || I18N_DATA.en;
  HOTSPOT_CONFIGS.forEach((cfg) => {
    const tip = document.getElementById(`tooltip-${cfg.id}`);
    if (tip && t.hotspots[cfg.id]) {
      tip.textContent = t.hotspots[cfg.id].title;
    }
  });
}

let tempProjVec = null;

export function updateHotspotPositions() {
  if (typeof document === 'undefined' || !appState.camera) return;
  const container = document.getElementById('canvasContainer');
  if (!container) return;
  const width = container.clientWidth;
  const height = container.clientHeight;
  if (!tempProjVec) tempProjVec = new THREE.Vector3();

  // Project with the camera matrix of the frame that is about to be rendered.
  // camera.matrixWorldInverse is otherwise one render late, which made every pin
  // swing and land in the wrong place while a right-drag look rotated the camera
  // in place (OrbitControls damping hid the same one-frame error while orbiting).
  const cam = appState.camera;
  cam.updateMatrixWorld();
  cam.matrixWorldInverse.copy(cam.matrixWorld).invert();

  const currentTourStopId =
    appState.isGuidedTour && GUIDED_TOUR_STOPS[appState.currentTourIndex]
      ? GUIDED_TOUR_STOPS[appState.currentTourIndex].hotspotId
      : null;

  HOTSPOT_CONFIGS.forEach((cfg) => {
    if (!cfg.domElement || !cfg.posVec) return;
    const isPostStrikePin = cfg.id === 'crater_damage' || cfg.id === 'second_wave';
    if (appState.damageSliderValue < 0.35 && isPostStrikePin && currentTourStopId !== cfg.id) {
      cfg.domElement.style.display = 'none';
      return;
    }
    if (
      appState.damageSliderValue >= 0.65 &&
      !isPostStrikePin &&
      cfg.id !== 'vow_shrine' &&
      currentTourStopId !== cfg.id
    ) {
      cfg.domElement.style.display = 'none';
      return;
    }
    if (appState.cutawayState === 2 && cfg.id === 'girls_upper_hall' && currentTourStopId !== cfg.id) {
      cfg.domElement.style.display = 'none';
      return;
    }

    tempProjVec.copy(cfg.posVec);
    tempProjVec.project(cam);

    if (tempProjVec.z > 1.0) {
      cfg.domElement.style.display = 'none';
      return;
    }

    cfg.domElement.style.display = 'block';
    cfg.domElement.classList.toggle(
      'active-pin',
      currentTourStopId === cfg.id || appState.activeHotspotId === cfg.id
    );
    const x = (tempProjVec.x * 0.5 + 0.5) * width;
    const y = (-tempProjVec.y * 0.5 + 0.5) * height;
    cfg.domElement.style.transform = `translate(-50%, -50%) translate(${x}px, ${y}px)`;
  });
}

export function selectHotspot(id) {
  appState.activeHotspotId = id;
  const cfg = HOTSPOT_CONFIGS.find((c) => c.id === id);
  if (!cfg) return;

  const slider = document.getElementById('timelineSlider');
  if (id === 'crater_damage' || id === 'second_wave') {
    setTemporalCondition(1.0);
    if (slider) slider.value = 1.0;
  } else {
    setTemporalCondition(0.0);
    if (slider) slider.value = 0.0;
    if (typeof cfg.cutaway === 'number') {
      setCutawayMode(cfg.cutaway);
    }
  }

  triggerCameraAnimation(cfg.presetCamVec, cfg.targetVec);
  showHotspotModal(id);
}

export function showHotspotModal(id) {
  appState.activeHotspotId = id;
  const currentLang = appState.currentLang;
  const t = I18N_DATA[currentLang] || I18N_DATA.en;
  const data = t.hotspots[id];
  if (!data) return;

  const setTxt = (elId, text) => {
    const el = document.getElementById(elId);
    if (el) el.textContent = text;
  };
  setTxt('modalTitle', data.title);
  setTxt('modalCategory', data.category);
  setTxt('modalDesc', data.desc);
  setTxt('modalFinding', data.finding);
  setTxt('modalRef', data.evidenceRef);

  const videoPlayer = document.getElementById('modalVideoPlayer');
  if (videoPlayer && data.videoFile) {
    videoPlayer.src = data.videoFile;
    videoPlayer.loop = true;
    videoPlayer.muted = true;
    videoPlayer.currentTime = 0;
    videoPlayer.play().catch(() => {});
  }

  const spotImg = document.getElementById('modalSpotImg');
  const spotCaption = document.getElementById('modalSpotCaption');
  if (spotImg && data.spotImg) {
    spotImg.src = data.spotImg;
  }
  if (spotCaption && data.spotCaption) {
    spotCaption.textContent = data.spotCaption;
  }

  const testBox = document.getElementById('modalTestimonyBox');
  if (testBox) {
    if (data.testimonyQuote) {
      setTxt('modalTestimonyQuote', data.testimonyQuote);
      setTxt('modalTestimonyAuthor', data.testimonyAuthor || '');
      testBox.classList.add('active');
    } else {
      testBox.classList.remove('active');
    }
  }

  const kidsStrip = document.getElementById('modalKidsStrip');
  const stripCountEl = document.getElementById('modalKidsStripCount');
  if (kidsStrip) kidsStrip.replaceChildren();

  const isFa = currentLang === 'fa';
  const { childrenList, teachersList, drawingsList } = appState;
  let wingVictims = [];
  let wingDrawings = [];

  if (id === 'courtyard_lines') {
    const zohreh = teachersList.find((item) => item.id === 'zohreh-shahriyari');
    const g12 = childrenList
      .filter((c) => c.photoPath && (c.grade === 1 || c.grade === 2))
      .slice(0, 14);
    wingVictims = zohreh ? [zohreh, ...g12] : g12;
    wingDrawings = drawingsList.filter((d) =>
      ['drawing-01', 'drawing-09', 'drawing-11', 'drawing-14'].includes(d.id)
    );
  } else if (id === 'boys_flower_arch') {
    wingVictims = childrenList
      .filter((c) => c.gender === 'boy' && c.photoPath && (c.grade >= 4 || c.grade === 1))
      .slice(0, 18);
    wingDrawings = drawingsList.filter((d) =>
      ['drawing-05', 'drawing-06', 'drawing-07', 'drawing-15', 'drawing-18'].includes(d.id)
    );
  } else if (id === 'boys_classroom') {
    wingVictims = childrenList
      .filter((c) => c.gender === 'boy' && c.photoPath && c.grade <= 3)
      .slice(0, 20);
    wingDrawings = drawingsList.filter((d) =>
      ['drawing-09', 'drawing-11', 'drawing-13', 'drawing-16', 'drawing-19'].includes(d.id)
    );
  } else if (id === 'rainbow_staircase') {
    wingVictims = [...teachersList, ...childrenList.filter((c) => c.photoPath).slice(0, 6)];
    wingDrawings = drawingsList.filter((d) =>
      ['drawing-04', 'drawing-10', 'drawing-23', 'drawing-24', 'drawing-26'].includes(d.id)
    );
  } else if (id === 'girls_upper_hall') {
    const baran = childrenList.find((c) => c.id === 'baran-ghasemy');
    const fatemehR = childrenList.find((c) => c.id === 'fatemeh-rahdar');
    const otherGirls = childrenList.filter(
      (c) =>
        c.gender === 'girl' &&
        c.photoPath &&
        c.id !== 'baran-ghasemy' &&
        c.id !== 'fatemeh-rahdar'
    );
    wingVictims = [baran, fatemehR, ...otherGirls].filter(Boolean);
    wingDrawings = drawingsList.filter((d) =>
      ['drawing-02', 'drawing-27', 'drawing-03', 'drawing-12', 'drawing-20', 'drawing-23'].includes(
        d.id
      )
    );
  } else if (id === 'crater_damage') {
    wingVictims = [
      ...teachersList.slice(0, 6),
      ...childrenList.filter((c) => c.photoPath && (c.grade === 3 || c.grade === 4)).slice(0, 14),
    ];
    wingDrawings = drawingsList.filter(
      (d) =>
        d.hasBlastDamage ||
        ['drawing-16', 'drawing-17', 'drawing-19', 'drawing-21', 'drawing-22'].includes(d.id)
    );
  } else {
    wingVictims = [
      ...childrenList.filter((c) => c.photoPath).slice(0, 12),
      ...teachersList.slice(0, 6),
    ];
    wingDrawings = drawingsList.slice(0, 8);
  }

  if (stripCountEl) {
    stripCountEl.textContent = isFa
      ? `${wingVictims.length} تصویر استودیویی — برای مشاهده شناسنامه کلیک کنید`
      : `${wingVictims.length} verified studio portraits · Click any portrait to inspect`;
  }

  if (kidsStrip) {
    wingVictims.forEach((person) => {
      const card = document.createElement('a');
      card.className = 'kid-mini-card';
      card.href = `child.html?id=${encodeURIComponent(person.id)}`;

      const displayName = (isFa && person.nameFa ? person.nameFa : person.name) || '';
      const roleOrGrade =
        person.category === 'teacher'
          ? isFa
            ? person.roleFa || 'آموزگار شهیده'
            : person.role || 'Educator'
          : isFa
            ? `پایه ${person.grade || '؟'}${person.age ? ' · ' + person.age + ' ساله' : ''}`
            : `Grade ${person.grade || '?'}${person.age ? ' · Age ' + person.age : ''}`;
      const imgSrc =
        person.photoPath || person.photo_path || 'images/children/amin-ahmadzade.jpg';

      const img = document.createElement('img');
      img.src = imgSrc;
      img.alt = displayName;
      img.loading = 'lazy';

      const nameSpan = document.createElement('span');
      nameSpan.className = 'kid-name';
      nameSpan.textContent = displayName;

      const metaSpan = document.createElement('span');
      metaSpan.className = 'kid-meta';
      metaSpan.textContent = roleOrGrade;

      card.append(img, nameSpan, metaSpan);
      kidsStrip.appendChild(card);
    });
  }

  const drwWrap = document.getElementById('modalDrawingsStripWrap');
  const drwStrip = document.getElementById('modalDrawingsStrip');
  if (drwWrap && drwStrip) {
    drwStrip.replaceChildren();
    if (wingDrawings.length > 0) {
      drwWrap.style.display = 'block';
      wingDrawings.forEach((drw) => {
        const dCard = document.createElement('div');
        dCard.className = 'drawing-mini-card';
        const dTitle =
          (drw.title && drw.title[currentLang]) || (drw.title && drw.title.en) || drw.id || '';
        const dAuthor = isFa
          ? drw.studentNameFa || 'دانش‌آموز شهید'
          : drw.studentNameEn || 'Elementary Student';

        const dImg = document.createElement('img');
        dImg.src = drw.thumb || drw.image || '';
        dImg.alt = dTitle;
        dImg.loading = 'lazy';

        const titleSpan = document.createElement('span');
        titleSpan.className = 'drw-title';
        titleSpan.textContent = dTitle;

        const authorSpan = document.createElement('span');
        authorSpan.className = 'drw-author';
        authorSpan.textContent = dAuthor;

        dCard.append(dImg, titleSpan, authorSpan);
        dCard.addEventListener('click', () => {
          openArtifactInspector({
            artifactType: 'drawing',
            item: drw,
            wingLabel: data.title,
          });
        });
        drwStrip.appendChild(dCard);
      });
    } else {
      drwWrap.style.display = 'none';
    }
  }

  const evModal = document.getElementById('evidenceModal');
  if (evModal) evModal.classList.add('visible');
}

export function closeModal() {
  if (typeof document === 'undefined') return;
  const evModal = document.getElementById('evidenceModal');
  if (evModal) evModal.classList.remove('visible');
  const videoPlayer = document.getElementById('modalVideoPlayer');
  if (videoPlayer) {
    videoPlayer.pause();
  }
  appState.activeHotspotId = null;
}

export function updateVowBadge() {
  if (typeof window !== 'undefined') {
    window.vowSignatoryCount = appState.vowSignatoryCount;
  }
  if (typeof document === 'undefined') return;
  const badge = document.getElementById('vowCountBadge');
  if (!badge) return;
  if (appState.vowSignatoryCount >= VOW_BADGE_THRESHOLD) {
    badge.textContent = appState.vowSignatoryCount.toLocaleString();
    badge.style.display = 'inline-block';
  } else {
    badge.textContent = '';
    badge.style.display = 'none';
  }
}

export async function fetchRealVowCount() {
  if (typeof window === 'undefined' || typeof fetch === 'undefined') return;
  let statsUrl = '/api/telegram/vow-stats/';
  if (window.location.protocol === 'file:' || window.location.port === '8090') {
    statsUrl = 'http://localhost:8000/api/telegram/vow-stats/';
  }
  try {
    const resp = await fetch(statsUrl, { cache: 'no-store' });
    if (resp.ok) {
      const data = await resp.json();
      if (typeof data.count === 'number') {
        appState.vowSignatoryCount = data.count;
        updateVowBadge();
      }
    }
  } catch (_) {
    updateVowBadge();
  }
}

export function syncReconstructionVowRolesUI() {
  if (typeof document === 'undefined') return;
  document.querySelectorAll('#vowContributionGroup .vow-role-option').forEach((lbl) => {
    const cb = lbl.querySelector('input[type="checkbox"]');
    lbl.classList.toggle('is-checked', Boolean(cb && cb.checked));
  });
}

export function getReconstructionSelectedVowRoles() {
  if (typeof document === 'undefined') return [];
  const groupEl = document.getElementById('vowContributionGroup');
  if (groupEl) {
    return Array.from(groupEl.querySelectorAll('input[name="vowContribution"]:checked'))
      .map((cb) => cb.value)
      .filter(Boolean);
  }
  const legacySelect = document.getElementById('vowContribution');
  return legacySelect && legacySelect.value ? [legacySelect.value] : [];
}

export function formatReconstructionVowSummary(rolesList) {
  if (!rolesList || rolesList.length === 0) {
    return 'Accountability Vow — Public Petitioner & Campaigner';
  }
  if (rolesList.length === 1) return rolesList[0];
  const shortLabels = rolesList.map((r) =>
    String(r)
      .replace(/^Accountability Vow\s*[—-]\s*/, '')
      .trim()
  );
  return ('Accountability Vow — ' + shortLabels.join(' | ')).slice(0, 500);
}

export function openVowModal() {
  if (typeof document === 'undefined') return;
  const statusEl = document.getElementById('vowStatusMsg');
  if (statusEl) statusEl.style.display = 'none';
  const groupEl = document.getElementById('vowContributionGroup');
  if (groupEl) {
    groupEl.removeAttribute('aria-invalid');
    if (!groupEl.__reconChangeBound) {
      groupEl.__reconChangeBound = true;
      groupEl.addEventListener('change', () => {
        syncReconstructionVowRolesUI();
        if (
          getReconstructionSelectedVowRoles().length > 0 &&
          groupEl.getAttribute('aria-invalid') === 'true'
        ) {
          groupEl.removeAttribute('aria-invalid');
          if (statusEl) statusEl.style.display = 'none';
        }
      });
    }
  }
  syncReconstructionVowRolesUI();
  const vowModal = document.getElementById('vowModal');
  if (vowModal) vowModal.classList.add('visible');
  if (typeof window !== 'undefined' && typeof window.__pfpTrackEvent === 'function') {
    window.__pfpTrackEvent('vow_open');
  }
}

export function closeVowModal() {
  if (typeof document === 'undefined') return;
  const vowModal = document.getElementById('vowModal');
  if (vowModal) vowModal.classList.remove('visible');
}

export async function submitVowForm(e) {
  e.preventDefault();
  const t = I18N_DATA[appState.currentLang] || I18N_DATA.en;
  const name = (document.getElementById('vowName')?.value || '').trim();
  const email = (document.getElementById('vowEmail')?.value || '').trim();
  const telegram_username = (document.getElementById('vowTelegram')?.value || '').trim();
  const phone_number = (document.getElementById('vowPhone')?.value || '').trim();
  const city = (document.getElementById('vowCity')?.value || '').trim();
  const selectedRoles = getReconstructionSelectedVowRoles();
  const personalMsg = (document.getElementById('vowMessage')?.value || '').trim();
  const statusEl = document.getElementById('vowStatusMsg');
  const submitBtn = document.getElementById('vowSubmitBtn');
  const groupEl = document.getElementById('vowContributionGroup');

  if (selectedRoles.length === 0) {
    if (groupEl) groupEl.setAttribute('aria-invalid', 'true');
    if (statusEl) {
      statusEl.style.display = 'block';
      statusEl.style.background = 'rgba(239, 68, 68, 0.16)';
      statusEl.style.color = '#fca5a5';
      statusEl.textContent = t.vowSelectError || 'Please select at least one way to take action.';
    }
    const firstCb = groupEl ? groupEl.querySelector('input[type="checkbox"]') : null;
    if (firstCb) firstCb.focus();
    return;
  }
  if (groupEl) groupEl.removeAttribute('aria-invalid');

  const roleSummary = formatReconstructionVowSummary(selectedRoles);

  if (statusEl) {
    statusEl.style.display = 'block';
    statusEl.style.background = 'rgba(255,255,255,0.06)';
    statusEl.style.color = '#f0ebe3';
    statusEl.textContent = 'Recording your Accountability Vow...';
  }
  if (submitBtn) submitBtn.disabled = true;

  const contact_handle = [telegram_username, phone_number].filter(Boolean).join(' | ');
  const rolesBulletText = selectedRoles.map((item) => `  - ${item}`).join('\n');
  const fullMessage = [
    '[MINAB ACCOUNTABILITY VOW — NOV 20 HYBRID EVENT]',
    `City/Country: ${city}`,
    telegram_username ? `Telegram: ${telegram_username}` : null,
    phone_number ? `Phone/Signal: ${phone_number}` : null,
    selectedRoles.length > 1
      ? `Action Roles (${selectedRoles.length}):\n${rolesBulletText}`
      : `Action Role: ${roleSummary}`,
    'Pledge: Affirmed solemn vow to participate in holding every person in the chain of command accountable.',
    `Note: ${personalMsg || 'Signed from 3D Spatial School Reconstruction.'}`,
  ]
    .filter(Boolean)
    .join('\n');

  let apiUrl = '/api/telegram/submit-contact/';
  if (window.location.protocol === 'file:' || window.location.port === '8090') {
    apiUrl = 'http://localhost:8000/api/telegram/submit-contact/';
  }

  try {
    const resp = await fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name,
        email,
        telegram_username,
        phone_number,
        city_country: city,
        contact_handle,
        role: roleSummary,
        roles: selectedRoles,
        message: fullMessage,
      }),
    });
    let data = {};
    try {
      data = await resp.json();
    } catch (_) {}

    if (!resp.ok) {
      throw new Error(data.error || data.message || `HTTP ${resp.status}`);
    }

    if (typeof data.vow_count === 'number') {
      appState.vowSignatoryCount = data.vow_count;
      window.vowSignatoryCount = data.vow_count;
    } else {
      appState.vowSignatoryCount += 1;
      window.vowSignatoryCount = appState.vowSignatoryCount;
    }
  } catch (_) {
    if (submitBtn) submitBtn.disabled = false;
    if (statusEl) {
      statusEl.style.display = 'block';
      statusEl.style.background = 'rgba(239, 68, 68, 0.16)';
      statusEl.style.color = '#fca5a5';
      statusEl.textContent =
        t.vowSubmitError || 'Could not save your Accountability Vow right now. Please try again.';
    }
    return;
  }

  updateVowBadge();
  if (typeof window.__pfpTrackEvent === 'function') {
    window.__pfpTrackEvent('vow_signed');
  }

  if (statusEl) {
    statusEl.style.background = 'rgba(16, 185, 129, 0.18)';
    statusEl.style.color = '#6ee7b7';
    const countSuffix =
      appState.vowSignatoryCount >= VOW_BADGE_THRESHOLD
        ? ` (#${appState.vowSignatoryCount.toLocaleString()})`
        : '';
    statusEl.textContent = (
      t.vowSuccessMsg || '✓ Thank you, {name}. Your Accountability Vow{count} has been recorded.'
    )
      .replace('{name}', name)
      .replace('{count}', countSuffix);
  }

  const formEl = document.getElementById('vowForm');
  if (formEl) formEl.reset();
  const defaultCb = document.getElementById('vowCheckPetitioner');
  if (defaultCb) defaultCb.checked = true;
  const consentCb = document.getElementById('vowCheckbox');
  if (consentCb) consentCb.checked = true;
  syncReconstructionVowRolesUI();
  if (submitBtn) submitBtn.disabled = false;

  setTimeout(() => {
    closeVowModal();
    if (statusEl) statusEl.style.display = 'none';
  }, 2600);
}

export function exportSceneToGLB() {
  if (typeof THREE === 'undefined' || typeof THREE.GLTFExporter === 'undefined') {
    alert('GLTFExporter is still loading. Please try again in a moment.');
    return;
  }
  if (!appState.terrainGroup || !appState.preStrikeModelGroup) return;

  const exporter = new THREE.GLTFExporter();
  const exportGroup = new THREE.Group();
  exportGroup.name = 'Minab_Shajareh_Tayyebeh_School_SpatialIO';
  exportGroup.add(appState.terrainGroup.clone());
  exportGroup.add(appState.preStrikeModelGroup.clone());

  exporter.parse(
    exportGroup,
    (result) => {
      const blob = new Blob([result], { type: 'model/gltf-binary' });
      const objUrl = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = objUrl;
      link.download = 'minab_shajareh_tayyebeh_spatial.glb';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      setTimeout(() => URL.revokeObjectURL(objUrl), 5000);
    },
    { binary: true }
  );
}

export function initUIControls() {
  const slider = document.getElementById('timelineSlider');
  if (slider) {
    slider.addEventListener('input', (e) => {
      setTemporalCondition(parseFloat(e.target.value));
    });
  }

  const btnStatePre = document.getElementById('btnStatePre');
  if (btnStatePre) {
    btnStatePre.addEventListener('click', () => {
      setTemporalCondition(0.0);
      if (slider) slider.value = 0;
    });
  }

  const btnStatePost = document.getElementById('btnStatePost');
  if (btnStatePost) {
    btnStatePost.addEventListener('click', () => {
      setTemporalCondition(1.0);
      if (slider) slider.value = 1;
    });
  }

  document.querySelectorAll('.lang-btn[data-lang]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const lang = btn.getAttribute('data-lang');
      if (lang) setLanguage(lang);
    });
  });

  document.querySelectorAll('[data-voice-slot]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const slot = btn.getAttribute('data-voice-slot');
      if (slot) selectNarratorByActor(slot);
    });
  });

  const btnGuidedTour = document.getElementById('btnGuidedTour');
  if (btnGuidedTour) {
    btnGuidedTour.addEventListener('click', () => {
      if (appState.isGuidedTour) stopGuidedTour();
      else startGuidedTour();
    });
  }

  const btnHudNarrator = document.getElementById('btnHudNarrator');
  if (btnHudNarrator) {
    btnHudNarrator.addEventListener('click', cycleNarratorForCurrentLanguage);
  }
  const btnSubrowNarrator = document.getElementById('btnSubrowNarrator');
  if (btnSubrowNarrator) {
    btnSubrowNarrator.addEventListener('click', cycleNarratorForCurrentLanguage);
  }
  const btnStoryNarrator = document.getElementById('btnStoryNarrator');
  if (btnStoryNarrator) {
    btnStoryNarrator.addEventListener('click', () => {
      resetWalkthroughIdleTimer();
      cycleNarratorForCurrentLanguage();
    });
  }

  const btnCutaway = document.getElementById('btnCutaway');
  if (btnCutaway) {
    btnCutaway.addEventListener('click', () => {
      setTemporalCondition(0.0);
      if (slider) slider.value = 0.0;
      setCutawayMode(appState.cutawayState + 1);
      if (appState.cutawayState !== 0) {
        triggerCameraAnimation(new THREE.Vector3(-18, 22, 18), new THREE.Vector3(0, 2.5, -5));
      }
    });
  }

  const btnSkipInterlude = document.getElementById('btnSkipInterlude');
  if (btnSkipInterlude) {
    btnSkipInterlude.addEventListener('click', () => {
      finishActiveInterlude();
    });
  }

  const btnStoryPrev = document.getElementById('btnStoryPrev');
  if (btnStoryPrev) {
    btnStoryPrev.addEventListener('click', () => {
      const prevIdx =
        (appState.currentTourIndex - 1 + GUIDED_TOUR_STOPS.length) % GUIDED_TOUR_STOPS.length;
      jumpGuidedTourStep(prevIdx);
    });
  }

  const btnStoryNext = document.getElementById('btnStoryNext');
  if (btnStoryNext) {
    btnStoryNext.addEventListener('click', () => {
      if (appState.activeInterludeState) {
        finishActiveInterlude();
        return;
      }
      if (appState.currentTourIndex === GUIDED_TOUR_STOPS.length - 1) {
        stopGuidedTour();
        openVowModal();
      } else {
        jumpGuidedTourStep(appState.currentTourIndex + 1);
      }
    });
  }

  const btnStoryAudio = document.getElementById('btnStoryAudio');
  if (btnStoryAudio) {
    btnStoryAudio.addEventListener('click', () => {
      resetWalkthroughIdleTimer();
      const stop = GUIDED_TOUR_STOPS[appState.currentTourIndex];
      if (isSpotAudioPlaying()) {
        pauseSpotNarration();
      } else if (stop) {
        resumeSpotNarration(stop.hotspotId);
      }
    });
  }

  ['pointermove', 'pointerdown', 'keydown'].forEach((evtName) => {
    window.addEventListener(
      evtName,
      () => {
        if (appState.isGuidedTour) resetWalkthroughIdleTimer();
      },
      { passive: true }
    );
  });

  window.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    const inspector = document.getElementById('artifactInspectorModal');
    if (inspector && inspector.classList.contains('visible')) {
      closeArtifactInspector();
      return;
    }
    const evModal = document.getElementById('evidenceModal');
    if (evModal && evModal.classList.contains('visible')) {
      closeModal();
      return;
    }
    const vModal = document.getElementById('vowModal');
    if (vModal && vModal.classList.contains('visible')) {
      closeVowModal();
      return;
    }
    if (appState.isGuidedTour) {
      stopGuidedTour();
    }
  });

  const speedSelect = document.getElementById('narrationSpeedSelect');
  if (speedSelect) {
    speedSelect.addEventListener('change', (e) => {
      appState.narrationRate = parseFloat(e.target.value) || 1.0;
      if (appState.narrationAudio) {
        appState.narrationAudio.playbackRate = appState.narrationRate;
      }
    });
  }

  const modalListenBtn = document.getElementById('modalListenBtn');
  if (modalListenBtn) {
    modalListenBtn.addEventListener('click', () => {
      if (!appState.activeHotspotId) return;
      if (isSpotAudioPlaying()) {
        stopSpotNarration();
      } else {
        appState.voiceNarrationEnabled = true;
        playSpotNarration(appState.activeHotspotId);
      }
    });
  }

  const btnStoryVideo = document.getElementById('btnStoryVideo');
  if (btnStoryVideo) {
    btnStoryVideo.addEventListener('click', () => {
      const stop = GUIDED_TOUR_STOPS[appState.currentTourIndex];
      if (stop) {
        if (stop.hotspotId === 'vow_shrine') openVowModal();
        else showHotspotModal(stop.hotspotId);
      }
    });
  }

  const btnStoryClose = document.getElementById('btnStoryClose');
  if (btnStoryClose) btnStoryClose.addEventListener('click', stopGuidedTour);

  const btnWalkMode = document.getElementById('btnWalkMode');
  if (btnWalkMode) btnWalkMode.addEventListener('click', toggleWalkMode);

  const presetBoysArch = document.getElementById('presetBoysArch');
  if (presetBoysArch) presetBoysArch.addEventListener('click', () => selectHotspot('boys_flower_arch'));

  const presetStairs = document.getElementById('presetStairs');
  if (presetStairs) presetStairs.addEventListener('click', () => selectHotspot('rainbow_staircase'));

  const presetGirlsHall = document.getElementById('presetGirlsHall');
  if (presetGirlsHall) presetGirlsHall.addEventListener('click', () => selectHotspot('girls_upper_hall'));

  const presetClassGalleryBtn = document.getElementById('presetClassGallery');
  if (presetClassGalleryBtn) {
    let galleryViewStep = 0;
    presetClassGalleryBtn.addEventListener('click', () => {
      closeModal();
      setTemporalCondition(0.0);
      if (slider) slider.value = 0.0;
      galleryViewStep = (galleryViewStep + 1) % 4;
      if (galleryViewStep === 1) {
        setCutawayMode(2);
        triggerCameraAnimation(
          new THREE.Vector3(-13.2, 2.45, -3.0),
          new THREE.Vector3(-18.2, 1.65, -5.4)
        );
      } else if (galleryViewStep === 2) {
        setCutawayMode(1);
        triggerCameraAnimation(
          new THREE.Vector3(-12.4, 5.85, -1.8),
          new THREE.Vector3(-18.2, 5.25, -7.5)
        );
      } else if (galleryViewStep === 3) {
        setCutawayMode(1);
        triggerCameraAnimation(
          new THREE.Vector3(17.2, 5.7, -11.8),
          new THREE.Vector3(10.5, 5.2, -8.2)
        );
      } else {
        setCutawayMode(2);
        triggerCameraAnimation(
          new THREE.Vector3(-1.4, 2.35, -3.8),
          new THREE.Vector3(-6.0, 1.9, -6.2)
        );
      }
    });
  }

  const presetCrater = document.getElementById('presetCrater');
  if (presetCrater) presetCrater.addEventListener('click', () => selectHotspot('crater_damage'));

  const inspectorCloseBtn = document.getElementById('inspectorCloseBtn');
  if (inspectorCloseBtn) {
    inspectorCloseBtn.addEventListener('click', closeArtifactInspector);
  }
  const inspectorModal = document.getElementById('artifactInspectorModal');
  if (inspectorModal) {
    inspectorModal.addEventListener('click', (e) => {
      if (e.target.id === 'artifactInspectorModal') closeArtifactInspector();
    });
  }

  const btnExportGlb = document.getElementById('btnExportGlb');
  if (btnExportGlb) btnExportGlb.addEventListener('click', exportSceneToGLB);

  const modalSignVowBtn = document.getElementById('modalSignVowBtn');
  if (modalSignVowBtn) {
    modalSignVowBtn.addEventListener('click', () => {
      closeModal();
      openVowModal();
    });
  }

  document.querySelectorAll('#openVowBtn').forEach((btn) => {
    if (!btn.__pfpReconVowBound) {
      btn.__pfpReconVowBound = true;
      btn.addEventListener('click', () => openVowModal());
    }
  });
  const vowCloseEl = document.getElementById('vowCloseBtn');
  if (vowCloseEl && !vowCloseEl.__pfpBound) {
    vowCloseEl.__pfpBound = true;
    vowCloseEl.addEventListener('click', closeVowModal);
  }
  const vowModalEl = document.getElementById('vowModal');
  if (vowModalEl && !vowModalEl.__pfpBackdropBound) {
    vowModalEl.__pfpBackdropBound = true;
    vowModalEl.addEventListener('click', (e) => {
      if (e.target.id === 'vowModal') closeVowModal();
    });
  }
  const vowFormEl = document.getElementById('vowForm');
  if (vowFormEl && !vowFormEl.__pfpBound) {
    vowFormEl.__pfpBound = true;
    vowFormEl.addEventListener('submit', submitVowForm);
  }

  const vrBtn = document.getElementById('enterVrBtn');
  if (vrBtn && typeof navigator !== 'undefined' && 'xr' in navigator) {
    navigator.xr.isSessionSupported('immersive-vr').then((supported) => {
      if (supported) {
        vrBtn.style.display = 'inline-flex';
        vrBtn.addEventListener('click', startWebXRSession);
      }
    });
  }

  const modalCloseBtn = document.getElementById('modalCloseBtn');
  if (modalCloseBtn) modalCloseBtn.addEventListener('click', closeModal);
  const evidenceModal = document.getElementById('evidenceModal');
  if (evidenceModal) {
    evidenceModal.addEventListener('click', (e) => {
      if (e.target.id === 'evidenceModal') closeModal();
    });
  }
}
