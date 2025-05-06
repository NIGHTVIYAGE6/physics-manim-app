from manim import *

class TestScene(Scene):
    def construct(self):
        dot = Dot(radius=0.1, color=BLUE).move_to(UP*5)
        text = Tex("Free Fall").next_to(dot, UP)

        self.play(Write(text))
        self.play(FadeIn(dot))

        trajectory = VMobject()
        trajectory.start_new_path(dot.get_center())
        
        for t in range(0, 60):
            y = 5 - 9.8 * (t / 60)**2 / 2
            if y < 0:
                y = 0
            new_point = np.array([0, y, 0])
            trajectory.add_line_to(new_point)
            self.play(dot.animate.move_to(new_point), run_time=1/60, rate_func=linear)
        
        self.play(dot.animate.set_color(RED))
        self.wait()