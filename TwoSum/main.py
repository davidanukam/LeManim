from manim import *


class TwoSum(Scene):
    def construct(self):
        # Inside your Manim Scene
        # self.add_sound("TwoSum.mp3")
        self.camera.background_color = "#1f1e2e"

        # Intro
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

        # Draw question marks onto screen
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

        # Transform question mark to list of numbers
        list_of_nums = Text("[2, 1, 5, 3]").scale(3)
        self.play(
            ReplacementTransform(question_mark, list_of_nums),
            FadeOut(question_mark_left),
            FadeOut(question_mark_right),
        )
        self.play(Indicate(list_of_nums))
        self.wait()
        self.play(list_of_nums.animate.shift(UP * 2))

        # Create target equation
        x_plus_y = MathTex("x + y = 4").scale(3).shift(DOWN)
        self.play(Write(x_plus_y))
        self.wait()

        # Add pause icon
        pause = (
            Triangle(color=WHITE)
            .set_fill(WHITE, 1)
            .set_opacity(0.5)
            .shift(RIGHT * 0.25)
            .scale(2)
            .rotate(-PI / 2)
        )  # -90 deg
        self.play(GrowFromCenter(pause))

        # title = Text("Two Sum", font_size=40).scale(2)

        # rec1 = Rectangle(WHITE, 1.5, 5).scale(2).set_fill(color="#0A0A0F", opacity=0)
        # nums_temp_label = Tex("nums").scale(2).shift(LEFT * 2.85, DOWN * 0.05)
        # nums_label = Tex("nums = [2, 1, 5, 3]").scale(2)
        # target_label = Tex("target = 4").scale(2).shift(DOWN)

        # arrow1 = (
        #     Arrow(start=DOWN, end=UP, buff=0.5)
        #     .next_to(nums_label, DOWN)
        #     .shift(RIGHT * 1.35)
        #     .set_fill(PURE_RED)
        #     .set_color(PURE_RED)
        # )

        # arrow2 = (
        #     Arrow(start=DOWN, end=UP, buff=0.5)
        #     .next_to(nums_label, DOWN)
        #     .shift(RIGHT * 3.65)
        #     .set_fill(PURE_BLUE)
        #     .set_color(PURE_BLUE)
        # )

        # self.play(Write(title))
        # self.play(title.animate.scale(0.5).to_edge(UP), Create(rec1))

        # self.play(rec1.animate.set_fill(color="#0A0A0F", opacity=1), Write(nums_label))
        # self.play(Create(arrow1), Create(arrow2))

        # temp_s = (
        #     Square(2)
        #     .set_fill("#0A0A0F", 1)
        #     .set_color("#0A0A0F")
        #     .shift(LEFT * 3)
        #     .scale(1.25)
        # )
        # self.add(temp_s, nums_temp_label)
        # self.play(FadeOut(arrow1), FadeOut(arrow2), Indicate(nums_temp_label))
        # self.remove(temp_s, nums_temp_label)

        # indi_circle = Circle(0.3, PURE_RED).scale(2).shift(RIGHT * 1.375)
        # indi_circle2 = Circle(0.3, PURE_RED).scale(2).shift(RIGHT * 3.55)
        # self.play(Create(indi_circle), Create(indi_circle2))
        # self.play(Indicate(indi_circle, color=None), Indicate(indi_circle2, color=None))
        # self.play(FadeOut(indi_circle), FadeOut(indi_circle2))

        # nums_label_group_1 = VGroup(rec1, nums_label)
        # self.play(FadeOut(title), nums_label_group_1.animate.shift(UP * 2))

        # num1 = Tex("1").shift(RIGHT * 1.4).scale(2).shift(UP * 2.075)
        # num3 = Tex("3").shift(RIGHT * 3.6).scale(2).shift(UP * 2.075)

        # num_group1 = VGroup(num1, num3)

        # self.add(num1, num3)
        # self.play(
        #     num1.animate.shift(DOWN * 3.075, LEFT * 3),
        #     num3.animate.shift(DOWN * 3.075, LEFT * 3),
        # )

        # sum1 = Tex("1 + 3 = ").scale(2).move_to(num_group1)
        # ans1 = Tex("4").scale(2).next_to(sum1, RIGHT)

        # self.play(ReplacementTransform(num_group1, sum1))
        # self.play(Write(ans1))
        # self.play(Indicate(ans1))
        # self.play(FadeOut(sum1))
        # self.play(ReplacementTransform(ans1, target_label))

        # self.wait()

        # NOTE: Later
        # self.play(num1.animate.shift(DOWN * 2), num3.animate.shift(DOWN * 2))

        # # Create Array Visual
        # nums = [2, 1, 5, 3]
        # array_boxes = (
        #     VGroup(*[Square(side_length=1) for _ in range(len(nums))])
        #     .arrange(RIGHT, buff=0.1)
        #     .shift(UP * 0.5)
        # )
        # array_vals = VGroup(*[Text(str(n)) for n in nums])
        # for i, val in enumerate(array_vals):
        #     val.move_to(array_boxes[i].get_center())

        # indices = VGroup(
        #     *[Text(str(i), font_size=20, color=GRAY) for i in range(len(nums))]
        # )
        # for i, index in enumerate(indices):
        #     index.next_to(array_boxes[i], DOWN, buff=0.1)

        # self.play(Create(array_boxes), Write(array_vals), Write(indices))

        # # Hash Map Setup
        # hash_map_title = Text(
        #     "prevMap {val : index}", font_size=28, color=YELLOW
        # ).shift(LEFT * 3 + DOWN * 1.5)
        # hash_map_box = Rectangle(height=2, width=4).next_to(hash_map_title, DOWN)
        # map_content = VGroup().move_to(hash_map_box.get_center())

        # self.play(Create(hash_map_box), Write(hash_map_title))

        # # Logic Display
        # calc_text = Text("Complement = target - n", font_size=24).shift(
        #     RIGHT * 3 + DOWN * 1
        # )
        # calc_val = Text("", font_size=30, color=BLUE).next_to(calc_text, DOWN)

        # self.play(Write(calc_text))

        # # Iteration Pointer
        # pointer = Arrow(UP, DOWN, color=RED).scale(0.5).next_to(array_boxes[0], UP)

        # # Step through logic
        # target = 4
        # prevMap = {}

        # for i, n in enumerate(nums):
        #     self.play(pointer.animate.next_to(array_boxes[i], UP))

        #     diff = target - n
        #     new_calc_val = Text(
        #         f"{target} - {n} = {diff}", font_size=30, color=BLUE
        #     ).move_to(calc_val)

        #     self.play(Transform(calc_val, new_calc_val))
        #     self.wait(1)

        #     if diff in prevMap:
        #         # Success state
        #         self.play(Indicate(array_boxes[i], color=GREEN))
        #         # Highlight the found complement in the map
        #         match_text = [m for m in map_content if f"{diff}:" in m.text][0]
        #         self.play(Indicate(match_text, color=GREEN))

        #         success_msg = Text("Match Found!", color=GREEN).shift(DOWN * 3)
        #         self.play(Write(success_msg))
        #         self.wait(2)
        #         break
        #     else:
        #         # Add to map
        #         prevMap[n] = i
        #         new_entry = Text(f"{n}: {i}", font_size=24).arrange(RIGHT)

        #         if len(map_content) == 0:
        #             new_entry.move_to(hash_map_box.get_top() + DOWN * 0.4)
        #         else:
        #             new_entry.next_to(map_content, DOWN, buff=0.2)

        #         map_content.add(new_entry)
        #         self.play(Write(new_entry))
        #         self.wait(1)

        # self.play(FadeOut(pointer), FadeOut(calc_text), FadeOut(calc_val))

        # # Complexity Summary
        # complexity = (
        #     VGroup(Text("Time: O(n)", color=GOLD), Text("Space: O(n)", color=GOLD))
        #     .arrange(DOWN)
        #     .to_edge(RIGHT, buff=1)
        # )

        # self.play(Write(complexity))
        self.wait(3)
