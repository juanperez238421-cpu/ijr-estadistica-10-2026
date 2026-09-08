# Statistics 10 · Class 4 V2 · Percentile Rank & Relative-Position Decisions

## Topic

**Percentile rank, relative position, and decision making.**

This V2 is a direct successor to the validated Class 4 V1. It does not replace the topic; it improves the visual and pedagogical route from an observed value to its cumulative relative position and then to a contextual decision.

## Class continuity

- **Class 3:** percentile → data value.
- **Class 4:** observed value → percentile rank → relative position → decision.

The opening keeps the Class 3 example `P65 ≈ 73.5` and explicitly reverses the question for Class 4.

## Classroom convention

For this lesson, ungrouped ordered data use:

```text
PR(x) = 100 × count(values <= x) / n
```

The lesson repeatedly says **AT OR BELOW**. Equal values are included because the class convention uses `<=`.

## Validated examples

All displayed numerical results are asserted before rendering:

- `PR(61) ≈ 33.3%`
- `PR(72) ≈ 66.7%`
- `PR(75) ≈ 77.8%`
- `PR(81) ≈ 88.9%`
- same score `72` in Class A: `66.7%`
- same score `72` in Class B: `44.4%`
- ties dataset: `PR(72) ≈ 66.7%`
- guided challenge: `PR(24) = 60%`
- Top-20% rule: `PR(81) >= 80`, while `PR(75) < 80`
- complement above 81: approximately `11.1%`

## Pedagogical improvements over V1

V2 changes the learning order from formula-first to:

```text
SEE → COUNT → LOCATE → FORMALIZE → INTERPRET → DECIDE
```

Major improvements:

1. **Same-score / different-group hook** before formal definition.
2. **Sequential cumulative counting** for `PR(72)` with an animated running counter.
3. Count → fraction → decimal → percentage → percentile-axis position.
4. Larger, projector-legible six-step navigator.
5. Full six-step worked example with sanity check.
6. `PR(61)`, `PR(72)`, and `PR(81)` on one shared percentile axis.
7. Top-20% threshold shown at `PR = 80` before evaluating 81.
8. Explicit comparison showing 81 qualifies while 75 does not.
9. New ties scene making the `<=` convention concrete.
10. New misconception clinic with TRUE/FALSE interpretation checks.
11. Stronger simultaneous comparison of percentile value vs percentile rank.
12. Guided challenge with a real student-thinking pause.
13. Exit ticket based on interpretation rather than long substitution.
14. Final method map that uses the screen intentionally.
15. Curricular bridge to **Introduction to the Normal Distribution** without introducing z-scores, the empirical rule, or normal-curve equations.

## Six-step method

1. ORDER DATA
2. IDENTIFY x, n
3. COUNT <= x
4. COMPUTE PR
5. INTERPRET
6. DECIDE + CHECK

## Visual standard

- JP Classroom architecture
- white background
- black typography
- restrained gray hierarchy
- numbered section headers
- monochrome academic styling
- no decorative color system
- no unnecessary spins or cartoon motion
- semantically meaningful transitions only

## Render target

- Manim Community Edition `0.20.1`
- 1920 × 1080
- 30 fps
- H.264
- yuv420p
- target classroom duration: 6:30–7:45

The pipeline derives the final `LESSON_TIME_SCALE` from the literal full-timeline PQL duration to target approximately 7:00 while preserving deliberate thinking pauses.

## QA pipeline

The workflow performs:

1. exact source copy and SHA-256
2. `python -m py_compile`
3. deterministic mathematical assertions
4. content guards
5. literal `-pql` full timeline
6. adaptive final timing calculation
7. literal `-pqh` final render
8. `ffprobe` acceptance checks
9. complete FFmpeg decode
10. 48 distributed QA frames
11. dense 5-second QA extraction
12. targeted cumulative-count frames
13. targeted contact sheets for percentile-axis, Top-20%, value-vs-rank, and final bridge
14. final hashes and render summary

## Final artifact

```text
Statistics10_Class4_Percentile_Rank_Decisions_V2_SENIOR_FINAL_pqh.mp4
```

Published directory after a successful workflow:

```text
deliveries/statistics10_class4_percentile_rank_decisions_v2_final/
```

The generated delivery README appends the exact duration, render timing scale, SHA-256, technical format, and complete-decode result.
