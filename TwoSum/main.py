from manim import *
from intro import Intro
from combinations import Combinations

import sys

ADD_SOUND = "--sound" in sys.argv


class TwoSum(Scene):
    def construct(self):
        # NOTE: Audio
        if ADD_SOUND:
            self.add_sound("audio/TwoSum_1Min.wav")

        # NOTE: Setup
        self.camera.background_color = "#1f1e2e"

        # NOTE: Scenes
        Intro.construct(self)
        Combinations.construct(self)
