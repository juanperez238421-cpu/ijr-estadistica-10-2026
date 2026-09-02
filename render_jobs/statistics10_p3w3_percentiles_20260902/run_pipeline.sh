#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)"
JOB="render_jobs/statistics10_p3w3_percentiles_20260902"
SCENE_NAME="Statistics10Period3Week3PercentilesPostRobledista"
OUT_NAME="Statistics10_P3W3_Quartiles_Deciles_Percentiles_PostRobledista_FINAL_pqh.mp4"
MANIM_IMAGE="manimcommunity/manim:v0.20.1"

mkdir -p "$JOB/build" "$JOB/delivery" "$JOB/qa_frames" library

# -----------------------------------------------------------------------------
# 1. Reconstruct exact source and consolidated JP style
# -----------------------------------------------------------------------------
cat "$JOB"/source_parts/part_*.pyfrag > "$JOB/build/scene.py"
printf '' > library/__init__.py
base64 -d render_jobs/statistics10_p3w2_iqr_boxplot_20260824/payload/jp_classroom_style.py.gz.b64 \
  | gzip -dc > library/jp_classroom_style.py

sha256sum "$JOB/build/scene.py" library/jp_classroom_style.py | tee "$JOB/delivery/source_sha256.txt"

# -----------------------------------------------------------------------------
# 2. Syntax + numerical assertions
# -----------------------------------------------------------------------------
docker run --rm -v "$ROOT:/manim" -w /manim "$MANIM_IMAGE" bash -c '
  set -euo pipefail
  python -m py_compile library/jp_classroom_style.py
  python -m py_compile render_jobs/statistics10_p3w3_percentiles_20260902/build/scene.py
  python -c "import importlib.util, pathlib; p=pathlib.Path(\"render_jobs/statistics10_p3w3_percentiles_20260902/build/scene.py\"); spec=importlib.util.spec_from_file_location(\"statistics10_p3w3_scene\", p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); m.validate_all_data(); print(\"Numerical assertions: PASS\")"
'

# -----------------------------------------------------------------------------
# 3. Literal -pql preview
# -----------------------------------------------------------------------------
docker run --rm -v "$ROOT:/manim" -w /manim --entrypoint bash "$MANIM_IMAGE" -c '
  set -euo pipefail
  mkdir -p /tmp/bin
  printf "#!/usr/bin/env bash\nexit 0\n" > /tmp/bin/xdg-open
  chmod +x /tmp/bin/xdg-open
  export PATH="/tmp/bin:$PATH"
  manim -pql render_jobs/statistics10_p3w3_percentiles_20260902/build/scene.py \
    Statistics10Period3Week3PercentilesPostRobledista \
    --format=mp4 --disable_caching
'

# -----------------------------------------------------------------------------
# 4. Literal -pqh final render
# -----------------------------------------------------------------------------
docker run --rm -v "$ROOT:/manim" -w /manim --entrypoint bash "$MANIM_IMAGE" -c '
  set -euo pipefail
  mkdir -p /tmp/bin
  printf "#!/usr/bin/env bash\nexit 0\n" > /tmp/bin/xdg-open
  chmod +x /tmp/bin/xdg-open
  export PATH="/tmp/bin:$PATH"
  manim -pqh render_jobs/statistics10_p3w3_percentiles_20260902/build/scene.py \
    Statistics10Period3Week3PercentilesPostRobledista \
    --format=mp4 --disable_caching
'

FINAL_MP4="$(find media/videos -type f -path '*1080p*' -name "${SCENE_NAME}.mp4" | sort | tail -n 1)"
test -n "$FINAL_MP4"
cp "$FINAL_MP4" "$JOB/delivery/$OUT_NAME"

# -----------------------------------------------------------------------------
# 5. Technical acceptance: ffprobe + full decode
# -----------------------------------------------------------------------------
docker run --rm -v "$ROOT:/manim" -w /manim "$MANIM_IMAGE" \
  ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt \
  -of default=noprint_wrappers=1 "$JOB/delivery/$OUT_NAME" \
  | tee "$JOB/delivery/ffprobe.txt"

grep -q '^codec_name=h264$' "$JOB/delivery/ffprobe.txt"
grep -q '^width=1920$' "$JOB/delivery/ffprobe.txt"
grep -q '^height=1080$' "$JOB/delivery/ffprobe.txt"
grep -q '^r_frame_rate=30/1$' "$JOB/delivery/ffprobe.txt"
grep -q '^pix_fmt=yuv420p$' "$JOB/delivery/ffprobe.txt"

docker run --rm -v "$ROOT:/manim" -w /manim "$MANIM_IMAGE" \
  ffmpeg -v error -i "$JOB/delivery/$OUT_NAME" -f null -

# -----------------------------------------------------------------------------
# 6. Dense visual audit sampling (~32 frames) + contact sheet
# -----------------------------------------------------------------------------
DURATION="$(docker run --rm -v "$ROOT:/manim" -w /manim "$MANIM_IMAGE" \
  ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$JOB/delivery/$OUT_NAME")"
INTERVAL="$(python -c "d=float('$DURATION'); print(max(d/32.0, 0.5))")"
rm -f "$JOB"/qa_frames/*.png

docker run --rm -v "$ROOT:/manim" -w /manim "$MANIM_IMAGE" \
  ffmpeg -v error -i "$JOB/delivery/$OUT_NAME" \
  -vf "fps=1/$INTERVAL,scale=480:-1" "$JOB/qa_frames/frame_%03d.png"

docker run --rm -v "$ROOT:/manim" -w /manim "$MANIM_IMAGE" python -c '
from pathlib import Path
from PIL import Image
folder=Path("render_jobs/statistics10_p3w3_percentiles_20260902/qa_frames")
paths=sorted(folder.glob("frame_*.png"))[:32]
if not paths:
    raise SystemExit("No QA frames generated")
ims=[Image.open(p).convert("RGB") for p in paths]
w=max(im.width for im in ims); h=max(im.height for im in ims)
cols=4; rows=(len(ims)+cols-1)//cols
sheet=Image.new("RGB", (cols*w, rows*h), "white")
for i,im in enumerate(ims):
    sheet.paste(im, ((i%cols)*w, (i//cols)*h))
sheet.save("render_jobs/statistics10_p3w3_percentiles_20260902/delivery/QA_contact_sheet.jpg", quality=90)
'

# -----------------------------------------------------------------------------
# 7. Canonical delivery package
# -----------------------------------------------------------------------------
cp "$JOB/build/scene.py" "$JOB/delivery/scene.py"
cp "$JOB/STORYBOARD.md" "$JOB/delivery/STORYBOARD.md"
cp library/jp_classroom_style.py "$JOB/delivery/jp_classroom_style.py"
sha256sum "$JOB/delivery/$OUT_NAME" | tee "$JOB/delivery/SHA256SUMS.txt"

printf 'Final scene: %s\nFinal MP4: %s\n' "$SCENE_NAME" "$JOB/delivery/$OUT_NAME" \
  | tee "$JOB/delivery/RENDER_SUMMARY.txt"
