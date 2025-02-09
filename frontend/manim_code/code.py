from manim import *

config.media_dir = "frontend/videos"

from manim import *


class DynamicScene(Scene):
    def construct(self):
        # Title
        title = Text("Quick Sort").to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Introduction to the concept
        intro_text = (
            Text(
                "Quick Sort is a sorting algorithm that uses divide and conquer to sort an array."
            )
            .scale(0.5)
            .move_to(UP * 2)
        )
        self.play(Write(intro_text))
        self.wait(2)

        # Example array
        array = [3, 7, 8, 5, 2, 1, 9, 5, 4]
        array_text = Text("Array: " + str(array)).scale(0.5).move_to(UP * 1.5)
        self.play(Write(array_text))
        self.wait(2)

        # Step-by-step quick sort visualization
        self.play(FadeOut(intro_text))

        # Initial array visualization
        array_mob = (
            VGroup(*[Text(str(num)).scale(0.5) for num in array])
            .arrange(RIGHT, buff=0.5)
            .move_to(DOWN)
        )
        self.play(Write(array_mob))
        self.wait(1)

        # Quick sort steps
        def quick_sort(arr, low, high):
            if low < high:
                pi = partition(arr, low, high)
                quick_sort(arr, low, pi - 1)
                quick_sort(arr, pi + 1, high)

        def partition(arr, low, high):
            i = low - 1
            pivot = arr[high]
            for j in range(low, high):
                if arr[j] <= pivot:
                    i = i + 1
                    arr[i], arr[j] = arr[j], arr[i]
                    self.play(Swap(array_mob[i], array_mob[j]))
                    self.wait(0.5)
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            self.play(Swap(array_mob[i + 1], array_mob[high]))
            self.wait(0.5)
            return i + 1

        quick_sort(array, 0, len(array) - 1)
        self.wait(2)

        # Conclusion text
        conclusion_text = (
            Text("Sorted Array: " + str(array)).scale(0.5).move_to(DOWN * 2)
        )
        self.play(Write(conclusion_text))
        self.wait(2)

        # Clean up the scene
        self.play(FadeOut(array_text), FadeOut(array_mob), FadeOut(conclusion_text))
        self.wait(1)

        # End of scene
        self.play(FadeOut(title))
        self.wait(1)
