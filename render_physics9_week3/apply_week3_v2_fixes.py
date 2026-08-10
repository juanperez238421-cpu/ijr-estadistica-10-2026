#!/usr/bin/env python3
from pathlib import Path
import hashlib

path = Path("physics9_week3_acceleration_galileo.py")
text = path.read_text(encoding="utf-8")

base_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
assert base_sha == "539627bb7f00f3e8f192e0cc0040dec2895a200af8df812ebfa096093b1b0e96", base_sha

old = '''            box_width=2.45,\n            box_height=1.15,\n            font_size=23,\n            gap=0.18,\n'''
new = '''            card_width=2.45,\n            card_height=1.15,\n            columns=5,\n'''
assert text.count(old) == 1
text = text.replace(old, new)

old = '''        ], box_width=2.5, box_height=1.18, font_size=23, gap=0.20)\n'''
new = '''        ], card_width=2.50, card_height=1.18, columns=5)\n'''
assert text.count(old) == 1
text = text.replace(old, new)

old = '''        card_panel = self.figure_panel(VGroup(cards, arrows, dv_labels), width=13.0, height=3.15, title="FOUR EQUAL-TIME SNAPSHOTS", caption="Equal Δv during equal Δt means constant acceleration.", title_size=31, caption_size=24)\n        calc = self.formula_panel(r"a=\\frac{\\Delta v}{\\Delta t}=\\frac{+3\\,m/s}{1\\,s}=+3\\,\\mathrm{m/s^2}", width=8.5, height=1.42, font_size=39)\n        lab = self.note_panel("LAB HABIT", ["Record time first. Record velocity second. Compare consecutive cards — do not skip intervals."], width=11.0, title_size=29, body_size=27)\n        group = VGroup(card_panel.group, calc, lab).arrange(DOWN, buff=0.28).move_to(DOWN * 0.45)\n'''
new = '''        card_panel = self.figure_panel(VGroup(cards, arrows, dv_labels), width=13.0, height=2.75, title="FOUR EQUAL-TIME SNAPSHOTS", caption="Equal Δv during equal Δt means constant acceleration.", title_size=30, caption_size=23)\n        calc = self.formula_panel(r"a=\\frac{\\Delta v}{\\Delta t}=\\frac{+3\\,m/s}{1\\,s}=+3\\,\\mathrm{m/s^2}", width=6.25, height=1.30, font_size=35)\n        lab = self.note_panel(\n            "LAB HABIT",\n            ["Record time first; velocity second.", "Compare consecutive cards — do not skip intervals."],\n            width=6.25, title_size=27, body_size=24, max_text_height=1.45,\n        )\n        bottom = VGroup(calc, lab).arrange(RIGHT, buff=0.28)\n        group = VGroup(card_panel.group, bottom).arrange(DOWN, buff=0.24).move_to(DOWN * 0.70)\n'''
assert text.count(old) == 1
text = text.replace(old, new)

path.write_text(text, encoding="utf-8")
out_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
assert out_sha == "4a26dccad452dec424a0fcf7f631680e7dfceb36c473ad3aef75de683d8972ad", out_sha
print("Week 3 V2 deterministic fixes applied:", out_sha)
