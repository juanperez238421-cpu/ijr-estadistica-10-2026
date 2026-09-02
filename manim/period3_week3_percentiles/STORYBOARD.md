# Statistics 10 · Period 3 · Week 3 — Post-Semana-Robledista
## Quartiles, Deciles & Percentiles in Context

**Target:** Grade 10 Statistics  
**Period:** 3  
**Week:** first regular academic week after Semana Robledista (7–11 Sep 2026)  
**Scene:** `Statistics10Period3Week3PercentilesPostRobledista`  
**ManimCE:** 0.20.x  
**Format:** JP Classroom monochrome, 1920×1080, 30 fps

## Pedagogical continuity

The previous consolidated lesson completes the IQR / modified box-plot route:

`ORDER → QUARTILES → IQR → FENCES → OUTLIERS → WHISKERS → GRAPH → INTERPRET`

This class does **not** repeat box-plot construction. Instead, it extracts the deeper positional idea already visible in the box plot:

- `Q1 = P25`
- `Q2 = P50`
- `Q3 = P75`

From there the lesson generalizes to deciles and percentiles.

## Classroom convention

The class preserves the established Grade 10 locator convention used in the previous percentile sequence:

```math
L=\frac{k}{100}(n+1)
```

For non-integer `L`, use linear interpolation between the adjacent ordered positions.

## Act sequence

1. **Boxplot bridge** — visually connect Q1/Q2/Q3 to P25/P50/P75.
2. **One family, three resolutions** — quartiles (4), deciles (10), percentiles (100).
3. **Locator rule** — distinguish position `L` from data value.
4. **Integer example** — calculate `P40` from a 9-value score dataset.
5. **Interpolation example** — calculate `P65 = 73.5` from locator `L=6.5`.
6. **Decile conversion** — show `D_j=P_{10j}` and calculate `D7=P70=75`.
7. **Percentile value vs percentile rank** — distinguish the two inverse questions.
8. **Context matters** — exam score vs race time; percentile is position, not automatic quality.
9. **Misconception clinic** — reject common false interpretations.
10. **Guided challenge** — students calculate `D3=17.6` and `P85=39.8` with an explicit pause.
11. **Final recipe** — reusable 8-step method.

## Primary verified dataset

Raw / ordered values:

`52, 58, 61, 64, 68, 72, 75, 81, 88`

Verified outputs:

- `P40`: `L=4`, `P40=64`
- `P50`: `L=5`, `P50=68`
- `P65`: `L=6.5`, `P65=73.5`
- `D7=P70`: `L=7`, value `75`
- `P75`: `L=7.5`, value `78`

## Guided challenge dataset

`12, 15, 17, 18, 21, 24, 27, 31, 34, 39, 43`

- `D3=P30`: `L=3.6`, value `17.6`
- `P85`: `L=10.2`, value `39.8`

## Visual rules

- white background;
- black/dark-gray typography and geometry;
- neutral grayscale fills only;
- persistent numbered header;
- bottom 8-step navigator in the safe frame zone;
- equations are revealed only after the relevant ordered positions are visible;
- no geometry-to-text morphs;
- no decorative camera movement;
- controlled zoom only on key final equations;
- projector-safe text sizes and explicit stage clearing between acts.

## Final takeaway

`POSITION FIRST → VALUE SECOND → INTERPRETATION LAST`
