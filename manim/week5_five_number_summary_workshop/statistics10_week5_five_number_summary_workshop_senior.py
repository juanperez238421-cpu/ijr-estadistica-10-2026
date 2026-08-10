from __future__ import annotations

from dataclasses import dataclass
from statistics import median
from typing import Iterable, Sequence

from manim import *

# ============================================================
# Statistics 10 · Week 5 · Five-Number Summary Workshop
# Senior classroom version · ManimCE 0.20.1
# ============================================================
# Visual contract:
# - 16:9 Full HD, white background
# - black/neutral typography, restrained gray hierarchy
# - persistent header + safe stage
# - LaTeX for mathematical notation
# - progressive construction and deliberate pauses
# - same classroom convention used in the Week 5 theory:
#   if n is odd, exclude Q2 from the lower/upper halves
# ============================================================

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

INK = BLACK
DARK = "#252525"
MID = "#5A5A5A"
LIGHT = "#D0D0D0"
PAPER = "#F4F4F4"
SOFT = "#E8E8E8"

SAFE_W = 14.25
Y_TITLE = 3.66
Y_SUBTITLE = 3.15
Y_DATA = 1.95
Y_WORK = 0.20
Y_NOTE = -2.50

RUN_FAST = 0.55
RUN = 0.75
RUN_SLOW = 1.0
PAUSE_SHORT = 0.65
PAUSE_READ = 1.25
PAUSE_TRY = 2.2
PAUSE_EXPLAIN = 1.55

STEP_LABELS = (
    "1 ORDER",
    "2 MIN/MAX",
    "3 FIND Q2",
    "4 SPLIT",
    "5 FIND Q1",
    "6 FIND Q3",
    "7 WRITE 5-NUM",
    "8 INTERPRET",
)


@dataclass(frozen=True)
class QuartileResult:
    ordered: tuple[float, ...]
    lower: tuple[float, ...]
    upper: tuple[float, ...]
    minimum: float
    q1: float
    q2: float
    q3: float
    maximum: float

    @property
    def iqr(self) -> float:
        return self.q3 - self.q1

    @property
    def data_range(self) -> float:
        return self.maximum - self.minimum

    @property
    def five(self) -> tuple[float, float, float, float, float]:
        return (self.minimum, self.q1, self.q2, self.q3, self.maximum)


def quartiles_excluding_median(values: Sequence[float]) -> QuartileResult:
    ordered = tuple(sorted(float(v) for v in values))
    n = len(ordered)
    if n < 4:
        raise ValueError("At least four observations are required.")

    q2 = float(median(ordered))
    if n % 2 == 1:
        m = n // 2
        lower = ordered[:m]
        upper = ordered[m + 1 :]
    else:
        m = n // 2
        lower = ordered[:m]
        upper = ordered[m:]

    return QuartileResult(
        ordered=ordered,
        lower=tuple(lower),
        upper=tuple(upper),
        minimum=ordered[0],
        q1=float(median(lower)),
        q2=q2,
        q3=float(median(upper)),
        maximum=ordered[-1],
    )


def fmt(v: float) -> str:
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:.2f}".rstrip("0").rstrip(".")


class Statistics10Week5FiveNumberSummaryWorkshopSenior(MovingCameraScene):
    """Eight-problem worked workshop for the five-number summary."""

    def setup(self):
        super().setup()
        self.camera.frame.save_state()

        self.r1 = quartiles_excluding_median((18, 7, 12, 5, 20, 9, 11, 16, 8))
        self.r2 = quartiles_excluding_median((13, 2, 18, 7, 24, 11, 16, 5, 21, 9))
        self.r3 = quartiles_excluding_median((3, 3, 4, 4, 7, 7, 9, 9, 12))
        self.r4 = quartiles_excluding_median((2.4, 1.2, 1.6, 2.9, 1.4, 2.1, 2.6, 1.8))
        self.r8 = quartiles_excluding_median((-2, 7, 1, 12, 5, 1, 9, 5, 0, 10, 5))
        self.ra = quartiles_excluding_median((4, 8, 12, 17, 21))
        self.rb = quartiles_excluding_median((3, 7, 12, 18, 22))
        self._validate()

    def _validate(self):
        def close_tuple(actual, expected, tol=1e-9):
            return len(actual) == len(expected) and all(abs(a-b) < tol for a, b in zip(actual, expected))

        assert close_tuple(self.r1.five, (5.0, 7.5, 11.0, 17.0, 20.0))
        assert close_tuple(self.r2.five, (2.0, 7.0, 12.0, 18.0, 24.0))
        assert close_tuple(self.r3.five, (3.0, 4.0, 7.0, 9.0, 12.0))
        assert close_tuple(self.r4.five, (1.2, 1.5, 1.95, 2.5, 2.9))
        assert close_tuple(self.r8.five, (-2.0, 1.0, 5.0, 9.0, 12.0))
        assert close_tuple(self.ra.five, (4.0, 8.0, 12.0, 17.0, 21.0))
        assert close_tuple(self.rb.five, (3.0, 7.0, 12.0, 18.0, 22.0))
        assert abs(self.ra.q2 - 12) < 1e-9 and abs(self.rb.q2 - 12) < 1e-9
        assert abs(self.ra.iqr - 9) < 1e-9 and abs(self.rb.iqr - 11) < 1e-9

    # ------------------------------------------------------------------
    # Core UI helpers
    # ------------------------------------------------------------------
    def t(self, content, size=28, weight=NORMAL, color=INK, **kwargs):
        # Allow callers to override line spacing without passing the keyword twice.
        line_spacing = kwargs.pop("line_spacing", 0.92)
        return Text(content, font_size=size, weight=weight, color=color,
                    line_spacing=line_spacing, **kwargs)

    def m(self, expr, size=40, color=INK, **kwargs):
        return MathTex(expr, font_size=size, color=color, **kwargs)

    def fit(self, mob, w=SAFE_W, h=5.65):
        if mob.width > w:
            mob.scale_to_fit_width(w)
        if mob.height > h:
            mob.scale_to_fit_height(h)
        return mob

    def panel(self, width, height, fill=PAPER, stroke=LIGHT, sw=1.5):
        return RoundedRectangle(width=width, height=height, corner_radius=0.12,
                                stroke_color=stroke, stroke_width=sw,
                                fill_color=fill, fill_opacity=1)

    def note(self, content, width=12.6, height=0.90, size=23):
        box = self.panel(width, height, fill=WHITE, stroke=LIGHT, sw=1.2)
        txt = self.t(content, size, NORMAL, color=MID)
        self.fit(txt, w=width-0.45, h=height-0.20)
        txt.move_to(box)
        return VGroup(box, txt)

    def set_header(self, title, subtitle=None, eyebrow="STATISTICS 10 · WEEK 5"):
        ey = self.t(eyebrow, 20, BOLD, color=MID).to_edge(UP, buff=0.30).align_to(LEFT*6.8, LEFT)
        ti = self.t(title, 34, BOLD, color=INK).move_to([0, Y_TITLE, 0])
        self.fit(ti, w=13.8, h=0.55)
        rule = Line([-7.1, 2.88, 0], [7.1, 2.88, 0], stroke_color=LIGHT, stroke_width=1.5)
        group = VGroup(ey, ti, rule)
        if subtitle:
            st = self.t(subtitle, 20, NORMAL, color=MID).move_to([0, Y_SUBTITLE, 0])
            self.fit(st, w=13.8, h=0.44)
            group.add(st)
        self.add(group)
        self.header = group
        return group

    def clear_stage(self, *keep):
        keep_ids = {id(m) for m in keep}
        mobs = [m for m in self.mobjects if id(m) not in keep_ids]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=RUN_FAST)

    def step_strip(self, active=0):
        cells = VGroup()
        for i, label in enumerate(STEP_LABELS):
            box = RoundedRectangle(width=1.65, height=0.48, corner_radius=0.08,
                                   stroke_color=DARK if i == active else LIGHT,
                                   stroke_width=2 if i == active else 1,
                                   fill_color=PAPER if i == active else WHITE,
                                   fill_opacity=1)
            txt = self.t(label, 13, BOLD if i == active else NORMAL,
                         color=DARK if i == active else MID)
            self.fit(txt, w=1.43, h=0.23)
            txt.move_to(box)
            cells.add(VGroup(box, txt))
        cells.arrange(RIGHT, buff=0.07)
        cells.move_to([0, 2.47, 0])
        return cells

    def update_step(self, strip, active):
        target = self.step_strip(active)
        self.play(Transform(strip, target), run_time=RUN_FAST)

    def make_data_cards(self, values, y=Y_DATA, max_width=13.2, show_indices=True):
        cards = VGroup()
        for i, v in enumerate(values, start=1):
            box = RoundedRectangle(width=0.88, height=0.82, corner_radius=0.08,
                                   stroke_color=DARK, stroke_width=1.4,
                                   fill_color=WHITE, fill_opacity=1)
            val = self.t(fmt(v), 24, BOLD, color=INK)
            val.move_to(box.get_center() + UP*0.06)
            parts = [box, val]
            if show_indices:
                idx = self.t(f"x{i}", 12, NORMAL, color=MID).next_to(box, DOWN, buff=0.06)
                parts.append(idx)
            cards.add(VGroup(*parts))
        cards.arrange(RIGHT, buff=0.12)
        self.fit(cards, w=max_width, h=1.28)
        cards.move_to([0, y, 0])
        return cards

    def quartile_row(self, values, label, width=5.6):
        box = self.panel(width, 1.18, fill=WHITE, stroke=LIGHT, sw=1.2)
        title = self.t(label, 16, BOLD, color=MID).move_to(box.get_top()+DOWN*0.18)
        row = self.make_data_cards(values, y=0, max_width=width-0.45, show_indices=False)
        row.scale(0.74)
        row.move_to(box.get_center()+DOWN*0.09)
        return VGroup(box, title, row)

    def calc_pair(self, symbol, a, b, result):
        tex = rf"{symbol}={fmt(result)}" if abs(a-b) < 1e-9 else rf"{symbol}=\frac{{{fmt(a)}+{fmt(b)}}}{{2}}={fmt(result)}"
        formula = self.m(tex, 38)
        box = self.panel(4.9, 0.88, fill=PAPER, stroke=LIGHT, sw=1.2)
        self.fit(formula, w=4.45, h=0.56)
        formula.move_to(box)
        return VGroup(box, formula)

    def five_number_visual(self, result: QuartileResult, y=-0.25, width=12.0):
        x0, x1 = -width/2, width/2
        lo, hi = result.minimum, result.maximum
        span = max(hi-lo, 1)
        def x(v):
            return x0 + (v-lo)/span*width

        axis = Line([x0, y, 0], [x1, y, 0], stroke_color=DARK, stroke_width=2)
        ticks = VGroup()
        labels = VGroup()
        names = ("min", "Q1", "Q2", "Q3", "max")
        vals = result.five
        for nm, val in zip(names, vals):
            xx = x(val)
            ticks.add(Line([xx,y-0.15,0],[xx,y+0.15,0],stroke_color=DARK,stroke_width=2))
            vl = self.t(fmt(val), 18, BOLD, color=INK).move_to([xx,y-0.42,0])
            nl = self.t(nm, 14, NORMAL, color=MID).move_to([xx,y+0.40,0])
            labels.add(vl,nl)
        return VGroup(axis,ticks,labels)

    # ------------------------------------------------------------------
    # Scene logic
    # ------------------------------------------------------------------
    def opening(self):
        eyebrow = self.t("STATISTICS 10 · WEEK 5", 22, BOLD, color=MID).move_to([0,2.60,0])
        title = self.t("FIVE-NUMBER SUMMARY · WORKSHOP", 42, BOLD, color=INK).move_to([0,1.70,0])
        subtitle = self.t("Different cases · same disciplined 8-step method", 25, NORMAL, color=MID).move_to([0,0.95,0])
        route = self.t("ORDER  →  MIN/MAX  →  Q2  →  SPLIT  →  Q1  →  Q3  →  5-NUM  →  INTERPRET", 21, BOLD, color=DARK).move_to([0,-0.10,0])
        self.fit(route,w=13.3,h=0.48)
        note = self.note("Class convention: when n is odd, exclude Q2 from both halves before finding Q1 and Q3.", 12.8, 0.98, 22).move_to([0,-1.40,0])
        self.play(FadeIn(eyebrow), FadeIn(title), run_time=RUN)
        self.play(FadeIn(subtitle), run_time=RUN_FAST)
        self.play(FadeIn(route), FadeIn(note), run_time=RUN)
        self.wait(PAUSE_READ)
        self.play(FadeOut(VGroup(eyebrow,title,subtitle,route,note)), run_time=RUN_FAST)

    def problem_intro(self, number, title, raw, prompt):
        self.set_header(f"PROBLEM {number} · {title}", "Try first. Then compare your reasoning with the full construction.")
        raw_title = self.t("RAW DATA", 18, BOLD, color=MID).move_to([0,2.25,0])
        raw_cards = self.make_data_cards(raw, y=1.48, max_width=12.5, show_indices=False)
        prompt_box = self.note(prompt, 12.6, 1.08, 23).move_to([0,0.05,0])
        try_text = self.t("YOUR TURN · pause and solve before the construction appears", 20, BOLD, color=DARK).move_to([0,-1.10,0])
        self.play(FadeIn(raw_title), FadeIn(raw_cards), run_time=RUN)
        self.play(FadeIn(prompt_box), FadeIn(try_text), run_time=RUN_FAST)
        self.wait(PAUSE_TRY)
        self.play(FadeOut(VGroup(raw_title,raw_cards,prompt_box,try_text)), run_time=RUN_FAST)
        return self.step_strip(0)

    def solve_problem(self, number, title, raw, result: QuartileResult, interpretation, extra_note=None):
        strip = self.problem_intro(number, title, raw, "Find the five-number summary and explain what it tells you about the data.")
        self.play(FadeIn(strip), run_time=RUN_FAST)

        # Step 1: order
        ordered_title = self.t("ORDERED DATA", 18, BOLD, color=MID).move_to([0,1.98,0])
        ordered = self.make_data_cards(result.ordered, y=1.24, max_width=12.8, show_indices=True)
        self.play(FadeIn(ordered_title), FadeIn(ordered), run_time=RUN)
        self.wait(PAUSE_SHORT)

        # Step 2: min/max
        self.update_step(strip,1)
        extremes = VGroup(
            self.calc_pair(r"\min", result.minimum, result.minimum, result.minimum),
            self.calc_pair(r"\max", result.maximum, result.maximum, result.maximum),
        ).arrange(RIGHT,buff=0.45).move_to([0,-0.18,0])
        self.play(FadeIn(extremes), run_time=RUN)
        self.wait(PAUSE_SHORT)

        # Step 3: Q2
        self.update_step(strip,2)
        n=len(result.ordered)
        if n%2:
            q2_tex=rf"Q_2=x_{{{n//2+1}}}={fmt(result.q2)}"
        else:
            q2_tex=rf"Q_2=\frac{{{fmt(result.ordered[n//2-1])}+{fmt(result.ordered[n//2])}}}{{2}}={fmt(result.q2)}"
        q2 = VGroup(self.panel(5.6,0.92,fill=PAPER,stroke=LIGHT,sw=1.2), self.m(q2_tex,38))
        self.fit(q2[1],w=5.0,h=0.58); q2[1].move_to(q2[0]); q2.move_to([0,-0.18,0])
        self.play(FadeOut(extremes), FadeIn(q2), run_time=RUN)
        self.wait(PAUSE_SHORT)

        # Step 4: split
        self.update_step(strip,3)
        lower = self.quartile_row(result.lower,"LOWER HALF")
        upper = self.quartile_row(result.upper,"UPPER HALF")
        halves = VGroup(lower,upper).arrange(RIGHT,buff=0.35).move_to([0,-0.35,0])
        convention = self.t("Exclude Q2 when n is odd" if n%2 else "Even n: split evenly", 18, BOLD, color=MID).move_to([0,-1.45,0])
        self.play(FadeOut(q2), FadeIn(halves), FadeIn(convention), run_time=RUN)
        self.wait(PAUSE_SHORT)

        # Step 5: Q1
        self.update_step(strip,4)
        l=result.lower; q1=self.calc_pair(r"Q_1",l[(len(l)-1)//2],l[len(l)//2],result.q1).move_to([0,-0.05,0])
        self.play(FadeOut(halves), FadeIn(q1), run_time=RUN)
        self.wait(PAUSE_SHORT)

        # Step 6: Q3
        self.update_step(strip,5)
        u=result.upper; q3=self.calc_pair(r"Q_3",u[(len(u)-1)//2],u[len(u)//2],result.q3).move_to([0,-0.05,0])
        self.play(Transform(q1,q3), run_time=RUN)
        self.wait(PAUSE_SHORT)

        # Step 7: five-number summary
        self.update_step(strip,6)
        five = self.m(rf"\left({fmt(result.minimum)},\ {fmt(result.q1)},\ {fmt(result.q2)},\ {fmt(result.q3)},\ {fmt(result.maximum)}\right)", 42)
        five_box = self.panel(7.2,1.02,fill=PAPER,stroke=DARK,sw=1.8)
        self.fit(five,w=6.65,h=0.62); five.move_to(five_box); five_group=VGroup(five_box,five).move_to([0,-0.10,0])
        self.play(FadeOut(VGroup(q1,convention)), FadeIn(five_group), run_time=RUN)
        self.wait(PAUSE_READ)

        # Step 8: interpretation
        self.update_step(strip,7)
        vis = self.five_number_visual(result,y=-0.15,width=11.5)
        interpretation_box = self.note(interpretation, 12.8, 0.98 if extra_note is None else 0.88, 21).move_to([0,-1.47,0])
        anims=[Transform(five_group,VGroup(self.panel(7.2,0.94,fill=WHITE,stroke=LIGHT,sw=1.2), five.copy()).move_to([0,1.10,0])), FadeIn(vis), FadeIn(interpretation_box)]
        self.play(*anims, run_time=RUN_SLOW)
        if extra_note:
            extra=self.t(extra_note,17,NORMAL,color=MID).move_to([0,-2.15,0])
            self.fit(extra,w=13.0,h=0.42)
            self.play(FadeIn(extra),run_time=RUN_FAST)
            self.wait(PAUSE_EXPLAIN)
            extra_objs=VGroup(extra)
        else:
            self.wait(PAUSE_EXPLAIN)
            extra_objs=VGroup()
        self.play(FadeOut(VGroup(ordered_title,ordered,strip,five_group,vis,interpretation_box,*extra_objs)), run_time=RUN_FAST)
        self.clear_stage()

    def error_analysis(self):
        self.set_header("PROBLEM 5 · ERROR ANALYSIS", "The most common quartile mistake: putting Q2 back into both halves.")
        raw=(4,7,9,11,15,18,22,26,28)
        result=quartiles_excluding_median(raw)
        ordered=self.make_data_cards(result.ordered,y=1.65,max_width=12.4,show_indices=True)
        prompt=self.note("A student says Q1 = 9 and Q3 = 22. Diagnose the error and calculate the correct values.",12.6,1.0,22).move_to([0,0.45,0])
        self.play(FadeIn(ordered),FadeIn(prompt),run_time=RUN)
        self.wait(PAUSE_TRY)
        bad=self.note("INCORRECT: including the median 15 in both halves changes the medians of those halves.",12.7,0.92,21).move_to([0,-0.72,0])
        self.play(FadeOut(prompt),FadeIn(bad),run_time=RUN)
        correct = VGroup(
            self.quartile_row((4,7,9,11),"CORRECT LOWER HALF",5.8),
            self.quartile_row((18,22,26,28),"CORRECT UPPER HALF",5.8),
        ).arrange(RIGHT,buff=0.35).move_to([0,0.25,0])
        self.play(FadeOut(bad),Transform(ordered,correct),run_time=RUN_SLOW)
        q1=self.m(r"Q_1=\frac{7+9}{2}=8",36)
        q3=self.m(r"Q_3=\frac{22+26}{2}=24",36)
        calcs=VGroup(q1,q3).arrange(RIGHT,buff=1.0).move_to([0,-1.20,0])
        five=self.m(r"(\min,Q_1,Q_2,Q_3,\max)=(4,8,15,24,28)",34).move_to([0,-2.00,0])
        self.play(FadeIn(calcs),FadeIn(five),run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def compare_spread(self):
        self.set_header("PROBLEM 6 · SAME MEDIAN, DIFFERENT SPREAD", "Center can be identical while variability is different.")
        prompt=self.note("Dataset A and Dataset B both have median 12. Which distribution is more spread out? Justify with IQR and range.",12.8,1.02,22).move_to([0,1.45,0])
        self.play(FadeIn(prompt),run_time=RUN)
        self.wait(PAUSE_TRY)

        card_a = self.panel(6.35, 2.25, fill=WHITE, stroke=DARK, sw=1.5).move_to([-3.35,0.35,0])
        card_b = self.panel(6.35, 2.25, fill=WHITE, stroke=DARK, sw=1.5).move_to([3.35,0.35,0])
        ta = VGroup(
            self.t("DATASET A", 23, BOLD, color=DARK),
            self.m(r"(4,8,12,17,21)", 34),
            self.t("IQR = 17 - 8 = 9", 22, NORMAL, color=MID),
            self.t("Range = 21 - 4 = 17", 22, NORMAL, color=MID),
        ).arrange(DOWN, buff=0.16); self.fit(ta,w=5.8,h=1.78); ta.move_to(card_a)
        tb = VGroup(
            self.t("DATASET B", 23, BOLD, color=DARK),
            self.m(r"(3,7,12,18,22)", 34),
            self.t("IQR = 18 - 7 = 11", 22, NORMAL, color=MID),
            self.t("Range = 22 - 3 = 19", 22, NORMAL, color=MID),
        ).arrange(DOWN, buff=0.16); self.fit(tb,w=5.8,h=1.78); tb.move_to(card_b)
        self.play(FadeOut(prompt), FadeIn(VGroup(card_a,ta)), FadeIn(VGroup(card_b,tb)), run_time=RUN_SLOW)
        conclusion = self.note("Dataset B is more spread out: it has the larger IQR (11) and the larger range (19).", 12.5, 0.92, 23).move_to([0,-1.85,0])
        self.play(FadeIn(conclusion), run_time=RUN)
        rule = self.t("Median describes center; IQR and range describe spread.", 22, BOLD, color=DARK).move_to([0,-2.65,0])
        self.play(FadeIn(rule), run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def reverse_reasoning(self):
        self.set_header("PROBLEM 7 · REVERSE REASONING", "Use the five-number summary to recover a missing observation.")
        summary=self.m(r"(\min,Q_1,Q_2,Q_3,\max)=(4,8,15,22.5,28)",36).move_to([0,1.75,0])
        data=self.t("Ordered data: 4, 6, 8, 10, x, 18, 21, 24, 28",28,BOLD,color=DARK).move_to([0,0.75,0])
        prompt=self.note("There are 9 observations. Find x and explain which landmark in the five-number summary determines it.",12.7,1.0,22).move_to([0,-0.35,0])
        self.play(FadeIn(summary),FadeIn(data),FadeIn(prompt),run_time=RUN)
        self.wait(PAUSE_TRY)
        answer=self.m(r"Q_2=x_5=15\quad\Rightarrow\quad x=15",42).move_to([0,-1.45,0])
        note=self.note("Because n = 9, the 5th ordered observation is the median. The supplied summary says Q2 = 15.",12.8,0.90,21).move_to([0,-2.35,0])
        self.play(FadeOut(prompt),FadeIn(answer),FadeIn(note),run_time=RUN)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    def closing(self):
        self.set_header("WORKSHOP COMPLETE", "One method. Many cases. Every answer must be constructed and interpreted.")
        rows = VGroup(
            self.t("1  ORDER the observations",22,BOLD,color=DARK),
            self.t("2  IDENTIFY min and max",22,NORMAL,color=MID),
            self.t("3  FIND Q2",22,NORMAL,color=MID),
            self.t("4  SPLIT correctly",22,NORMAL,color=MID),
            self.t("5  FIND Q1",22,NORMAL,color=MID),
            self.t("6  FIND Q3",22,NORMAL,color=MID),
            self.t("7  WRITE (min, Q1, Q2, Q3, max)",22,NORMAL,color=MID),
            self.t("8  INTERPRET center and spread",22,NORMAL,color=MID),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.18).move_to([-3.6,-0.15,0])
        preview_box = self.panel(6.1,3.65,fill=WHITE,stroke=DARK,sw=1.5).move_to([3.55,-0.10,0])
        five = self.m(r"\min\;|\;Q_1\;|\;Q_2\;|\;Q_3\;|\;\max",37).move_to([3.55,1.20,0])
        arrow = Arrow([3.55,0.35,0],[3.55,-0.35,0],color=DARK,stroke_width=3,max_tip_length_to_length_ratio=0.18)
        next_text = self.t("Week 6: turn these five landmarks\ninto the geometry of a box plot.", 24, BOLD, color=DARK, line_spacing=0.9)
        self.fit(next_text,w=5.3,h=1.10); next_text.move_to([3.55,-1.05,0])
        self.play(LaggedStart(*[FadeIn(r) for r in rows],lag_ratio=0.10), FadeIn(preview_box), run_time=RUN_SLOW)
        self.play(FadeIn(five), GrowArrow(arrow), FadeIn(next_text), run_time=RUN)
        self.wait(PAUSE_READ)

    def construct(self):
        self.opening()
        self.solve_problem(1, "ODD n · DECIMAL QUARTILES", (18,7,12,5,20,9,11,16,8), self.r1,
                           "The middle 50% lies from Q1 = 7.5 to Q3 = 17; its width is IQR = 9.5.",
                           "For odd n, Q2 = 11 is excluded before finding Q1 and Q3.")
        self.solve_problem(2, "EVEN n · MEDIAN IS AN AVERAGE", (13,2,18,7,24,11,16,5,21,9), self.r2,
                           "The center is Q2 = 12. The middle half runs from 7 to 18, so IQR = 11.")
        self.solve_problem(3, "REPEATED VALUES", (3,3,4,4,7,7,9,9,12), self.r3,
                           "Repeated observations stay in the ordered list. The summary is (3, 4, 7, 9, 12).")
        self.solve_problem(4, "DECIMAL MEASUREMENTS", (2.4,1.2,1.6,2.9,1.4,2.1,2.6,1.8), self.r4,
                           "Q2 = 1.95 and the central 50% runs from 1.5 to 2.5; therefore IQR = 1.0.")
        self.error_analysis()
        self.compare_spread()
        self.reverse_reasoning()
        self.solve_problem(8, "FINAL CHALLENGE · NEGATIVES + REPEATED VALUES", (-2,7,1,12,5,1,9,5,0,10,5), self.r8,
                           "The summary is (-2, 1, 5, 9, 12). The middle 50% spans 8 units, from 1 to 9.",
                           "Negative values and repeated values do not change the method: order first, then construct.")
        self.closing()
