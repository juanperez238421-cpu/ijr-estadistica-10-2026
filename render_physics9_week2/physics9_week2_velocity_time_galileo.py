#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 9 — Week 2: velocity–time graphs + Galileo bridge.

Two independent ManimCE scenes using the JP Classroom visual protocol:
    1) Physics9Week2VelocityTimeTheory
    2) Physics9Week2VelocityTimeProblems

Pedagogical sequence
--------------------
- Recover x–t slope = velocity from the previous lesson.
- Use a schematic Galileo inclined-plane reconstruction to motivate changing speed.
- Build the v–t graph language: positive, zero, negative velocity.
- Interpret horizontal v–t segments as constant velocity.
- Derive signed area under v(t) as displacement for constant/piecewise-constant motion.
- Solve problems progressively without introducing formal acceleration yet.

Target: ManimCE 0.20.x, horizontal Full HD, white JP Classroom style.
"""

from __future__ import annotations

import math
import numpy as np
from manim import *

from library.jp_classroom_style import (
    JPMathClassroomScene,
    BLACK_TEXT,
    BLACK_LINE,
    DARK_GRAY,
    MID_GRAY,
    LIGHT_GRAY,
    VERY_LIGHT_GRAY,
    PAPER_GRAY,
    WHITE_FILL,
    SAFE_WIDTH,
    FRAME_WIDTH,
    RUN_QUICK,
    RUN_NORMAL,
    RUN_SLOW,
    PAUSE_SHORT,
    PAUSE_READ,
    PAUSE_EXPLAIN,
    PAUSE_WORK,
    PAUSE_SUMMARY,
    PAUSE_FINAL,
    assert_close,
)


# =============================================================================
# VALIDATED LESSON DATA
# =============================================================================
GALILEO_T = np.array([0, 1, 2, 3, 4], dtype=float)
# Schematic positions proportional to t^2; not presented as Galileo's exact data.
GALILEO_S = 0.25 * GALILEO_T**2
GALILEO_INTERVALS = np.diff(GALILEO_S)

VT_SEGMENTS = [
    (0.0, 3.0, 4.0),
    (3.0, 5.0, 0.0),
    (5.0, 9.0, -2.0),
]
VT_DISPLACEMENTS = [(b - a) * v for a, b, v in VT_SEGMENTS]
VT_NET_DISPLACEMENT = sum(VT_DISPLACEMENTS)
VT_DISTANCE = sum(abs(x) for x in VT_DISPLACEMENTS)

PROBLEM_2_SEGMENTS = [
    (0.0, 2.0, 3.0),
    (2.0, 4.0, 0.0),
    (4.0, 7.0, -1.0),
]
PROBLEM_2_DISP = sum((b - a) * v for a, b, v in PROBLEM_2_SEGMENTS)
PROBLEM_2_DIST = sum(abs((b - a) * v) for a, b, v in PROBLEM_2_SEGMENTS)


def validate_week2_data() -> None:
    assert np.allclose(GALILEO_INTERVALS, [0.25, 0.75, 1.25, 1.75])
    assert_close(VT_DISPLACEMENTS[0], 12.0, label="segment A displacement")
    assert_close(VT_DISPLACEMENTS[1], 0.0, label="segment B displacement")
    assert_close(VT_DISPLACEMENTS[2], -8.0, label="segment C displacement")
    assert_close(VT_NET_DISPLACEMENT, 4.0, label="week2 net displacement")
    assert_close(VT_DISTANCE, 20.0, label="week2 total distance")
    assert_close(PROBLEM_2_DISP, 3.0, label="problem 2 net displacement")
    assert_close(PROBLEM_2_DIST, 9.0, label="problem 2 distance")


# =============================================================================
# COMMON VISUAL BASE
# =============================================================================
class Physics9Week2Base(JPMathClassroomScene):
    """Shared, frame-audited helpers for both Week 2 videos."""

    def validate_lesson_data(self) -> None:
        validate_week2_data()

    def set_header(self, number: int, title: str, subtitle: str) -> None:
        """Larger V5.3 header with fade transitions rather than text morphing."""
        number_box = RoundedRectangle(
            width=0.78,
            height=0.56,
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=WHITE_FILL,
            fill_opacity=1.0,
        )
        number_text = self.text(f"{number:02d}", 26, BOLD).move_to(number_box)
        title_text = self.text(title, 39, BOLD)
        self.fit(title_text, SAFE_WIDTH - number_box.width - 0.40, 0.64)
        title_row = VGroup(VGroup(number_box, number_text), title_text).arrange(RIGHT, buff=0.28)
        title_row.to_edge(UP, buff=0.13).to_edge(LEFT, buff=0.48)

        rule = Line(LEFT * 7.48, RIGHT * 7.48, color=LIGHT_GRAY, stroke_width=2)
        rule.next_to(title_row, DOWN, buff=0.07)

        words = subtitle.split()
        if len(subtitle) > 92:
            midpoint = len(words) // 2
            best = min(
                range(max(1, midpoint - 5), min(len(words), midpoint + 6)),
                key=lambda i: abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))),
            )
            subtitle_text = VGroup(
                self.text(" ".join(words[:best]), 26),
                self.text(" ".join(words[best:]), 26),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        else:
            subtitle_text = self.text(subtitle, 26)
        self.fit(subtitle_text, 14.10, 0.92)
        subtitle_text.next_to(rule, DOWN, buff=0.08).align_to(title_row, LEFT)

        new_header = VGroup(title_row, rule)
        if self.header_group is None:
            self.header_group = new_header
            self.subtitle_group = subtitle_text
            self.add(new_header, subtitle_text)
        else:
            old_header = self.header_group
            old_subtitle = self.subtitle_group
            self.play(FadeOut(old_header), FadeOut(old_subtitle), run_time=RUN_QUICK)
            self.remove(old_header, old_subtitle)
            self.header_group = new_header
            self.subtitle_group = subtitle_text
            self.play(FadeIn(new_header), FadeIn(subtitle_text), run_time=RUN_QUICK)

    def motion_object(self, scale_factor: float = 1.0) -> VGroup:
        body = RoundedRectangle(
            width=0.82,
            height=0.34,
            corner_radius=0.07,
            stroke_color=BLACK_LINE,
            stroke_width=2.2,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1,
        )
        roof = Polygon(
            LEFT * 0.25 + UP * 0.17,
            LEFT * 0.08 + UP * 0.42,
            RIGHT * 0.25 + UP * 0.42,
            RIGHT * 0.36 + UP * 0.17,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=WHITE_FILL,
            fill_opacity=1,
        )
        w1 = Circle(radius=0.09, color=BLACK_LINE, stroke_width=2, fill_color=WHITE, fill_opacity=1).move_to(LEFT * 0.25 + DOWN * 0.22)
        w2 = w1.copy().move_to(RIGHT * 0.25 + DOWN * 0.22)
        return VGroup(body, roof, w1, w2).scale(scale_factor)

    def number_track(self, x_min=-6, x_max=12, step=2, length=6.1) -> tuple[VGroup, NumberLine]:
        line = NumberLine(
            x_range=[x_min, x_max, step],
            length=length,
            include_numbers=True,
            font_size=26,
            color=BLACK_LINE,
            stroke_width=2.2,
            decimal_number_config={"color": BLACK_TEXT, "num_decimal_places": 0},
        )
        label = self.text("position x (m)", 26, MEDIUM).next_to(line, DOWN, buff=0.44).align_to(line, RIGHT)
        return VGroup(line, label), line

    def vt_axes(self, x_max=10, y_min=-4, y_max=5, width=6.4, height=3.9) -> tuple[VGroup, Axes]:
        axes = Axes(
            x_range=[0, x_max, 1],
            y_range=[y_min, y_max, 1],
            x_length=width,
            y_length=height,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.0, "include_tip": True},
            x_axis_config={"numbers_to_include": list(range(0, x_max, 2)), "font_size": 23},
            y_axis_config={"numbers_to_include": list(range(y_min, y_max + 1, 2)), "font_size": 23},
        )
        xl = self.math(r"t\,(s)", 28).next_to(axes.x_axis.get_end(), DOWN, buff=0.08)
        yl = self.math(r"v\,(m/s)", 28).next_to(axes.y_axis.get_end(), LEFT, buff=0.08)
        return VGroup(axes, xl, yl), axes

    def xt_axes(self, x_max=6, y_max=12, width=5.6, height=3.45) -> tuple[VGroup, Axes]:
        axes = Axes(
            x_range=[0, x_max, 1],
            y_range=[0, y_max, 2],
            x_length=width,
            y_length=height,
            axis_config={"color": BLACK_LINE, "stroke_width": 2.0, "include_tip": True},
            x_axis_config={"numbers_to_include": [0, 2, 4, 6], "font_size": 22},
            y_axis_config={"numbers_to_include": [0, 4, 8, 12], "font_size": 22},
        )
        xl = self.math(r"t\,(s)", 27).next_to(axes.x_axis.get_end(), DOWN, buff=0.07)
        yl = self.math(r"x\,(m)", 27).next_to(axes.y_axis.get_end(), LEFT, buff=0.07)
        return VGroup(axes, xl, yl), axes

    def segment_label(self, text: str, point: np.ndarray, size: int = 26) -> Text:
        label = self.text(text, size, BOLD)
        label.move_to(point)
        return label

    def signed_area_rectangle(self, axes: Axes, t0: float, t1: float, velocity: float, opacity: float = 0.18) -> Rectangle:
        p0 = axes.c2p(t0, 0)
        p1 = axes.c2p(t1, velocity)
        rect = Rectangle(
            width=abs(p1[0] - p0[0]),
            height=max(0.02, abs(p1[1] - p0[1])),
            stroke_color=BLACK_LINE,
            stroke_width=1.8,
            fill_color=MID_GRAY if velocity < 0 else LIGHT_GRAY,
            fill_opacity=opacity,
        )
        rect.move_to((p0 + p1) / 2)
        return rect


class Physics9Week2VelocityTimeTheory(Physics9Week2Base):
    """Week 2 theory: v–t language and signed area as displacement."""

    def construct(self) -> None:
        self.scene_00_opening()
        self.scene_01_bridge_xt_to_vt()
        self.scene_02_galileo_ramp()
        self.scene_03_vt_anatomy()
        self.scene_04_positive_velocity()
        self.scene_05_rest_and_negative()
        self.scene_06_piecewise_story()
        self.scene_07_area_displacement()
        self.scene_08_signed_area_total()
        self.scene_09_summary()

    def scene_00_opening(self) -> None:
        self.standard_opening(
            "GRADE 9 · PHYSICS · WEEK 2",
            "VELOCITY–TIME GRAPHS",
            "Direction, rest, constant velocity and displacement from area",
            "A velocity–time graph does not show where the object is. It shows how fast and in which direction it is moving.",
        )

    def scene_01_bridge_xt_to_vt(self) -> None:
        self.set_header(1, "FROM x–t SLOPE TO A NEW GRAPH", "Last class: the slope of x(t) is velocity. Now we put that velocity directly on the vertical axis.")
        xt_group, xt = self.xt_axes(x_max=6, y_max=12, width=5.6, height=3.55)
        xt_line = xt.plot(lambda t: 2 * t + 1, x_range=[0, 5], color=BLACK_LINE, stroke_width=3.4)
        slope_tri = Polygon(xt.c2p(1, 3), xt.c2p(3, 3), xt.c2p(3, 7), color=MID_GRAY, stroke_width=2, fill_opacity=0)
        slope_lab = self.math(r"v=\frac{\Delta x}{\Delta t}=\frac{4}{2}=2\,\mathrm{m/s}", 34).move_to(xt.c2p(2.9, 9.9))
        xt_fig = VGroup(xt_group, xt_line, slope_tri, slope_lab)
        xt_panel = self.figure_panel(xt_fig, width=7.0, height=4.85, title="POSITION–TIME", caption="Constant slope means constant velocity.", title_size=31, caption_size=25)
        vt_group, vt = self.vt_axes(x_max=6, y_min=-1, y_max=4, width=5.4, height=3.4)
        vt_line = Line(vt.c2p(0, 2), vt.c2p(5.3, 2), color=BLACK_LINE, stroke_width=3.4)
        vlab = self.math(r"v=+2\,\mathrm{m/s}", 35).move_to(vt.c2p(3.5, 3.15))
        vt_fig = VGroup(vt_group, vt_line, vlab)
        vt_panel = self.figure_panel(vt_fig, width=6.45, height=4.85, title="VELOCITY–TIME", caption="The same motion becomes a horizontal line at +2 m/s.", title_size=31, caption_size=25)
        layout = self.split_layout(xt_panel.group, vt_panel.group, left_width=7.0, right_width=6.45, max_height=5.25, center_y=-0.47, gap=0.35)
        self.assert_content_safe(layout.group, "xt to vt bridge")
        self.play(FadeIn(xt_panel.box), FadeIn(xt_panel.title), Create(xt_group), run_time=RUN_NORMAL)
        self.play(Create(xt_line), run_time=RUN_SLOW)
        self.play(Create(slope_tri), FadeIn(slope_lab), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(vt_panel.box), FadeIn(vt_panel.title), Create(vt_group), run_time=RUN_NORMAL)
        self.play(Create(vt_line), FadeIn(vlab), FadeIn(xt_panel.caption), FadeIn(vt_panel.caption), run_time=RUN_SLOW)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    def scene_02_galileo_ramp(self) -> None:
        self.set_header(2, "GALILEO'S INCLINED PLANE: MAKE CHANGE VISIBLE", "A ramp slows the motion enough to compare equal time intervals. The reconstruction below is schematic, not Galileo's exact measured data.")
        ramp_start = LEFT * 2.65 + UP * 1.28
        ramp_end = RIGHT * 2.55 + DOWN * 1.55
        ramp = Line(ramp_start, ramp_end, color=BLACK_LINE, stroke_width=4)
        ground = Line(LEFT * 3.05 + DOWN * 1.58, RIGHT * 3.05 + DOWN * 1.58, color=LIGHT_GRAY, stroke_width=2)
        angle_arc = Arc(radius=0.55, start_angle=0, angle=math.atan2(ramp_start[1]-ramp_end[1], ramp_end[0]-ramp_start[0]), color=MID_GRAY, stroke_width=2).move_arc_center_to(ramp_end)
        theta = self.math(r"\theta", 27).next_to(angle_arc, LEFT, buff=0.03)
        alphas = GALILEO_S / GALILEO_S[-1]
        dots = VGroup(); tick_labels = VGroup()
        for i, a in enumerate(alphas):
            p = interpolate(ramp_start, ramp_end, float(a))
            dot = Dot(p, radius=0.075, color=BLACK_LINE)
            lab = self.math(fr"t_{i}", 24).next_to(dot, UP + RIGHT, buff=0.06)
            dots.add(dot); tick_labels.add(lab)
        ball = Circle(radius=0.14, color=BLACK_LINE, stroke_width=2.3, fill_color=WHITE, fill_opacity=1).move_to(dots[0])
        ramp_fig = VGroup(ramp, ground, angle_arc, theta, dots, tick_labels, ball)
        ramp_panel = self.figure_panel(ramp_fig, width=7.35, height=5.05, title="EQUAL Δt — GROWING SPACING", caption="The distance covered in each equal time interval grows: speed is not staying constant.", title_size=30, caption_size=24)
        interval_rows = VGroup()
        for k, d in enumerate(GALILEO_INTERVALS, start=1):
            interval_rows.add(self.math(fr"\Delta x_{k}={d:.2f}\,\mathrm{{m}}", 32))
        interval_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.23)
        inequality = self.math(r"\Delta x_1<\Delta x_2<\Delta x_3<\Delta x_4", 35)
        time_note = self.math(r"\Delta t_1=\Delta t_2=\Delta t_3=\Delta t_4", 32)
        question = self.note_panel("WHAT CHANGES?", ["Equal time intervals do not produce equal displacements.", "Therefore the speed changes during the descent.", "Later we will quantify that change with acceleration."], width=5.8, title_size=29, body_size=26)
        right = VGroup(time_note, interval_rows, inequality, question).arrange(DOWN, buff=0.23)
        layout = self.split_layout(ramp_panel.group, right, left_width=7.35, right_width=5.85, max_height=5.30, center_y=-0.47, gap=0.34)
        self.assert_content_safe(layout.group, "Galileo ramp layout")
        self.play(FadeIn(ramp_panel.box), FadeIn(ramp_panel.title), Create(ramp), Create(ground), FadeIn(theta), run_time=RUN_NORMAL)
        self.play(FadeIn(dots), FadeIn(tick_labels), FadeIn(ball), run_time=RUN_NORMAL)
        self.play(FadeIn(time_note), run_time=RUN_NORMAL)
        for i in range(1, len(dots)):
            self.play(ball.animate.move_to(dots[i].get_center()), FadeIn(interval_rows[i-1]), run_time=RUN_NORMAL)
            self.wait(PAUSE_SHORT)
        self.play(FadeIn(inequality), FadeIn(question), FadeIn(ramp_panel.caption), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    def scene_03_vt_anatomy(self) -> None:
        self.set_header(3, "THE ANATOMY OF A v–t GRAPH", "Read the vertical value first: its magnitude tells speed; its sign tells direction; zero means rest.")
        axes_group, axes = self.vt_axes(x_max=8, y_min=-4, y_max=5, width=7.0, height=4.2)
        pos = Line(axes.c2p(0.5, 3), axes.c2p(7.1, 3), color=BLACK_LINE, stroke_width=3.2)
        zero = Line(axes.c2p(0.5, 0), axes.c2p(7.1, 0), color=MID_GRAY, stroke_width=3.0)
        neg = Line(axes.c2p(0.5, -2), axes.c2p(7.1, -2), color=DARK_GRAY, stroke_width=3.0)
        lp = self.text("positive velocity", 27, BOLD).move_to(axes.c2p(5.3, 3.7))
        lz = self.text("rest", 27, BOLD).move_to(axes.c2p(6.0, 0.75))
        ln = self.text("negative velocity", 27, BOLD).move_to(axes.c2p(5.15, -2.85))
        fig = VGroup(axes_group, pos, zero, neg, lp, lz, ln)
        panel = self.figure_panel(fig, width=7.8, height=5.1, title="READ v, NOT POSITION", caption="Above the axis: + direction. On the axis: rest. Below the axis: − direction.", title_size=31, caption_size=24)
        glossary = self.key_value_panel("GRAPH LANGUAGE", [("Vertical axis", "velocity v"), ("Horizontal axis", "time t"), ("Height |v|", "speed"), ("Sign of v", "direction")], width=5.55, label_size=25, value_size=26)
        warning = self.note_panel("DO NOT CONFUSE", ["A line below the axis does not mean a negative position.", "It means the object moves in the negative direction."], width=5.55, title_size=29, body_size=26)
        right = VGroup(glossary, warning).arrange(DOWN, buff=0.28)
        layout = self.split_layout(panel.group, right, left_width=7.8, right_width=5.6, max_height=5.3, center_y=-0.48, gap=0.34)
        self.assert_content_safe(layout.group, "vt anatomy")
        self.play(FadeIn(panel.box), FadeIn(panel.title), Create(axes_group), run_time=RUN_NORMAL)
        self.play(Create(pos), FadeIn(lp), run_time=RUN_NORMAL); self.wait(PAUSE_READ)
        self.play(Create(zero), FadeIn(lz), run_time=RUN_NORMAL); self.wait(PAUSE_READ)
        self.play(Create(neg), FadeIn(ln), run_time=RUN_NORMAL); self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(glossary), FadeIn(warning), FadeIn(panel.caption), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY); self.clear_stage()

    def scene_04_positive_velocity(self) -> None:
        self.set_header(4, "CONSTANT POSITIVE VELOCITY", "A horizontal line above the time axis means the object moves in the positive direction at constant speed.")
        track_group, track = self.number_track(x_min=0, x_max=12, step=2, length=6.2)
        cart = self.motion_object(0.78).move_to(track.n2p(1) + UP * 0.48)
        start_dot = Dot(track.n2p(1), color=BLACK_LINE); end_dot = Dot(track.n2p(10), color=BLACK_LINE)
        arrow = Arrow(track.n2p(1) + UP * 0.08, track.n2p(10) + UP * 0.08, buff=0.05, color=BLACK_LINE, stroke_width=2.6)
        track_fig = VGroup(track_group, cart, start_dot, end_dot, arrow)
        track_panel = self.figure_panel(track_fig, width=7.0, height=4.7, title="MOTION STORY", caption="The object keeps moving to the right; equal times produce equal displacements.", title_size=31, caption_size=24)
        axes_group, axes = self.vt_axes(x_max=5, y_min=-1, y_max=5, width=5.35, height=3.5)
        line = Line(axes.c2p(0, 3), axes.c2p(4.5, 3), color=BLACK_LINE, stroke_width=3.4)
        lab = self.math(r"v=+3\,\mathrm{m/s}", 35).move_to(axes.c2p(3.0, 4.05))
        vt_fig = VGroup(axes_group, line, lab)
        vt_panel = self.figure_panel(vt_fig, width=6.35, height=4.7, title="v–t REPRESENTATION", caption="The graph is horizontal because the velocity value does not change.", title_size=31, caption_size=24)
        layout = self.split_layout(track_panel.group, vt_panel.group, left_width=7.0, right_width=6.35, max_height=5.22, center_y=-0.48, gap=0.35)
        self.assert_content_safe(layout.group, "positive velocity")
        self.play(FadeIn(track_panel.box), FadeIn(track_panel.title), Create(track_group), FadeIn(cart), run_time=RUN_NORMAL)
        self.play(GrowArrow(arrow), cart.animate.move_to(track.n2p(10) + UP * 0.48), run_time=RUN_SLOW * 1.6)
        self.play(FadeIn(vt_panel.box), FadeIn(vt_panel.title), Create(axes_group), run_time=RUN_NORMAL)
        self.play(Create(line), FadeIn(lab), FadeIn(track_panel.caption), FadeIn(vt_panel.caption), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY); self.clear_stage()

    def scene_05_rest_and_negative(self) -> None:
        self.set_header(5, "ZERO VELOCITY AND NEGATIVE VELOCITY", "Zero velocity means no change of position. Negative velocity means motion in the chosen negative direction.")
        axes_group, axes = self.vt_axes(x_max=8, y_min=-4, y_max=4, width=7.0, height=4.1)
        rest_line = Line(axes.c2p(0.6, 0), axes.c2p(3.6, 0), color=BLACK_LINE, stroke_width=3.4)
        neg_line = Line(axes.c2p(4.1, -2), axes.c2p(7.3, -2), color=BLACK_LINE, stroke_width=3.4)
        rest_lab = self.text("REST", 28, BOLD).move_to(axes.c2p(2.0, 0.8))
        neg_lab = self.math(r"v=-2\,\mathrm{m/s}", 34).move_to(axes.c2p(5.7, -3.0))
        fig = VGroup(axes_group, rest_line, neg_line, rest_lab, neg_lab)
        panel = self.figure_panel(fig, width=7.65, height=5.0, title="TWO DIFFERENT IDEAS", caption="The zero line and a negative line are not interchangeable.", title_size=31, caption_size=24)
        rest_note = self.note_panel("AT REST", ["Position stays constant.", "Velocity is exactly zero."], width=5.55, title_size=29, body_size=27)
        neg_note = self.note_panel("MOVING NEGATIVE", ["Position is changing.", "The direction is negative, not the speed."], width=5.55, title_size=29, body_size=27)
        formula = self.formula_panel(r"\text{speed}=|v|", width=5.55, height=1.05, font_size=39)
        right = VGroup(rest_note, neg_note, formula).arrange(DOWN, buff=0.25)
        layout = self.split_layout(panel.group, right, left_width=7.65, right_width=5.6, max_height=5.25, center_y=-0.48, gap=0.35)
        self.assert_content_safe(layout.group, "rest and negative")
        self.play(FadeIn(panel.box), FadeIn(panel.title), Create(axes_group), run_time=RUN_NORMAL)
        self.play(Create(rest_line), FadeIn(rest_lab), FadeIn(rest_note), run_time=RUN_NORMAL); self.wait(PAUSE_EXPLAIN)
        self.play(Create(neg_line), FadeIn(neg_lab), FadeIn(neg_note), run_time=RUN_NORMAL); self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(formula), FadeIn(panel.caption), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY); self.clear_stage()

    def scene_06_piecewise_story(self) -> None:
        self.set_header(6, "ONE STORY CAN HAVE SEVERAL VELOCITY SEGMENTS", "Read the graph from left to right: move positive, stop, then move negative.")
        axes_group, axes = self.vt_axes(x_max=10, y_min=-4, y_max=5, width=7.25, height=4.2)
        seg1 = Line(axes.c2p(0, 4), axes.c2p(3, 4), color=BLACK_LINE, stroke_width=3.4)
        seg2 = Line(axes.c2p(3, 0), axes.c2p(5, 0), color=MID_GRAY, stroke_width=3.4)
        seg3 = Line(axes.c2p(5, -2), axes.c2p(9, -2), color=DARK_GRAY, stroke_width=3.4)
        jumps = VGroup(DashedLine(axes.c2p(3, 4), axes.c2p(3, 0), color=LIGHT_GRAY, dash_length=0.08), DashedLine(axes.c2p(5, 0), axes.c2p(5, -2), color=LIGHT_GRAY, dash_length=0.08))
        labels = VGroup(self.text("A: + direction", 25, BOLD).move_to(axes.c2p(1.55, 4.7)), self.text("B: rest", 25, BOLD).move_to(axes.c2p(4.0, 0.9)), self.text("C: − direction", 25, BOLD).move_to(axes.c2p(7.1, -2.9)))
        fig = VGroup(axes_group, jumps, seg1, seg2, seg3, labels)
        panel = self.figure_panel(fig, width=8.0, height=5.15, title="READ IT AS A TIMELINE", caption="Each horizontal segment is a constant-velocity interval.", title_size=31, caption_size=24)
        story = self.key_value_panel("MOTION STORY", [("0–3 s", "+4 m/s"), ("3–5 s", "0 m/s"), ("5–9 s", "-2 m/s")], width=5.25, label_size=26, value_size=28)
        questions = self.note_panel("ASK IN THIS ORDER", ["1. What is the sign?", "2. What is |v|?", "3. How long does it last?"], width=5.25, title_size=29, body_size=27)
        right = VGroup(story, questions).arrange(DOWN, buff=0.30)
        layout = self.split_layout(panel.group, right, left_width=8.0, right_width=5.3, max_height=5.32, center_y=-0.49, gap=0.35)
        self.assert_content_safe(layout.group, "piecewise story")
        self.play(FadeIn(panel.box), FadeIn(panel.title), Create(axes_group), run_time=RUN_NORMAL)
        for seg, lab in zip([seg1, seg2, seg3], labels):
            self.play(Create(seg), FadeIn(lab), run_time=RUN_NORMAL); self.wait(PAUSE_READ)
        self.play(FadeIn(jumps), FadeIn(story), run_time=RUN_NORMAL); self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(questions), FadeIn(panel.caption), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY); self.clear_stage()

    def scene_07_area_displacement(self) -> None:
        self.set_header(7, "WHY AREA UNDER v(t) BECOMES DISPLACEMENT", "For constant velocity, displacement equals velocity times elapsed time — exactly the rectangle's signed area.")
        axes_group, axes = self.vt_axes(x_max=6, y_min=-1, y_max=5, width=6.7, height=3.95)
        line = Line(axes.c2p(1, 3), axes.c2p(5, 3), color=BLACK_LINE, stroke_width=3.4)
        rect = self.signed_area_rectangle(axes, 1, 5, 3, opacity=0.24)
        base_lab = self.math(r"\Delta t=4\,\mathrm{s}", 30).move_to(axes.c2p(3, 0.65))
        height_lab = self.math(r"v=3\,\mathrm{m/s}", 30).move_to(axes.c2p(4.05, 3.65))
        fig = VGroup(axes_group, rect, line, base_lab, height_lab)
        panel = self.figure_panel(fig, width=7.45, height=4.95, title="RECTANGLE = v × Δt", caption="The rectangle's units are (m/s)×s = m, so its area represents displacement.", title_size=31, caption_size=24)
        stack = self.equation_stack([r"\Delta x=v\Delta t", r"\Delta x=(3\,\mathrm{m/s})(4\,\mathrm{s})", r"\Delta x=+12\,\mathrm{m}", r"\text{area}=\text{base}\times\text{height}=\Delta t\,v"], sizes=[42, 37, 42, 34], buff=0.30, max_width=5.8, max_height=3.15)
        note = self.note_panel("THE SIGN MATTERS", ["Area above the axis is positive.", "Area below the axis is negative."], width=5.8, title_size=29, body_size=27)
        right = VGroup(stack, note).arrange(DOWN, buff=0.26)
        layout = self.split_layout(panel.group, right, left_width=7.45, right_width=5.85, max_height=5.25, center_y=-0.48, gap=0.36)
        self.assert_content_safe(layout.group, "area derivation")
        self.play(FadeIn(panel.box), FadeIn(panel.title), Create(axes_group), Create(line), run_time=RUN_NORMAL)
        self.play(FadeIn(rect), FadeIn(base_lab), FadeIn(height_lab), run_time=RUN_NORMAL); self.wait(PAUSE_EXPLAIN)
        self.animate_equation_stack(stack, pause=PAUSE_READ)
        self.play(FadeIn(note), FadeIn(panel.caption), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY); self.clear_stage()

    def scene_08_signed_area_total(self) -> None:
        self.set_header(8, "ADD SIGNED AREAS FOR NET DISPLACEMENT", "Positive areas add positive displacement; negative areas subtract. Distance counts every segment by magnitude.")
        axes_group, axes = self.vt_axes(x_max=10, y_min=-4, y_max=5, width=7.0, height=4.0)
        segs = VGroup(); areas = VGroup()
        for t0, t1, v in VT_SEGMENTS:
            segs.add(Line(axes.c2p(t0, v), axes.c2p(t1, v), color=BLACK_LINE, stroke_width=3.3))
            if abs(v) > 1e-9: areas.add(self.signed_area_rectangle(axes, t0, t1, v, opacity=0.22))
        area_labs = VGroup(self.math(r"+12\,m", 30).move_to(axes.c2p(1.5, 2.1)), self.math(r"-8\,m", 30).move_to(axes.c2p(7.0, -1.15)))
        fig = VGroup(axes_group, areas, segs, area_labs)
        panel = self.figure_panel(fig, width=7.65, height=5.0, title="SIGNED AREA ACCOUNTING", caption="The stop interval has zero height, so it contributes zero displacement.", title_size=31, caption_size=24)
        disp_stack = self.equation_stack([r"\Delta x_{\rm total}=12+0-8", r"\Delta x_{\rm total}=+4\,\mathrm{m}"], sizes=[39, 43], buff=0.30, max_width=5.6, max_height=1.75)
        dist_stack = self.equation_stack([r"d_{\rm total}=|12|+|0|+|-8|", r"d_{\rm total}=20\,\mathrm{m}"], sizes=[37, 42], buff=0.30, max_width=5.6, max_height=1.75)
        right = VGroup(disp_stack, dist_stack).arrange(DOWN, buff=0.52)
        layout = self.split_layout(panel.group, right, left_width=7.65, right_width=5.65, max_height=5.25, center_y=-0.48, gap=0.36)
        self.assert_content_safe(layout.group, "signed area total")
        self.play(FadeIn(panel.box), FadeIn(panel.title), Create(axes_group), run_time=RUN_NORMAL)
        self.play(FadeIn(areas), Create(segs), FadeIn(area_labs), run_time=RUN_SLOW); self.wait(PAUSE_EXPLAIN)
        self.animate_equation_stack(disp_stack, pause=PAUSE_READ); self.wait(PAUSE_WORK)
        self.animate_equation_stack(dist_stack, pause=PAUSE_READ)
        self.play(FadeIn(panel.caption), run_time=RUN_NORMAL); self.wait(PAUSE_SUMMARY); self.clear_stage()

    def scene_09_summary(self) -> None:
        self.set_header(9, "THE v–t RECIPE", "Read sign, magnitude and time interval first. Then use signed area when the question asks for displacement.")
        route = self.process_map([("1", "READ THE TIME INTERVAL"), ("2", "READ THE SIGN OF v"), ("3", "READ THE MAGNITUDE |v|"), ("4", "IDENTIFY REST IF v=0"), ("5", "FIND SIGNED AREA FOR Δx"), ("6", "ADD MAGNITUDES FOR DISTANCE")], card_width=4.45, card_height=1.12, columns=3)
        route.move_to(DOWN * 0.15); self.fit(route, 14.05, 3.55)
        formulas = VGroup(self.math(r"\text{speed}=|v|", 40), self.math(r"\Delta x=\text{signed area under }v(t)", 40), self.math(r"d=\sum |\Delta x_i|", 40)).arrange(RIGHT, buff=0.7)
        self.fit(formulas, 13.7, 0.95); formulas.to_edge(DOWN, buff=0.48)
        bridge = self.text("Galileo's ramp gives the next question: what quantity measures how quickly velocity itself changes?", 30, MEDIUM)
        self.fit(bridge, 13.4, 0.82); bridge.move_to(UP * 1.95)
        self.play(FadeIn(bridge), run_time=RUN_NORMAL); self.wait(PAUSE_EXPLAIN)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in route], lag_ratio=0.10), run_time=RUN_SLOW * 1.8)
        self.wait(PAUSE_WORK); self.play(FadeIn(formulas), run_time=RUN_NORMAL); self.wait(PAUSE_FINAL)
        self.standard_closing("Velocity tells how position changes. The v–t graph lets us read direction and recover displacement.")


class Physics9Week2VelocityTimeProblems(Physics9Week2Base):
    """Step-by-step worked problems for the Week 2 v–t lesson."""

    def construct(self) -> None:
        self.scene_00_opening(); self.scene_01_problem_read_graph(); self.scene_02_problem_area_accounting(); self.scene_03_problem_story_to_graph(); self.scene_04_problem_xt_to_vt(); self.scene_05_problem_galileo_interpretation(); self.scene_06_final_checklist()

    def scene_00_opening(self) -> None:
        self.standard_opening("GRADE 9 · PHYSICS · WEEK 2", "v–t GRAPHS: WORKED PROBLEMS", "Read → represent → calculate → interpret", "Every solution will keep the graph visible while the mathematical reasoning is built step by step.")

    def scene_01_problem_read_graph(self) -> None:
        self.set_header(1, "PROBLEM 1 · READ THE GRAPH BEFORE CALCULATING", "A particle has three constant-velocity intervals. Identify direction, rest and speed in each interval.")
        axes_group, axes = self.vt_axes(x_max=10, y_min=-4, y_max=5, width=7.2, height=4.1)
        segments = VGroup(Line(axes.c2p(0, 4), axes.c2p(3, 4), color=BLACK_LINE, stroke_width=3.4), Line(axes.c2p(3, 0), axes.c2p(5, 0), color=MID_GRAY, stroke_width=3.4), Line(axes.c2p(5, -2), axes.c2p(9, -2), color=DARK_GRAY, stroke_width=3.4))
        fig = VGroup(axes_group, segments)
        panel = self.figure_panel(fig, width=7.75, height=5.0, title="GIVEN v–t GRAPH", caption="First classify each segment. Do not calculate area yet.", title_size=31, caption_size=24)
        table = self.build_table(["Interval", "v", "Direction", "Speed"], [["0–3 s", "+4", "+ direction", "4 m/s"], ["3–5 s", "0", "rest", "0 m/s"], ["5–9 s", "−2", "− direction", "2 m/s"]], [1.25, 1.0, 1.7, 1.35], math_columns=(), row_height=0.72, header_height=0.76, body_font_size=25, header_font_size=24)
        self.fit(table.group, 5.65, 3.75)
        rule = self.note_panel("RULE", ["Direction comes from sign.", "Speed is |v|."], width=5.65, title_size=29, body_size=27)
        right = VGroup(table.group, rule).arrange(DOWN, buff=0.28)
        layout = self.split_layout(panel.group, right, left_width=7.75, right_width=5.7, max_height=5.28, center_y=-0.48, gap=0.35)
        self.assert_content_safe(layout.group, "problem 1")
        self.play(FadeIn(panel.box), FadeIn(panel.title), Create(axes_group), Create(segments), run_time=RUN_NORMAL)
        for row in table.rows:
            self.play(FadeIn(row, shift=RIGHT * 0.08), run_time=RUN_NORMAL); self.wait(PAUSE_READ)
        self.play(FadeIn(rule), FadeIn(panel.caption), run_time=RUN_NORMAL); self.wait(PAUSE_SUMMARY); self.clear_stage()

    def scene_02_problem_area_accounting(self) -> None:
        self.set_header(2, "PROBLEM 2 · DISPLACEMENT AND DISTANCE FROM v–t", "Use signed rectangles for displacement. Use the magnitudes of those displacements for total distance.")
        axes_group, axes = self.vt_axes(x_max=8, y_min=-3, y_max=4, width=6.9, height=4.05)
        segs = VGroup(); areas = VGroup()
        for t0, t1, v in PROBLEM_2_SEGMENTS:
            segs.add(Line(axes.c2p(t0, v), axes.c2p(t1, v), color=BLACK_LINE, stroke_width=3.3))
            if abs(v) > 1e-9: areas.add(self.signed_area_rectangle(axes, t0, t1, v, opacity=0.22))
        fig = VGroup(axes_group, areas, segs)
        panel = self.figure_panel(fig, width=7.55, height=5.0, title="0–2 s: +3 · 2–4 s: 0 · 4–7 s: −1", caption="Each rectangle contributes one signed displacement.", title_size=29, caption_size=24)
        steps = self.equation_stack([r"\Delta x_1=(+3)(2)=+6\,\mathrm{m}", r"\Delta x_2=(0)(2)=0\,\mathrm{m}", r"\Delta x_3=(-1)(3)=-3\,\mathrm{m}", r"\Delta x_{\rm total}=6+0-3=+3\,\mathrm{m}", r"d_{\rm total}=|6|+|0|+|-3|=9\,\mathrm{m}"], sizes=[34, 34, 34, 35, 35], buff=0.22, max_width=5.85, max_height=3.9)
        interpretation = self.note_panel("INTERPRET", ["Final position is 3 m ahead of the start.", "The object traveled 9 m in total."], width=5.85, title_size=29, body_size=26)
        right = VGroup(steps, interpretation).arrange(DOWN, buff=0.22)
        layout = self.split_layout(panel.group, right, left_width=7.55, right_width=5.9, max_height=5.28, center_y=-0.48, gap=0.34)
        self.assert_content_safe(layout.group, "problem 2")
        self.play(FadeIn(panel.box), FadeIn(panel.title), Create(axes_group), run_time=RUN_NORMAL)
        self.play(FadeIn(areas), Create(segs), run_time=RUN_NORMAL); self.wait(PAUSE_EXPLAIN)
        self.animate_equation_stack(steps, pause=PAUSE_READ)
        self.play(FadeIn(interpretation), FadeIn(panel.caption), run_time=RUN_NORMAL); self.wait(PAUSE_SUMMARY); self.clear_stage()

    def scene_03_problem_story_to_graph(self) -> None:
        self.set_header(3, "PROBLEM 3 · TURN A MOTION STORY INTO v–t", "Story: move right at 2 m/s for 3 s, stop for 2 s, then move left at 1 m/s for 4 s.")
        story = self.note_panel("GIVEN STORY", ["0–3 s: right at 2 m/s", "3–5 s: stopped", "5–9 s: left at 1 m/s"], width=6.2, title_size=30, body_size=28)
        rules = self.key_value_panel("TRANSLATE WORDS TO SIGNS", [("right", "+"), ("stopped", "0"), ("left", "-")], width=6.2, label_size=27, value_size=31)
        left = VGroup(story, rules).arrange(DOWN, buff=0.32)
        axes_group, axes = self.vt_axes(x_max=10, y_min=-3, y_max=4, width=6.3, height=3.85)
        s1 = Line(axes.c2p(0, 2), axes.c2p(3, 2), color=BLACK_LINE, stroke_width=3.5); s2 = Line(axes.c2p(3, 0), axes.c2p(5, 0), color=MID_GRAY, stroke_width=3.5); s3 = Line(axes.c2p(5, -1), axes.c2p(9, -1), color=DARK_GRAY, stroke_width=3.5)
        fig = VGroup(axes_group, s1, s2, s3)
        panel = self.figure_panel(fig, width=7.0, height=5.0, title="BUILD ONE SEGMENT AT A TIME", caption="The height gives velocity; the width gives how long that velocity lasts.", title_size=30, caption_size=24)
        layout = self.split_layout(left, panel.group, left_width=6.25, right_width=7.0, max_height=5.28, center_y=-0.48, gap=0.34)
        self.assert_content_safe(layout.group, "problem 3")
        self.play(FadeIn(story), FadeIn(rules), FadeIn(panel.box), FadeIn(panel.title), Create(axes_group), run_time=RUN_NORMAL)
        self.play(Create(s1), run_time=RUN_NORMAL); self.wait(PAUSE_EXPLAIN)
        self.play(Create(s2), run_time=RUN_NORMAL); self.wait(PAUSE_EXPLAIN)
        self.play(Create(s3), FadeIn(panel.caption), run_time=RUN_NORMAL); self.wait(PAUSE_SUMMARY); self.clear_stage()

    def scene_04_problem_xt_to_vt(self) -> None:
        self.set_header(4, "PROBLEM 4 · CONVERT x–t SLOPES INTO v–t LEVELS", "Find the slope of each straight x–t segment, then place that velocity at the same time interval on v–t.")
        xt_group, xt = self.xt_axes(x_max=6, y_max=12, width=5.9, height=3.65)
        p0, p1, p2, p3 = xt.c2p(0, 2), xt.c2p(2, 8), xt.c2p(4, 8), xt.c2p(6, 4)
        xt_segments = VGroup(Line(p0, p1, color=BLACK_LINE, stroke_width=3.3), Line(p1, p2, color=MID_GRAY, stroke_width=3.3), Line(p2, p3, color=DARK_GRAY, stroke_width=3.3))
        xt_fig = VGroup(xt_group, xt_segments)
        xt_panel = self.figure_panel(xt_fig, width=6.7, height=4.75, title="GIVEN x–t", caption="Compute slope Δx/Δt for each segment.", title_size=31, caption_size=24)
        eqs = self.equation_stack([r"v_1=\frac{8-2}{2-0}=+3\,\mathrm{m/s}", r"v_2=\frac{8-8}{4-2}=0\,\mathrm{m/s}", r"v_3=\frac{4-8}{6-4}=-2\,\mathrm{m/s}"], sizes=[33, 33, 33], buff=0.27, max_width=6.2, max_height=2.2)
        vt_group, vt = self.vt_axes(x_max=6, y_min=-3, y_max=4, width=5.8, height=3.55)
        vt_segments = VGroup(Line(vt.c2p(0, 3), vt.c2p(2, 3), color=BLACK_LINE, stroke_width=3.3), Line(vt.c2p(2, 0), vt.c2p(4, 0), color=MID_GRAY, stroke_width=3.3), Line(vt.c2p(4, -2), vt.c2p(6, -2), color=DARK_GRAY, stroke_width=3.3))
        vt_fig = VGroup(vt_group, vt_segments)
        vt_panel = self.figure_panel(vt_fig, width=6.7, height=4.75, title="RESULTING v–t", caption="Each x–t slope becomes one horizontal v–t level.", title_size=31, caption_size=24)
        top = VGroup(xt_panel.group, vt_panel.group).arrange(RIGHT, buff=0.40); self.fit(top, 13.6, 4.72); top.move_to(UP * 0.02)
        eqs.to_edge(DOWN, buff=0.42); self.fit(eqs, 13.0, 1.55)
        self.assert_content_safe(VGroup(top, eqs), "problem 4")
        self.play(FadeIn(xt_panel.box), FadeIn(xt_panel.title), Create(xt_group), Create(xt_segments), run_time=RUN_NORMAL)
        self.animate_equation_stack(eqs, pause=PAUSE_READ)
        self.play(FadeIn(vt_panel.box), FadeIn(vt_panel.title), Create(vt_group), run_time=RUN_NORMAL)
        for seg in vt_segments:
            self.play(Create(seg), run_time=RUN_NORMAL); self.wait(PAUSE_READ)
        self.play(FadeIn(xt_panel.caption), FadeIn(vt_panel.caption), run_time=RUN_NORMAL); self.wait(PAUSE_SUMMARY); self.clear_stage()

    def scene_05_problem_galileo_interpretation(self) -> None:
        self.set_header(5, "PROBLEM 5 · WHAT DOES THE GALILEO PATTERN TELL US?", "Equal time intervals show displacements 0.25, 0.75, 1.25 and 1.75 m. Is the velocity constant? Explain from the data.")
        table = self.build_table(["Interval", "Δt (s)", "Δx (m)"], [["1", "1", "0.25"], ["2", "1", "0.75"], ["3", "1", "1.25"], ["4", "1", "1.75"]], [1.35, 1.35, 1.5], row_height=0.72, header_height=0.78, body_font_size=27, header_font_size=25)
        self.fit(table.group, 5.6, 4.0)
        panel = self.figure_panel(table.group, width=6.3, height=4.85, title="SCHEMATIC EQUAL-TIME DATA", caption="These values illustrate the pattern; they are not claimed as Galileo's exact historical measurements.", title_size=29, caption_size=23)
        steps = self.equation_stack([r"\Delta t=1,1,1,1\ \mathrm{s}", r"\Delta x=0.25,0.75,1.25,1.75\ \mathrm{m}", r"\Delta x\ \text{increases while}\ \Delta t\ \text{stays equal}", r"\therefore\ \text{velocity is not constant}"], sizes=[36, 35, 33, 38], buff=0.32, max_width=6.4, max_height=3.1)
        answer = self.note_panel("PHYSICS INTERPRETATION", ["The object covers more distance in each equal time interval.", "Its speed is increasing down the ramp.", "Formal acceleration comes next in the course."], width=6.4, title_size=29, body_size=26)
        right = VGroup(steps, answer).arrange(DOWN, buff=0.25)
        layout = self.split_layout(panel.group, right, left_width=6.3, right_width=6.45, max_height=5.25, center_y=-0.48, gap=0.42)
        self.assert_content_safe(layout.group, "problem 5")
        self.play(FadeIn(panel.box), FadeIn(panel.title), run_time=RUN_NORMAL)
        self.animate_table_rows(table, pause=PAUSE_READ, include_header=True); self.wait(PAUSE_EXPLAIN)
        self.animate_equation_stack(steps, pause=PAUSE_READ)
        self.play(FadeIn(answer), FadeIn(panel.caption), run_time=RUN_NORMAL); self.wait(PAUSE_SUMMARY); self.clear_stage()

    def scene_06_final_checklist(self) -> None:
        self.set_header(6, "CHECK YOUR SOLUTION BEFORE YOU FINISH", "A correct answer includes the graph reading, the calculation and a physical interpretation with units and direction.")
        route = self.process_map([("1", "MARK EACH TIME INTERVAL"), ("2", "READ THE SIGN OF v"), ("3", "READ THE SPEED |v|"), ("4", "DRAW / IDENTIFY RECTANGLES"), ("5", "ADD SIGNED AREAS FOR Δx"), ("6", "STATE UNITS + DIRECTION")], card_width=4.45, card_height=1.12, columns=3)
        route.move_to(DOWN * 0.10); self.fit(route, 14.0, 3.6)
        final = self.note_panel("ONE-SENTENCE TEST", ["Can you explain what the sign, height, width and area mean physically?"], width=9.6, title_size=31, body_size=29)
        final.to_edge(DOWN, buff=0.48)
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in route], lag_ratio=0.10), run_time=RUN_SLOW * 1.8)
        self.wait(PAUSE_WORK); self.play(FadeIn(final), run_time=RUN_NORMAL); self.wait(PAUSE_FINAL)
        self.standard_closing("Read the graph first. Then calculate. Finally, translate the number back into motion.")


if __name__ == "__main__":
    validate_week2_data()
    print("Physics 9 Week 2 velocity-time lesson assertions passed.")
