#!/usr/bin/env bash
# End-to-end 1080p Director's Cut renderer (repo-relative).
# Usage:
#   bash PFP_Platform/web/tools/walkthrough/render_directors_cut.sh           # renders both en & fa (Mostafa default)
#   bash PFP_Platform/web/tools/walkthrough/render_directors_cut.sh en        # renders English only
#   bash PFP_Platform/web/tools/walkthrough/render_directors_cut.sh en leila_en
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
PUB="$REPO_ROOT/PFP_Platform/web/public"
REC="${PFP_OUT_DIR:-$REPO_ROOT/scratch/walkthrough_recordings}"
PORT="${PFP_PORT:-8123}"

mkdir -p "$REC"

if ! curl -s -o /dev/null "http://localhost:${PORT}/reconstruction.html"; then
  echo "[server] Starting local HTTP server on :${PORT}..."
  (cd "$PUB" && nohup python3 -m http.server "$PORT" >/tmp/pfp_http.log 2>&1 &)
  sleep 2
fi

render_one() {
  local lang="$1"
  local voice="${2:-}"
  local suffix="${lang}${voice:+_$voice}"
  local name="pfp_walkthrough_directors_cut_${suffix}"
  echo "============================================================"
  echo "[$(date '+%H:%M:%S')] Recording Director's Cut: lang=$lang voice=${voice:-default} -> $name"
  echo "============================================================"

  PFP_PORT="$PORT" PFP_OUT_DIR="$REC" node "$SCRIPT_DIR/record_tour.mjs" "$lang" "$name" -1 "$voice"

  local webm="$REC/${name}.webm"
  local tl="$REC/${name}.timeline.json"
  local wav="$REC/${name}.wav"
  local trim_txt="$REC/${name}.trim.txt"
  local mp4="$REC/${name}.mp4"

  python3 "$SCRIPT_DIR/build_audio.py" "$tl" "$lang" "$webm" "$wav" "$trim_txt"
  local trim_s
  trim_s="$(cat "$trim_txt")"

  echo "[$(date '+%H:%M:%S')] Encoding 1080p H.264 + stereo AAC MP4 (trim_start=${trim_s}s)..."
  ffmpeg -y -v error \
    -ss "$trim_s" -i "$webm" \
    -i "$wav" \
    -map 0:v:0 -map 1:a:0 \
    -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p \
    -c:a aac -b:a 192k -ac 2 \
    -movflags +faststart -shortest \
    "$mp4"

  rm -f "$webm" "$wav" "$trim_txt"
  echo "[$(date '+%H:%M:%S')] FINISHED $mp4"
  ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height,channels -of default=noprint_wrappers=1 "$mp4"
}

if [ "${1:-all}" = "all" ]; then
  render_one en "${2:-}"
  render_one fa "${2:-}"
else
  render_one "$1" "${2:-}"
fi
