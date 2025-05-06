from manim import *

class TestScene(Scene):
    def construct(self):
        dot = Dot().set_color(RED).shift(UP*3)
        text = Tex("自由落体").next_to(dot, UP)

        self.play(Write(text))
        self.play(FadeIn(dot))

        trajectory = VMobject()
        trajectory.set_points_as_corners([dot.get_center(), dot.get_center()])

        self.add(trajectory)

        for _ in range(180):
            new_point = dot.get_center() + DOWN * 0.1
            trajectory.add_line_to(new_point)
            self.wait(1 / 30)  # simulate time step
            self.play(dot.animate.move_to(new_point), run_time=1/30, rate_func=linear)