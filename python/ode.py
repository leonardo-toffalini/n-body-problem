import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

"""
y' = f(t, y)
y(t_0) = y_0
"""


def n_body(t, z):
    [m0, x0, y0, vx0, vy0, m1, x1, y1, vx1, vy1, m2, x2, y2, vx2, vy2] = z

    r01 = np.sqrt( (x0 - x1)**2 + (y0 - y1)**2 )
    r02 = np.sqrt( (x0 - x2)**2 + (y0 - y2)**2 )
    r12 = np.sqrt( (x1 - x2)**2 + (y1 - y2)**2 )

    ax0 = m1 * (x1 - x0)/(r01 ** 3) + m2 * (x2 - x0)/(r02 ** 3)
    ay0 = m1 * (y1 - y0)/(r01 ** 3) + m2 * (y2 - y0)/(r02 ** 3)
    ax1 = m0 * (x0 - x1)/(r01 ** 3) + m2 * (x2 - x1)/(r12 ** 3)
    ay1 = m0 * (y0 - y1)/(r01 ** 3) + m2 * (y2 - y1)/(r12 ** 3)
    ax2 = m0 * (x0 - x2)/(r02 ** 3) + m1 * (x1 - x2)/(r12 ** 3)
    ay2 = m0 * (y0 - y2)/(r02 ** 3) + m1 * (y1 - y2)/(r12 ** 3)

         # [m0,  x0,  y0, vx0, vy0, m1,  x1,  y1, vx1, vy1, m2,  x2,  y2, vx2, vy2]
    return [ 0, vx0, vy0, ax0, ay0,  0, vx1, vy1, ax1, ay1,  0, vx2, vy2, ax2, ay2]



def ode(f, y0, h=1e-3, t_range=(0, 1)):
    t0 = t_range[0]
    num_steps = int(t_range[1] // h)
    y = [y0]
    for i in range(num_steps):
        y.append(y[-1] + h * f(t0 + i * h, y[-1]))

    return y


def f_exp(t, y):
    return y
# e = ode(f_exp, 1)

t_start = 0
t_stop = 10
t_eval = np.linspace(start=t_start, stop=t_stop, num=1000, endpoint=True)
e = solve_ivp(fun=f_exp, t_span=(t_start, t_stop), y0=[1], t_eval=t_eval)

   # [m0,  x0,  y0, vx0, vy0, m1,  x1,  y1, vx1, vy1, m2,  x2,  y2, vx2, vy2]
y0 = [1,    0,   0,   0,   0,  1,   1,   0,   0,   1,  1,   0,  -1,   0,   -1]
bodies = solve_ivp(fun=n_body, t_span=(t_start, t_stop), y0=y0, t_eval=t_eval)
print(bodies.y.shape)

plt.plot(bodies.y[1], bodies.y[2], color="r")
plt.plot(bodies.y[6], bodies.y[7], color="b")
plt.plot(bodies.y[11], bodies.y[12], color="g")
plt.show()


# plt.plot(e.y[0])
# plt.show()

