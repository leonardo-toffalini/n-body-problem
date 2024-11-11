from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

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



m0, m1, m2 = [1], [1], [1]
pos0 = [-1.5, 0]
vel0 = [0, 0.2]
pos1 = [0, 0]
vel1 = [0, 0]
pos2 = [1.5, 0]
vel2 = [0, -0.2]
y0 = m0 + pos0 + vel0 + m1 + pos1 + vel1 + m2 + pos2 + vel2



bodies = solve_ivp(fun=three_body, t_span=(0, 10), y0=y0, rtol=1e-5)
sols = np.array([
    list(zip(bodies.y[1 + i * 5], bodies.y[2 + i * 5]))
    for i in range(3)
])

print(sols[0].shape)
plt.plot(sols[0, :, 0], sols[0, :, 1], c="deepskyblue")
plt.plot(sols[1, :, 0], sols[1, :, 1], c="lightskyblue")
plt.plot(sols[2, :, 0], sols[2, :, 1], c="skyblue")
plt.show()

