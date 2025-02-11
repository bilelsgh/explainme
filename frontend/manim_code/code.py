from manim import *

config.media_dir = "frontend/videos"

from manim import *


class DynamicScene(Scene):
    def construct(self):
        # Initial list
        initial_list = [1, 5, -9, 25, -98, 547, 3, 6, -87]
        list_mob = [Tex(str(num)).scale(0.8) for num in initial_list]

        # Arrange list items horizontally
        list_group = VGroup(*list_mob).arrange(RIGHT, buff=1)
        list_group.move_to(UP)

        # Display initial list
        self.play(FadeIn(list_group))
        self.wait(1)

        # Merge sort function
        def merge_sort(arr):
            if len(arr) <= 1:
                return arr
            mid = len(arr) // 2
            left = merge_sort(arr[:mid])
            right = merge_sort(arr[mid:])
            return merge(left, right)

        def merge(left, right):
            sorted_list = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    sorted_list.append(left[i])
                    i += 1
                else:
                    sorted_list.append(right[j])
                    j += 1
            sorted_list.extend(left[i:])
            sorted_list.extend(right[j:])
            return sorted_list

        # Animate merge sort
        def animate_merge_sort(arr):
            if len(arr) <= 1:
                return arr
            mid = len(arr) // 2
            left = animate_merge_sort(arr[:mid])
            right = animate_merge_sort(arr[mid:])
            return animate_merge(left, right)

        def animate_merge(left, right):
            sorted_list = []
            i = j = 0
            left_mob = [Tex(str(num)).scale(0.8) for num in left]
            right_mob = [Tex(str(num)).scale(0.8) for num in right]
            left_group = (
                VGroup(*left_mob).arrange(RIGHT, buff=1).move_to(UP * 2 + LEFT * 3)
            )
            right_group = (
                VGroup(*right_mob).arrange(RIGHT, buff=1).move_to(UP * 2 + RIGHT * 3)
            )

            self.play(
                Transform(list_group, left_group),
                Transform(list_group.copy(), right_group),
            )
            self.wait(1)

            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    sorted_list.append(left[i])
                    self.play(
                        left_group[i].animate.move_to(
                            list_group[len(sorted_list) - 1].get_center()
                        )
                    )
                    i += 1
                else:
                    sorted_list.append(right[j])
                    self.play(
                        right_group[j].animate.move_to(
                            list_group[len(sorted_list) - 1].get_center()
                        )
                    )
                    j += 1
                self.wait(0.5)

            while i < len(left):
                sorted_list.append(left[i])
                self.play(
                    left_group[i].animate.move_to(
                        list_group[len(sorted_list) - 1].get_center()
                    )
                )
                i += 1
                self.wait(0.5)

            while j < len(right):
                sorted_list.append(right[j])
                self.play(
                    right_group[j].animate.move_to(
                        list_group[len(sorted_list) - 1].get_center()
                    )
                )
                j += 1
                self.wait(0.5)

            self.play(FadeOut(left_group), FadeOut(right_group))
            return sorted_list

        # Perform merge sort animation
        sorted_list = animate_merge_sort(initial_list)

        # Display sorted list
        sorted_list_mob = [Tex(str(num)).scale(0.8) for num in sorted_list]
        sorted_list_group = VGroup(*sorted_list_mob).arrange(RIGHT, buff=1).move_to(UP)
        self.play(Transform(list_group, sorted_list_group))
        self.wait(2)

        # Clean up
        self.play(FadeOut(list_group))
        self.wait(1)
