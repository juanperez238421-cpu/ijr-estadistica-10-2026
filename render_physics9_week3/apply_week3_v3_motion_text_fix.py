#!/usr/bin/env python3
from pathlib import Path
import hashlib

path = Path("physics9_week3_acceleration_galileo.py")
text = path.read_text(encoding="utf-8")

base_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
assert base_sha == "4a26dccad452dec424a0fcf7f631680e7dfceb36c473ad3aef75de683d8972ad", base_sha

replacements = {
    '        self.play(TransformFromCopy(VGroup(rising, live), formula), FadeIn(fig_panel.caption), run_time=RUN_NORMAL)\n':
    '        self.play(Indicate(rising, color=MID_GRAY), FadeIn(formula, shift=RIGHT * 0.05), FadeIn(fig_panel.caption), run_time=RUN_NORMAL)\n',

    '            self.play(TransformFromCopy(tri, eq), run_time=RUN_NORMAL)\n':
    '            self.play(Indicate(line, color=MID_GRAY), FadeIn(eq, shift=RIGHT * 0.05), run_time=RUN_NORMAL)\n',

    '        self.play(TransformFromCopy(tri, eq), FadeIn(vt_panel.caption), FadeIn(ramp_panel.caption), run_time=RUN_NORMAL)\n':
    '        self.play(Indicate(fit_line, color=MID_GRAY), FadeIn(eq, shift=DOWN * 0.04), FadeIn(vt_panel.caption), FadeIn(ramp_panel.caption), run_time=RUN_NORMAL)\n',

    '            self.play(FadeIn(tri), TransformFromCopy(seg, eqs[i]), run_time=RUN_NORMAL)\n':
    '            self.play(FadeIn(tri), Indicate(seg, color=MID_GRAY), FadeIn(eqs[i], shift=RIGHT * 0.05), run_time=RUN_NORMAL)\n',
}

for old, new in replacements.items():
    assert text.count(old) == 1, old
    text = text.replace(old, new)

path.write_text(text, encoding="utf-8")
out_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
assert out_sha == "315bcb5d213f2a740033b44fe97ca5cb77e7028fb40f47d81e17f737240d2104", out_sha
print("Week 3 V3 geometry-to-text transition fixes applied:", out_sha)
