# Statistics 10 — IQR / Modified Box Plot — Step-by-Step Senior V1

## Pedagogical objective
Build a modified box plot from raw data in a causal sequence students can reproduce in their notebooks: order the observations, determine Q1/Q2/Q3, calculate IQR, calculate the 1.5×IQR fences, identify outliers, choose the actual whisker endpoints, and only then draw and interpret the graph.

## Reference dataset and convention
Dataset: `4, 15, 3, 7, 2, 8, 4, 6, 5`.

Ordered data: `2, 3, 4, 4, 5, 6, 7, 8, 15`.

Quartile convention: for odd `n`, exclude the overall median from both halves before finding Q1 and Q3.

Validated results: Q1 = 3.5, Q2 = 5, Q3 = 7.5, IQR = 4, lower fence = -2.5, upper fence = 13.5, outlier = 15, whiskers = 2 and 8.

## Visual continuity strategy
The lesson uses one stable white/black JP Classroom visual language. Every act has a large current-step banner and a bottom route strip. The dataset remains card-based while quartiles are derived. The plot is not shown as a finished object until every numerical decision that determines it has been made.

## Act order
1. Opening mental model: `DATA → QUARTILES → IQR → FENCES → WHISKERS → BOX PLOT`.
2. Order the raw data.
3. Find the median Q2 and explicitly state the odd-n exclusion rule.
4. Split into lower/upper halves and calculate Q1/Q3.
5. Calculate and interpret IQR as the width of the middle 50%.
6. Calculate lower and upper 1.5×IQR fences.
7. Classify 15 as an outlier and identify 2/8 as whisker endpoints.
8. Build the modified box plot element by element: scale → Q1/Q3 marks → box → median → whiskers → outlier.
9. Zoom into the completed plot for a deliberate reading pause.
10. Interpret each element and close with a reproducible 8-step method.

## Persistent objects
Within each act the step banner and route strip remain stable. The section header remains persistent except during the deliberate plot zoom, where it temporarily fades to maximize usable projector space.

## Camera / zoom behavior
Camera movement is restrained. The only major zoom is after the graph has been fully constructed. The zoom encloses the complete plot and returns to the default camera before the next act, preserving spatial orientation.

## Equation progression
Equations are revealed one decision at a time. No frame presents fences, whiskers, or the final box plot before their prerequisite values are established.

## Timing intent
- Short pause after every visual state change.
- Reading pause after each key formula.
- Longer explanation pause after IQR/fences/whisker decisions.
- Dedicated final zoom/read pause on the completed graph.
- Final summary remains visible long enough for notebook copying.

## Transition rules
- Prefer Fade/Create/Write for semantic continuity.
- Avoid geometry-to-text morphs.
- Do not transform unrelated objects through glyph interpolation.
- Clear content between major acts while keeping the JP header architecture stable.

## Final conceptual takeaway
The box plot is not an arbitrary drawing. It is the visual consequence of ordered data, quartiles, IQR, fences, outlier classification, and whisker selection.

## QA risks to audit
- Route strip must remain inside the lower safe frame.
- Step banner must not enter the persistent header zone.
- Axis number labels and box annotations must not overlap.
- Whisker labels must not be confused with fences.
- Outlier label at 15 must stay inside the right frame margin.
- Plot zoom must include the entire outlier and axis labels.
- Final recap cards must remain large enough for projection and not collide with the closing note.
