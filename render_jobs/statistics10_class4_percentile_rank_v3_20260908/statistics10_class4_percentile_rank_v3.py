#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statistics 10 · Class 4 · Percentile Rank V3.

Pedagogical focus
-----------------
This lesson deliberately starts where the previous percentile-value lesson ends:
Class 3 asked for a VALUE from a percentage (k -> P_k -> value).
Class 4 reverses the question and asks for a POSITION from a score
(x -> PR(x) -> percentage).

The scene uses the classroom convention
    PR(x) = 100 * #{x_i <= x} / n
and explicitly states that percentile-rank conventions can differ across books
and software. Ties are therefore part of the teaching objective, not a hidden
implementation detail.

Visual contract
---------------
- Manim Community Edition 0.20.x.
- Horizontal 16:9, Full HD, 30 fps for the final render.
- White background, black/gray hierarchy, no decorative color dependency.
- Persistent numbered section header and subtitle.
- Safe layout with short text blocks, explicit numerical steps and pauses.
- No external assets: fully reproducible in Docker/GitHub Actions.
"""

from __future__ import annotations

import os
from typing import Iterable, Sequence

import numpy as np
from manim import *


# =============================================================================
# RENDER CONFIGURATION
# =============================================================================
PREVIEW = os.getenv("JP_PREVIEW", "0") == "1"
if PREVIEW:
    config.pixel_width = 854
    config.pixel_height = 480
    config.frame_rate = 15
else:
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 30
config.frame_width = 16
config.frame_height = 9
config.background_color = WHITE


# =============================================================================
# DATA — ALL DISPLAYED NUMBERS ARE ASSERTED BELOW
# =============================================================================
MAIN_DATA = np.array([52, 58, 61, 64, 68, 72, 75, 81, 88], dtype=float)
GROUP_B = np.array([65, 68, 70, 72, 74, 76, 78, 81, 85], dtype=float)
TIES_DATA = np.array([60, 65, 70, 72, 72, 72, 80, 85, 90], dtype=float)
CHALLENGE_DATA = np.array([12, 15, 17, 18, 21, 24, 27, 31, 34, 39], dtype=float)


def percentile_rank(data: Sequence[float], score: float) -> float:
    """Inclusive empirical percentile rank used in this lesson."""
    ordered = np.sort(np.asarray(data, dtype=float))
    return 100.0 * np.count_nonzero(ordered <= score) / len(ordered)


def percentile_value_n_plus_one(data: Sequence[float], k: float) -> float:
    """Class-3 continuity helper: L=(k/100)(n+1), linear interpolation."""
    ordered = np.sort(np.asarray(data, dtype=float))
    position = (k / 100.0) * (len(ordered) + 1)
    if position <= 1:
        return float(ordered[0])
    if position >= len(ordered):
        return float(ordered[-1])
    lower_position = int(np.floor(position))
    fraction = position - lower_position
    lower_value = ordered[lower_position - 1]
    upper_value = ordered[lower_position]
    return float(lower_value + fraction * (upper_value - lower_value))


def validate_all_data() -> None:
    assert np.all(np.diff(MAIN_DATA) >= 0)
    assert np.all(np.diff(GROUP_B) >= 0)
    assert np.all(np.diff(TIES_DATA) >= 0)
    assert np.all(np.diff(CHALLENGE_DATA) >= 0)

    # Bridge from the preceding percentile-value lesson.
    assert abs(percentile_value_n_plus_one(MAIN_DATA, 65) - 73.5) < 1e-12

    # Main reverse-direction example.
    assert int(np.count_nonzero(MAIN_DATA <= 72)) == 6
    assert abs(percentile_rank(MAIN_DATA, 72) - 66.66666666666667) < 1e-12

    # Same score, different reference group.
    assert int(np.count_nonzero(GROUP_B <= 72)) == 4
    assert abs(percentile_rank(GROUP_B, 72) - 44.44444444444444) < 1e-12

    # Ties are included by the <= convention.
    assert int(np.count_nonzero(TIES_DATA <= 72)) == 6
    assert int(np.count_nonzero(TIES_DATA == 72)) == 3
    assert abs(percentile_rank(TIES_DATA, 72) - 66.66666666666667) < 1e-12

    # Rank ladder values.
    expected = {
        61: 33.333333333333336,
        68: 55.55555555555556,
        72: 66.66666666666667,
        81: 88.88888888888889,
        88: 100.0,
    }
    for score, answer in expected.items():
        assert abs(percentile_rank(MAIN_DATA, score) - answer) < 1e-12

    # Guided challenge.
    assert int(np.count_nonzero(CHALLENGE_DATA <= 24)) == 6
    assert abs(percentile_rank(CHALLENGE_DATA, 24) - 60.0) < 1e-12


validate_all_data()


# =============================================================================
# STYLE CONSTANTS
# =============================================================================
BLACK_TEXT = BLACK
DARK_GRAY = "#303030"
MID_GRAY = "#777777"
LIGHT_GRAY = "#D7D7D7"
VERY_LIGHT_GRAY = "#F1F1F1"
PAPER_GRAY = "#F8F8F8"

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

RUN_FAST = 0.55
RUN = 0.85
RUN_SLOW = 1.15
PAUSE_SHORT = 0.8
PAUSE_READ = 1.8
PAUSE_EXPLAIN = 2.8
PAUSE_WORK = 4.0
PAUSE_FINAL = 5.0

SAFE_W = 14.6
SAFE_CONTENT_H = 5.75


# =============================================================================
# MAIN SCENE
# =============================================================================
class Statistics10Class4PercentileRankV3(MovingCameraScene):
    """Improved decision-focused Grade 10 Class 4 on percentile rank."""

    def setup(self) -> None:
        super().setup()
        validate_all_data()
        self.camera.background_color = WHITE
        self.camera.frame.set(width=16).move_to(ORIGIN)
        self.header_group: VGroup | None = None

    # ------------------------------------------------------------------
    # Timing wrappers
    # ------------------------------------------------------------------
    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # ------------------------------------------------------------------
    # Typography + fitting
    # ------------------------------------------------------------------
    def txt(self, content: str, size: int = 29, weight=NORMAL, color=BLACK_TEXT) -> Text:
        return Text(content, font_size=size, weight=weight, color=color, line_spacing=0.92)

    def math(self, expression: str, size: int = 38) -> MathTex:
        return MathTex(expression, font_size=size, color=BLACK_TEXT)

    @staticmethod
    def fit(mob: Mobject, max_width: float, max_height: float) -> Mobject:
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        if mob.height > max_height:
            mob.scale_to_fit_height(max_height)
        return mob

    # ------------------------------------------------------------------
    # Reusable classroom components
    # ------------------------------------------------------------------
    def set_header(self, number: int, title: str, subtitle: str) -> None:
        num_box = RoundedRectangle(
            width=0.72,
            height=0.52,
            corner_radius=0.10,
            stroke_color=BLACK,
            stroke_width=2,
            fill_color=WHITE,
            fill_opacity=1,
        )
        num = self.txt(f"{number:02d}", 22, BOLD).move_to(num_box)
        title_mob = self.txt(title, 34, BOLD)
        self.fit(title_mob, 13.6, 0.58)
        row = VGroup(VGroup(num_box, num), title_mob).arrange(RIGHT, buff=0.25)
        row.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.48)
        rule = Line(LEFT * 7.45, RIGHT * 7.45, color=LIGHT_GRAY, stroke_width=2)
        rule.next_to(row, DOWN, buff=0.07)
        subtitle_mob = self.txt(subtitle, 20, color=DARK_GRAY)
        self.fit(subtitle_mob, 14.3, 0.52)
        subtitle_mob.next_to(rule, DOWN, buff=0.08).align_to(row, LEFT)
        new_header = VGroup(row, rule, subtitle_mob)

        if self.header_group is None:
            self.header_group = new_header
            self.play(FadeIn(new_header), run_time=RUN_FAST)
        else:
            old = self.header_group
            self.header_group = new_header
            self.play(ReplacementTransform(old, new_header), run_time=RUN_FAST)

    def panel(
        self,
        title: str,
        body_lines: Sequence[str],
        width: float = 6.2,
        body_size: int = 25,
        title_size: int = 25,
        fill=PAPER_GRAY,
    ) -> VGroup:
        title_mob = self.txt(title, title_size, BOLD)
        body = VGroup(*[self.txt(line, body_size) for line in body_lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        content = VGroup(title_mob, body).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.fit(content, width - 0.60, 3.4)
        box = RoundedRectangle(
            width=width,
            height=max(1.25, content.height + 0.62),
            corner_radius=0.12,
            stroke_color=BLACK,
            stroke_width=1.8,
            fill_color=fill,
            fill_opacity=1,
        )
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.30)
        return VGroup(box, content)

    def formula_panel(self, expression: str, width=8.2, height=1.15, size=40) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=BLACK,
            stroke_width=2,
            fill_color=PAPER_GRAY,
            fill_opacity=1,
        )
        eq = self.math(expression, size)
        self.fit(eq, width - 0.55, height - 0.26)
        eq.move_to(box)
        return VGroup(box, eq)

    def value_card(self, value: str, width=1.15, height=0.75, font_size=28) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.10,
            stroke_color=BLACK,
            stroke_width=1.8,
            fill_color=WHITE,
            fill_opacity=1,
        )
        label = self.txt(value, font_size, BOLD).move_to(box)
        return VGroup(box, label)

    def dataset_strip(
        self,
        data: Iterable[float],
        *,
        indices: bool = True,
        target: float | None = None,
        highlight_le: bool = False,
        card_width: float = 1.12,
    ) -> tuple[VGroup, list[VGroup], list[Text]]:
        values = [int(v) if float(v).is_integer() else float(v) for v in data]
        cards: list[VGroup] = []
        index_mobs: list[Text] = []
        for idx, value in enumerate(values, 1):
            card = self.value_card(str(value), width=card_width)
            if target is not None and highlight_le and float(value) <= target:
                card[0].set_fill(VERY_LIGHT_GRAY, opacity=1)
                card[0].set_stroke(width=2.4)
            if target is not None and float(value) == target:
                card[0].set_stroke(width=3.5)
            cards.append(card)
            if indices:
                index_mobs.append(self.txt(str(idx), 18, color=MID_GRAY))

        row = VGroup(*cards).arrange(RIGHT, buff=0.12)
        group = VGroup(row)
        if indices:
            indexes = VGroup(*index_mobs)
            for i, mob in enumerate(index_mobs):
                mob.next_to(cards[i], UP, buff=0.10)
            group.add(indexes)
        self.fit(group, 13.7, 1.35)
        return group, cards, index_mobs

    def step_card(self, number: int, title: str, detail: str, width=4.25) -> VGroup:
        circle = Circle(radius=0.28, stroke_color=BLACK, stroke_width=2, fill_color=WHITE, fill_opacity=1)
        n = self.txt(str(number), 20, BOLD).move_to(circle)
        title_mob = self.txt(title, 23, BOLD)
        detail_mob = self.txt(detail, 19, color=DARK_GRAY)
        self.fit(title_mob, width - 1.0, 0.42)
        self.fit(detail_mob, width - 1.0, 0.38)
        text = VGroup(title_mob, detail_mob).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        row = VGroup(VGroup(circle, n), text).arrange(RIGHT, buff=0.20)
        box = RoundedRectangle(
            width=width,
            height=1.10,
            corner_radius=0.12,
            stroke_color=BLACK,
            stroke_width=1.6,
            fill_color=PAPER_GRAY,
            fill_opacity=1,
        )
        row.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.24)
        return VGroup(box, row)

    def interpretation_bar(self, text: str, width=12.4) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=0.92,
            corner_radius=0.12,
            stroke_color=BLACK,
            stroke_width=2,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1,
        )
        mob = self.txt(text, 27, BOLD)
        self.fit(mob, width - 0.55, 0.52)
        mob.move_to(box)
        return VGroup(box, mob)

    def fade_stage(self, *mobs: Mobject) -> None:
        existing = [m for m in mobs if m is not None]
        if existing:
            self.play(*[FadeOut(m) for m in existing], run_time=RUN_FAST)

    # ------------------------------------------------------------------
    # Lesson orchestration
    # ------------------------------------------------------------------
    def construct(self) -> None:
        self.opening()
        self.scene_01_reverse_the_question()
        self.scene_02_definition_and_convention()
        self.scene_03_full_worked_example()
        self.scene_04_value_vs_rank()
        self.scene_05_same_score_different_group()
        self.scene_06_ties_matter()
        self.scene_07_rank_ladder()
        self.scene_08_misconception_clinic()
        self.scene_09_guided_challenge()
        self.scene_10_final_method_map()

    def opening(self) -> None:
        course = self.txt("GRADE 10 · STATISTICS", 28, BOLD, DARK_GRAY)
        title = self.txt("CLASS 4 · PERCENTILE RANK", 52, BOLD)
        subtitle = self.txt("From a score to its relative position", 31)
        promise = self.txt("Same family of position measures. Opposite question.", 25, color=DARK_GRAY)
        block = VGroup(course, title, subtitle, promise).arrange(DOWN, buff=0.25)
        self.fit(block, 13.8, 4.3)
        block.move_to(UP * 0.35)

        question = self.formula_panel(r"x=72\quad\Longrightarrow\quad PR(72)=\ ?", width=6.6, height=1.05, size=39)
        question.next_to(block, DOWN, buff=0.55)

        self.play(FadeIn(course), run_time=RUN_FAST)
        self.play(Write(title), run_time=RUN)
        self.play(FadeIn(subtitle, shift=UP * 0.08), FadeIn(promise), run_time=RUN)
        self.play(FadeIn(question), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.fade_stage(block, question)

    # ------------------------------------------------------------------
    # 01 — Continuity with Class 3 + Q/D/P bridge
    # ------------------------------------------------------------------
    def scene_01_reverse_the_question(self) -> None:
        self.set_header(
            1,
            "SAME FAMILY, OPPOSITE QUESTION",
            "Class 3 found a value from a percentage. Class 4 starts with a score and locates its relative position.",
        )

        forward = self.panel(
            "CLASS 3 · FORWARD",
            ["Given a percentage k", "Find the percentile value Pk", "Example: 65% → P65 → 73.5"],
            width=6.3,
        )
        reverse = self.panel(
            "CLASS 4 · REVERSE",
            ["Given a score x", "Find the percentile rank PR(x)", "Example: 72 → PR(72) → ?"],
            width=6.3,
        )
        pair = VGroup(forward, reverse).arrange(RIGHT, buff=0.55)
        pair.move_to(UP * 0.20)

        family = VGroup(
            self.txt("POSITION-MEASURE BRIDGE", 24, BOLD),
            self.math(r"Q_1=P_{25}\qquad Q_2=P_{50}=D_5\qquad Q_3=P_{75}", 38),
            self.txt("Quartiles and deciles are named checkpoints inside the percentile scale.", 22, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.17)
        family_box = SurroundingRectangle(family, buff=0.26, corner_radius=0.10, color=BLACK, stroke_width=1.8)
        family_group = VGroup(family_box, family)
        family_group.next_to(pair, DOWN, buff=0.42)

        self.play(FadeIn(forward, shift=RIGHT * 0.12), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(reverse, shift=LEFT * 0.12), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(family_group), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.fade_stage(pair, family_group)

    # ------------------------------------------------------------------
    # 02 — Definition + convention
    # ------------------------------------------------------------------
    def scene_02_definition_and_convention(self) -> None:
        self.set_header(
            2,
            "FORMAL DEFINITION — PERCENTILE RANK",
            "For this class we use the inclusive empirical convention: count every observation at or below the score.",
        )

        formula = self.formula_panel(
            r"PR(x)=100\,\frac{\#\{x_i\le x\}}{n}", width=8.6, height=1.25, size=46
        )
        formula.move_to(UP * 1.05)

        numerator = self.panel(
            "NUMERATOR",
            ["Count observations ≤ x", "Include x itself", "Include every tie equal to x"],
            width=5.7,
            body_size=23,
        )
        denominator = self.panel(
            "DENOMINATOR",
            ["n = total observations", "Do not use only the values below x", "The result is a percentage"],
            width=5.7,
            body_size=23,
        )
        pieces = VGroup(numerator, denominator).arrange(RIGHT, buff=0.55)
        pieces.next_to(formula, DOWN, buff=0.43)

        convention = self.txt(
            "Convention note: some textbooks/software define percentile rank differently. Always identify the rule being used.",
            21,
            color=DARK_GRAY,
        )
        self.fit(convention, 13.5, 0.44)
        convention.to_edge(DOWN, buff=0.42)

        self.play(FadeIn(formula), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(numerator), FadeIn(denominator), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.play(FadeIn(convention), run_time=RUN_FAST)
        self.wait(PAUSE_READ)
        self.fade_stage(formula, pieces, convention)

    # ------------------------------------------------------------------
    # 03 — Core worked example
    # ------------------------------------------------------------------
    def scene_03_full_worked_example(self) -> None:
        self.set_header(
            3,
            "FULL WORKED EXAMPLE — PR(72)",
            "Sort, locate 72, count the observations at or below it, divide by the total, and interpret the percentage.",
        )

        label = self.txt("ORDERED DATA · n = 9", 24, BOLD)
        strip, cards, _ = self.dataset_strip(MAIN_DATA, target=72, highlight_le=False)
        dataset = VGroup(label, strip).arrange(DOWN, buff=0.22)
        dataset.move_to(UP * 1.05)

        self.play(FadeIn(label), run_time=RUN_FAST)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.05) for card in cards], lag_ratio=0.08), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)

        # Explicit cumulative count: first six cards are at or below 72.
        self.play(
            *[
                cards[i][0].animate.set_fill(VERY_LIGHT_GRAY, opacity=1).set_stroke(width=2.5)
                for i in range(6)
            ],
            run_time=RUN,
        )
        self.play(cards[5][0].animate.set_stroke(width=4.0), run_time=RUN_FAST)
        count = self.txt("6 observations are ≤ 72", 27, BOLD)
        count.next_to(dataset, DOWN, buff=0.38)
        self.play(FadeIn(count), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)

        calculation = self.formula_panel(
            r"PR(72)=100\left(\frac{6}{9}\right)=66.7\%", width=7.2, height=1.10, size=42
        )
        calculation.next_to(count, DOWN, buff=0.32)
        self.play(FadeIn(calculation), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)

        meaning = self.interpretation_bar("Interpretation: 66.7% of the observations are at or below 72.")
        meaning.to_edge(DOWN, buff=0.34)
        self.play(FadeIn(meaning), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.fade_stage(dataset, count, calculation, meaning)

    # ------------------------------------------------------------------
    # 04 — P_k vs PR(x)
    # ------------------------------------------------------------------
    def scene_04_value_vs_rank(self) -> None:
        self.set_header(
            4,
            "PERCENTILE VALUE VS PERCENTILE RANK",
            "They use the same percentile language but answer different questions. Keep the input and output directions visible.",
        )

        pvalue = self.panel(
            "PERCENTILE VALUE · P65",
            ["INPUT: percentage 65%", "QUESTION: what value is there?", "OUTPUT: value 73.5"],
            width=6.25,
            body_size=25,
        )
        prank = self.panel(
            "PERCENTILE RANK · PR(72)",
            ["INPUT: score 72", "QUESTION: where does it stand?", "OUTPUT: rank 66.7%"],
            width=6.25,
            body_size=25,
        )
        pair = VGroup(pvalue, prank).arrange(RIGHT, buff=0.55)
        pair.move_to(UP * 0.20)

        arrows = VGroup(
            self.math(r"65\%\ \longrightarrow\ P_{65}\ \longrightarrow\ 73.5", 34),
            self.math(r"72\ \longrightarrow\ PR(72)\ \longrightarrow\ 66.7\%", 34),
        ).arrange(DOWN, buff=0.20)
        arrows.next_to(pair, DOWN, buff=0.40)

        warning = self.interpretation_bar("Do not say “72 is 66.7%”. Say “66.7% of observations are ≤ 72”.", width=12.6)
        warning.to_edge(DOWN, buff=0.35)

        self.play(FadeIn(pvalue), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeIn(prank), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(arrows), run_time=RUN)
        self.play(FadeIn(warning), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.fade_stage(pair, arrows, warning)

    # ------------------------------------------------------------------
    # 05 — Reference group matters
    # ------------------------------------------------------------------
    def scene_05_same_score_different_group(self) -> None:
        self.set_header(
            5,
            "SAME SCORE, DIFFERENT POSITION",
            "Percentile rank is relative to a reference group. The same score can occupy a very different position in another dataset.",
        )

        title_a = self.txt("GROUP A", 24, BOLD)
        strip_a, cards_a, _ = self.dataset_strip(MAIN_DATA, target=72, highlight_le=True, card_width=1.00)
        result_a = self.math(r"\#(x_i\le72)=6\quad\Rightarrow\quad PR_A(72)=66.7\%", 31)
        block_a = VGroup(title_a, strip_a, result_a).arrange(DOWN, buff=0.20)

        title_b = self.txt("GROUP B", 24, BOLD)
        strip_b, cards_b, _ = self.dataset_strip(GROUP_B, target=72, highlight_le=True, card_width=1.00)
        result_b = self.math(r"\#(x_i\le72)=4\quad\Rightarrow\quad PR_B(72)=44.4\%", 31)
        block_b = VGroup(title_b, strip_b, result_b).arrange(DOWN, buff=0.20)

        blocks = VGroup(block_a, block_b).arrange(DOWN, buff=0.64)
        blocks.move_to(DOWN * 0.05)
        self.fit(blocks, 13.7, 4.65)

        self.play(FadeIn(block_a), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(block_b), run_time=RUN)
        self.wait(PAUSE_WORK)

        insight = self.interpretation_bar("A percentile rank describes position inside a group — not an absolute property of the score.", width=12.9)
        insight.to_edge(DOWN, buff=0.32)
        self.play(FadeIn(insight), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.fade_stage(blocks, insight)

    # ------------------------------------------------------------------
    # 06 — Ties
    # ------------------------------------------------------------------
    def scene_06_ties_matter(self) -> None:
        self.set_header(
            6,
            "TIES MATTER — COUNT EVERY VALUE EQUAL TO x",
            "With the inclusive ≤ convention, all observations tied at the target score are included in the cumulative count.",
        )

        strip, cards, _ = self.dataset_strip(TIES_DATA, target=72, highlight_le=False)
        strip.move_to(UP * 1.10)
        self.play(LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.08), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)

        # Highlight three tied 72s first, then the full cumulative set.
        self.play(*[cards[i][0].animate.set_stroke(width=4.0) for i in (3, 4, 5)], run_time=RUN)
        tie_note = self.txt("Three observations are tied at 72.", 26, BOLD)
        tie_note.next_to(strip, DOWN, buff=0.35)
        self.play(FadeIn(tie_note), run_time=RUN_FAST)
        self.wait(PAUSE_EXPLAIN)

        self.play(
            *[cards[i][0].animate.set_fill(VERY_LIGHT_GRAY, opacity=1) for i in range(6)],
            run_time=RUN,
        )
        formula = self.formula_panel(r"PR(72)=100\left(\frac{6}{9}\right)=66.7\%", width=7.0, height=1.08, size=41)
        formula.next_to(tie_note, DOWN, buff=0.32)
        self.play(FadeIn(formula), run_time=RUN)

        rule = self.interpretation_bar("Do not count only one 72. Under this convention, every 72 is included.", width=11.7)
        rule.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(rule), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.fade_stage(strip, tie_note, formula, rule)

    # ------------------------------------------------------------------
    # 07 — Rank ladder / empirical staircase
    # ------------------------------------------------------------------
    def scene_07_rank_ladder(self) -> None:
        self.set_header(
            7,
            "RANK LADDER — SEE THE RELATIVE POSITION CHANGE",
            "As x moves to the right through the ordered data, the cumulative count increases and so does the percentile rank.",
        )

        headers = ["score x", "count ≤ x", "PR(x)"]
        rows = [
            ["61", "3 / 9", "33.3%"],
            ["68", "5 / 9", "55.6%"],
            ["72", "6 / 9", "66.7%"],
            ["81", "8 / 9", "88.9%"],
            ["88", "9 / 9", "100.0%"],
        ]
        table_data = [headers] + rows
        table = Table(
            table_data,
            include_outer_lines=True,
            line_config={"color": BLACK, "stroke_width": 1.5},
            element_to_mobject=lambda s: self.txt(str(s), 23, BOLD if str(s) in headers else NORMAL),
            h_buff=0.55,
            v_buff=0.25,
        )
        self.fit(table, 8.2, 4.65)
        table.move_to(LEFT * 2.8 + DOWN * 0.10)

        logic = self.panel(
            "WHAT CHANGES?",
            [
                "x increases → more values are ≤ x",
                "the denominator n stays fixed",
                "PR(x) therefore moves upward",
                "at the maximum value → 100%",
            ],
            width=5.4,
            body_size=23,
        )
        logic.move_to(RIGHT * 4.3 + DOWN * 0.15)

        self.play(Create(table.get_horizontal_lines()), Create(table.get_vertical_lines()), run_time=RUN)
        self.play(FadeIn(table.get_entries()), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(logic), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.fade_stage(table, logic)

    # ------------------------------------------------------------------
    # 08 — Common mistakes
    # ------------------------------------------------------------------
    def scene_08_misconception_clinic(self) -> None:
        self.set_header(
            8,
            "MISCONCEPTION CLINIC — FOUR CHECKS BEFORE YOU FINISH",
            "Most errors come from changing the inequality, the denominator, the meaning of the percentage, or the direction of the question.",
        )

        cards = VGroup(
            self.step_card(1, "USE ≤, NOT <", "Include the target score and its ties."),
            self.step_card(2, "DENOMINATOR = n", "Divide by the total number of observations."),
            self.step_card(3, "INTERPRET THE %", "It is the share of observations at or below x."),
            self.step_card(4, "CHECK DIRECTION", "Pk asks for a value; PR(x) asks for a rank."),
        )
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.45, 0.42))
        cards.move_to(DOWN * 0.10)
        self.fit(cards, 13.4, 4.3)

        for card in cards:
            self.play(FadeIn(card, shift=UP * 0.06), run_time=RUN_FAST)
            self.wait(PAUSE_SHORT)
        self.wait(PAUSE_WORK)
        self.fade_stage(cards)

    # ------------------------------------------------------------------
    # 09 — Student challenge with delayed reveal
    # ------------------------------------------------------------------
    def scene_09_guided_challenge(self) -> None:
        self.set_header(
            9,
            "GUIDED CHALLENGE — YOUR TURN",
            "For the ordered data below, estimate PR(24) before the solution appears. Use the exact same six-step method.",
        )

        prompt = self.formula_panel(r"x=24\qquad PR(24)=\ ?", width=5.8, height=1.02, size=39)
        prompt.move_to(UP * 1.25)
        strip, cards, _ = self.dataset_strip(CHALLENGE_DATA, target=24, highlight_le=False, card_width=1.00)
        strip.next_to(prompt, DOWN, buff=0.50)
        think = self.txt("Pause: count first. Do not calculate until you know the numerator.", 24, BOLD)
        think.next_to(strip, DOWN, buff=0.40)

        self.play(FadeIn(prompt), run_time=RUN)
        self.play(LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.07), run_time=RUN_SLOW)
        self.play(FadeIn(think), run_time=RUN_FAST)
        self.wait(PAUSE_WORK + 2.0)

        self.play(*[cards[i][0].animate.set_fill(VERY_LIGHT_GRAY, opacity=1) for i in range(6)], run_time=RUN)
        reveal = self.formula_panel(r"PR(24)=100\left(\frac{6}{10}\right)=60\%", width=6.8, height=1.08, size=42)
        reveal.to_edge(DOWN, buff=0.42)
        self.play(FadeIn(reveal), run_time=RUN)
        self.wait(PAUSE_WORK)
        self.fade_stage(prompt, strip, think, reveal)

    # ------------------------------------------------------------------
    # 10 — Final reproducible method
    # ------------------------------------------------------------------
    def scene_10_final_method_map(self) -> None:
        self.set_header(
            10,
            "FINAL MAP — VALUE → POSITION → INTERPRETATION",
            "A correct percentile-rank answer is not only a percentage; it includes the count rule, the calculation, and a sentence about relative position.",
        )

        cards = VGroup(
            self.step_card(1, "SORT", "Put the data in ascending order.", width=4.15),
            self.step_card(2, "LOCATE x", "Find the target score.", width=4.15),
            self.step_card(3, "COUNT ≤ x", "Include x and all ties.", width=4.15),
            self.step_card(4, "DIVIDE BY n", "Use the total sample size.", width=4.15),
            self.step_card(5, "MULTIPLY ×100", "Convert the fraction to percent.", width=4.15),
            self.step_card(6, "INTERPRET", "State the share at or below x.", width=4.15),
        )
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.32, 0.40))
        cards.move_to(UP * 0.10)
        self.fit(cards, 13.7, 3.3)

        for card in cards:
            self.play(FadeIn(card, shift=UP * 0.06), run_time=RUN_FAST)
        self.wait(PAUSE_EXPLAIN)

        final_formula = self.formula_panel(r"PR(x)=100\,\frac{\#\{x_i\le x\}}{n}", width=7.6, height=1.02, size=39)
        final_formula.next_to(cards, DOWN, buff=0.35)
        self.play(FadeIn(final_formula), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)

        closing = self.interpretation_bar("Percentile values answer “how much?”. Percentile ranks answer “where?”.", width=11.5)
        closing.to_edge(DOWN, buff=0.30)
        self.play(FadeIn(closing), run_time=RUN)
        self.wait(PAUSE_FINAL)

        self.fade_stage(cards, final_formula, closing)
        if self.header_group is not None:
            self.play(FadeOut(self.header_group), run_time=RUN_FAST)
            self.header_group = None

        end = VGroup(
            self.txt("CLASS 4 COMPLETE", 30, BOLD, DARK_GRAY),
            self.txt("PERCENTILE RANK", 50, BOLD),
            self.txt("Sort · Count ≤ x · Divide by n · Convert · Interpret", 27),
        ).arrange(DOWN, buff=0.28)
        end.move_to(UP * 0.20)
        check = self.math(r"72\ \longrightarrow\ 6/9\ \longrightarrow\ 66.7\%", 42)
        check.next_to(end, DOWN, buff=0.55)
        self.play(FadeIn(end), run_time=RUN)
        self.play(Write(check), run_time=RUN)
        self.wait(PAUSE_FINAL)


# Local preview:
#   JP_PREVIEW=1 LESSON_TIME_SCALE=0.25 manim -pql statistics10_class4_percentile_rank_v3.py Statistics10Class4PercentileRankV3 --disable_caching
# Final:
#   JP_PREVIEW=0 manim -pqh statistics10_class4_percentile_rank_v3.py Statistics10Class4PercentileRankV3 --disable_caching
