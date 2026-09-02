# Render instructions

Scene:

```text
Statistics10Period3Week3PercentilesPostRobledista
```

Preview validation:

```bash
manim -pql manim/period3_week3_percentiles/scene.py Statistics10Period3Week3PercentilesPostRobledista --disable_caching
```

Final render:

```bash
manim -pqh manim/period3_week3_percentiles/scene.py Statistics10Period3Week3PercentilesPostRobledista --disable_caching
```

Target: Manim Community Edition 0.20.1, 1920×1080, 30 fps.
