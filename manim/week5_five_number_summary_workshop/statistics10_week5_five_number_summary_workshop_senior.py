#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statistics 10 · Period 1 · Week 5 Workshop — Five-Number Summary.

Senior worked-solutions edition. Direct companion to the Week 5 theory class.

Classroom quartile convention (same as Weeks 1–2 and Week 5 theory):
- ORDER the data first.
- Odd n: Q2 is the middle observation and is excluded from both halves.
- Even n: Q2 is the mean of the two central observations; split evenly.
- Q1 and Q3 are the medians of the lower and upper halves.

Persistent solution route:
1. ORDER
2. MIN / MAX
3. FIND Q2
4. SPLIT
5. FIND Q1
6. FIND Q3
7. WRITE 5-NUM
8. INTERPRET

Target: ManimCE 0.20.x, Full HD, white classroom style, literal -pqh render.
"""
from __future__ import annotations

from dataclasses import dataclass
from statistics import median
from manim import *

# ---------------------------------------------------------------------------
# Render / visual contract
# ---------------------------------------------------------------------------
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

INK = BLACK
DARK = "#303030"
MID = "#777777"
LIGHT = "#D6D6D6"
VERY_LIGHT = "#EEEEEE"
PAPER = "#F8F8F8"
SAFE_W = 14.60

RUN_FAST = 0.34
RUN = 0.62
RUN_SLOW = 0.90
PAUSE_READ = 1.05
PAUSE_EXPLAIN = 1.55
PAUSE_WORK = 2.70
PAUSE_FINAL = 2.60

Y_DATA = 2.28
Y_META = 1.06
Y_LOWER = 0.52
Y_UPPER = -0.25
Y_CALC = -1.22
Y_RESULT = -2.28
Y_STEPS = -3.57

# ---------------------------------------------------------------------------
# Math model
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class FiveNumberResult:
    ordered: tuple[float, ...]
    lower: tuple[float, ...]
    upper: tuple[float, ...]
    minimum: float
    q1: float
    q2: float
    q3: float
    maximum: float

    @property
    def five(self):
        return (self.minimum, self.q1, self.q2, self.q3, self.maximum)

    @property
    def iqr(self):
        return self.q3 - self.q1

    @property
    def data_range(self):
        return self.maximum - self.minimum


def five_number_summary(values: tuple[float, ...]) -> FiveNumberResult:
    ordered = tuple(sorted(values))
    n = len(ordered)
    if n < 5:
        raise ValueError("Need at least five values for this workshop.")
    if n % 2:
        mid = n // 2
        q2 = float(ordered[mid])
        lower = ordered[:mid]
        upper = ordered[mid + 1 :]
    else:
        mid = n // 2
        q2 = (ordered[mid - 1] + ordered[mid]) / 2
        lower = ordered[:mid]
        upper = ordered[mid:]
    q1 = float(median(lower))
    q3 = float(median(upper))
    return FiveNumberResult(
        ordered=ordered,
        lower=tuple(lower),
        upper=tuple(upper),
        minimum=float(ordered[0]),
        q1=q1,
        q2=q2,
        q3=q3,
        maximum=float(ordered[-1]),
    )


def fmt(v: float) -> str:
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:.2f}".rstrip("0").rstrip(".")


class Statistics10Week5FiveNumberSummaryWorkshopSenior(Scene):
    STEP_NAMES = (
        "ORDER", "MIN / MAX", "FIND Q2", "SPLIT",
        "FIND Q1", "FIND Q3", "WRITE 5-NUM", "INTERPRET",
    )

    P1 = (14, 5, 20, 8, 16, 11, 7, 18, 10)
    P2 = (18, 2, 15, 24, 9, 13, 20, 7, 11, 5)
    P3 = (7, 3, 9, 4, 12, 7, 4, 9, 6)
    P4 = (2.4, 1.2, 2.9, 1.8, 2.1, 1.4, 2.6, 1.6)
    P8 = (6, -2, 9, 3, 3, 12, 0, 7, 5, 10, 1)

    THEORY_A = (13, 4, 18, 9, 21, 12, 7, 16, 10)
    THEORY_B = (18, 3, 13, 22, 7, 11, 20, 8, 14, 5)

    def setup(self):
        super().setup()
        self.camera.background_color = WHITE
        self.header = None
        self.step_strip = None
        self.r1 = five_number_summary(self.P1)
        self.r2 = five_number_summary(self.P2)
        self.r3 = five_number_summary(self.P3)
        self.r4 = five_number_summary(self.P4)
        self.r8 = five_number_summary(self.P8)
        self.ra = five_number_summary(self.THEORY_A)
        self.rb = five_number_summary(self.THEORY_B)
        self._validate()

    def _validate(self):
        assert self.r1.five == (5.0, 7.5, 11.0, 17.0, 20.0)
        assert self.r2.five == (2.0, 7.0, 12.0, 18.0, 24.0)
        assert self.r3.five == (3.0, 4.0, 7.0, 9.0, 12.0)
        assert self.r4.five == (1.2, 1.5, 1.95, 2.5, 2.9)
        assert self.r8.five == (-2.0, 1.0, 5.0, 9.0, 12.0)
        assert self.ra.five == (4.0, 8.0, 12.0, 17.0, 21.0)
        assert self.rb.five == (3.0, 7.0, 12.0, 18.0, 22.0)
        assert self.ra.q2 == self.rb.q2 == 12
        assert self.ra.iqr == 9 and self.rb.iqr == 11

    def t(self, content, size=28, weight=NORMAL, color=INK, **kwargs):
        return Text(content, font_size=size, weight=weight, color=color,
                    line_spacing=0.92, **kwargs)

    def m(self, expr, size=40, color=INK, **kwargs):
        return MathTex(expr, font_size=size, color=color, **kwargs)

    def fit(self, mob, w=SAFE_W, h=5.65):
        if mob.width > w:
            mob.scale_to_fit_width(w)
        if mob.height > h:
            mob.scale_to_fit_height(h)
        return mob

    def panel(self, width, height, fill=PAPER, stroke=LIGHT, sw=1.5):
        return RoundedRectangle(width=width, height=height, corner_radius=0.12,
                                stroke_color=stroke, stroke_width=sw,
                                fill_color=fill, fill_opacity=1)

    def note(self, text, width=11.2, height=0.84, size=24, fill=VERY_LIGHT):
        box = self.panel(width, height, fill=fill)
        tx = self.t(text, size, NORMAL, color=DARK)
        self.fit(tx, w=width - 0.48, h=height - 0.18)
        tx.move_to(box)
        return VGroup(box, tx)

    def formula_panel(self, tex, width=6.0, height=0.94, size=38):
        box = self.panel(width, height, fill=WHITE, stroke=DARK, sw=1.6)
        eq = self.m(tex, size)
        self.fit(eq, w=width - 0.52, h=height - 0.20)
        eq.move_to(box)
        return VGroup(box, eq)

    def set_header(self, section, subtitle):
        if self.header is not None and self.header in self.mobjects:
            self.remove(self.header)
        label = self.t(section, 23, BOLD, color=DARK).to_edge(UL, buff=0.42)
        available = 14.85 - label.width - 0.38
        sub = self.t(subtitle, 24, NORMAL, color=MID)
        if sub.width > available:
            sub.scale_to_fit_width(max(available, 4.0))
        sub.next_to(label, RIGHT, buff=0.34)
        line = Line(LEFT * 7.55, RIGHT * 7.55, color=LIGHT, stroke_width=1.6)
        line.next_to(label, DOWN, buff=0.20).align_to(label, LEFT)
        self.header = VGroup(label, sub, line)
        self.add(self.header)

    def clear_stage(self, keep_header=True, keep_steps=False):
        keep = set()
        if keep_header and self.header is not None:
            keep.add(self.header)
        if keep_steps and self.step_strip is not None:
            keep.add(self.step_strip)
        removable = [mob for mob in self.mobjects if mob not in keep]
        if removable:
            self.play(*[FadeOut(mob) for mob in removable], run_time=RUN_FAST)
        if keep_header and self.header is not None and self.header not in self.mobjects:
            self.add(self.header)
        if keep_steps and self.step_strip is not None and self.step_strip not in self.mobjects:
            self.add(self.step_strip)

    def build_step_strip(self, active=1):
        widths = (1.42, 1.72, 1.48, 1.30, 1.48, 1.48, 1.84, 1.70)
        cells = VGroup()
        for i, (name, width) in enumerate(zip(self.STEP_NAMES, widths), 1):
            box = RoundedRectangle(
                width=width, height=0.72, corner_radius=0.08,
                stroke_color=DARK if i == active else LIGHT,
                stroke_width=2.4 if i == active else 1.05,
                fill_color="#EAEAEA" if i == active else WHITE,
                fill_opacity=1,
            )
            num = self.t(str(i), 18, BOLD, color=DARK)
            lab = self.t(name, 14.2, BOLD if i == active else NORMAL,
                         color=DARK if i == active else MID)
            content = VGroup(num, lab).arrange(RIGHT, buff=0.075)
            self.fit(content, w=width - 0.16, h=0.40)
            content.move_to(box)
            cells.add(VGroup(box, content))
        strip = cells.arrange(RIGHT, buff=0.06)
        if strip.width > 14.82:
            strip.scale_to_fit_width(14.82)
        strip.move_to([0, Y_STEPS, 0])
        return strip

    def set_step(self, active):
        new = self.build_step_strip(active)
        if self.step_strip is None or self.step_strip not in self.mobjects:
            self.step_strip = new
            self.play(FadeIn(new), run_time=RUN_FAST)
        else:
            self.play(Transform(self.step_strip, new), run_time=RUN_FAST)

    def data_cards(self, values, y=Y_DATA, max_width=13.2, show_indices=True):
        values = tuple(values)
        n = len(values)
        card_w = min(0.98, (max_width - 0.11 * (n - 1)) / n)
        cards = VGroup()
        for i, value in enumerate(values, 1):
            box = RoundedRectangle(width=card_w, height=0.70, corner_radius=0.075,
                                   stroke_color=DARK, stroke_width=1.35,
                                   fill_color=WHITE, fill_opacity=1)
            val = self.t(fmt(value), 23, BOLD, color=DARK).move_to(box)
            if show_indices:
                idx = self.t(str(i), 13.2, NORMAL, color=MID).next_to(box, DOWN, buff=0.065)
                cards.add(VGroup(box, val, idx))
            else:
                cards.add(VGroup(box, val))
        cards.arrange(RIGHT, buff=0.11)
        if cards.width > max_width:
            cards.scale_to_fit_width(max_width)
        cards.move_to([0, y, 0])
        return cards

    def labeled_row(self, label, values, y):
        lab = self.t(label, 19, BOLD, color=MID)
        row = self.data_cards(values, y=0, max_width=10.5, show_indices=False)
        group = VGroup(lab, row).arrange(RIGHT, buff=0.30)
        self.fit(group, w=13.4, h=0.82)
        group.move_to([0, y, 0])
        return group

    def summary_panel(self, result, y=Y_RESULT):
        expr = rf"\left({fmt(result.minimum)},\ {fmt(result.q1)},\ {fmt(result.q2)},\ {fmt(result.q3)},\ {fmt(result.maximum)}\right)"
        box = self.panel(12.5, 1.02, fill=WHITE, stroke=DARK, sw=1.8)
        lab = self.t("FIVE-NUMBER SUMMARY", 19.5, BOLD, color=MID)
        eq = self.m(expr, 39)
        g = VGroup(lab, eq).arrange(RIGHT, buff=0.34)
        self.fit(g, w=12.0, h=0.75)
        g.move_to(box)
        return VGroup(box, g).move_to([0, y, 0])

    def quartile_formula(self, symbol, pair, result, x, y=Y_CALC):
        a, b = pair
        tex = rf"{symbol}={fmt(result)}" if abs(a-b) < 1e-9 else rf"{symbol}=\frac{{{fmt(a)}+{fmt(b)}}}{{2}}={fmt(result)}"
        return self.formula_panel(tex, 5.75, 0.92, 36).move_to([x, y, 0])

    def middle_pair(self, values):
        n = len(values)
        if n % 2:
            return (values[n//2], values[n//2])
        return (values[n//2-1], values[n//2])

    def attempt_card(self, text="TRY IT FIRST · Use the 8-step route"):
        return self.note(text, 10.6, 0.86, 24).move_to([0, 0.70, 0])

    def opening(self):
        title = self.t("STATISTICS 10 · WEEK 5", 31, BOLD, color=DARK)
        subtitle = self.t("FIVE-NUMBER SUMMARY · WORKSHOP", 43, BOLD)
        line = self.t("Different cases · same disciplined 8-step method", 27, NORMAL, color=MID)
        g = VGroup(title, subtitle, line).arrange(DOWN, buff=0.30).move_to(UP*0.55)
        self.play(FadeIn(title), Write(subtitle), run_time=RUN_SLOW)
        self.play(FadeIn(line), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(g), run_time=RUN_FAST)

        self.set_header("WORKSHOP MAP", "8 PROBLEMS · 8 DIFFERENT DECISIONS")
        labels = (
            "1 · odd n", "2 · even n", "3 · repeated", "4 · decimals",
            "5 · error analysis", "6 · compare spread", "7 · reverse", "8 · challenge",
        )
        cards = VGroup()
        for i, lab in enumerate(labels):
            box = self.panel(3.25, 1.05, fill=WHITE if i%2==0 else PAPER)
            tx = self.t(lab, 21, BOLD if i in (4,7) else NORMAL, color=DARK)
            self.fit(tx, w=2.90, h=0.68); tx.move_to(box)
            cards.add(VGroup(box, tx))
        grid = VGroup(
            VGroup(*cards[:4]).arrange(RIGHT, buff=0.18),
            VGroup(*cards[4:]).arrange(RIGHT, buff=0.18),
        ).arrange(DOWN, buff=0.25).move_to([0, 0.10, 0])
        self.play(LaggedStart(*[FadeIn(c) for row in grid for c in row], lag_ratio=0.06), run_time=RUN_SLOW)
        footer = self.note("Rule: do not interpret until the five numbers have been constructed correctly.", 12.6, 0.82, 23).move_to([0,-2.15,0])
        self.play(FadeIn(footer), run_time=RUN)
        self.wait(PAUSE_READ)
        self.clear_stage()

    def solve_problem(self, number, subtitle, raw, result, interpretation, challenge=False):
        self.set_header(f"PROBLEM {number}", subtitle)
        self.step_strip = None
        raw_lab = self.t("RAW DATA", 20, BOLD, color=MID).move_to([-6.55, 2.45, 0])
        raw_cards = self.data_cards(raw, y=2.15, max_width=12.5, show_indices=False)
        self.play(FadeIn(raw_lab), LaggedStart(*[FadeIn(c) for c in raw_cards], lag_ratio=0.045), run_time=RUN_SLOW)
        prompt_text = "FINAL CHALLENGE · Solve before the reveal" if challenge else "TRY IT FIRST · Build the complete five-number summary"
        prompt = self.attempt_card(prompt_text)
        self.play(FadeIn(prompt), run_time=RUN)
        self.wait(PAUSE_WORK + (0.9 if challenge else 0))
        self.play(FadeOut(prompt), FadeOut(raw_lab), FadeOut(raw_cards), run_time=RUN_FAST)

        self.set_step(1)
        ordered_lab = self.t("ORDERED DATA", 19, BOLD, color=MID).move_to([-6.35, 2.72, 0])
        ordered = self.data_cards(result.ordered, y=2.25, max_width=12.8, show_indices=True)
        self.play(FadeIn(ordered_lab), LaggedStart(*[FadeIn(c) for c in ordered], lag_ratio=0.045), run_time=RUN_SLOW)
        self.wait(0.62)

        self.set_step(2)
        minp = self.formula_panel(rf"\min={fmt(result.minimum)}", 3.15, 0.90, 35).move_to([-3.55, Y_META, 0])
        maxp = self.formula_panel(rf"\max={fmt(result.maximum)}", 3.15, 0.90, 35).move_to([3.55, Y_META, 0])
        self.play(FadeIn(minp), FadeIn(maxp), run_time=RUN)
        self.wait(0.55)

        self.set_step(3)
        self.play(FadeOut(minp), FadeOut(maxp), run_time=RUN_FAST)
        n = len(result.ordered)
        if n % 2:
            q2tex = rf"Q_2=x_{{{n//2+1}}}={fmt(result.q2)}"
        else:
            a, b = result.ordered[n//2-1], result.ordered[n//2]
            q2tex = rf"Q_2=\frac{{{fmt(a)}+{fmt(b)}}}{{2}}={fmt(result.q2)}"
        q2p = self.formula_panel(q2tex, 6.6, 0.96, 37).move_to([0, Y_META, 0])
        self.play(FadeIn(q2p), run_time=RUN)
        self.wait(0.72)

        self.set_step(4)
        self.play(FadeOut(q2p), run_time=RUN_FAST)
        lower = self.labeled_row("LOWER", result.lower, Y_LOWER)
        upper = self.labeled_row("UPPER", result.upper, Y_UPPER)
        split_note = self.t("Exclude Q2 when n is odd" if n%2 else "Even n: split evenly", 18.5, BOLD, color=MID).move_to([0, 1.28, 0])
        self.play(FadeIn(split_note), FadeIn(lower), FadeIn(upper), run_time=RUN_SLOW)
        self.wait(0.70)

        self.set_step(5)
        q1pair = self.middle_pair(result.lower)
        q1p = self.quartile_formula("Q_1", q1pair, result.q1, -3.25)
        self.play(FadeIn(q1p), run_time=RUN)
        self.wait(0.60)

        self.set_step(6)
        q3pair = self.middle_pair(result.upper)
        q3p = self.quartile_formula("Q_3", q3pair, result.q3, 3.25)
        self.play(FadeIn(q3p), run_time=RUN)
        self.wait(0.65)

        self.set_step(7)
        self.play(FadeOut(split_note), FadeOut(lower), FadeOut(upper), FadeOut(q1p), FadeOut(q3p), run_time=RUN_FAST)
        summary = self.summary_panel(result)
        self.play(FadeIn(summary), run_time=RUN)
        self.wait(0.78)

        self.set_step(8)
        interpretation_full = f"{interpretation}  IQR = {fmt(result.iqr)}; range = {fmt(result.data_range)}."
        interp = self.note(interpretation_full, 12.8, 0.98, 22.5, fill=WHITE).move_to([0, Y_RESULT, 0])
        self.play(Transform(summary, interp), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage(keep_header=False, keep_steps=False)
        self.header = None
        self.step_strip = None

    def error_analysis(self):
        result = self.r1
        self.set_header("PROBLEM 5", "ERROR ANALYSIS · SHOULD Q2 BE INCLUDED IN BOTH HALVES?")
        self.step_strip = None
        ordered = self.data_cards(result.ordered, y=2.25, max_width=12.4, show_indices=True)
        self.play(FadeIn(ordered), run_time=RUN_SLOW)
        prompt = self.attempt_card("Find the student's mistake before the correction appears")
        self.play(FadeIn(prompt)); self.wait(PAUSE_WORK); self.play(FadeOut(prompt), run_time=RUN_FAST)
        self.set_step(3)
        q2 = self.formula_panel(r"Q_2=11", 4.4, 0.92, 38).move_to([0,1.08,0])
        self.play(FadeIn(q2), run_time=RUN)
        self.set_step(4)
        wrong_l = self.labeled_row("WRONG LOWER", (5,7,8,10,11), 0.40)
        wrong_u = self.labeled_row("WRONG UPPER", (11,14,16,18,20), -0.42)
        self.play(FadeOut(q2), FadeIn(wrong_l), FadeIn(wrong_u), run_time=RUN_SLOW)
        wrong = self.note("Mistake: Q2 = 11 was included in BOTH halves.", 11.8, 0.82, 24).move_to([0,-1.55,0])
        self.play(FadeIn(wrong), run_time=RUN); self.wait(0.9)
        self.set_step(5)
        correct_l = self.labeled_row("CORRECT LOWER", result.lower, 0.40)
        correct_u = self.labeled_row("CORRECT UPPER", result.upper, -0.42)
        self.play(Transform(wrong_l, correct_l), Transform(wrong_u, correct_u), FadeOut(wrong), run_time=RUN_SLOW)
        q1 = self.quartile_formula("Q_1", self.middle_pair(result.lower), result.q1, -3.25)
        self.play(FadeIn(q1), run_time=RUN)
        self.set_step(6)
        q3 = self.quartile_formula("Q_3", self.middle_pair(result.upper), result.q3, 3.25)
        self.play(FadeIn(q3), run_time=RUN)
        self.set_step(7)
        self.play(FadeOut(wrong_l), FadeOut(wrong_u), FadeOut(q1), FadeOut(q3), run_time=RUN_FAST)
        summary = self.summary_panel(result)
        self.play(FadeIn(summary), run_time=RUN)
        self.set_step(8)
        final = self.note("Odd n rule: remove the median before finding Q1 and Q3. Correct summary: (5, 7.5, 11, 17, 20).", 12.9, 0.98, 22).move_to([0,Y_RESULT,0])
        self.play(Transform(summary, final), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage(keep_header=False); self.header=None; self.step_strip=None

    def compare_spread(self):
        self.set_header("PROBLEM 6", "COMPARE TWO SUMMARIES · SAME MEDIAN ≠ SAME SPREAD")
        a = self.ra; b = self.rb
        prompt = self.note("Both datasets have Q2 = 12. Which distribution is more spread out? Justify with IQR and range.", 13.0, 0.92, 23).move_to([0,2.25,0])
        self.play(FadeIn(prompt)); self.wait(PAUSE_WORK)
        card_a = self.panel(6.35, 2.25, fill=WHITE, stroke=DARK, sw=1.5).move_to([-3.35,0.35,0])
        card_b = self.panel(6.35, 2.25, fill=WHITE, stroke=DARK, sw=1.5).move_to([3.35,0.35,0])
        ta = VGroup(self.t("DATASET A", 23, BOLD, color=DARK), self.m(r"(4,8,12,17,21)", 34), self.t("IQR = 17 - 8 = 9", 22, NORMAL, color=MID), self.t("Range = 21 - 4 = 17", 22, NORMAL, color=MID)).arrange(DOWN, buff=0.16)
        self.fit(ta,w=5.8,h=1.78); ta.move_to(card_a)
        tb = VGroup(self.t("DATASET B", 23, BOLD, color=DARK), self.m(r"(3,7,12,18,22)", 34), self.t("IQR = 18 - 7 = 11", 22, NORMAL, color=MID), self.t("Range = 22 - 3 = 19", 22, NORMAL, color=MID)).arrange(DOWN, buff=0.16)
        self.fit(tb,w=5.8,h=1.78); tb.move_to(card_b)
        self.play(FadeOut(prompt), FadeIn(VGroup(card_a,ta)), FadeIn(VGroup(card_b,tb)), run_time=RUN_SLOW)
        conclusion = self.note("Dataset B is more spread out: it has the larger IQR (11) and the larger range (19).", 12.5, 0.92, 23).move_to([0,-1.85,0])
        self.play(FadeIn(conclusion), run_time=RUN)
        rule = self.t("Median describes center; IQR and range describe spread.", 22, BOLD, color=DARK).move_to([0,-2.65,0])
        self.play(FadeIn(rule), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage(keep_header=False); self.header=None

    def reverse_reasoning(self):
        self.set_header("PROBLEM 7", "REVERSE REASONING · FIND THE MISSING VALUE")
        ordered = (4,7,9,12,"x",18,21,24,28)
        cards = VGroup()
        for i,v in enumerate(ordered,1):
            box = RoundedRectangle(width=0.98,height=0.70,corner_radius=0.075,stroke_color=DARK,stroke_width=1.35,fill_color=WHITE,fill_opacity=1)
            val = self.t(str(v),23,BOLD,color=DARK).move_to(box)
            idx = self.t(str(i),13.2,NORMAL,color=MID).next_to(box,DOWN,buff=0.065)
            cards.add(VGroup(box,val,idx))
        cards.arrange(RIGHT,buff=0.11).move_to([0,2.20,0])
        given = self.formula_panel(r"(\min,Q_1,Q_2,Q_3,\max)=(4,8,15,22.5,28)", 10.9, 0.98, 36).move_to([0,0.85,0])
        self.play(FadeIn(cards), FadeIn(given), run_time=RUN_SLOW)
        prompt = self.note("What must x be? Then verify Q1 and Q3.", 9.2, 0.82, 24).move_to([0,-0.35,0])
        self.play(FadeIn(prompt)); self.wait(PAUSE_WORK)
        arrow = Arrow(cards[4][0].get_bottom(), [0,-0.95,0], color=DARK, stroke_width=2.1, buff=0.08)
        q2 = self.formula_panel(r"Q_2=x_5=15\quad\Rightarrow\quad x=15", 7.2, 0.94, 37).move_to([0,-1.35,0])
        self.play(FadeOut(prompt), GrowArrow(arrow), FadeIn(q2), run_time=RUN_SLOW)
        verify = self.note("Check: Q1 = (7+9)/2 = 8 and Q3 = (21+24)/2 = 22.5. The given summary is consistent.", 12.9, 0.88, 22).move_to([0,-2.35,0])
        self.play(FadeIn(verify), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage(keep_header=False); self.header=None

    def closing(self):
        self.set_header("WORKSHOP COMPLETE", "READY FOR WEEK 6 · BOX-AND-WHISKER PLOT")
        title = self.t("A five-number summary is a construction, not a guess.", 31, BOLD, color=DARK).move_to([0,2.25,0])
        self.play(FadeIn(title), run_time=RUN)
        rows = VGroup(self.note("1–2 · organize the data and lock the endpoints", 6.25, 0.80, 22), self.note("3–4 · locate Q2 and split correctly", 6.25, 0.80, 22), self.note("5–6 · compute Q1 and Q3 from the halves", 6.25, 0.80, 22), self.note("7–8 · write the five numbers and interpret spread", 6.25, 0.80, 22)).arrange(DOWN,buff=0.14).move_to([-3.35,0.10,0])
        preview_box = self.panel(6.1,3.65,fill=WHITE,stroke=DARK,sw=1.6).move_to([3.55,0.10,0])
        five = self.m(r"\min\;|\;Q_1\;|\;Q_2\;|\;Q_3\;|\;\max", 37).move_to([3.55,0.82,0])
        arrow = Arrow([3.55,0.35,0],[3.55,-0.35,0],color=DARK,stroke_width=2.2,buff=0.06)
        next_text = self.t("Week 6: turn these five landmarks\ninto the geometry of a box plot.", 24, BOLD, color=DARK, line_spacing=0.9)
        self.fit(next_text,w=5.3,h=1.10); next_text.move_to([3.55,-1.08,0])
        self.play(LaggedStart(*[FadeIn(r) for r in rows],lag_ratio=0.10), FadeIn(preview_box), run_time=RUN_SLOW)
        self.play(FadeIn(five), GrowArrow(arrow), FadeIn(next_text), run_time=RUN_SLOW)
        self.wait(PAUSE_FINAL)

    def construct(self):
        self.opening()
        self.solve_problem(1, "ODD n · EXCLUDE THE MEDIAN", self.P1, self.r1, "Q2 is the center; the middle 50% runs from 7.5 to 17.")
        self.solve_problem(2, "EVEN n · MEDIAN FROM TWO CENTRAL VALUES", self.P2, self.r2, "The center is 12; half of the central data lie between 7 and 18.")
        self.solve_problem(3, "REPEATED VALUES · KEEP EVERY OBSERVATION", self.P3, self.r3, "Repeated values remain in the ordered list; they still affect positions.")
        self.solve_problem(4, "DECIMAL MEASUREMENTS · KEEP PRECISION", self.P4, self.r4, "The summary preserves measurement precision; Q2 = 1.95 is a valid midpoint.")
        self.error_analysis()
        self.compare_spread()
        self.reverse_reasoning()
        self.solve_problem(8, "FINAL CHALLENGE · NEGATIVES + REPEATED VALUES", self.P8, self.r8, "The method is unchanged with negative or repeated data.", challenge=True)
        self.closing()
