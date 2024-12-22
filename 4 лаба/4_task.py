import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return 1 / (1 + 25 * x**2)


def lagrange_basis(x, xi, i):
    L = 1
    for j in range(len(xi)):
        if j != i:
            L *= (x - xi[j]) / (xi[i] - xi[j])
    return L


def lagrange_polynomial(x, xi, yi):
    P = 0
    for i in range(len(xi)):
        P += yi[i] * lagrange_basis(x, xi, i)
    return P


a, b = -1, 1

N1 = 5
N2 = 20

xi1 = np.linspace(a, b, N1 + 1)
yi1 = f(xi1)

xi2 = np.linspace(a, b, N2 + 1)
yi2 = f(xi2)

xi_chebyshev_5 = np.cos((2 * np.arange(N1 + 1) + 1) / (2 * (N1 + 1)) * np.pi)
xi_chebyshev_20 = np.cos((2 * np.arange(N2 + 1) + 1) / (2 * (N2 + 1)) * np.pi)

xi_chebyshev_5 = 0.5 * (b - a) * (xi_chebyshev_5 + 1) + a
xi_chebyshev_20 = 0.5 * (b - a) * (xi_chebyshev_20 + 1) + a

yi_chebyshev_5 = f(xi_chebyshev_5)
yi_chebyshev_20 = f(xi_chebyshev_20)

x_plot = np.linspace(a, b, 500)
y_exact = f(x_plot)

y_lagrange_5_chebyshev = [lagrange_polynomial(x, xi_chebyshev_5, yi_chebyshev_5) for x in x_plot]
y_lagrange_20_chebyshev = [lagrange_polynomial(x, xi_chebyshev_20, yi_chebyshev_20) for x in x_plot]

y_lagrange_5 = [lagrange_polynomial(x, xi1, yi1) for x in x_plot]
y_lagrange_20 = [lagrange_polynomial(x, xi2, yi2) for x in x_plot]

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(x_plot, y_exact, label="Точная функция $f(x)$", color="black")
plt.plot(x_plot, y_lagrange_5, label="Полином Лагранжа (N=5)", color="red")
plt.scatter(xi1, yi1, color="red", label="Узлы интерполяции")
plt.title("Полином Лагранжа (5 степень)")
plt.xlabel("$x$")
plt.ylabel("$f(x)$")
plt.legend()
plt.grid()

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


plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(x_plot, y_exact, label="Точная функция $f(x)$", color="black")
plt.plot(x_plot, y_lagrange_5_chebyshev, label="Полином Лагранжа (Чебышёв, N=5)", color="green")
plt.scatter(xi_chebyshev_5, yi_chebyshev_5, color="green", label="Узлы Чебышёва")
plt.title("Полином Лагранжа (узлы Чебышёва, 5 степень)")
plt.xlabel("$x$")
plt.ylabel("$f(x)$")
plt.legend()
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(x_plot, y_exact, label="Точная функция $f(x)$", color="black")
plt.plot(x_plot, y_lagrange_20_chebyshev, label="Полином Лагранжа (Чебышёв, N=20)", color="purple")
plt.scatter(xi_chebyshev_20, yi_chebyshev_20, color="purple", label="Узлы Чебышёва")
plt.title("Полином Лагранжа (узлы Чебышёва, 20 степень)")
plt.xlabel("$x$")
plt.ylabel("$f(x)$")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
