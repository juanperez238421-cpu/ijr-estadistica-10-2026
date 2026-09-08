# Statistics 10 · Class 4 · Percentile Rank Decisions · V2 QA

## Why V2 exists

The uploaded V1 final MP4 was reviewed across its full 425 s timeline and with dense frame sampling. The statistical core is correct under the declared classroom convention, but the rendered video has several presentation defects and a few places where the teaching language can be more exact.

### Confirmed V1 defects

- Scene 01: the bottom inversion diagram and the sentence `These are different questions.` occupy the same vertical band during the final reveal.
- Scene 01 → Scene 02 transition: header text briefly collides during the stage clear / next-header reveal.
- Scene 02: the value/rank cards, warning sentence and lower safe margin are too compressed.
- Scene 07: interpretation cards plus value/relative-position cards create an unnecessarily dense lower stack above the persistent navigation strip.
- Scene 09: the top-20% decision is mathematically valid, but the complement calculation is less direct than stating and testing the percentile-rank criterion `PR(x) >= 80`.
- V1 repository documentation is internally inconsistent: one README calls the method a five-step method while the rendered/source lesson uses six steps.

## V2 corrections

1. Rebuild Scene 01 into three separate vertical bands: comparison cards, reverse-direction band, key-distinction card.
2. Re-space Scene 02 and explicitly state the class convention `PR(x)=100*count(values<=x)/n`, including ties at `x`.
3. Rebuild Scene 07 with two interpretation bands plus one compact value→position relation, removing the cramped lower card pair.
4. Rebuild Scene 09 around the direct criterion `top 20% -> PR(x) >= 80` and then compare `88.9 >= 80`.
5. Replace the final bridge with explicit continuity: percentile value → percentile rank → distribution comparison with boxplots → normal distribution.
6. Preserve the validated V1 numerical examples, six-step navigator, student pause structure, monochrome JP classroom format, 1920x1080 output and ManimCE 0.20.1.

## Numerical convention

For this classroom lesson:

`PR(x) = 100 × count(observations <= x) / n`

Validated inherited results:

- `PR(72) = 100*(6/9) ≈ 66.7`
- `PR(61) = 100*(3/9) ≈ 33.3`
- `PR(81) = 100*(8/9) ≈ 88.9`
- guided challenge: `PR(24) = 100*(6/10) = 60`

## Render target

- Scene: `Statistics10Class4PercentileRankV2`
- Final: `Statistics10_Class4_Percentile_Rank_Decisions_V2_FINAL_pqh.mp4`
- ManimCE: `0.20.1`
- Video: `1920×1080`, `30 fps`, H.264, yuv420p
- Gates: py_compile → inherited math assertions → PQL full timeline → PQH → ffprobe → full decode → duration gate → dense contact sheet → SHA-256 → branch publication.
