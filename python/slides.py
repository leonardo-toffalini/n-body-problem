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

class NBodyEq1(Scene):
    eq = MathTex(
        r"x_{i}''(t) = \sum_{i \neq j} m_{j} \frac{\vec{x}_{j} - \vec{x}_{i}}{ \| \vec{x}_{j} - \vec{x}_{i} \|^{3}  }"
    )

    atvitel_elv = MathTex(
        r"""
            x_{i}'(t) &= v_{i}(t) \\
            v_{i}'(t) &= \sum_{i \neq j} m_{j} \frac{\vec{x}_{j} - \vec{x}_{i}}{ \| \vec{x}_{j} - \vec{x}_{i} \|^{3}  }
        """
    )

    def construct(self):
        self.play(Write(self.eq))
        self.wait(1)

class NBodyEq2(NBodyEq1):
    def construct(self):
        self.play(Unwrite(self.eq))
        self.play(Write(self.atvitel_elv))

class Garbonzo(Scene):
    renaming = MathTex(
        r"""
            u_{1} &= x_{1},  &u_{2} = x_{1}', \quad &u_{3} = y_{1},  &u_{4} = y_{1}' \\
            u_{5} &= x_{2},  &u_{6} = x_{2}', \quad &u_{7} = y_{2}, &u_{8} = y_{2}' \\
            u_{9} &= x_{3},  &u_{10} = x_{3}', \quad &u_{11} = y_{3}, &u_{12} = y_{3}'
        """
    )

    first = MathTex(
        r"""
            p_{1x}' &= v_{1x} \\
            v_{1x}' &= m_{2} \frac{p_{2x} - p_{1x}}{r_{21}^{3}} + m_{3} \frac{p_{3x} - p_{1x}}{r_{31}^{3}} \\
            p_{1y}' &= v_{1y} \\
            v_{1y}' &= m_{2} \frac{p_{2y} - p_{1y}}{r_{21}^{3}} + m_{3} \frac{p_{3y} - p_{1y}}{r_{31}^{3}} \\
        """
    )

    second = MathTex(
        r"""
            p_{2x}' &= v_{2x} \\
            v_{2x}' &= m_{1} \frac{p_{1x} - p_{2x}}{r_{21}^{3}} + m_{3} \frac{p_{3x} - p_{2x}}{r_{32}^{3}} \\
            p_{2y}' &= v_{2y} \\
            v_{2y}' &= m_{1} \frac{p_{1y} - p_{2y}}{r_{21}^{3}} + m_{3} \frac{p_{3y} - p_{2y}}{r_{32}^{3}} \\
        """
    )

    third = MathTex(
        r"""
            p_{3x}' &= v_{3x} \\
    v_{3x}' &= m_{1} \frac{p_{1x} - p_{3x}}{r_{31}^{3}} + m_{2} \frac{p_{2x} - p_{3x}}{r_{32}^{3}} \\
            p_{3y}' &= v_{3y} \\
            v_{3y}' &= m_{1} \frac{p_{1y} - p_{3y}}{r_{31}^{3}} + m_{2} \frac{p_{2y} - p_{3y}}{r_{32}^{3}} \\
        """
    )

class Garbonzo1(Garbonzo):
    def construct(self):
        self.play(Write(self.renaming))
        self.wait(1)

class Garbonzo2(Garbonzo):
    def construct(self):
        self.play(Write(self.first))
        self.wait(1)

class Garbonzo3(Garbonzo):
    def construct(self):
        self.play(Write(self.second))
        self.wait(1)

class Garbonzo4(Garbonzo):
    def construct(self):
        self.play(Write(self.third))
        self.wait(1)

