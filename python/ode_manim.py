from manim import *
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

"""
y' = f(t, y)
y(t_0) = y_0
"""

# TODO: Make the curves parametric and reutnr a dense output with the doe solver
#       so that the rate at which the curve moves is constant


def three_body(t, z):
    [m0, x0, y0, vx0, vy0, m1, x1, y1, vx1, vy1, m2, x2, y2, vx2, vy2] = z

    # calculate distances
    r01 = np.sqrt( (x0 - x1)**2 + (y0 - y1)**2 )
    r02 = np.sqrt( (x0 - x2)**2 + (y0 - y2)**2 )
    r12 = np.sqrt( (x1 - x2)**2 + (y1 - y2)**2 )

    # calculate accelerations
    ax0 = m1 * (x1 - x0)/(r01 ** 3) + m2 * (x2 - x0)/(r02 ** 3)
    ay0 = m1 * (y1 - y0)/(r01 ** 3) + m2 * (y2 - y0)/(r02 ** 3)
    ax1 = m0 * (x0 - x1)/(r01 ** 3) + m2 * (x2 - x1)/(r12 ** 3)
    ay1 = m0 * (y0 - y1)/(r01 ** 3) + m2 * (y2 - y1)/(r12 ** 3)
    ax2 = m0 * (x0 - x2)/(r02 ** 3) + m1 * (x1 - x2)/(r12 ** 3)
    ay2 = m0 * (y0 - y2)/(r02 ** 3) + m1 * (y1 - y2)/(r12 ** 3)

    #      [m0,  x0,  y0, vx0, vy0, m1,  x1,  y1, vx1, vy1, m2,  x2,  y2, vx2, vy2]
    return [ 0, vx0, vy0, ax0, ay0,  0, vx1, vy1, ax1, ay1,  0, vx2, vy2, ax2, ay2]

def two_body(t, z):
    [m0, x0, y0, vx0, vy0, m1, x1, y1, vx1, vy1] = z

    # calculate distances
    r = np.sqrt( (x0 - x1)**2 + (y0 - y1)**2 )

    # calculate accelerations
    ax0 = m1 * (x1 - x0)/(r ** 3)
    ay0 = m1 * (y1 - y0)/(r ** 3)
    ax1 = m0 * (x0 - x1)/(r ** 3)
    ay1 = m0 * (y0 - y1)/(r ** 3)

    #      [m0,  x0,  y0, vx0, vy0, m1,  x1,  y1, vx1, vy1]
    return [ 0, vx0, vy0, ax0, ay0,  0, vx1, vy1, ax1, ay1]


def sim_three_body(evolution_time: int = 60, method:str ="RK45", step_size_type: str = "adaptive"):
    t_start = 0
    t_stop = evolution_time
    dt = 0.01
    num = int(t_stop / dt)

    m0, m1, m2 = 1, 1, 1
    pos0 = [-1.5, 0]
    vel0 = [0, 0.2]
    pos1 = [0, 0]
    vel1 = [0, 0]
    pos2 = [1.5, 0]
    vel2 = [0, -0.2]
    y0 = [m0] + pos0 + vel0
    y0.append(m1)
    y0 = y0 + pos1 + vel1
    y0.apend(m2)
    y0 = y0 + pos2 + vel2
    #    [m0,  x0,  y0, vx0, vy0, m1,  x1,  y1, vx1,   vy1,  m2, x2, y2, vx2,  vy2]
    # y0 = [1,    0,   0,   0,   0,  1,  -2,   0,   0,  0.2,   1,  2,  0,   0, -0.2]
    # y0 = [1, -1.5,   0,   0, 0.2,  1,   0,   0,   0,     0,   1, 1.5,  0,   0,   -0.2]

    if step_size_type == "fix":
        t_eval = np.linspace(t_start, t_stop, num=num, endpoint=True)
        bodies = solve_ivp(fun=three_body, t_span=(t_start, t_stop), y0=y0, method=method, t_eval=t_eval)
    elif step_size_type == "adaptive":
        # bodies = solve_ivp(fun=n_body, t_span=(t_start, t_stop), y0=y0, method=method, rtol=1e-6)
        bodies = solve_ivp(fun=three_body, t_span=(t_start, t_stop), y0=y0, method="RK45", rtol=1e-5)

    else:
        assert False, "step_size_type must of either 'fix' or 'adaptive'"

    print(f"{method = }, {step_size_type = }, {bodies.y.shape = }")
    return bodies, bodies.y.shape[-1]

def sim_two_body(evolution_time: int = 60):
    t_start = 0
    t_stop = evolution_time

    #    [m0, x0, y0, vx0, vy0, m1, x1, y1, vx1, vy1]
    y0 = [ 3, -1,  0,   0, -0.9, 3,  1,  0,   0, 0.9]
    bodies = solve_ivp(fun=two_body, t_span=(t_start, t_stop), y0=y0, rtol=1e-5)
    print(f"{bodies.y.shape = }")
    return bodies

def get_energy(z):
    # 2-body
    if len(z) == 10:
        [m0, x0, y0, vx0, vy0, m1, x1, y1, vx1, vy1] = z
        # 0.5 * m * v^2
        kinetic = 0.5 * m0 * (vx0**2 + vy0**2) + 0.5 * m1 * (vx1**2 + vy1**2)
        r = np.sqrt( (x0 - x1)**2 + (y0 - y1)**2 )
        potential = - m0 * m1 / r
        return kinetic + potential

    # 3-body
    elif len(z) == 15:
        raise NotImplementedError

    else:
        assert False


class ThreeBodyDiffMethods(Scene):
    def construct(self):
        evolution_time = 30

        # calculate the solution of the differential equation
        bodies_adaptive, num_points_adaptive = sim_three_body(evolution_time, step_size_type="adaptive")
        zeros = np.zeros_like(bodies_adaptive.y[1]).tolist()
        adaptive_points = [
            list(zip(bodies_adaptive.y[1 + i * 5], bodies_adaptive.y[2 + i * 5], zeros))
            for i in range(3)
        ]

        bodies_fix, num_points_fix = sim_three_body(evolution_time, method="RK45", step_size_type="fix")
        zeros = np.zeros_like(bodies_fix.y[1]).tolist()
        fix_points = [
            list(zip(bodies_fix.y[1 + i * 5], bodies_fix.y[2 + i * 5], zeros))
            for i in range(3)
        ]

        # create a vector group to cold the curves drawn by the planets
        curves = VGroup()

        # adaptive step size method curves
        for points in adaptive_points:
            curve = VMobject().set_points_smoothly(points)
            curve.set_stroke(BLUE)
            curves.add(curve)

        # fix step size method curves
        for points in fix_points:
            curve = VMobject().set_points_smoothly(points)
            curve.set_stroke(RED)
            curves.add(curve)

        curves.set_stroke(width=2, opacity=1)
        curves.scale(1.8)

        adaptive_text = MathTex(
            rf"\text{{RK45}} \\ \text{{num points}} = {num_points_adaptive}",
            color=BLUE
        ).to_corner(UL)
        fix_text = MathTex(
            rf"\text{{RK4}} \\ \text{{num points}} = {num_points_fix}",
            color=RED
        ).to_corner(UR)

        # Play the animations
        self.play(Write(adaptive_text), Write(fix_text))
        self.play(
            *(
                Create(curve, rate_func=linear, run_time=evolution_time)
                for curve in curves
            ),
            run_time=evolution_time
        )
        self.play(curves.animate.scale(1.5).move_to(ORIGIN))
        self.wait(3)


class TwoBody(Scene):
    def construct(self):
        evolution_time = 30

        # calculate the solution of the differential equation
        bodies = sim_two_body(evolution_time)
        energies = [get_energy(z) for z in zip(*bodies.y)]
        zeros = np.zeros_like(bodies.y[1]).tolist()
        sols = [
            list(zip(bodies.y[1 + i * 5], bodies.y[2 + i * 5], zeros))
            for i in range(2)
        ]

        # create a vector group to cold the curves drawn by the planets
        curves = VGroup()

        for points in sols:
            curve = VMobject().set_points_smoothly(points)
            curve.set_stroke(BLUE)
            curves.add(curve)


        curves.set_stroke(width=2, opacity=1)
        curves.scale(1.8)


        # Play the animations
        self.play(
            *(
                Create(curve, rate_func=linear, run_time=evolution_time)
                for curve in curves
            ),
            run_time=evolution_time
        )
        self.play(curves.animate.scale(1.5).move_to(ORIGIN))
        self.wait(3)

        plt.plot(energies)
        plt.show()


