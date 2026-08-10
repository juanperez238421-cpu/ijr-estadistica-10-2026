#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statistics 10 · Period 1 · Week 1 — IQR diagram recovery.

Self-contained render source. Its visual constants, safe-layout rules, persistent
header architecture, pacing, and monochrome classroom system are adapted from
`jp_classroom_style.py` supplied for this lesson.

Scope: recovery only. The 1.5·IQR outlier rule is intentionally deferred to the
later outlier lesson; today the basic whiskers use observed min and max.
"""
from __future__ import annotations

from statistics import median
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
SAFE_W = 14.6
RUN_Q = 0.75
RUN_N = 1.00
RUN_S = 1.35
P_SHORT = 0.9
P_READ = 1.8
P_EXPLAIN = 2.8
P_WORK = 3.8
P_FINAL = 5.0

RAW = (9, 3, 7, 5, 11, 6, 4, 10, 8)
DATA = tuple(sorted(RAW))
LOW = DATA[:4]
HIGH = DATA[5:]
Q2 = float(median(DATA))
Q1 = float(median(LOW))
Q3 = float(median(HIGH))
IQR = Q3 - Q1
MINV, MAXV = float(min(DATA)), float(max(DATA))

assert DATA == (3,4,5,6,7,8,9,10,11)
assert (Q1,Q2,Q3,IQR,MINV,MAXV) == (4.5,7.0,9.5,5.0,3.0,11.0)


def f(v: float) -> str:
    return str(int(v)) if float(v).is_integer() else f"{v:.1f}"


class Statistics10Period1Week1IQRRecovery(MovingCameraScene):
    def setup(self):
        super().setup()
        self.camera.background_color = WHITE
        self.camera.frame.set(width=16).move_to(ORIGIN)
        self.header = None
        self.subtitle = None

    def text(self, s, size=30, weight=NORMAL):
        return Text(s, font_size=size, color=INK, weight=weight, line_spacing=0.92)

    def math(self, s, size=38):
        return MathTex(s, font_size=size, color=INK)

    def fit(self, mob, w=SAFE_W, h=7.4):
        if mob.width > w: mob.scale_to_fit_width(w)
        if mob.height > h: mob.scale_to_fit_height(h)
        return mob

    def set_header(self, n, title, subtitle):
        badge = RoundedRectangle(width=.72,height=.52,corner_radius=.1,stroke_color=INK,stroke_width=2,fill_color=WHITE,fill_opacity=1)
        num = self.text(f"{n:02d}",23,BOLD).move_to(badge)
        ttl = self.text(title,33,BOLD)
        self.fit(ttl,13.4,.6)
        row = VGroup(VGroup(badge,num),ttl).arrange(RIGHT,buff=.25).to_edge(UP,buff=.16).to_edge(LEFT,buff=.48)
        rule = Line(LEFT*7.48,RIGHT*7.48,color=LIGHT,stroke_width=2).next_to(row,DOWN,buff=.07)
        sub = self.text(subtitle,20)
        self.fit(sub,14.2,.7)
        sub.next_to(rule,DOWN,buff=.08).align_to(row,LEFT)
        newh = VGroup(row,rule)
        if self.header is None:
            self.add(newh,sub)
        else:
            self.play(FadeOut(self.header),FadeOut(self.subtitle),run_time=RUN_Q)
            self.play(FadeIn(newh),FadeIn(sub),run_time=RUN_Q)
        self.header,self.subtitle = newh,sub

    def clear(self):
        keep=set()
        for x in (self.header,self.subtitle):
            if x: keep.update(id(m) for m in x.get_family())
        rem=[m for m in self.mobjects if id(m) not in keep]
        if rem: self.play(*[FadeOut(m) for m in rem],run_time=RUN_N)
        self.camera.frame.set(width=16).move_to(ORIGIN)

    def formula(self, tex, width=8.0, fs=40):
        box=RoundedRectangle(width=width,height=1.12,corner_radius=.12,stroke_color=INK,stroke_width=2,fill_color=PAPER,fill_opacity=1)
        eq=self.math(tex,fs); self.fit(eq,width-.55,.82); eq.move_to(box)
        return VGroup(box,eq)

    def note(self,title,lines,width=6.2):
        head=self.text(title,25,BOLD)
        body=VGroup(*[self.text(x,22) for x in lines]).arrange(DOWN,aligned_edge=LEFT,buff=.14)
        content=VGroup(head,body).arrange(DOWN,aligned_edge=LEFT,buff=.2)
        self.fit(content,width-.6,2.7)
        box=RoundedRectangle(width=width,height=max(1.2,content.height+.62),corner_radius=.12,stroke_color=INK,stroke_width=1.8,fill_color=WHITE,fill_opacity=1)
        content.move_to(box).align_to(box,LEFT).shift(RIGHT*.3)
        return VGroup(box,content)

    def chip(self,v,fill=WHITE,width=.9):
        b=RoundedRectangle(width=width,height=.66,corner_radius=.1,stroke_color=INK,stroke_width=1.7,fill_color=fill,fill_opacity=1)
        t=self.text(str(v),26,BOLD).move_to(b)
        return VGroup(b,t)

    def chips(self,vals,fill=WHITE):
        g=VGroup(*[self.chip(v,fill) for v in vals]).arrange(RIGHT,buff=.13)
        self.fit(g,13.8,.76); return g

    def axis(self,y=-.6):
        mn,mx=2,12; width=12.5; left=-width/2
        def xp(v): return left+(v-mn)/(mx-mn)*width
        base=Line([left,y,0],[left+width,y,0],color=INK,stroke_width=2.4)
        ticks=VGroup(); labels=VGroup()
        for v in range(mn,mx+1):
            x=xp(v); ticks.add(Line([x,y-.13,0],[x,y+.13,0],color=INK,stroke_width=1.7)); labels.add(self.text(str(v),19).move_to([x,y-.42,0]))
        return VGroup(base,ticks,labels),xp

    def construct(self):
        self.opening(); self.recovery(); self.ordering(); self.quartiles(); self.iqr_summary(); self.graph(); self.interpret()

    def opening(self):
        a=self.text("STATISTICS 10 · PERIOD 1 · WEEK 1",28,BOLD)
        b=self.text("IQR DIAGRAM RECOVERY",50,BOLD)
        r=Line(LEFT*5.5,RIGHT*5.5,color=INK,stroke_width=2.2)
        c=self.text("Median · Quartiles · Interquartile Range · Box-and-Whisker Plot",27)
        d=self.text("Order first. Use positions. Build the graph last.",25,MEDIUM)
        g=VGroup(a,b,r,c,d).arrange(DOWN,buff=.3); self.fit(g,14.4,6.5)
        self.play(FadeIn(a,shift=UP*.15),run_time=RUN_N); self.play(Write(b),run_time=RUN_S); self.play(Create(r),FadeIn(c),run_time=RUN_N); self.wait(P_EXPLAIN); self.play(FadeIn(d),run_time=RUN_N); self.wait(P_FINAL); self.play(FadeOut(g),run_time=RUN_N)

    def recovery(self):
        self.set_header(1,"RECOVERY CHECK + HUMAN NUMBER LINE","Recover the meaning of median, quartiles, and IQR before touching the final graph.")
        cards=VGroup(
            self.note("MEDIAN / Q2",["Center of the ordered observations.","For n=9, use position 5."],4.25),
            self.note("QUARTILES",["Q1, Q2, Q3 divide ordered data","into four positional regions."],4.25),
            self.note("IQR",["IQR = Q3 - Q1","Width of the middle 50%."],4.25),
        ).arrange(RIGHT,buff=.28).move_to(UP*.85)
        self.play(LaggedStart(*[FadeIn(c,shift=UP*.08) for c in cards],lag_ratio=.15),run_time=RUN_S*1.6); self.wait(P_WORK)
        self.play(FadeOut(cards),run_time=RUN_N)
        ax,xp=self.axis(y=-.55); self.play(Create(ax),run_time=RUN_N)
        people=VGroup()
        for v in DATA:
            dot=Circle(radius=.15,stroke_color=INK,stroke_width=2,fill_color=WHITE,fill_opacity=1).move_to([xp(v),.45,0])
            tag=self.text(str(v),18,BOLD).next_to(dot,UP,buff=.05); people.add(VGroup(dot,tag))
        self.play(LaggedStart(*[FadeIn(p,shift=UP*.08) for p in people],lag_ratio=.09),run_time=RUN_S)
        med=Line([xp(7),-.1,0],[xp(7),1.3,0],color=INK,stroke_width=5); lab=self.text("Q2 = 7",23,BOLD).next_to(med,UP,buff=.05)
        self.play(Create(med),FadeIn(lab),run_time=RUN_N); self.wait(P_EXPLAIN)
        low=BraceBetweenPoints([xp(3),1.45,0],[xp(6),1.45,0],direction=UP,color=INK); high=BraceBetweenPoints([xp(8),1.45,0],[xp(11),1.45,0],direction=UP,color=INK)
        self.play(Create(low),Create(high),FadeIn(self.text("lower half",19,BOLD).next_to(low,UP,buff=.04)),FadeIn(self.text("upper half",19,BOLD).next_to(high,UP,buff=.04)),run_time=RUN_N); self.wait(P_WORK); self.clear()

    def ordering(self):
        self.set_header(2,"STEP 1 — ORDER THE DATA","Quartiles are positional statistics, so an unordered list cannot be used directly.")
        raw=VGroup(self.text("RAW DATA",24,BOLD),self.chips(RAW)).arrange(DOWN,buff=.22).move_to(UP*1.35)
        arr=Arrow(UP*.35,DOWN*.35,color=INK,stroke_width=2.5); lab=self.text("smallest → largest",21,BOLD).next_to(arr,RIGHT,buff=.2)
        ordered=VGroup(self.text("ORDERED DATA",24,BOLD),self.chips(DATA,PAPER)).arrange(DOWN,buff=.22).move_to(DOWN*.75)
        self.play(FadeIn(raw),run_time=RUN_N); self.wait(P_READ); self.play(GrowArrow(arr),FadeIn(lab),run_time=RUN_N); self.play(FadeIn(ordered),run_time=RUN_S); self.wait(P_EXPLAIN)
        check=self.formula(r"n=9\Rightarrow Q_2=x_{(5)}=7",6.5,40).to_edge(DOWN,buff=.22); self.play(FadeIn(check),run_time=RUN_N); self.wait(P_WORK); self.clear()

    def quartiles(self):
        self.set_header(3,"STEPS 2–3 — FIND Q2, THEN Q1 AND Q3","For odd n, exclude Q2 from the two halves; then take the median of each half.")
        row=self.chips(DATA); row[4][0].set_fill(PAPER,opacity=1); row.move_to(UP*1.75)
        pos=VGroup(*[self.text(str(i+1),16).next_to(row[i],UP,buff=.05) for i in range(9)])
        self.play(FadeIn(row),FadeIn(pos),run_time=RUN_N); self.wait(P_READ)
        q2=self.formula(r"Q_2=x_{(5)}=7",4.7,40).move_to(UP*.55); self.play(FadeIn(q2),run_time=RUN_N); self.wait(P_EXPLAIN)
        left=VGroup(self.text("LOWER HALF",23,BOLD),self.chips(LOW,PAPER),self.formula(r"Q_1=\frac{4+5}{2}=4.5",5.8,36)).arrange(DOWN,buff=.2)
        right=VGroup(self.text("UPPER HALF",23,BOLD),self.chips(HIGH,PAPER),self.formula(r"Q_3=\frac{9+10}{2}=9.5",5.8,36)).arrange(DOWN,buff=.2)
        halves=VGroup(left,right).arrange(RIGHT,buff=.55).move_to(DOWN*1.15)
        self.play(LaggedStart(FadeIn(left),FadeIn(right),lag_ratio=.2),run_time=RUN_S); self.wait(P_WORK); self.clear()

    def iqr_summary(self):
        self.set_header(4,"STEPS 4–5 — CALCULATE IQR + FIVE-NUMBER SUMMARY","IQR measures only the middle half; the graph itself is located by five reference values.")
        eq=self.formula(r"IQR=Q_3-Q_1=9.5-4.5=5",9.0,42).move_to(UP*1.55)
        meaning=self.text("The middle 50% spans 5 units.",25,BOLD).next_to(eq,DOWN,buff=.23)
        self.play(FadeIn(eq),run_time=RUN_S); self.play(FadeIn(meaning),run_time=RUN_N); self.wait(P_EXPLAIN)
        labels=["MIN","Q1","Q2","Q3","MAX"]; vals=[MINV,Q1,Q2,Q3,MAXV]; cards=VGroup()
        for l,v in zip(labels,vals):
            b=RoundedRectangle(width=2.35,height=1.75,corner_radius=.12,stroke_color=INK,stroke_width=1.8,fill_color=WHITE,fill_opacity=1)
            c=VGroup(self.text(l,21,BOLD),self.text(f(v),34,BOLD)).arrange(DOWN,buff=.22).move_to(b); cards.add(VGroup(b,c))
        cards.arrange(RIGHT,buff=.25).move_to(DOWN*.65); self.play(LaggedStart(*[FadeIn(c,shift=UP*.06) for c in cards],lag_ratio=.12),run_time=RUN_S*1.5); self.wait(P_EXPLAIN)
        note=self.text("Today: whiskers use min and max. The formal 1.5·IQR outlier rule is a later lesson.",20,BOLD).to_edge(DOWN,buff=.25); self.play(FadeIn(note),run_time=RUN_N); self.wait(P_WORK); self.clear()

    def graph(self):
        self.set_header(5,"STEP 6 — CONSTRUCT THE BOX-AND-WHISKER DIAGRAM","Use one common scale: mark the five numbers, build the box Q1→Q3, add Q2, then add whiskers.")
        ax,xp=self.axis(y=-1.55); self.play(Create(ax),run_time=RUN_N)
        marks=[MINV,Q1,Q2,Q3,MAXV]; names=["MIN","Q1","Q2","Q3","MAX"]
        guides=VGroup(*[Dot([xp(v),-1.55,0],radius=.085,color=INK) for v in marks]); tags=VGroup(*[VGroup(self.text(n,17,BOLD),self.text(f(v),17,BOLD)).arrange(DOWN,buff=.01).move_to([xp(v),-2.5,0]) for n,v in zip(names,marks)])
        self.play(LaggedStart(*[FadeIn(d) for d in guides],lag_ratio=.1),run_time=RUN_N); self.play(LaggedStart(*[FadeIn(t) for t in tags],lag_ratio=.08),run_time=RUN_N); self.wait(P_EXPLAIN)
        y=.15; h=1.45; x0,x1,x2,x3,x4=[xp(v) for v in marks]
        box=Rectangle(width=x3-x1,height=h,stroke_color=INK,stroke_width=4,fill_color=PAPER,fill_opacity=1).move_to([(x1+x3)/2,y,0]); med=Line([x2,y-h/2,0],[x2,y+h/2,0],color=INK,stroke_width=5)
        lw=Line([x0,y,0],[x1,y,0],color=INK,stroke_width=4); rw=Line([x3,y,0],[x4,y,0],color=INK,stroke_width=4); lc=Line([x0,y-.45,0],[x0,y+.45,0],color=INK,stroke_width=4); rc=Line([x4,y-.45,0],[x4,y+.45,0],color=INK,stroke_width=4)
        cap1=self.text("1. BOX = Q1 to Q3",22,BOLD).move_to(UP*1.55); self.play(Create(box),FadeIn(cap1),run_time=RUN_S); self.wait(P_EXPLAIN)
        cap2=self.text("2. MEDIAN = Q2",22,BOLD).move_to(UP*2.0); self.play(Create(med),FadeIn(cap2),run_time=RUN_N); self.wait(P_EXPLAIN)
        cap3=self.text("3. WHISKERS = min↔Q1 and Q3↔max",22,BOLD).move_to(UP*2.45); self.play(Create(lw),Create(rw),Create(lc),Create(rc),FadeIn(cap3),run_time=RUN_S); self.wait(P_WORK); self.clear()

    def interpret(self):
        self.set_header(6,"READ IT, THEN REPEAT THE RECIPE","The box is the central 50%; the final objective is a reproducible construction method, not a memorized picture.")
        ax,xp=self.axis(y=-.45); y=.95; h=1.25; x0,x1,x2,x3,x4=[xp(v) for v in [MINV,Q1,Q2,Q3,MAXV]]
        graph=VGroup(ax,Rectangle(width=x3-x1,height=h,stroke_color=INK,stroke_width=4,fill_color=PAPER,fill_opacity=1).move_to([(x1+x3)/2,y,0]),Line([x2,y-h/2,0],[x2,y+h/2,0],color=INK,stroke_width=5),Line([x0,y,0],[x1,y,0],color=INK,stroke_width=4),Line([x3,y,0],[x4,y,0],color=INK,stroke_width=4),Line([x0,y-.4,0],[x0,y+.4,0],color=INK,stroke_width=4),Line([x4,y-.4,0],[x4,y+.4,0],color=INK,stroke_width=4))
        self.play(FadeIn(graph),run_time=RUN_S); self.wait(P_EXPLAIN)
        brace=Brace(graph[1],UP,color=INK); ilab=self.math(r"IQR=5\quad\text{(middle 50\%)}",30).next_to(brace,UP,buff=.08); self.play(Create(brace),FadeIn(ilab),run_time=RUN_N)
        route=VGroup(*[self.note(str(i),[s],3.25) for i,s in enumerate(["ORDER DATA","FIND Q2","SPLIT HALVES","FIND Q1 & Q3","COMPUTE IQR","FIVE NUMBERS","DRAW BOX","ADD WHISKERS"],1)]).arrange_in_grid(rows=2,cols=4,buff=(.18,.18)); route.scale(.72).to_edge(DOWN,buff=.22)
        self.play(LaggedStart(*[FadeIn(c,shift=UP*.05) for c in route],lag_ratio=.07),run_time=RUN_S*1.7); self.wait(P_FINAL)
        closing=self.text("Order → positions → quartiles → IQR → graph → interpretation.",34,BOLD); self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=RUN_N); self.play(FadeIn(closing),run_time=RUN_S); self.wait(P_FINAL); self.play(FadeOut(closing),run_time=RUN_N)
