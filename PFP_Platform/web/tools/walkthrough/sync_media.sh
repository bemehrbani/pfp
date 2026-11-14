#!/usr/bin/env bash
# Downloads large gitignored media assets (ambient score, 3D wall reels, Cinema Interludes)
# directly from staging.peopleforpeace.live into PFP_Platform/web/public/media/ for local dev & rendering.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
PUB="$REPO_ROOT/PFP_Platform/web/public"
ORIGIN_URL="${PFP_MEDIA_ORIGIN:-https://staging.peopleforpeace.live}"

mkdir -p \
  "$PUB/media/audio" \
  "$PUB/media/walkthrough_interludes/posters" \
  "$PUB/media/walkthrough_pip/posters"

fetch_asset() {
  local rel="$1"
  local dst="$PUB/$rel"
  if [ -s "$dst" ]; then
    return 0
  fi
  mkdir -p "$(dirname "$dst")"
  echo "  ↓ $rel"
  curl -fsSL "$ORIGIN_URL/${rel// /%20}" -o "$dst"
}

echo "Syncing walkthrough audio & video assets from $ORIGIN_URL ..."
fetch_asset "media/audio/memorial_ambient_loop.mp3"
fetch_asset "media/audio/Whistle MOP.ogg"
fetch_asset "media/walkthrough_pip/manifest.json"

for clip in \
  01_sync_morning_queue 01_sync_porch_still \
  02_sync_playroom_memories 02_sync_rose_arch_photo \
  03_sync_boys_carpet_clapping 03_sync_faces_and_drawings \
  04_sync_stairs_welcome 04_sync_stairwell_collapse \
  05_sync_80_girls_hall 05_sync_desks_and_notebooks \
  06_sync_crater_comparison 06_sync_mothers_bags_and_drawings \
  07_sync_barehands_rescue 07_sync_tomahawk_then_smoke \
  08_sync_echo_of_rooms 08_sync_justice_vow \
  01_courtyard_lines_01 01_courtyard_lines_02 01_courtyard_football_and_flags \
  02_boys_flower_arch_01 02_boys_flower_arch_02 02_boys_playroom_prestrike \
  03_boys_classroom_01 03_boys_classroom_02 03_boys_fieldtrip_and_class \
  04_rainbow_staircase_01 04_rainbow_staircase_02 04_intact_doors_and_gate \
  05_girls_upper_hall_01 05_girls_upper_hall_02 05_pink_room_only_four_survived \
  06_crater_damage_01 06_crater_damage_02 06_mothers_rubble_and_backpack \
  07_second_wave_01 07_second_wave_02 \
  08_vow_shrine_01 08_vow_shrine_02 08_eyes_and_justice_vigil; do
  fetch_asset "media/walkthrough_pip/${clip}.mp4"
  fetch_asset "media/walkthrough_pip/posters/${clip}.jpg" || true
done

for il in \
  interlude_02_rose_arch_and_mahan \
  interlude_01_rose_arch_singing \
  interlude_02_mahan_mothers_day \
  interlude_03_boys_classroom_laughter \
  interlude_04_the_hinge_1045am \
  interlude_05_staircase_witness_and_shoes \
  interlude_06_survivors_and_150_graves; do
  fetch_asset "media/walkthrough_interludes/${il}.mp4"
  fetch_asset "media/walkthrough_interludes/posters/${il}.jpg" || true
done

echo "✅ All 3D walkthrough media assets synced to $PUB/media/"
