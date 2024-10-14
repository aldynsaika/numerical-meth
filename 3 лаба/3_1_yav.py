import numpy as np
import matplotlib.pyplot as plt


alpha = 4/(np.pi**2)
L = 2.0
T = 0.5
Nx = 50
Nt = 1000
dx = L / (Nx - 1)
dt = T / Nt
r = alpha * dt / (dx ** 2)


def initial_condition(x):
    return np.sin((np.pi/2) * x)


def boundary_conditions(u):
    u[0] = 0
    u[-1] = 0

# Решение явной схемой
def explicit_scheme(u0, r, Nt, Nx):
    u = u0.copy()
    u_history = np.zeros((Nt, Nx))
    u_new = u.copy()

    for n in range(Nt):
        for j in range(1, Nx - 1):
            u_new[j] = u[j] + r * (u[j + 1] - 2 * u[j] + u[j - 1])
        boundary_conditions(u_new)
        u = u_new.copy()
        u_history[n] = u.copy()

    return u_history


x = np.linspace(0, L, Nx)

u0 = initial_condition(x)

u_history_explicit = explicit_scheme(u0, r, Nt, Nx)

plt.figure(figsize=(10, 6))
plt.imshow(u_history_explicit, aspect='auto', extent=[0, L, T, 0], origin='upper', cmap='hot')
plt.colorbar(label='Temperature')
plt.xlabel('Position')
plt.ylabel('Time')
plt.title('Explicit Scheme')
plt.show()
