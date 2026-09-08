#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)"
JOB="render_jobs/statistics10_class4_percentile_rank_decisions_20260908_v2"
BASE_JOB="render_jobs/statistics10_class4_percentile_rank_decisions_20260904"
SOURCE="$JOB/statistics10_class4_percentile_rank_v2.py"
SCENE="Statistics10Class4PercentileRankV2"
OUT="Statistics10_Class4_Percentile_Rank_Decisions_V2_FINAL_pqh.mp4"
MANIM_IMAGE="manimcommunity/manim:v0.20.1"
DOCKER_USER_ARGS=(--user "$(id -u):$(id -g)" -e HOME=/tmp/manim-home)

mkdir -p "$JOB/delivery" "$JOB/qa" library media
rm -f "$JOB/qa"/* || true

# Reconstruct the shared JP classroom style used by the validated V1 branch.
printf '' > library/__init__.py
base64 -d render_jobs/statistics10_p3w2_iqr_boxplot_20260824/payload/jp_classroom_style.py.gz.b64 | gzip -dc > library/jp_classroom_style.py

sha256sum "$BASE_JOB/statistics10_class4_percentile_rank.py" "$SOURCE" library/jp_classroom_style.py \
  | tee "$JOB/delivery/source_sha256.txt"

# 1. Syntax, inherited numerical assertions, and V2 contract checks.
docker run --rm "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint bash "$MANIM_IMAGE" -c '
  set -euo pipefail
  export PYTHONPATH="/manim:${PYTHONPATH:-}"
  python -m py_compile library/jp_classroom_style.py
  python -m py_compile render_jobs/statistics10_class4_percentile_rank_decisions_20260904/statistics10_class4_percentile_rank.py
  python -m py_compile render_jobs/statistics10_class4_percentile_rank_decisions_20260908_v2/statistics10_class4_percentile_rank_v2.py
  python - <<"PY"
import sys
sys.path.insert(0, "render_jobs/statistics10_class4_percentile_rank_decisions_20260904")
import statistics10_class4_percentile_rank as base
base.validate_all_data()
print("Inherited mathematical assertions: PASS")
PY
'

grep -Fq 'class Statistics10Class4PercentileRankV2' "$SOURCE"
grep -Fq 'Ties at x are included' "$SOURCE"
grep -Fq 'PR}(x)\ge 80' "$SOURCE"
grep -Fq 'normal distribution' "$SOURCE"

# Guard against the overlap wording/layout pattern identified in the uploaded V1 render.
if grep -Fq 'These are different questions.' "$SOURCE"; then
  echo 'Old low-position overlap-prone Scene 01 message found in V2.' >&2
  exit 1
fi

# 2. Literal PQL full-timeline preview gate with compressed classroom timing.
rm -rf media/videos/statistics10_class4_percentile_rank_v2 || true
docker run --rm "${DOCKER_USER_ARGS[@]}" -e LESSON_TIME_SCALE=0.16 -v "$ROOT:/manim" -w /manim --entrypoint bash "$MANIM_IMAGE" -c '
  set -euo pipefail
  mkdir -p /tmp/bin
  printf "#!/usr/bin/env bash\nexit 0\n" > /tmp/bin/xdg-open
  chmod +x /tmp/bin/xdg-open
  export PATH="/tmp/bin:$PATH"
  export PYTHONPATH="/manim:${PYTHONPATH:-}"
  manim -pql render_jobs/statistics10_class4_percentile_rank_decisions_20260908_v2/statistics10_class4_percentile_rank_v2.py Statistics10Class4PercentileRankV2 --format=mp4 --disable_caching
'
PQL_MP4="$(find media/videos -type f -path '*480p*' -name "${SCENE}.mp4" | sort | tail -n 1)"
test -n "$PQL_MP4" && test -s "$PQL_MP4"
printf 'PQL full-timeline gate: PASS\n' | tee "$JOB/delivery/PQL_QA.txt"

# 3. Final Full-HD 30-fps render. Retain real thinking pauses without the excessive V1 timing scale.
rm -rf media/videos/statistics10_class4_percentile_rank_v2/1080p* || true
docker run --rm "${DOCKER_USER_ARGS[@]}" -e LESSON_TIME_SCALE=1.35 -v "$ROOT:/manim" -w /manim --entrypoint bash "$MANIM_IMAGE" -c '
  set -euo pipefail
  mkdir -p /tmp/bin
  printf "#!/usr/bin/env bash\nexit 0\n" > /tmp/bin/xdg-open
  chmod +x /tmp/bin/xdg-open
  export PATH="/tmp/bin:$PATH"
  export PYTHONPATH="/manim:${PYTHONPATH:-}"
  manim -pqh render_jobs/statistics10_class4_percentile_rank_decisions_20260908_v2/statistics10_class4_percentile_rank_v2.py Statistics10Class4PercentileRankV2 --fps 30 --format=mp4 --disable_caching
'
FINAL_MP4="$(find media/videos -type f -path '*1080p*' -name "${SCENE}.mp4" | sort | tail -n 1)"
test -n "$FINAL_MP4" && test -s "$FINAL_MP4"
cp "$FINAL_MP4" "$JOB/delivery/$OUT"

# 4. Technical acceptance + complete decode.
docker run --rm "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint ffprobe "$MANIM_IMAGE" \
  -v error -select_streams v:0 -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt \
  -of default=noprint_wrappers=1 "$JOB/delivery/$OUT" | tee "$JOB/delivery/ffprobe.txt"
grep -q '^codec_name=h264$' "$JOB/delivery/ffprobe.txt"
grep -q '^width=1920$' "$JOB/delivery/ffprobe.txt"
grep -q '^height=1080$' "$JOB/delivery/ffprobe.txt"
grep -q '^r_frame_rate=30/1$' "$JOB/delivery/ffprobe.txt"
grep -q '^pix_fmt=yuv420p$' "$JOB/delivery/ffprobe.txt"

docker run --rm "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint ffmpeg "$MANIM_IMAGE" \
  -nostdin -v error -i "$JOB/delivery/$OUT" -f null -
printf 'Full FFmpeg decode: PASS\n' | tee "$JOB/delivery/DECODE_QA.txt"

# 5. Duration gate and dense visual audit contact sheet.
DURATION="$(docker run --rm "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint ffprobe "$MANIM_IMAGE" \
  -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$JOB/delivery/$OUT")"
python - "$DURATION" <<'PY'
import sys
d=float(sys.argv[1])
assert 280 <= d <= 470, f"Unexpected V2 duration: {d:.2f}s"
print(f"Duration gate: PASS ({d:.2f}s)")
PY
printf 'duration_seconds=%s\n' "$DURATION" > "$JOB/delivery/duration.txt"

docker run --rm "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint ffmpeg "$MANIM_IMAGE" \
  -nostdin -y -v error -i "$JOB/delivery/$OUT" \
  -vf "fps=1/12,scale=480:-2,tile=4x9:padding=4:margin=4" -frames:v 1 "$JOB/qa/QA_contact_sheet.jpg"
test -s "$JOB/qa/QA_contact_sheet.jpg"
cp "$JOB/qa/QA_contact_sheet.jpg" "$JOB/delivery/QA_contact_sheet.jpg"

# 6. Final hashes and summary.
sha256sum "$JOB/delivery/$OUT" "$JOB/delivery/QA_contact_sheet.jpg" "$SOURCE" \
  | tee "$JOB/delivery/SHA256SUMS.txt"
cat > "$JOB/delivery/RENDER_SUMMARY.txt" <<EOF
Statistics 10 · Class 4 · Percentile Rank Decisions · V2 QA
Scene: $SCENE
ManimCE: 0.20.1
Output: $OUT
Duration: $DURATION s
Video: H.264 / 1920x1080 / 30 fps / yuv420p
Math assertions: PASS
PQL full-timeline gate: PASS
PQH render: PASS
Full FFmpeg decode: PASS
Dense contact-sheet audit generated: PASS
V2 focus: overlap removal, convention clarity, top-20% decision rule, curriculum bridge.
EOF
