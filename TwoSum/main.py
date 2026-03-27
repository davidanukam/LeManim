from manim import *

import sys

ADD_SOUND = "--sound" in sys.argv


class TwoSum(Scene):
    def construct(self):
        # NOTE: Start audio and setup scene
        if ADD_SOUND:
            self.add_sound("audio/TwoSum_1Min.wav")

        self.camera.background_color = "#1f1e2e"

        # NOTE: Intro
        question_mark_left = (
            Text("?", font_size=50)
            .scale(2)
            .shift(LEFT * 1.5)
            .set_fill(opacity=0)
            .set_stroke(color=WHITE, width=2)
        )
        question_mark = Text("?", font_size=50).scale(5).shift(DOWN * 6)
        question_mark_right = (
            Text("?", font_size=50)
            .scale(2.5)
            .shift(RIGHT * 1.5)
            .set_fill(opacity=0)
            .set_stroke(color=WHITE, width=2)
        )

        # NOTE: Draw question marks onto screen
        self.add(question_mark)
        self.play(Write(question_mark_left))
        self.play(Write(question_mark_right))
        self.play(
            question_mark.animate.move_to(ORIGIN),
            question_mark_left.animate.shift(LEFT).scale(2).rotate(0.436332),  # 25 deg
            question_mark_right.animate.shift(RIGHT)
            .scale(1.5)
            .rotate(-0.523599),  # -30 deg
        )
        self.wait()

        # NOTE: Transform question mark to list of numbers
        list_of_nums = Text("[2, 1, 5, 3]").scale(3)
        self.play(
            ReplacementTransform(question_mark, list_of_nums),
            FadeOut(question_mark_left),
            FadeOut(question_mark_right),
        )
        self.wait(0.25)
        self.play(Indicate(list_of_nums))
        self.wait(0.25)
        self.play(list_of_nums.animate.shift(UP * 2))

        # NOTE: Create target equation
        x_plus_y = MathTex(r"{{ x }} + {{ y }} = {{ 4 }}").scale(3).shift(DOWN)
        self.play(Write(x_plus_y))
        self.wait(0.75)

        # NOTE: Add pause icon
        pause = (
            Triangle(color=WHITE)
            .set_fill(WHITE, 1)
            .set_opacity(0.5)
            .shift(RIGHT * 0.25)
            .scale(2)
            .rotate(-PI / 2)  # -90 deg
        )
        self.play(GrowFromCenter(pause), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(pause))

        # Note: Show the obvious answer
        x_plus_y_ans = MathTex(r"{{ 1 }} + {{ 3 }} = {{ 4 }}").scale(3).shift(DOWN)
        self.wait(3)
        self.play(
            Indicate(list_of_nums[3], color=RED),
            Indicate(list_of_nums[7], color=RED),
        )
        self.play(ReplacementTransform(x_plus_y, x_plus_y_ans))
        self.wait()

        # NOTE: Surround the x and y
        x_plus_y = MathTex(r"{{ x }} + {{ y }} = {{ 4 }}").scale(3).shift(DOWN)
        self.play(ReplacementTransform(x_plus_y_ans, x_plus_y))

        surr_rcct1 = SurroundingRectangle(x_plus_y[0])
        surr_rcct2 = SurroundingRectangle(x_plus_y[2])

        self.wait(2.5)
        self.play(Create(surr_rcct1), Create(surr_rcct2))
        self.play(Indicate(surr_rcct1), Indicate(surr_rcct2))
        self.play(FadeOut(surr_rcct1), FadeOut(surr_rcct2))

        # NOTE: Shrink and move equation
        self.wait()
        self.play(x_plus_y.animate.shift(UP * 1.25).scale(2 / 3))

        # NOTE: Add Dumb and Smart Emojis
        dumb_emoji = SVGMobject("assets/NaiveEmoji.svg").shift(LEFT * 3)
        arr = Arrow(start=LEFT, end=RIGHT).scale(2)
        smart_emoji = SVGMobject("assets/SmartEmoji.svg").shift(RIGHT * 3)

        dumb_to_smart = VGroup(dumb_emoji, arr, smart_emoji)
        dumb_to_smart.shift(DOWN * 1.5)

        self.play(Write(dumb_emoji), run_time=1)
        self.play(Write(arr), run_time=1)
        self.play(Write(smart_emoji), run_time=1)

        # NOTE: Move screen stuff to left
        self.wait(0.5)
        temp_screen = VGroup(list_of_nums, x_plus_y, dumb_to_smart)
        self.play(temp_screen.animate.shift(LEFT * 3.75).scale(2 / 3), run_time=0.5)

        div_line = Line(start=DOWN * 4, end=UP * 4)
        self.play(Create(div_line))

        # NOTE: Add the One Million with an X
        one_mil = Text("1,000,000").scale(2).shift(RIGHT * 3.5)
        cross1 = (
            Line(start=DOWN * 2, end=UP * 2, color=PURE_RED, stroke_width=3)
            .move_to(one_mil)
            .rotate(-PI / 4)  # -45 deg
        )
        cross2 = (
            Line(start=DOWN * 2, end=UP * 2, color=PURE_RED, stroke_width=3)
            .move_to(one_mil)
            .rotate(PI / 4)  # 45 deg
        )

        self.play(Write(one_mil))
        self.play(Create(cross1), Create(cross2))

        self.wait(0.5)
        self.play(FadeOut(one_mil), FadeOut(cross1), FadeOut(cross2))

        # NOTE: Add the first 45 numbers
        nums = VGroup(
            *[Text(f"{num:>2}", font="Consolas", font_size=36) for num in range(1, 46)]
        )
        nums[0].to_edge(UP, buff=1).shift(RIGHT * 1.5)
        self.play(Write(nums[0]), run_time=0.3)

        for i in range(1, len(nums)):
            current_num = nums[i]

            if i % 5 == 0:
                current_num.next_to(nums[i - 5], DOWN, buff=0.5, aligned_edge=RIGHT)
            else:
                prev_num = nums[i - 1]
                current_num.next_to(prev_num, RIGHT, buff=0.8)

            self.play(Write(current_num), run_time=0.05)
        self.wait(0.5)
        self.play(FadeOut(nums), FadeOut(div_line), run_time=0.5)

        # NOTE: Move screen stuff back to middle
        self.play(temp_screen.animate.shift(RIGHT * 3.75).scale(3 / 2), run_time=0.5)
        self.play(FadeOut(dumb_to_smart))

        # NOTE: Show Brain and Lightbulb
        brain = SVGMobject("assets/Brain.svg").shift(DOWN * 2)
        self.play(Write(brain), run_time=1)

        self.wait(3)
