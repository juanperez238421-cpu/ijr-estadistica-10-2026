#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)"
JOB="render_jobs/statistics10_class4_percentile_rank_decisions_20260904"
SCENE_NAME="Statistics10Class4PercentileRank"
OUT_NAME="Statistics10_Class4_Percentile_Rank_Decisions_FINAL_pqh.mp4"
SOURCE="$JOB/statistics10_class4_percentile_rank.py"
MANIM_IMAGE="manimcommunity/manim:v0.20.1"
DOCKER_USER_ARGS=(--user "$(id -u):$(id -g)" -e HOME=/tmp/manim-home)

mkdir -p "$JOB/build" "$JOB/delivery" "$JOB/qa_frames" "$JOB/qa_dense" library media
rm -f "$JOB/qa_frames"/*.png "$JOB/qa_dense"/*.png
cp "$SOURCE" "$JOB/build/scene.py"
printf '' > library/__init__.py
base64 -d render_jobs/statistics10_p3w2_iqr_boxplot_20260824/payload/jp_classroom_style.py.gz.b64 | gzip -dc > library/jp_classroom_style.py
sha256sum "$JOB/build/scene.py" library/jp_classroom_style.py | tee "$JOB/delivery/source_sha256.txt"

# 1) Syntax + architecture + deterministic mathematical QA.
docker run --rm "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint bash "$MANIM_IMAGE" -c '
  set -euo pipefail
  export PYTHONPATH="/manim:${PYTHONPATH:-}"
  python -m py_compile library/jp_classroom_style.py
  python -m py_compile render_jobs/statistics10_class4_percentile_rank_decisions_20260904/build/scene.py
  python -c "import sys; sys.path.insert(0, \"render_jobs/statistics10_class4_percentile_rank_decisions_20260904/build\"); import scene; scene.validate_all_data(); print(\"Mathematical assertions: PASS\")"
'
grep -Fq 'class Statistics10Class4PercentileRank' "$JOB/build/scene.py"
grep -Fq 'SIX STEPS FOR PERCENTILE RANK' "$JOB/build/scene.py"
grep -Fq 'WORKED EXAMPLE A — FIND PR(72)' "$JOB/build/scene.py"
grep -Fq 'SAME DATASET — DIFFERENT RELATIVE POSITIONS' "$JOB/build/scene.py"
grep -Fq 'USE RELATIVE POSITION TO MAKE A DECISION' "$JOB/build/scene.py"
grep -Fq 'DO NOT CONFUSE THESE TWO QUESTIONS' "$JOB/build/scene.py"
grep -Fq 'GUIDED CHALLENGE — YOUR TURN' "$JOB/build/scene.py"
grep -Fq 'FINAL RECIPE — VALUE → POSITION' "$JOB/build/scene.py"
grep -Fq 'Position Measures + Boxplot Comparisons' "$JOB/build/scene.py"
if grep -Eqi 'z-score|z score|standard normal|empirical rule|normal distribution|pandas|google colab' "$JOB/build/scene.py"; then
  echo 'Out-of-scope future/programming content found in Class 4 source.' >&2
  exit 1
fi

# 2) Literal full-timeline PQL gate, compressed only for CI preview speed.
rm -rf media/videos/scene/480p15
docker run --rm "${DOCKER_USER_ARGS[@]}" -e LESSON_TIME_SCALE=0.18 -v "$ROOT:/manim" -w /manim --entrypoint bash "$MANIM_IMAGE" -c '
  set -euo pipefail
  mkdir -p /tmp/bin
  printf "#!/usr/bin/env bash\nexit 0\n" > /tmp/bin/xdg-open
  chmod +x /tmp/bin/xdg-open
  export PATH="/tmp/bin:$PATH"
  export PYTHONPATH="/manim:${PYTHONPATH:-}"
  manim -pql render_jobs/statistics10_class4_percentile_rank_decisions_20260904/build/scene.py Statistics10Class4PercentileRank --format=mp4 --disable_caching
'
PQL_MP4="$(find media/videos -type f -path '*480p*' -name "${SCENE_NAME}.mp4" | sort | tail -n 1)"
test -n "$PQL_MP4" && test -s "$PQL_MP4"
printf 'PQL full-timeline gate: PASS\n' | tee "$JOB/delivery/PQL_QA.txt"

# 3) Literal PQH final render. The lesson scale is intentionally >1 to preserve the requested classroom pauses.
rm -rf media/videos/scene/1080p60 media/videos/scene/1080p30
docker run --rm "${DOCKER_USER_ARGS[@]}" -e LESSON_TIME_SCALE=1.60 -v "$ROOT:/manim" -w /manim --entrypoint bash "$MANIM_IMAGE" -c '
  set -euo pipefail
  mkdir -p /tmp/bin
  printf "#!/usr/bin/env bash\nexit 0\n" > /tmp/bin/xdg-open
  chmod +x /tmp/bin/xdg-open
  export PATH="/tmp/bin:$PATH"
  export PYTHONPATH="/manim:${PYTHONPATH:-}"
  manim -pqh render_jobs/statistics10_class4_percentile_rank_decisions_20260904/build/scene.py Statistics10Class4PercentileRank --fps 30 --format=mp4 --disable_caching
'
FINAL_MP4="$(find media/videos -type f -path '*1080p*' -name "${SCENE_NAME}.mp4" | sort | tail -n 1)"
test -n "$FINAL_MP4" && test -s "$FINAL_MP4"
cp "$FINAL_MP4" "$JOB/delivery/$OUT_NAME"

# 4) Technical acceptance: H.264, Full HD, 30 fps, yuv420p, complete decode.
docker run --rm "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint ffprobe "$MANIM_IMAGE" \
  -v error -select_streams v:0 -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt \
  -of default=noprint_wrappers=1 "$JOB/delivery/$OUT_NAME" | tee "$JOB/delivery/ffprobe.txt"
grep -q '^codec_name=h264$' "$JOB/delivery/ffprobe.txt"
grep -q '^width=1920$' "$JOB/delivery/ffprobe.txt"
grep -q '^height=1080$' "$JOB/delivery/ffprobe.txt"
grep -q '^r_frame_rate=30/1$' "$JOB/delivery/ffprobe.txt"
grep -q '^pix_fmt=yuv420p$' "$JOB/delivery/ffprobe.txt"
docker run --rm "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint ffmpeg "$MANIM_IMAGE" -nostdin -v error -i "$JOB/delivery/$OUT_NAME" -f null -
printf 'Full FFmpeg decode: PASS\n' | tee "$JOB/delivery/DECODE_QA.txt"

# 5) Runtime and dense QA-frame extraction.
DURATION="$(docker run --rm "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint ffprobe "$MANIM_IMAGE" -v error -show_entries format=duration -of default=nk=1:nw=1 "$JOB/delivery/$OUT_NAME")"
FILE_SIZE="$(stat -c%s "$JOB/delivery/$OUT_NAME")"
python -c "d=float('$DURATION'); assert 330 <= d <= 510, f'Class duration outside 6–8 min target tolerance: {d:.2f}s'"
INTERVAL="$(python -c "d=float('$DURATION'); print(max(d/60.0, 0.5))")"

docker run --rm "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint ffmpeg "$MANIM_IMAGE" -nostdin -v error -i "$JOB/delivery/$OUT_NAME" -vf "fps=1/$INTERVAL,scale=480:-2" "$JOB/qa_frames/frame_%03d.png"
docker run --rm "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint ffmpeg "$MANIM_IMAGE" -nostdin -v error -i "$JOB/delivery/$OUT_NAME" -vf "fps=1/5,scale=640:-2" "$JOB/qa_dense/dense_%03d.png"
DISTRIBUTED_COUNT="$(find "$JOB/qa_frames" -type f -name 'frame_*.png' | wc -l)"
DENSE_COUNT="$(find "$JOB/qa_dense" -type f -name 'dense_*.png' | wc -l)"
test "$DISTRIBUTED_COUNT" -ge 55
test "$DENSE_COUNT" -ge 60

# 6) 60-frame contact sheet for visual QA.
docker run --rm "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint python "$MANIM_IMAGE" -c '
from pathlib import Path
from PIL import Image, ImageDraw
folder=Path("render_jobs/statistics10_class4_percentile_rank_decisions_20260904/qa_frames")
paths=sorted(folder.glob("frame_*.png"))[:60]
if len(paths) < 55: raise SystemExit(f"Insufficient QA frames: {len(paths)}")
ims=[]
for i,p in enumerate(paths,1):
    im=Image.open(p).convert("RGB")
    canvas=Image.new("RGB", (im.width, im.height+24), "white")
    canvas.paste(im, (0,24)); ImageDraw.Draw(canvas).text((8,5), f"audit {i:02d}", fill="black"); ims.append(canvas)
w=max(im.width for im in ims); h=max(im.height for im in ims); cols=5; rows=(len(ims)+cols-1)//cols
sheet=Image.new("RGB", (cols*w, rows*h), "white")
for i,im in enumerate(ims): sheet.paste(im, ((i%cols)*w, (i//cols)*h))
sheet.save("render_jobs/statistics10_class4_percentile_rank_decisions_20260904/delivery/QA_contact_sheet.jpg", quality=92)
'

# 7) Canonical delivery package and traceability.
cp "$JOB/build/scene.py" "$JOB/delivery/statistics10_class4_percentile_rank.py"
cp "$JOB/README.md" "$JOB/delivery/README.md"
cp library/jp_classroom_style.py "$JOB/delivery/jp_classroom_style.py"
sha256sum "$JOB/delivery/$OUT_NAME" | tee "$JOB/delivery/SHA256SUMS.txt"
SHA256="$(cut -d' ' -f1 "$JOB/delivery/SHA256SUMS.txt")"
{
  printf 'Scene: %s\n' "$SCENE_NAME"
  printf 'ManimCE: 0.20.1\n'
  printf 'Render command: LESSON_TIME_SCALE=1.60 manim -pqh %s/build/scene.py %s --fps 30 --format=mp4 --disable_caching\n' "$JOB" "$SCENE_NAME"
  printf 'Final MP4: %s\n' "$OUT_NAME"
  printf 'Duration seconds: %s\n' "$DURATION"
  printf 'File size bytes: %s\n' "$FILE_SIZE"
  printf 'SHA-256: %s\n' "$SHA256"
  printf 'Distributed audit frames: %s\n' "$DISTRIBUTED_COUNT"
  printf 'Dense 5-second audit frames: %s\n' "$DENSE_COUNT"
  printf 'Mathematical QA: PASS\nPQL full-timeline QA: PASS\nPQH technical QA: PASS\nFull decode: PASS\n'
  printf 'Visual audit deliverable: QA_contact_sheet.jpg + qa_dense/*.png\n'
} | tee "$JOB/delivery/RENDER_SUMMARY.txt"
