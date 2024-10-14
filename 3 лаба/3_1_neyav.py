import numpy as np
import matplotlib.pyplot as plt

alpha = 4 / (np.pi ** 2)
L = 2.0
T = 1
Nx = 50
Nt = 1000
dx = L / (Nx - 1)
dt = T / Nt
r = alpha * dt / (dx ** 2)


def analytical_solution(x, t):
    return np.sin((np.pi/2)*x*np.exp(-1*t))


def initial_condition(x):
    return np.sin((np.pi / 2) * x)


def boundary_conditions(u):
    u[0] = 0
    u[-1] = 0


def diag_algorithm(a, b, c, d):
    n = len(d)
    c_ = np.zeros(n)
    d_ = np.zeros(n)
    c_[0] = c[0] / b[0]
    d_[0] = d[0] / b[0]

    for i in range(1, n):
        curr = b[i] - a[i - 1] * c_[i - 1]
        c_[i] = c[i-1] / curr
        d_[i] = (d[i] - a[i - 1] * d_[i - 1]) / curr

    x = np.zeros(n)
    x[-1] = d_[-1]

    for i in range(n - 2, -1, -1):
        x[i] = d_[i] - c_[i] * x[i + 1]

    return x


def implicit_scheme(u0, r, Nt, Nx):
    u = u0.copy()
    u_history = np.zeros((Nt, Nx))

    a = -r * np.ones(Nx - 1)
    b = (1 + 2 * r) * np.ones(Nx)
    c = -r * np.ones(Nx - 1)
    b[0] = 1
    b[-1] = 1
    c[-1] = 0
    a[0] = 0

    for n in range(Nt):
        d = u.copy()
        x1 = np.linalg.norm(d)
        boundary_conditions(d)
        u = diag_algorithm(a, b, c, d)
        u_history[n] = u.copy()

    return u_history

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
    for i in u_history:
        print(i)
    # print(u_history[-1, 24])
    print(np.linalg.norm(u_history[-1]))
    return u_history


x = np.linspace(0, L, Nx)
t_values = np.linspace(0, T, Nt)


u0 = initial_condition(x)
print(*u0)

u_history_implicit = implicit_scheme(u0, r, Nt, Nx)

u_history_explicit = explicit_scheme(u0, r, Nt, Nx)

u_analytical = np.array([[analytical_solution(xi, t) for xi in x] for t in t_values])

print("ошибка =", abs(np.linalg.norm(u_history_implicit[24])-np.linalg.norm(u_analytical[24]))/np.linalg.norm(u_analytical[24]))
print("ошибка =", abs(np.linalg.norm(u_history_explicit[24])-np.linalg.norm(u_analytical[24]))/np.linalg.norm(u_analytical[24]))

relative_error_L2_implicit = np.zeros(Nt)
relative_error_L2_explicit = np.zeros(Nt)

t_star = 0.25

t_index = np.argmin(np.abs(t_values - t_star))

u_implicit_t_star = u_history_implicit[t_index]
u_explicit_t_star = u_history_explicit[t_index]
u_analytical_t_star = u_analytical[t_index]

plt.figure(figsize=(10, 6))
plt.plot(x, u_implicit_t_star, label='Implicit Scheme', color='b')
plt.plot(x, u_explicit_t_star, label='Explicit Scheme', color='r', linestyle='--')
plt.xlabel('Position x')
plt.ylabel(f'Solution at t = {t_star}')
plt.title(f'Solution at t = {t_star} (Implicit & Explicit)')
plt.legend()
plt.grid(True)
plt.show()

print("пусть при t = 0.5")
print((np.linalg.norm(u_history_implicit[-1] - np.linalg.norm(u_analytical[-1])**2))**0.5/np.linalg.norm(u_analytical[-1])**2)

for n in range(Nt):
    norm_diff_implicit = np.linalg.norm(u_history_implicit[n] - u_analytical[n])
    norm_analytical = np.linalg.norm(u_analytical[n])
    if norm_analytical != 0:
        relative_error_L2_implicit[n] = norm_diff_implicit / norm_analytical
    else:
        relative_error_L2_implicit[n] = 0

for n in range(Nt):
    norm_diff_explicit = np.linalg.norm(u_history_explicit[n] - u_analytical[n])
    norm_analytical = np.linalg.norm(u_analytical[n])
    if norm_analytical != 0:
        relative_error_L2_explicit[n] = norm_diff_explicit / norm_analytical
    else:
        relative_error_L2_explicit[n] = 0


# plt.figure(figsize=(10, 6))
# plt.imshow(u_history_implicit, aspect='auto', extent=[0, L, T, 0], origin='upper', cmap='hot')
# plt.colorbar(label='Temperature')
# plt.xlabel('Position')
# plt.ylabel('Time')
# plt.title('Implicit Scheme')
# plt.show()
#
# plt.figure(figsize=(10, 6))
# plt.yscale('log')
# plt.plot(t_values, relative_error_L2_implicit, label='Implicit Scheme L2 Error', color='b')
# plt.plot(t_values, relative_error_L2_explicit, label='Explicit Scheme L2 Error', color='r', linestyle='--')
# plt.xlabel('Time')
# plt.ylabel('Relative Error (L2 norm)')
# plt.title('Relative L2 Error over Time (Implicit vs Explicit)')
# plt.legend()
# plt.grid(True)
# plt.show()
