#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statistics 10 · Period 1 · Week 1 — IQR worked exercises.

Continuation of the theory video `Statistics10Period1Week1IQRRecovery`.
Every worked example follows exactly the same numbered construction recipe:

1. ORDER DATA
2. FIND Q2
3. SPLIT HALVES
4. FIND Q1 & Q3
5. COMPUTE IQR
6. FIVE NUMBERS
7. DRAW BOX
8. ADD WHISKERS

Scope note: the formal 1.5·IQR outlier rule is intentionally NOT used here.
For this Week 1 recovery class, whiskers extend to the observed min and max.

Target: Manim Community Edition 0.20.x, horizontal Full HD 16:9.
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
PAPER = "#F0F0F0"
PAPER_2 = "#F8F8F8"
SAFE_W = 14.65
SAFE_H = 7.55

RUN_Q = 0.72
RUN_N = 1.00
RUN_S = 1.35
RUN_XS = 0.58
P_SHORT = 0.85
P_READ = 1.75
P_EXPLAIN = 2.65
P_WORK = 3.60
P_TRY = 5.20
P_FINAL = 4.80

STEP_TITLES = (
    "ORDER DATA",
    "FIND Q2",
    "SPLIT HALVES",
    "FIND Q1 & Q3",
    "COMPUTE IQR",
    "FIVE NUMBERS",
    "DRAW BOX",
    "ADD WHISKERS",
)

@dataclass(frozen=True)
class IQRProblem:
    number: int
    title: str
    context: str
    raw: tuple[float, ...]
    lesson_note: str

    @property
    def ordered(self) -> tuple[float, ...]:
        return tuple(sorted(self.raw))

    @property
    def n(self) -> int:
        return len(self.raw)

    @property
    def q2(self) -> float:
        return float(median(self.ordered))

    @property
    def lower(self) -> tuple[float, ...]:
        d = self.ordered
        k = len(d) // 2
        return d[:k]

    @property
    def upper(self) -> tuple[float, ...]:
        d = self.ordered
        k = len(d) // 2
        return d[k + 1 :] if len(d) % 2 else d[k:]

    @property
    def q1(self) -> float:
        return float(median(self.lower))

    @property
    def q3(self) -> float:
        return float(median(self.upper))

    @property
    def iqr(self) -> float:
        return self.q3 - self.q1

    @property
    def five(self) -> tuple[float, float, float, float, float]:
        return (
            float(min(self.ordered)),
            self.q1,
            self.q2,
            self.q3,
            float(max(self.ordered)),
        )

PROBLEMS = (
    IQRProblem(
        1,
        "ODD NUMBER OF DATA VALUES",
        "Practice the exact Week 1 recipe with n = 9.",
        (12, 5, 9, 7, 15, 6, 13, 8, 10),
        "Odd n: exclude Q2 before finding Q1 and Q3.",
    ),
    IQRProblem(
        2,
        "EVEN NUMBER OF DATA VALUES",
        "Now the median is the average of the two central observations.",
        (14, 6, 18, 10, 8, 12, 16, 20, 4, 22),
        "Even n: Q2 is the mean of the two middle values; split into equal halves.",
    ),
    IQRProblem(
        3,
        "REPEATED VALUES",
        "Repeated observations do not change the construction method.",
        (12, 4, 9, 2, 15, 7, 4, 13, 10, 9, 8, 5),
        "Repeated values are kept. Do not delete duplicates before finding quartiles.",
    ),
)

EXPECTED = {
    1: ((5, 6, 7, 8, 9, 10, 12, 13, 15), 6.5, 9.0, 12.5, 6.0, (5.0, 6.5, 9.0, 12.5, 15.0)),
    2: ((4, 6, 8, 10, 12, 14, 16, 18, 20, 22), 8.0, 13.0, 18.0, 10.0, (4.0, 8.0, 13.0, 18.0, 22.0)),
    3: ((2, 4, 4, 5, 7, 8, 9, 9, 10, 12, 13, 15), 4.5, 8.5, 11.0, 6.5, (2.0, 4.5, 8.5, 11.0, 15.0)),
}

for _p in PROBLEMS:
    exp = EXPECTED[_p.number]
    assert _p.ordered == exp[0]
    assert abs(_p.q1 - exp[1]) < 1e-12
    assert abs(_p.q2 - exp[2]) < 1e-12
    assert abs(_p.q3 - exp[3]) < 1e-12
    assert abs(_p.iqr - exp[4]) < 1e-12
    assert all(abs(a - b) < 1e-12 for a, b in zip(_p.five, exp[5]))


def fmt(v: float) -> str:
    v = float(v)
    return str(int(v)) if v.is_integer() else f"{v:.1f}"


def latex_num(v: float) -> str:
    return fmt(v)


class Statistics10Period1Week1IQRExercises(MovingCameraScene):
    """Three full worked problems following the theory's Steps 1–8 exactly."""

    def setup(self):
        super().setup()
        self.camera.background_color = WHITE
        self.camera.frame.set(width=16).move_to(ORIGIN)
        self.header = None
        self.subtitle = None
        self.step_strip = None

    def text(self, s: str, size: int = 30, weight=NORMAL, color=INK) -> Text:
        return Text(s, font_size=size, color=color, weight=weight, line_spacing=0.92)

    def math(self, s: str, size: int = 38) -> MathTex:
        return MathTex(s, font_size=size, color=INK)

    def fit(self, mob: Mobject, w: float = SAFE_W, h: float = SAFE_H) -> Mobject:
        if mob.width > w:
            mob.scale_to_fit_width(w)
        if mob.height > h:
            mob.scale_to_fit_height(h)
        return mob

    def set_header(self, section: str, title: str, subtitle: str):
        badge = RoundedRectangle(width=1.10, height=0.52, corner_radius=0.10, stroke_color=INK, stroke_width=2, fill_color=WHITE, fill_opacity=1)
        badge_text = self.text(section, 20, BOLD).move_to(badge)
        ttl = self.text(title, 32, BOLD)
        self.fit(ttl, 12.9, 0.62)
        row = VGroup(VGroup(badge, badge_text), ttl).arrange(RIGHT, buff=0.25)
        row.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.46)
        rule = Line(LEFT * 7.48, RIGHT * 7.48, color=LIGHT, stroke_width=2)
        rule.next_to(row, DOWN, buff=0.07)
        sub = self.text(subtitle, 19, NORMAL, DARK)
        self.fit(sub, 14.15, 0.66)
        sub.next_to(rule, DOWN, buff=0.07).align_to(row, LEFT)
        new_header = VGroup(row, rule)
        if self.header is None:
            self.add(new_header, sub)
        else:
            self.play(FadeOut(self.header), FadeOut(self.subtitle), run_time=RUN_Q)
            self.play(FadeIn(new_header), FadeIn(sub), run_time=RUN_Q)
        self.header, self.subtitle = new_header, sub

    def clear_content(self, keep_step_strip: bool = False):
        keep_ids = set()
        for obj in (self.header, self.subtitle):
            if obj is not None:
                keep_ids.update(id(m) for m in obj.get_family())
        if keep_step_strip and self.step_strip is not None:
            keep_ids.update(id(m) for m in self.step_strip.get_family())
        rem = [m for m in self.mobjects if id(m) not in keep_ids]
        if rem:
            self.play(*[FadeOut(m) for m in rem], run_time=RUN_Q)
        self.camera.frame.set(width=16).move_to(ORIGIN)
        if not keep_step_strip:
            self.step_strip = None

    def formula_panel(self, tex: str, width: float = 7.0, fs: int = 38) -> VGroup:
        box = RoundedRectangle(width=width, height=1.05, corner_radius=0.12, stroke_color=INK, stroke_width=1.8, fill_color=PAPER, fill_opacity=1)
        eq = self.math(tex, fs)
        self.fit(eq, width - 0.48, 0.76)
        eq.move_to(box)
        return VGroup(box, eq)

    def note_panel(self, title: str, lines: Sequence[str], width: float = 6.3) -> VGroup:
        t = self.text(title, 24, BOLD)
        body = VGroup(*[self.text(line, 21) for line in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        content = VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.fit(content, width - 0.55, 2.5)
        box = RoundedRectangle(width=width, height=max(1.15, content.height + 0.55), corner_radius=0.12, stroke_color=INK, stroke_width=1.7, fill_color=WHITE, fill_opacity=1)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.28)
        return VGroup(box, content)

    def chip(self, v: float, fill=WHITE, width: float = 0.82) -> VGroup:
        b = RoundedRectangle(width=width, height=0.62, corner_radius=0.09, stroke_color=INK, stroke_width=1.6, fill_color=fill, fill_opacity=1)
        t = self.text(fmt(v), 23, BOLD).move_to(b)
        return VGroup(b, t)

    def chips(self, vals: Sequence[float], fill=WHITE, max_width: float = 13.7) -> VGroup:
        g = VGroup(*[self.chip(v, fill) for v in vals]).arrange(RIGHT, buff=0.11)
        self.fit(g, max_width, 0.72)
        return g

    def step_badge(self, step: int, active: bool = False) -> VGroup:
        box = RoundedRectangle(width=1.63, height=0.72, corner_radius=0.10, stroke_color=INK, stroke_width=2.2 if active else 1.25, fill_color=PAPER if active else WHITE, fill_opacity=1)
        num = self.text(str(step), 20, BOLD)
        label = self.text(STEP_TITLES[step - 1], 12, BOLD if active else NORMAL, DARK)
        content = VGroup(num, label).arrange(DOWN, buff=0.02).move_to(box)
        return VGroup(box, content)

    def show_step_strip(self, active: int):
        new_strip = VGroup(*[self.step_badge(i, i == active) for i in range(1, 9)])
        new_strip.arrange(RIGHT, buff=0.10).scale(0.94)
        new_strip.to_edge(DOWN, buff=0.12)
        if self.step_strip is None:
            self.step_strip = new_strip
            self.play(FadeIn(new_strip, shift=UP * 0.04), run_time=RUN_Q)
        else:
            old = self.step_strip
            self.step_strip = new_strip
            self.play(ReplacementTransform(old, new_strip), run_time=RUN_XS)

    def step_title(self, step: int, extra: str = "") -> VGroup:
        n = self.text(f"STEP {step}", 24, BOLD)
        t = self.text(STEP_TITLES[step - 1], 31, BOLD)
        row = VGroup(n, t).arrange(RIGHT, buff=0.28)
        if extra:
            e = self.text(extra, 20, NORMAL, DARK)
            g = VGroup(row, e).arrange(DOWN, aligned_edge=LEFT, buff=0.09)
        else:
            g = row
        g.to_edge(LEFT, buff=0.65).move_to([g.get_center()[0], 2.40, 0])
        return g

    def axis(self, p: IQRProblem, y: float = -0.75):
        minv, _, _, _, maxv = p.five
        span = maxv - minv
        pad = max(1.0, span * 0.10)
        lo = minv - pad
        hi = maxv + pad
        width = 12.3
        left = -width / 2
        def xp(v: float) -> float:
            return left + (v - lo) / (hi - lo) * width
        base = Line([left, y, 0], [left + width, y, 0], color=INK, stroke_width=2.4)
        ticks = VGroup()
        labels = VGroup()
        start = int(minv) - 1
        end = int(maxv) + 1
        step = 1 if (end - start) <= 20 else 2
        for v in range(start, end + 1, step):
            x = xp(v)
            if left - 0.01 <= x <= left + width + 0.01:
                ticks.add(Line([x, y - 0.11, 0], [x, y + 0.11, 0], color=INK, stroke_width=1.5))
                labels.add(self.text(str(v), 16).move_to([x, y - 0.36, 0]))
        return VGroup(base, ticks, labels), xp

    def five_cards(self, p: IQRProblem) -> VGroup:
        labels = ("MIN", "Q1", "Q2", "Q3", "MAX")
        cards = VGroup()
        for lab, val in zip(labels, p.five):
            box = RoundedRectangle(width=2.22, height=1.42, corner_radius=0.10, stroke_color=INK, stroke_width=1.6, fill_color=WHITE, fill_opacity=1)
            content = VGroup(self.text(lab, 19, BOLD), self.text(fmt(val), 31, BOLD)).arrange(DOWN, buff=0.12).move_to(box)
            cards.add(VGroup(box, content))
        cards.arrange(RIGHT, buff=0.20)
        return cards

    def construct(self):
        self.opening()
        self.recipe_overview()
        for p in PROBLEMS:
            self.problem_prompt(p)
            self.solve_problem(p)
        self.compare_results()
        self.closing()

    def opening(self):
        top = self.text("STATISTICS 10 · PERIOD 1 · WEEK 1", 27, BOLD)
        title = self.text("IQR CONSTRUCTION · WORKED EXERCISES", 46, BOLD)
        rule = Line(LEFT * 5.8, RIGHT * 5.8, color=INK, stroke_width=2.2)
        sub = self.text("Three complete solutions using the same Steps 1–8 from the theory video", 26)
        tag = self.text("Goal: turn raw data into a correct box-and-whisker plot.", 24, MEDIUM)
        g = VGroup(top, title, rule, sub, tag).arrange(DOWN, buff=0.28)
        self.fit(g, 14.4, 6.2)
        self.play(FadeIn(top, shift=UP * 0.10), run_time=RUN_N)
        self.play(Write(title), run_time=RUN_S)
        self.play(Create(rule), FadeIn(sub), run_time=RUN_N)
        self.wait(P_EXPLAIN)
        self.play(FadeIn(tag), run_time=RUN_N)
        self.wait(P_FINAL)
        self.play(FadeOut(g), run_time=RUN_N)

    def recipe_overview(self):
        self.set_header("00", "THE SAME RECIPE FOR EVERY PROBLEM", "Do not invent a new method. Repeat the theory's eight numbered construction steps.")
        cards = VGroup()
        subtitles = (
            "smallest → largest",
            "locate the median",
            "lower / upper data",
            "medians of each half",
            "Q3 − Q1",
            "min, Q1, Q2, Q3, max",
            "box from Q1 to Q3 + median",
            "min↔Q1 and Q3↔max",
        )
        for i, (name, desc) in enumerate(zip(STEP_TITLES, subtitles), 1):
            cards.add(self.note_panel(f"{i}. {name}", [desc], 3.33))
        cards.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.26)).scale(0.93)
        cards.move_to(DOWN * 0.15)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.06) for c in cards], lag_ratio=0.07), run_time=2.0)
        self.wait(P_WORK)
        note = self.text("Week 1 rule: whiskers reach observed MIN and MAX. Outlier fences come later.", 20, BOLD)
        note.to_edge(DOWN, buff=0.16)
        self.play(FadeIn(note), run_time=RUN_N)
        self.wait(P_EXPLAIN)
        self.clear_content()

    def problem_prompt(self, p: IQRProblem):
        self.set_header(f"P{p.number}", f"PROBLEM {p.number} — {p.title}", p.context)
        prompt = self.note_panel("YOUR TASK", ["Construct the complete IQR / box-and-whisker diagram.", "Write Q1, Q2, Q3, IQR and the five-number summary.", "Use Steps 1–8 in order."], 8.2).move_to(UP * 0.90)
        raw_title = self.text("RAW DATA", 22, BOLD)
        raw = self.chips(p.raw, WHITE, 12.9)
        raw_group = VGroup(raw_title, raw).arrange(DOWN, buff=0.18).move_to(DOWN * 0.80)
        self.play(FadeIn(prompt, shift=UP * 0.08), run_time=RUN_N)
        self.play(FadeIn(raw_group), run_time=RUN_N)
        self.wait(P_READ)
        pause = self.text("PAUSE THE VIDEO AND TRY THE 8 STEPS BEFORE THE SOLUTION.", 22, BOLD)
        pause.to_edge(DOWN, buff=0.28)
        self.play(FadeIn(pause), run_time=RUN_N)
        self.wait(P_TRY)
        self.clear_content()

    def solve_problem(self, p: IQRProblem):
        self.set_header(f"P{p.number}", f"PROBLEM {p.number} — COMPLETE SOLUTION", p.lesson_note)

        self.show_step_strip(1)
        st = self.step_title(1, "Quartiles are positional: order the observations first.")
        raw = VGroup(self.text("RAW", 20, BOLD), self.chips(p.raw, WHITE, 12.8)).arrange(DOWN, buff=0.14).move_to(UP * 0.75)
        arrow = Arrow(UP * 0.10, DOWN * 0.55, color=INK, stroke_width=2.4).move_to(DOWN * 0.15)
        ordered = VGroup(self.text("ORDERED", 20, BOLD), self.chips(p.ordered, PAPER, 12.8)).arrange(DOWN, buff=0.14).move_to(DOWN * 1.18)
        self.play(FadeIn(st), FadeIn(raw), run_time=RUN_N)
        self.wait(P_READ)
        self.play(GrowArrow(arrow), run_time=RUN_N)
        self.play(FadeIn(ordered, shift=DOWN * 0.05), run_time=RUN_S)
        self.wait(P_EXPLAIN)
        self.clear_content(keep_step_strip=True)

        self.show_step_strip(2)
        st = self.step_title(2, "Locate the center of the ordered observations.")
        row = self.chips(p.ordered, PAPER, 13.0).move_to(UP * 0.62)
        positions = VGroup(*[self.text(str(i + 1), 15, NORMAL, MID).next_to(row[i], UP, buff=0.04) for i in range(p.n)])
        self.play(FadeIn(st), FadeIn(row), FadeIn(positions), run_time=RUN_N)
        self.wait(P_READ)
        if p.n % 2:
            k = p.n // 2
            row[k][0].set_fill(PAPER_2, opacity=1)
            marker = SurroundingRectangle(row[k], color=INK, buff=0.07, stroke_width=2.5)
            eq = self.formula_panel(rf"Q_2=x_{{({k+1})}}={latex_num(p.q2)}", 5.5, 40).move_to(DOWN * 0.82)
            self.play(Create(marker), FadeIn(eq), run_time=RUN_N)
        else:
            k = p.n // 2
            pair = VGroup(row[k - 1], row[k])
            marker = SurroundingRectangle(pair, color=INK, buff=0.07, stroke_width=2.5)
            a, b = p.ordered[k - 1], p.ordered[k]
            eq = self.formula_panel(rf"Q_2=\frac{{{latex_num(a)}+{latex_num(b)}}}{{2}}={latex_num(p.q2)}", 6.8, 39).move_to(DOWN * 0.82)
            self.play(Create(marker), FadeIn(eq), run_time=RUN_N)
        self.wait(P_WORK)
        self.clear_content(keep_step_strip=True)

        self.show_step_strip(3)
        st = self.step_title(3, "Create the lower half and upper half correctly.")
        row = self.chips(p.ordered, PAPER, 13.0).move_to(UP * 1.18)
        self.play(FadeIn(st), FadeIn(row), run_time=RUN_N)
        k = p.n // 2
        if p.n % 2:
            center = row[k]
            center_box = SurroundingRectangle(center, color=INK, stroke_width=2.2, buff=0.05)
            center_label = self.text("exclude Q2", 18, BOLD).next_to(center_box, UP, buff=0.07)
            self.play(Create(center_box), FadeIn(center_label), run_time=RUN_N)
            self.wait(P_EXPLAIN)
        low = VGroup(self.text("LOWER HALF", 21, BOLD), self.chips(p.lower, WHITE, 5.4)).arrange(DOWN, buff=0.14)
        high = VGroup(self.text("UPPER HALF", 21, BOLD), self.chips(p.upper, WHITE, 5.4)).arrange(DOWN, buff=0.14)
        halves = VGroup(low, high).arrange(RIGHT, buff=0.85).move_to(DOWN * 0.82)
        self.play(LaggedStart(FadeIn(low), FadeIn(high), lag_ratio=0.18), run_time=RUN_S)
        self.wait(P_WORK)
        self.clear_content(keep_step_strip=True)

        self.show_step_strip(4)
        st = self.step_title(4, "Take the median of each half.")
        low_group = VGroup(self.text("LOWER HALF", 20, BOLD), self.chips(p.lower, PAPER, 5.7)).arrange(DOWN, buff=0.14)
        high_group = VGroup(self.text("UPPER HALF", 20, BOLD), self.chips(p.upper, PAPER, 5.7)).arrange(DOWN, buff=0.14)
        halves = VGroup(low_group, high_group).arrange(RIGHT, buff=0.72).move_to(UP * 0.72)
        self.play(FadeIn(st), FadeIn(halves), run_time=RUN_N)
        q1tex = self.median_formula("Q_1", p.lower, p.q1)
        q3tex = self.median_formula("Q_3", p.upper, p.q3)
        e1 = self.formula_panel(q1tex, 6.15, 35)
        e3 = self.formula_panel(q3tex, 6.15, 35)
        VGroup(e1, e3).arrange(RIGHT, buff=0.42).move_to(DOWN * 1.03)
        self.play(LaggedStart(FadeIn(e1), FadeIn(e3), lag_ratio=0.20), run_time=RUN_S)
        self.wait(P_WORK)
        self.clear_content(keep_step_strip=True)

        self.show_step_strip(5)
        st = self.step_title(5, "Measure the width of the middle 50%.")
        eq = self.formula_panel(rf"IQR=Q_3-Q_1={latex_num(p.q3)}-{latex_num(p.q1)}={latex_num(p.iqr)}", 8.7, 42).move_to(UP * 0.55)
        meaning = self.note_panel("INTERPRETATION", [f"The middle 50% spans {fmt(p.iqr)} units.", "A larger IQR means more spread in the central half."], 7.5).move_to(DOWN * 1.20)
        self.play(FadeIn(st), run_time=RUN_N)
        self.play(FadeIn(eq), run_time=RUN_S)
        self.wait(P_EXPLAIN)
        self.play(FadeIn(meaning), run_time=RUN_N)
        self.wait(P_WORK)
        self.clear_content(keep_step_strip=True)

        self.show_step_strip(6)
        st = self.step_title(6, "These five values locate every basic part of the graph.")
        cards = self.five_cards(p).move_to(UP * 0.38)
        formula = self.formula_panel(rf"\left({latex_num(p.five[0])},\ {latex_num(p.q1)},\ {latex_num(p.q2)},\ {latex_num(p.q3)},\ {latex_num(p.five[4])}\right)", 8.6, 39).move_to(DOWN * 1.35)
        self.play(FadeIn(st), run_time=RUN_N)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.05) for c in cards], lag_ratio=0.10), run_time=RUN_S)
        self.wait(P_EXPLAIN)
        self.play(FadeIn(formula), run_time=RUN_N)
        self.wait(P_WORK)
        self.clear_content(keep_step_strip=True)

        self.show_step_strip(7)
        st = self.step_title(7, "Use one scale. Draw the box from Q1 to Q3 and place Q2 inside.")
        ax, xp = self.axis(p, y=-1.18)
        y, h = 0.28, 1.38
        mn, q1, q2, q3, mx = p.five
        x1, x2, x3 = xp(q1), xp(q2), xp(q3)
        box = Rectangle(width=x3 - x1, height=h, stroke_color=INK, stroke_width=4, fill_color=PAPER, fill_opacity=1).move_to([(x1 + x3) / 2, y, 0])
        medline = Line([x2, y - h / 2, 0], [x2, y + h / 2, 0], color=INK, stroke_width=5)
        qtags = VGroup(self.text(f"Q1 = {fmt(q1)}", 18, BOLD).next_to([x1, y + h / 2, 0], UP, buff=0.09), self.text(f"Q2 = {fmt(q2)}", 18, BOLD).next_to([x2, y + h / 2, 0], UP, buff=0.09), self.text(f"Q3 = {fmt(q3)}", 18, BOLD).next_to([x3, y + h / 2, 0], UP, buff=0.09))
        self.play(FadeIn(st), Create(ax), run_time=RUN_N)
        self.play(Create(box), run_time=RUN_S)
        self.wait(P_EXPLAIN)
        self.play(Create(medline), FadeIn(qtags), run_time=RUN_N)
        self.wait(P_WORK)
        self.clear_content(keep_step_strip=True)

        self.show_step_strip(8)
        st = self.step_title(8, "Week 1: connect the box to observed MIN and MAX.")
        ax, xp = self.axis(p, y=-1.18)
        y, h = 0.28, 1.38
        mn, q1, q2, q3, mx = p.five
        x0, x1, x2, x3, x4 = [xp(v) for v in p.five]
        box = Rectangle(width=x3 - x1, height=h, stroke_color=INK, stroke_width=4, fill_color=PAPER, fill_opacity=1).move_to([(x1 + x3) / 2, y, 0])
        medline = Line([x2, y - h / 2, 0], [x2, y + h / 2, 0], color=INK, stroke_width=5)
        lw = Line([x0, y, 0], [x1, y, 0], color=INK, stroke_width=4)
        rw = Line([x3, y, 0], [x4, y, 0], color=INK, stroke_width=4)
        lc = Line([x0, y - 0.42, 0], [x0, y + 0.42, 0], color=INK, stroke_width=4)
        rc = Line([x4, y - 0.42, 0], [x4, y + 0.42, 0], color=INK, stroke_width=4)
        five_tags = VGroup(*[VGroup(self.text(name, 15, BOLD), self.text(fmt(v), 17, BOLD)).arrange(DOWN, buff=0.01).move_to([xp(v), -2.08, 0]) for name, v in zip(("MIN", "Q1", "Q2", "Q3", "MAX"), p.five)])
        self.play(FadeIn(st), Create(ax), run_time=RUN_N)
        self.play(FadeIn(box), FadeIn(medline), run_time=RUN_N)
        self.play(Create(lw), Create(rw), Create(lc), Create(rc), run_time=RUN_S)
        self.play(LaggedStart(*[FadeIn(t) for t in five_tags], lag_ratio=0.08), run_time=RUN_N)
        self.wait(P_EXPLAIN)
        check = self.text(f"CHECK: Q1 ≤ Q2 ≤ Q3  ·  IQR = {fmt(p.iqr)}  ·  middle 50% = [{fmt(q1)}, {fmt(q3)}]", 20, BOLD).move_to(UP * 2.30)
        self.play(FadeIn(check), run_time=RUN_N)
        self.wait(P_FINAL)
        self.clear_content()

    def median_formula(self, symbol: str, values: Sequence[float], result: float) -> str:
        vals = tuple(values)
        n = len(vals)
        if n % 2:
            middle = vals[n // 2]
            return rf"{symbol}=\operatorname{{median}}={latex_num(middle)}"
        a, b = vals[n // 2 - 1], vals[n // 2]
        return rf"{symbol}=\frac{{{latex_num(a)}+{latex_num(b)}}}{{2}}={latex_num(result)}"

    def compare_results(self):
        self.set_header("CHK", "COMPARE THE THREE COMPLETED EXERCISES", "The construction recipe is identical; only the positions and arithmetic change.")
        labels = ("Problem", "Q1", "Q2", "Q3", "IQR", "Min", "Max")
        widths = (2.10, 1.30, 1.30, 1.30, 1.30, 1.30, 1.30)
        all_rows = [(labels, True)]
        for p in PROBLEMS:
            all_rows.append(((f"P{p.number}", fmt(p.q1), fmt(p.q2), fmt(p.q3), fmt(p.iqr), fmt(p.five[0]), fmt(p.five[4])), False))
        table = VGroup()
        for vals, is_header in all_rows:
            row = VGroup()
            for text_value, w in zip(vals, widths):
                cell = Rectangle(width=w, height=0.75, stroke_color=INK, stroke_width=1.4, fill_color=PAPER if is_header else WHITE, fill_opacity=1)
                txt = self.text(str(text_value), 18, BOLD if is_header else NORMAL).move_to(cell)
                row.add(VGroup(cell, txt))
            row.arrange(RIGHT, buff=0)
            table.add(row)
        table.arrange(DOWN, buff=0).move_to(UP * 0.45)
        self.play(FadeIn(table), run_time=RUN_S)
        self.wait(P_EXPLAIN)
        note = self.note_panel("WHAT CHANGED?", ["P1: odd n → exclude Q2 from the halves.", "P2: even n → Q2 is the average of two centers.", "P3: duplicates stay in the ordered list.", "But Steps 1–8 never change."], 9.0).move_to(DOWN * 1.65)
        self.play(FadeIn(note), run_time=RUN_N)
        self.wait(P_FINAL)
        self.clear_content()

    def closing(self):
        title = self.text("THE RECIPE YOU SHOULD REPEAT ON PAPER", 38, BOLD)
        route = self.text("1 Order  →  2 Q2  →  3 Halves  →  4 Q1 & Q3  →  5 IQR  →  6 Five numbers  →  7 Box  →  8 Whiskers", 22, BOLD)
        reminder = self.text("Do the statistics first. Draw the graph only after the five-number summary is correct.", 24)
        g = VGroup(title, route, reminder).arrange(DOWN, buff=0.42)
        self.fit(g, 14.4, 5.6)
        self.play(FadeIn(title), run_time=RUN_S)
        self.play(FadeIn(route), run_time=RUN_N)
        self.wait(P_EXPLAIN)
        self.play(FadeIn(reminder), run_time=RUN_N)
        self.wait(P_FINAL)
        self.play(FadeOut(g), run_time=RUN_N)
