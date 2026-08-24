#!/usr/bin/env bash
set -euo pipefail
set -o pipefail

JOB="render_jobs/statistics10_p3w2_iqr_boxplot_20260824"
SRC="$JOB/statistics10_p3w2_iqr_boxplot_construction_senior.py"
STORY="$JOB/STORYBOARD.md"
PROTOCOL="protocols/PROTOCOL_MANIMCE_PQH_PROJECT_PACKAGE_STANDARD_v1.1.md"
SCENE="Statistics10Period3Week2IQRBoxPlotConstructionSenior"
EXPECTED_SHA="d2118c1a14a0a2dde9c58536ea130dcc5521d33853829c812a51e4151820f509"

rm -rf qa_runtime delivery
mkdir -p qa_runtime/pql qa_runtime/pqh qa_runtime/audit_frames delivery

echo '[1/7] Reconstruct + validate exact source'
test -s "$STORY" && test -s "$PROTOCOL"
cat "$JOB"/source_parts/part_*.b64 | base64 --decode | gzip -dc > "$SRC"
python -m py_compile "$SRC"
printf '%s  %s\n' "$EXPECTED_SHA" "$SRC" | sha256sum --check --strict
grep -q "^class $SCENE" "$SRC"
sha256sum "$SRC" "$STORY" "$PROTOCOL" > qa_runtime/PRE_RENDER_SHA256.txt

echo '[2/7] Pull ManimCE 0.20.1 + literal PQL'
docker pull manimcommunity/manim:v0.20.1
docker run --rm --user "$(id -u):$(id -g)" \
  -e HOME=/tmp/manim-home -e LESSON_TIME_SCALE=0.10 \
  -v "$PWD:/manim" -w /manim --entrypoint bash \
  manimcommunity/manim:v0.20.1 -c "
    set -euo pipefail
    mkdir -p /tmp/manim-home /tmp/manim-bin
    printf '#!/usr/bin/env bash\\nexit 0\\n' > /tmp/manim-bin/xdg-open
    chmod +x /tmp/manim-bin/xdg-open
    export PATH=\"/tmp/manim-bin:\$PATH\"
    manim -pql '$SRC' '$SCENE' --format=mp4 --disable_caching --media_dir qa_runtime/pql
  " 2>&1 | tee qa_runtime/render_pql.log
PQL="$(find qa_runtime/pql -type f -name "${SCENE}.mp4" -print -quit)"
test -n "$PQL" && test -s "$PQL"
cp "$PQL" qa_runtime/PQL_PREVIEW.mp4

echo '[3/7] Literal PQH final render'
docker run --rm --user "$(id -u):$(id -g)" \
  -e HOME=/tmp/manim-home -e LESSON_TIME_SCALE=1.00 \
  -v "$PWD:/manim" -w /manim --entrypoint bash \
  manimcommunity/manim:v0.20.1 -c "
    set -euo pipefail
    mkdir -p /tmp/manim-home /tmp/manim-bin
    printf '#!/usr/bin/env bash\\nexit 0\\n' > /tmp/manim-bin/xdg-open
    chmod +x /tmp/manim-bin/xdg-open
    export PATH=\"/tmp/manim-bin:\$PATH\"
    manim -pqh '$SRC' '$SCENE' --format=mp4 --disable_caching --media_dir qa_runtime/pqh
  " 2>&1 | tee qa_runtime/render_pqh.log
PQH="$(find qa_runtime/pqh -type f -name "${SCENE}.mp4" -print -quit)"
test -n "$PQH" && test -s "$PQH"
cp "$PQH" qa_runtime/FINAL_SOURCE_RENDER.mp4

echo '[4/7] ffprobe + full decode'
sudo apt-get update -qq
sudo apt-get install -y -qq ffmpeg
V="qa_runtime/FINAL_SOURCE_RENDER.mp4"
codec="$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=nw=1:nk=1 "$V")"
width="$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of default=nw=1:nk=1 "$V")"
height="$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of default=nw=1:nk=1 "$V")"
fps="$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=nw=1:nk=1 "$V")"
pix="$(ffprobe -v error -select_streams v:0 -show_entries stream=pix_fmt -of default=nw=1:nk=1 "$V")"
duration="$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$V")"
size="$(ffprobe -v error -show_entries format=size -of default=nw=1:nk=1 "$V")"
test "$codec" = h264
test "$width" = 1920
test "$height" = 1080
test "$fps" = 30/1
test "$pix" = yuv420p
printf 'field\tvalue\ncodec\t%s\nwidth\t%s\nheight\t%s\nfps\t%s\npix_fmt\t%s\nduration_s\t%s\nsize_bytes\t%s\n' \
  "$codec" "$width" "$height" "$fps" "$pix" "$duration" "$size" > qa_runtime/VIDEO_TECHNICAL.tsv
ffmpeg -v error -i "$V" -f null - 2> qa_runtime/full_decode.log
test ! -s qa_runtime/full_decode.log

echo '[5/7] Dense visual audit frames (JPEG for runner robustness)'
python - "$duration" > qa_runtime/audit_times.txt <<'PY'
import sys
d=float(sys.argv[1]); n=32
a=min(1.0,d*0.01); b=max(a,d-min(1.0,d*0.01))
for i in range(n):
    print(f"{a+(b-a)*i/(n-1):.6f}")
PY
i=0
while IFS= read -r t; do
  printf -v idx '%02d' "$i"
  ffmpeg -y -loglevel error -threads 1 -ss "$t" -i "$V" -frames:v 1 -q:v 2 "qa_runtime/audit_frames/frame_${idx}.jpg"
  i=$((i+1))
done < qa_runtime/audit_times.txt
test "$i" -eq 32
python -m pip install --quiet pillow
python - <<'PY'
from pathlib import Path
from PIL import Image, ImageDraw
fs=sorted(Path('qa_runtime/audit_frames').glob('frame_*.jpg'))
assert len(fs)==32
sheet=Image.new('RGB',(1600,1936),'white')
for i,f in enumerate(fs):
    im=Image.open(f).convert('RGB'); im.thumbnail((384,216))
    tile=Image.new('RGB',(400,242),'white')
    tile.paste(im,((400-im.width)//2,6))
    ImageDraw.Draw(tile).text((8,222),f.stem,fill='black')
    sheet.paste(tile,((i%4)*400,(i//4)*242))
sheet.save('qa_runtime/QA_CONTACT_SHEET.jpg',quality=92)
PY
test -s qa_runtime/QA_CONTACT_SHEET.jpg

echo '[6/7] Canonical project ZIP'
PROJECT="Statistics10_P3W2_IQR_BoxPlot_Construction_Senior_V1_PQH_PACKAGE"
ROOT="delivery/$PROJECT"
FINAL="Statistics10_P3W2_IQR_BoxPlot_Construction_Senior_V1_FINAL_pqh.mp4"
ZIP="Statistics10_P3W2_IQR_BoxPlot_Construction_Senior_V1_FINAL_PQH_PROJECT.zip"
mkdir -p "$ROOT/src" "$ROOT/storyboard" "$ROOT/render" "$ROOT/qa/audit_frames" "$ROOT/protocol" "$ROOT/workflow"
cp "$SRC" "$ROOT/src/"
cp "$STORY" "$ROOT/storyboard/STORYBOARD.md"
cp "$V" "$ROOT/render/$FINAL"
cp qa_runtime/VIDEO_TECHNICAL.tsv qa_runtime/full_decode.log qa_runtime/render_pql.log qa_runtime/render_pqh.log qa_runtime/audit_times.txt qa_runtime/QA_CONTACT_SHEET.jpg "$ROOT/qa/"
cp qa_runtime/audit_frames/*.jpg "$ROOT/qa/audit_frames/"
cp "$PROTOCOL" "$ROOT/protocol/PROTOCOL_MANIMCE_PQH_PROJECT_PACKAGE_STANDARD.md"
cp "$JOB/run_pipeline.sh" "$ROOT/workflow/"
if test -s .github/workflows/render_statistics10_p3w2_iqr_boxplot_push.yml; then
  cp .github/workflows/render_statistics10_p3w2_iqr_boxplot_push.yml "$ROOT/workflow/"
fi
MP4_SHA="$(sha256sum "$ROOT/render/$FINAL" | awk '{print $1}')"
cat > "$ROOT/README.md" <<EOF
# Statistics 10 — Period 3 Week 2 — IQR / Modified Box-Plot Construction

Version: V1 FINAL PQH
ManimCE: 0.20.1
Scene: $SCENE
Source: src/$(basename "$SRC")
Storyboard: storyboard/STORYBOARD.md

Pedagogical route:
ORDER → Q2 → Q1/Q3 → IQR → 1.5·IQR FENCES → OUTLIERS → WHISKERS → BUILD PLOT → INTERPRET.

Final technical target: 1920x1080, 30 fps, H.264, yuv420p.
Full FFmpeg decode: PASS when qa/full_decode.log is empty.
Dense visual QA: 32 full-resolution audit frames plus qa/QA_CONTACT_SHEET.jpg.
Final MP4 SHA-256: $MP4_SHA

The package contains the exact rendered source, storyboard, final PQH MP4, technical QA, literal PQL/PQH logs, audit frames, protocol and reproduction pipeline.
EOF
(
  cd "$ROOT"
  sha256sum render/* src/* storyboard/* protocol/* qa/VIDEO_TECHNICAL.tsv qa/full_decode.log qa/QA_CONTACT_SHEET.jpg qa/audit_frames/* workflow/* > qa/SHA256SUMS.txt
)
cp "$ROOT/render/$FINAL" "delivery/$FINAL"
(cd delivery && zip -qr "$ZIP" "$PROJECT")
test -s "delivery/$ZIP"
sha256sum "delivery/$ZIP" > "delivery/${ZIP}.sha256"
unzip -t "delivery/$ZIP" | tee delivery/ZIP_TEST.txt
sha256sum "$SRC" "$STORY" "$PROTOCOL" > qa_runtime/POST_RENDER_SHA256.txt
cmp qa_runtime/PRE_RENDER_SHA256.txt qa_runtime/POST_RENDER_SHA256.txt

echo '[7/7] Pipeline PASS'
cat qa_runtime/VIDEO_TECHNICAL.tsv
cat "delivery/${ZIP}.sha256"
