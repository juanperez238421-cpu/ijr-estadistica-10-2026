#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)"
JOB="render_jobs/statistics10_class4_percentile_rank_decisions_v2_20260908"
SCENE_NAME="Statistics10Class4PercentileRankV2"
OUT_NAME="Statistics10_Class4_Percentile_Rank_Decisions_V2_SENIOR_FINAL_pqh.mp4"
SOURCE="$JOB/statistics10_class4_percentile_rank_v2.py"
MANIM_IMAGE="manimcommunity/manim:v0.20.1"
DOCKER_USER_ARGS=(--user "$(id -u):$(id -g)" -e HOME=/tmp/manim-home)

mkdir -p "$JOB/build" "$JOB/delivery" "$JOB/qa_frames" "$JOB/qa_dense" "$JOB/qa_targeted" library media
rm -f "$JOB/qa_frames"/*.png "$JOB/qa_dense"/*.png "$JOB/qa_targeted"/*.png
cp "$SOURCE" "$JOB/build/scene.py"
printf '' > library/__init__.py
base64 -d render_jobs/statistics10_p3w2_iqr_boxplot_20260824/payload/jp_classroom_style.py.gz.b64 | gzip -dc > library/jp_classroom_style.py
sha256sum "$JOB/build/scene.py" library/jp_classroom_style.py | tee "$JOB/delivery/source_sha256.txt"

# 1) Syntax, architecture, deterministic mathematical QA, and content guards.
docker run --rm "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint bash "$MANIM_IMAGE" -c '
  set -euo pipefail
  export PYTHONPATH="/manim:${PYTHONPATH:-}"
  python -m py_compile library/jp_classroom_style.py
  python -m py_compile render_jobs/statistics10_class4_percentile_rank_decisions_v2_20260908/build/scene.py
  python -c "import sys; sys.path.insert(0, \"render_jobs/statistics10_class4_percentile_rank_decisions_v2_20260908/build\"); import scene; scene.validate_all_data(); print(\"Mathematical assertions: PASS\")"
'

grep -Fq 'class Statistics10Class4PercentileRankV2' "$JOB/build/scene.py"
grep -Fq 'SAME SCORE, DIFFERENT POSITION' "$JOB/build/scene.py"
grep -Fq 'SEE THE RELATIVE POSITION' "$JOB/build/scene.py"
grep -Fq 'FORMAL DEFINITION' "$JOB/build/scene.py"
grep -Fq 'FULL WORKED EXAMPLE — PR(72)' "$JOB/build/scene.py"
grep -Fq 'COMPARE THREE POSITIONS' "$JOB/build/scene.py"
grep -Fq 'DECISION MAKING — TOP 20%' "$JOB/build/scene.py"
grep -Fq 'TIES MATTER' "$JOB/build/scene.py"
grep -Fq 'MISCONCEPTION CLINIC' "$JOB/build/scene.py"
grep -Fq 'PERCENTILE VALUE VS PERCENTILE RANK' "$JOB/build/scene.py"
grep -Fq 'GUIDED CHALLENGE — YOUR TURN' "$JOB/build/scene.py"
grep -Fq 'EXIT TICKET' "$JOB/build/scene.py"
grep -Fq 'FINAL MAP — VALUE → POSITION → DECISION' "$JOB/build/scene.py"
grep -Fq 'INTRODUCTION TO THE NORMAL DISTRIBUTION' "$JOB/build/scene.py"
grep -Fq 'AT OR BELOW' "$JOB/build/scene.py"
if grep -Eqi 'z-score|z score|empirical rule|68-95-99|standard normal|google colab|pandas' "$JOB/build/scene.py"; then
  echo 'Out-of-scope future/programming content found in Class 4 V2 source.' >&2
  exit 1
fi
printf 'Source + content guards: PASS\n' | tee "$JOB/delivery/SOURCE_QA.txt"

# 2) Literal PQL gate with compressed timing only for preview speed.
rm -rf media/videos/scene/480p15
docker run --rm "${DOCKER_USER_ARGS[@]}" -e LESSON_TIME_SCALE=0.16 -v "$ROOT:/manim" -w /manim --entrypoint bash "$MANIM_IMAGE" -c '
  set -euo pipefail
  mkdir -p /tmp/bin
  printf "#!/usr/bin/env bash\nexit 0\n" > /tmp/bin/xdg-open
  chmod +x /tmp/bin/xdg-open
  export PATH="/tmp/bin:$PATH"
  export PYTHONPATH="/manim:${PYTHONPATH:-}"
  manim -pql render_jobs/statistics10_class4_percentile_rank_decisions_v2_20260908/build/scene.py Statistics10Class4PercentileRankV2 --format=mp4 --disable_caching
'
PQL_MP4="$(find media/videos -type f -path '*480p*' -name "${SCENE_NAME}.mp4" | sort | tail -n 1)"
test -n "$PQL_MP4" && test -s "$PQL_MP4"
PQL_DURATION="$(docker run --rm "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint ffprobe "$MANIM_IMAGE" -v error -show_entries format=duration -of default=nk=1:nw=1 "$PQL_MP4")"
printf 'PQL full-timeline gate: PASS\nPQL duration: %s s\n' "$PQL_DURATION" | tee "$JOB/delivery/PQL_QA.txt"

# Compute a final timing scale from the full-timeline PQL duration so the PQH
# stays in the requested 6:30–7:45 classroom window. Target midpoint: 7:00.
FINAL_SCALE="$(python - <<PY
pql=float('$PQL_DURATION')
base=pql/0.16
target=420.0
scale=target/base if base > 0 else 1.0
scale=max(0.78, min(1.35, scale))
print(f'{scale:.5f}')
PY
)"
printf 'Adaptive final LESSON_TIME_SCALE=%s\n' "$FINAL_SCALE" | tee "$JOB/delivery/TIMING_QA.txt"

# 3) Literal PQH final render.
rm -rf media/videos/scene/1080p60 media/videos/scene/1080p30
docker run --rm "${DOCKER_USER_ARGS[@]}" -e LESSON_TIME_SCALE="$FINAL_SCALE" -v "$ROOT:/manim" -w /manim --entrypoint bash "$MANIM_IMAGE" -c '
  set -euo pipefail
  mkdir -p /tmp/bin
  printf "#!/usr/bin/env bash\nexit 0\n" > /tmp/bin/xdg-open
  chmod +x /tmp/bin/xdg-open
  export PATH="/tmp/bin:$PATH"
  export PYTHONPATH="/manim:${PYTHONPATH:-}"
  manim -pqh render_jobs/statistics10_class4_percentile_rank_decisions_v2_20260908/build/scene.py Statistics10Class4PercentileRankV2 --fps 30 --format=mp4 --disable_caching
'
FINAL_MP4="$(find media/videos -type f -path '*1080p*' -name "${SCENE_NAME}.mp4" | sort | tail -n 1)"
test -n "$FINAL_MP4" && test -s "$FINAL_MP4"
cp "$FINAL_MP4" "$JOB/delivery/$OUT_NAME"

# 4) Technical acceptance: H.264, Full HD, 30 fps, yuv420p, full decode.
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

# 5) Duration gate + distributed/dense QA extraction.
DURATION="$(docker run --rm "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint ffprobe "$MANIM_IMAGE" -v error -show_entries format=duration -of default=nk=1:nw=1 "$JOB/delivery/$OUT_NAME")"
FILE_SIZE="$(stat -c%s "$JOB/delivery/$OUT_NAME")"
python - <<PY
D=float('$DURATION')
assert 390 <= D <= 465, f'Class duration outside 6:30–7:45 target: {D:.2f}s'
print(f'Duration gate: PASS ({D:.2f}s)')
PY
INTERVAL="$(python -c "d=float('$DURATION'); print(d/48.0)")"
docker run --rm "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint ffmpeg "$MANIM_IMAGE" -nostdin -v error -i "$JOB/delivery/$OUT_NAME" -vf "fps=1/$INTERVAL,scale=540:-2" "$JOB/qa_frames/frame_%03d.png"
docker run --rm "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint ffmpeg "$MANIM_IMAGE" -nostdin -v error -i "$JOB/delivery/$OUT_NAME" -vf "fps=1/5,scale=640:-2" "$JOB/qa_dense/dense_%03d.png"
DISTRIBUTED_COUNT="$(find "$JOB/qa_frames" -type f -name 'frame_*.png' | wc -l)"
DENSE_COUNT="$(find "$JOB/qa_dense" -type f -name 'dense_*.png' | wc -l)"
test "$DISTRIBUTED_COUNT" -ge 46
test "$DENSE_COUNT" -ge 70

# Extra targeted frames around each cumulative-count sequence.
for spec in '017:cumulative_visual' '035:cumulative_worked' '060:cumulative_ties' '079:cumulative_challenge'; do
  pct="${spec%%:*}"; name="${spec##*:}"
  start="$(python -c "d=float('$DURATION'); p=float('$pct')/100; print(max(0,d*p-7))")"
  docker run --rm "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint ffmpeg "$MANIM_IMAGE" -nostdin -v error \
    -ss "$start" -t 14 -i "$JOB/delivery/$OUT_NAME" -vf "fps=2,scale=640:-2" "$JOB/qa_targeted/${name}_%03d.png"
done

# 6) Build main + targeted contact sheets.
docker run --rm -i "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint python "$MANIM_IMAGE" - <<'PY'
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path('render_jobs/statistics10_class4_percentile_rank_decisions_v2_20260908')

def sheet(paths, out, cols=4, label_prefix='audit'):
    paths=list(paths)
    if not paths:
        raise SystemExit(f'No frames for {out}')
    ims=[]
    for i,p in enumerate(paths,1):
        im=Image.open(p).convert('RGB')
        canvas=Image.new('RGB',(im.width,im.height+24),'white')
        canvas.paste(im,(0,24))
        ImageDraw.Draw(canvas).text((8,5),f'{label_prefix} {i:02d}',fill='black')
        ims.append(canvas)
    w=max(i.width for i in ims); h=max(i.height for i in ims)
    rows=(len(ims)+cols-1)//cols
    outim=Image.new('RGB',(cols*w,rows*h),'white')
    for i,im in enumerate(ims):
        outim.paste(im,((i%cols)*w,(i//cols)*h))
    outim.save(out,quality=92)

frames=sorted((ROOT/'qa_frames').glob('frame_*.png'))[:48]
if len(frames) < 46:
    raise SystemExit(f'Insufficient distributed QA frames: {len(frames)}')
sheet(frames, ROOT/'delivery/QA_contact_sheet.jpg', cols=4)
PY

# Create targeted sheets from time windows using a small reusable shell/Python helper.
make_target_sheet() {
  local fraction="$1"; local window="$2"; local stem="$3"; local prefix="$4"
  local start
  start="$(python -c "d=float('$DURATION'); f=float('$fraction'); w=float('$window'); print(max(0,d*f-w/2))")"
  local tmp="$JOB/qa_targeted/${stem}_frames"
  mkdir -p "$tmp"; rm -f "$tmp"/*.png
  docker run --rm "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint ffmpeg "$MANIM_IMAGE" -nostdin -v error \
    -ss "$start" -t "$window" -i "$JOB/delivery/$OUT_NAME" -vf "fps=1/3,scale=640:-2" "$tmp/f_%03d.png"
  docker run --rm -i "${DOCKER_USER_ARGS[@]}" -v "$ROOT:/manim" -w /manim --entrypoint python "$MANIM_IMAGE" - "$tmp" "$JOB/delivery/${stem}.jpg" "$prefix" <<'PY'
from pathlib import Path
from PIL import Image,ImageDraw
import sys
folder=Path(sys.argv[1]); out=Path(sys.argv[2]); prefix=sys.argv[3]
paths=sorted(folder.glob('f_*.png'))
ims=[]
for i,p in enumerate(paths,1):
    im=Image.open(p).convert('RGB'); c=Image.new('RGB',(im.width,im.height+24),'white'); c.paste(im,(0,24)); ImageDraw.Draw(c).text((8,5),f'{prefix} {i:02d}',fill='black'); ims.append(c)
if not ims: raise SystemExit('No targeted frames')
cols=4; w=max(x.width for x in ims); h=max(x.height for x in ims); rows=(len(ims)+cols-1)//cols
s=Image.new('RGB',(cols*w,rows*h),'white')
for i,im in enumerate(ims): s.paste(im,((i%cols)*w,(i//cols)*h))
s.save(out,quality=92)
PY
}
make_target_sheet 0.46 30 QA_percentile_rank_axis axis
make_target_sheet 0.53 32 QA_top20_decision top20
make_target_sheet 0.71 30 QA_value_vs_rank distinction
make_target_sheet 0.95 34 QA_final_bridge bridge

# 7) Canonical delivery package + traceability.
cp "$JOB/build/scene.py" "$JOB/delivery/statistics10_class4_percentile_rank_v2.py"
cp "$JOB/README.md" "$JOB/delivery/README.md"
cp library/jp_classroom_style.py "$JOB/delivery/jp_classroom_style.py"
sha256sum "$JOB/delivery/$OUT_NAME" | tee "$JOB/delivery/SHA256SUMS.txt"
SHA256="$(cut -d' ' -f1 "$JOB/delivery/SHA256SUMS.txt")"
{
  printf 'Scene: %s\n' "$SCENE_NAME"
  printf 'ManimCE: 0.20.1\n'
  printf 'Render command: LESSON_TIME_SCALE=%s manim -pqh %s/build/scene.py %s --fps 30 --format=mp4 --disable_caching\n' "$FINAL_SCALE" "$JOB" "$SCENE_NAME"
  printf 'Final MP4: %s\n' "$OUT_NAME"
  printf 'Duration seconds: %s\n' "$DURATION"
  printf 'File size bytes: %s\n' "$FILE_SIZE"
  printf 'SHA-256: %s\n' "$SHA256"
  printf 'Distributed audit frames: %s\n' "$DISTRIBUTED_COUNT"
  printf 'Dense 5-second audit frames: %s\n' "$DENSE_COUNT"
  printf 'Mathematical QA: PASS\nSource/content QA: PASS\nPQL full-timeline QA: PASS\nPQH technical QA: PASS\nFull decode: PASS\n'
  printf 'Visual QA evidence: QA_contact_sheet.jpg, QA_percentile_rank_axis.jpg, QA_top20_decision.jpg, QA_value_vs_rank.jpg, QA_final_bridge.jpg, qa_targeted/*.png\n'
} | tee "$JOB/delivery/RENDER_SUMMARY.txt"

cat >> "$JOB/delivery/README.md" <<EOF

## Render verification

- ManimCE: 0.20.1
- Resolution: 1920 × 1080
- FPS: 30
- Codec / pixel format: H.264 / yuv420p
- Duration: ${DURATION} s
- SHA-256: ${SHA256}
- Complete FFmpeg decode: PASS
- Dense distributed visual-QA evidence generated: PASS
- Adaptive classroom timing scale: ${FINAL_SCALE}
EOF
