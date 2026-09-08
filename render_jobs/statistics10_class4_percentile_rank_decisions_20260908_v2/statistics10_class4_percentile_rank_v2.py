#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Statistics 10 · Class 4 · Percentile Rank & Relative-Position Decisions · V2 QA.

This revision inherits the validated V1 lesson and overrides the scenes that
showed spacing/overlap risk in the rendered MP4. It also strengthens the
classroom convention, decision criterion, and bridge to the remaining Period III
curriculum (box-plot comparison -> normal distribution).

Target: ManimCE 0.20.1, 1920x1080, 30 fps.
"""
from __future__ import annotations

import sys
from pathlib import Path

BASE_JOB = (
    Path(__file__).resolve().parents[1]
    / "statistics10_class4_percentile_rank_decisions_20260904"
)
sys.path.insert(0, str(BASE_JOB))

from statistics10_class4_percentile_rank import *  # noqa: F401,F403


class Statistics10Class4PercentileRankV2(Statistics10Class4PercentileRank):
    """Frame-QA revision of the original Class 4."""

    def construct(self):
        self.scene_01_reverse_question()
        self.scene_02_meaning()
        self.scene_03_six_steps()
        self.scene_04_example_setup()
        self.scene_05_count()
        self.scene_06_compute()
        self.scene_07_interpret()
        self.scene_08_compare()
        self.scene_09_decision()
        self.scene_10_distinction()
        self.scene_11_guided_challenge()
        self.scene_12_final_recipe()
        self.final_closing()

    def scene_01_reverse_question(self):
        self.set_header(
            1,
            "REVERSE THE QUESTION",
            "Last class: percentile → value. Today: observed value → relative position.",
        )

        left = self.card("CLASS 3", r"P_{65}\ \longrightarrow\ ?", 5.2, 1.95, True)
        right = self.card("CLASS 4", r"72\ \longrightarrow\ ?", 5.2, 1.95, True)
        pair = VGroup(left, right).arrange(RIGHT, buff=0.72).move_to(UP * 0.95)

        left_label = self.text("PERCENTILE → VALUE", 22, BOLD).next_to(
            left, DOWN, buff=0.14
        )
        right_label = self.text("VALUE → PERCENTILE RANK", 22, BOLD).next_to(
            right, DOWN, buff=0.14
        )

        self.play(FadeIn(left, shift=RIGHT * 0.12), run_time=RUN_NORMAL)
        self.play(Write(left_label), run_time=RUN_NORMAL)
        self.wait(1.8)

        solved = self.math(r"P_{65}\ \longrightarrow\ 73.5", 38).move_to(left[1][1])
        self.play(ReplacementTransform(left[1][1], solved), run_time=RUN_NORMAL)
        self.wait(1.8)

        self.play(FadeIn(right, shift=LEFT * 0.12), run_time=RUN_NORMAL)
        self.play(Write(right_label), run_time=RUN_NORMAL)
        self.wait(1.8)

        reverse_band = self.formula_box(
            r"\mathrm{percentile}\rightarrow\mathrm{value}"
            r"\qquad\Longleftrightarrow\qquad"
            r"\mathrm{value}\rightarrow\mathrm{relative\ position}",
            width=12.6,
            font_size=30,
            height=1.05,
        ).move_to(DOWN * 1.40)

        self.play(FadeIn(reverse_band), run_time=RUN_NORMAL)
        self.wait(2.2)

        note = self.interpretation_box(
            [
                "Same dataset, different question.",
                "Do not treat the two directions as exact algebraic inverses.",
            ],
            width=10.7,
            title="KEY DISTINCTION",
        ).move_to(DOWN * 2.62)

        self.play(FadeIn(note), run_time=RUN_NORMAL)
        self.wait(3.0)
        self.clear_stage()

    def scene_02_meaning(self):
        self.set_header(
            2,
            "PERCENTILE RANK = RELATIVE POSITION",
            "Class convention: PR(x) = 100 × count(values ≤ x) / n. Ties at x are included.",
        )

        q = self.text(
            "Where does 72 stand inside this dataset?", 31, BOLD
        ).move_to(UP * 1.78)

        axis, _ = self.percentile_axis(
            rank=66.7,
            label="72  ≈ 67th percentile",
            width=11.4,
            y=0.55,
        )
        x0 = -11.4 / 2
        x67 = x0 + 11.4 * 0.667
        progress = Line(
            [x0, 0.55, 0],
            [x67, 0.55, 0],
            color=MID_GRAY,
            stroke_width=8,
        )

        explain = self.interpretation_box(
            [
                "About 66.7% of the observations are at or below 72.",
                "So 72 is approximately at the 67th percentile.",
            ],
            width=10.6,
            title="RELATIVE POSITION",
        ).move_to(DOWN * 0.92)

        pair = VGroup(
            self.card("OBSERVED VALUE", "72", 3.7, 1.20),
            self.card("PERCENTILE RANK", "≈ 66.7%", 4.4, 1.20),
        ).arrange(RIGHT, buff=0.50).move_to(DOWN * 2.18)

        warning = self.text(
            "The rank is a percentage position — not a new score.",
            24,
            BOLD,
        ).move_to(DOWN * 3.05)

        convention = self.text(
            "Note: percentile-rank conventions can vary; this class always uses count ≤ x.",
            20,
            MEDIUM,
        ).set_color(MID_GRAY).move_to(DOWN * 3.45)

        self.play(Write(q), run_time=RUN_NORMAL)
        self.wait(1.8)
        self.play(
            Create(axis[0]),
            FadeIn(axis[1]),
            FadeIn(axis[2]),
            run_time=RUN_NORMAL,
        )
        self.wait(1.3)
        self.play(Create(progress), run_time=RUN_SLOW)
        self.play(FadeIn(VGroup(*axis[3:])), run_time=RUN_NORMAL)
        self.wait(2.1)
        self.play(FadeIn(explain), run_time=RUN_NORMAL)
        self.wait(2.4)
        self.play(FadeIn(pair), run_time=RUN_NORMAL)
        self.wait(1.8)
        self.play(Write(warning), run_time=RUN_NORMAL)
        self.play(FadeIn(convention), run_time=RUN_NORMAL)
        self.wait(3.0)
        self.clear_stage()

    def scene_07_interpret(self):
        self.set_header(
            7,
            "INTERPRET, DON'T JUST CALCULATE",
            "A percentile rank states where an observed value stands inside the dataset.",
        )
        nav = self.build_step_navigation(5)
        self.play(FadeIn(nav), run_time=RUN_NORMAL)

        result = self.formula_box(
            r"\mathrm{PR}(72)\approx 66.7",
            width=6.3,
            font_size=44,
        ).move_to(UP * 1.62)
        q = self.section_question("What does 66.7 mean?", y=0.72, size=31)

        self.play(FadeIn(result), run_time=RUN_NORMAL)
        self.play(Write(q), run_time=RUN_NORMAL)
        self.wait(2.7)

        a = self.interpretation_box(
            ["About 66.7% of the observations are at or below 72."],
            width=10.3,
            title="INTERPRETATION",
        ).move_to(DOWN * 0.36)
        self.play(FadeIn(a), run_time=RUN_NORMAL)
        self.wait(2.2)

        b = self.interpretation_box(
            ["72 is approximately at the 67th percentile."],
            width=9.4,
            title="STATISTICAL LANGUAGE",
        ).move_to(DOWN * 1.55)
        self.play(FadeIn(b), run_time=RUN_NORMAL)
        self.wait(2.3)

        relation = self.formula_box(
            r"\mathrm{value}\ 72"
            r"\quad\longrightarrow\quad"
            r"\mathrm{relative\ position}\ \approx 67^{\mathrm{th}}\ \mathrm{percentile}",
            width=11.8,
            font_size=30,
            height=1.02,
        ).move_to(DOWN * 2.72)
        self.play(FadeIn(relation), run_time=RUN_NORMAL)
        self.wait(3.0)
        self.clear_stage()

    def scene_09_decision(self):
        self.set_header(
            9,
            "USE RELATIVE POSITION TO MAKE A DECISION",
            "A program selects students in approximately the top 20% of the group.",
        )
        nav = self.build_step_navigation(6)
        self.play(FadeIn(nav), run_time=RUN_NORMAL)

        q = self.section_question("Would a score of 81 qualify?", y=1.92, size=33)
        self.play(Write(q), run_time=RUN_NORMAL)
        self.wait(2.7)

        rule = self.formula_box(
            r"\mathrm{Top\ 20\%}\quad\Rightarrow\quad \mathrm{PR}(x)\ge 80",
            width=7.6,
            font_size=36,
            height=1.02,
        ).move_to(UP * 0.95)
        self.play(FadeIn(rule), run_time=RUN_NORMAL)
        self.wait(2.0)

        known = self.formula_box(
            r"\mathrm{PR}(81)\approx 88.9",
            width=5.6,
            font_size=41,
            height=1.00,
        ).move_to(UP * 0.02)
        self.play(FadeIn(known), run_time=RUN_NORMAL)
        self.wait(1.7)

        axis, _ = self.percentile_axis(
            rank=88.9,
            label="81 → 88.9",
            top_region_start=80,
            width=11.4,
            y=-1.05,
        )
        self.play(FadeIn(axis), run_time=RUN_NORMAL)
        self.wait(2.4)

        compare = self.text(
            "88.9 ≥ 80  →  the score is inside the top-20% region.",
            27,
            BOLD,
        ).move_to(DOWN * 2.05)
        self.play(Write(compare), run_time=RUN_NORMAL)
        self.wait(2.1)

        yes = self.card(
            "DECISION",
            "YES — 81 qualifies under this percentile-rank rule.",
            9.8,
            1.18,
        ).move_to(DOWN * 2.88)
        self.play(FadeIn(yes), run_time=RUN_NORMAL)
        self.wait(3.1)
        self.clear_stage()

    def scene_12_final_recipe(self):
        self.set_header(
            12,
            "FINAL RECIPE — VALUE → POSITION",
            "Order, identify, count carefully, compute, interpret, then decide.",
        )

        cards = VGroup()
        for number, label in STEP_LABELS:
            card = RoundedRectangle(
                width=4.3,
                height=0.78,
                corner_radius=0.08,
                stroke_color=BLACK_LINE,
                stroke_width=1.4,
                fill_color=WHITE,
                fill_opacity=1.0,
            )
            badge = RoundedRectangle(
                width=0.58,
                height=0.46,
                corner_radius=0.06,
                stroke_color=BLACK_LINE,
                stroke_width=1.2,
                fill_color=VERY_LIGHT_GRAY,
                fill_opacity=1.0,
            )
            n = self.text(str(number), 18, BOLD).move_to(badge)
            t = self.text(label, 21, BOLD)
            content = VGroup(VGroup(badge, n), t).arrange(RIGHT, buff=0.18)
            content.move_to(card)
            cards.add(VGroup(card, content))

        cards.arrange_in_grid(rows=2, cols=3, buff=(0.36, 0.28)).move_to(UP * 0.95)
        self.play(
            LaggedStart(
                *[FadeIn(c, shift=UP * 0.08) for c in cards],
                lag_ratio=0.15,
            ),
            run_time=RUN_SLOW * 2.5,
        )
        self.wait(2.2)

        formula = self.formula_box(
            r"\mathrm{PR}(x)=100"
            r"\left(\frac{\#\{\mathrm{observations}\le x\}}{n}\right)",
            width=9.5,
            font_size=36,
            height=1.10,
        ).move_to(DOWN * 0.78)
        self.play(FadeIn(formula), run_time=RUN_NORMAL)
        self.wait(2.3)

        bridge = self.interpretation_box(
            [
                "Class 3: percentile k → data value.",
                "Class 4: observed value → percentile rank.",
                "Next: compare distributions with boxplots, then connect to the normal distribution.",
            ],
            width=11.8,
            title="CURRICULUM BRIDGE",
        ).move_to(DOWN * 2.30)
        self.play(FadeIn(bridge), run_time=RUN_NORMAL)
        self.wait(3.6)
        self.clear_stage()

    def final_closing(self):
        title = self.text("PERCENTILE RANK", 42, BOLD).move_to(UP * 0.55)
        rule = Line(LEFT * 2.8, RIGHT * 2.8, color=BLACK_LINE, stroke_width=1.6)
        rule.next_to(title, DOWN, buff=0.18)
        a = self.text("A raw value tells you what was obtained.", 26, MEDIUM)
        b = self.text("A percentile rank tells you where it stands.", 28, BOLD)
        c = self.text(
            "Next: distribution comparison → normal distribution.",
            22,
            MEDIUM,
        ).set_color(MID_GRAY)
        body = VGroup(a, b, c).arrange(DOWN, buff=0.24)
        body.next_to(rule, DOWN, buff=0.30)
        closing = VGroup(title, rule, body)
        self.play(FadeIn(closing), run_time=RUN_SLOW)
        self.wait(4.0)
        self.play(FadeOut(closing), run_time=RUN_NORMAL)
