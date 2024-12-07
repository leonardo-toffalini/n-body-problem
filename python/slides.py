from manim import *

class TwoBodies(Scene):
    def construct(self):
        planet1 = Circle(radius=1, color=BLUE, fill_opacity=0.8)
        planet2 = Circle(radius=1, color=BLUE, fill_opacity=0.8)

        planet1.move_to(3*RIGHT)
        planet2.move_to(3*LEFT)
        mass1 = MathTex(r"m_1").move_to(planet1.get_center() + 0.5*RIGHT)
        mass2 = MathTex(r"m_2").move_to(planet2.get_center() + 0.5*LEFT)

        line = Line(planet1.get_center(), planet2.get_center()).set_color(GREEN).set_opacity(0.6)
        brace = Brace(line).move_to(2*DOWN)
        brace_text = brace.get_tex(r"r_{12}")

        force1 = Arrow(start=planet1.get_center(), end=RIGHT, color=RED).set_opacity(0.8)
        force2 = Arrow(start=planet2.get_center(), end=LEFT, color=RED).set_opacity(0.8)
        force1_text = MathTex(r"F").next_to(force1.get_end(), 0.6*UP)
        force2_text = MathTex(r"F").next_to(force2.get_end(), 0.6*UP)

        eq = MathTex(
            r"F = \gamma \cdot \frac{m_1 \cdot m_2}{r_{12}^2}"
        ).move_to(3*UP)
        framebox = SurroundingRectangle(eq, buff = .1)

        self.add(planet1, planet2)
        self.play(Write(mass1))
        self.play(Write(mass2))

        self.play(Create(brace))
        self.play(Write(brace_text))

        self.play(Create(force1))
        self.play(Create(force2))
        self.play(Write(force1_text))
        self.play(Write(force2_text))
        self.wait(1)

        self.play(Write(eq))

        self.play(Create(framebox))
        self.wait(1)
        self.play(Uncreate(framebox))
        self.wait(1)
