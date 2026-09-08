#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)"
JOB="render_jobs/statistics10_class4_percentile_rank_v3_20260908"
SOURCE="$JOB/statistics10_class4_percentile_rank_v3.py"
SCENE="Statistics10Class4PercentileRankV3"
OUT="Statistics10_Class4_Percentile_Rank_V3_SENIOR_FINAL_pqh.mp4"
IMAGE="manimcommunity/manim:v0.20.1"
USER_ARGS=(--user "$(id -u):$(id -g)" -e HOME=/tmp/manim-home)

rm -rf "$JOB/pql_media" "$JOB/final_media" "$JOB/delivery" "$JOB/qa_frames"
mkdir -p "$JOB/pql_media" "$JOB/final_media" "$JOB/delivery" "$JOB/qa_frames"

# -----------------------------------------------------------------------------
# 1. Syntax + deterministic mathematical QA.
# -----------------------------------------------------------------------------
docker run --rm "${USER_ARGS[@]}" \
  -v "$ROOT:/manim" -w /manim --entrypoint bash "$IMAGE" -c "
    set -euo pipefail
    python -m py_compile '$SOURCE'
    python - <<'PY'
import importlib.util
p='render_jobs/statistics10_class4_percentile_rank_v3_20260908/statistics10_class4_percentile_rank_v3.py'
s=importlib.util.spec_from_file_location('class4v3',p)
m=importlib.util.module_from_spec(s)
s.loader.exec_module(m)
m.validate_all_data()
print('Syntax + mathematical assertions: PASS')
PY
  "

grep -Fq 'SAME FAMILY, OPPOSITE QUESTION' "$SOURCE"
grep -Fq 'FORMAL DEFINITION — PERCENTILE RANK' "$SOURCE"
grep -Fq 'FULL WORKED EXAMPLE — PR(72)' "$SOURCE"
grep -Fq 'PERCENTILE VALUE VS PERCENTILE RANK' "$SOURCE"
grep -Fq 'SAME SCORE, DIFFERENT POSITION' "$SOURCE"
grep -Fq 'TIES MATTER' "$SOURCE"
grep -Fq 'RANK LADDER' "$SOURCE"
grep -Fq 'MISCONCEPTION CLINIC' "$SOURCE"
grep -Fq 'GUIDED CHALLENGE — YOUR TURN' "$SOURCE"
grep -Fq 'FINAL MAP' "$SOURCE"
printf 'Content guards: PASS\n' | tee "$JOB/delivery/SOURCE_QA.txt"

# -----------------------------------------------------------------------------
# 2. Mandatory low-quality full-timeline gate.
#    JP_PREVIEW makes the source itself render 854x480 @ 15 fps.
# -----------------------------------------------------------------------------
docker run --rm "${USER_ARGS[@]}" \
  -e JP_PREVIEW=1 -e LESSON_TIME_SCALE=0.18 \
  -v "$ROOT:/manim" -w /manim --entrypoint bash "$IMAGE" -c "
    set -euo pipefail
    mkdir -p /tmp/bin
    printf '#!/usr/bin/env bash\nexit 0\n' > /tmp/bin/xdg-open
    chmod +x /tmp/bin/xdg-open
    export PATH=/tmp/bin:\$PATH
    manim -pql '$SOURCE' '$SCENE' --media_dir '$JOB/pql_media' --format=mp4 --disable_caching
  "

PQL="$(find "$JOB/pql_media" -type f -name "$SCENE.mp4" | sort | tail -n 1)"
test -n "$PQL" && test -s "$PQL"
PW="$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$PQL")"
PH="$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$PQL")"
PF="$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 "$PQL")"
PD="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$PQL")"
test "$PW" = "854"
test "$PH" = "480"
test "$PF" = "15/1"
printf 'PQL gate: PASS\nPreview: %sx%s @ %s\nPreview duration: %s s\n' "$PW" "$PH" "$PF" "$PD" | tee "$JOB/delivery/PQL_QA.txt"
rm -rf "$JOB/pql_media"

# -----------------------------------------------------------------------------
# 3. Literal final -pqh render, Full HD @ 30 fps.
# -----------------------------------------------------------------------------
docker run --rm "${USER_ARGS[@]}" \
  -e JP_PREVIEW=0 -e LESSON_TIME_SCALE=1.0 \
  -v "$ROOT:/manim" -w /manim --entrypoint bash "$IMAGE" -c "
    set -euo pipefail
    mkdir -p /tmp/bin
    printf '#!/usr/bin/env bash\nexit 0\n' > /tmp/bin/xdg-open
    chmod +x /tmp/bin/xdg-open
    export PATH=/tmp/bin:\$PATH
    manim -pqh '$SOURCE' '$SCENE' --media_dir '$JOB/final_media' --format=mp4 --disable_caching
  "

FINAL="$(find "$JOB/final_media" -type f -name "$SCENE.mp4" | sort | tail -n 1)"
test -n "$FINAL" && test -s "$FINAL"
cp "$FINAL" "$JOB/delivery/$OUT"

# -----------------------------------------------------------------------------
# 4. Technical acceptance + full decode.
# -----------------------------------------------------------------------------
ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt \
  -of default=noprint_wrappers=1 "$JOB/delivery/$OUT" | tee "$JOB/delivery/ffprobe.txt"
grep -q '^codec_name=h264$' "$JOB/delivery/ffprobe.txt"
grep -q '^width=1920$' "$JOB/delivery/ffprobe.txt"
grep -q '^height=1080$' "$JOB/delivery/ffprobe.txt"
grep -q '^r_frame_rate=30/1$' "$JOB/delivery/ffprobe.txt"
grep -q '^pix_fmt=yuv420p$' "$JOB/delivery/ffprobe.txt"
ffmpeg -nostdin -v error -i "$JOB/delivery/$OUT" -f null -
printf 'Full decode: PASS\n' | tee "$JOB/delivery/DECODE_QA.txt"

DURATION="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$JOB/delivery/$OUT")"
SIZE="$(stat -c%s "$JOB/delivery/$OUT")"
python - <<PY
D=float('$DURATION')
assert 110 <= D <= 360, f'Unexpected lesson duration: {D:.2f}s'
print(f'Duration gate: PASS ({D:.2f}s)')
PY
printf 'Final duration: %s s\nFinal bytes: %s\n' "$DURATION" "$SIZE" | tee "$JOB/delivery/VIDEO_QA.txt"

# -----------------------------------------------------------------------------
# 5. Visual QA evidence: distributed frames + one contact sheet.
# -----------------------------------------------------------------------------
INTERVAL="$(python -c "d=float('$DURATION'); print(max(4.0,d/30.0))")"
ffmpeg -nostdin -v error -i "$JOB/delivery/$OUT" \
  -vf "fps=1/$INTERVAL,scale=640:-2" "$JOB/qa_frames/frame_%03d.png"
COUNT="$(find "$JOB/qa_frames" -type f -name 'frame_*.png' | wc -l)"
test "$COUNT" -ge 25

python - <<'PY'
from pathlib import Path
try:
    from PIL import Image, ImageDraw
except Exception as exc:
    raise SystemExit(f'Pillow required for contact sheet: {exc}')
root=Path('render_jobs/statistics10_class4_percentile_rank_v3_20260908')
paths=sorted((root/'qa_frames').glob('frame_*.png'))[:30]
ims=[]
for i,p in enumerate(paths,1):
    im=Image.open(p).convert('RGB')
    canvas=Image.new('RGB',(im.width,im.height+24),'white')
    canvas.paste(im,(0,24))
    ImageDraw.Draw(canvas).text((8,5),f'QA {i:02d}',fill='black')
    ims.append(canvas)
cols=5
w=max(im.width for im in ims); h=max(im.height for im in ims)
rows=(len(ims)+cols-1)//cols
sheet=Image.new('RGB',(cols*w,rows*h),'white')
for i,im in enumerate(ims):
    sheet.paste(im,((i%cols)*w,(i//cols)*h))
sheet.save(root/'delivery/QA_contact_sheet.jpg',quality=90)
PY

# -----------------------------------------------------------------------------
# 6. Reproducibility package.
# -----------------------------------------------------------------------------
cp "$SOURCE" "$JOB/delivery/statistics10_class4_percentile_rank_v3.py"
sha256sum "$JOB/delivery/$OUT" "$JOB/delivery/statistics10_class4_percentile_rank_v3.py" | tee "$JOB/delivery/SHA256SUMS.txt"
cat > "$JOB/delivery/RENDER_REPORT.txt" <<EOF
Statistics 10 · Class 4 · Percentile Rank V3
Scene: $SCENE
ManimCE: 0.20.1
Final command: manim -pqh $SOURCE $SCENE --format=mp4 --disable_caching
Resolution: 1920x1080
FPS: 30
Duration: $DURATION s
PQL gate: PASS
PQH render: PASS
ffprobe acceptance: PASS
Full decode: PASS
Distributed visual QA frames: $COUNT
EOF

printf 'CLASS 4 V3 PIPELINE: PASS\n'