#!/usr/bin/env bash
set -euo pipefail
MODE="$1"
if [[ "$MODE" == preview ]]; then
  SCALE=0.08; QUALITY=pql; FPS=15; RES=854,480; DIR=media_preview; OUT=Statistics10_IQR_Graph_Construction_Problems_pql.mp4
else
  SCALE=1.00; QUALITY=pqh; FPS=30; RES=1920,1080; DIR=media_final; OUT=Statistics10_IQR_Graph_Construction_Problems_Professional_pqh.mp4
fi
docker run --rm --user "$(id -u):$(id -g)" \
  -e HOME=/tmp/manim-home -e LESSON_TIME_SCALE="$SCALE" \
  -v "$PWD:/manim" -w /manim --entrypoint bash manimcommunity/manim:v0.20.1 -c "
    set -euo pipefail
    mkdir -p /tmp/manim-home /tmp/manim-bin delivery
    printf '#!/usr/bin/env bash\\nexit 0\\n' > /tmp/manim-bin/xdg-open
    chmod +x /tmp/manim-bin/xdg-open
    export PATH=/tmp/manim-bin:\$PATH
    manim -$QUALITY --fps $FPS -r $RES statistics10_iqr_graph_construction_problems.py Statistics10IQRGraphConstructionProblems --format=mp4 --disable_caching --media_dir $DIR
    VIDEO=\$(find $DIR -type f -name Statistics10IQRGraphConstructionProblems.mp4 -print -quit)
    test -n \"\$VIDEO\" && test -s \"\$VIDEO\"
    cp \"\$VIDEO\" delivery/$OUT
  "
ffmpeg -v error -i "delivery/$OUT" -f null -
