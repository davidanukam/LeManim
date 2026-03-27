from manim import *


class Combinations(Scene):
    def construct(self):
        # NOTE: Setup
        self.camera.background_color = "#1f1e2e"

        # NOTE: Create stuff from last scene
        list_of_nums = Text("[2, 1, 5, 3]").scale(3).shift(UP * 1.5)
        x_plus_y = MathTex(r"{{ x }} + {{ y }} = {{ 4 }}").scale(2).to_edge(UP)
        self.add(list_of_nums)
        self.add(x_plus_y)

        self.wait(3)
