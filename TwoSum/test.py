from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService  # For AI placeholder

# from manim_voiceover.services.recorder import RecorderService # For recording live


class VoiceoverExample(VoiceoverScene):
    def construct(self):
        # 1. Set up your speech service
        self.set_speech_service(GTTSService())

        circle = Circle()
        square = Square()

        # 2. Wrap your animations in a voiceover block
        with self.voiceover(text="This is a circle, drawn in real-time.") as tracker:
            self.play(Create(circle))
            # The scene will automatically wait until the audio finishes!

        with self.voiceover(text="Now, watch it transform into a square.") as tracker:
            self.play(ReplacementTransform(circle, square))

        self.wait(1)
