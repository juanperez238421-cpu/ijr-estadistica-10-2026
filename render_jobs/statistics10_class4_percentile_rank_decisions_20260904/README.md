# Statistics 10 · Class 4 · Percentile Rank & Decisions

## Instructional position

This package is the direct continuation of the real Statistics 10 Class 3 step-by-step percentile lesson on branch `render/statistics10-p3w3-percentiles-step-by-step-v3-20260903` (baseline SHA `6290602c05276fd3116f8098a9d5a8e29f0cdc00`).

Class 3 asks **percentile → value**. Class 4 reverses the question to **raw value → relative position → decision** without claiming an exact inverse relationship.

## Classroom convention

For this lesson only, ungrouped ordered data use:

`PR(x) = 100 × count(v <= x) / n`

The lesson explicitly notes that percentile-rank conventions can vary across texts/software and that this cumulative classroom convention is used consistently.

## Scene

- Source assembled from `source_parts/part_*.pyfrag`
- Scene: `Stat10Class4PercentileRankDecisions`
- Target MP4: `Stat10_Class4_Percentile_Rank_Decisions_SENIOR_FINAL_PQH.mp4`
- ManimCE: `0.20.1`
- Final: 1920×1080, 30 fps, H.264/yuv420p

## Five-step method

1. ORDER THE DATA
2. IDENTIFY x AND n
3. COUNT VALUES <= x
4. COMPUTE PR(x)
5. INTERPRET AND DECIDE

## Numerical gates

The source validates all displayed datasets/results before rendering, including PR(72)≈66.7, PR(75)≈77.8, PR(81)≈88.9, the same-72/different-group example, ties, guided challenge and exit ticket.

## Render protocol

`source reconstruction → py_compile → numerical assertions → literal -pql full timeline (CI-compressed timing only) → literal -pqh full classroom timing → ffprobe → full FFmpeg decode → dense distributed frame extraction/contact sheet → SHA-256 → direct branch publication`

No normal distribution, z-scores, Python/Colab instruction, Pandas, or programming content is introduced in this lesson.
