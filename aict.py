import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib import animation
import sympy as sym
import matplotlib.patches as patches
g = sym.symbols('g')
l = sym.symbols('l')
m = sym.symbols('m')
t = sym.symbols('t')
theta = sym.symbols('\u03B8', cls=sym.Function)
theta = theta(t)
x = l * sym.sin(theta)
y = -l * sym.cos(theta)
# Kinetic energy
T = sym.Rational(1, 2) * m * (x.diff(t) **2 + y.diff(t) **2)

# Potential energy
V = m * g * y
L = T - V

LE = (sym.diff(sym.diff(L, sym.diff(theta, t)), t) - sym.diff(L, theta)).simplify()
sol = sym.solve(LE, sym.diff(theta, t, t), simplify=False, rational=False)

#printing the oridnary differential eq for angle
#here theta is angle and alpha is angular acceleration
print("\n\ndifferential equation of simple pendulum system:")
print("\u03B1=",sol[0],'\n')

sol_f = sym.lambdify((t, theta, sym.diff(theta, t), g, l, m), sol[0])
def dSdt(S, t, g, l, m):
    theta, omega = S
    dtheta_dt = omega
    domega_dt = sol_f(t, theta, omega, g, l, m)
    return dtheta_dt, domega_dt
t = np.linspace(0, 50, 2001)

theta0_deg = float(input("Enter inital angle (in degrees): "))
theta0 = np.deg2rad(theta0_deg)   # convert to radians

theta_dot0 = float(input("Enter initial angular velocity (rad/s): "))
g = 9.81
l = float(input("Enter length of pendulum (in meters): "))
m = float(input("Enter mass of pendulum (in kg): "))
ans = odeint(dSdt, (theta0, theta_dot0), t, args=(g, l, m))

# Plot of the position and velocity of the pendulum
fig, ax = plt.subplots(1, 1, figsize=(11, 11))
ax.plot(t, ans[:, 0])
ax.set_xlabel('Time (s)')
ax.set_ylabel('Angle (rad)')
fig, bx = plt.subplots(1, 1, figsize=(11, 11))
bx.plot(t, ans[:, 1])
bx.set_xlabel('Time (s)')
bx.set_ylabel('Angular velocity (rad/s)')

fig, ax = plt.subplots(1, 1, figsize=(10, 5))
x_values, y_values = np.meshgrid(np.linspace(-10, 10, 20), np.linspace(-10, 10, 20))
u_values = y_values
v_values = -g/l * np.sin(x_values)
ax.streamplot(x_values, y_values, u_values, v_values)
ax.set_xlabel('Angle (rad)')
ax.set_ylabel('Angular velocity (rad/s)')
ax.grid()
fig, ax = plt.subplots(1, 1, figsize=(10, 5))
x_values, y_values = np.meshgrid(np.linspace(-10, 10, 20), np.linspace(-10, 10, 20))
u_values = y_values
v_values = -g/l * np.sin(x_values)
ax.streamplot(x_values, y_values, u_values, v_values)
ax.set_xlabel('Angle (rad)')
ax.set_ylabel('Angular velocity (rad/s)')
ax.grid()
plt.show()
def get_x_y(theta, l):
    x = l * np.sin(theta)
    y = -l * np.cos(theta)
    return x, y

# Animation of the pendulum
fig, ax = plt.subplots(figsize=(5, 5))
ax.set_xlim(-l-1, l+1)
ax.set_ylim(-l-1, l+1)
ax.set_aspect('equal')
ax.grid()

line, = ax.plot([], [],'-', lw=2,color= 'brown')
bob = patches.Circle((0, 0), 0.09, fc='grey', ec='grey', zorder=3)
ax.add_patch(bob)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

# X and Y coordinates of the pendulum
x, y = get_x_y(ans[:, 0], l)

def init():
    line.set_data([], [])
    time_text.set_text('')
    bob.center=(0,0)
    return line,bob, time_text

def animate(i):
    thisx = [0, x[i]]
    thisy = [0, y[i]]
    bob.center = (x[i], y[i])
    line.set_data(thisx, thisy)
    time_text.set_text(time_template % (i * t[1]))
    return line,bob, time_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(ans)),
                                interval=25, blit=True, init_func=init)

plt.rcParams['animation.embed_limit'] = 100
plt.show()