"""
Two Sum - Manim explainer
Render: manim -pqm main.py TwoSum -- --sound
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *
from helper_methods import (
    Explainer,
    MONO,
    ARIAL,
    RED,
    PURP,
    PURP_FILL,
    PURP_LIGHT,
    BOX_FILL,
    BOX_FILL_ALT,
    BOX_STROKE,
    LABEL_GRAY,
    WHITE,
)

SUCCESS = "#22C55E"
SUCCESS_FILL = "#1A3D2E"
SLOW_FILL = "#3D1A1A"

ARRAY = [2, 1, 5, 3]
TARGET = 4

ADD_SOUND = "--sound" in sys.argv
AUDIO = "audio/TwoSum_Edited.mp3"
AUDIO = "audio/TwoSum_1Min.wav"


class TwoSum(Explainer):
    def construct(self):
        if ADD_SOUND:
            self.add_sound(AUDIO)
        self.problem_hook()
        self.answer_reveal()
        self.naive_vs_clever()
        # self.brute_force_intro()
        # self.brute_force_checks()
        # self.scan_pattern()
        # self.time_complexity()
        # self.scale_problem()
        # self.narrator_reframe()
        # self.partner_concept()
        # self.reframed_problem()
        # self.hashmap_metaphor()
        # self.build_as_you_go()
        # self.hashmap_walkthrough()
        # self.solution_found()
        # self.one_pass_proof()
        # self.complexity_comparison()
        # self.space_complexity()
        # self.outro()

    # --- Two Sum visuals ---

    def make_array_cell(self, value, index=None, active=False, partner=False):
        stroke = PURP if active else SUCCESS if partner else BOX_STROKE
        fill = PURP_FILL if active else SUCCESS_FILL if partner else BOX_FILL
        box = RoundedRectangle(
            corner_radius=0.12,
            width=1.1,
            height=1.1,
            stroke_color=stroke,
            stroke_width=2 if active or partner else 1.5,
            fill_color=fill,
            fill_opacity=1,
        )
        val = Text(str(value), font=MONO, font_size=32, color=WHITE, weight=BOLD)
        val.move_to(box.get_center())
        grp = VGroup(box, val)
        if index is not None:
            idx_lbl = Text(
                f"[{index}]",
                font=MONO,
                font_size=14,
                color=LABEL_GRAY,
            )
            idx_lbl.next_to(box, DOWN, buff=0.15)
            grp.add(idx_lbl)
        return grp

    def make_array_row(self, values=None, highlight_indices=None, partner_indices=None):
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

    def make_hash_hook(self, value, filled=False, highlight=False):
        stroke = PURP if highlight else BOX_STROKE
        fill = PURP_FILL if filled else BOX_FILL_ALT
        hook_box = RoundedRectangle(
            corner_radius=0.08,
            width=1.0,
            height=0.55,
            stroke_color=stroke,
            stroke_width=1.2,
            fill_color=BOX_FILL_ALT,
            fill_opacity=1,
        )
        hook_lbl = Text(str(value), font_size=16, color=LABEL_GRAY, font="Monospace")
        hook_lbl.move_to(hook_box.get_center())
        grp = VGroup(hook_box, hook_lbl)
        if filled:
            val_box = RoundedRectangle(
                corner_radius=0.08,
                width=0.7,
                height=0.7,
                stroke_color=stroke,
                stroke_width=1.5,
                fill_color=fill,
                fill_opacity=1,
            )
            val_txt = Text(str(value), font_size=20, color=WHITE, weight=BOLD)
            val_txt.move_to(val_box.get_center())
            val_box.next_to(hook_box, UP, buff=0.15)
            val_txt.move_to(val_box.get_center())
            grp.add(val_box, val_txt)
        return grp

    def make_hash_wall(self, hook_values, filled_values=None, highlight_hook=None):
        filled_values = filled_values or set()
        hooks = VGroup(
            *[
                self.make_hash_hook(
                    v,
                    filled=v in filled_values,
                    highlight=v == highlight_hook,
                )
                for v in hook_values
            ]
        )
        hooks.arrange(RIGHT, buff=0.55)
        wall_lbl = self.spaced_caps("THE WALL", size=12, color=LABEL_GRAY)
        wall_lbl.next_to(hooks, UP, buff=0.35)
        return VGroup(wall_lbl, hooks)

    # - SCENE 1
    def problem_hook(self):
        tag = self.corner_label("TWO SUM · SETUP")
        title = self.two_tone_title("TWO", "SUM", accent_color=PURP, size=44)
        title.to_edge(UP, buff=1.1)

        hook = self.narrator_line(
            "A question that sounds almost insultingly simple",
            font="Inter",
            size=30,
            color=WHITE,
        )

        array_label = self.dot_label(
            "GIVEN THIS LIST", dot_color=PURP, text_color=WHITE
        )
        array_row = self.make_array_row()
        array_grp = VGroup(array_label, array_row).arrange(DOWN, buff=0.45)

        target_box = self.make_label_box(
            "TARGET",
            str(TARGET),
            stroke_color=PURP,
            fill_color=PURP_FILL,
            label_color=PURP_LIGHT,
            width=3,
            height=1.6,
        )

        content = VGroup(array_grp, target_box).arrange(DOWN, buff=0.55)
        content.next_to(title, DOWN, buff=0.65)

        question = Text(
            "GOAL: Find the two that add up to the target",
            font=MONO,
            font_size=26,
            color=WHITE,
        )
        question.next_to(content, DOWN, buff=0.45)

        self.play(
            FadeIn(tag),
            FadeIn(title, shift=UP * 0.1),
            run_time=1.0,
        )
        self.play(Write(hook), run_time=1.5)
        self.hold(2)
        self.play(FadeOut(hook), FadeIn(array_label), run_time=0.6)
        self.stagger_in(list(array_row), shift=DOWN * 0.12, lag=0.15, run_time=1.0)
        self.play(Write(question), run_time=1.0)
        self.play(FadeIn(target_box, shift=UP * 0.15), run_time=0.8)
        self.hold(1.0)

        pause = (
            Triangle(color=WHITE)
            .set_fill(WHITE, 1)
            .set_opacity(0.5)
            .shift(RIGHT * 0.25)
            .scale(2)
            .rotate(-PI / 2)  # -90 deg
        )
        self.play(GrowFromCenter(pause), run_time=0.5)
        self.hold(2)
        self.clear_scene()

    # - SCENE 2
    def answer_reveal(self):
        tag = self.corner_label("SPOILER")
        joke = self.narrator_line(
            "Obviously I'm joking!",
            size=30,
        ).shift(UP * 2)

        array_row = self.make_array_row()
        array_row.shift(UP * 0.6)

        self.play(FadeIn(tag), FadeIn(array_row), run_time=1.0)
        self.play(FadeIn(joke, shift=UP * 0.1), run_time=1.5)

        one = (
            self.make_array_cell(1, 1, partner=True)
            .move_to(array_row[1].get_center())
            .scale(1.05)
        )
        three = (
            self.make_array_cell(3, 3, partner=True)
            .move_to(array_row[3].get_center())
            .scale(1.05)
        )

        self.play(
            Transform(
                array_row[1],
                one,
            ),
            Transform(
                array_row[3],
                three,
            ),
            run_time=1.2,
        )

        target_box = self.make_label_box(
            "TARGET",
            str(TARGET),
            stroke_color=PURP,
            fill_color=PURP_FILL,
            label_color=PURP_LIGHT,
            width=3,
            height=1.6,
        )
        target_box.next_to(array_row, DOWN, buff=0.5).shift(LEFT * 0.05)
        self.play(FadeIn(target_box, shift=UP * 0.15), run_time=0.8)

        eq = Text("1  +  3  =  4", font_size=48, color=WHITE, weight=BOLD)
        eq.next_to(target_box, DOWN, buff=0.5).shift(LEFT * 0.05)
        check = Text("✓", font_size=56, color=SUCCESS)
        check.next_to(eq, RIGHT, buff=0.5)

        self.play(Write(eq), run_time=1.2)
        self.play(FadeIn(check, scale=0.5), run_time=0.7)
        self.hold(2.0)
        self.clear_scene()

    # - SCENE 3
    def naive_vs_clever(self):
        tag = self.corner_label("WHY IT MATTERS")
        lead = Text(
            "how you find them matters enormously",
            font_size=30,
            color=WHITE,
        )
        lead.next_to(tag, DOWN, buff=0.55).align_to(tag, LEFT)

        naive = self.make_label_box(
            "NAIVE",
            "chokes",
            stroke_color=RED,
            fill_color=SLOW_FILL,
            label_color=RED,
            width=3.5,
            height=2,
        )
        clever = self.make_label_box(
            "CLEVER",
            "breezes through",
            stroke_color=PURP,
            fill_color=PURP_FILL,
            label_color=PURP_LIGHT,
            width=3.5,
            height=2,
        )
        boxes = VGroup(naive, clever).arrange(RIGHT, buff=2.2)
        boxes.next_to(lead, DOWN, buff=0.75).shift(RIGHT * 0.5)

        scale = self.make_stat_callout(
            "AT SCALE",
            "1,000,000",
            sub="numbers in the array",
            width=5.0,
            height=2.0,
        )
        scale.next_to(boxes, DOWN, buff=0.65)

        insight = self.spaced_caps(
            "THE INSIGHT IS SOMETHING YOU COULD INVENT YOURSELF",
            size=11,
            color=LABEL_GRAY,
        )
        insight.next_to(scale, DOWN, buff=0.45)

        self.play(FadeIn(tag), Write(lead), run_time=1.5)
        self.play(FadeIn(naive, shift=RIGHT * 0.2), run_time=1.0)
        self.play(FadeIn(clever, shift=LEFT * 0.2), run_time=1.0)
        self.play(FadeIn(scale, shift=UP * 0.15), run_time=1.2)
        self.play(Write(insight), run_time=1.5)
        self.hold(7.0)
        self.clear_scene()

    # - SCENE 5 - Brute Force Intro

    def scene_05_brute_force_intro(self):
        self.gap(12)

        tag = self.corner_label("BRUTE FORCE")
        header = self.spaced_caps("TRY EVERY COMBINATION", size=18, color=RED)
        header.next_to(tag, DOWN, buff=0.5).align_to(tag, LEFT)

        subtitle = Text(
            "the most natural thing your brain does",
            font_size=26,
            color=LABEL_GRAY,
        )
        subtitle.next_to(header, DOWN, buff=0.4).align_to(header, LEFT)

        array_row = self.make_array_row(highlight_indices=[0])
        array_row.next_to(subtitle, DOWN, buff=0.85).shift(RIGHT * 0.3)

        pointer = Text(
            "start with 2 →", font_size=20, color=PURP, font="Monospace"
        )
        pointer.next_to(array_row[0], UP, buff=0.3)

        self.play(FadeIn(tag), Write(header), run_time=1.2)
        self.play(Write(subtitle), run_time=1.2)
        self.play(FadeIn(array_row), FadeIn(pointer), run_time=1.0)

        for i in range(1, 4):
            self.play(
                Transform(
                    array_row[0],
                    self.make_array_cell(ARRAY[0], 0, active=False),
                ),
                Transform(
                    array_row[i],
                    self.make_array_cell(ARRAY[i], i, active=True),
                ),
                run_time=0.55,
            )
            self.wait(0.35)
            self.play(
                Transform(
                    array_row[i],
                    self.make_array_cell(ARRAY[i], i, active=False),
                ),
                run_time=0.35,
            )

        self.play(
            Transform(
                array_row[0],
                self.make_array_cell(ARRAY[0], 0, active=True),
            ),
            run_time=0.5,
        )
        self.hold(6.0)
        self.clear_scene()

    # - SCENE 6 - Brute Force Pair Checks

    def scene_06_brute_force_checks(self):
        self.gap(10)

        tag = self.corner_label("CHECKING PAIRS")
        array_row = self.make_array_row(highlight_indices=[0])
        array_row.scale(0.85).to_edge(UP, buff=1.4)

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
        rows.arrange(DOWN, buff=0.32)
        rows.next_to(array_row, DOWN, buff=0.55)

        self.play(FadeIn(tag), FadeIn(array_row), run_time=1.0)
        self.stagger_in(list(rows), shift=DOWN * 0.12, lag=0.14, run_time=2.0)

        pair_highlights = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)]

        def active_fn(idx):
            return self.make_numbered_row(
                checks[idx][0],
                checks[idx][1],
                active=(idx == len(checks) - 1),
            )

        def inactive_fn(idx):
            return self.make_numbered_row(checks[idx][0], checks[idx][1], active=False)

        for idx in range(len(checks)):
            a, b = pair_highlights[idx]
            self.play(
                Transform(array_row[a], self.make_array_cell(ARRAY[a], a, active=True)),
                Transform(array_row[b], self.make_array_cell(ARRAY[b], b, active=True)),
                run_time=0.45,
            )
            active_row = active_fn(idx)
            active_row.move_to(rows[idx].get_center())
            if idx > 0:
                prev = inactive_fn(idx - 1)
                prev.move_to(rows[idx - 1].get_center())
                self.play(
                    Transform(rows[idx - 1], prev),
                    Transform(rows[idx], active_row),
                    run_time=0.65,
                )
            else:
                self.play(Transform(rows[idx], active_row), run_time=0.65)
            self.wait(0.65 if idx < len(checks) - 1 else 1.5)
            if idx < len(checks) - 1:
                self.play(
                    Transform(
                        array_row[a], self.make_array_cell(ARRAY[a], a, active=False)
                    ),
                    Transform(
                        array_row[b], self.make_array_cell(ARRAY[b], b, active=False)
                    ),
                    run_time=0.3,
                )

        self.hold(5.0)
        self.clear_scene()

    # - SCENE 7 - Scan Pattern

    def scene_07_scan_pattern(self):
        self.gap(12)

        tag = self.corner_label("WHAT'S ACTUALLY HAPPENING")
        header = self.spaced_caps(
            "FOR EACH ELEMENT · SCAN EVERYTHING AFTER",
            size=13,
            color=LABEL_GRAY,
        )
        header.next_to(tag, DOWN, buff=0.45).align_to(tag, LEFT)

        array_row = self.make_array_row()
        array_row.scale(0.9).next_to(header, DOWN, buff=0.65).shift(RIGHT * 0.2)

        scan_data = [
            ("01", "element 0 checks  n − 1  others"),
            ("02", "element 1 checks  n − 2  others"),
            ("03", "element 2 checks  n − 3  others"),
        ]
        rows = VGroup(
            *[
                self.make_numbered_row(num, lbl, active=(i == 0))
                for i, (num, lbl) in enumerate(scan_data)
            ]
        )
        rows.arrange(DOWN, buff=0.38)
        rows.next_to(array_row, DOWN, buff=0.55)

        scan_arrows = VGroup()

        self.play(FadeIn(tag), Write(header), FadeIn(array_row), run_time=1.4)
        self.play(FadeIn(rows), run_time=1.0)

        scan_ranges = [(1, 4), (2, 4), (3, 4)]
        for i, (start, end) in enumerate(scan_ranges):
            if i > 0:
                prev_row = self.make_numbered_row(
                    scan_data[i - 1][0], scan_data[i - 1][1], active=False
                )
                prev_row.move_to(rows[i - 1].get_center())
                active_row = self.make_numbered_row(
                    scan_data[i][0], scan_data[i][1], active=True
                )
                active_row.move_to(rows[i].get_center())
                self.play(
                    Transform(rows[i - 1], prev_row),
                    Transform(rows[i], active_row),
                    run_time=0.65,
                )
            self.play(
                Transform(
                    array_row[i],
                    self.make_array_cell(ARRAY[i], i, active=True),
                ),
                run_time=0.5,
            )
            new_arrows = VGroup()
            for j in range(start, end):
                arr = Arrow(
                    array_row[i].get_bottom() + DOWN * 0.05,
                    array_row[j].get_top() + UP * 0.05,
                    color=PURP,
                    stroke_width=1.5,
                    buff=0.08,
                    max_tip_length_to_length_ratio=0.15,
                )
                new_arrows.add(arr)
            if scan_arrows:
                self.play(FadeOut(scan_arrows), FadeIn(new_arrows), run_time=0.6)
            else:
                self.play(FadeIn(new_arrows), run_time=0.6)
            scan_arrows = new_arrows
            self.wait(0.75)

        self.hold(6.0)
        self.clear_scene()

    # - SCENE 8 - O(n²) Time Complexity

    def scene_08_time_complexity(self):
        self.gap(12)

        tag = self.corner_label("TIME COMPLEXITY")
        card = self.make_stat_callout(
            "BRUTE FORCE",
            "O(n²)",
            sub="roughly n² comparisons in the worst case",
            width=6.0,
            height=2.6,
        )
        card.shift(UP * 0.2)

        formula = Text(
            "n + (n−1) + (n−2) + … + 1  ≈  n²", font_size=24, color=LABEL_GRAY
        )
        formula.next_to(card, DOWN, buff=0.55)

        self.play(FadeIn(tag), FadeIn(card, shift=UP * 0.15), run_time=1.5)
        self.write_then_hold(formula, write_time=1.4, hold_time=7.0)
        self.clear_scene()

    # - SCENE 9 - Scale Problem

    def scene_09_scale_problem(self):
        self.gap(12)

        tag = self.corner_label("SCALE")

        small = self.make_label_box(
            "4 ELEMENTS",
            "totally fine",
            stroke_color=SUCCESS,
            fill_color=SUCCESS_FILL,
            label_color=SUCCESS,
            width=3.6,
            height=1.8,
        )
        big = self.make_stat_callout(
            "1,000,000 ELEMENTS",
            "~1 trillion",
            sub="comparisons",
            width=5.5,
            height=2.2,
            stroke_color=RED,
            fill_color=SLOW_FILL,
        )

        content = VGroup(small, big).arrange(DOWN, buff=0.85)
        content.next_to(tag, DOWN, buff=0.65).shift(RIGHT * 0.4)

        better = Text(
            "there must be a better way",
            font_size=28,
            color=WHITE,
            weight=BOLD,
        )
        better.next_to(content, DOWN, buff=0.6)

        self.play(FadeIn(tag), FadeIn(small, shift=DOWN * 0.1), run_time=1.2)
        self.play(FadeIn(big, shift=DOWN * 0.1), run_time=1.3)
        self.write_then_hold(better, write_time=1.4, hold_time=7.0)
        self.clear_scene()

    # - SCENE 10 - Narrator: Shift the Question

    def scene_10_narrator_reframe(self):
        self.gap(14)

        tag = self.corner_label("REFRAME")
        line1 = self.narrator_line(
            "shift the question you're asking",
            size=36,
            corner=DL,
            buff=1.0,
        )
        line2 = Text(
            "ask the right question — and you could invent the answer",
            font_size=24,
            color=LABEL_GRAY,
        )
        line2.next_to(line1, UP, buff=0.45).align_to(line1, LEFT)

        self.play(FadeIn(tag), run_time=0.6)
        self.play(AddTextLetterByLetter(line1), run_time=2.5)
        self.play(FadeIn(line2, shift=UP * 0.1), run_time=1.2)
        self.hold(8.0)
        self.clear_scene()

    # - SCENE 11 - Partner Concept

    def scene_11_partner_concept(self):
        self.gap(14)

        tag = self.corner_label("PARTNER")
        header = self.spaced_caps(
            "WHAT ARE YOU ACTUALLY LOOKING FOR?", size=14, color=LABEL_GRAY
        )
        header.next_to(tag, DOWN, buff=0.45).align_to(tag, LEFT)

        array_row = self.make_array_row(highlight_indices=[1])
        array_row.next_to(header, DOWN, buff=0.7).shift(RIGHT * 0.2)

        known = Text("you already know one half:  1", font_size=26, color=WHITE)
        known.next_to(array_row, DOWN, buff=0.55)

        eq = Text("4  −  1  =  3", font_size=44, color=WHITE, weight=BOLD)
        eq.next_to(known, DOWN, buff=0.45)

        partner_def = self.spaced_caps(
            "THE OTHER NUMBER THAT HITS THE TARGET",
            size=11,
            color=PURP_LIGHT,
        )
        partner_def.next_to(eq, DOWN, buff=0.4)

        partner_tag = self.make_badge("PARTNER OF 1", size=13)
        partner_tag.next_to(partner_def, DOWN, buff=0.3)

        self.play(FadeIn(tag), Write(header), run_time=1.2)
        self.play(FadeIn(array_row), run_time=0.9)
        self.reveal_stack(
            [known, eq, partner_def, partner_tag], item_pause=1.0, run_time=0.9
        )
        self.hold(9.0)
        self.clear_scene()

    # - SCENE 12 - Reframed Problem

    def scene_12_reframed_problem(self):
        self.gap(14)

        tag = self.corner_label("NEW FRAMING")
        old_q = self.make_label_box(
            "OLD QUESTION",
            "find two numbers",
            stroke_color=BOX_STROKE,
            width=4.2,
            height=1.7,
        )
        new_q = self.make_label_box(
            "NEW QUESTION",
            "does partner exist?",
            stroke_color=PURP,
            fill_color=PURP_FILL,
            label_color=PURP_LIGHT,
            width=4.2,
            height=1.7,
        )

        arrow = Arrow(
            old_q.get_right() + RIGHT * 0.08,
            new_q.get_left() + LEFT * 0.08,
            color=PURP,
            stroke_width=2,
            buff=0.08,
            max_tip_length_to_length_ratio=0.12,
        )
        boxes = VGroup(old_q, arrow, new_q)
        boxes.next_to(tag, DOWN, buff=0.65).shift(RIGHT * 0.5)

        formula = self.mono_string("y = target − x", size=34, color=PURP_LIGHT)
        formula.next_to(boxes, DOWN, buff=0.65)

        exists = Text(
            "does the corresponding y exist in the array?",
            font_size=24,
            color=LABEL_GRAY,
        )
        exists.next_to(formula, DOWN, buff=0.4)

        tool = self.make_badge("BUILD THE RIGHT TOOL FIRST", size=13)
        tool.next_to(exists, DOWN, buff=0.45)

        self.play(FadeIn(tag), FadeIn(old_q), run_time=1.0)
        self.play(Create(arrow), FadeIn(new_q), run_time=1.2)
        self.reveal_stack([formula, exists, tool], item_pause=0.9, run_time=0.85)
        self.hold(9.0)
        self.clear_scene()

    # - SCENE 13 - HashMap Metaphor

    def scene_13_hashmap_metaphor(self):
        self.gap(14)

        tag = self.corner_label("HASH MAP")
        header = self.spaced_caps("HOOKS ON A WALL", size=20, color=PURP)
        header.next_to(tag, DOWN, buff=0.45).align_to(tag, LEFT)

        subtitle = Text(
            "each number hangs on a hook labeled with its value",
            font_size=24,
            color=LABEL_GRAY,
        )
        subtitle.next_to(header, DOWN, buff=0.35).align_to(header, LEFT)

        hooks = self.make_hash_wall([2, 1, 5, 3], filled_values={2, 1, 5, 3})
        hooks.next_to(subtitle, DOWN, buff=0.75).shift(RIGHT * 0.3)

        question = Text('"Does 3 exist?"', font_size=30, color=WHITE, weight=BOLD)
        question.next_to(hooks, DOWN, buff=0.55)

        teleport = self.spaced_caps(
            "INSTANT TELEPORT · NO SCANNING",
            size=13,
            color=PURP_LIGHT,
        )
        teleport.next_to(question, DOWN, buff=0.35)

        badge = self.make_badge("HASH MAP", size=16)
        badge.next_to(teleport, DOWN, buff=0.4)

        self.play(FadeIn(tag), Write(header), Write(subtitle), run_time=1.4)
        self.stagger_in(list(hooks[1]), shift=UP * 0.15, lag=0.18, run_time=2.0)
        self.play(Write(question), run_time=1.0)
        hook_3 = hooks[1][3]
        self.play(
            hook_3[0].animate.set_stroke(PURP, width=2.5),
            hook_3[1].animate.set_color(PURP),
            run_time=0.8,
        )
        self.play(Write(teleport), FadeIn(badge), run_time=1.2)
        self.hold(9.0)
        self.clear_scene()

    # - SCENE 14 - Build As You Go

    def scene_14_build_as_you_go(self):
        self.gap(14)

        tag = self.corner_label("EDGE CASE")
        header = self.spaced_caps("BUILD THE WALL AS YOU GO", size=15, color=LABEL_GRAY)
        header.next_to(tag, DOWN, buff=0.45).align_to(tag, LEFT)

        naive_pipe = self.make_pipeline(
            ["HANG ALL", "THEN ASK"],
            active_index=0,
            width=2.4,
        )
        naive_pipe.next_to(header, DOWN, buff=0.6).shift(RIGHT * 0.3)

        problem = self.make_label_box(
            "PROBLEM",
            "2 + 2 = 4",
            stroke_color=RED,
            fill_color=SLOW_FILL,
            label_color=RED,
            width=3.2,
            height=1.5,
        )
        problem.next_to(naive_pipe, DOWN, buff=0.55)

        warn = Text(
            "same element twice — can't use the same 2",
            font_size=22,
            color=RED,
        )
        warn.next_to(problem, DOWN, buff=0.35)

        fix_pipe = self.make_pipeline(
            ["CHECK FIRST", "HANG AFTER"],
            active_index=0,
            width=2.5,
        )
        fix_pipe.next_to(warn, DOWN, buff=0.55)

        self.play(FadeIn(tag), Write(header), run_time=1.2)
        self.play(FadeIn(naive_pipe), run_time=1.0)
        self.play(FadeIn(problem), Write(warn), run_time=1.3)
        self.play(
            Transform(
                naive_pipe,
                self.make_pipeline(["HANG ALL", "THEN ASK"], active_index=None),
            ),
            FadeIn(fix_pipe, shift=UP * 0.1),
            run_time=1.2,
        )
        self.hold(9.0)
        self.clear_scene()

    # - SCENE 15 - HashMap Walkthrough

    def scene_15_hashmap_walkthrough(self):
        self.gap(16)

        tag = self.corner_label("ONE PASS WALKTHROUGH")
        header = self.spaced_caps("BUILD AS YOU GO", size=18, color=PURP)
        header.next_to(tag, DOWN, buff=0.4).align_to(tag, LEFT)

        array_row = self.make_array_row()
        array_row.scale(0.8).next_to(header, DOWN, buff=0.5).shift(RIGHT * 0.2)

        wall = self.make_hash_wall([2, 1, 5, 3], filled_values=set())
        wall.scale(0.85).next_to(array_row, DOWN, buff=0.45)

        steps = [
            ("2", "partner 2?  wall empty  →  hang 2", {2}),
            ("1", "partner 3?  only 2       →  hang 1", {2, 1}),
            ("5", "partner −1? no          →  hang 5", {2, 1, 5}),
            ("3", "partner 1?  yes at [1]  →  done", {2, 1, 5}),
        ]

        step_lbl = None
        step_anchor = wall.get_bottom() + DOWN * 0.55

        self.play(
            FadeIn(tag), Write(header), FadeIn(array_row), FadeIn(wall), run_time=1.2
        )

        for i, (val, desc, filled) in enumerate(steps):
            idx = ARRAY.index(int(val))
            self.play(
                Transform(
                    array_row[idx],
                    self.make_array_cell(ARRAY[idx], idx, active=True),
                ),
                run_time=0.45,
            )
            new_lbl = Text(desc, font_size=18, color=LABEL_GRAY if i < 3 else SUCCESS)
            new_lbl.move_to(step_anchor)
            if step_lbl is None:
                step_lbl = new_lbl
                self.play(FadeIn(step_lbl), run_time=0.55)
            else:
                self.play(Transform(step_lbl, new_lbl), run_time=0.55)

            if i < 3:
                new_wall = self.make_hash_wall([2, 1, 5, 3], filled_values=filled)
                new_wall.scale(0.85).move_to(wall.get_center())
                self.play(Transform(wall, new_wall), run_time=0.7)
            else:
                self.play(
                    wall[1][1].animate.set_stroke(SUCCESS, width=2.5),
                    run_time=0.6,
                )

            self.play(
                Transform(
                    array_row[idx],
                    self.make_array_cell(
                        ARRAY[idx], idx, active=False, partner=(i == 3)
                    ),
                ),
                run_time=0.4,
            )
            self.wait(0.85 if i < 3 else 2.0)

        self.hold(7.0)
        self.clear_scene()

    # - SCENE 16 - Solution Found

    def scene_16_solution_found(self):
        self.gap(12)

        tag = self.corner_label("SOLUTION")
        header = self.spaced_caps("INDICES RETURNED", size=18, color=SUCCESS)
        header.next_to(tag, DOWN, buff=0.45).align_to(tag, LEFT)

        array_row = self.make_array_row(partner_indices=[1, 3])
        array_row.next_to(header, DOWN, buff=0.65).shift(RIGHT * 0.2)

        result = self.mono_string("[1, 3]", size=48, color=SUCCESS)
        result.next_to(array_row, DOWN, buff=0.65)

        summary = self.spaced_caps(
            "ONE PASS · ONE CHECK PER ELEMENT",
            size=13,
            color=LABEL_GRAY,
        )
        summary.next_to(result, DOWN, buff=0.4)

        self.play(FadeIn(tag), Write(header), run_time=1.0)
        self.play(FadeIn(array_row), run_time=0.9)
        self.play(Write(result), run_time=1.0)
        self.play(Write(summary), run_time=1.0)
        self.hold(7.0)
        self.clear_scene()

    # - SCENE 17 - One Pass Proof

    def scene_17_one_pass_proof(self):
        self.gap(14)

        tag = self.corner_label("WHY IT WORKS")
        header = self.spaced_caps("ELEMENT A COMES BEFORE B", size=15, color=LABEL_GRAY)
        header.next_to(tag, DOWN, buff=0.45).align_to(tag, LEFT)

        elem_a = self.make_label_box(
            "ELEMENT A",
            "visited first",
            stroke_color=PURP,
            fill_color=PURP_FILL,
            label_color=PURP_LIGHT,
            width=3.0,
            height=1.5,
        )
        elem_b = self.make_label_box(
            "ELEMENT B",
            "visited later",
            stroke_color=SUCCESS,
            fill_color=SUCCESS_FILL,
            label_color=SUCCESS,
            width=3.0,
            height=1.5,
        )
        boxes = VGroup(elem_a, elem_b).arrange(RIGHT, buff=1.8)
        boxes.next_to(header, DOWN, buff=0.65).shift(RIGHT * 0.3)

        timeline = Arrow(
            elem_a.get_bottom() + DOWN * 0.15,
            elem_b.get_bottom() + DOWN * 0.15 + RIGHT * 0.5,
            color=LABEL_GRAY,
            stroke_width=1.5,
            buff=0.08,
        )
        timeline.shift(DOWN * 0.35)

        steps = [
            ("01", "visit A → B not on wall yet → hang A"),
            ("02", "visit B → A already on wall → found"),
        ]
        rows = VGroup(
            *[
                self.make_numbered_row(
                    num, lbl, active=(i == 1), width=9.0, height=0.75
                )
                for i, (num, lbl) in enumerate(steps)
            ]
        )
        rows.arrange(DOWN, buff=0.3)
        rows.next_to(timeline, DOWN, buff=0.65)

        guarantee = Text(
            "no matter where the pair lives, this logic always holds",
            font_size=22,
            color=LABEL_GRAY,
        )
        guarantee.next_to(rows, DOWN, buff=0.4)

        self.play(FadeIn(tag), Write(header), run_time=1.0)
        self.play(FadeIn(elem_a), FadeIn(elem_b), Create(timeline), run_time=1.2)
        self.stagger_in(list(rows), shift=DOWN * 0.1, lag=0.2, run_time=1.5)
        self.play(Write(guarantee), run_time=1.2)
        self.hold(11.0)
        self.clear_scene()

    # - SCENE 18 - Complexity Comparison

    def scene_18_complexity_comparison(self):
        self.gap(14)

        tag = self.corner_label("COMPLEXITY")
        brute = self.make_stat_callout(
            "BRUTE FORCE",
            "O(n²)",
            sub="~1 trillion ops at 1M elements",
            width=5.0,
            height=2.3,
            stroke_color=RED,
            fill_color=SLOW_FILL,
        )
        optimal = self.make_stat_callout(
            "HASH MAP",
            "O(n)",
            sub="n comparisons + n insertions",
            width=5.0,
            height=2.3,
        )

        cards = VGroup(brute, optimal).arrange(RIGHT, buff=1.2)
        cards.next_to(tag, DOWN, buff=0.65).shift(RIGHT * 0.3)

        pipeline = self.make_pipeline(
            ["ONE PASS", "CONSTANT LOOKUP"],
            active_index=1,
            width=2.6,
        )
        pipeline.next_to(cards, DOWN, buff=0.55)

        self.play(FadeIn(tag), FadeIn(brute, shift=RIGHT * 0.15), run_time=1.2)
        self.play(FadeIn(optimal, shift=LEFT * 0.15), run_time=1.2)
        self.play(FadeIn(pipeline), run_time=1.0)
        self.hold(9.0)
        self.clear_scene()

    # - SCENE 19 - Space Complexity

    def scene_19_space_complexity(self):
        self.gap(14)

        tag = self.corner_label("SPACE")
        header = self.spaced_caps("SPACE COMPLEXITY", size=18, color=LABEL_GRAY)
        header.next_to(tag, DOWN, buff=0.45).align_to(tag, LEFT)

        space = Text("O(n)", font_size=64, color=PURP, weight=BOLD)
        space.next_to(header, DOWN, buff=0.55).shift(RIGHT * 0.5)

        trade = self.make_vertical_bar(
            "MEMORY",
            0.55,
            fill_color=PURP,
            label_color=PURP_LIGHT,
        )
        runtime = self.make_vertical_bar(
            "RUNTIME SAVED",
            0.92,
            fill_color=SUCCESS,
            label_color=SUCCESS,
        )
        bars = VGroup(trade, runtime).arrange(RIGHT, buff=0.8)
        bars.next_to(space, DOWN, buff=0.55)

        caption = Text(
            "a little extra memory ↔ dramatically less runtime",
            font_size=22,
            color=LABEL_GRAY,
        )
        caption.next_to(bars, DOWN, buff=0.45)

        self.play(FadeIn(tag), Write(header), run_time=1.0)
        self.play(Write(space), run_time=1.0)
        self.play(
            FadeIn(trade, shift=UP * 0.1), FadeIn(runtime, shift=UP * 0.1), run_time=1.3
        )
        self.write_then_hold(caption, write_time=1.2, hold_time=7.0)
        self.clear_scene()

    # - SCENE 20 - Outro

    def scene_20_outro(self):
        self.gap(14)

        tag = self.corner_label("HABIT OF MIND")
        line1 = Text(
            "what exactly am I looking for?",
            font_size=38,
            color=WHITE,
            weight=BOLD,
        )
        line2 = self.spaced_caps(
            "BUILD A LOOKUP · SEARCH BECOMES TRIVIAL",
            size=15,
            color=PURP_LIGHT,
        )
        content = VGroup(line1, line2).arrange(DOWN, buff=0.65)
        content.move_to(ORIGIN)

        dismiss = Text(
            "the pattern isn't about Two Sum — it's about how you think",
            font_size=22,
            color=LABEL_GRAY,
        )
        dismiss.next_to(content, DOWN, buff=0.55)

        self.play(FadeIn(tag), Write(line1), run_time=2.0)
        self.play(Write(line2), run_time=1.5)
        self.play(FadeIn(dismiss, shift=UP * 0.1), run_time=1.2)
        self.hold(12.0)
        self.clear_scene()
        self.gap(18)
