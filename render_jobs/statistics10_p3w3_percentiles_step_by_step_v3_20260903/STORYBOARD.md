# Statistics 10 · P3W3 Percentiles — Step-by-Step V3

## Revision goal

This version preserves the mathematical content of the accepted post-Semana-Robledista class while changing the instructional rhythm for students who learn better from explicit procedural numbering.

The core method is now repeated consistently in every worked example:

1. **ORDER DATA**
2. **IDENTIFY k, n**
3. **COMPUTE L** using `L=(k/100)(n+1)`
4. **DECIDE TYPE** — integer or decimal locator
5. **READ / INTERPOLATE**
6. **INTERPRET + CHECK**

## Main changes from the accepted V2

- Replaces the tiny eight-item navigator with a larger six-step method bar.
- Adds a large numbered step banner before each operation.
- Uses the same six-step language in P40, P65, and the guided challenge.
- Adds explicit raw-data → ordered-data staging before percentile calculations.
- Makes the integer/decimal locator decision a dedicated step.
- Makes interpolation for P65 visually explicit between positions 6 and 7 and values 72 and 75.
- Adds longer read/thinking pauses after each numbered instruction and before answer reveals.
- Removes camera-focus zooms from worked examples so progress navigation stays visually stable.
- Keeps the IQR/boxplot bridge: `Q1=P25`, `Q2=P50`, `Q3=P75`.
- Keeps quartile/decile conversion, percentile value vs percentile rank, contextual interpretation, and guided practice.

## Verified examples

Primary data after ordering:
`52, 58, 61, 64, 68, 72, 75, 81, 88`

- `P40`: `L=4`, therefore `P40=64`.
- `P65`: `L=6.5`, therefore `P65=72+0.5(75-72)=73.5`.
- `D7=P70`: `L=7`, therefore `D7=P70=75`.

Challenge data after ordering:
`12, 15, 17, 18, 21, 24, 27, 31, 34, 39, 43`

- `D3=P30`: `L=3.6`, result `17.6`.
- `P85`: `L=10.2`, result `39.8`.

## Scene order

1. Opening — *Percentiles: Step by Step*.
2. IQR / boxplot bridge.
3. Universal six-step method.
4. Worked Example A: P40, all six steps.
5. Worked Example B: P65, all six steps plus animated interpolation.
6. Quartile and decile translation into percentile language.
7. Percentile value vs percentile rank + context check.
8. Guided challenge with a deliberate solve pause and full numbered reveal.
9. Final six-step recipe + common-error reminders.

## Visual contract

- ManimCE 0.20.1.
- 1920×1080, 30 fps.
- White background; monochrome black/gray classroom hierarchy.
- JP Classroom style library.
- Larger numbered instructions and stable camera.
- No overlapping step navigator during zoom because this revision does not use worked-example camera zooms.

## Render acceptance

Pipeline must pass:

`py_compile → numerical assertions → literal -pql preview → literal -pqh final → ffprobe 1920×1080/30/H.264/yuv420p → full FFmpeg decode → dense QA frame sampling → SHA-256 → direct repository delivery`.
