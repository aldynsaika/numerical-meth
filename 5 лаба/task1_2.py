import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Генерация равномерной сетки
def generate_grid(N):
    h = 1 / (N - 1)  # Шаг сетки
    x = np.linspace(0, 1, N)  # Массив координат с учетом границ
    y = np.linspace(0, 1, N)
    return x, y, h

# Построение матрицы Лапласа
def build_poisson_matrix(N):
    inner_N = N - 2  # Число внутренних узлов
    A = np.zeros((inner_N * inner_N, inner_N * inner_N))

    for i in range(inner_N):
        for j in range(inner_N):
            idx = i * inner_N + j
            A[idx, idx] = -4  # Диагональ

            if j > 0:
                A[idx, idx - 1] = 1  # Левый сосед
            if j < inner_N - 1:
                A[idx, idx + 1] = 1  # Правый сосед
            if i > 0:
                A[idx, idx - inner_N] = 1  # Верхний сосед
            if i < inner_N - 1:
                A[idx, idx + inner_N] = 1  # Нижний сосед
    return A

# Построение правой части уравнения
def build_rhs(N, h, f, g):
    rhs = np.zeros((N - 2, N - 2))
    x, y = np.linspace(h, 1 - h, N - 2), np.linspace(h, 1 - h, N - 2)

    # Вклад от функции f
    for i in range(N - 2):
        for j in range(N - 2):
            rhs[i, j] = f(x[i], y[j]) * h**2

    # Влияние граничных условий
    for i in range(N - 2):
        rhs[i, 0] -= g(0, y[i])  # Левая граница
        rhs[i, -1] -= g(1, y[i])  # Правая граница
        rhs[0, i] -= g(x[i], 0)  # Нижняя граница
        rhs[-1, i] -= g(x[i], 1)  # Верхняя граница

    return rhs.ravel()

# Метод Якоби
def jacobi_method(A, b, tol=1e-6, max_iter=10000):
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
def gauss_seidel_method(A, b, tol=1e-6, max_iter=10000):
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

    u_full = np.zeros((N, N))
    u_full[1:-1, 1:-1] = u.reshape((N - 2, N - 2))

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

def compute_local_convergence_order(N, f, g, method="jacobi"):
    # Решаем уравнение на сетках с шагами h и h/2
    u_h, x_h, y_h = solve_poisson(N, f, g, method)
    u_h2, x_h2, y_h2 = solve_poisson(N // 2 + 1, f, g, method)

    # Создаем координаты для интерполяции
    x_full_h2, y_full_h2 = np.meshgrid(x_h2[1:-1], y_h2[1:-1])

    # Интерполяция u_h на сетку u_h2
    points_h = np.array([(x_h[i], y_h[j]) for i in range(N) for j in range(N)])
    values_h = u_h.flatten()
    u_h_interp = griddata(points_h, values_h, (x_full_h2, y_full_h2), method='linear')

    # Проверяем размеры массивов
    print(f"Размеры u_h2: {u_h2.shape}, u_h_interp: {u_h_interp.shape}")

    # Вычисляем локальный порядок сходимости
    local_order = []
    for i in range(u_h2.shape[0]):
        for j in range(u_h2.shape[1]):
            norm_diff = np.abs(u_h2[i, j] - u_h_interp[i, j])
            if norm_diff > 0:  # Избегаем деления на ноль
                # Определяем, есть ли следующий элемент для сравнения
                if i + 1 < u_h2.shape[0]:
                    order = np.log2(norm_diff / np.abs(u_h2[i, j] - u_h2[i + 1, j]))
                    local_order.append(order)

    return np.mean(local_order) if local_order else None

# Основной блок программы
if __name__ == "__main__":
    N = 10
    f = lambda x, y: 1
    g = lambda x, y: x + y

    u_jacobi, x, y = solve_poisson(N, f, g, method="jacobi")
    order_jacobi = compute_local_convergence_order(N, f, g, method="jacobi")
    print(f"Локальный порядок сходимости метода Якоби: {order_jacobi}")
    print("Решение методом Якоби:")
    plot_heatmap(u_jacobi, x, y)

    u_gauss_seidel, x, y = solve_poisson(N, f, g, method="gauss_seidel")
    order_gauss_seidel = compute_local_convergence_order(N, f, g, method="gauss_seidel")
    print(f"Локальный порядок сходимости метода Зейделя: {order_gauss_seidel}")
    print("Решение методом Зейделя:")
    plot_heatmap(u_gauss_seidel, x, y)
