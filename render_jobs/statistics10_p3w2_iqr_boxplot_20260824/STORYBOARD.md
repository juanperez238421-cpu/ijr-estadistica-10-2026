# Storyboard — Statistics 10 · Period 3 · Week 2
## IQR / Modified Box-Plot Construction — Senior Consolidated Edition

**Version:** 2026-08-24 V1  
**Target class:** Grade 10 Statistics, Period 3, Week 2 (24–28 Aug 2026)  
**Primary class date:** 25 Aug 2026  
**Scene:** `Statistics10Period3Week2IQRBoxPlotConstructionSenior`

## 1. Pedagogical objective

Students must be able to construct a modified box-and-whisker plot from raw data without treating the graph as a memorized picture. Every geometric element must be causally linked to a statistical calculation or decision:

1. order the observations;
2. find Q2;
3. split the ordered data and find Q1/Q3;
4. compute IQR;
5. compute 1.5·IQR fences;
6. classify outliers and identify the actual whisker endpoints;
7. build the modified box plot on a numerical scale;
8. interpret center, middle-50% spread, asymmetry and outliers;
9. compare plots only on a common numerical scale.

The lesson preserves the established classroom convention: for odd `n`, Q2 is excluded before calculating Q1 and Q3.

## 2. Source consolidation used

This revision intentionally combines the strongest already-validated elements from the recovered IQR package instead of inventing a new visual language:

- **2026-08-04 IQR / Modified Box-Plot Construction FINAL:** ordered-data route, odd-n quartile convention, `IQR = Q3 - Q1`, 1.5·IQR fences, outlier classification, and the distinction between fences and actual whisker endpoints.
- **2026-08-10 Box-and-Whisker Plot Senior:** large projector-safe typography, persistent step navigator, progressive plot geometry, and same-scale comparison logic.
- **2026-08-24 ManimCE PQH Project Package Standard v1.1:** storyboard, literal PQL, literal PQH, technical verification, dense audit frames, SHA-256, exact-source preservation, and a canonical reproducible ZIP.

## 3. Mathematical dataset

Raw data:

`4, 15, 3, 7, 2, 8, 4, 6, 5`

Ordered data:

`2, 3, 4, 4, 5, 6, 7, 8, 15`

Derived statistics:

- `Q1 = 3.5`
- `Q2 = 5`
- `Q3 = 7.5`
- `IQR = 4`
- lower fence `= -2.5`
- upper fence `= 13.5`
- outlier `= 15`
- lower whisker `= 2`
- upper whisker `= 8`

Comparison group:

`2, 3, 4, 4, 5, 6, 7, 8, 11`

It intentionally preserves the same Q1/Q2/Q3/IQR but has a different upper tail, so the final comparison can focus on scale, whisker length, and outlier behavior.

## 4. Persistent visual continuity

During the instructional core, two structures remain stable:

- a top header containing course/week, act title and one concise explanatory subtitle;
- an eight-step navigator at the bottom showing the current construction step.

The plot is not repeatedly destroyed and rebuilt once the graph-construction act begins. Its components are added in the same coordinate system:

`scale → Q1/Q3 marks → box → median → whiskers → outlier`.

This preserves the viewer's spatial mental model.

## 5. Act order

### Act 0 — Opening
Large title and purpose. State that the lesson constructs the graph from raw data without skipping statistical decisions.

### Act 1 — Route preview
Show the eight-step process as a map. Explicitly flag the most common conceptual error: **fences are not whiskers**.

### Act 2 — Order the data
Show raw data first. Animate the transition to ordered data. Add positional indices only after sorting. Use one controlled camera zoom to make the ordered row and indices easy to copy.

### Act 3 — Q2, Q1, Q3
Highlight the fifth ordered observation as Q2. Then dim Q2 and split the remaining values into lower and upper halves. Calculate Q1 and Q3 transparently from their middle pairs. Use a controlled focus zoom on the two halves.

### Act 4 — IQR and fences
First compute and interpret IQR as the width of the middle 50%. Only after that, introduce the 1.5·IQR fences. Keep the two ideas visually separate so students do not confuse IQR width with fence locations.

### Act 5 — Outlier and whisker decision
Apply the fences to the ordered data. Highlight 15 only after the complete row is visible. State:

- 15 is an outlier because `15 > 13.5`;
- lower whisker endpoint is 2;
- upper whisker endpoint is 8;
- fences are decision boundaries, not drawn whisker endpoints.

### Act 6 — Build the modified box plot
Use one fixed numerical scale from -4 to 16. Build the plot in five visible substeps:

1. mark Q1 and Q3;
2. draw the box Q1→Q3;
3. add Q2 median line;
4. connect whiskers to 2 and 8;
5. plot 15 separately as an outlier.

Finish with labels and a controlled zoom on the completed geometry.

### Act 7 — Interpret and compare
Read:

- median = 5;
- middle 50% = 3.5 to 7.5;
- IQR = 4;
- 15 is isolated above the upper fence;
- visible asymmetry is present because the median is not centered in the box and the high outlier is separated.

Then compare Group A with Group B on the same numerical scale. The comparison is designed to show that equal quartiles/IQR do not imply identical tails.

### Act 8 — Final recipe
Full-screen two-column recipe. End with the invariant conceptual distinction:

**1.5·IQR fences classify values; whiskers end at actual non-outlier observations.**

## 6. Camera protocol

Camera use is deliberately sparse:

- default frame is stable 16:9;
- zoom only for the ordered-data positional row;
- zoom only for lower/upper-half quartile calculation;
- zoom only once on the completed modified box plot;
- every zoom returns smoothly to the full classroom frame before the next conceptual state.

No camera zoom is used merely as decoration.

## 7. Typography and layout rules

- 1920×1080, 30 fps, white background.
- Black/dark-gray text; neutral grayscale fills.
- Large classroom typography; no dense multi-paragraph cards.
- Header and step navigator occupy reserved zones.
- Main content stays between the header rule and the step navigator.
- Equations are revealed after the relevant data/geometry is visible.
- Long explanatory sentences are reduced to one line or one note card.

## 8. Transition rules

- Use `FadeIn`, `Create`, `Write`, and controlled `ReplacementTransform` only for like-for-like UI state changes.
- Avoid geometry-to-text morphs.
- Avoid simultaneous disappearance/reappearance of the complete plot during construction.
- Never transform a fence into a whisker because they represent different concepts.
- Preserve the numerical axis while assembling the graph.

## 9. QA risks to audit densely

Critical audit windows:

1. ordered-data indices after camera zoom;
2. lower/upper half layout and Q1/Q3 equations;
3. two fence equations displayed simultaneously;
4. whisker endpoint note versus bottom step navigator;
5. plot labels Q1/Q2/Q3 and outlier 15;
6. camera restoration after plot focus;
7. Group A / Group B common-scale comparison;
8. final two-column recipe and bottom closure line.

Reject the render if any text is clipped, if a label touches another mathematical object, if the step strip overlaps a note, or if a plot component disappears during a causal construction sequence.

## 10. Final conceptual takeaway

A box plot is not drawn directly from raw data. It is the visual consequence of a sequence of statistical decisions:

`ORDER → QUARTILES → IQR → FENCES → OUTLIERS → WHISKERS → GRAPH → INTERPRET`.
