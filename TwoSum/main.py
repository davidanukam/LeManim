from manim import *

class TwoSum(Scene):
    def construct(self):
        a = Square(2).shift(LEFT * 4)
        b = a.copy().shift(RIGHT * 2)
        c = b.copy().shift(RIGHT * 2)
        d = c.copy().shift(RIGHT * 2)
        e = d.copy().shift(RIGHT * 2)
        nums = VGroup(a, b, c, d, e)
        self.play(Write(nums))
        self.play(nums.animate.scale(0.5))
        self.play(nums.animate.shift(UP * 2))
        
        prevMap = nums.copy()
        
        self.play(prevMap.animate.shift(DOWN * 1.5))
        
        numText = Text("nums").next_to(nums, LEFT)
        self.play(Write(numText))
        
        self.wait()

# class Solution:
#     def twoSum(self, nums: List[int], target: int) -> List[int]:
#         prevMap = {}  # val -> index

#         for i, n in enumerate(nums):
#             diff = target - n
#             if diff in prevMap:
#                 return [prevMap[diff], i]
#             prevMap[n] = i