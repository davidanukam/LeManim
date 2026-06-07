"""
Two Sum - Manim explainer
Render: manim -pqm main.py TwoSum
"""

from manim import *

# - Color Palette - #
BG = "#141414"
ACCENT = "#3B82F6"
ACCENT_DARK = "#2563EB"
ACCENT_FILL = "#1E3A5F"
ACCENT_LIGHT = "#93C5FD"
SLOW_RED = "#f83645"
BOX_FILL = "#1E1E1E"
BOX_FILL_ALT = "#232323"
BOX_STROKE = "#444444"
LABEL_GRAY = "#888888"
WHITE = "#FFFFFF"
SUCCESS = "#22C55E"

# - Constants - #
MONO = "monospace"
ARIAL = "arial"

ARRAY = [2, 1, 5, 3]
TARGET = 4

import sys

ADD_SOUND = "--sound" in sys.argv


class TwoSum(Scene):
    def setup(self):
        self.camera.background_color = BG

    def construct(self):
        if ADD_SOUND:
            self.add_sound("audio/TwoSum_1Min.wav")
        self.scene_01_problem_hook()
        self.scene_02_narrator_simple()
        self.scene_03_answer_reveal()
        self.scene_04_naive_vs_clever()
        # self.scene_05_brute_force_intro()
        # self.scene_06_brute_force_checks()
        # self.scene_07_scan_pattern()
        # self.scene_08_time_complexity()
        # self.scene_09_scale_problem()
        # self.scene_10_narrator_reframe()
        # self.scene_11_partner_concept()
        # self.scene_12_reframed_problem()
        # self.scene_13_hashmap_metaphor()
        # self.scene_14_build_as_you_go()
        # self.scene_15_hashmap_walkthrough()
        # self.scene_16_solution_found()
        # self.scene_17_one_pass_proof()
        # self.scene_18_complexity_comparison()
        # self.scene_19_space_complexity()
        # self.scene_20_outro()

    # - Helper Methods - #

    def spaced_caps(self, text, size=20, color=LABEL_GRAY, weight=NORMAL):
        """Render text with spaced-caps effect."""
        spaced = " ".join(list(text.upper()))
        return Text(
            spaced,
            font_size=size,
            color=color,
            font="Monospace",
            weight=weight,
        )

    def make_label_box(
        self,
        label_text,
        main_text,
        stroke_color=BOX_STROKE,
        fill_color=BOX_FILL,
        label_color=LABEL_GRAY,
        width=4,
        height=2,
    ):
        """Box with small spaced-caps label and large main text."""
        box = RoundedRectangle(
            corner_radius=0.15,
            width=width,
            height=height,
            stroke_color=stroke_color,
            stroke_width=1.5,
            fill_color=fill_color,
            fill_opacity=1,
        )
        label = self.spaced_caps(label_text, size=14, color=label_color)
        main = Text(main_text, font_size=36, color=WHITE, weight=BOLD)
        content = VGroup(label, main).arrange(DOWN, buff=0.25)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def make_numbered_row(self, number, label_text, active=False, width=8, height=0.9):
        """Horizontal numbered row like '01   PARSE SQL'."""
        num_color = ACCENT if active else LABEL_GRAY
        fill_color = ACCENT_FILL if active else BOX_FILL
        stroke_col = ACCENT if active else BOX_STROKE
        box = RoundedRectangle(
            corner_radius=0.12,
            width=width,
            height=height,
            stroke_color=stroke_col,
            stroke_width=1.5,
            fill_color=fill_color,
            fill_opacity=1,
        )
        num_text = Text(number, font_size=20, color=num_color, font="Monospace")
        lbl_text = Text(label_text, font_size=24, color=WHITE, weight=BOLD)
        num_text.move_to(box.get_left() + RIGHT * 0.7)
        lbl_text.move_to(box.get_center() + RIGHT * 0.3)
        return VGroup(box, num_text, lbl_text)

    def make_array_cell(self, value, index=None, active=False, partner=False):
        """Single array element box with optional index label."""
        stroke = ACCENT if active else SUCCESS if partner else BOX_STROKE
        fill = ACCENT_FILL if active else "#1A3D2E" if partner else BOX_FILL
        box = RoundedRectangle(
            corner_radius=0.12,
            width=1.1,
            height=1.1,
            stroke_color=stroke,
            stroke_width=2 if active or partner else 1.5,
            fill_color=fill,
            fill_opacity=1,
        )
        val = Text(str(value), font_size=32, color=WHITE, weight=BOLD)
        val.move_to(box.get_center())
        grp = VGroup(box, val)
        if index is not None:
            idx_lbl = Text(
                f"[{index}]",
                font_size=14,
                color=LABEL_GRAY,
                font="Monospace",
            )
            idx_lbl.next_to(box, DOWN, buff=0.15)
            grp.add(idx_lbl)
        return grp

    def make_array_row(self, values=None, highlight_indices=None, partner_indices=None):
        """Horizontal row of array cells."""
        values = values or ARRAY
        highlight_indices = highlight_indices or []
        partner_indices = partner_indices or []
        cells = VGroup(
            *[
                self.make_array_cell(
                    v,
                    i,
                    active=i in highlight_indices,
                    partner=i in partner_indices,
                )
                for i, v in enumerate(values)
            ]
        )
        cells.arrange(RIGHT, buff=0.35)
        return cells

    def clear_scene(self, run_time=0.8):
        """Fade out everything on screen."""
        if self.mobjects:
            self.play(FadeOut(Group(*self.mobjects)), run_time=run_time)
        self.wait(0.3)

    def hold(self, seconds=2.0):
        """Pause on a finished composition before transitioning."""
        self.wait(seconds)

    def gap(self, seconds=10):
        """Black-screen pause between scenes (narrator pacing)."""
        self.wait(seconds)

    # - SCENE 1 - Problem Hook

    def scene_01_problem_hook(self):
        header = self.spaced_caps("TWO SUM", size=28, color=WHITE)
        header.to_edge(UP, buff=0.9)

        array_label = self.spaced_caps("ARRAY", size=14, color=LABEL_GRAY)
        array_row = self.make_array_row()
        array_grp = VGroup(array_label, array_row).arrange(DOWN, buff=0.4)

        target_box = self.make_label_box(
            "TARGET",
            str(TARGET),
            stroke_color=ACCENT,
            fill_color=ACCENT_FILL,
            label_color=ACCENT_LIGHT,
            width=3,
            height=1.6,
        )

        content = VGroup(array_grp, target_box).arrange(DOWN, buff=0.5)
        content.next_to(header, DOWN, buff=0.7)

        question = Text(
            "Find two that add up to the target",
            font_size=28,
            color=LABEL_GRAY,
        )
        question.next_to(content, DOWN, buff=0.75)

        self.play(Write(header), run_time=1.2)
        self.play(FadeIn(array_label), FadeIn(array_row), run_time=1.5)
        self.play(FadeIn(target_box), run_time=1.0)
        self.play(Write(question), run_time=2.0)
        self.hold(2.0)
        self.clear_scene()

    # - SCENE 2 - Narrator: Sounds Simple

    def scene_02_narrator_simple(self):
        text = Text(
            "sounds almost insultingly simple",
            font_size=38,
            color=WHITE,
        )
        text.to_corner(DL, buff=1.2)
        self.play(AddTextLetterByLetter(text), run_time=3.0)
        self.hold(2.0)
        self.clear_scene()

    # - SCENE 3 - Answer Reveal: 1 + 3

    def scene_03_answer_reveal(self):
        self.gap(8)

        array_row = self.make_array_row(partner_indices=[1, 3])
        array_row.shift(UP * 0.8)

        eq = Text("1  +  3  =  4", font_size=48, color=WHITE, weight=BOLD)
        eq.next_to(array_row, DOWN, buff=1.0)

        check = Text("✓", font_size=56, color=SUCCESS)
        check.next_to(eq, RIGHT, buff=0.5)

        self.play(FadeIn(array_row), run_time=1.0)
        self.play(Write(eq), run_time=1.5)
        self.play(FadeIn(check, scale=0.5), run_time=0.8)
        self.hold(2.0)
        self.clear_scene()

    # - SCENE 4 - Naive vs Clever

    def scene_04_naive_vs_clever(self):
        self.gap(10)

        naive = self.make_label_box(
            "NAIVE",
            "chokes",
            stroke_color=SLOW_RED,
            fill_color="#3D1A1A",
            label_color=SLOW_RED,
            width=3.5,
            height=2,
        )
        clever = self.make_label_box(
            "CLEVER",
            "breezes",
            stroke_color=ACCENT,
            fill_color=ACCENT_FILL,
            label_color=ACCENT_LIGHT,
            width=3.5,
            height=2,
        )
        group = VGroup(naive, clever).arrange(RIGHT, buff=2.5)
        group.move_to(ORIGIN)

        scale = self.spaced_caps("1 MILLION NUMBERS", size=16, color=LABEL_GRAY)
        scale.next_to(group, DOWN, buff=0.8)

        self.play(FadeIn(naive), run_time=1.0)
        self.play(FadeIn(clever), run_time=1.0)
        self.play(Write(scale), run_time=1.5)
        self.hold(2.0)
        self.clear_scene()

    # - SCENE 5 - Brute Force Intro

    def scene_05_brute_force_intro(self):
        self.gap(10)

        header = self.spaced_caps("BRUTE FORCE", size=22, color=SLOW_RED)
        header.to_edge(UP, buff=0.8)

        subtitle = Text(
            "try every combination",
            font_size=28,
            color=LABEL_GRAY,
        )
        subtitle.next_to(header, DOWN, buff=0.5)

        array_row = self.make_array_row(highlight_indices=[0])
        array_row.next_to(subtitle, DOWN, buff=1.0)

        pointer = Text("start →", font_size=20, color=ACCENT, font="Monospace")
        pointer.next_to(array_row[0], UP, buff=0.3)

        self.play(Write(header), run_time=1.2)
        self.play(Write(subtitle), run_time=1.5)
        self.play(FadeIn(array_row), FadeIn(pointer), run_time=1.2)
        self.hold(6.0)
        self.clear_scene()

    # - SCENE 6 - Brute Force Pair Checks

    def scene_06_brute_force_checks(self):
        self.gap(8)

        checks = [
            ("01", "2 + 1 = 3  ✗"),
            ("02", "2 + 5 = 7  ✗"),
            ("03", "2 + 3 = 5  ✗"),
            ("04", "1 + 5 = 6  ✗"),
            ("05", "1 + 3 = 4  ✓"),
        ]
        rows = VGroup(
            *[self.make_numbered_row(num, lbl, active=False) for num, lbl in checks]
        )
        rows.arrange(DOWN, buff=0.4)
        rows.move_to(ORIGIN)

        self.play(
            AnimationGroup(
                *[FadeIn(row, shift=DOWN * 0.15) for row in rows],
                lag_ratio=0.2,
            ),
            run_time=2.5,
        )

        for idx in range(len(checks)):
            active_row = self.make_numbered_row(
                checks[idx][0],
                checks[idx][1],
                active=(idx == len(checks) - 1),
            )
            active_row.move_to(rows[idx].get_center())
            self.play(Transform(rows[idx], active_row), run_time=0.7)
            self.wait(0.5 if idx < len(checks) - 1 else 1.0)

        self.hold(4.0)
        self.clear_scene()

    # - SCENE 7 - Scan Pattern

    def scene_07_scan_pattern(self):
        self.gap(10)

        header = self.spaced_caps(
            "FOR EACH ELEMENT · SCAN EVERYTHING AFTER",
            size=14,
            color=LABEL_GRAY,
        )
        header.to_edge(UP, buff=0.8)

        scan_data = [
            ("01", "element 0 checks  n - 1  others"),
            ("02", "element 1 checks  n - 2  others"),
            ("03", "element 2 checks  n - 3  others"),
        ]
        rows = VGroup(
            *[
                self.make_numbered_row(num, lbl, active=(i == 0))
                for i, (num, lbl) in enumerate(scan_data)
            ]
        )
        rows.arrange(DOWN, buff=0.5)
        rows.next_to(header, DOWN, buff=0.8)

        self.play(Write(header), run_time=1.5)
        self.play(FadeIn(rows), run_time=1.5)

        for i in range(1, len(scan_data)):
            active_row = self.make_numbered_row(
                scan_data[i][0], scan_data[i][1], active=True
            )
            active_row.move_to(rows[i].get_center())
            prev_row = self.make_numbered_row(
                scan_data[i - 1][0], scan_data[i - 1][1], active=False
            )
            prev_row.move_to(rows[i - 1].get_center())
            self.play(
                Transform(rows[i - 1], prev_row),
                Transform(rows[i], active_row),
                run_time=0.7,
            )
            self.wait(0.5)

        self.hold(5.0)
        self.clear_scene()

    # - SCENE 8 - O(n²) Time Complexity

    def scene_08_time_complexity(self):
        self.gap(10)

        header = self.spaced_caps("BRUTE FORCE", size=22, color=LABEL_GRAY)

        complexity = Text("O(n²)", font_size=72, color=SLOW_RED, weight=BOLD)
        sub = Text(
            "roughly n² comparisons",
            font_size=28,
            color=LABEL_GRAY,
        )

        content = VGroup(header, complexity, sub).arrange(DOWN, buff=0.55)
        content.move_to(ORIGIN)

        self.play(Write(header), run_time=1.0)
        self.play(Write(complexity), run_time=1.5)
        self.play(Write(sub), run_time=1.2)
        self.hold(6.0)
        self.clear_scene()

    # - SCENE 9 - Scale Problem

    def scene_09_scale_problem(self):
        self.gap(10)

        small_header = self.spaced_caps("4 ELEMENTS", size=18, color=LABEL_GRAY)
        small_ok = Text("totally fine", font_size=32, color=SUCCESS)

        big_header = self.spaced_caps("1 000 000 ELEMENTS", size=18, color=LABEL_GRAY)
        big_bad = Text("~1 trillion comparisons", font_size=32, color=SLOW_RED)

        small_grp = VGroup(small_header, small_ok).arrange(DOWN, buff=0.4)
        big_grp = VGroup(big_header, big_bad).arrange(DOWN, buff=0.4)
        content = VGroup(small_grp, big_grp).arrange(DOWN, buff=1.2)
        content.move_to(ORIGIN)

        self.play(FadeIn(small_grp), run_time=1.2)
        self.play(FadeIn(big_grp), run_time=1.5)
        self.hold(8.0)
        self.clear_scene()

    # - SCENE 10 - Narrator: Shift the Question

    def scene_10_narrator_reframe(self):
        self.gap(10)

        text = Text(
            "shift the question you're asking",
            font_size=38,
            color=WHITE,
        )
        text.to_corner(DL, buff=1.2)
        self.play(AddTextLetterByLetter(text), run_time=3.0)
        self.hold(6.0)
        self.clear_scene()

    # - SCENE 11 - Partner Concept

    def scene_11_partner_concept(self):
        self.gap(10)

        header = self.spaced_caps("PARTNER", size=22, color=ACCENT)
        header.to_edge(UP, buff=0.8)

        array_row = self.make_array_row(highlight_indices=[1])
        array_row.next_to(header, DOWN, buff=0.8)

        eq = Text("4  -  1  =  3", font_size=44, color=WHITE, weight=BOLD)
        eq.next_to(array_row, DOWN, buff=0.9)

        partner_lbl = self.spaced_caps(
            "THE OTHER NUMBER THAT HITS THE TARGET",
            size=12,
            color=LABEL_GRAY,
        )
        partner_lbl.next_to(eq, DOWN, buff=0.5)

        self.play(Write(header), run_time=1.0)
        self.play(FadeIn(array_row), run_time=1.0)
        self.play(Write(eq), run_time=1.5)
        self.play(Write(partner_lbl), run_time=1.5)
        self.hold(8.0)
        self.clear_scene()

    # - SCENE 12 - Reframed Problem

    def scene_12_reframed_problem(self):
        self.gap(10)

        old_q = self.make_label_box(
            "OLD QUESTION",
            "find two numbers",
            stroke_color=BOX_STROKE,
            width=4.5,
            height=1.8,
        )
        new_q = self.make_label_box(
            "NEW QUESTION",
            "does partner exist?",
            stroke_color=ACCENT,
            fill_color=ACCENT_FILL,
            label_color=ACCENT_LIGHT,
            width=4.5,
            height=1.8,
        )

        arrow = Arrow(
            old_q.get_right() + RIGHT * 0.1,
            new_q.get_left() + LEFT * 0.1,
            color=ACCENT,
            stroke_width=2,
            buff=0.1,
            max_tip_length_to_length_ratio=0.12,
        )

        formula = Text(
            "y = target - x", font_size=32, color=ACCENT_LIGHT, font="Monospace"
        )
        formula.next_to(VGroup(old_q, new_q), DOWN, buff=0.8)

        group = VGroup(old_q, arrow, new_q)
        group.move_to(ORIGIN + UP * 0.3)

        self.play(FadeIn(old_q), run_time=1.0)
        self.play(Create(arrow), FadeIn(new_q), run_time=1.5)
        self.play(Write(formula), run_time=1.2)
        self.hold(8.0)
        self.clear_scene()

    # - SCENE 13 - HashMap Metaphor

    def scene_13_hashmap_metaphor(self):
        self.gap(10)

        header = self.spaced_caps("HASH MAP", size=28, color=ACCENT)
        header.to_edge(UP, buff=0.7)

        subtitle = Text(
            "each value hangs on a labeled hook",
            font_size=24,
            color=LABEL_GRAY,
        )
        subtitle.next_to(header, DOWN, buff=0.4)

        hooks = VGroup()
        for val in [2, 1, 5, 3]:
            hook_box = RoundedRectangle(
                corner_radius=0.08,
                width=1.0,
                height=0.55,
                stroke_color=BOX_STROKE,
                stroke_width=1.2,
                fill_color=BOX_FILL_ALT,
                fill_opacity=1,
            )
            hook_lbl = Text(str(val), font_size=16, color=LABEL_GRAY, font="Monospace")
            hook_lbl.move_to(hook_box.get_center())
            val_box = RoundedRectangle(
                corner_radius=0.08,
                width=0.7,
                height=0.7,
                stroke_color=ACCENT,
                stroke_width=1.5,
                fill_color=ACCENT_FILL,
                fill_opacity=1,
            )
            val_txt = Text(str(val), font_size=20, color=WHITE, weight=BOLD)
            val_txt.move_to(val_box.get_center())
            hook_grp = VGroup(hook_box, hook_lbl, val_box, val_txt)
            val_box.next_to(hook_box, UP, buff=0.15)
            val_txt.move_to(val_box.get_center())
            hooks.add(hook_grp)

        hooks.arrange(RIGHT, buff=0.6)
        hooks.next_to(subtitle, DOWN, buff=0.9)

        teleport = self.spaced_caps(
            "INSTANT LOOKUP · NO SCANNING",
            size=14,
            color=ACCENT_LIGHT,
        )
        teleport.next_to(hooks, DOWN, buff=0.7)

        self.play(Write(header), Write(subtitle), run_time=1.5)
        self.play(
            AnimationGroup(
                *[FadeIn(h, shift=UP * 0.2) for h in hooks],
                lag_ratio=0.2,
            ),
            run_time=2.5,
        )
        self.play(Write(teleport), run_time=1.2)
        self.hold(8.0)
        self.clear_scene()

    # - SCENE 14 - Build As You Go

    def scene_14_build_as_you_go(self):
        self.gap(10)

        header = self.spaced_caps("BUILD THE WALL AS YOU GO", size=16, color=LABEL_GRAY)
        header.to_edge(UP, buff=0.8)

        problem = self.make_label_box(
            "EDGE CASE",
            "2 + 2 = 4",
            stroke_color=SLOW_RED,
            fill_color="#3D1A1A",
            label_color=SLOW_RED,
            width=3.5,
            height=1.6,
        )
        problem.next_to(header, DOWN, buff=0.7)

        fix = Text(
            "check first · hang after",
            font_size=28,
            color=ACCENT_LIGHT,
            weight=BOLD,
        )
        fix.next_to(problem, DOWN, buff=0.7)

        self.play(Write(header), run_time=1.5)
        self.play(FadeIn(problem), run_time=1.0)
        self.play(Write(fix), run_time=1.5)
        self.hold(8.0)
        self.clear_scene()

    # - SCENE 15 - HashMap Walkthrough

    def scene_15_hashmap_walkthrough(self):
        self.gap(10)

        header = self.spaced_caps("ONE PASS", size=22, color=ACCENT)
        header.to_edge(UP, buff=0.6)

        steps = [
            ("01", "2 → partner 2?  wall empty  →  hang 2"),
            ("02", "1 → partner 3?  only 2       →  hang 1"),
            ("03", "5 → partner -1? no          →  hang 5"),
            ("04", "3 → partner 1?  yes at [1]  →  done"),
        ]

        rows = VGroup()
        for num, lbl in steps:
            rows.add(
                self.make_numbered_row(num, lbl, active=False, width=10, height=0.85)
            )
        rows.arrange(DOWN, buff=0.35)
        rows.next_to(header, DOWN, buff=0.6)

        self.play(Write(header), run_time=1.0)
        self.play(FadeIn(rows), run_time=1.5)

        for idx in range(len(steps)):
            active_row = self.make_numbered_row(
                steps[idx][0],
                steps[idx][1],
                active=True,
                width=10,
                height=0.85,
            )
            active_row.move_to(rows[idx].get_center())
            if idx > 0:
                prev_row = self.make_numbered_row(
                    steps[idx - 1][0],
                    steps[idx - 1][1],
                    active=False,
                    width=10,
                    height=0.85,
                )
                prev_row.move_to(rows[idx - 1].get_center())
                self.play(
                    Transform(rows[idx - 1], prev_row),
                    Transform(rows[idx], active_row),
                    run_time=0.8,
                )
            else:
                self.play(Transform(rows[idx], active_row), run_time=0.8)
            self.wait(0.7 if idx < len(steps) - 1 else 1.2)

        self.hold(5.0)
        self.clear_scene()

    # - SCENE 16 - Solution Found

    def scene_16_solution_found(self):
        self.gap(8)

        header = self.spaced_caps("SOLUTION", size=28, color=SUCCESS)
        header.to_edge(UP, buff=0.8)

        array_row = self.make_array_row(partner_indices=[1, 3])
        array_row.next_to(header, DOWN, buff=0.8)

        result = Text(
            "[1, 3]", font_size=48, color=SUCCESS, font="Monospace", weight=BOLD
        )
        result.next_to(array_row, DOWN, buff=0.8)

        summary = self.spaced_caps(
            "ONE PASS · ONE CHECK PER ELEMENT",
            size=14,
            color=LABEL_GRAY,
        )
        summary.next_to(result, DOWN, buff=0.5)

        self.play(Write(header), run_time=1.0)
        self.play(FadeIn(array_row), run_time=1.0)
        self.play(Write(result), run_time=1.2)
        self.play(Write(summary), run_time=1.2)
        self.hold(8.0)
        self.clear_scene()

    # - SCENE 17 - One Pass Proof (A before B)

    def scene_17_one_pass_proof(self):
        self.gap(10)

        header = self.spaced_caps("WHY ONE PASS WORKS", size=18, color=LABEL_GRAY)
        header.to_edge(UP, buff=0.8)

        elem_a = self.make_label_box(
            "ELEMENT A",
            "comes first",
            stroke_color=ACCENT,
            fill_color=ACCENT_FILL,
            label_color=ACCENT_LIGHT,
            width=3.2,
            height=1.6,
        )
        elem_b = self.make_label_box(
            "ELEMENT B",
            "comes later",
            stroke_color=SUCCESS,
            fill_color="#1A3D2E",
            label_color=SUCCESS,
            width=3.2,
            height=1.6,
        )
        boxes = VGroup(elem_a, elem_b).arrange(RIGHT, buff=2.0)
        boxes.next_to(header, DOWN, buff=0.8)

        arrow = Arrow(
            elem_a.get_bottom(),
            elem_b.get_bottom() + DOWN * 0.5,
            color=LABEL_GRAY,
            stroke_width=1.5,
            buff=0.1,
        )
        arrow.shift(DOWN * 0.3)

        steps = [
            ("01", "visit A → partner B not on wall yet → hang A"),
            ("02", "visit B → A already on wall → found instantly"),
        ]
        rows = VGroup(
            *[
                self.make_numbered_row(num, lbl, active=(i == 1), width=9.5, height=0.8)
                for i, (num, lbl) in enumerate(steps)
            ]
        )
        rows.arrange(DOWN, buff=0.35)
        rows.next_to(boxes, DOWN, buff=1.0)

        self.play(Write(header), run_time=1.0)
        self.play(FadeIn(elem_a), FadeIn(elem_b), run_time=1.2)
        self.play(FadeIn(rows), run_time=1.5)
        self.hold(10.0)
        self.clear_scene()

    # - SCENE 18 - Complexity Comparison

    def scene_18_complexity_comparison(self):
        self.gap(10)

        brute = self.make_label_box(
            "BRUTE FORCE",
            "O(n²)",
            stroke_color=SLOW_RED,
            fill_color="#3D1A1A",
            label_color=SLOW_RED,
            width=3.5,
            height=2,
        )
        optimal = self.make_label_box(
            "HASH MAP",
            "O(n)",
            stroke_color=ACCENT,
            fill_color=ACCENT_FILL,
            label_color=ACCENT_LIGHT,
            width=3.5,
            height=2,
        )
        group = VGroup(brute, optimal).arrange(RIGHT, buff=2.5)
        group.shift(UP * 0.5)

        brute_ops = Text(
            "~1 trillion ops", font_size=22, color=SLOW_RED, font="Monospace"
        )
        optimal_ops = Text(
            "~1 million ops", font_size=22, color=ACCENT_LIGHT, font="Monospace"
        )
        brute_ops.next_to(brute, DOWN, buff=0.4)
        optimal_ops.next_to(optimal, DOWN, buff=0.4)

        self.play(FadeIn(brute), FadeIn(optimal), run_time=1.5)
        self.play(Write(brute_ops), Write(optimal_ops), run_time=1.5)
        self.hold(10.0)
        self.clear_scene()

    # - SCENE 19 - Space Complexity

    def scene_19_space_complexity(self):
        self.gap(10)

        header = self.spaced_caps("SPACE COMPLEXITY", size=20, color=LABEL_GRAY)

        space = Text("O(n)", font_size=64, color=ACCENT, weight=BOLD)

        trade = Text(
            "extra memory  ↔  dramatically less runtime",
            font_size=26,
            color=LABEL_GRAY,
        )

        content = VGroup(header, space, trade).arrange(DOWN, buff=0.55)
        content.move_to(ORIGIN)

        self.play(Write(header), run_time=1.0)
        self.play(Write(space), run_time=1.2)
        self.play(Write(trade), run_time=1.5)
        self.hold(8.0)
        self.clear_scene()

    # - SCENE 20 - Outro: Habit of Mind

    def scene_20_outro(self):
        self.gap(10)

        line1 = Text(
            "what exactly am I looking for?",
            font_size=40,
            color=WHITE,
            weight=BOLD,
        )
        line2 = self.spaced_caps(
            "BUILD A LOOKUP · SEARCH BECOMES TRIVIAL",
            size=16,
            color=ACCENT_LIGHT,
        )
        content = VGroup(line1, line2).arrange(DOWN, buff=0.7)
        content.move_to(ORIGIN)

        self.play(Write(line1), run_time=2.0)
        self.play(Write(line2), run_time=2.0)
        self.hold(10.0)
        self.clear_scene()
        self.gap(15)
