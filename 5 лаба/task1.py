import numpy as np
import matplotlib.pyplot as plt


# Генерация равномерной сетки
def generate_grid(N):
    h = 1 / (N)  # Шаг сетки
    x = np.linspace(0, 1, N + 1)  # Массив координат с учетом границ
    y = np.linspace(0, 1, N + 1)
    return x, y, h


# Построение матрицы Лапласа
def build_poisson_matrix(N):
    inner_N = N - 1  # Число внутренних узлов
    A = np.zeros((inner_N * inner_N, inner_N * inner_N))

    for i in range(inner_N):
        for j in range(inner_N):
            idx = i * inner_N + j
            A[idx, idx] = 4  # Диагональ

            if j > 0:
                A[idx, idx - 1] = -1  # Левый сосед
            if j < inner_N - 1:
                A[idx, idx + 1] = -1  # Правый сосед
            if i > 0:
                A[idx, idx - inner_N] = -1  # Верхний сосед
            if i < inner_N - 1:
                A[idx, idx + inner_N] = -1  # Нижний сосед
    print('matrix A:\n ', A)
    return A


# Построение правой части уравнения
def build_rhs(N, h, f, g):
    rhs = np.zeros((N - 1, N - 1))
    x, y = np.linspace(h, 1, N), np.linspace(h, 1, N)

    # Вклад от функции f
    for i in range(N - 1):
        for j in range(N - 1):
            rhs[i, j] = f(x[i], y[j]) * h**2

    # Влияние граничных условий
    for i in range(N - 1):
        rhs[i, 0] += g(0, y[i])  # Левая граница
        rhs[i, -1] += g(1, y[i])  # Правая граница
        rhs[0, i] += g(x[i], 0)  # Нижняя граница
        rhs[-1, i] += g(x[i], 1)  # Верхняя граница
    #print(rhs.ravel(), '---------')
    #print('h = ', h)

    return rhs.ravel()


# Метод Якоби
def jacobi_method(A, b, tol=1e-4, max_iter=1000000000):
    x = np.zeros_like(b, dtype=float)
    D = np.diag(A)
    R = A - np.diagflat(D)

    for _ in range(max_iter):
        x_new = (b - R @ x) / D
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new
        x = x_new

    raise ValueError("Метод Якоби не сошелся")


# Метод Зейделя
def gauss_seidel_method(A, b, tol=1e-4, max_iter=1000000000):
    x = np.zeros_like(b, dtype=float)

    for _ in range(max_iter):
        x_new = np.copy(x)
        for i in range(len(b)):
            s1 = np.dot(A[i, :i], x_new[:i])
            s2 = np.dot(A[i, i + 1:], x[i + 1:])
            x_new[i] = (b[i] - s1 - s2) / A[i, i]

        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new
        x = x_new

    raise ValueError("Метод Зейделя не сошелся")


# Решение уравнения Пуассона
def solve_poisson(N, f, g, method="jacobi"):
    x, y, h = generate_grid(N)
    A = build_poisson_matrix(N)
    b = build_rhs(N, h, f, g)

    if method == "jacobi":
        u = jacobi_method(A, b)
    elif method == "gauss_seidel":
        u = gauss_seidel_method(A, b)
    else:
        raise ValueError("Неизвестный метод")

    u_full = np.zeros((N + 1, N + 1))
    u_full[1:-1, 1:-1] = u.reshape((N - 1, N - 1))
    u_full[0, :] = g(x, 0)
    u_full[-1, :] = g(x, 1)
    u_full[:, 0] = g(0, y)
    u_full[:, -1] = g(1, y)

    return u_full, x, y


# Визуализация решения
def plot_heatmap(u, x, y):
    plt.figure(figsize=(8, 6))
    plt.imshow(u, extent=(x[0], x[-1], y[0], y[-1]), origin='lower', cmap='hot', aspect='auto')
    plt.colorbar(label='Решение u(x, y)')
    plt.title('Решение уравнения Пуассона')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()


def runge_error(N, f, g, method="jacobi"):
    # Решаем уравнение на трех сетках: h, h/2, h/4
    u_h, _, _ = solve_poisson(N, f, g, method)
    u_h2, _, _ = solve_poisson(2 * N, f, g, method)
    u_h4, _, _ = solve_poisson(4 * N, f, g, method)

    u_h_inner = u_h[1:-1, 1:-1]  # Размер (N-1, N-1)


    u_h2_down = u_h2[2:-2:2, 2:-2:2]
    u_h4_down = u_h4[4:-4:4, 4:-4:4]

    norm_h = np.linalg.norm(u_h2_down - u_h_inner)
    norm_h2 = np.linalg.norm(u_h4_down - u_h2_down)

    if norm_h2 > 0:
        order = np.log2(norm_h / norm_h2)
        return abs(order)
    else:
        return None


# Основной блок программы
if __name__ == "__main__":
    N = 16
    f = lambda x, y: 1
    g = lambda x, y: x + y

    u_jacobi, x, y = solve_poisson(N, f, g, method="jacobi")
    order_jacobi = runge_error(N, f, g, method="jacobi")
    print(f"Порядок сходимости метода Якоби: {order_jacobi}")
    print("Решение методом Якоби:")
    plot_heatmap(u_jacobi, x, y)

    u_gauss_seidel, x, y = solve_poisson(N, f, g, method="gauss_seidel")
    order_gauss_seidel = runge_error(N, f, g, method="gauss_seidel")
    print(f"Порядок сходимости метода Зейделя: {order_gauss_seidel}")
    print("Решение методом Зейделя:")
    plot_heatmap(u_gauss_seidel, x, y)