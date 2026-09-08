#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statistics 10 · Class 4 V2 · Percentile Rank, Relative Position & Decisions.

Direct successor to Class 4 V1 while preserving the established JP Classroom
visual language and the exact classroom convention:

    PR(x) = 100 * count(values <= x) / n

Pedagogical sequence:
    SEE -> COUNT -> LOCATE -> FORMALIZE -> INTERPRET -> DECIDE

Target: Manim Community Edition 0.20.1 · 1920x1080 · 30 fps.
"""
from __future__ import annotations

import math
import numpy as np

from library.jp_classroom_style import *


# =============================================================================
# DATA + NUMERICAL SOURCE OF TRUTH
# =============================================================================
MAIN_DATA = [52, 58, 61, 64, 68, 72, 75, 81, 88]
GROUP_B = [65, 68, 70, 72, 74, 76, 78, 81, 85]
TIES_DATA = [60, 65, 70, 72, 72, 72, 80, 85, 90]
CHALLENGE_DATA = [12, 15, 17, 18, 21, 24, 27, 31, 34, 39]

STEP_LABELS = [
    (1, "ORDER"),
    (2, "IDENTIFY x, n"),
    (3, "COUNT <= x"),
    (4, "COMPUTE PR"),
    (5, "INTERPRET"),
    (6, "DECIDE + CHECK"),
]


def count_leq(data, x):
    return sum(value <= x for value in data)


def percentile_rank(data, x):
    return 100.0 * count_leq(data, x) / len(data)


def percentile_value_nplus1(data, k):
    """Class-3 interpolation convention used only to validate the continuity example."""
    values = sorted(data)
    position = (k / 100.0) * (len(values) + 1)
    if position <= 1:
        return float(values[0])
    if position >= len(values):
        return float(values[-1])
    lo = int(math.floor(position))
    frac = position - lo
    a = values[lo - 1]
    b = values[lo]
    return a + frac * (b - a)


def validate_all_data():
    # Class 3 continuity example.
    assert abs(percentile_value_nplus1(MAIN_DATA, 65) - 73.5) < 1e-12

    # Main data.
    assert MAIN_DATA == sorted(MAIN_DATA)
    assert len(MAIN_DATA) == 9
    assert count_leq(MAIN_DATA, 61) == 3
    assert abs(percentile_rank(MAIN_DATA, 61) - 33.3333333333) < 1e-8
    assert count_leq(MAIN_DATA, 72) == 6
    assert abs(percentile_rank(MAIN_DATA, 72) - 66.6666666667) < 1e-8
    assert count_leq(MAIN_DATA, 75) == 7
    assert abs(percentile_rank(MAIN_DATA, 75) - 77.7777777778) < 1e-8
    assert count_leq(MAIN_DATA, 81) == 8
    assert abs(percentile_rank(MAIN_DATA, 81) - 88.8888888889) < 1e-8

    # Same score, different surrounding group.
    assert GROUP_B == sorted(GROUP_B)
    assert len(GROUP_B) == 9
    assert count_leq(GROUP_B, 72) == 4
    assert abs(percentile_rank(GROUP_B, 72) - 44.4444444444) < 1e-8

    # Ties.
    assert TIES_DATA == sorted(TIES_DATA)
    assert len(TIES_DATA) == 9
    assert count_leq(TIES_DATA, 72) == 6
    assert abs(percentile_rank(TIES_DATA, 72) - 66.6666666667) < 1e-8

    # Guided challenge.
    assert CHALLENGE_DATA == sorted(CHALLENGE_DATA)
    assert len(CHALLENGE_DATA) == 10
    assert count_leq(CHALLENGE_DATA, 24) == 6
    assert percentile_rank(CHALLENGE_DATA, 24) == 60.0

    # Decision boundary and complement.
    assert percentile_rank(MAIN_DATA, 81) >= 80.0
    assert percentile_rank(MAIN_DATA, 75) < 80.0
    assert abs((100.0 - percentile_rank(MAIN_DATA, 81)) - 11.1111111111) < 1e-8


# =============================================================================
# MAIN LESSON
# =============================================================================
class Statistics10Class4PercentileRankV2(JPMathClassroomScene):
    """Value -> cumulative position -> percentile rank -> interpretation -> decision."""

    NAV_Y = -3.58
    STAGE_BOTTOM = -2.92

    def validate_lesson_data(self):
        validate_all_data()

    # ------------------------------------------------------------------
    # General visual helpers
    # ------------------------------------------------------------------
    def card(self, title, body_lines, width=5.8, height=2.0, *, body_size=27,
             title_size=22, math_body=None, fill=WHITE):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.8,
            fill_color=fill,
            fill_opacity=1.0,
        )
        title_m = self.text(title, title_size, BOLD)
        if math_body is not None:
            body = self.math(math_body, body_size + 8)
        else:
            if isinstance(body_lines, str):
                body_lines = [body_lines]
            body = VGroup(*[self.text(line, body_size, BOLD if i == 0 and len(body_lines) == 1 else NORMAL)
                            for i, line in enumerate(body_lines)])
            body.arrange(DOWN, aligned_edge=LEFT, buff=0.11)
        content = VGroup(title_m, body).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        self.fit(content, width - 0.55, height - 0.44)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.28)
        return VGroup(box, content)

    def formula_box(self, expression, width=8.5, height=1.15, font_size=40):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=PAPER_GRAY,
            fill_opacity=1.0,
        )
        eq = self.math(expression, font_size)
        self.fit(eq, width - 0.48, height - 0.24)
        eq.move_to(box)
        return VGroup(box, eq)

    def small_note(self, text, width=10.5):
        note = self.text(text, 21, MEDIUM).set_color(MID_GRAY)
        self.fit(note, width, 0.55)
        return note

    def make_data_row(self, values, *, target=None, y=0.0, compact=False,
                      qualify_count=0, dim_after=None, index_labels=False):
        cell_w = 0.92 if compact else 1.08
        cell_h = 0.66 if compact else 0.80
        font = 23 if compact else 28
        buff = 0.075 if compact else 0.095
        cells = VGroup()
        boxes, labels = [], []
        indices = VGroup()
        for i, value in enumerate(values):
            is_target = target is not None and value == target
            is_qualifying = i < qualify_count
            fill = VERY_LIGHT_GRAY if is_qualifying else WHITE
            stroke = BLACK_LINE if (is_target or is_qualifying) else LIGHT_GRAY
            sw = 2.6 if is_target else (2.0 if is_qualifying else 1.25)
            text_color = MID_GRAY if dim_after is not None and i >= dim_after else BLACK_TEXT
            box = RoundedRectangle(
                width=cell_w,
                height=cell_h,
                corner_radius=0.07,
                stroke_color=stroke,
                stroke_width=sw,
                fill_color=fill,
                fill_opacity=1.0,
            )
            label = self.text(str(value), font, BOLD if is_target else MEDIUM).set_color(text_color)
            label.move_to(box)
            cell = VGroup(box, label)
            cells.add(cell); boxes.append(box); labels.append(label)
        cells.arrange(RIGHT, buff=buff).move_to(UP * y)
        if index_labels:
            for i, cell in enumerate(cells, start=1):
                idx = self.text(str(i), 16, MEDIUM).set_color(MID_GRAY)
                idx.next_to(cell, DOWN, buff=0.08)
                indices.add(idx)
        group = VGroup(cells, indices) if index_labels else VGroup(cells)
        return {"group": group, "cells": cells, "boxes": boxes, "labels": labels, "indices": indices}

    def step_navigation(self, active=None):
        panel = RoundedRectangle(
            width=15.1,
            height=1.00,
            corner_radius=0.10,
            stroke_color=LIGHT_GRAY,
            stroke_width=1.3,
            fill_color=WHITE,
            fill_opacity=1.0,
        )
        widths = [2.05, 2.45, 2.25, 2.25, 2.18, 2.62]
        cards = VGroup()
        for (number, label), width in zip(STEP_LABELS, widths):
            active_now = number == active
            card = RoundedRectangle(
                width=width,
                height=0.74,
                corner_radius=0.07,
                stroke_color=BLACK_LINE if active_now else LIGHT_GRAY,
                stroke_width=2.2 if active_now else 1.1,
                fill_color=VERY_LIGHT_GRAY if active_now else WHITE,
                fill_opacity=1.0,
            )
            badge = Circle(
                radius=0.16,
                stroke_color=BLACK_LINE,
                stroke_width=1.4,
                fill_color=BLACK_LINE if active_now else WHITE,
                fill_opacity=1.0,
            )
            n = self.text(str(number), 16, BOLD)
            if active_now:
                n.set_color(WHITE)
            n.move_to(badge)
            lab = self.text(label, 18, BOLD if active_now else MEDIUM)
            self.fit(lab, width - 0.58, 0.44)
            content = VGroup(VGroup(badge, n), lab).arrange(RIGHT, buff=0.10).move_to(card)
            cards.add(VGroup(card, content))
        cards.arrange(RIGHT, buff=0.07).move_to(panel)
        nav = VGroup(panel, cards).move_to(UP * self.NAV_Y)
        assert nav.get_bottom()[1] > -4.42 and nav.get_top()[1] < -3.00
        return nav

    def swap_step(self, old_nav, active):
        new_nav = self.step_navigation(active)
        self.play(ReplacementTransform(old_nav, new_nav), run_time=RUN_QUICK)
        return new_nav

    def axis_base(self, *, width=11.8, y=-0.1, ticks=(0, 25, 50, 75, 100),
                  label_suffix="%"):
        x0, x1 = -width / 2.0, width / 2.0
        base = Line([x0, y, 0], [x1, y, 0], color=BLACK_LINE, stroke_width=2.4)
        tick_group = VGroup(); label_group = VGroup()
        for p in ticks:
            x = x0 + width * p / 100.0
            tick = Line([x, y - 0.11, 0], [x, y + 0.11, 0], color=BLACK_LINE, stroke_width=1.5)
            lab = self.text(f"{p:g}{label_suffix}", 18, MEDIUM).next_to(tick, DOWN, buff=0.10)
            tick_group.add(tick); label_group.add(lab)
        group = VGroup(base, tick_group, label_group)
        assert group.get_left()[0] > -7.7 and group.get_right()[0] < 7.7
        return group, x0

    def axis_marker(self, rank, value_label, *, width=11.8, y=-0.1, rank_below=True,
                    value_size=22, rank_size=20):
        x0 = -width / 2.0
        x = x0 + width * rank / 100.0
        marker = Triangle(
            stroke_color=BLACK_LINE,
            fill_color=BLACK_LINE,
            fill_opacity=1.0,
        ).scale(0.12).rotate(PI).move_to([x, y + 0.34, 0])
        value = self.text(value_label, value_size, BOLD).next_to(marker, UP, buff=0.09)
        rank_text = self.text(f"{rank:.1f}%", rank_size, BOLD)
        if rank_below:
            rank_text.move_to([x, y - 0.47, 0])
        else:
            rank_text.next_to(value, UP, buff=0.06)
        return VGroup(marker, value, rank_text)

    def animate_cumulative_count(self, row, count, *, counter_pos=DOWN * 1.15,
                                 wait_each=0.30, check_size=22, show_checks=True):
        label = self.text("COUNT AT OR BELOW", 21, BOLD)
        number = self.text("0", 34, BOLD)
        counter_box = RoundedRectangle(
            width=3.4, height=1.10, corner_radius=0.10,
            stroke_color=BLACK_LINE, stroke_width=1.7,
            fill_color=WHITE, fill_opacity=1.0,
        )
        content = VGroup(label, number).arrange(DOWN, buff=0.08).move_to(counter_box)
        counter = VGroup(counter_box, content).move_to(counter_pos)
        self.play(FadeIn(counter), run_time=RUN_QUICK)
        checks = VGroup()
        for i in range(count):
            new_number = self.text(str(i + 1), 34, BOLD).move_to(number)
            anims = [
                row["boxes"][i].animate.set_fill(VERY_LIGHT_GRAY, opacity=1.0).set_stroke(BLACK_LINE, width=2.0),
                ReplacementTransform(number, new_number),
            ]
            if show_checks:
                check = self.text("✓", check_size, BOLD).next_to(row["cells"][i], UP, buff=0.08)
                checks.add(check)
                anims.append(FadeIn(check, shift=DOWN * 0.05))
            self.play(*anims, run_time=0.42)
            number = new_number
            self.wait(wait_each)
        return counter, checks

    def claim_card(self, letter, claim_lines, truth, reason=None):
        width, height = 12.4, 1.45 if reason is None else 1.70
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.10,
            stroke_color=BLACK_LINE, stroke_width=1.6,
            fill_color=WHITE, fill_opacity=1.0,
        )
        badge = Circle(radius=0.26, stroke_color=BLACK_LINE, stroke_width=1.5,
                       fill_color=VERY_LIGHT_GRAY, fill_opacity=1.0)
        btxt = self.text(letter, 19, BOLD).move_to(badge)
        claim = VGroup(*[self.text(line, 23) for line in claim_lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        truth_m = self.text(truth, 28, BOLD)
        row = VGroup(VGroup(badge, btxt), claim, truth_m).arrange(RIGHT, buff=0.34)
        if reason:
            reason_m = self.text(reason, 19, MEDIUM).set_color(MID_GRAY)
            content = VGroup(row, reason_m).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        else:
            content = row
        self.fit(content, width - 0.55, height - 0.30)
        content.move_to(box)
        return VGroup(box, content)

    # ------------------------------------------------------------------
    # Timeline
    # ------------------------------------------------------------------
    def construct(self):
        self.scene_01_reverse_question()
        self.scene_02_same_score_different_group()
        self.scene_03_visual_meaning()
        self.scene_04_formal_definition()
        self.scene_05_six_step_method()
        self.scene_06_worked_pr72()
        self.scene_07_compare_three_positions()
        self.scene_08_top20_decision()
        self.scene_09_ties()
        self.scene_10_misconception_clinic()
        self.scene_11_value_vs_rank()
        self.scene_12_guided_challenge()
        self.scene_13_exit_ticket()
        self.scene_14_final_map()
        self.scene_15_normal_distribution_preview()

    # ------------------------------------------------------------------
    # 01. Continuity with Class 3
    # ------------------------------------------------------------------
    def scene_01_reverse_question(self):
        self.set_header(1, "REVERSE THE QUESTION", "Class 3: position → value. Class 4: value → relative position.")

        def direction_card(title, equation, given, find):
            box = RoundedRectangle(width=6.2, height=3.05, corner_radius=0.12,
                                   stroke_color=BLACK_LINE, stroke_width=1.8,
                                   fill_color=WHITE, fill_opacity=1.0)
            title_m = self.text(title, 24, BOLD)
            eq = self.math(equation, 42)
            given_m = self.text(f"GIVEN: {given}", 22)
            find_m = self.text(f"FIND: {find}", 22, BOLD)
            content = VGroup(title_m, eq, given_m, find_m).arrange(DOWN, buff=0.22)
            self.fit(content, 5.65, 2.55); content.move_to(box)
            return VGroup(box, content)

        left = direction_card("CLASS 3", r"P_{65}\ \longrightarrow\ 73.5", "relative position", "data value")
        right = direction_card("CLASS 4", r"72\ \longrightarrow\ ?", "data value", "relative position")
        pair = VGroup(left, right).arrange(RIGHT, buff=0.55).move_to(UP * 0.62)
        arrows = VGroup(
            self.text("POSITION  →  VALUE", 25, BOLD),
            self.text("VALUE  →  POSITION", 25, BOLD),
        ).arrange(RIGHT, buff=2.15).move_to(DOWN * 1.15)
        takeaway = self.card(
            "TODAY'S QUESTION",
            ["The DATA VALUE is known.", "We want to know WHERE IT STANDS."],
            width=10.8, height=1.45, body_size=26, fill=PAPER_GRAY,
        ).move_to(DOWN * 2.35)

        self.play(FadeIn(left, shift=RIGHT * 0.12), run_time=RUN_NORMAL)
        self.wait(1.8)
        self.play(FadeIn(right, shift=LEFT * 0.12), run_time=RUN_NORMAL)
        self.wait(1.8)
        self.play(FadeIn(arrows), run_time=RUN_NORMAL)
        self.wait(2.0)
        self.play(FadeIn(takeaway), run_time=RUN_NORMAL)
        self.wait(3.0)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 02. Hook: same score, different group
    # ------------------------------------------------------------------
    def scene_02_same_score_different_group(self):
        self.set_header(2, "SAME SCORE, DIFFERENT POSITION", "Does the same score always have the same relative position?")
        question = self.text("Two students both score 72. Are they in the same relative position?", 31, BOLD)
        self.fit(question, 13.7, 0.65); question.move_to(UP * 2.05)

        label_a = self.text("CLASS A", 23, BOLD).move_to(LEFT * 6.35 + UP * 0.85)
        row_a = self.make_data_row(MAIN_DATA, target=72, y=0.80, compact=True, dim_after=6)
        row_a["group"].shift(LEFT * 3.25)
        label_b = self.text("CLASS B", 23, BOLD).move_to(LEFT * 6.35 + DOWN * 0.50)
        row_b = self.make_data_row(GROUP_B, target=72, y=-0.55, compact=True, dim_after=4)
        row_b["group"].shift(LEFT * 3.25)

        a_result = self.card("CLASS A", ["6 of 9 at or below 72", "PR_A(72) ≈ 66.7%"], width=4.9, height=1.55, body_size=22)
        b_result = self.card("CLASS B", ["4 of 9 at or below 72", "PR_B(72) ≈ 44.4%"], width=4.9, height=1.55, body_size=22)
        VGroup(a_result, b_result).arrange(DOWN, buff=0.24).move_to(RIGHT * 4.65 + UP * 0.10)

        same_not_same = self.formula_box(r"\mathrm{SAME\ VALUE}\ \neq\ \mathrm{SAME\ RELATIVE\ POSITION}", width=11.3, height=1.05, font_size=34)
        same_not_same.move_to(DOWN * 2.10)
        conclusion = self.text("Percentile rank depends on the group around the value.", 27, BOLD).move_to(DOWN * 2.85)

        self.play(Write(question), run_time=RUN_NORMAL)
        self.wait(2.3)
        self.play(FadeIn(label_a), FadeIn(row_a["group"]), run_time=RUN_NORMAL)
        self.wait(1.8)
        self.play(FadeIn(a_result), run_time=RUN_NORMAL)
        self.wait(2.2)
        self.play(FadeIn(label_b), FadeIn(row_b["group"]), run_time=RUN_NORMAL)
        floating = row_a["cells"][5].copy().set_z_index(10)
        self.add(floating)
        self.play(floating.animate.move_to(row_b["cells"][3]).scale(1.08), run_time=RUN_SLOW)
        self.play(FadeOut(floating), FadeIn(b_result), run_time=RUN_NORMAL)
        self.wait(2.5)
        self.play(FadeIn(same_not_same), run_time=RUN_NORMAL)
        self.wait(2.0)
        self.play(Write(conclusion), run_time=RUN_NORMAL)
        self.wait(3.0)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 03. Build meaning visually BEFORE formula
    # ------------------------------------------------------------------
    def scene_03_visual_meaning(self):
        self.set_header(3, "SEE THE RELATIVE POSITION", "First see the group. Then count. The formula comes later.")
        q = self.text("Where does 72 stand?", 35, BOLD).move_to(UP * 2.00)
        row = self.make_data_row(MAIN_DATA, target=72, y=0.85, dim_after=6, index_labels=False)
        self.play(Write(q), run_time=RUN_NORMAL)
        self.play(FadeIn(row["group"]), run_time=RUN_NORMAL)
        self.wait(2.0)
        counter, checks = self.animate_cumulative_count(row, 6, counter_pos=DOWN * 0.62, wait_each=0.25)
        self.wait(1.6)

        chain = VGroup(
            self.text("6 out of 9", 28, BOLD),
            self.math(r"\frac{6}{9}", 43),
            self.text("0.666...", 28, BOLD),
            self.text("66.7%", 34, BOLD),
        ).arrange(RIGHT, buff=0.48).move_to(DOWN * 1.75)
        arrows = VGroup(*[
            Arrow(chain[i].get_right(), chain[i + 1].get_left(), buff=0.10, color=BLACK_LINE, stroke_width=1.8)
            for i in range(3)
        ])
        self.play(FadeIn(chain[0]), run_time=RUN_QUICK)
        for i in range(3):
            self.play(GrowArrow(arrows[i]), FadeIn(chain[i + 1]), run_time=RUN_NORMAL)
            self.wait(0.8)

        axis, _ = self.axis_base(width=11.4, y=-2.30, ticks=(0, 25, 50, 75, 100))
        marker = self.axis_marker(66.7, "72", width=11.4, y=-2.30, rank_below=False)
        marker[2].set_opacity(0)
        self.play(FadeOut(counter), FadeIn(axis), run_time=RUN_NORMAL)
        self.play(FadeIn(marker[0]), FadeIn(marker[1]), run_time=RUN_NORMAL)
        self.wait(2.0)
        definition = self.text("Percentile rank = percentage of observations at or below a given value.", 25, BOLD)
        self.fit(definition, 13.4, 0.55); definition.move_to(DOWN * 3.15)
        self.play(Write(definition), run_time=RUN_NORMAL)
        self.wait(3.0)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 04. Formal definition after the intuition
    # ------------------------------------------------------------------
    def scene_04_formal_definition(self):
        self.set_header(4, "FORMAL DEFINITION", "The formula records the visual idea we just counted.")
        label = self.text("PERCENTILE RANK", 27, BOLD).move_to(UP * 1.75)
        readable = self.formula_box(
            r"\mathrm{PR}(x)=\frac{\#\{\mathrm{observations}\le x\}}{n}\times100",
            width=10.8, height=1.35, font_size=42,
        ).move_to(UP * 0.55)
        equivalent = self.math(r"\mathrm{PR}(x)=100\times\frac{\mathrm{count(values\le x)}}{n}", 36).move_to(DOWN * 0.55)
        convention = self.card(
            "CLASSROOM CONVENTION",
            ["We count observations AT OR BELOW x.", "The symbol <= includes the target value."],
            width=10.4, height=1.55, body_size=24, fill=PAPER_GRAY,
        ).move_to(DOWN * 1.70)
        note = self.small_note("Different books or software may use other ranking conventions. In this class, use this rule consistently.", 12.8)
        note.move_to(DOWN * 2.78)

        self.play(FadeIn(label), run_time=RUN_QUICK)
        self.play(FadeIn(readable), run_time=RUN_NORMAL)
        self.wait(2.4)
        self.play(Write(equivalent), run_time=RUN_NORMAL)
        self.wait(2.0)
        self.play(FadeIn(convention), run_time=RUN_NORMAL)
        self.wait(2.7)
        self.play(FadeIn(note), run_time=RUN_NORMAL)
        self.wait(3.0)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 05. Six-step navigator
    # ------------------------------------------------------------------
    def scene_05_six_step_method(self):
        self.set_header(5, "SIX STEPS FOR PERCENTILE RANK", "Use the same route every time.")
        cards = VGroup()
        labels = [
            ("1", "ORDER DATA"),
            ("2", "IDENTIFY x, n"),
            ("3", "COUNT <= x"),
            ("4", "COMPUTE PR"),
            ("5", "INTERPRET"),
            ("6", "DECIDE + CHECK"),
        ]
        for n, txt in labels:
            box = RoundedRectangle(width=6.2, height=0.86, corner_radius=0.08,
                                   stroke_color=BLACK_LINE, stroke_width=1.6,
                                   fill_color=WHITE, fill_opacity=1.0)
            badge = RoundedRectangle(width=0.72, height=0.54, corner_radius=0.07,
                                     stroke_color=BLACK_LINE, stroke_width=1.5,
                                     fill_color=VERY_LIGHT_GRAY, fill_opacity=1.0)
            b = self.text(n, 20, BOLD).move_to(badge)
            t = self.text(txt, 25, BOLD)
            content = VGroup(VGroup(badge, b), t).arrange(RIGHT, buff=0.24).move_to(box)
            cards.add(VGroup(box, content))
        cards.arrange_in_grid(rows=3, cols=2, buff=(0.50, 0.30)).move_to(UP * 0.15)
        route = self.text("SEE  →  COUNT  →  LOCATE  →  FORMALIZE  →  INTERPRET  →  DECIDE", 25, BOLD)
        route.move_to(DOWN * 2.45)

        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in cards], lag_ratio=0.14), run_time=RUN_SLOW * 2.2)
        self.wait(2.8)
        self.play(Write(route), run_time=RUN_NORMAL)
        self.wait(3.0)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 06. Full worked example PR(72)
    # ------------------------------------------------------------------
    def scene_06_worked_pr72(self):
        self.set_header(6, "FULL WORKED EXAMPLE — PR(72)", "Run the complete six-step method and check whether the result is reasonable.")
        nav = self.step_navigation(1)
        self.play(FadeIn(nav), run_time=RUN_NORMAL)
        row = self.make_data_row(MAIN_DATA, target=72, y=1.05, index_labels=True)
        prompt = self.text("STEP 1 — DATA ARE ALREADY ORDERED", 28, BOLD).move_to(UP * 2.00)
        self.play(Write(prompt), FadeIn(row["group"]), run_time=RUN_NORMAL)
        self.wait(2.2)

        nav = self.swap_step(nav, 2)
        p2 = self.text("STEP 2 — IDENTIFY x AND n", 28, BOLD).move_to(prompt)
        self.play(ReplacementTransform(prompt, p2), run_time=RUN_NORMAL)
        xn = VGroup(
            self.card("TARGET", "x = 72", width=3.3, height=1.08, body_size=24),
            self.card("TOTAL", "n = 9", width=3.3, height=1.08, body_size=24),
        ).arrange(RIGHT, buff=0.34).move_to(DOWN * 0.30)
        self.play(FadeIn(xn), run_time=RUN_NORMAL)
        self.wait(1.8)

        nav = self.swap_step(nav, 3)
        p3 = self.text("STEP 3 — COUNT VALUES <= 72", 28, BOLD).move_to(p2)
        self.play(ReplacementTransform(p2, p3), FadeOut(xn), run_time=RUN_NORMAL)
        counter, checks = self.animate_cumulative_count(row, 6, counter_pos=DOWN * 0.78, wait_each=0.15)
        self.wait(1.4)
        count_text = self.text("6 observations", 25, BOLD).move_to(DOWN * 1.58)
        self.play(Write(count_text), run_time=RUN_QUICK)

        nav = self.swap_step(nav, 4)
        p4 = self.text("STEP 4 — COMPUTE PR", 28, BOLD).move_to(p3)
        calc = self.math(r"\frac{6}{9}\times100=66.666\ldots\approx66.7\%", 38).move_to(DOWN * 2.25)
        self.play(ReplacementTransform(p3, p4), FadeOut(counter), run_time=RUN_NORMAL)
        self.play(Write(calc), run_time=RUN_NORMAL)
        self.wait(2.0)

        nav = self.swap_step(nav, 5)
        p5 = self.text("STEP 5 — INTERPRET", 28, BOLD).move_to(p4)
        interp = self.card(
            "INTERPRETATION",
            ["About 66.7% of the observations are at or below 72.",
             "72 is approximately at the 67th percentile."],
            width=11.7, height=1.52, body_size=22, fill=PAPER_GRAY,
        ).move_to(DOWN * 1.48)
        self.play(ReplacementTransform(p4, p5), FadeOut(VGroup(calc, count_text)), run_time=RUN_NORMAL)
        self.play(FadeIn(interp), run_time=RUN_NORMAL)
        self.wait(2.5)

        nav = self.swap_step(nav, 6)
        p6 = self.text("STEP 6 — DECIDE + CHECK", 28, BOLD).move_to(p5)
        check = self.card(
            "SANITY CHECK",
            ["6 out of 9 is about two-thirds.", "66.7% is reasonable."],
            width=8.3, height=1.40, body_size=23,
        ).move_to(DOWN * 0.05)
        self.play(ReplacementTransform(p5, p6), FadeOut(interp), run_time=RUN_NORMAL)
        self.play(FadeIn(check), run_time=RUN_NORMAL)
        self.wait(3.0)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 07. Compare three relative positions on one axis
    # ------------------------------------------------------------------
    def scene_07_compare_three_positions(self):
        self.set_header(7, "COMPARE THREE POSITIONS", "Use one percentile scale so the relative positions can be compared directly.")
        row = self.make_data_row(MAIN_DATA, y=1.45, compact=True)
        self.play(FadeIn(row["group"]), run_time=RUN_NORMAL)
        self.wait(1.6)
        axis, _ = self.axis_base(width=11.6, y=-0.20, ticks=(0, 25, 50, 75, 100))
        self.play(FadeIn(axis), run_time=RUN_NORMAL)
        markers = [
            self.axis_marker(33.3, "61", width=11.6, y=-0.20),
            self.axis_marker(66.7, "72", width=11.6, y=-0.20),
            self.axis_marker(88.9, "81", width=11.6, y=-0.20),
        ]
        for marker in markers:
            self.play(FadeIn(marker[0]), FadeIn(marker[1]), FadeIn(marker[2]), run_time=RUN_NORMAL)
            self.wait(1.3)
        note = self.card(
            "RELATIVE POSITION",
            ["PR(61) ≈ 33.3%", "PR(72) ≈ 66.7%", "PR(81) ≈ 88.9%"],
            width=5.0, height=1.55, body_size=21,
        ).move_to(DOWN * 1.95 + LEFT * 3.25)
        conclusion = self.card(
            "CONCLUSION",
            ["Higher percentile rank = higher relative position", "in this dataset."],
            width=6.7, height=1.55, body_size=22, fill=PAPER_GRAY,
        ).move_to(DOWN * 1.95 + RIGHT * 2.85)
        caution = self.small_note("Percentile-rank gaps do not mean equal raw-score gaps.", 10.2).move_to(DOWN * 2.95)
        self.play(FadeIn(note), FadeIn(conclusion), run_time=RUN_NORMAL)
        self.wait(2.4)
        self.play(FadeIn(caution), run_time=RUN_NORMAL)
        self.wait(3.0)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 08. Top-20% decision boundary
    # ------------------------------------------------------------------
    def scene_08_top20_decision(self):
        self.set_header(8, "DECISION MAKING — TOP 20%", "Turn relative position into a clear threshold before testing a score.")
        nav = self.step_navigation(6)
        self.play(FadeIn(nav), run_time=RUN_NORMAL)
        context = self.text("A program selects approximately the TOP 20% of the group.", 30, BOLD).move_to(UP * 2.00)
        threshold = self.formula_box(r"\mathrm{TOP\ 20\%}\ \Longrightarrow\ \mathrm{use\ }PR(x)\ge80", width=9.5, height=1.10, font_size=37)
        threshold.move_to(UP * 1.00)
        self.play(Write(context), run_time=RUN_NORMAL)
        self.wait(2.0)
        self.play(FadeIn(threshold), run_time=RUN_NORMAL)
        self.wait(2.2)

        axis, x0 = self.axis_base(width=11.4, y=-0.30, ticks=(0, 20, 40, 60, 80, 100))
        x80 = x0 + 11.4 * 0.80
        region = Rectangle(width=11.4 * 0.20, height=0.22, stroke_width=0,
                           fill_color=LIGHT_GRAY, fill_opacity=0.85)
        region.move_to([(x80 + 11.4 / 2) / 2, -0.88, 0])
        bracket = Line([x80, -0.68, 0], [11.4 / 2, -0.68, 0], color=BLACK_LINE, stroke_width=5)
        top_label = self.text("TOP 20% REGION", 19, BOLD).next_to(bracket, DOWN, buff=0.09)
        threshold_line = DashedLine([x80, -0.72, 0], [x80, 0.50, 0], color=MID_GRAY, stroke_width=1.8)
        threshold_label = self.text("80% threshold", 19, BOLD).move_to([x80 - 0.72, 0.68, 0])
        self.play(FadeIn(axis), FadeIn(region), Create(bracket), FadeIn(top_label), Create(threshold_line), FadeIn(threshold_label), run_time=RUN_NORMAL)
        self.wait(2.3)

        m81 = self.axis_marker(88.9, "81", width=11.4, y=-0.30, rank_below=False)
        rank81 = self.text("PR = 88.9%", 20, BOLD).next_to(m81[1], UP, buff=0.05)
        self.play(FadeIn(m81[0]), FadeIn(m81[1]), FadeIn(rank81), run_time=RUN_NORMAL)
        self.wait(1.8)
        decision81 = self.card(
            "81",
            ["88.9 >= 80", "YES — qualifies under this rule."],
            width=5.7, height=1.35, body_size=22,
        ).move_to(DOWN * 1.80 + LEFT * 3.15)
        complement = self.card(
            "CHECK ABOVE 81",
            ["100% - 88.9% = 11.1%", "11.1% <= 20%"],
            width=5.9, height=1.35, body_size=21, fill=PAPER_GRAY,
        ).move_to(DOWN * 1.80 + RIGHT * 3.05)
        self.play(FadeIn(decision81), run_time=RUN_NORMAL)
        self.play(FadeIn(complement), run_time=RUN_NORMAL)
        self.wait(2.3)

        m75 = self.axis_marker(77.8, "75", width=11.4, y=-0.30, rank_below=False)
        compare75 = self.text("PR(75) ≈ 77.8% < 80%  →  75 does NOT qualify.", 24, BOLD).move_to(DOWN * 2.72)
        self.play(FadeIn(m75[0]), FadeIn(m75[1]), run_time=RUN_NORMAL)
        self.play(Write(compare75), run_time=RUN_NORMAL)
        self.wait(3.0)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 09. Ties and the <= convention
    # ------------------------------------------------------------------
    def scene_09_ties(self):
        self.set_header(9, "TIES MATTER", "Under our classroom rule, every value equal to x is included in the cumulative count.")
        q = self.text("Find PR(72) when 72 appears three times.", 32, BOLD).move_to(UP * 1.95)
        row = self.make_data_row(TIES_DATA, target=72, y=0.85, dim_after=6)
        self.play(Write(q), FadeIn(row["group"]), run_time=RUN_NORMAL)
        self.wait(2.0)
        counter, checks = self.animate_cumulative_count(row, 6, counter_pos=DOWN * 0.55, wait_each=0.18)
        self.wait(1.5)
        rule = self.text("All three 72 values count because value <= 72.", 25, BOLD).move_to(DOWN * 1.48)
        calc = self.math(r"PR(72)=100\left(\frac{6}{9}\right)\approx66.7\%", 37).move_to(DOWN * 2.13)
        conclusion = self.small_note("Equal values receive the same cumulative percentile rank under this classroom convention.", 13.0)
        conclusion.move_to(DOWN * 2.85)
        self.play(Write(rule), run_time=RUN_NORMAL)
        self.play(Write(calc), run_time=RUN_NORMAL)
        self.wait(2.0)
        self.play(FadeIn(conclusion), run_time=RUN_NORMAL)
        self.wait(3.0)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 10. Misconception clinic
    # ------------------------------------------------------------------
    def scene_10_misconception_clinic(self):
        self.set_header(10, "MISCONCEPTION CLINIC", "Read the meaning carefully: percentile rank describes position, not the raw score itself.")
        a = self.claim_card("A", ["PR(72) = 66.7 means", "the score itself is 66.7."], "FALSE")
        b = self.claim_card("B", ["PR(72) = 66.7 means 66.7%", "are at or below 72."], "TRUE")
        c = self.claim_card("C", ["PR(72) = 66.7 means exactly 66.7%", "scored LOWER than 72."], "FALSE", "Reason: our formula uses AT OR BELOW.")
        group = VGroup(a, b, c).arrange(DOWN, buff=0.23).move_to(DOWN * 0.15)
        self.play(FadeIn(a), run_time=RUN_NORMAL)
        self.wait(1.8)
        self.play(FadeIn(b), run_time=RUN_NORMAL)
        self.wait(1.8)
        self.play(FadeIn(c), run_time=RUN_NORMAL)
        self.wait(3.2)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 11. Percentile value versus percentile rank
    # ------------------------------------------------------------------
    def scene_11_value_vs_rank(self):
        self.set_header(11, "PERCENTILE VALUE VS PERCENTILE RANK", "The direction of the question changes, so the input and output change too.")

        def distinction_card(title, input_line, question_line, equation, output_line):
            box = RoundedRectangle(width=6.45, height=3.65, corner_radius=0.12,
                                   stroke_color=BLACK_LINE, stroke_width=1.8,
                                   fill_color=WHITE, fill_opacity=1.0)
            title_m = self.text(title, 25, BOLD)
            inp = self.text(input_line, 21)
            q = self.text(question_line, 20)
            self.fit(q, 5.85, 0.52)
            eq = self.math(equation, 38)
            out = self.text(output_line, 21, BOLD)
            content = VGroup(title_m, inp, q, eq, out).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            self.fit(content, 5.85, 3.10); content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.30)
            return VGroup(box, content)

        left = distinction_card(
            "PERCENTILE VALUE",
            "INPUT: percentile k",
            "QUESTION: Which VALUE corresponds to k?",
            r"P_{65}\approx73.5",
            "OUTPUT: original data units",
        )
        right = distinction_card(
            "PERCENTILE RANK",
            "INPUT: observed value x",
            "QUESTION: What percentage is at or below x?",
            r"PR(72)\approx66.7\%",
            "OUTPUT: percent / relative position",
        )
        pair = VGroup(left, right).arrange(RIGHT, buff=0.42).move_to(UP * 0.35)
        arrows = VGroup(
            self.text("POSITION  →  VALUE", 23, BOLD),
            self.text("VALUE  →  POSITION", 23, BOLD),
        ).arrange(RIGHT, buff=2.10).move_to(DOWN * 1.82)
        neq = self.math(r"P_{65}\neq PR(65)", 40).move_to(DOWN * 2.42)
        expl = self.text("P65 asks for a VALUE.  PR(65) asks where the VALUE 65 stands.", 23, BOLD)
        self.fit(expl, 13.2, 0.55); expl.move_to(DOWN * 3.02)
        self.play(FadeIn(pair), run_time=RUN_NORMAL)
        self.wait(2.8)
        self.play(FadeIn(arrows), run_time=RUN_NORMAL)
        self.wait(2.0)
        self.play(Write(neq), run_time=RUN_NORMAL)
        self.play(Write(expl), run_time=RUN_NORMAL)
        self.wait(3.0)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 12. Guided challenge with real thinking pause
    # ------------------------------------------------------------------
    def scene_12_guided_challenge(self):
        self.set_header(12, "GUIDED CHALLENGE — YOUR TURN", "Find PR(24). Think through the first three steps before the answer appears.")
        nav = self.step_navigation(None)
        row = self.make_data_row(CHALLENGE_DATA, target=24, y=1.15, compact=True)
        prompt = self.text("Find PR(24).", 34, BOLD).move_to(UP * 2.05)
        think = self.card(
            "THINK",
            ["1. What is x?", "2. What is n?", "3. How many values are <= 24?"],
            width=7.1, height=1.65, body_size=23, fill=PAPER_GRAY,
        ).move_to(DOWN * 0.30)
        self.play(FadeIn(nav), Write(prompt), FadeIn(row["group"]), run_time=RUN_NORMAL)
        self.play(FadeIn(think), run_time=RUN_NORMAL)
        self.wait(6.0)
        self.play(FadeOut(think), run_time=RUN_QUICK)
        counter, checks = self.animate_cumulative_count(row, 6, counter_pos=DOWN * 0.55, wait_each=0.16)
        self.wait(1.2)
        calc = self.math(r"PR(24)=100\left(\frac{6}{10}\right)=60\%", 39).move_to(DOWN * 1.55)
        interp = self.card(
            "INTERPRETATION",
            ["60% of the observations are at or below 24.", "24 is at the 60th percentile under our convention."],
            width=11.0, height=1.36, body_size=21,
        ).move_to(DOWN * 2.22)
        self.play(FadeOut(counter), Write(calc), run_time=RUN_NORMAL)
        self.wait(1.8)
        self.play(FadeIn(interp), run_time=RUN_NORMAL)
        self.wait(3.0)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 13. Exit ticket
    # ------------------------------------------------------------------
    def scene_13_exit_ticket(self):
        self.set_header(13, "EXIT TICKET", "Estimate the relative position first; then confirm with a short count.")
        q = VGroup(
            self.text("Without a long calculation, where is PR(75)?", 31, BOLD),
            self.text("BELOW 50     •     BETWEEN 50 AND 80     •     ABOVE 80", 25, BOLD),
        ).arrange(DOWN, buff=0.28).move_to(UP * 1.80)
        row = self.make_data_row(MAIN_DATA, target=75, y=0.55)
        self.play(FadeIn(q), FadeIn(row["group"]), run_time=RUN_NORMAL)
        self.wait(7.0)
        count = self.text("7 of 9 values are <= 75.", 27, BOLD).move_to(DOWN * 0.70)
        calc = self.math(r"PR(75)=100\left(\frac{7}{9}\right)\approx77.8\%", 39).move_to(DOWN * 1.45)
        answer = self.card("CORRECT CATEGORY", "BETWEEN 50 AND 80", width=7.4, height=1.20, body_size=27, fill=PAPER_GRAY)
        answer.move_to(DOWN * 2.35)
        self.play(Write(count), run_time=RUN_NORMAL)
        self.play(Write(calc), run_time=RUN_NORMAL)
        self.wait(1.8)
        self.play(FadeIn(answer), run_time=RUN_NORMAL)
        self.wait(3.0)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 14. Final map with full use of screen space
    # ------------------------------------------------------------------
    def scene_14_final_map(self):
        self.set_header(14, "FINAL MAP — VALUE → POSITION → DECISION", "Use this route to reproduce the reasoning independently.")
        labels = [
            "OBSERVED VALUE x",
            "ORDER THE DATA",
            "COUNT VALUES <= x",
            "DIVIDE BY n",
            "× 100",
            "PERCENTILE RANK",
            "INTERPRET",
            "DECIDE",
        ]
        nodes = VGroup()
        for i, label in enumerate(labels):
            w = 3.55 if i not in (0, 5) else 4.0
            box = RoundedRectangle(width=w, height=0.78, corner_radius=0.08,
                                   stroke_color=BLACK_LINE, stroke_width=1.5,
                                   fill_color=VERY_LIGHT_GRAY if i in (0, 5) else WHITE,
                                   fill_opacity=1.0)
            t = self.text(label, 21 if len(label) < 19 else 19, BOLD).move_to(box)
            nodes.add(VGroup(box, t))
        nodes.arrange_in_grid(rows=2, cols=4, buff=(0.34, 0.80)).move_to(UP * 0.55)
        arrows = VGroup()
        for i in range(3):
            arrows.add(Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), buff=0.10, color=BLACK_LINE, stroke_width=1.8))
        # second row is read from right to left visually through a connector from node 3 to node 4
        connector = Arrow(nodes[3].get_bottom(), nodes[7].get_top(), buff=0.10, color=BLACK_LINE, stroke_width=1.8)
        arrows2 = VGroup(
            Arrow(nodes[7].get_left(), nodes[6].get_right(), buff=0.10, color=BLACK_LINE, stroke_width=1.8),
            Arrow(nodes[6].get_left(), nodes[5].get_right(), buff=0.10, color=BLACK_LINE, stroke_width=1.8),
            Arrow(nodes[5].get_left(), nodes[4].get_right(), buff=0.10, color=BLACK_LINE, stroke_width=1.8),
        )
        six_cards = self.process_map(
            [("1", "ORDER DATA"), ("2", "IDENTIFY x, n"), ("3", "COUNT <= x"),
             ("4", "COMPUTE PR"), ("5", "INTERPRET"), ("6", "DECIDE + CHECK")],
            card_width=3.9, card_height=0.86, columns=3,
        )
        six_cards.move_to(DOWN * 1.45)
        takeaway = self.text("A percentile rank is not just a calculation. It tells where a value stands inside a distribution.", 24, BOLD)
        self.fit(takeaway, 13.6, 0.58); takeaway.move_to(DOWN * 2.75)

        self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.06) for n in nodes], lag_ratio=0.08), run_time=RUN_SLOW * 1.9)
        self.play(LaggedStart(*[GrowArrow(a) for a in VGroup(*arrows, connector, *arrows2)], lag_ratio=0.10), run_time=RUN_SLOW * 1.6)
        self.wait(2.0)
        self.play(FadeOut(VGroup(nodes, arrows, connector, arrows2)), FadeIn(six_cards), run_time=RUN_NORMAL)
        self.wait(2.8)
        self.play(Write(takeaway), run_time=RUN_NORMAL)
        self.wait(3.2)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 15. Curricular bridge: intuitive normal-distribution preview only
    # ------------------------------------------------------------------
    def scene_15_normal_distribution_preview(self):
        self.set_header(15, "NEXT — FROM POSITION TO DISTRIBUTION SHAPE", "We now move from one value's position to the overall shape formed by many observations.")
        axis, _ = self.axis_base(width=11.5, y=0.45, ticks=(0, 25, 50, 75, 100))
        marker = self.axis_marker(66.7, "72", width=11.5, y=0.45, rank_below=True)
        self.play(FadeIn(axis), FadeIn(marker), run_time=RUN_NORMAL)
        self.wait(2.0)

        # Transform the idea of a single position into many observations.
        dots = VGroup()
        xs = np.linspace(-5.4, 5.4, 31)
        for x in xs:
            height = 2.0 * math.exp(-0.5 * (x / 2.15) ** 2)
            levels = max(1, int(round(height * 3.0)))
            for j in range(levels):
                dots.add(Dot([x, -1.15 + 0.18 * j, 0], radius=0.045, color=BLACK_LINE))
        curve = VMobject(stroke_color=BLACK_LINE, stroke_width=3.0)
        curve_pts = []
        for x in np.linspace(-5.5, 5.5, 90):
            y = -0.92 + 2.15 * math.exp(-0.5 * (x / 2.05) ** 2)
            curve_pts.append([x, y, 0])
        curve.set_points_smoothly(curve_pts)
        baseline = Line(LEFT * 5.8 + DOWN * 1.18, RIGHT * 5.8 + DOWN * 1.18, color=LIGHT_GRAY, stroke_width=1.5)

        self.play(FadeOut(VGroup(axis, marker)), FadeIn(baseline), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.015), run_time=RUN_SLOW * 2.3)
        self.wait(1.6)
        self.play(Create(curve), run_time=RUN_SLOW * 1.6)
        preview = self.card(
            "NEXT",
            ["FROM RELATIVE POSITION", "TO THE SHAPE OF A DISTRIBUTION"],
            width=8.2, height=1.35, body_size=24, fill=PAPER_GRAY,
        ).move_to(UP * 1.72)
        question = self.text("Why do many observations cluster near the center while fewer appear toward the extremes?", 23, BOLD)
        self.fit(question, 13.4, 0.55); question.move_to(DOWN * 2.15)
        final = self.text("NEXT CLASS  •  INTRODUCTION TO THE NORMAL DISTRIBUTION", 28, BOLD).move_to(DOWN * 2.82)
        self.play(FadeIn(preview), run_time=RUN_NORMAL)
        self.play(Write(question), run_time=RUN_NORMAL)
        self.wait(2.8)
        self.play(Write(final), run_time=RUN_NORMAL)
        self.wait(4.0)
        self.play(FadeOut(VGroup(dots, curve, baseline, preview, question, final)), run_time=RUN_NORMAL)


# Preview:
#   manim -pql statistics10_class4_percentile_rank_v2.py Statistics10Class4PercentileRankV2 --disable_caching
# Final:
#   manim -pqh statistics10_class4_percentile_rank_v2.py Statistics10Class4PercentileRankV2 --fps 30 --disable_caching
