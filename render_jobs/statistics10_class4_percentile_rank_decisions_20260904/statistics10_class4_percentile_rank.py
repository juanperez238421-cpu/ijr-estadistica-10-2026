#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statistics 10 · Class 4 · Percentile Rank & Decisions Based on Relative Position.

Direct continuation of Class 3:
    percentile -> value
becomes:
    raw value -> percentile rank -> relative-position decision

Class convention:
    PR(x) = 100 * count(observations <= x) / n

Target: Manim Community Edition 0.20.1, 1920x1080, 30 fps, white classroom style.
"""
from __future__ import annotations

from library.jp_classroom_style import *


MAIN_DATA = [52, 58, 61, 64, 68, 72, 75, 81, 88]
CHALLENGE_DATA = [12, 15, 17, 18, 21, 24, 27, 31, 34, 39]

STEP_LABELS = [
    (1, "ORDER DATA"),
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


def validate_all_data():
    assert MAIN_DATA == sorted(MAIN_DATA)
    assert len(MAIN_DATA) == 9
    assert count_leq(MAIN_DATA, 72) == 6
    assert abs(percentile_rank(MAIN_DATA, 72) - 66.6666666667) < 1e-8
    assert count_leq(MAIN_DATA, 61) == 3
    assert abs(percentile_rank(MAIN_DATA, 61) - 33.3333333333) < 1e-8
    assert count_leq(MAIN_DATA, 81) == 8
    assert abs(percentile_rank(MAIN_DATA, 81) - 88.8888888889) < 1e-8
    assert CHALLENGE_DATA == sorted(CHALLENGE_DATA)
    assert len(CHALLENGE_DATA) == 10
    assert count_leq(CHALLENGE_DATA, 24) == 6
    assert percentile_rank(CHALLENGE_DATA, 24) == 60.0


class Statistics10Class4PercentileRank(JPMathClassroomScene):
    """Value -> percentile rank -> interpretation -> decision."""

    def validate_lesson_data(self):
        validate_all_data()

    def card(self, title, body, width=5.8, height=2.0, body_math=False):
        box = RoundedRectangle(width=width, height=height, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=1.8, fill_color=WHITE, fill_opacity=1.0)
        title_m = self.text(title, 23, BOLD)
        body_m = self.math(body, 35) if body_math else self.text(body, 27, BOLD)
        self.fit(body_m, width - 0.50, height - 0.82)
        content = VGroup(title_m, body_m).arrange(DOWN, buff=0.18)
        content.move_to(box)
        return VGroup(box, content)

    def formula_box(self, expression, width=7.6, font_size=42, height=1.25):
        box = RoundedRectangle(width=width, height=height, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=2.0, fill_color=PAPER_GRAY, fill_opacity=1.0)
        eq = self.math(expression, font_size)
        self.fit(eq, width - 0.45, height - 0.24)
        eq.move_to(box)
        return VGroup(box, eq)

    def interpretation_box(self, lines, width=11.8, title="INTERPRETATION"):
        title_m = self.text(title, 22, BOLD)
        body = VGroup(*[self.text(line, 25 if len(line) < 70 else 22) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.11)
        content = VGroup(title_m, body).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        self.fit(content, width - 0.55, 2.0)
        box = RoundedRectangle(width=width, height=max(1.45, content.height + 0.50),
            corner_radius=0.12, stroke_color=BLACK_LINE, stroke_width=1.8,
            fill_color=PAPER_GRAY, fill_opacity=1.0)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.28)
        return VGroup(box, content)

    def make_data_row(self, values, *, show_indices=True, selected_value=None,
                      active_count=None, dim_after=None, y=0.3, compact=False):
        cell_w = 0.92 if compact else 1.12
        cell_h = 0.68 if compact else 0.82
        font = 23 if compact else 29
        buff = 0.08 if compact else 0.11
        cells = VGroup(); boxes = []; labels = []; indices = VGroup()
        for i, value in enumerate(values):
            fill = WHITE; stroke = LIGHT_GRAY; stroke_width = 1.4; text_color = BLACK_TEXT
            if active_count is not None and i < active_count:
                fill = VERY_LIGHT_GRAY; stroke = BLACK_LINE; stroke_width = 2.0
            if dim_after is not None and i >= dim_after:
                text_color = MID_GRAY; stroke = LIGHT_GRAY
            if selected_value is not None and value == selected_value:
                fill = LIGHT_GRAY; stroke = BLACK_LINE; stroke_width = 3.0
            box = RoundedRectangle(width=cell_w, height=cell_h, corner_radius=0.07,
                stroke_color=stroke, stroke_width=stroke_width, fill_color=fill, fill_opacity=1.0)
            label = self.text(str(value), font, BOLD if value == selected_value else NORMAL)
            label.set_color(text_color); label.move_to(box)
            cells.add(VGroup(box, label)); boxes.append(box); labels.append(label)
        cells.arrange(RIGHT, buff=buff); cells.move_to(UP * y)
        if show_indices:
            for i, cell in enumerate(cells, start=1):
                idx = self.text(str(i), 17, MEDIUM).set_color(MID_GRAY)
                idx.next_to(cell, DOWN, buff=0.10); indices.add(idx)
            group = VGroup(cells, indices)
        else:
            group = VGroup(cells)
        return {"group": group, "cells": cells, "boxes": boxes, "labels": labels, "indices": indices}

    def build_step_navigation(self, active=None):
        panel = RoundedRectangle(width=15.0, height=0.88, corner_radius=0.10,
            stroke_color=LIGHT_GRAY, stroke_width=1.4, fill_color=WHITE, fill_opacity=1.0)
        cards = VGroup(); widths = [2.20, 2.38, 2.20, 2.12, 2.20, 2.50]
        for (number, label), width in zip(STEP_LABELS, widths):
            is_active = number == active
            c = RoundedRectangle(width=width, height=0.66, corner_radius=0.07,
                stroke_color=BLACK_LINE if is_active else LIGHT_GRAY,
                stroke_width=2.2 if is_active else 1.0,
                fill_color=VERY_LIGHT_GRAY if is_active else WHITE, fill_opacity=1.0)
            badge = Circle(radius=0.15, stroke_color=BLACK_LINE, stroke_width=1.4,
                fill_color=BLACK_LINE if is_active else WHITE, fill_opacity=1.0)
            n = self.text(str(number), 15, BOLD)
            if is_active: n.set_color(WHITE)
            n.move_to(badge)
            lab = self.text(label, 14, BOLD if is_active else MEDIUM)
            self.fit(lab, width - 0.62, 0.42)
            content = VGroup(VGroup(badge, n), lab).arrange(RIGHT, buff=0.11); content.move_to(c)
            cards.add(VGroup(c, content))
        cards.arrange(RIGHT, buff=0.08); cards.move_to(panel)
        return VGroup(panel, cards).move_to(DOWN * 3.72)

    def swap_step(self, old_nav, active):
        new_nav = self.build_step_navigation(active)
        self.play(ReplacementTransform(old_nav, new_nav), run_time=RUN_QUICK)
        return new_nav

    def percentile_axis(self, rank=None, label=None, top_region_start=None, width=11.0, y=-0.25):
        x0, x1 = -width / 2, width / 2
        base = Line([x0, y, 0], [x1, y, 0], color=BLACK_LINE, stroke_width=2.2)
        ticks = VGroup(); labels = VGroup()
        for p in [0, 25, 50, 75, 100]:
            x = x0 + width * p / 100.0
            tick = Line([x, y - 0.10, 0], [x, y + 0.10, 0], color=BLACK_LINE, stroke_width=1.6)
            lab = self.text(f"{p}%", 19, MEDIUM).next_to(tick, DOWN, buff=0.10)
            ticks.add(tick); labels.add(lab)
        group = VGroup(base, ticks, labels)
        if top_region_start is not None:
            xs = x0 + width * top_region_start / 100.0
            region = Line([xs, y + 0.23, 0], [x1, y + 0.23, 0], color=MID_GRAY, stroke_width=8)
            region_label = self.text(f"TOP {100-top_region_start:.0f}%", 20, BOLD).next_to(region, UP, buff=0.08)
            group.add(region, region_label)
        marker = None
        if rank is not None:
            xr = x0 + width * rank / 100.0
            marker = Triangle(stroke_color=BLACK_LINE, fill_color=BLACK_LINE, fill_opacity=1).scale(0.13).rotate(PI).move_to([xr, y + 0.34, 0])
            mlabel = self.text(label or f"{rank:.1f}", 21, BOLD).next_to(marker, UP, buff=0.08)
            group.add(marker, mlabel)
        return group, marker

    def section_question(self, question, y=1.55, size=31):
        q = self.text(question, size, BOLD); self.fit(q, 13.6, 0.65); q.move_to(UP * y); return q

    def construct(self):
        self.scene_01_reverse_question(); self.scene_02_meaning(); self.scene_03_six_steps()
        self.scene_04_example_setup(); self.scene_05_count(); self.scene_06_compute()
        self.scene_07_interpret(); self.scene_08_compare(); self.scene_09_decision()
        self.scene_10_distinction(); self.scene_11_guided_challenge(); self.scene_12_final_recipe()
        self.final_closing()

    def scene_01_reverse_question(self):
        self.set_header(1, "REVERSE THE QUESTION", "Last class: percentile → value. Today: value → relative position.")
        left = self.card("CLASS 3", r"P_{65}\ \longrightarrow\ ?", 5.3, 2.10, True)
        right = self.card("CLASS 4", r"72\ \longrightarrow\ ?", 5.3, 2.10, True)
        VGroup(left, right).arrange(RIGHT, buff=0.75).move_to(UP * 0.55)
        class3_label = self.text("PERCENTILE → VALUE", 23, BOLD).next_to(left, DOWN, buff=0.15)
        class4_label = self.text("VALUE → PERCENTILE RANK", 23, BOLD).next_to(right, DOWN, buff=0.15)
        self.play(FadeIn(left, shift=RIGHT * 0.15), run_time=RUN_NORMAL); self.play(Write(class3_label), run_time=RUN_NORMAL); self.wait(2.0)
        solved = self.math(r"P_{65}\ \longrightarrow\ 73.5", 40).move_to(left[1][1])
        self.play(ReplacementTransform(left[1][1], solved), run_time=RUN_NORMAL); self.wait(2.2)
        self.play(FadeIn(right, shift=LEFT * 0.15), run_time=RUN_NORMAL); self.play(Write(class4_label), run_time=RUN_NORMAL); self.wait(2.0)
        arrow_down = Arrow(UP * 0.30, DOWN * 0.30, buff=0, color=BLACK_LINE, stroke_width=2.2)
        arrow_up = Arrow(DOWN * 0.30 + RIGHT * 0.25, UP * 0.30 + RIGHT * 0.25, buff=0, color=BLACK_LINE, stroke_width=2.2)
        q1 = self.text("PERCENTILE → VALUE", 24, BOLD); q2 = self.text("VALUE → POSITION", 24, BOLD)
        inversion_text = VGroup(q1, VGroup(arrow_down, arrow_up), q2).arrange(DOWN, buff=0.16).move_to(DOWN * 2.15)
        self.play(FadeIn(inversion_text), run_time=RUN_NORMAL); self.wait(2.4)
        msg = self.text("These are different questions.", 30, BOLD).move_to(DOWN * 2.95)
        self.play(Write(msg), run_time=RUN_NORMAL); self.wait(3.0); self.clear_stage()

    def scene_02_meaning(self):
        self.set_header(2, "PERCENTILE RANK = RELATIVE POSITION", "Percentile rank tells us the percentage of observations that are at or below a particular value.")
        q = self.text("Where does 72 stand inside this dataset?", 32, BOLD).move_to(UP * 1.85)
        axis, _ = self.percentile_axis(rank=66.7, label="72  ≈ 67th percentile", width=11.5, y=0.55)
        x0 = -11.5 / 2; x67 = x0 + 11.5 * 0.667
        progress = Line([x0, 0.55, 0], [x67, 0.55, 0], color=MID_GRAY, stroke_width=8)
        explain = self.interpretation_box(["About 67% of the observations", "are at or below 72."], width=8.8, title="RELATIVE POSITION").move_to(DOWN * 1.20)
        value_card = self.card("VALUE", "72", 3.3, 1.40); rank_card = self.card("PERCENTILE RANK", "≈ 67", 4.2, 1.40)
        pair = VGroup(value_card, rank_card).arrange(RIGHT, buff=0.55).move_to(DOWN * 2.55)
        self.play(Write(q), run_time=RUN_NORMAL); self.wait(2.2)
        self.play(Create(axis[0]), FadeIn(axis[1]), FadeIn(axis[2]), run_time=RUN_NORMAL); self.wait(1.5)
        self.play(Create(progress), run_time=RUN_SLOW); self.play(FadeIn(VGroup(*axis[3:])), run_time=RUN_NORMAL); self.wait(2.8)
        self.play(FadeIn(explain), run_time=RUN_NORMAL); self.wait(3.0); self.play(FadeIn(pair), run_time=RUN_NORMAL); self.wait(2.5)
        warning = self.text("Percentile rank does NOT mean the score is 67.", 25, BOLD).move_to(DOWN * 3.30)
        self.play(Write(warning), run_time=RUN_NORMAL); self.wait(3.0); self.clear_stage()

    def scene_03_six_steps(self):
        self.set_header(3, "SIX STEPS FOR PERCENTILE RANK", "Say the step number before doing the math.")
        steps = VGroup()
        for number, label in STEP_LABELS:
            badge = RoundedRectangle(width=0.72, height=0.58, corner_radius=0.08, stroke_color=BLACK_LINE, stroke_width=1.8, fill_color=VERY_LIGHT_GRAY, fill_opacity=1.0)
            n = self.text(str(number), 21, BOLD).move_to(badge); body = self.text(label, 25, BOLD)
            card = RoundedRectangle(width=6.2, height=0.78, corner_radius=0.08, stroke_color=BLACK_LINE, stroke_width=1.5, fill_color=WHITE, fill_opacity=1.0)
            content = VGroup(VGroup(badge, n), body).arrange(RIGHT, buff=0.22); content.move_to(card); steps.add(VGroup(card, content))
        steps.arrange_in_grid(rows=3, cols=2, buff=(0.48, 0.28)).move_to(DOWN * 0.15)
        self.play(LaggedStart(*[FadeIn(step, shift=UP * 0.12) for step in steps], lag_ratio=0.22), run_time=RUN_SLOW * 3.2); self.wait(3.6)
        route = self.formula_box(r"\mathrm{value}\ \rightarrow\ \mathrm{count}\ \rightarrow\ \mathrm{fraction}\ \rightarrow\ \mathrm{percent}\ \rightarrow\ \mathrm{meaning}", width=12.6, font_size=33).move_to(DOWN * 2.75)
        self.play(FadeIn(route), run_time=RUN_NORMAL); self.wait(3.0); self.clear_stage()

    def scene_04_example_setup(self):
        self.set_header(4, "WORKED EXAMPLE A — FIND PR(72)", "Use the same dataset from Class 3.")
        nav = self.build_step_navigation(1); self.play(FadeIn(nav), run_time=RUN_NORMAL)
        prompt = self.text("STEP 1 — ORDER THE DATA", 29, BOLD).move_to(UP * 1.90)
        row = self.make_data_row(MAIN_DATA, show_indices=True, selected_value=72, y=0.58)
        self.play(Write(prompt), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(cell, shift=UP * 0.08) for cell in row["cells"]], lag_ratio=0.09), FadeIn(row["indices"]), run_time=RUN_SLOW * 1.9); self.wait(3.2)
        nav = self.swap_step(nav, 2); step2 = self.text("STEP 2 — IDENTIFY x AND n", 29, BOLD).move_to(UP * 1.90)
        self.play(ReplacementTransform(prompt, step2), run_time=RUN_NORMAL)
        x_card = self.card("TARGET VALUE", "x = 72", 3.7, 1.30); n_card = self.card("NUMBER OF DATA", "n = 9", 3.7, 1.30)
        VGroup(x_card, n_card).arrange(RIGHT, buff=0.50).move_to(DOWN * 1.15)
        self.play(FadeIn(x_card), run_time=RUN_NORMAL); self.wait(1.7); self.play(FadeIn(n_card), run_time=RUN_NORMAL)
        self.play(Circumscribe(row["cells"][5], color=BLACK_LINE, time_width=0.8), run_time=RUN_NORMAL); self.wait(3.4); self.clear_stage()

    def scene_05_count(self):
        self.set_header(5, "COUNT THE OBSERVATIONS AT OR BELOW x", "The symbol ≤ includes the target value itself.")
        nav = self.build_step_navigation(3); self.play(FadeIn(nav), run_time=RUN_NORMAL)
        q = self.section_question("How many observations are ≤ 72?", y=1.78, size=32)
        row = self.make_data_row(MAIN_DATA, show_indices=True, selected_value=72, dim_after=6, y=0.50)
        self.play(Write(q), run_time=RUN_NORMAL); self.play(FadeIn(row["group"]), run_time=RUN_NORMAL); self.wait(3.2)
        checks = VGroup()
        for i in range(6):
            check = self.text("✓", 23, BOLD).next_to(row["cells"][i], UP, buff=0.09); checks.add(check)
            self.play(row["boxes"][i].animate.set_fill(VERY_LIGHT_GRAY, opacity=1).set_stroke(BLACK_LINE, width=2.0), FadeIn(check, shift=DOWN * 0.05), run_time=0.48); self.wait(0.48)
        count = self.card("COUNT", "6 of 9 observations", 5.5, 1.30).move_to(DOWN * 1.05)
        self.play(FadeIn(count), run_time=RUN_NORMAL); self.wait(2.2)
        six = self.math(r"6", 50).move_to(DOWN * 2.20 + LEFT * 0.75); frac = self.math(r"\frac{6}{9}", 50).move_to(DOWN * 2.20 + RIGHT * 0.75)
        self.play(TransformFromCopy(checks, six), run_time=RUN_NORMAL); self.wait(1.6); self.play(TransformFromCopy(six, frac), run_time=RUN_NORMAL); self.wait(3.0); self.clear_stage()

    def scene_06_compute(self):
        self.set_header(6, "COMPUTE PR(72)", "Follow the chain: count → fraction → percentage → percentile rank.")
        nav = self.build_step_navigation(4); self.play(FadeIn(nav), run_time=RUN_NORMAL)
        formula = self.formula_box(r"\mathrm{PR}(x)=100\left(\frac{\#\{\mathrm{observations}\le x\}}{n}\right)", width=10.2, font_size=39).move_to(UP * 1.55)
        sub = self.math(r"\mathrm{PR}(72)=100\left(\frac{6}{9}\right)", 42).move_to(UP * 0.40)
        decimal = self.math(r"\mathrm{PR}(72)=66.666\ldots", 42).move_to(DOWN * 0.55)
        result = self.formula_box(r"\mathrm{PR}(72)\approx 66.7", width=6.7, font_size=46).move_to(DOWN * 1.60)
        rank = self.text("≈ 67th percentile", 30, BOLD).move_to(DOWN * 2.55)
        self.play(FadeIn(formula), run_time=RUN_NORMAL); self.wait(2.2); self.play(Write(sub), run_time=RUN_NORMAL); self.wait(2.0)
        self.play(Write(decimal), run_time=RUN_NORMAL); self.wait(2.4); self.play(FadeIn(result), run_time=RUN_NORMAL); self.wait(2.0)
        self.play(Write(rank), run_time=RUN_NORMAL); self.wait(3.4); self.clear_stage()

    def scene_07_interpret(self):
        self.set_header(7, "INTERPRET, DON'T JUST CALCULATE", "A percentile rank is a statement about relative position in the dataset.")
        nav = self.build_step_navigation(5); self.play(FadeIn(nav), run_time=RUN_NORMAL)
        result = self.formula_box(r"\mathrm{PR}(72)\approx 66.7", width=6.5, font_size=46).move_to(UP * 1.55)
        q = self.section_question("What does 66.7 mean?", y=0.45, size=32)
        self.play(FadeIn(result), run_time=RUN_NORMAL); self.play(Write(q), run_time=RUN_NORMAL); self.wait(3.2)
        a = self.interpretation_box(["About 66.7% of the observations are at or below 72."], width=10.5).move_to(DOWN * 0.55)
        self.play(FadeIn(a), run_time=RUN_NORMAL); self.wait(2.6)
        b = self.interpretation_box(["72 is approximately at the 67th percentile."], width=9.5, title="STATISTICAL LANGUAGE").move_to(DOWN * 1.75)
        self.play(FadeIn(b), run_time=RUN_NORMAL); self.wait(2.8)
        value = self.card("VALUE", "72", 3.2, 1.18); position = self.card("RELATIVE POSITION", "≈ 67th percentile", 5.2, 1.18)
        VGroup(value, position).arrange(RIGHT, buff=0.42).move_to(DOWN * 2.85)
        self.play(FadeIn(VGroup(value, position)), run_time=RUN_NORMAL); self.wait(3.0); self.clear_stage()

    def scene_08_compare(self):
        self.set_header(8, "SAME DATASET — DIFFERENT RELATIVE POSITIONS", "Compare 61 and 81 using exactly the same counting rule.")
        row = self.make_data_row(MAIN_DATA, show_indices=False, y=1.75, compact=True)
        self.play(FadeIn(row["group"]), run_time=RUN_NORMAL); self.wait(1.8)
        left = self.card("x_A = 61", r"\mathrm{PR}(61)=100\left(\frac{3}{9}\right)=33.3", 6.0, 1.70, True)
        right = self.card("x_B = 81", r"\mathrm{PR}(81)=100\left(\frac{8}{9}\right)=88.9", 6.0, 1.70, True)
        VGroup(left, right).arrange(RIGHT, buff=0.55).move_to(UP * 0.25)
        self.play(FadeIn(left), run_time=RUN_NORMAL); self.wait(2.5); self.play(FadeIn(right), run_time=RUN_NORMAL); self.wait(2.5)
        axis, _ = self.percentile_axis(width=11.4, y=-1.25); self.play(FadeIn(axis), run_time=RUN_NORMAL)
        x0 = -11.4 / 2
        m33 = Triangle(stroke_color=BLACK_LINE, fill_color=BLACK_LINE, fill_opacity=1).scale(0.11).rotate(PI); m89 = m33.copy()
        m33.move_to([x0 + 11.4 * 0.333, -0.90, 0]); m89.move_to([x0 + 11.4 * 0.889, -0.90, 0])
        l33 = self.text("61 → ~33rd", 21, BOLD).next_to(m33, UP, buff=0.08); l89 = self.text("81 → ~89th", 21, BOLD).next_to(m89, UP, buff=0.08)
        self.play(FadeIn(m33), Write(l33), run_time=RUN_NORMAL); self.wait(1.8); self.play(FadeIn(m89), Write(l89), run_time=RUN_NORMAL); self.wait(2.3)
        conclusion = self.interpretation_box(["81 has a much higher relative position within this distribution."], width=10.2, title="COMPARE").move_to(DOWN * 2.55)
        self.play(FadeIn(conclusion), run_time=RUN_NORMAL); self.wait(3.3); self.clear_stage()

    def scene_09_decision(self):
        self.set_header(9, "USE RELATIVE POSITION TO MAKE A DECISION", "A program selects students in approximately the top 20% of the group.")
        nav = self.build_step_navigation(6); self.play(FadeIn(nav), run_time=RUN_NORMAL)
        q = self.section_question("Would a score of 81 qualify?", y=1.82, size=34)
        self.play(Write(q), run_time=RUN_NORMAL); self.wait(3.0)
        known = self.formula_box(r"\mathrm{PR}(81)\approx 88.9", width=5.9, font_size=43).move_to(UP * 0.80)
        self.play(FadeIn(known), run_time=RUN_NORMAL); self.wait(2.0)
        axis, _ = self.percentile_axis(rank=88.9, label="81  →  88.9", top_region_start=80, width=11.5, y=-0.42)
        self.play(FadeIn(axis), run_time=RUN_NORMAL); self.wait(2.8)
        complement = VGroup(self.math(r"100\%-88.9\%=11.1\%", 40), self.text("Only about 11.1% are above 81.", 27, BOLD)).arrange(DOWN, buff=0.16).move_to(DOWN * 1.58)
        self.play(Write(complement[0]), run_time=RUN_NORMAL); self.wait(1.7); self.play(Write(complement[1]), run_time=RUN_NORMAL); self.wait(2.2)
        yes = self.card("DECISION", "YES — 81 lies approximately in the top 11%.", 9.6, 1.25).move_to(DOWN * 2.72)
        self.play(FadeIn(yes), run_time=RUN_NORMAL); self.wait(3.3); self.clear_stage()

    def scene_10_distinction(self):
        self.set_header(10, "DO NOT CONFUSE THESE TWO QUESTIONS", "Percentile value and percentile rank reverse the direction of the question, but they are not the same quantity.")
        left = RoundedRectangle(width=6.45, height=4.15, corner_radius=0.12, stroke_color=BLACK_LINE, stroke_width=1.8, fill_color=WHITE, fill_opacity=1)
        right = left.copy()
        lt = self.text("PERCENTILE VALUE", 27, BOLD)
        lb = VGroup(self.text("Input: percentile k", 23), self.text("Question: what value corresponds to k?", 22), self.math(r"P_{65}\approx 73.5", 37), self.text("Output: original data units", 22, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        lc = VGroup(lt, lb).arrange(DOWN, aligned_edge=LEFT, buff=0.30); lc.move_to(left).align_to(left, LEFT).shift(RIGHT * 0.35)
        rt = self.text("PERCENTILE RANK", 27, BOLD)
        rb = VGroup(self.text("Input: observed value x", 23), self.text("Question: what % is at or below x?", 22), self.math(r"\mathrm{PR}(72)\approx 66.7", 37), self.text("Output: percent / relative position", 22, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        rc = VGroup(rt, rb).arrange(DOWN, aligned_edge=LEFT, buff=0.30); rc.move_to(right).align_to(right, LEFT).shift(RIGHT * 0.35)
        panels = VGroup(VGroup(left, lc), VGroup(right, rc)).arrange(RIGHT, buff=0.48).move_to(DOWN * 0.05)
        self.play(FadeIn(panels[0]), run_time=RUN_NORMAL); self.wait(2.4); self.play(FadeIn(panels[1]), run_time=RUN_NORMAL); self.wait(2.8)
        neq = self.math(r"P_{65}\neq \mathrm{PR}(65)", 43).move_to(DOWN * 2.55); note = self.text("Do not swap the input and output.", 27, BOLD).move_to(DOWN * 3.15)
        self.play(Write(neq), run_time=RUN_NORMAL); self.wait(2.0); self.play(Write(note), run_time=RUN_NORMAL); self.wait(3.0); self.clear_stage()

    def scene_11_guided_challenge(self):
        self.set_header(11, "GUIDED CHALLENGE — YOUR TURN", "Find the percentile rank of 24 using the same six-step method.")
        nav = self.build_step_navigation(None); self.play(FadeIn(nav), run_time=RUN_NORMAL)
        row = self.make_data_row(CHALLENGE_DATA, show_indices=True, selected_value=24, y=1.30, compact=True)
        self.play(FadeIn(row["group"]), run_time=RUN_NORMAL)
        q = self.section_question("Find PR(24).", y=2.20, size=34); self.play(Write(q), run_time=RUN_NORMAL); self.wait(5.0)
        x_n = VGroup(self.card("TARGET", "x = 24", 3.0, 1.12), self.card("TOTAL", "n = 10", 3.0, 1.12)).arrange(RIGHT, buff=0.35).move_to(UP * 0.05)
        self.play(FadeIn(x_n), run_time=RUN_NORMAL); self.wait(1.8)
        for i in range(6): self.play(row["boxes"][i].animate.set_fill(VERY_LIGHT_GRAY, opacity=1).set_stroke(BLACK_LINE, width=2.0), run_time=0.32)
        count = self.text("6 observations are ≤ 24.", 27, BOLD).move_to(DOWN * 0.80)
        calc = self.math(r"\mathrm{PR}(24)=100\left(\frac{6}{10}\right)=60", 42).move_to(DOWN * 1.55)
        answer = self.formula_box(r"24\ \text{is at the }60\text{th percentile}", width=8.9, font_size=39).move_to(DOWN * 2.35)
        self.play(Write(count), run_time=RUN_NORMAL); self.wait(1.8); self.play(Write(calc), run_time=RUN_NORMAL); self.wait(2.3)
        self.play(FadeIn(answer), run_time=RUN_NORMAL); self.wait(2.8)
        meaning = self.text("60% of the observations are at or below 24.", 25, BOLD).move_to(DOWN * 3.05)
        self.play(Write(meaning), run_time=RUN_NORMAL); self.wait(3.2); self.clear_stage()

    def scene_12_final_recipe(self):
        self.set_header(12, "FINAL RECIPE — VALUE → POSITION", "Use the same method every time: count carefully, compute, interpret, then decide.")
        route = self.process_map([("1", "ORDER DATA"), ("2", "IDENTIFY x, n"), ("3", "COUNT ≤ x"), ("4", "COMPUTE PR"), ("5", "INTERPRET"), ("6", "DECIDE + CHECK")], card_width=4.15, card_height=1.0, columns=3)
        route.move_to(UP * 0.70)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.10) for card in route], lag_ratio=0.12), run_time=RUN_SLOW * 2.2); self.wait(3.0)
        formula = self.formula_box(r"\mathrm{PR}(x)=100\left(\frac{\#\{\mathrm{observations}\le x\}}{n}\right)", width=10.7, font_size=40).move_to(DOWN * 1.25)
        self.play(FadeIn(formula), run_time=RUN_NORMAL); self.wait(2.8)
        bridge = VGroup(self.text("CLASS 3", 21, BOLD), self.text("Percentile → Value", 25), self.text("CLASS 4", 21, BOLD), self.text("Value → Relative Position", 25), self.text("NEXT", 21, BOLD), self.text("Position Measures + Boxplot Comparisons", 25)).arrange_in_grid(rows=3, cols=2, col_alignments="ll", buff=(0.35, 0.18))
        bridge.move_to(DOWN * 2.65); self.play(FadeIn(bridge), run_time=RUN_NORMAL); self.wait(3.6); self.clear_stage()

    def final_closing(self):
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=RUN_NORMAL)
        course = self.text("STATISTICS 10", 27, BOLD); title = self.text("PERCENTILE RANK", 48, BOLD)
        rule = Line(LEFT * 4.8, RIGHT * 4.8, color=BLACK_LINE, stroke_width=2.0)
        line1 = self.text("A raw value tells you what was obtained.", 29)
        line2 = self.text("A percentile rank tells you where it stands.", 29, BOLD)
        nxt = self.text("Next: Position Measures + Boxplot Comparisons", 22, MEDIUM).set_color(MID_GRAY)
        group = VGroup(course, title, rule, line1, line2, nxt).arrange(DOWN, buff=0.28); self.fit(group, 13.6, 5.4)
        self.play(FadeIn(course), run_time=RUN_NORMAL); self.play(Write(title), run_time=RUN_SLOW); self.play(Create(rule), run_time=RUN_NORMAL)
        self.play(FadeIn(line1), run_time=RUN_NORMAL); self.play(FadeIn(line2), run_time=RUN_NORMAL); self.play(FadeIn(nxt), run_time=RUN_NORMAL)
        self.wait(3.4); self.play(FadeOut(group), run_time=RUN_NORMAL)

# Preview: manim -pql statistics10_class4_percentile_rank.py Statistics10Class4PercentileRank --disable_caching
# Final:   manim -pqh statistics10_class4_percentile_rank.py Statistics10Class4PercentileRank --fps 30 --disable_caching
