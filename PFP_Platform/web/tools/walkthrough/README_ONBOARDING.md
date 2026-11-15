# Minab Primary School 3D Spatial Walkthrough & Director's Cut Renderer
### Developer Onboarding Guide (`reconstruction.html` + `js/reconstruction/`)

Welcome! This guide covers the architecture, media pipeline, and headless 1080p60/4K video export workflow for the **Shajareh Tayyebeh Primary School 3D Spatial Reconstruction & Memorial Walkthrough** ahead of the **November 20, 2026 World Children's Day** premiere at **Helsinki XR Center (HXRC)**.

---

## 1. Quick Start (Local Run in 60 Seconds)

Large `.mp4` media files are intentionally excluded from Git object history (`.gitignore`) while all human voiceovers (`media/narration/voices/**`) are tracked in Git.

```bash
# 1. Pull the gitignored ambient score, 3D room wall clips & Cinema Interludes from staging:
bash PFP_Platform/web/tools/walkthrough/sync_media.sh

# 2. Serve the public web directory locally:
cd PFP_Platform/web/public
python3 -m http.server 8123

# 3. Open in Chrome / Chromium:
#    Interactive 3D experience:  http://localhost:8123/reconstruction.html
#    Auto-start Director's Cut:  http://localhost:8123/reconstruction.html?autostart=1&lang=en
#    Eyewitness raw media hub:   http://localhost:8123/multimedia.html
```

---

## 2. Core Architecture (`PFP_Platform/web/public/`)

| File / Directory | Purpose |
|---|---|
| `reconstruction.html` & `css/reconstruction.css` | Full-viewport WebGL canvas, HUD controls, segmented narrator chooser (`Mostafa · Leila · Ali`), Prologue/Epilogue bookends, Cinema Witness Interlude overlay (`16:9`, `4:3`, `3:4`, `4:5`, `9:16` true-aspect frames), and extracted stylesheet. |
| `js/reconstruction/main.js` & `state.js` | ES module entry point, `requestAnimationFrame` loop, `window.PFPRecon` / Playwright shims, and shared `appState` container. |
| `js/reconstruction/engine/core.js` & `camera-rig.js` | Three.js (`r128`) renderer, ACES Filmic exposure, directional/hemisphere lighting, pre/post-strike visibility, WebXR session setup, waypoint spline interpolation, and WASD navigation. |
| `js/reconstruction/scene/school-world.js`, `memorial-gallery.js` & `in-world-screens.js` | Procedural pre-strike & post-strike 2-floor school geometry, courtyard murals, 145 student/teacher 3D framed portraits, 28 rubble drawings, and lazy-decoded 3D wall video screens. |
| `js/reconstruction/data/tour-config.js` & `i18n.js` | Declarative `GUIDED_TOUR_STOPS` camera spline waypoints, `IN_WORLD_SCREEN_SPECS`, `WALKTHROUGH_INTERLUDES`, trilingual (`EN`/`FI`/`FA`) copy, and `NARRATOR_PROFILES`. |
| `js/reconstruction/tour/tour-director.js` & `ui/hud-modals-vow.js` | Cancel-safe 8-station Director's Cut state machine, WebAudio room atmosphere, live HTTP 206 vs. recording-mode Blob media loader, Evidence/Inspector/Vow modals, and Spatial.io `.glb` export. |
| `media/narration/voices/` | Human & studio narrator profiles tracked in Git (`mostafa_en` **[Default EN]**, `leila_en`, `ali_en`, `mostafa_fa` **[Default FA]**, `leila_fa`) + `manifest.json`. |
| `media/walkthrough_interludes/` | 6 mastered between-narration Cinema Witness Interlude `.mp4` reels (loudness-normalized diegetic audio, watermarks removed, social-media music stripped where needed). |
| `media/walkthrough_pip/` | 23 muted 720p/1080p `.mp4` reels + posters mounted directly onto the 3D classroom/courtyard walls (`IN_WORLD_SCREEN_SPECS`). |
| `media-data.js` & `multimedia.html` | Master catalog for investigative documentaries + the 36 anonymized `eyewitness` school/aftermath clips (`media/raw_eyewitness/`). |

---

## 3. Five-Act Dramatic Flow (8 Stations + 6 Cinema Interludes)

1. **Prologue (`5.2s`):** Aerial descent into the sunlit pre-strike courtyard behind the opening dedication card.
2. **Station 1 (`courtyard_lines`) → Interlude 1 (`11.4s`, with sound):** Yellow morning assembly lines & final morning football match → *12 boys in royal-blue uniforms singing aloud under the red rose arches*.
3. **Station 2 (`boys_flower_arch`) → Interlude 2 (`11.2s`, raw voice):** Ground-floor ceremony room & colorful ball-pit playroom → *Young Mahan's Mother's Day message ("I love you, my beautiful mother — from your son, Mahan")*.
4. **Station 3 (`boys_classroom`) → Interlude 3 (`15.5s`, raw classroom audio):** Sky-blue boys' classroom → *Unedited childhood laughter of boys playing at their green desks*.
5. **Station 4 (`rainbow_staircase`) → Station 5 (`girls_upper_hall`):** Rainbow central stairs & intact flower-decorated classroom doors ascending directly to the upstairs girls' hall (*"only 4 survived"* group photo).
6. **Interlude 4 — The Hinge (`23.2s`):** *First-grade teacher's final photos sent to mothers minutes before impact → `2.5s` silent black strike card (`FEB 28, 2026 · FIRST STRIKE`) → raw citizen phone video in the dust-choked courtyard ("Mohaddeseh!")*, switching the 3D school behind the curtain to post-strike rubble.
7. **Station 6 (`crater_damage`) → Interlude 5 (`36.0s`, raw field testimony):** 5m crater, mothers atop rubble & `"MY HEART"` backpack → *On-site witness standing before the sheared central staircase + rows of recovered tiny shoes on carpets*.
8. **Station 7 (`second_wave`) → Interlude 6 (`21.5s`, scored with *Melody of Peace*):** 2:30 PM second wave & `MADE IN USA` Tomahawk guidance plates → *Surviving sisters Reyhaneh & Mastaneh, a child's sneaker lifted from concrete, and aerial drone view of 150+ graves*.
9. **Station 8 (`vow_shrine`) → Epilogue (`7.0s`):** Accountability Vow Shrine (*Wall of Eyes* & vigil) → solemn dedication swell → Accountability Vow modal.

---

## 4. Exporting Full 1080p60 / 4K Walkthrough Videos

Prerequisites: `node` (with `playwright` installed), `python3` (`numpy`), and `ffmpeg`.

```bash
# Install Playwright locally if not already installed:
npm install --no-save playwright && npx playwright install chromium

# Render both English (Mostafa default) and Farsi (Mostafa default) Director's Cut MP4s:
bash PFP_Platform/web/tools/walkthrough/render_directors_cut.sh

# Or render a specific language + narrator profile:
bash PFP_Platform/web/tools/walkthrough/render_directors_cut.sh en mostafa_en
bash PFP_Platform/web/tools/walkthrough/render_directors_cut.sh en leila_en
bash PFP_Platform/web/tools/walkthrough/render_directors_cut.sh fa mostafa_fa
```

How sync works: `reconstruction.js` emits exact `performance.now()` markers (`prologue_start`, `station_voice_start`, `interlude_start`, `epilogue_start`) into `window.__tourEvents`. `build_audio.py` reads the `.timeline.json` log and synthesizes a sample-accurate 44.1 kHz stereo WAV with automatic ambient-score ducking (`0.015`) during Cinema Interludes, then `ffmpeg` muxes H.264 (`yuv420p`, `+faststart`) + 192 kbps stereo AAC.

---

## 5. High-Impact Polish Opportunities Ahead of Nov 20 HXRC Screening

- **Three.js Lighting, Shadows & Post-Processing:** Upgrade pre-strike sunlit warmth (Stations 1–5: soft ambient occlusion, warm directional sunlight shafts, subtle dust motes) vs. post-strike atmosphere (Stations 6–7: cooler desaturated grade, volumetric haze over the crater).
- **Camera Spline Interpolation:** Smooth `GUIDED_TOUR_STOPS[i].waypoints` with Catmull-Rom / cubic easing and subtle handheld breathing so camera turns between Screen A and Screen B feel like a cinema dolly.
- **4K60 HXRC Projection Master:** Bump `viewport` & `recordVideo.size` in `record_tour.mjs` to `2560x1440` or `3840x2160` on a dedicated GPU machine for the main HXRC auditorium screen.
- **Studio Voice Drop-In:** Whenever updated `.mp3` studio takes arrive, drop them into `media/narration/voices/<profile>/`, update durations in `voices/manifest.json`, and re-run `render_directors_cut.sh`.
