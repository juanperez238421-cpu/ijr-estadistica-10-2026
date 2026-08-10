#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""JP Classroom ManimCE Style Library.

Reusable base architecture derived from the class-layout conventions used in
`statistics10_frequency_variance_layout_v10(1).py`.

Design contract
---------------
- Horizontal Full HD 16:9, 1920x1080, 30 fps.
- White background.
- Black text / MathTex and neutral gray hierarchy.
- Persistent numbered section header + subtitle.
- Safe-layout fitting before animation.
- Custom tables with independently addressable cells/rows/columns.
- Controlled MovingCameraScene focus that temporarily hides the header.
- Centralized timing and LESSON_TIME_SCALE for QA previews.
- Geometry, equations and tables should coexist when pedagogically useful.
- Numerical/data claims should be validated before rendering.

Compatible target: Manim Community Edition 0.20.x.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence

import numpy as np
from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

BLACK_TEXT = BLACK
BLACK_LINE = BLACK
DARK_GRAY = "#303030"
MID_GRAY = "#787878"
LIGHT_GRAY = "#D7D7D7"
VERY_LIGHT_GRAY = "#F0F0F0"
PAPER_GRAY = "#F8F8F8"
WHITE_FILL = WHITE

FRAME_WIDTH = 16.0
FRAME_HEIGHT = 9.0
SAFE_WIDTH = 14.75
SAFE_HEIGHT = 7.65
CONTENT_TOP_Y = 2.60
CONTENT_BOTTOM_Y = -4.05

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))
RUN_QUICK = 0.70
RUN_NORMAL = 1.00
RUN_SLOW = 1.35
RUN_CAMERA = 1.25
PAUSE_SHORT = 0.85
PAUSE_READ = 1.80
PAUSE_EXPLAIN = 2.80
PAUSE_WORK = 3.80
PAUSE_SUMMARY = 4.60
PAUSE_FINAL = 5.20

@dataclass
class TableDiagram:
    group: VGroup
    rectangles: list[list[Rectangle]]
    entries: list[list[Mobject]]
    rows: list[VGroup]
    columns: list[VGroup]
    header: VGroup
    body: VGroup

@dataclass
class FigurePanel:
    group: VGroup
    box: RoundedRectangle
    figure: Mobject
    title: Mobject | None
    caption: Mobject | None

@dataclass
class SplitLayout:
    group: VGroup
    left: Mobject
    right: Mobject

class JPClassroomScene(MovingCameraScene):
    def setup(self) -> None:
        super().setup()
        self.validate_lesson_data()
        self.camera.background_color = WHITE
        self.camera.frame.set(width=FRAME_WIDTH).move_to(ORIGIN)
        self.header_group: VGroup | None = None
        self.subtitle_group: Mobject | None = None

    def validate_lesson_data(self) -> None:
        pass

    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration: float = 1.0, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    def text(self, content: str, size: int = 30, weight=NORMAL, **kwargs) -> Text:
        return Text(content, font_size=size, color=BLACK_TEXT, weight=weight, line_spacing=0.92, **kwargs)

    def math(self, expression: str, size: int = 38, **kwargs) -> MathTex:
        return MathTex(expression, font_size=size, color=BLACK_TEXT, **kwargs)

    def fit(self, mob: Mobject, max_width: float = SAFE_WIDTH, max_height: float = SAFE_HEIGHT) -> Mobject:
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        if mob.height > max_height:
            mob.scale_to_fit_height(max_height)
        return mob

    def fit_content_zone(self, mob: Mobject, max_width: float = 14.4, max_height: float = 5.85) -> Mobject:
        return self.fit(mob, max_width=max_width, max_height=max_height)

    def formula_panel(self, expression: str, width: float = 8.4, height: float = 1.25, font_size: int = 42, fill_opacity: float = 1.0) -> VGroup:
        panel = RoundedRectangle(width=width, height=height, corner_radius=0.12, stroke_color=BLACK_LINE, stroke_width=2.0, fill_color=PAPER_GRAY, fill_opacity=fill_opacity)
        equation = self.math(expression, font_size)
        self.fit(equation, width - 0.55, height - 0.28)
        equation.move_to(panel)
        return VGroup(panel, equation)

    def note_panel(self, title: str, lines: Sequence[str], width: float = 6.4, title_size: int = 26, body_size: int = 23, max_text_height: float = 2.55) -> VGroup:
        title_mob = self.text(title, title_size, BOLD)
        body = VGroup(*[self.text(line, body_size) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        content = VGroup(title_mob, body).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.fit(content, width - 0.62, max_text_height)
        box_height = max(1.10, content.height + 0.64)
        box = RoundedRectangle(width=width, height=box_height, corner_radius=0.12, stroke_color=BLACK_LINE, stroke_width=1.8, fill_color=WHITE_FILL, fill_opacity=1.0)
        content.move_to(box)
        content.align_to(box, LEFT).shift(RIGHT * 0.31)
        return VGroup(box, content)

    def key_value_panel(self, title: str, pairs: Sequence[tuple[str, str]], width: float = 6.0, label_size: int = 23, value_size: int = 28) -> VGroup:
        title_mob = self.text(title, 26, BOLD)
        rows = VGroup()
        for label, value in pairs:
            lhs = self.text(label, label_size, BOLD)
            rhs = self.math(value, value_size) if any(c in value for c in "_^\\=") else self.text(value, value_size)
            rows.add(VGroup(lhs, rhs).arrange(RIGHT, buff=0.25))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        content = VGroup(title_mob, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.fit(content, width - 0.60, 4.8)
        box = RoundedRectangle(width=width, height=max(1.3, content.height + 0.65), corner_radius=0.12, stroke_color=BLACK_LINE, stroke_width=1.8, fill_color=WHITE_FILL, fill_opacity=1)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.30)
        return VGroup(box, content)

    def clear_stage(self, keep_header: bool = True) -> None:
        keep_family_ids: set[int] = set()
        if keep_header:
            for persistent in (self.header_group, self.subtitle_group):
                if persistent is not None:
                    keep_family_ids.update(id(member) for member in persistent.get_family())
        removable = [mob for mob in self.mobjects if id(mob) not in keep_family_ids]
        if removable:
            self.play(*[FadeOut(mob) for mob in removable], run_time=RUN_NORMAL)
        self.camera.frame.set(width=FRAME_WIDTH).move_to(ORIGIN)

    def assert_within_frame(self, mob: Mobject, label: str, margin: float = 0.08) -> None:
        left_limit = -FRAME_WIDTH / 2 + margin
        right_limit = FRAME_WIDTH / 2 - margin
        bottom_limit = -FRAME_HEIGHT / 2 + margin
        top_limit = FRAME_HEIGHT / 2 - margin
        if mob.get_left()[0] < left_limit or mob.get_right()[0] > right_limit or mob.get_bottom()[1] < bottom_limit or mob.get_top()[1] > top_limit:
            raise ValueError(f"{label} exceeds frame bounds")

    def assert_content_safe(self, mob: Mobject, label: str) -> None:
        self.assert_within_frame(mob, label, margin=0.15)
        if mob.get_top()[1] > CONTENT_TOP_Y:
            raise ValueError(f"{label} overlaps the persistent header zone")
        if mob.get_bottom()[1] < CONTENT_BOTTOM_Y:
            raise ValueError(f"{label} exceeds the safe lower content zone")

    def build_table(self, headers: Sequence[str], body_rows: Sequence[Sequence[str]], column_widths: Sequence[float], *, math_columns: Iterable[int] = (), row_height: float = 0.62, header_height: float = 0.72, body_font_size: int = 25, header_font_size: int = 23) -> TableDiagram:
        data = [list(headers)] + [list(row) for row in body_rows]
        rectangles=[]; entries=[]; rows=[]
        math_columns=set(math_columns)
        y=0.0
        for r,row in enumerate(data):
            h=header_height if r==0 else row_height
            x=-sum(column_widths)/2
            rect_row=[]; entry_row=[]; row_group=VGroup()
            for c,(value,w) in enumerate(zip(row,column_widths)):
                rect=Rectangle(width=w,height=h,stroke_color=BLACK_LINE,stroke_width=1.5,fill_color=PAPER_GRAY if r==0 else WHITE_FILL,fill_opacity=1)
                rect.move_to([x+w/2,y-h/2,0])
                if c in math_columns and r>0:
                    entry=self.math(value, body_font_size)
                else:
                    entry=self.text(value, header_font_size if r==0 else body_font_size, BOLD if r==0 else NORMAL)
                self.fit(entry,w-0.18,h-0.14); entry.move_to(rect)
                rect_row.append(rect); entry_row.append(entry); row_group.add(rect,entry); x+=w
            rectangles.append(rect_row); entries.append(entry_row); rows.append(row_group); y-=h
        group=VGroup(*rows).move_to(ORIGIN)
        columns=[]
        for c in range(len(headers)):
            columns.append(VGroup(*[VGroup(rectangles[r][c],entries[r][c]) for r in range(len(rows))]))
        return TableDiagram(group,rectangles,entries,rows,columns,rows[0],VGroup(*rows[1:]))

    def animate_table_rows(self, table: TableDiagram, *, direction: np.ndarray = RIGHT, pause: float = PAUSE_SHORT, include_header: bool = True) -> None:
        start=0 if include_header else 1
        for index in range(start,len(table.rows)):
            self.play(FadeIn(table.rows[index], shift=direction*0.12), run_time=RUN_NORMAL)
            self.wait(pause)

    def figure_panel(self, figure: Mobject, *, width: float = 6.2, height: float = 4.5, title: str | None = None, caption: str | None = None, inner_margin: float = 0.28, title_size: int = 25, caption_size: int = 20) -> FigurePanel:
        box=RoundedRectangle(width=width,height=height,corner_radius=0.12,stroke_color=BLACK_LINE,stroke_width=1.8,fill_color=WHITE_FILL,fill_opacity=1)
        title_mob=self.text(title,title_size,BOLD) if title else None
        caption_mob=self.text(caption,caption_size) if caption else None
        top_reserve=0.52 if title_mob else 0.10
        bottom_reserve=0.58 if caption_mob else 0.10
        self.fit(figure,width-2*inner_margin,height-top_reserve-bottom_reserve-0.20)
        figure.move_to(box.get_center()+UP*(bottom_reserve-top_reserve)/2)
        if title_mob:
            self.fit(title_mob,width-0.45,0.45); title_mob.next_to(box.get_top(),DOWN,buff=0.18)
        if caption_mob:
            self.fit(caption_mob,width-0.45,0.48); caption_mob.next_to(box.get_bottom(),UP,buff=0.17)
        group=VGroup(box,figure)
        if title_mob: group.add(title_mob)
        if caption_mob: group.add(caption_mob)
        return FigurePanel(group,box,figure,title_mob,caption_mob)

    def split_layout(self, left: Mobject, right: Mobject, *, left_width: float = 6.7, right_width: float = 6.7, max_height: float = 5.5, gap: float = 0.45, center_y: float = -0.40) -> SplitLayout:
        self.fit(left,left_width,max_height); self.fit(right,right_width,max_height)
        left.move_to(LEFT*((right_width+gap)/2)+UP*center_y)
        right.move_to(RIGHT*((left_width+gap)/2)+UP*center_y)
        group=VGroup(left,right); self.fit_content_zone(group,max_width=14.4,max_height=max_height)
        return SplitLayout(group,left,right)

    def equation_stack(self, equations: Sequence[str], *, sizes: Sequence[int] | None = None, buff: float = 0.26, max_width: float = 7.2, max_height: float = 4.8) -> VGroup:
        sizes=sizes or [36]*len(equations)
        mobs=VGroup(*[self.math(eq,size) for eq,size in zip(equations,sizes)])
        mobs.arrange(DOWN,aligned_edge=LEFT,buff=buff); self.fit(mobs,max_width,max_height); return mobs

    def animate_equation_stack(self, stack: VGroup, *, pause: float = PAUSE_READ) -> None:
        for line in stack:
            self.play(FadeIn(line, shift=RIGHT*0.10), run_time=RUN_NORMAL); self.wait(pause)

    def process_map(self, steps: Sequence[tuple[str,str]], *, card_width: float = 4.4, card_height: float = 1.05, columns: int = 3) -> VGroup:
        cards=VGroup()
        for n,label in steps:
            badge=RoundedRectangle(width=0.46,height=0.34,corner_radius=0.07,stroke_color=BLACK_LINE,stroke_width=1.5,fill_color=PAPER_GRAY,fill_opacity=1)
            num=self.text(n,18,BOLD).move_to(badge)
            txt=self.text(label,22,BOLD); self.fit(txt,card_width-0.95,card_height-0.28)
            content=VGroup(VGroup(badge,num),txt).arrange(RIGHT,buff=0.18)
            card=RoundedRectangle(width=card_width,height=card_height,corner_radius=0.10,stroke_color=BLACK_LINE,stroke_width=1.6,fill_color=WHITE_FILL,fill_opacity=1)
            content.move_to(card); cards.add(VGroup(card,content))
        rows=[]
        for i in range(0,len(cards),columns):
            row=VGroup(*cards[i:i+columns]).arrange(RIGHT,buff=0.28); rows.append(row)
        return VGroup(*rows).arrange(DOWN,buff=0.28)

    def standard_opening(self, grade_line: str, title: str, subtitle: str, statement: str) -> None:
        grade=self.text(grade_line,27,BOLD)
        title_m=self.text(title,48,BOLD); self.fit(title_m,13.8,0.85)
        sub=self.text(subtitle,30,MEDIUM); self.fit(sub,13.2,0.65)
        rule=Line(LEFT*3.1,RIGHT*3.1,color=LIGHT_GRAY,stroke_width=2)
        body=self.text(statement,27); self.fit(body,13.0,0.9)
        stack=VGroup(grade,title_m,rule,sub,body).arrange(DOWN,buff=0.24).move_to(ORIGIN)
        self.play(FadeIn(grade),run_time=RUN_NORMAL); self.play(FadeIn(title_m),run_time=RUN_NORMAL); self.play(Create(rule),FadeIn(sub),run_time=RUN_NORMAL); self.play(FadeIn(body),run_time=RUN_NORMAL); self.wait(PAUSE_SUMMARY); self.play(FadeOut(stack),run_time=RUN_NORMAL)

    def standard_closing(self, statement: str) -> None:
        self.clear_stage(keep_header=False)
        text=self.text(statement,34,MEDIUM); self.fit(text,13.6,1.4); text.move_to(ORIGIN)
        self.play(FadeIn(text),run_time=RUN_NORMAL); self.wait(PAUSE_FINAL); self.play(FadeOut(text),run_time=RUN_NORMAL)

class JPMathClassroomScene(JPClassroomScene):
    pass

class JPThreeDClassroomScene(ThreeDScene):
    pass

def assert_close(actual: float, expected: float, *, tol: float = 1e-10, label: str = "value") -> None:
    if abs(actual-expected)>tol:
        raise AssertionError(f"{label}: expected {expected}, got {actual}")

def validate_relative_asset(path: str | Path) -> Path:
    path=Path(path)
    if path.is_absolute():
        raise ValueError("Asset paths must be project-relative")
    if not path.exists():
        raise FileNotFoundError(path)
    return path

def validate_all(checks: Sequence[tuple[str,Callable[[],bool]]]) -> None:
    for label,check in checks:
        if not check():
            raise AssertionError(label)
