import numpy as np
import matplotlib.pyplot as plt

# Параметры задачи
alpha = 4/(np.pi**2)
L = 2.0
T = 0.5  # общее время моделирования
Nx = 50  # количество узлов по пространству
Nt = 1000  # количество временных шагов
dx = L / (Nx - 1)  # шаг по пространству
dt = T / Nt  # шаг по времени
r = alpha * dt / (dx ** 2) # параметр схемы


# Начальные и граничные условия
def initial_condition(x):
    return np.sin((np.pi/2) * x)


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
    A_new = np.zeros((Nx, Nx))
    b = np.zeros(Nx)
    q = np.zeros(Nx)
    x = np.zeros(Nx)

    for j in range(0, Nx - 1):
        A[j, j+1] = -r
        A[j, j] = 1 + 2 * r
        A[j+1, j] = -r
    A[0, 0] = A[-1, -1] = 1
    A[0, 1] = 0
    A[Nx - 2, Nx - 1] = 0
    A_new[0, 0] = A_new[-1, -1] = 1

    for j in range(0, Nx):
        b[j] = u[j]

    A_new[0, 1] = A[0, 1]/A[0,0]
    for j in range(0, Nx-1):
        A_new[j, j] = 1

    for j in range(1, Nx-1):
        A_new[j, j + 1] = A[j, j + 1]/(A[j, j] - A[j+1, j]*A_new[j-1, j])

    q[0] = b[0]/A[0, 0]
    for j in range(1, Nx-1):
        q[j] = (b[j] - A_new[j + 1, j]*q[j-1])/(A[j, j] - A[j+1, j]*A_new[j-1, j])

    x[-1] = q[-1]
    for i in range(Nx-2, -1, -1):
        x[i] = -A[i, i+1]*x[i+1] + q[i]

    return x


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
plt.xlabel('Position')
plt.ylabel('Temperature')
plt.title('Heat Distribution over time')
plt.legend()
plt.show()
