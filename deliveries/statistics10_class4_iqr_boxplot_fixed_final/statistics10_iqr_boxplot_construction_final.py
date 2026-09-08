#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statistics 10 — IQR and Modified Box-Plot Construction Masterclass.

A professional, classroom-paced ManimCE animation derived from the visual
system used by the Grade 10 frequency-table, dispersion, and variance lesson.

Pedagogical route
-----------------
1. Order an unsorted dataset.
2. Locate the median Q2.
3. Exclude the median and split the data into equal halves.
4. Calculate Q1 and Q3 from the two middle pairs.
5. Compute and interpret the interquartile range.
6. Compute the 1.5-IQR fences.
7. Identify outliers and the actual whisker endpoints.
8. Construct a modified box plot element by element.
9. Interpret every graphical component.
10. Compare range and IQR under an extreme-value change.

Quartile convention
-------------------
For an odd number of observations, the overall median is excluded before
calculating Q1 and Q3.

Validated render commands
-------------------------
Preview:
    manim -pql statistics10_iqr_boxplot_construction_masterclass.py \
        Statistics10IQRBoxPlotConstruction \
        --format=mp4 --disable_caching

Final:
    manim -pqh statistics10_iqr_boxplot_construction_masterclass.py \
        Statistics10IQRBoxPlotConstruction \
        --format=mp4 --disable_caching

Timing control
--------------
    LESSON_TIME_SCALE=0.12  # accelerated complete QA render
    LESSON_TIME_SCALE=1.00  # full classroom pacing
"""

from __future__ import annotations

import math
import os
from dataclasses import dataclass
from statistics import median
from typing import Sequence

from manim import *


# =============================================================================
# RENDER CONFIGURATION
# =============================================================================
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE


# =============================================================================
# MONOCHROME VISUAL SYSTEM — SAME FAMILY AS THE CURRENT CODE BASE
# =============================================================================
BLACK_TEXT = BLACK
BLACK_LINE = BLACK
DARK_GRAY = "#303030"
MID_GRAY = "#707070"
LIGHT_GRAY = "#D3D3D3"
VERY_LIGHT_GRAY = "#EEEEEE"
PAPER_GRAY = "#F7F7F7"
WHITE_FILL = WHITE

FRAME_WIDTH = 16.0
FRAME_HEIGHT = 9.0
SAFE_WIDTH = 14.70
SAFE_HEIGHT = 7.55
TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

RUN_QUICK = 0.65
RUN_NORMAL = 0.95
RUN_SLOW = 1.30
RUN_CAMERA = 1.20

PAUSE_SHORT = 0.80
PAUSE_READ = 1.65
PAUSE_EXPLAIN = 2.50
PAUSE_WORK = 3.30
PAUSE_SUMMARY = 4.20
PAUSE_FINAL = 5.00


# =============================================================================
# VERIFIED LESSON DATA
# =============================================================================
RAW_DATA: tuple[int, ...] = (4, 15, 3, 7, 2, 8, 4, 6, 5)
ORDERED_DATA: tuple[int, ...] = tuple(sorted(RAW_DATA))
N = len(ORDERED_DATA)

Q2 = float(median(ORDERED_DATA))
LOWER_HALF = ORDERED_DATA[: N // 2]
UPPER_HALF = ORDERED_DATA[N // 2 + 1 :]
Q1 = float(median(LOWER_HALF))
Q3 = float(median(UPPER_HALF))
IQR = Q3 - Q1
LOWER_FENCE = Q1 - 1.5 * IQR
UPPER_FENCE = Q3 + 1.5 * IQR
OUTLIERS = tuple(x for x in ORDERED_DATA if x < LOWER_FENCE or x > UPPER_FENCE)
NON_OUTLIERS = tuple(x for x in ORDERED_DATA if LOWER_FENCE <= x <= UPPER_FENCE)
LOWER_WHISKER = min(NON_OUTLIERS)
UPPER_WHISKER = max(NON_OUTLIERS)
DATA_RANGE = max(ORDERED_DATA) - min(ORDERED_DATA)

EXTREME_DATA: tuple[int, ...] = tuple(150 if x == 15 else x for x in ORDERED_DATA)
EXTREME_Q2 = float(median(EXTREME_DATA))
EXTREME_Q1 = float(median(EXTREME_DATA[: N // 2]))
EXTREME_Q3 = float(median(EXTREME_DATA[N // 2 + 1 :]))
EXTREME_IQR = EXTREME_Q3 - EXTREME_Q1
EXTREME_RANGE = max(EXTREME_DATA) - min(EXTREME_DATA)


def validate_lesson_data() -> None:
    """Fail before rendering if any displayed numerical claim is inconsistent."""

    assert ORDERED_DATA == (2, 3, 4, 4, 5, 6, 7, 8, 15)
    assert N == 9
    assert Q2 == 5
    assert LOWER_HALF == (2, 3, 4, 4)
    assert UPPER_HALF == (6, 7, 8, 15)
    assert math.isclose(Q1, 3.5)
    assert math.isclose(Q3, 7.5)
    assert math.isclose(IQR, 4.0)
    assert math.isclose(LOWER_FENCE, -2.5)
    assert math.isclose(UPPER_FENCE, 13.5)
    assert OUTLIERS == (15,)
    assert NON_OUTLIERS == (2, 3, 4, 4, 5, 6, 7, 8)
    assert LOWER_WHISKER == 2
    assert UPPER_WHISKER == 8
    assert DATA_RANGE == 13
    assert EXTREME_Q1 == Q1
    assert EXTREME_Q2 == Q2
    assert EXTREME_Q3 == Q3
    assert EXTREME_IQR == IQR
    assert EXTREME_RANGE == 148


# =============================================================================
# SMALL STRUCTURES FOR REUSABLE GRAPHICS
# =============================================================================
@dataclass
class BoxPlotParts:
    axis: VGroup
    lower_cap: Line
    lower_whisker: Line
    box: Rectangle
    median_line: Line
    upper_whisker: Line
    upper_cap: Line
    outlier: Dot
    labels: VGroup


# =============================================================================
# MAIN SCENE
# =============================================================================
class Statistics10IQRBoxPlotConstruction(MovingCameraScene):
    """Final audited step-by-step construction of a modified box plot."""

    def setup(self) -> None:
        super().setup()
        validate_lesson_data()
        self.camera.background_color = WHITE
        self.camera.frame.set(width=FRAME_WIDTH).move_to(ORIGIN)
        self.header_group: VGroup | None = None
        self.subtitle_group: Mobject | None = None

    # ------------------------------------------------------------------
    # Timing wrappers
    # ------------------------------------------------------------------
    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration: float = DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # ------------------------------------------------------------------
    # Typography and safe layout
    # ------------------------------------------------------------------
    def text(self, content: str, size: int = 30, weight=NORMAL, **kwargs) -> Text:
        return Text(
            content,
            font_size=size,
            color=BLACK_TEXT,
            weight=weight,
            line_spacing=0.92,
            **kwargs,
        )

    def math(self, expression: str, size: int = 38, **kwargs) -> MathTex:
        return MathTex(expression, font_size=size, color=BLACK_TEXT, **kwargs)

    def fit(
        self,
        mob: Mobject,
        max_width: float = SAFE_WIDTH,
        max_height: float = SAFE_HEIGHT,
    ) -> Mobject:
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        if mob.height > max_height:
            mob.scale_to_fit_height(max_height)
        return mob

    def assert_within_frame(self, mob: Mobject, label: str, margin: float = 0.04) -> None:
        left, right = mob.get_left()[0], mob.get_right()[0]
        bottom, top = mob.get_bottom()[1], mob.get_top()[1]
        if left < -FRAME_WIDTH / 2 + margin or right > FRAME_WIDTH / 2 - margin:
            raise ValueError(f"{label} exceeds horizontal bounds: {left=:.3f}, {right=:.3f}")
        if bottom < -FRAME_HEIGHT / 2 + margin or top > FRAME_HEIGHT / 2 - margin:
            raise ValueError(f"{label} exceeds vertical bounds: {bottom=:.3f}, {top=:.3f}")

    def formula_panel(
        self,
        expression: str,
        width: float = 8.4,
        height: float = 1.18,
        font_size: int = 40,
    ) -> VGroup:
        panel = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=PAPER_GRAY,
            fill_opacity=1.0,
        )
        equation = self.math(expression, font_size)
        self.fit(equation, width - 0.58, height - 0.28)
        equation.move_to(panel)
        return VGroup(panel, equation)

    def note_panel(
        self,
        title: str,
        lines: Sequence[str],
        width: float = 6.4,
        title_size: int = 26,
        body_size: int = 23,
    ) -> VGroup:
        heading = self.text(title, title_size, BOLD)
        body = VGroup(*[self.text(line, body_size) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        content = VGroup(heading, body).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        self.fit(content, width - 0.62, 2.60)
        height = max(1.10, content.height + 0.62)
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.8,
            fill_color=WHITE_FILL,
            fill_opacity=1.0,
        )
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.31)
        return VGroup(box, content)

    def labeled_chip_panel(
        self,
        title: str,
        values: Sequence[int],
        fills: Sequence[str],
        width: float = 5.7,
    ) -> VGroup:
        """Create a data card where the title and chips occupy separate rows.

        The earlier version reused ``note_panel`` and then placed chips over its
        body text, which duplicated the values and created a visible overlap.
        This helper reserves explicit vertical zones for both elements.
        """

        panel = RoundedRectangle(
            width=width,
            height=1.62,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.8,
            fill_color=WHITE_FILL,
            fill_opacity=1.0,
        )
        heading = self.text(title, 25, BOLD)
        chips = self.chip_row(values, chip_width=0.98, buff=0.18, fills=fills)
        heading.next_to(panel.get_top(), DOWN, buff=0.18)
        heading.align_to(panel, LEFT).shift(RIGHT * 0.28)
        chips.next_to(heading, DOWN, buff=0.18)
        chips.set_x(panel.get_x())
        self.fit(chips, width - 0.42, 0.72)
        return VGroup(panel, heading, chips)

    def clean_text_swap(
        self,
        old_text: Mobject,
        new_text: Mobject,
        *simultaneous,
        run_time: float = RUN_NORMAL,
    ) -> Mobject:
        """Replace unlike text without glyph morphing or letter collisions."""

        self.play(FadeOut(old_text, shift=UP * 0.05), run_time=RUN_QUICK)
        self.remove(old_text)
        self.wait(0.05)
        self.play(
            FadeIn(new_text, shift=UP * 0.05),
            *simultaneous,
            run_time=run_time,
        )
        return new_text

    def set_header(self, number: int, title: str, subtitle: str) -> None:
        badge = RoundedRectangle(
            width=0.72,
            height=0.52,
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=WHITE_FILL,
            fill_opacity=1.0,
        )
        badge_text = self.text(f"{number:02d}", 23, BOLD).move_to(badge)
        title_text = self.text(title, 34, BOLD)
        self.fit(title_text, SAFE_WIDTH - 1.15, 0.58)
        row = VGroup(VGroup(badge, badge_text), title_text).arrange(RIGHT, buff=0.25)
        row.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.48)

        rule = Line(LEFT * 7.48, RIGHT * 7.48, color=LIGHT_GRAY, stroke_width=2)
        rule.next_to(row, DOWN, buff=0.07)

        words = subtitle.split()
        if len(subtitle) > 96:
            middle = len(words) // 2
            split = min(
                range(max(1, middle - 5), min(len(words), middle + 6)),
                key=lambda index: abs(
                    len(" ".join(words[:index])) - len(" ".join(words[index:]))
                ),
            )
            subtitle_mob = VGroup(
                self.text(" ".join(words[:split]), 20),
                self.text(" ".join(words[split:]), 20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        else:
            subtitle_mob = self.text(subtitle, 21)
        self.fit(subtitle_mob, 14.25, 0.72)
        subtitle_mob.next_to(rule, DOWN, buff=0.08).align_to(row, LEFT)

        new_header = VGroup(row, rule)
        old_header = self.header_group
        old_subtitle = self.subtitle_group
        self.header_group = new_header
        self.subtitle_group = subtitle_mob

        if old_header is None and old_subtitle is None:
            self.add(new_header, subtitle_mob)
        else:
            outgoing = [item for item in (old_header, old_subtitle) if item is not None]
            if outgoing:
                self.play(*[FadeOut(item) for item in outgoing], run_time=RUN_QUICK)
                self.remove(*outgoing)
                self.wait(0.08)
            self.play(FadeIn(new_header), FadeIn(subtitle_mob), run_time=RUN_QUICK)

    def clear_stage(self, keep_header: bool = True) -> None:
        keep_ids: set[int] = set()
        if keep_header:
            for persistent in (self.header_group, self.subtitle_group):
                if persistent is not None:
                    keep_ids.update(id(member) for member in persistent.get_family())
        removable = [mob for mob in self.mobjects if id(mob) not in keep_ids]
        if removable:
            self.play(*[FadeOut(mob) for mob in removable], run_time=RUN_NORMAL)
            self.remove(*removable)
        self.camera.frame.set(width=FRAME_WIDTH).move_to(ORIGIN)
        self.wait(0.10)

    def focus_on(self, mob: Mobject, width: float = 8.5, pause: float = PAUSE_READ) -> None:
        """Focus on one object without allowing surrounding content to clip.

        Every non-target context object fades before the camera moves. This
        prevents cards, axes, and equations from crossing the frame boundary
        during the zoom transition. The full context returns only after the
        16:9 camera has been restored.
        """

        persistent = [
            item for item in (self.header_group, self.subtitle_group) if item is not None
        ]
        target_ids = {id(item) for item in mob.get_family()}
        context = [
            item
            for item in self.mobjects
            if id(item) not in target_ids and item not in persistent
        ]
        outgoing = [*persistent, *context]
        if outgoing:
            self.play(*[FadeOut(item) for item in outgoing], run_time=RUN_QUICK)

        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.set(width=max(width, mob.width + 0.8)).move_to(mob),
            run_time=RUN_CAMERA,
        )
        self.wait(pause)
        self.play(Restore(self.camera.frame), run_time=RUN_CAMERA)

        if context:
            self.play(*[FadeIn(item) for item in context], run_time=RUN_QUICK)
        if persistent:
            self.play(*[FadeIn(item) for item in persistent], run_time=RUN_QUICK)

    # ------------------------------------------------------------------
    # Data chips and axes
    # ------------------------------------------------------------------
    def data_chip(
        self,
        value: int | str,
        width: float = 0.82,
        height: float = 0.68,
        fill_color: str = WHITE_FILL,
        font_size: int = 28,
    ) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=1.7,
            fill_color=fill_color,
            fill_opacity=1.0,
        )
        label = self.text(str(value), font_size, BOLD).move_to(box)
        return VGroup(box, label)

    def chip_row(
        self,
        values: Sequence[int | str],
        *,
        chip_width: float = 0.82,
        chip_height: float = 0.68,
        buff: float = 0.16,
        fills: Sequence[str] | None = None,
    ) -> VGroup:
        fills = fills or [WHITE_FILL] * len(values)
        row = VGroup(
            *[
                self.data_chip(value, chip_width, chip_height, fills[index])
                for index, value in enumerate(values)
            ]
        )
        row.arrange(RIGHT, buff=buff)
        return row

    def number_axis(
        self,
        minimum: float,
        maximum: float,
        step: float,
        *,
        width: float = 13.2,
        y: float = -0.25,
        label_every: float | None = None,
    ) -> tuple[VGroup, callable]:
        left = -width / 2
        right = width / 2

        def map_x(value: float) -> float:
            return left + (value - minimum) / (maximum - minimum) * width

        baseline = Line([left, y, 0], [right, y, 0], color=BLACK_LINE, stroke_width=2.5)
        ticks = VGroup()
        labels = VGroup()
        count = int(round((maximum - minimum) / step))
        label_every = label_every or step
        for index in range(count + 1):
            value = minimum + index * step
            x = map_x(value)
            tick_height = 0.18 if math.isclose((value - minimum) % label_every, 0, abs_tol=1e-9) else 0.11
            ticks.add(Line([x, y - tick_height, 0], [x, y + tick_height, 0], color=BLACK_LINE, stroke_width=1.7))
            ratio = (value - minimum) / label_every
            if math.isclose(ratio, round(ratio), abs_tol=1e-9):
                label_value = int(value) if math.isclose(value, round(value)) else value
                labels.add(self.text(str(label_value), 20).move_to([x, y - 0.40, 0]))
        axis = VGroup(baseline, ticks, labels)
        return axis, map_x

    def quartile_position_diagram(self) -> VGroup:
        line = Line(LEFT * 5.8, RIGHT * 5.8, color=BLACK_LINE, stroke_width=3)
        positions = [(-4.35, "Q1", "25%"), (0, "Q2", "50%"), (4.35, "Q3", "75%")]
        markers = VGroup()
        for x, name, percent in positions:
            tick = Line([x, -0.25, 0], [x, 0.25, 0], color=BLACK_LINE, stroke_width=3)
            name_text = self.math(name, 34).next_to(tick, UP, buff=0.16)
            pct = self.text(percent, 22, BOLD).next_to(tick, DOWN, buff=0.16)
            markers.add(VGroup(tick, name_text, pct))
        labels = VGroup(
            self.text("lower 25%", 22).move_to([-5.1, -0.92, 0]),
            self.text("middle 50%", 22, BOLD).move_to([0, -0.92, 0]),
            self.text("upper 25%", 22).move_to([5.1, -0.92, 0]),
        )
        return VGroup(line, markers, labels)

    def create_box_plot(
        self,
        *,
        axis_min: float = 0,
        axis_max: float = 16,
        axis_width: float = 13.0,
        center_y: float = -0.20,
        include_labels: bool = True,
    ) -> BoxPlotParts:
        axis, map_x = self.number_axis(
            axis_min,
            axis_max,
            1,
            width=axis_width,
            y=center_y - 1.55,
            label_every=1,
        )
        box_height = 1.55
        lower_cap = Line(
            [map_x(LOWER_WHISKER), center_y - 0.48, 0],
            [map_x(LOWER_WHISKER), center_y + 0.48, 0],
            color=BLACK_LINE,
            stroke_width=4,
        )
        lower_whisker = Line(
            [map_x(LOWER_WHISKER), center_y, 0],
            [map_x(Q1), center_y, 0],
            color=BLACK_LINE,
            stroke_width=4,
        )
        box = Rectangle(
            width=map_x(Q3) - map_x(Q1),
            height=box_height,
            stroke_color=BLACK_LINE,
            stroke_width=4,
            fill_color=VERY_LIGHT_GRAY,
            fill_opacity=1.0,
        ).move_to([(map_x(Q1) + map_x(Q3)) / 2, center_y, 0])
        median_line = Line(
            [map_x(Q2), center_y - box_height / 2, 0],
            [map_x(Q2), center_y + box_height / 2, 0],
            color=BLACK_LINE,
            stroke_width=5,
        )
        upper_whisker = Line(
            [map_x(Q3), center_y, 0],
            [map_x(UPPER_WHISKER), center_y, 0],
            color=BLACK_LINE,
            stroke_width=4,
        )
        upper_cap = Line(
            [map_x(UPPER_WHISKER), center_y - 0.48, 0],
            [map_x(UPPER_WHISKER), center_y + 0.48, 0],
            color=BLACK_LINE,
            stroke_width=4,
        )
        outlier = Dot([map_x(15), center_y, 0], radius=0.12, color=BLACK_LINE)

        labels = VGroup()
        if include_labels:
            label_specs = [
                (LOWER_WHISKER, "2", center_y - 1.02, NORMAL),
                (Q1, "Q1 = 3.5", center_y + 1.26, BOLD),
                (Q2, "Q2 = 5", center_y + 1.26, BOLD),
                (Q3, "Q3 = 7.5", center_y + 1.26, BOLD),
                (UPPER_WHISKER, "8", center_y - 1.02, NORMAL),
                (15, "outlier 15", center_y + 1.26, BOLD),
            ]
            for value, name, label_y, weight in label_specs:
                label = self.text(name, 20, weight)
                label.move_to([map_x(value), label_y, 0])
                labels.add(label)

        return BoxPlotParts(
            axis=axis,
            lower_cap=lower_cap,
            lower_whisker=lower_whisker,
            box=box,
            median_line=median_line,
            upper_whisker=upper_whisker,
            upper_cap=upper_cap,
            outlier=outlier,
            labels=labels,
        )

    # ------------------------------------------------------------------
    # Main orchestration
    # ------------------------------------------------------------------
    def construct(self) -> None:
        self.opening()
        self.core_vocabulary()
        self.order_the_data()
        self.find_median_and_halves()
        self.calculate_q1_q3()
        self.calculate_iqr()
        self.calculate_fences()
        self.identify_outlier_and_whiskers()
        self.construct_modified_box_plot()
        self.interpret_box_plot()
        self.compare_range_and_iqr()
        self.final_method_map()

    # ------------------------------------------------------------------
    # 01 — Opening
    # ------------------------------------------------------------------
    def opening(self) -> None:
        title = self.text("IQR AND BOX-PLOT CONSTRUCTION", 48, BOLD)
        subtitle = self.text(
            "From raw observations to a complete modified box plot",
            28,
        )
        heading = VGroup(title, subtitle).arrange(DOWN, buff=0.22)
        heading.to_edge(UP, buff=0.56)

        raw_label = self.text("Unsorted observations", 24, BOLD)
        raw_row = self.chip_row(RAW_DATA, chip_width=0.86, buff=0.18)
        raw_group = VGroup(raw_label, raw_row).arrange(DOWN, buff=0.22)
        raw_group.move_to(UP * 0.55)

        preview = self.create_box_plot(center_y=-1.35, include_labels=False)
        preview_group = VGroup(
            preview.axis,
            preview.lower_cap,
            preview.lower_whisker,
            preview.box,
            preview.median_line,
            preview.upper_whisker,
            preview.upper_cap,
            preview.outlier,
        )
        self.fit(preview_group, 13.9, 3.55)

        objective = self.note_panel(
            "LEARNING OBJECTIVE",
            [
                "Calculate Q1, Q2, Q3 and the IQR.",
                "Use 1.5 IQR fences to classify outliers.",
                "Construct and interpret every element of the graph.",
            ],
            width=9.2,
            title_size=27,
            body_size=23,
        )
        objective.to_edge(DOWN, buff=0.18)

        self.play(FadeIn(heading, shift=DOWN * 0.15), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(FadeIn(raw_group), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(
            LaggedStart(
                Create(preview.axis),
                Create(preview.lower_cap),
                Create(preview.lower_whisker),
                FadeIn(preview.box),
                Create(preview.median_line),
                Create(preview.upper_whisker),
                Create(preview.upper_cap),
                FadeIn(preview.outlier),
                lag_ratio=0.16,
            ),
            run_time=RUN_SLOW * 3.0,
        )
        self.wait(PAUSE_READ)
        self.play(FadeIn(objective), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        outgoing = list(self.mobjects)
        self.play(*[FadeOut(mob) for mob in outgoing], run_time=RUN_NORMAL)
        self.remove(*outgoing)
        self.wait(0.10)

    # ------------------------------------------------------------------
    # 02 — Vocabulary
    # ------------------------------------------------------------------
    def core_vocabulary(self) -> None:
        self.set_header(
            2,
            "THE LANGUAGE OF AN IQR GRAPH",
            "Quartiles divide ordered data by position; the modified box plot converts those positions into a compact graph.",
        )

        diagram = self.quartile_position_diagram().move_to(UP * 1.25)

        left = self.note_panel(
            "QUARTILES",
            [
                "Q1: median of the lower half.",
                "Q2: median of the complete dataset.",
                "Q3: median of the upper half.",
            ],
            width=6.55,
            body_size=24,
        )
        right = self.note_panel(
            "IQR AND OUTLIERS",
            [
                "IQR = Q3 - Q1: width of the middle 50%.",
                "Fences: Q1 - 1.5 IQR and Q3 + 1.5 IQR.",
                "Values beyond a fence are plotted separately.",
            ],
            width=6.95,
            body_size=23,
        )
        cards = VGroup(left, right).arrange(RIGHT, buff=0.36, aligned_edge=UP)
        cards.move_to(DOWN * 1.65)
        self.fit(cards, 14.1, 3.35)

        self.play(Create(diagram[0]), run_time=RUN_NORMAL)
        self.play(
            LaggedStart(*[FadeIn(marker, shift=UP * 0.10) for marker in diagram[1]], lag_ratio=0.22),
            run_time=RUN_SLOW * 1.7,
        )
        self.play(FadeIn(diagram[2]), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(left, shift=RIGHT * 0.15), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(right, shift=LEFT * 0.15), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 03 — Order data
    # ------------------------------------------------------------------
    def order_the_data(self) -> None:
        self.set_header(
            3,
            "STEP 1 — ORDER THE OBSERVATIONS",
            "Quartiles depend on position, so every value must be arranged from smallest to largest before any calculation.",
        )

        unsorted_label = self.text("Original order", 25, BOLD)
        unsorted = self.chip_row(RAW_DATA, chip_width=0.88, buff=0.18)
        top = VGroup(unsorted_label, unsorted).arrange(DOWN, buff=0.22).move_to(UP * 1.20)

        arrow = Arrow(UP * 0.20, DOWN * 0.55, color=BLACK_LINE, stroke_width=3)
        ordered_label = self.text("Ascending order", 25, BOLD)
        ordered = self.chip_row(ORDERED_DATA, chip_width=0.88, buff=0.18)
        positions = VGroup(*[self.text(str(index), 19) for index in range(1, N + 1)])
        for index, label in enumerate(positions):
            label.next_to(ordered[index], DOWN, buff=0.15)
        bottom = VGroup(ordered_label, VGroup(ordered, positions)).arrange(DOWN, buff=0.22)
        bottom.move_to(DOWN * 1.35)

        note = self.formula_panel(
            r"x_{(1)}\le x_{(2)}\le\cdots\le x_{(9)}",
            width=6.2,
            height=1.02,
            font_size=38,
        )
        note.to_edge(DOWN, buff=0.16)

        self.play(FadeIn(top), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(GrowArrow(arrow), run_time=RUN_NORMAL)
        self.play(FadeIn(ordered_label), run_time=RUN_QUICK)
        self.play(TransformFromCopy(unsorted, ordered), run_time=RUN_SLOW * 2.0)
        # Ensure the exact ordered row is present after the illustrative transformation.
        self.add(ordered)
        self.play(FadeIn(positions), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.play(FadeIn(note), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 04 — Median and halves
    # ------------------------------------------------------------------
    def find_median_and_halves(self) -> None:
        self.set_header(
            4,
            "STEP 2 — LOCATE Q2 AND SPLIT THE DATA",
            "With nine observations, the fifth ordered value is the median; our convention excludes it before finding Q1 and Q3.",
        )

        fills = [WHITE_FILL] * N
        fills[4] = LIGHT_GRAY
        row = self.chip_row(ORDERED_DATA, chip_width=0.92, buff=0.18, fills=fills)
        row.move_to(UP * 1.45)
        positions = VGroup(*[self.text(str(i), 19) for i in range(1, N + 1)])
        for index, label in enumerate(positions):
            label.next_to(row[index], UP, buff=0.14)

        median_arrow = Arrow(
            row[4].get_bottom() + DOWN * 0.85,
            row[4].get_bottom() + DOWN * 0.10,
            color=BLACK_LINE,
            stroke_width=3,
        )
        median_formula = self.formula_panel(r"Q_2=x_{(5)}=5", 5.2, 1.05, 43)
        median_formula.move_to(DOWN * 0.10)

        lower = self.chip_row(LOWER_HALF, chip_width=0.88, buff=0.16)
        upper = self.chip_row(UPPER_HALF, chip_width=0.88, buff=0.16)
        lower_group = VGroup(self.text("Lower half", 23, BOLD), lower).arrange(DOWN, buff=0.18)
        upper_group = VGroup(self.text("Upper half", 23, BOLD), upper).arrange(DOWN, buff=0.18)
        halves = VGroup(lower_group, upper_group).arrange(RIGHT, buff=2.25)
        halves.move_to(DOWN * 1.70)

        exclusion = self.note_panel(
            "IMPORTANT CONVENTION",
            ["Because n is odd, exclude Q2 from both halves."],
            width=8.2,
            title_size=25,
            body_size=24,
        )
        exclusion.to_edge(DOWN, buff=0.12)

        self.play(FadeIn(row), FadeIn(positions), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(GrowArrow(median_arrow), FadeIn(median_formula), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.play(
            LaggedStart(
                *[TransformFromCopy(row[i], lower[i]) for i in range(4)],
                *[TransformFromCopy(row[i + 5], upper[i]) for i in range(4)],
                lag_ratio=0.10,
            ),
            run_time=RUN_SLOW * 2.2,
        )
        self.add(lower, upper)
        self.play(FadeIn(lower_group[0]), FadeIn(upper_group[0]), run_time=RUN_QUICK)
        self.play(FadeIn(exclusion), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 05 — Q1 and Q3
    # ------------------------------------------------------------------
    def calculate_q1_q3(self) -> None:
        self.set_header(
            5,
            "STEP 3 — CALCULATE Q1 AND Q3",
            "Each half contains four values, so its median is the mean of the two central observations.",
        )

        lower_fills = [WHITE_FILL, LIGHT_GRAY, LIGHT_GRAY, WHITE_FILL]
        upper_fills = [WHITE_FILL, LIGHT_GRAY, LIGHT_GRAY, WHITE_FILL]

        lower_card = self.labeled_chip_panel("LOWER HALF", LOWER_HALF, lower_fills)
        upper_card = self.labeled_chip_panel("UPPER HALF", UPPER_HALF, upper_fills)
        halves = VGroup(lower_card, upper_card).arrange(RIGHT, buff=0.90)
        halves.move_to(UP * 1.12)

        q1_formula = self.formula_panel(r"Q_1=\frac{3+4}{2}=3.5", 5.9, 1.16, 43)
        q3_formula = self.formula_panel(r"Q_3=\frac{7+8}{2}=7.5", 5.9, 1.16, 43)
        formulas = VGroup(q1_formula, q3_formula).arrange(RIGHT, buff=0.70)
        formulas.move_to(DOWN * 0.75)

        summary = self.formula_panel(
            r"Q_1=3.5\qquad Q_2=5\qquad Q_3=7.5",
            8.9,
            1.10,
            42,
        )
        summary.to_edge(DOWN, buff=0.16)

        self.play(FadeIn(halves), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(q1_formula), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(q3_formula), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.play(FadeIn(summary), run_time=RUN_NORMAL)
        self.focus_on(summary, width=10.0, pause=PAUSE_EXPLAIN)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 06 — IQR
    # ------------------------------------------------------------------
    def calculate_iqr(self) -> None:
        self.set_header(
            6,
            "STEP 4 — COMPUTE THE INTERQUARTILE RANGE",
            "The IQR measures the horizontal width occupied by the central half of the ordered observations.",
        )

        axis, map_x = self.number_axis(0, 10, 1, width=12.0, y=-0.35, label_every=1)
        shade = Rectangle(
            width=map_x(Q3) - map_x(Q1),
            height=0.70,
            stroke_width=0,
            fill_color=LIGHT_GRAY,
            fill_opacity=0.75,
        ).move_to([(map_x(Q1) + map_x(Q3)) / 2, -0.35, 0])
        q1_line = DashedLine([map_x(Q1), -1.00, 0], [map_x(Q1), 1.15, 0], color=BLACK_LINE)
        q3_line = DashedLine([map_x(Q3), -1.00, 0], [map_x(Q3), 1.15, 0], color=BLACK_LINE)
        q1_label = self.math(r"Q_1=3.5", 34).next_to(q1_line, UP, buff=0.12)
        q3_label = self.math(r"Q_3=7.5", 34).next_to(q3_line, UP, buff=0.12)
        middle_label = self.text("middle 50%", 26, BOLD).move_to([0, 0.28, 0])
        graph = VGroup(shade, axis, q1_line, q3_line, q1_label, q3_label, middle_label)
        graph.move_to(UP * 0.85)

        formula = self.formula_panel(r"IQR=Q_3-Q_1=7.5-3.5=4", 8.3, 1.20, 43)
        formula.move_to(DOWN * 1.25)
        interpretation = self.note_panel(
            "INTERPRETATION",
            [
                "The central 50% spans 4 units.",
                "IQR ignores the lowest and highest quarters.",
                "A small IQR means the central values are tightly clustered.",
            ],
            width=10.5,
            body_size=24,
        )
        interpretation.to_edge(DOWN, buff=0.13)

        self.play(FadeIn(shade), Create(axis), run_time=RUN_NORMAL)
        self.play(Create(q1_line), Create(q3_line), FadeIn(q1_label), FadeIn(q3_label), run_time=RUN_NORMAL)
        self.play(FadeIn(middle_label), run_time=RUN_QUICK)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(formula), run_time=RUN_NORMAL)
        self.focus_on(formula, width=9.2, pause=PAUSE_EXPLAIN)
        self.play(FadeIn(interpretation), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 07 — Fences
    # ------------------------------------------------------------------
    def calculate_fences(self) -> None:
        self.set_header(
            7,
            "STEP 5 — CALCULATE THE OUTLIER FENCES",
            "The fences are decision boundaries. They are not automatically the endpoints of the whiskers.",
        )

        multiplier = self.formula_panel(r"1.5(IQR)=1.5(4)=6", 6.7, 1.10, 41)
        multiplier.move_to(UP * 1.55)

        lower = self.formula_panel(
            r"LF=Q_1-1.5(IQR)=3.5-6=-2.5",
            6.9,
            1.24,
            38,
        )
        upper = self.formula_panel(
            r"UF=Q_3+1.5(IQR)=7.5+6=13.5",
            6.9,
            1.24,
            38,
        )
        fences = VGroup(lower, upper).arrange(RIGHT, buff=0.38)
        fences.move_to(DOWN * 0.05)

        axis, map_x = self.number_axis(-3, 16, 1, width=13.4, y=-2.30, label_every=1)
        lower_fence_line = DashedLine([map_x(LOWER_FENCE), -2.85, 0], [map_x(LOWER_FENCE), -1.55, 0], color=BLACK_LINE)
        upper_fence_line = DashedLine([map_x(UPPER_FENCE), -2.85, 0], [map_x(UPPER_FENCE), -1.55, 0], color=BLACK_LINE)
        lf_label = self.text("LF = -2.5", 22, BOLD).next_to(lower_fence_line, UP, buff=0.08)
        uf_label = self.text("UF = 13.5", 22, BOLD).next_to(upper_fence_line, UP, buff=0.08)
        safe_label = self.text("non-outlier interval", 23, BOLD).move_to([0.0, -1.62, 0])
        graph = VGroup(axis, lower_fence_line, upper_fence_line, lf_label, uf_label, safe_label)

        self.play(FadeIn(multiplier), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(lower), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(upper), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.play(Create(axis), Create(lower_fence_line), Create(upper_fence_line), run_time=RUN_SLOW)
        self.play(FadeIn(lf_label), FadeIn(uf_label), FadeIn(safe_label), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 08 — Outlier and whisker endpoints
    # ------------------------------------------------------------------
    def identify_outlier_and_whiskers(self) -> None:
        self.set_header(
            8,
            "STEP 6 — CLASSIFY VALUES AND CHOOSE WHISKERS",
            "Compare each observation with the fences, then use the most extreme observed non-outliers as whisker endpoints.",
        )

        axis, map_x = self.number_axis(-3, 16, 1, width=13.4, y=-0.35, label_every=1)
        lf = DashedLine([map_x(LOWER_FENCE), -1.10, 0], [map_x(LOWER_FENCE), 1.30, 0], color=MID_GRAY)
        uf = DashedLine([map_x(UPPER_FENCE), -1.10, 0], [map_x(UPPER_FENCE), 1.30, 0], color=MID_GRAY)
        fence_labels = VGroup(
            self.text("LF", 21, BOLD).next_to(lf, UP, buff=0.08),
            self.text("UF", 21, BOLD).next_to(uf, UP, buff=0.08),
        )

        points = VGroup()
        point_labels = VGroup()
        for value in ORDERED_DATA:
            y = -0.35 + 0.22 if value == 4 and len([p for p in points if math.isclose(p.get_center()[0], map_x(4), abs_tol=1e-6)]) else -0.35
            dot = Dot([map_x(value), y, 0], radius=0.10, color=BLACK_LINE)
            points.add(dot)
        for value in sorted(set(ORDERED_DATA)):
            point_labels.add(self.text(str(value), 19).move_to([map_x(value), -0.92, 0]))

        outlier_ring = Circle(radius=0.22, color=BLACK_LINE, stroke_width=3).move_to([map_x(15), -0.35, 0])
        outlier_note = self.note_panel(
            "OUTLIER TEST",
            ["15 > 13.5, so 15 is an upper outlier."],
            width=6.7,
            title_size=26,
            body_size=24,
        ).move_to(UP * 2.15 + RIGHT * 2.9)

        whisker_note = self.note_panel(
            "WHISKER ENDPOINTS",
            [
                "Lower whisker: 2, the smallest non-outlier.",
                "Upper whisker: 8, the largest non-outlier.",
                "The whiskers do not stop at -2.5 and 13.5.",
            ],
            width=8.0,
            title_size=26,
            body_size=23,
        ).move_to(DOWN * 2.15)

        lower_arrow = Arrow([map_x(2), 1.55, 0], [map_x(2), 0.05, 0], color=BLACK_LINE, stroke_width=3)
        upper_arrow = Arrow([map_x(8), 1.55, 0], [map_x(8), 0.05, 0], color=BLACK_LINE, stroke_width=3)
        whisker_labels = VGroup(
            self.text("lower whisker = 2", 21, BOLD).next_to(lower_arrow, UP, buff=0.08),
            self.text("upper whisker = 8", 21, BOLD).next_to(upper_arrow, UP, buff=0.08),
        )

        self.play(Create(axis), Create(lf), Create(uf), FadeIn(fence_labels), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(dot, scale=0.5) for dot in points], lag_ratio=0.10), run_time=RUN_SLOW * 1.8)
        self.play(FadeIn(point_labels), run_time=RUN_QUICK)
        self.wait(PAUSE_EXPLAIN)
        self.play(
            Create(outlier_ring),
            FadeIn(outlier_note),
            FadeOut(fence_labels),
            run_time=RUN_NORMAL,
        )
        self.wait(PAUSE_WORK)
        self.play(
            FadeOut(outlier_note),
            FadeIn(fence_labels),
            GrowArrow(lower_arrow),
            GrowArrow(upper_arrow),
            FadeIn(whisker_labels),
            run_time=RUN_NORMAL,
        )
        self.remove(outlier_note)
        self.play(FadeIn(whisker_note), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 09 — Construct graph
    # ------------------------------------------------------------------
    def construct_modified_box_plot(self) -> None:
        self.set_header(
            9,
            "STEP 7 — CONSTRUCT THE MODIFIED BOX PLOT",
            "Build the graph in a fixed order so that every line has a mathematical meaning.",
        )

        # Keep labels hidden while the construction guide is present.  They are
        # introduced only after the guide has disappeared, avoiding collisions
        # between Q1/Q2/Q3 labels, the panel, and the developing box.
        parts = self.create_box_plot(center_y=-0.82, include_labels=False)

        steps = [
            "1. Draw a scaled number line.",
            "2. Mark Q1 and Q3; draw the box.",
            "3. Draw the median line at Q2.",
            "4. Connect Q1 to 2 and Q3 to 8.",
            "5. Plot 15 separately as an outlier.",
        ]
        step_panel = self.note_panel(
            "CONSTRUCTION ORDER",
            steps,
            width=6.65,
            title_size=24,
            body_size=20,
        )
        step_panel.move_to(UP * 2.02 + LEFT * 3.75)

        current_step = self.text("Scaled axis", 27, BOLD).move_to(UP * 2.05 + RIGHT * 3.55)

        self.play(FadeIn(step_panel), run_time=RUN_NORMAL)
        self.play(Create(parts.axis), FadeIn(current_step), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)

        next_step = self.text("Box from Q1 to Q3", 27, BOLD).move_to(current_step)
        current_step = self.clean_text_swap(
            current_step, next_step, FadeIn(parts.box), run_time=RUN_NORMAL
        )
        self.wait(PAUSE_EXPLAIN)

        next_step = self.text("Median at Q2", 27, BOLD).move_to(current_step)
        current_step = self.clean_text_swap(
            current_step, next_step, Create(parts.median_line), run_time=RUN_NORMAL
        )
        self.wait(PAUSE_EXPLAIN)

        next_step = self.text("Whiskers to observed non-outliers", 24, BOLD).move_to(current_step)
        current_step = self.clean_text_swap(
            current_step,
            next_step,
            Create(parts.lower_whisker),
            Create(parts.lower_cap),
            Create(parts.upper_whisker),
            Create(parts.upper_cap),
            run_time=RUN_SLOW,
        )
        self.wait(PAUSE_WORK)

        next_step = self.text("Outlier plotted separately", 27, BOLD).move_to(current_step)
        current_step = self.clean_text_swap(
            current_step,
            next_step,
            FadeIn(parts.outlier, scale=0.5),
            run_time=RUN_NORMAL,
        )
        self.wait(PAUSE_EXPLAIN)

        # Remove the instructional overlay before displaying final graph labels.
        self.play(FadeOut(step_panel), FadeOut(current_step), run_time=RUN_NORMAL)
        self.remove(step_panel, current_step)

        final_labels = self.create_box_plot(center_y=-0.82, include_labels=True).labels
        completion = self.text("Completed modified box plot", 28, BOLD).move_to(UP * 2.05)
        self.play(FadeIn(completion), FadeIn(final_labels), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 10 — Interpretation
    # ------------------------------------------------------------------
    def interpret_box_plot(self) -> None:
        self.set_header(
            10,
            "READ THE GRAPH, NOT JUST THE FORMULAS",
            "The box plot summarizes location, central spread, non-outlier extent, and unusual observations in one view.",
        )

        parts = self.create_box_plot(center_y=0.65, include_labels=True)
        plot = VGroup(
            parts.axis,
            parts.lower_cap,
            parts.lower_whisker,
            parts.box,
            parts.median_line,
            parts.upper_whisker,
            parts.upper_cap,
            parts.outlier,
            parts.labels,
        )
        plot.move_to(UP * 0.65)

        left = self.note_panel(
            "WHAT THE BOX SAYS",
            [
                "Q1 to Q3 contains the middle 50%.",
                "Its width is the IQR: 4 units.",
                "The median is closer to Q1 than to Q3.",
            ],
            width=6.75,
            body_size=23,
        )
        right = self.note_panel(
            "WHAT THE WHISKERS SAY",
            [
                "Non-outlier values extend from 2 to 8.",
                "15 is beyond the upper fence.",
                "A longer right side suggests greater upper-side spread.",
            ],
            width=6.75,
            body_size=23,
        )
        notes = VGroup(left, right).arrange(RIGHT, buff=0.38)
        notes.move_to(DOWN * 2.25)

        self.play(FadeIn(plot), run_time=RUN_SLOW)
        self.wait(PAUSE_WORK)
        self.play(FadeIn(left, shift=RIGHT * 0.12), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(right, shift=LEFT * 0.12), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 11 — Resistance comparison
    # ------------------------------------------------------------------
    def compare_range_and_iqr(self) -> None:
        self.set_header(
            11,
            "WHY IQR IS CALLED A RESISTANT MEASURE",
            "Changing only the largest extreme value can transform the range while leaving the quartiles and IQR unchanged.",
        )

        original = self.chip_row(ORDERED_DATA, chip_width=0.82, buff=0.13)
        modified = self.chip_row(EXTREME_DATA, chip_width=0.82, buff=0.13)
        original_label = self.text("Original maximum: 15", 24, BOLD)
        modified_label = self.text("Replace 15 with 150", 24, BOLD)
        left_group = VGroup(original_label, original).arrange(DOWN, buff=0.18)
        right_group = VGroup(modified_label, modified).arrange(DOWN, buff=0.18)
        rows = VGroup(left_group, right_group).arrange(DOWN, buff=0.46)
        rows.move_to(UP * 1.55)

        range_before = self.formula_panel(r"Range=15-2=13", 5.1, 0.90, 35)
        range_after = self.formula_panel(r"Range=150-2=148", 5.5, 0.90, 35)
        range_group = VGroup(range_before, range_after).arrange(DOWN, buff=0.14)

        iqr_before = self.formula_panel(r"Q_1=3.5,\;Q_3=7.5,\;IQR=4", 6.7, 0.90, 34)
        iqr_after = self.formula_panel(r"Q_1=3.5,\;Q_3=7.5,\;IQR=4", 6.7, 0.90, 34)
        iqr_group = VGroup(iqr_before, iqr_after).arrange(DOWN, buff=0.14)

        range_column = VGroup(self.text("RANGE", 23, BOLD), range_group).arrange(DOWN, buff=0.14)
        iqr_column = VGroup(self.text("IQR", 23, BOLD), iqr_group).arrange(DOWN, buff=0.14)
        comparison = VGroup(range_column, iqr_column).arrange(RIGHT, buff=0.48, aligned_edge=UP)
        comparison.move_to(DOWN * 1.52)

        conclusion = self.note_panel(
            "CONCLUSION",
            ["Range reacts directly to extremes; IQR follows the central positions."],
            width=10.0,
            title_size=25,
            body_size=24,
        )
        conclusion.to_edge(DOWN, buff=0.10)

        self.play(FadeIn(left_group), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(right_group), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.play(FadeIn(comparison[0]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(comparison[1]), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.play(FadeIn(conclusion), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 12 — Final method map
    # ------------------------------------------------------------------
    def final_method_map(self) -> None:
        self.set_header(
            12,
            "THE COMPLETE IQR AND BOX-PLOT ROUTE",
            "Use the same sequence every time: positions first, calculations second, graph construction last.",
        )

        steps = [
            ("1", "ORDER", r"2,3,4,4,5,6,7,8,15"),
            ("2", "MEDIAN", r"Q_2=5"),
            ("3", "SPLIT", r"\text{exclude }Q_2"),
            ("4", "LOWER QUARTILE", r"Q_1=3.5"),
            ("5", "UPPER QUARTILE", r"Q_3=7.5"),
            ("6", "IQR", r"Q_3-Q_1=4"),
            ("7", "FENCES", r"-2.5,\;13.5"),
            ("8", "OUTLIER", r"15>13.5"),
            ("9", "WHISKERS", r"2\text{ to }8"),
            ("10", "DRAW", r"\text{box, median, whiskers, point}"),
        ]

        def route_card(number: str, title: str, formula: str) -> VGroup:
            badge = RoundedRectangle(
                width=0.70,
                height=0.50,
                corner_radius=0.08,
                stroke_color=BLACK_LINE,
                stroke_width=1.5,
                fill_color=VERY_LIGHT_GRAY,
                fill_opacity=1.0,
            )
            num = self.text(number, 19, BOLD).move_to(badge)
            heading = self.text(title, 20, BOLD)
            top = VGroup(VGroup(badge, num), heading).arrange(RIGHT, buff=0.16)
            expression = self.math(formula, 22)
            content = VGroup(top, expression).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
            box = RoundedRectangle(
                width=6.75,
                height=1.00,
                corner_radius=0.12,
                stroke_color=BLACK_LINE,
                stroke_width=1.6,
                fill_color=WHITE_FILL,
                fill_opacity=1.0,
            )
            self.fit(content, 6.25, 0.78)
            content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.22)
            return VGroup(box, content)

        left_cards = VGroup(*[route_card(*step) for step in steps[:5]]).arrange(DOWN, buff=0.18)
        right_cards = VGroup(*[route_card(*step) for step in steps[5:]]).arrange(DOWN, buff=0.18)
        grid = VGroup(left_cards, right_cards).arrange(RIGHT, buff=0.40, aligned_edge=UP)
        grid.move_to(DOWN * 0.10)
        self.fit(grid, 14.15, 5.90)

        final_values = self.formula_panel(
            r"Q_1=3.5\qquad Q_2=5\qquad Q_3=7.5\qquad IQR=4",
            10.2,
            1.00,
            37,
        )
        final_values.to_edge(DOWN, buff=0.12)

        self.play(
            LaggedStart(
                *[FadeIn(card, shift=UP * 0.10) for card in list(left_cards) + list(right_cards)],
                lag_ratio=0.09,
            ),
            run_time=RUN_SLOW * 2.8,
        )
        self.wait(PAUSE_WORK)
        self.play(FadeIn(final_values), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)

        closing = VGroup(
            self.text("ORDER → QUARTILES → IQR → FENCES → BOX PLOT", 39, BOLD),
            self.text("Every line in the graph must come from a verified value.", 27),
        ).arrange(DOWN, buff=0.22)
        closing.move_to(ORIGIN)
        outgoing = list(self.mobjects)
        self.play(*[FadeOut(mob) for mob in outgoing], run_time=RUN_NORMAL)
        self.remove(*outgoing)
        self.wait(0.10)
        self.play(FadeIn(closing, shift=UP * 0.12), run_time=RUN_SLOW)
        self.wait(PAUSE_FINAL)
        self.play(FadeOut(closing), run_time=RUN_NORMAL)


if __name__ == "__main__":
    validate_lesson_data()
    print("IQR final-layout lesson assertions passed.")
    print(
        {
            "ordered_data": ORDERED_DATA,
            "Q1": Q1,
            "Q2": Q2,
            "Q3": Q3,
            "IQR": IQR,
            "lower_fence": LOWER_FENCE,
            "upper_fence": UPPER_FENCE,
            "outliers": OUTLIERS,
            "whiskers": (LOWER_WHISKER, UPPER_WHISKER),
        }
    )
