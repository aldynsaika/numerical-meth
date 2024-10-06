import numpy as np
import matplotlib.pyplot as plt

# Параметры задачи
alpha = 0.01  # коэффициент теплопроводности
L = 1.0  # длина стержня
T = 0.5  # общее время моделирования
Nx = 50  # количество узлов по пространству
Nt = 1000  # количество временных шагов
dx = L / (Nx - 1)  # шаг по пространству
dt = T / Nt  # шаг по времени
r = alpha * dt / dx ** 2  # параметр схемы


# Начальные и граничные условия
def initial_condition(x):
    return np.sin(np.pi * x)


def boundary_conditions(u, t):
    u[0] = 0  # температура на левом конце
    u[-1] = 0  # температура на правом конце


# Решение явной схемой
def explicit_scheme(u0, r, Nt, Nx):
    u = u0.copy()
    u_new = np.zeros_like(u)

    for n in range(Nt):
        for j in range(1, Nx - 1):
            u_new[j] = u[j] + r * (u[j + 1] - 2 * u[j] + u[j - 1])
        boundary_conditions(u_new, n * dt)
        u = u_new.copy()

    return u


# Решение неявной схемой (метод прогонки)
def implicit_scheme(u0, r, Nt, Nx):
    u = u0.copy()
    A = np.zeros((Nx, Nx))
    b = np.zeros(Nx)

    # Матрица коэффициентов для неявной схемы
    for j in range(1, Nx - 1):
        A[j, j - 1] = -r
        A[j, j] = 1 + 2 * r
        A[j, j + 1] = -r
    A[0, 0] = A[-1, -1] = 1  # Граничные условия

    for n in range(Nt):
        b[1:-1] = u[1:-1]
        b[0] = b[-1] = 0  # Граничные условия
        u = np.linalg.solve(A, b)

    return u


# Пространственная сетка
x = np.linspace(0, L, Nx)

# Начальное распределение температуры
u0 = initial_condition(x)

# Решение явной схемой
u_explicit = explicit_scheme(u0, r, Nt, Nx)

# Решение неявной схемой
u_implicit = implicit_scheme(u0, r, Nt, Nx)

# Графики
plt.plot(x, u0, label='Initial Condition')
plt.plot(x, u_explicit, label='Explicit Scheme')
plt.plot(x, u_implicit, label='Implicit Scheme')
plt.xlabel('Position along the rod')
plt.ylabel('Temperature')
plt.title('Heat Distribution over time')
plt.legend()
plt.show()
