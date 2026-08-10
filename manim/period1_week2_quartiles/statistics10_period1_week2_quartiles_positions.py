#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statistics 10 · Period 1 · Week 2 — Quartiles: Ordering & Position.

Full theory + worked-exercise lesson, designed as the direct continuation of
Week 1 IQR recovery. The lesson deliberately keeps the same classroom
quartile convention used in Week 1:

- Always order the observations first.
- If n is odd, Q2 is the central observation and is excluded before splitting.
- If n is even, Q2 is the mean of the two central observations.
- Q1 is the median of the lower half.
- Q3 is the median of the upper half.
- Repeated values remain in the ordered list.

The formal percentile/interpolation formulas are intentionally not introduced
here because Week 3 is reserved for deciles and percentiles.

Target: Manim Community Edition 0.20.x, 1920x1080, 30 fps, white classroom
style. Render final with literal `-pqh` following the supplied protocol.
"""
from __future__ import annotations

from dataclasses import dataclass
from statistics import median
from typing import Sequence

from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

INK = BLACK
DARK = "#303030"
MID = "#787878"
LIGHT = "#D7D7D7"
VERY_LIGHT = "#F0F0F0"
PAPER = "#F8F8F8"
WHITE_FILL = WHITE
SAFE_W = 14.65

RUN_FAST = 0.55
RUN = 0.85
RUN_SLOW = 1.15
PAUSE_READ = 1.35
PAUSE_EXPLAIN = 2.15
PAUSE_WORK = 3.4
PAUSE_SUMMARY = 3.8


@dataclass(frozen=True)
class QuartileSolution:
    raw: tuple[float, ...]
    ordered: tuple[float, ...]
    lower: tuple[float, ...]
    upper: tuple[float, ...]
    q1: float
    q2: float
    q3: float


def course_quartiles(values: Sequence[float]) -> QuartileSolution:
    if len(values) < 4:
        raise ValueError("At least four observations are required.")
    ordered = tuple(sorted(float(v) for v in values))
    n = len(ordered)
    q2 = float(median(ordered))
    if n % 2:
        mid = n // 2
        lower = ordered[:mid]
        upper = ordered[mid + 1 :]
    else:
        mid = n // 2
        lower = ordered[:mid]
        upper = ordered[mid:]
    return QuartileSolution(
        raw=tuple(float(v) for v in values),
        ordered=ordered,
        lower=tuple(lower),
        upper=tuple(upper),
        q1=float(median(lower)),
        q2=q2,
        q3=float(median(upper)),
    )


def fmt(v: float) -> str:
    return str(int(v)) if abs(v - round(v)) < 1e-9 else f"{v:g}"


class Statistics10Period1Week2QuartilesPositions(MovingCameraScene):
    STEP_NAMES = (
        "ORDER",
        "COUNT n",
        "FIND Q2",
        "SPLIT",
        "FIND Q1",
        "FIND Q3",
        "CHECK",
        "INTERPRET",
    )

    def setup(self):
        super().setup()
        self.camera.background_color = WHITE
        self.camera.frame.set(width=16).move_to(ORIGIN)
        self.header = None
        self.step_strip = None
        self._validate_lesson_data()

    def _validate_lesson_data(self):
        odd = course_quartiles((14, 8, 11, 5, 9, 16, 7, 13, 10))
        assert odd.ordered == (5, 7, 8, 9, 10, 11, 13, 14, 16)
        assert (odd.q1, odd.q2, odd.q3) == (7.5, 10.0, 13.5)
        even = course_quartiles((18, 6, 14, 4, 12, 16, 8, 10))
        assert even.ordered == (4, 6, 8, 10, 12, 14, 16, 18)
        assert (even.q1, even.q2, even.q3) == (7.0, 11.0, 15.0)
        repeated = course_quartiles((10, 5, 14, 8, 5, 12, 10, 8))
        assert repeated.ordered == (5, 5, 8, 8, 10, 10, 12, 14)
        assert (repeated.q1, repeated.q2, repeated.q3) == (6.5, 9.0, 11.0)
        ex_a = course_quartiles((15, 3, 20, 8, 11, 6, 13))
        assert (ex_a.q1, ex_a.q2, ex_a.q3) == (6.0, 11.0, 15.0)
        ex_b = course_quartiles((12, 2, 18, 7, 9, 4))
        assert (ex_b.q1, ex_b.q2, ex_b.q3) == (4.0, 8.0, 12.0)

    def t(self, content, size=30, weight=NORMAL, color=INK, **kwargs):
        return Text(
            content,
            font_size=size,
            color=color,
            weight=weight,
            line_spacing=0.92,
            **kwargs,
        )

    def m(self, expr, size=40, color=INK, **kwargs):
        return MathTex(expr, font_size=size, color=color, **kwargs)

    def fit(self, mob, w=SAFE_W, h=5.75):
        if mob.width > w:
            mob.scale_to_fit_width(w)
        if mob.height > h:
            mob.scale_to_fit_height(h)
        return mob

    def panel(self, width, height, fill=PAPER, stroke=LIGHT):
        return RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=stroke,
            stroke_width=1.6,
            fill_color=fill,
            fill_opacity=1,
        )

    def set_header(self, section, subtitle):
        if self.header is not None:
            self.remove(self.header)
        label = self.t(section, 24, BOLD, color=DARK).to_edge(UL, buff=0.42)
        sub = self.t(subtitle, 25, NORMAL, color=MID).next_to(label, RIGHT, buff=0.36)
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

    def note(self, text, width=10.8, height=0.82, size=26):
        box = self.panel(width, height, fill=VERY_LIGHT, stroke=LIGHT)
        tx = self.t(text, size, NORMAL, color=DARK)
        self.fit(tx, w=width - 0.45, h=height - 0.18)
        tx.move_to(box)
        return VGroup(box, tx)

    def value_card(self, value, width=0.86, height=0.72):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.09,
            stroke_color=DARK,
            stroke_width=1.6,
            fill_color=WHITE_FILL,
            fill_opacity=1,
        )
        tx = self.t(fmt(value), 28, BOLD).move_to(box)
        return VGroup(box, tx)

    def data_row(self, values, y, label=None, max_width=12.8):
        cards = VGroup(*[self.value_card(v) for v in values]).arrange(RIGHT, buff=0.13)
        if cards.width > max_width:
            cards.scale_to_fit_width(max_width)
        cards.move_to([0.65 if label else 0, y, 0])
        if label:
            lab = self.t(label, 24, BOLD, color=MID).next_to(cards, LEFT, buff=0.30)
            return VGroup(lab, cards)
        return cards

    def indexed_row(self, values, y=0.35):
        cards = VGroup(*[self.value_card(v, width=0.88, height=0.70) for v in values]).arrange(RIGHT, buff=0.12)
        if cards.width > 12.0:
            cards.scale_to_fit_width(12.0)
        cards.move_to([0, y, 0])
        indices = VGroup()
        for i, card in enumerate(cards, start=1):
            indices.add(self.t(str(i), 20, NORMAL, color=MID).next_to(card, DOWN, buff=0.16))
        caption = self.t("position", 20, NORMAL, color=MID).next_to(indices, LEFT, buff=0.28)
        return VGroup(cards, indices, caption)

    def build_step_strip(self, active=None):
        chips = VGroup()
        for i, name in enumerate(self.STEP_NAMES, start=1):
            is_active = active == i
            rect = RoundedRectangle(
                width=1.67,
                height=0.52,
                corner_radius=0.08,
                stroke_color=INK if is_active else LIGHT,
                stroke_width=2.2 if is_active else 1.2,
                fill_color=VERY_LIGHT if is_active else WHITE,
                fill_opacity=1,
            )
            n = self.t(str(i), 18, BOLD, color=INK if is_active else MID)
            nm = self.t(name, 15, BOLD, color=INK if is_active else MID)
            chips.add(VGroup(rect, VGroup(n, nm).arrange(RIGHT, buff=0.09).move_to(rect)))
        chips.arrange(RIGHT, buff=0.10)
        chips.scale_to_fit_width(14.35)
        chips.to_edge(DOWN, buff=0.32)
        return chips

    def set_active_step(self, step):
        new = self.build_step_strip(step)
        if self.step_strip is None:
            self.step_strip = new
            self.play(FadeIn(self.step_strip), run_time=RUN_FAST)
        else:
            self.play(Transform(self.step_strip, new), run_time=RUN_FAST)

    def median_equation(self, values, result, symbol):
        vals = tuple(values)
        if len(vals) % 2:
            center = vals[len(vals) // 2]
            expr = rf"{symbol}={fmt(center)}"
        else:
            a = vals[len(vals) // 2 - 1]
            b = vals[len(vals) // 2]
            expr = rf"{symbol}=\frac{{{fmt(a)}+{fmt(b)}}}{{2}}={fmt(result)}"
        return self.m(expr, 42)

    def opening(self):
        kicker = self.t("STATISTICS 10 · PERIOD 1 · WEEK 2", 27, BOLD, color=MID)
        title = self.t("QUARTILES", 54, BOLD)
        subtitle = self.t("Ordering & Position", 36, NORMAL, color=DARK)
        line = Line(LEFT * 4.8, RIGHT * 4.8, color=LIGHT, stroke_width=2)
        target = self.t(
            "Today: locate Q1, Q2 and Q3 correctly before doing any calculation.",
            26,
            NORMAL,
            color=DARK,
        )
        group = VGroup(kicker, title, subtitle, line, target).arrange(DOWN, buff=0.28)
        self.fit(group, w=13.6, h=5.8)
        self.play(FadeIn(kicker), run_time=RUN_FAST)
        self.play(Write(title), run_time=RUN)
        self.play(FadeIn(subtitle), Create(line), run_time=RUN)
        self.play(FadeIn(target), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeOut(group), run_time=RUN_FAST)

    def scene_order_matters(self):
        self.set_header("1 · CORE IDEA", "Quartiles are positions in ordered data")
        title = self.t("The same values — two very different views", 34, BOLD).move_to([0, 2.05, 0])
        raw_values = (14, 8, 11, 5, 9, 16, 7, 13, 10)
        raw = self.data_row(raw_values, 0.85, "RAW")
        ordered = self.data_row(tuple(sorted(raw_values)), -0.55, "ORDERED")
        bad = self.note("In the raw list, position 1, 2, 3... has no statistical meaning.", 12.2).move_to([0, -1.75, 0])
        good = self.note("After ordering, positions become meaningful: low → center → high.", 12.2).move_to([0, -2.78, 0])
        self.play(Write(title), run_time=RUN)
        self.play(FadeIn(raw), run_time=RUN_SLOW)
        self.play(FadeIn(bad), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(ordered), run_time=RUN_SLOW)
        self.play(FadeIn(good), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def scene_vocabulary(self):
        self.set_header("2 · VOCABULARY", "What each quartile means")
        left_box = self.panel(6.55, 4.85).move_to([-3.55, -0.18, 0])
        right_box = self.panel(6.55, 4.85).move_to([3.55, -0.18, 0])
        left_title = self.t("POSITION LANGUAGE", 27, BOLD).next_to(left_box.get_top(), DOWN, buff=0.30)
        left_lines = VGroup(
            self.m(r"n=\text{number of observations}", 34),
            self.m(r"Q_2=\text{median}", 36),
            self.m(r"Q_1=\text{median of lower half}", 34),
            self.m(r"Q_3=\text{median of upper half}", 34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.43)
        self.fit(left_lines, w=5.8, h=3.7)
        left_lines.move_to(left_box).shift(DOWN * 0.30)
        right_title = self.t("THE RECIPE", 27, BOLD).next_to(right_box.get_top(), DOWN, buff=0.30)
        recipe = VGroup()
        for i, name in enumerate(self.STEP_NAMES, start=1):
            recipe.add(VGroup(self.t(str(i), 22, BOLD), self.t(name, 22, BOLD if i <= 6 else NORMAL, color=DARK)).arrange(RIGHT, buff=0.22))
        recipe.arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        recipe.move_to(right_box).shift(DOWN * 0.28)
        self.play(FadeIn(left_box), FadeIn(right_box), run_time=RUN)
        self.play(Write(left_title), Write(right_title), run_time=RUN)
        self.play(LaggedStart(*[FadeIn(x) for x in left_lines], lag_ratio=0.15), run_time=RUN_SLOW)
        self.play(LaggedStart(*[FadeIn(x) for x in recipe], lag_ratio=0.10), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        reminder = self.note("Do not start with a quartile formula. Start by ordering and locating positions.", 12.5).move_to([0, -3.18, 0])
        self.play(FadeIn(reminder), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def worked_case(self, section, subtitle, raw_values, case_note):
        sol = course_quartiles(raw_values)
        self.set_header(section, subtitle)
        self.step_strip = self.build_step_strip(None)
        self.add(self.step_strip)
        prompt = self.t("DATA", 24, BOLD, color=MID)
        raw = self.data_row(sol.raw, 1.63)
        prompt.next_to(raw, LEFT, buff=0.32)
        self.play(FadeIn(prompt), FadeIn(raw), run_time=RUN_SLOW)
        note = self.note(case_note, 12.6).move_to([0, 0.72, 0])
        self.play(FadeIn(note), run_time=RUN)
        self.wait(PAUSE_READ)

        self.set_active_step(1)
        ordered_row = self.indexed_row(sol.ordered, y=-0.10)
        self.play(FadeOut(note), run_time=RUN_FAST)
        self.play(FadeIn(ordered_row), run_time=RUN_SLOW)
        order_caption = self.note("STEP 1: Smallest → largest. Only now do positions mean something.", 12.2).move_to([0, -1.43, 0])
        self.play(FadeIn(order_caption), run_time=RUN)
        self.wait(PAUSE_READ)

        self.set_active_step(2)
        n_eq = self.m(rf"n={len(sol.ordered)}", 44).move_to([0, -2.35, 0])
        parity = self.t("ODD" if len(sol.ordered) % 2 else "EVEN", 25, BOLD, color=MID).next_to(n_eq, RIGHT, buff=0.35)
        self.play(Write(n_eq), FadeIn(parity), run_time=RUN)
        self.wait(PAUSE_READ)

        self.set_active_step(3)
        q2eq = self.median_equation(sol.ordered, sol.q2, "Q_2").move_to([0, -2.98, 0])
        self.play(Write(q2eq), run_time=RUN)
        cards = ordered_row[0]
        if len(sol.ordered) % 2:
            idxs = [len(sol.ordered) // 2]
        else:
            idxs = [len(sol.ordered) // 2 - 1, len(sol.ordered) // 2]
        outlines = VGroup(*[SurroundingRectangle(cards[i], color=INK, stroke_width=2.4, buff=0.06) for i in idxs])
        self.play(Create(outlines), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)

        self.set_active_step(4)
        self.play(FadeOut(order_caption), FadeOut(n_eq), FadeOut(parity), FadeOut(q2eq), FadeOut(outlines), run_time=RUN_FAST)
        lower_row = self.data_row(sol.lower, -1.55, "LOWER")
        upper_row = self.data_row(sol.upper, -2.55, "UPPER")
        self.play(FadeIn(lower_row), FadeIn(upper_row), run_time=RUN_SLOW)
        split_text = "Odd n: exclude Q2, then split the remaining observations." if len(sol.ordered) % 2 else "Even n: split into two equal halves after locating the central pair."
        split_note = self.note(split_text, 12.4).move_to([0, 0.76, 0])
        self.play(FadeIn(split_note), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)

        self.set_active_step(5)
        q1eq = self.median_equation(sol.lower, sol.q1, "Q_1").move_to([-3.25, -3.18, 0])
        self.play(Write(q1eq), run_time=RUN)
        self.wait(PAUSE_READ)

        self.set_active_step(6)
        q3eq = self.median_equation(sol.upper, sol.q3, "Q_3").move_to([3.25, -3.18, 0])
        self.play(Write(q3eq), run_time=RUN)
        self.wait(PAUSE_READ)

        self.set_active_step(7)
        check = self.m(rf"Q_1={fmt(sol.q1)}\;<\;Q_2={fmt(sol.q2)}\;<\;Q_3={fmt(sol.q3)}", 42).move_to([0, 0.74, 0])
        self.play(ReplacementTransform(split_note, check), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)

        self.set_active_step(8)
        interp = self.note(
            "Interpretation: Q1, Q2 and Q3 are landmarks near the 25%, 50% and 75% positions of the ordered data.",
            13.1,
            0.90,
            24,
        ).move_to([0, -0.80, 0])
        self.play(FadeOut(lower_row), FadeOut(upper_row), FadeOut(q1eq), FadeOut(q3eq), run_time=RUN_FAST)
        self.play(FadeIn(interp), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        summary = self.panel(7.5, 1.45, fill=VERY_LIGHT, stroke=DARK).move_to([0, -2.35, 0])
        sum_tex = self.m(rf"Q_1={fmt(sol.q1)}\qquad Q_2={fmt(sol.q2)}\qquad Q_3={fmt(sol.q3)}", 44).move_to(summary)
        self.play(FadeIn(summary), Write(sum_tex), run_time=RUN)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage(keep_header=True, keep_steps=False)
        self.step_strip = None

    def scene_repeated_values(self):
        self.set_header("5 · SPECIAL CASE", "Repeated values stay in the data")
        sol = course_quartiles((10, 5, 14, 8, 5, 12, 10, 8))
        raw = self.data_row(sol.raw, 1.45, "RAW")
        ordered = self.indexed_row(sol.ordered, y=0.10)
        self.play(FadeIn(raw), run_time=RUN_SLOW)
        self.play(FadeIn(ordered), run_time=RUN_SLOW)
        message = self.note("A repeated observation is still an observation. Never delete duplicates.", 12.4).move_to([0, -1.15, 0])
        self.play(FadeIn(message), run_time=RUN)
        cards = ordered[0]
        boxes = VGroup(*[
            SurroundingRectangle(VGroup(cards[a], cards[b]), color=MID, stroke_width=2.0, buff=0.07)
            for a, b in ((0, 1), (2, 3), (4, 5))
        ])
        self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.18), run_time=RUN_SLOW)
        result = self.m(r"Q_1=6.5\qquad Q_2=9\qquad Q_3=11", 46).move_to([0, -2.30, 0])
        self.play(Write(result), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        warn = self.note("Deleting duplicates changes n, changes positions, and therefore changes the quartiles.", 12.7).move_to([0, -3.16, 0])
        self.play(FadeIn(warn), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def mini_exercise(self, number, values):
        sol = course_quartiles(values)
        self.set_header(f"6.{number} · YOU TRY", "Use the same eight-step recipe")
        prompt = self.t(f"EXERCISE {number}", 31, BOLD)
        data = self.data_row(sol.raw, 1.20)
        task = self.t("Find Q1, Q2 and Q3. Show the ordered list and the split.", 27, NORMAL, color=DARK).move_to([0, 0.15, 0])
        timer = self.note("Pause here and solve it before the answer appears.", 10.8).move_to([0, -0.92, 0])
        self.play(FadeIn(prompt), FadeIn(data), FadeIn(task), FadeIn(timer), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.play(FadeOut(timer), FadeOut(task), run_time=RUN_FAST)
        ordered = self.data_row(sol.ordered, 0.28, "ORDERED")
        self.play(FadeIn(ordered), run_time=RUN_SLOW)
        lower = self.data_row(sol.lower, -0.80, "LOWER")
        upper = self.data_row(sol.upper, -1.72, "UPPER")
        self.play(FadeIn(lower), FadeIn(upper), run_time=RUN_SLOW)
        eq1 = self.median_equation(sol.lower, sol.q1, "Q_1")
        eq2 = self.median_equation(sol.ordered, sol.q2, "Q_2")
        eq3 = self.median_equation(sol.upper, sol.q3, "Q_3")
        eqs = VGroup(eq1, eq2, eq3).arrange(RIGHT, buff=0.65)
        self.fit(eqs, w=13.2, h=1.1)
        eqs.move_to([0, -2.82, 0])
        self.play(LaggedStart(*[Write(e) for e in eqs], lag_ratio=0.25), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        answer = self.note(
            f"Answer: Q1 = {fmt(sol.q1)}    |    Q2 = {fmt(sol.q2)}    |    Q3 = {fmt(sol.q3)}",
            11.8,
            0.82,
            27,
        ).move_to([0, -3.47, 0])
        self.play(FadeIn(answer), run_time=RUN)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    def scene_odd_even_compare(self):
        self.set_header("7 · DECISION RULE", "Odd n versus even n")
        left = self.panel(6.5, 4.75).move_to([-3.55, -0.12, 0])
        right = self.panel(6.5, 4.75).move_to([3.55, -0.12, 0])
        lt = self.t("ODD n", 31, BOLD).next_to(left.get_top(), DOWN, buff=0.34)
        rt = self.t("EVEN n", 31, BOLD).next_to(right.get_top(), DOWN, buff=0.34)
        lcontent = VGroup(
            self.t("1 central value", 26, BOLD),
            self.m(r"Q_2=\text{central value}", 34),
            self.t("Exclude Q2", 25, BOLD),
            self.t("Split what remains", 25),
            self.t("Median of each half → Q1 and Q3", 23),
        ).arrange(DOWN, buff=0.36)
        rcontent = VGroup(
            self.t("2 central values", 26, BOLD),
            self.m(r"Q_2=\frac{x_{mid1}+x_{mid2}}{2}", 34),
            self.t("Do not delete extra values", 24, BOLD),
            self.t("Split into equal halves", 25),
            self.t("Median of each half → Q1 and Q3", 23),
        ).arrange(DOWN, buff=0.36)
        self.fit(lcontent, w=5.7, h=3.65)
        self.fit(rcontent, w=5.7, h=3.65)
        lcontent.move_to(left).shift(DOWN * 0.30)
        rcontent.move_to(right).shift(DOWN * 0.30)
        self.play(FadeIn(left), FadeIn(right), Write(lt), Write(rt), run_time=RUN)
        self.play(LaggedStart(*[FadeIn(x) for x in lcontent], lag_ratio=0.14), run_time=RUN_SLOW)
        self.play(LaggedStart(*[FadeIn(x) for x in rcontent], lag_ratio=0.14), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        key = self.note("The decision is made by n — not by guessing from the values.", 11.8).move_to([0, -3.22, 0])
        self.play(FadeIn(key), run_time=RUN)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    def closing(self):
        self.set_header("8 · FINAL RECIPE", "Quartiles: ordering and position")
        title = self.t("ONE PROCEDURE — EVERY DATA SET", 35, BOLD).move_to([0, 2.00, 0])
        self.play(Write(title), run_time=RUN)
        descriptions = (
            "Order from smallest to largest.",
            "Count the observations: n.",
            "Locate the median Q2.",
            "Split into lower and upper halves.",
            "Q1 = median of the lower half.",
            "Q3 = median of the upper half.",
            "Check Q1 < Q2 < Q3 and your positions.",
            "Interpret the quartiles as ordered-data landmarks.",
        )
        rows = VGroup()
        for i, (name, desc) in enumerate(zip(self.STEP_NAMES, descriptions), start=1):
            circle = Circle(radius=0.20, stroke_color=DARK, stroke_width=1.7, fill_color=WHITE, fill_opacity=1)
            num = self.t(str(i), 17, BOLD).move_to(circle)
            tag = self.t(name, 21, BOLD)
            detail = self.t(desc, 21, NORMAL, color=DARK)
            rows.add(VGroup(VGroup(circle, num), tag, detail).arrange(RIGHT, buff=0.20))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.fit(rows, w=13.7, h=4.55)
        rows.move_to([0, -0.46, 0])
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.09), run_time=2.2)
        self.wait(PAUSE_EXPLAIN)
        final = self.note("Quartiles are positions first — calculations second.", 11.8, 0.90, 28).move_to([0, -3.23, 0])
        self.play(FadeIn(final), run_time=RUN)
        self.wait(PAUSE_SUMMARY)

    def construct(self):
        self.opening()
        self.scene_order_matters()
        self.scene_vocabulary()
        self.worked_case(
            "3 · WORKED CASE A",
            "Odd n: one central observation",
            (14, 8, 11, 5, 9, 16, 7, 13, 10),
            "n is odd: Q2 will be one exact central observation.",
        )
        self.worked_case(
            "4 · WORKED CASE B",
            "Even n: two central observations",
            (18, 6, 14, 4, 12, 16, 8, 10),
            "n is even: Q2 will be the average of the two central observations.",
        )
        self.scene_repeated_values()
        self.mini_exercise(1, (15, 3, 20, 8, 11, 6, 13))
        self.mini_exercise(2, (12, 2, 18, 7, 9, 4))
        self.scene_odd_even_compare()
        self.closing()
