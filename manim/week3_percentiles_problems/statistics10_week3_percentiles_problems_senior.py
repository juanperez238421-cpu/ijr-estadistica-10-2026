#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statistics 10 · Period 1 · Week 3 — Deciles & Percentiles Problems.

Senior Problems Edition · direct continuation of the Week 3 Senior FINAL theory.

Course convention used throughout:
    L = (k / 100) (n + 1)

If L is an integer, use that 1-indexed ordered position.
If L = j + d with 0 < d < 1, interpolate:
    P_k = x_j + d (x_{j+1} - x_j)

Eight-step workshop recipe:
1. ORDER
2. COUNT n
3. CHOOSE k
4. LOCATE L
5. NEIGHBORS
6. INTERPOLATE
7. STATE
8. INTERPRET

Target: Manim Community Edition 0.20.x, 1920x1080, 30 fps, white JP classroom
style. Final render must use literal `-pqh`.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import floor
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
MID = "#777777"
LIGHT = "#D6D6D6"
VERY_LIGHT = "#EEEEEE"
PAPER = "#F8F8F8"
SAFE_W = 14.65

RUN_FAST = 0.42
RUN = 0.76
RUN_SLOW = 1.02
PAUSE_READ = 1.25
PAUSE_EXPLAIN = 2.0
PAUSE_WORK = 3.8
PAUSE_SUMMARY = 3.2

@dataclass(frozen=True)
class PercentileSolution:
    raw: tuple[float, ...]
    ordered: tuple[float, ...]
    k: float
    locator: float
    lower_position: int
    upper_position: int
    fraction: float
    value: float

def fmt(v: float) -> str:
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:.2f}".rstrip("0").rstrip(".")

def percentile_course(values: Sequence[float], k: float) -> PercentileSolution:
    if len(values) < 3:
        raise ValueError("At least three observations are required.")
    if not (0 < k < 100):
        raise ValueError("k must satisfy 0 < k < 100.")
    ordered = tuple(sorted(float(v) for v in values))
    n = len(ordered)
    locator = (k / 100.0) * (n + 1)
    if locator < 1 or locator > n:
        raise ValueError("Chosen percentile falls outside the interior locator range.")
    j = floor(locator)
    fraction = locator - j
    if abs(fraction) < 1e-9:
        lower_position = upper_position = j
        value = ordered[j - 1]
        fraction = 0.0
    else:
        lower_position = j
        upper_position = j + 1
        low = ordered[j - 1]
        high = ordered[j]
        value = low + fraction * (high - low)
    return PercentileSolution(tuple(float(v) for v in values), ordered, float(k), float(locator), lower_position, upper_position, float(fraction), float(value))

class Statistics10Week3PercentilesProblemsSenior(MovingCameraScene):
    STEP_NAMES = ("ORDER", "COUNT n", "CHOOSE k", "LOCATE L", "NEIGHBORS", "INTERPOLATE", "STATE", "INTERPRET")
    P1 = ((28, 14, 22, 35, 18, 31, 12, 26, 20), 20)
    P2 = ((42, 25, 33, 18, 30, 36, 21, 39, 27), 60)
    P3 = ((16, 8, 19, 11, 14, 25, 10, 21, 13, 18, 23), 35)
    P4 = ((55, 32, 47, 61, 28, 44, 39, 52, 35, 58, 30, 49, 42, 63), 72)
    P5 = ((5, 8, 8, 10, 10, 10, 12, 15, 18), 45)
    P6 = ((12, 18, 21, 25, 29, 32, 36, 40, 45), 70)
    P7 = ((-8, 4, -2, 10, 6, -5, 0, 8, 2), 30)
    P8 = ((62, 48, 55, 71, 39, 67, 44, 59, 75), 55)

    def setup(self):
        super().setup()
        self.camera.background_color = WHITE
        self.camera.frame.set(width=16).move_to(ORIGIN)
        self.header = None
        self.step_strip = None
        self._validate_workshop()

    def _validate_workshop(self):
        expected = ((self.P1,2.0,14.0),(self.P2,6.0,33.0),(self.P3,4.2,13.2),(self.P4,10.8,54.4),(self.P5,4.5,10.0),(self.P6,7.0,36.0),(self.P7,3.0,-2.0),(self.P8,5.5,60.5))
        for values_k, loc, val in expected:
            values, k = values_k
            sol = percentile_course(values, k)
            assert abs(sol.locator - loc) < 1e-9
            assert abs(sol.value - val) < 1e-9
        assert percentile_course(self.P5[0], self.P5[1]).ordered[3:5] == (10.0, 10.0)

    def t(self, content, size=29, weight=NORMAL, color=INK, **kwargs):
        return Text(content, font_size=size, color=color, weight=weight, line_spacing=0.92, **kwargs)

    def m(self, expr, size=40, color=INK, **kwargs):
        return MathTex(expr, font_size=size, color=color, **kwargs)

    def fit(self, mob, w=SAFE_W, h=5.75):
        if mob.width > w: mob.scale_to_fit_width(w)
        if mob.height > h: mob.scale_to_fit_height(h)
        return mob

    def panel(self, width, height, fill=PAPER, stroke=LIGHT, sw=1.5):
        return RoundedRectangle(width=width,height=height,corner_radius=0.12,stroke_color=stroke,stroke_width=sw,fill_color=fill,fill_opacity=1)

    def note(self, text, width=11.0, height=0.82, size=25):
        box = self.panel(width, height, fill=VERY_LIGHT)
        tx = self.t(text, size, NORMAL, color=DARK)
        self.fit(tx, w=width-0.45, h=height-0.18)
        tx.move_to(box)
        return VGroup(box, tx)

    def set_header(self, section, subtitle):
        if self.header is not None: self.remove(self.header)
        label = self.t(section,23,BOLD,color=DARK).to_edge(UL,buff=0.42)
        sub = self.t(subtitle,24,NORMAL,color=MID).next_to(label,RIGHT,buff=0.34)
        line = Line(LEFT*7.55,RIGHT*7.55,color=LIGHT,stroke_width=1.6)
        line.next_to(label,DOWN,buff=0.20).align_to(label,LEFT)
        self.header = VGroup(label,sub,line)
        self.add(self.header)

    def clear_stage(self, keep_header=True, keep_steps=False):
        keep=set()
        if keep_header and self.header is not None: keep.add(self.header)
        if keep_steps and self.step_strip is not None: keep.add(self.step_strip)
        removable=[mob for mob in self.mobjects if mob not in keep]
        if removable: self.play(*[FadeOut(mob) for mob in removable],run_time=RUN_FAST)
        if keep_header and self.header is not None and self.header not in self.mobjects: self.add(self.header)
        if keep_steps and self.step_strip is not None and self.step_strip not in self.mobjects: self.add(self.step_strip)

    def value_card(self, value, width=0.88, height=0.70, fill=WHITE):
        box=RoundedRectangle(width=width,height=height,corner_radius=0.09,stroke_color=DARK,stroke_width=1.5,fill_color=fill,fill_opacity=1)
        tx=self.t(fmt(float(value)),27,BOLD).move_to(box)
        return VGroup(box,tx)

    def data_row(self, values, y, label=None, max_width=12.8):
        cards=VGroup(*[self.value_card(v) for v in values]).arrange(RIGHT,buff=0.13)
        if cards.width>max_width: cards.scale_to_fit_width(max_width)
        cards.move_to([0.65 if label else 0,y,0])
        if label:
            lab=self.t(label,23,BOLD,color=MID).next_to(cards,LEFT,buff=0.28)
            return VGroup(lab,cards)
        return cards

    def indexed_row(self, values, y=1.56):
        width=0.90 if len(values)<=11 else 0.78
        cards=VGroup(*[self.value_card(v,width=width,height=0.66) for v in values]).arrange(RIGHT,buff=0.10)
        if cards.width>12.65: cards.scale_to_fit_width(12.65)
        cards.move_to([0,y,0])
        indices=VGroup()
        for i,card in enumerate(cards,start=1): indices.add(self.t(str(i),18,NORMAL,color=MID).next_to(card,DOWN,buff=0.08))
        return VGroup(cards,indices)

    def build_step_strip(self, active=1):
        cells=VGroup()
        for i,name in enumerate(self.STEP_NAMES,start=1):
            fill="#EAEAEA" if i==active else WHITE
            sw=2.5 if i==active else 1.15
            box=RoundedRectangle(width=1.76,height=0.72,corner_radius=0.08,stroke_color=DARK if i==active else LIGHT,stroke_width=sw,fill_color=fill,fill_opacity=1)
            num=self.t(str(i),19,BOLD,color=DARK)
            lab=self.t(name,15.2,BOLD if i==active else NORMAL,color=DARK if i==active else MID)
            content=VGroup(num,lab).arrange(RIGHT,buff=0.11)
            self.fit(content,w=1.54,h=0.42); content.move_to(box)
            cells.add(VGroup(box,content))
        strip=cells.arrange(RIGHT,buff=0.075); strip.move_to([0,-3.60,0]); return strip

    def set_step(self, active):
        new=self.build_step_strip(active)
        if self.step_strip is None or self.step_strip not in self.mobjects:
            self.step_strip=new; self.play(FadeIn(new),run_time=RUN_FAST)
        else: self.play(Transform(self.step_strip,new),run_time=RUN_FAST)

    def locator_marker(self, indexed, locator, label_tex):
        cards=indexed[0]; j=floor(locator); d=locator-j
        if abs(d)<1e-9: x=cards[j-1].get_center()[0]
        else:
            x0=cards[j-1].get_center()[0]; x1=cards[j].get_center()[0]; x=x0+d*(x1-x0)
        arrow=Arrow([x,2.52,0],[x,2.04,0],buff=0.03,color=DARK,stroke_width=3,max_tip_length_to_length_ratio=0.22)
        label=self.m(label_tex,31).next_to(arrow,UP,buff=0.04)
        return VGroup(arrow,label)

    def interpolation_track(self, low, high, fraction, result, y=-1.15):
        x0,x1=-3.55,3.55
        line=Line([x0,y,0],[x1,y,0],color=DARK,stroke_width=3)
        left_tick=Line([x0,y-0.16,0],[x0,y+0.16,0],color=DARK,stroke_width=2)
        right_tick=Line([x1,y-0.16,0],[x1,y+0.16,0],color=DARK,stroke_width=2)
        xm=x0+fraction*(x1-x0); mark=Dot([xm,y,0],radius=0.075,color=DARK)
        low_lab=self.t(fmt(low),24,BOLD).next_to(left_tick,DOWN,buff=0.12)
        high_lab=self.t(fmt(high),24,BOLD).next_to(right_tick,DOWN,buff=0.12)
        res_lab=self.t(fmt(result),26,BOLD).next_to(mark,UP,buff=0.12)
        frac_lab=self.m(rf"d={fmt(fraction)}",30).next_to(line,UP,buff=0.55)
        return VGroup(line,left_tick,right_tick,mark,low_lab,high_lab,res_lab,frac_lab)

    def variable_cards(self, sol, decile_name=None):
        k_label=f"k = {fmt(sol.k)}" if not decile_name else f"{decile_name} → P{fmt(sol.k)}"
        labels=(k_label,f"n = {len(sol.ordered)}",f"L = {fmt(sol.locator)}",f"d = {fmt(sol.fraction)}")
        cards=VGroup()
        for label in labels:
            box=self.panel(2.62,0.70,fill=WHITE); tx=self.t(label,22,BOLD,color=DARK); self.fit(tx,w=2.35,h=0.42); tx.move_to(box); cards.add(VGroup(box,tx))
        cards.arrange(RIGHT,buff=0.20); return cards

    def opening(self):
        title=self.t("STATISTICS 10 · WEEK 3",31,BOLD,color=DARK)
        subtitle=self.t("DECILES & PERCENTILES · PROBLEM WORKSHOP",42,BOLD)
        line=self.t("Position first. Formula second. Interpretation always.",27,NORMAL,color=MID)
        group=VGroup(title,subtitle,line).arrange(DOWN,buff=0.32).move_to(UP*0.55)
        self.play(FadeIn(title),Write(subtitle),run_time=RUN_SLOW); self.play(FadeIn(line),run_time=RUN)
        recipe=self.note("Use exactly the same 8-step method from the Senior theory class.",11.6,0.84,25).move_to([0,-1.62,0])
        self.play(FadeIn(recipe),run_time=RUN); self.wait(PAUSE_READ); self.play(FadeOut(group),FadeOut(recipe),run_time=RUN_FAST)

    def workshop_map(self):
        self.set_header("WORKSHOP MAP","Eight problems · each one isolates a different decision")
        items=(("P1","Integer locator"),("P2","Decile → percentile"),("P3","Interpolation d = 0.2"),("P4","Interpolation d = 0.8"),("P5","Repeated values"),("P6","Error analysis"),("P7","Negative values"),("P8","Final challenge"))
        cards=VGroup()
        for tag,desc in items:
            box=self.panel(3.18,1.22,fill=WHITE); tg=self.t(tag,24,BOLD,color=DARK); ds=self.t(desc,22,NORMAL,color=MID); content=VGroup(tg,ds).arrange(DOWN,buff=0.10); self.fit(content,w=2.80,h=0.78); content.move_to(box); cards.add(VGroup(box,content))
        rows=VGroup(VGroup(*cards[:4]).arrange(RIGHT,buff=0.27),VGroup(*cards[4:]).arrange(RIGHT,buff=0.27)).arrange(DOWN,buff=0.34).move_to([0,0.34,0])
        self.play(LaggedStart(*[FadeIn(c,shift=UP*0.08) for c in cards],lag_ratio=0.08),run_time=2.0)
        note=self.note("Goal: recognize the TYPE of percentile problem before calculating.",11.8,0.84,25).move_to([0,-2.35,0]); self.play(FadeIn(note),run_time=RUN); self.wait(PAUSE_EXPLAIN); self.clear_stage()

    def solve_problem(self, number, values, k, title, focus, decile_name=None, special_note=None):
        sol=percentile_course(values,k); self.set_header(f"PROBLEM {number} · {title}",focus); self.set_step(1)
        raw=self.data_row(sol.raw,1.58,"RAW",max_width=12.65)
        prompt_name=f"Find {decile_name}" if decile_name else f"Find P{fmt(k)}"
        prompt=self.note(f"{prompt_name}. Show all 8 steps before checking the solution.",11.8,0.82,25).move_to([0,0.56,0])
        self.play(FadeIn(raw),FadeIn(prompt),run_time=RUN); self.wait(PAUSE_WORK)
        indexed=self.indexed_row(sol.ordered,1.58); self.play(FadeOut(prompt),Transform(raw,indexed),run_time=RUN_SLOW)
        self.set_step(2); n_eq=self.m(rf"n={len(sol.ordered)}",39).move_to([-2.25,0.48,0]); self.play(Write(n_eq),run_time=RUN_FAST)
        self.set_step(3)
        if decile_name: k_eq=self.m(rf"{decile_name}=P_{{{int(k)}}}\quad\Rightarrow\quad k={int(k)}",38).move_to([1.65,0.48,0])
        else: k_eq=self.m(rf"k={fmt(k)}",39).move_to([1.65,0.48,0])
        self.play(Write(k_eq),run_time=RUN_FAST)
        self.set_step(4); loc_eq=self.m(rf"L=\frac{{{fmt(k)}}}{{100}}({len(sol.ordered)}+1)={fmt(sol.locator)}",43).move_to([0,-0.14,0]); self.play(Write(loc_eq),run_time=RUN)
        marker=self.locator_marker(indexed,sol.locator,rf"L={fmt(sol.locator)}"); self.play(FadeIn(marker),run_time=RUN)
        self.set_step(5); cards=indexed[0]
        for pos in sorted(set((sol.lower_position,sol.upper_position))): self.play(Indicate(cards[pos-1],color=DARK,scale_factor=1.10),run_time=RUN_FAST)
        if sol.lower_position==sol.upper_position: neigh_text=f"Position {sol.lower_position} → x{sol.lower_position} = {fmt(sol.value)}"
        else:
            low=sol.ordered[sol.lower_position-1]; high=sol.ordered[sol.upper_position-1]; neigh_text=f"Positions {sol.lower_position} and {sol.upper_position} → {fmt(low)} and {fmt(high)}"
        neighbors=self.t(neigh_text,26,BOLD,color=DARK).move_to([0,-0.77,0]); self.play(FadeIn(neighbors),run_time=RUN)
        self.set_step(6); self.play(FadeOut(n_eq),FadeOut(k_eq),FadeOut(loc_eq),FadeOut(neighbors),run_time=RUN_FAST); track=None
        if sol.fraction==0:
            calc=self.m(rf"P_{{{int(k)}}}=x_{{{sol.lower_position}}}={fmt(sol.value)}",48).move_to([0,-1.52,0]); no_interp=self.note("Integer locator → one ordered position → no interpolation.",10.4,0.68,23).move_to([0,-2.24,0]); self.play(Write(calc),FadeIn(no_interp),run_time=RUN_SLOW)
        else:
            low=sol.ordered[sol.lower_position-1]; high=sol.ordered[sol.upper_position-1]; track=self.interpolation_track(low,high,sol.fraction,sol.value,y=-1.10); self.play(FadeIn(track),run_time=RUN); calc=self.m(rf"P_{{{int(k)}}}={fmt(low)}+{fmt(sol.fraction)}({fmt(high)}-{fmt(low)})={fmt(sol.value)}",43).move_to([0,-2.10,0]); self.play(Write(calc),run_time=RUN_SLOW)
        self.set_step(7)
        if sol.fraction==0: self.play(FadeOut(no_interp),run_time=RUN_FAST)
        result_text=f"{decile_name} = P{int(k)} = {fmt(sol.value)}" if decile_name else f"P{fmt(k)} = {fmt(sol.value)}"
        result=self.note(result_text,7.8,0.64,27).move_to([0,-2.78,0]); self.play(FadeIn(result),run_time=RUN)
        self.set_step(8); interpretation=self.note(f"{fmt(sol.value)} is the value located at the P{fmt(k)} position under our course convention.",12.0,0.70,22).move_to([0,-2.78,0]); self.play(Transform(result,interpretation),run_time=RUN)
        if special_note:
            extra=self.note(special_note,12.4,0.68,21).move_to([0,-2.03,0])
            if track is not None: self.play(FadeOut(calc),FadeOut(track),run_time=RUN_FAST)
            else: self.play(FadeOut(calc),run_time=RUN_FAST)
            self.play(FadeIn(extra),run_time=RUN)
        self.wait(PAUSE_EXPLAIN); self.clear_stage(keep_steps=False); self.step_strip=None

    def error_analysis(self):
        values,k=self.P6; sol=percentile_course(values,k); self.set_header("PROBLEM 6 · ERROR ANALYSIS","Percentile is a position idea, not k% of one data value"); self.set_step(1)
        raw=self.data_row(values,1.62,"RAW"); wrong=self.panel(12.2,1.48,fill=WHITE); w1=self.t("A student writes:",24,BOLD,color=DARK); w2=self.m(r"P_{70}=0.70(45)=31.5",43); wg=VGroup(w1,w2).arrange(DOWN,buff=0.16).move_to(wrong); wrong_group=VGroup(wrong,wg).move_to([0,0.20,0]); q=self.note("What is the conceptual error? Correct the solution using the 8-step method.",12.2,0.82,24).move_to([0,-1.12,0]); self.play(FadeIn(raw),FadeIn(wrong_group),FadeIn(q),run_time=RUN); self.wait(PAUSE_WORK)
        self.play(FadeOut(q),FadeOut(wrong_group),run_time=RUN_FAST); indexed=self.indexed_row(sol.ordered,1.58); self.play(Transform(raw,indexed),run_time=RUN_SLOW)
        self.set_step(2); count=self.m(r"n=9",37).move_to([-2.0,0.48,0]); self.play(Write(count),run_time=RUN_FAST)
        self.set_step(3); choose=self.m(r"k=70",37).move_to([1.65,0.48,0]); self.play(Write(choose),run_time=RUN_FAST)
        self.set_step(4); loc=self.m(r"L=\frac{70}{100}(9+1)=7",42).move_to([0,-0.18,0]); self.play(Write(loc),run_time=RUN); marker=self.locator_marker(indexed,sol.locator,r"L=7"); self.play(FadeIn(marker),run_time=RUN)
        self.set_step(5); self.play(Indicate(indexed[0][6],color=DARK,scale_factor=1.12),run_time=RUN); neigh=self.t("Position 7 contains 36",27,BOLD,color=DARK).move_to([0,-0.90,0]); self.play(FadeIn(neigh),run_time=RUN)
        self.set_step(6); self.play(FadeOut(count),FadeOut(choose),FadeOut(loc),FadeOut(neigh),run_time=RUN_FAST); calc=self.m(r"P_{70}=x_7=36",48).move_to([0,-1.58,0]); self.play(Write(calc),run_time=RUN)
        self.set_step(7); ans=self.note("Correct result: P70 = 36",8.6,0.66,27).move_to([0,-2.34,0]); self.play(FadeIn(ans),run_time=RUN)
        self.set_step(8); misconception=self.note("31.5 came from multiplying a VALUE. Percentiles locate a POSITION in ordered data.",12.4,0.72,23).move_to([0,-3.02,0]); self.play(FadeIn(misconception),run_time=RUN); self.wait(PAUSE_EXPLAIN); self.clear_stage(keep_steps=False); self.step_strip=None

    def final_challenge(self):
        values,k=self.P8; sol=percentile_course(values,k); self.set_header("PROBLEM 8 · FINAL CHALLENGE","Minimal guidance · complete all eight steps yourself"); self.set_step(1)
        raw=self.data_row(values,1.62,"RAW"); task=self.note("Find P55. Your final answer must include L, neighbors, interpolation and interpretation.",12.4,0.82,24).move_to([0,0.42,0]); self.play(FadeIn(raw),FadeIn(task),run_time=RUN); self.wait(PAUSE_WORK+1.5)
        indexed=self.indexed_row(sol.ordered,1.58); self.play(FadeOut(task),Transform(raw,indexed),run_time=RUN_SLOW); self.set_step(2); summary=self.variable_cards(sol).move_to([0,0.30,0]); self.play(FadeIn(summary),run_time=RUN); self.set_step(4); marker=self.locator_marker(indexed,sol.locator,r"L=5.5"); self.play(FadeIn(marker),run_time=RUN); self.set_step(5); self.play(Indicate(indexed[0][4],color=DARK,scale_factor=1.10),Indicate(indexed[0][5],color=DARK,scale_factor=1.10),run_time=RUN); self.set_step(6); self.play(FadeOut(summary),run_time=RUN_FAST); track=self.interpolation_track(59,62,0.5,60.5,y=-0.85); calc=self.m(r"P_{55}=59+0.5(62-59)=60.5",44).move_to([0,-1.82,0]); self.play(FadeIn(track),Write(calc),run_time=RUN_SLOW); self.set_step(7); result=self.note("P55 = 60.5",7.0,0.64,28).move_to([0,-2.68,0]); self.play(FadeIn(result),run_time=RUN); self.set_step(8); self.wait(PAUSE_EXPLAIN); self.clear_stage(keep_steps=False); self.step_strip=None

    def final_summary(self):
        self.set_header("WORKSHOP COMPLETE","What changed from problem to problem?")
        left_items=("Integer L → select one position","Decimal L → interpolate","Decile Dj → percentile P10j","Repeated values stay in the ordered list")
        right_items=("d can be 0.2, 0.5, 0.8…","Negative values do not change the method","Percentile value is not k% of a data value","Always end with an interpretation")
        def build_column(items,title):
            box=self.panel(6.55,4.15,fill=WHITE); tt=self.t(title,27,BOLD,color=DARK).move_to(box).shift(UP*1.62); rows=VGroup()
            for s in items:
                bullet=self.t("•",27,BOLD,color=DARK); tx=self.t(s,23,NORMAL,color=DARK); row=VGroup(bullet,tx).arrange(RIGHT,buff=0.18); self.fit(row,w=5.85,h=0.56); rows.add(row)
            rows.arrange(DOWN,aligned_edge=LEFT,buff=0.42).move_to(box).shift(DOWN*0.18); return VGroup(box,tt,rows)
        pair=VGroup(build_column(left_items,"CALCULATION"),build_column(right_items,"REASONING")).arrange(RIGHT,buff=0.52).move_to([0,0.32,0]); self.play(FadeIn(pair),run_time=RUN_SLOW); close=self.note("Next step: Week 4 uses percentile values to make real interpretations and comparisons.",12.3,0.82,24).move_to([0,-2.78,0]); self.play(FadeIn(close),run_time=RUN); self.wait(PAUSE_SUMMARY)

    def construct(self):
        self.opening(); self.workshop_map()
        self.solve_problem(1,*self.P1,title="P20 · INTEGER LOCATOR",focus="L lands exactly on one ordered position")
        self.solve_problem(2,*self.P2,title="D6 · DECILE TRANSLATION",focus="Translate D6 to P60 before locating",decile_name="D_6")
        self.solve_problem(3,*self.P3,title="P35 · d = 0.2",focus="Decimal locator does not always mean midpoint")
        self.solve_problem(4,*self.P4,title="P72 · d = 0.8",focus="The marker sits much closer to the upper neighbor")
        self.solve_problem(5,*self.P5,title="P45 · REPEATED VALUES",focus="Duplicates remain; interpolation can connect equal values",special_note="Here x4 = x5 = 10, so interpolation still gives 10.")
        self.error_analysis()
        self.solve_problem(7,*self.P7,title="D3 · SIGNED DATA",focus="Negative values change the order, not the algorithm",decile_name="D_3")
        self.final_challenge(); self.final_summary()
