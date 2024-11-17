import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return 1 / (1 + 25 * x**2)


def lagrange_basis(x, xi, i):
    """
    Вычисление i-го базисного полинома Лагранжа L_i(x) для заданного x
    """
    L = 1
    for j in range(len(xi)):
        if j != i:
            L *= (x - xi[j]) / (xi[i] - xi[j])
    return L


def lagrange_polynomial(x, xi, yi):
    """
    Вычисление полинома Лагранжа P_N(x) для заданного x
    """
    P = 0
    for i in range(len(xi)):
        P += yi[i] * lagrange_basis(x, xi, i)
    return P


# Интервал
a, b = -1, 1

# Узлы интерполяции для полиномов степени 5 и 20
N1 = 5
N2 = 20

# Узлы и значения функции
xi1 = np.linspace(a, b, N1 + 1)
yi1 = f(xi1)

xi2 = np.linspace(a, b, N2 + 1)
yi2 = f(xi2)

# Точки для построения графика
x_plot = np.linspace(a, b, 500)
y_exact = f(x_plot)

# Полиномы Лагранжа
y_lagrange_5 = [lagrange_polynomial(x, xi1, yi1) for x in x_plot]
y_lagrange_20 = [lagrange_polynomial(x, xi2, yi2) for x in x_plot]

# Построение графиков
plt.figure(figsize=(12, 6))

# Полином 5 степени
plt.subplot(1, 2, 1)
plt.plot(x_plot, y_exact, label="Точная функция $f(x)$", color="black")
plt.plot(x_plot, y_lagrange_5, label="Полином Лагранжа (N=5)", color="red")
plt.scatter(xi1, yi1, color="red", label="Узлы интерполяции")
plt.title("Полином Лагранжа (5 степень)")
plt.xlabel("$x$")
plt.ylabel("$f(x)$")
plt.legend()
plt.grid()

# Полином 20 степени
plt.subplot(1, 2, 2)
plt.plot(x_plot, y_exact, label="Точная функция $f(x)$", color="black")
plt.plot(x_plot, y_lagrange_20, label="Полином Лагранжа (N=20)", color="blue")
plt.scatter(xi2, yi2, color="blue", label="Узлы интерполяции")
plt.title("Полином Лагранжа (20 степень)")
plt.xlabel("$x$")
plt.ylabel("$f(x)$")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
