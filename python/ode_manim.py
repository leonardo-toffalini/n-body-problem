from manim import *
import numpy as np
from scipy.integrate import solve_ivp

"""
y' = f(t, y)
y(t_0) = y_0
"""

# TODO: Make the curves parametric and reutnr a dense output with the doe solver
#       so that the rate at which the curve moves is constant


def n_body(t, z):
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


def sim_nbody(evolution_time: int = 60, method:str ="RK45", step_size_type: str = "adaptive"):
    t_start = 0
    t_stop = evolution_time
    dt = 0.01
    num = int(t_stop / dt)

    #    [m0,  x0,  y0, vx0, vy0, m1,  x1,  y1, vx1,   vy1,  m2, x2, y2, vx2,  vy2]
    y0 = [1,    0,   0,   0,   0,  1,  -2,   0,   0,  0.2,   1,  2,  0,   0, -0.2]
    y0 = [1,    0,   1,   0,   0,  1,  -2,   0,   0,  0.2,   1,  2,  0,   0, -0.2]

    if step_size_type == "fix":
        t_eval = np.linspace(t_start, t_stop, num=num, endpoint=True)
        bodies = solve_ivp(fun=n_body, t_span=(t_start, t_stop), y0=y0, method=method, t_eval=t_eval)
    elif step_size_type == "adaptive":
        # bodies = solve_ivp(fun=n_body, t_span=(t_start, t_stop), y0=y0, method=method, rtol=1e-6)
        bodies = solve_ivp(fun=n_body, t_span=(t_start, t_stop), y0=y0, method="Radau")

    else:
        assert False, "step_size_type must of either 'fix' or 'adaptive'"

    print(f"{method = }, {step_size_type = }, {bodies.y.shape = }")
    return bodies


class NBody(Scene):
    def construct(self):
        evolution_time = 30

        # calculate the solution of the differential equation
        bodies = sim_nbody(evolution_time, method="RK45", step_size_type="adaptive")
        zeros = np.zeros_like(bodies.y[1]).tolist()
        adaptive_points = [
            list(zip(bodies.y[1 + i * 5], bodies.y[2 + i * 5], zeros))
            for i in range(3)
        ]

        bodies_fix = sim_nbody(evolution_time, method="RK45", step_size_type="fix")
        zeros = np.zeros_like(bodies_fix.y[1]).tolist()
        fix_points = [
            list(zip(bodies.y[1 + i * 5], bodies.y[2 + i * 5], zeros))
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
            # curves.add(curve)

        curves.set_stroke(width=2, opacity=1)
        curves.scale(1.8)


        # Play the animations
        show_traces = False
        if show_traces:
            dot1 = Dot(color=BLUE)
            trace1 = TracedPath(dot1.get_center, stroke_width=3, stroke_color=BLUE,
                                dissipating_time=1, stroke_opacity=[0, 1])
            dot2 = Dot(color=RED)
            trace2 = TracedPath(dot2.get_center, stroke_width=3, stroke_color=RED,
                                dissipating_time=1, stroke_opacity=[0, 1])
            dot3 = Dot(color=GREEN)
            trace3 = TracedPath(dot3.get_center, stroke_width=3, stroke_color=GREEN,
                                dissipating_time=1, stroke_opacity=[0, 1])

            self.add(trace1, trace2, trace3)
            self.play(
                *(
                    MoveAlongPath(dot1, curve1),
                    MoveAlongPath(dot2, curve2),
                    MoveAlongPath(dot3, curve3)
                )
                , run_time=evolution_time)

        show_entire_path = True
        if show_entire_path:
            self.play(
                *(
                    Create(curve, rate_func=linear, run_time=evolution_time)
                    for curve in curves
                ),
                run_time=evolution_time
            )
            self.play(curves.animate.scale(0.1).move_to(ORIGIN))
            self.wait(3)




