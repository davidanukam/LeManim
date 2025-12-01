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
        
        self.play(prevMap.animate.shift(DOWN * 2))
        
        numText = Text("nums").next_to(nums, LEFT)
        self.play(Write(numText))
        
        num1 = Text("16").move_to(nums[0], ORIGIN)
        num2 = Text("8").move_to(nums[1], ORIGIN)
        num3 = Text("23").move_to(nums[2], ORIGIN)
        num4 = Text("4").move_to(nums[3], ORIGIN)
        num5 = Text("15").move_to(nums[4], ORIGIN)
        
        self.play(Write(num1))
        self.play(Write(num2))
        self.play(Write(num3))
        self.play(Write(num4))
        self.play(Write(num5))
        
        targetText = Text("target:").shift(DOWN * 2)
        self.play(Write(targetText))
        
        target = Text("19").next_to(targetText, RIGHT)
        self.play(Write(target))
        
        self.play(targetText.animate.shift(RIGHT * 4, UP * 4), target.animate.shift(RIGHT * 4, UP * 4))
        
        self.wait()

# class Solution:
#     def twoSum(self, nums: List[int], target: int) -> List[int]:
#         prevMap = {}  # val -> index

#         for i, n in enumerate(nums):
#             diff = target - n
#             if diff in prevMap:
#                 return [prevMap[diff], i]
#             prevMap[n] = i